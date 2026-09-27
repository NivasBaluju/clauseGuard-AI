import logging
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.audit_log import AuditLog
from app.middleware.auth import optional_auth, require_auth
from app.services.audit_service import log_audit_event

logger = logging.getLogger(__name__)
audit_bp = Blueprint("audit", __name__)

@audit_bp.route("/audit", methods=["GET"])
@optional_auth
def get_audit_logs():
    """
    Retrieves recent audit logs for the current user or system.
    Supports filtering by action, resource_type, and pagination.
    """
    try:
        user = getattr(g, "user", None)
        limit = min(int(request.args.get("limit", 100)), 500)
        offset = int(request.args.get("offset", 0))
        action_filter = request.args.get("action")
        resource_type = request.args.get("resource_type")

        if not user:
            return jsonify({
                "total": 0,
                "logs": [],
                "limit": limit,
                "offset": offset
            }), 200

        query = AuditLog.query

        # Restrict strictly to user's own logs (by user_id or user_email)
        if getattr(user, "role", "user") != "admin":
            query = query.filter((AuditLog.user_id == user.id) | (AuditLog.user_email == user.email))

        if action_filter:
            query = query.filter(AuditLog.action == action_filter)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)

        total_count = query.count()
        logs = query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()

        return jsonify({
            "total": total_count,
            "logs": [l.to_dict() for l in logs],
            "limit": limit,
            "offset": offset
        }), 200

    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        return jsonify({"error": "Failed to retrieve audit logs"}), 500

@audit_bp.route("/audit", methods=["POST"])
@optional_auth
def create_client_audit_log():
    """
    Allows the frontend to log specific client interactions
    (e.g., CHAT_OPENED, GUIDE_VIEWED, DOCUMENT_ANALYSIS_VIEWED).
    """
    try:
        data = request.get_json() or {}
        action = data.get("action")
        if not action:
            return jsonify({"error": "Action is required"}), 400

        user = getattr(g, "user", None)
        user_id = user.id if user else None
        user_email = user.email if user else data.get("user_email")

        log_entry = log_audit_event(
            action=action,
            user_id=user_id,
            user_email=user_email,
            resource_type=data.get("resource_type"),
            resource_id=data.get("resource_id"),
            details=data.get("details", {}),
            ip_address=request.headers.get("X-Forwarded-For", request.remote_addr)
        )

        return jsonify({"ok": True, "log": log_entry.to_dict() if log_entry else None}), 201

    except Exception as e:
        logger.error(f"Error recording client audit log: {e}")
        return jsonify({"error": "Failed to record audit log"}), 500
