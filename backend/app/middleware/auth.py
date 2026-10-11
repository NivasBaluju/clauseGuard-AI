import jwt
from functools import wraps
from flask import request, jsonify, g, current_app
from app.extensions import db
from app.models.user import User, Session

def get_jwt_secret():
    if current_app:
        return current_app.config.get("JWT_SECRET") or current_app.config.get("SECRET_KEY") or "deciva-super-secret-jwt-key-change-in-production"
    return "deciva-super-secret-jwt-key-change-in-production"

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif request.cookies.get("token"):
            token = request.cookies.get("token")
        elif request.args.get("token"):
            token = request.args.get("token")
        elif request.args.get("auth_token"):
            token = request.args.get("auth_token")

        if not token:
            return jsonify({"error": "Authentication required. No token provided."}), 401

        jwt_secret = get_jwt_secret()
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except Exception:
            resp = jsonify({"error": "Invalid or expired session token."})
            resp.set_cookie("token", "", expires=0, path="/", httponly=True)
            return resp, 401

        session_id = payload.get("sessionId")
        user_id = payload.get("userId")

        if not user_id:
            resp = jsonify({"error": "Invalid token payload."})
            resp.set_cookie("token", "", expires=0, path="/", httponly=True)
            return resp, 401

        if session_id:
            session_obj = db.session.get(Session, session_id)
            if session_obj and session_obj.revoked:
                resp = jsonify({"error": "Session has been revoked or expired."})
                resp.set_cookie("token", "", expires=0, path="/", httponly=True)
                return resp, 401
            g.session = session_obj

        user_obj = db.session.get(User, user_id)
        if not user_obj:
            return jsonify({"error": "User no longer exists."}), 401

        g.user = user_obj
        return f(*args, **kwargs)
    return decorated_function

def optional_auth(f):
    """Optionally attaches g.user and g.session if a valid token is present."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.user = None
        g.session = None
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif request.cookies.get("token"):
            token = request.cookies.get("token")
        elif request.args.get("token"):
            token = request.args.get("token")
        elif request.args.get("auth_token"):
            token = request.args.get("auth_token")

        if token:
            jwt_secret = get_jwt_secret()
            try:
                payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
                session_id = payload.get("sessionId")
                user_id = payload.get("userId")
                if user_id:
                    user_obj = db.session.get(User, user_id)
                    if user_obj:
                        if session_id:
                            session_obj = db.session.get(Session, session_id)
                            if session_obj and not session_obj.revoked:
                                g.session = session_obj
                                g.user = user_obj
                            elif not session_obj:
                                g.user = user_obj
                        else:
                            g.user = user_obj
            except Exception:
                pass
        return f(*args, **kwargs)
    return decorated_function
