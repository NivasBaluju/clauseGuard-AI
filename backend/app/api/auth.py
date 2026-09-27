import os
import uuid
import datetime
import jwt
from flask import Blueprint, request, jsonify, g, make_response
from app.extensions import db
from app.models.user import User, Session
from app.middleware.auth import require_auth, get_jwt_secret
from app.utils.password_policy import (
    validate_password,
    hash_password,
    verify_password,
    verify_dummy_password,
)
from app.services.audit_service import log_audit_event

auth_bp = Blueprint("auth", __name__)


def get_cookie_kwargs():
    is_prod = os.environ.get("FLASK_ENV") == "production"
    return {
        "httponly": True,
        "secure": is_prod,
        "samesite": "Lax",
        "max_age": 7 * 24 * 60 * 60,  # 7 days in seconds
        "path": "/",
    }

# 1. REGISTER
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if not email or not isinstance(email, str):
        return jsonify({"error": "Valid email is required", "field": "email"}), 400

    clean_email = email.strip().lower()
    if "@" not in clean_email or len(clean_email) > 255:
        return jsonify({"error": "Valid email is required", "field": "email"}), 400

    clean_name = name.strip() if name and isinstance(name, str) else clean_email.split("@")[0]

    # Validate password rules
    pw_check = validate_password(password, confirm_password)
    if not pw_check["valid"]:
        return jsonify({"error": pw_check["reason"], "field": "password"}), 400

    # Check if user already exists
    existing = User.query.filter_by(email=clean_email).first()
    if existing:
        return jsonify({"error": "An account with this email already exists", "field": "email"}), 400

    # Hash password & save user
    password_hash = hash_password(password)
    user = User(
        name=clean_name,
        email=clean_email,
        password_hash=password_hash,
        role="user",
    )
    db.session.add(user)
    db.session.commit()

    # Create session
    session_obj = Session(
        user_id=user.id,
        ip=request.remote_addr,
        device_fingerprint=request.headers.get("User-Agent", "")[:250],
        revoked=False,
    )
    db.session.add(session_obj)
    db.session.commit()

    # Sign JWT (valid for 7 days)
    jwt_secret = get_jwt_secret()
    payload = {
        "sessionId": str(session_obj.id),
        "userId": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    # Record audit log
    log_audit_event(
        action="USER_REGISTER",
        user_id=user.id,
        user_email=user.email,
        resource_type="user",
        resource_id=str(user.id),
        details={"name": user.name, "role": user.role}
    )

    response = make_response(jsonify({
        "ok": True,
        "token": token,
        "user": user.to_dict(),
    }), 201)

    response.set_cookie("token", token, **get_cookie_kwargs())
    return response

# 2. LOGIN
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    clean_email = email.strip().lower()
    user = User.query.filter_by(email=clean_email).first()

    if not user or not user.password_hash:
        # Prevents timing attack / user enumeration
        verify_dummy_password(password)
        log_audit_event(
            action="LOGIN_FAILED",
            user_email=clean_email,
            details={"reason": "User not found"}
        )
        return jsonify({"error": "Invalid email or password"}), 401

    if not verify_password(password, user.password_hash):
        log_audit_event(
            action="LOGIN_FAILED",
            user_id=user.id,
            user_email=user.email,
            details={"reason": "Invalid password"}
        )
        return jsonify({"error": "Invalid email or password"}), 401

    # Create new session
    session_obj = Session(
        user_id=user.id,
        ip=request.remote_addr,
        device_fingerprint=request.headers.get("User-Agent", "")[:250],
        revoked=False,
    )
    db.session.add(session_obj)
    db.session.commit()

    jwt_secret = get_jwt_secret()
    payload = {
        "sessionId": str(session_obj.id),
        "userId": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    # Record audit log
    log_audit_event(
        action="USER_LOGIN",
        user_id=user.id,
        user_email=user.email,
        resource_type="session",
        resource_id=str(session_obj.id),
        details={"ip": request.remote_addr, "userAgent": request.headers.get("User-Agent", "")[:100]}
    )

    response = make_response(jsonify({
        "ok": True,
        "token": token,
        "user": user.to_dict(),
    }), 200)

    response.set_cookie("token", token, **get_cookie_kwargs())
    return response

# 3. CURRENT USER (/me)
@auth_bp.route("/auth/me", methods=["GET"])
@require_auth
def get_current_user():
    return jsonify({
        "ok": True,
        "user": g.user.to_dict(),
    }), 200

# 4. LOGOUT
@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    # If authenticated, revoke session
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif request.cookies.get("token"):
        token = request.cookies.get("token")

    if token:
        try:
            payload = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])
            session_id = payload.get("sessionId")
            user_id = payload.get("userId")
            if session_id:
                session_obj = db.session.get(Session, session_id)
                if session_obj:
                    session_obj.revoked = True
                    db.session.commit()
            log_audit_event(
                action="USER_LOGOUT",
                user_id=user_id,
                resource_type="session",
                resource_id=str(session_id)
            )
        except Exception:
            pass

    response = make_response(jsonify({"ok": True, "message": "Signed out successfully"}), 200)
    response.set_cookie("token", "", expires=0, path="/", httponly=True)
    return response

