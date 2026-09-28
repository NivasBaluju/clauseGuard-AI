import logging
from flask import request
from app.extensions import db
from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)

def log_audit_event(
    action: str,
    user_id=None,
    user_email: str = None,
    resource_type: str = None,
    resource_id: str = None,
    details: dict = None,
    ip_address: str = None
) -> AuditLog:
    """
    Safely records an audit event in PostgreSQL.
    """
    try:
        if not ip_address:
            try:
                ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
                if ip_address and "," in ip_address:
                    ip_address = ip_address.split(",")[0].strip()
            except Exception:
                ip_address = "127.0.0.1"

        log_entry = AuditLog(
            action=action,
            user_id=user_id,
            user_email=user_email,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            details=details or {},
            ip_address=ip_address
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    except Exception as e:
        logger.warning(f"Failed to record audit log: {e}")
        db.session.rollback()
        return None
