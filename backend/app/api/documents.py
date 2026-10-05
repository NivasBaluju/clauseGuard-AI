import os
import tempfile
import threading
import logging
from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.document import Document
from app.utils.validators import allowed_file, validate_document_type
from app.services.pipeline import process_document_pipeline
from app.services.audit_service import log_audit_event

logger = logging.getLogger(__name__)

documents_bp = Blueprint("documents", __name__)

from app.middleware.auth import optional_auth

def run_pipeline_async(app, document_id, file_path, ext):
    with app.app_context():
        try:
            process_document_pipeline(document_id, file_path, ext)
        except Exception as e:
            logger.error(f"Async pipeline processing failed for {document_id}: {e}")
        finally:
            try:
                db.session.remove()
            except Exception:
                pass

@documents_bp.route("/documents", methods=["POST"])
@optional_auth
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded in 'file' field."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Selected file has an empty filename."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file format. Supported formats: .pdf, .docx, .txt"}), 400

    doc_type = request.form.get("document_type", "").strip()
    if not validate_document_type(doc_type):
        return jsonify({
            "error": "Invalid document_type. Must be one of: 'rental_agreement', 'job_offer_letter', 'insurance_policy'"
        }), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"cg_{filename}")
    file.save(temp_path)

    user = getattr(g, "user", None)
    user_id = user.id if user else None

    doc = Document(
        filename=filename,
        original_format=ext,
        document_type=doc_type,
        status="uploaded",
        processing_stage="queued",
        user_id=user_id,
    )
    db.session.add(doc)
    db.session.commit()

    app = current_app._get_current_object()
    thread = threading.Thread(target=run_pipeline_async, args=(app, str(doc.id), temp_path, ext))
    thread.daemon = True
    thread.start()

    log_audit_event(
        action="DOC_UPLOADED",
        user_id=user_id,
        user_email=user.email if user else None,
        resource_type="document",
        resource_id=str(doc.id),
        details={"filename": doc.filename, "document_type": doc.document_type, "format": ext}
    )

    return jsonify({
        "id": str(doc.id),
        "document_id": str(doc.id),
        "status": doc.status,
        "processing_stage": doc.processing_stage,
        "filename": doc.filename,
        "document_type": doc.document_type,
    }), 201

@documents_bp.route("/documents", methods=["GET"])
@optional_auth
def list_documents():
    user = getattr(g, "user", None)
    if not user:
        docs = Document.query.filter(Document.user_id.is_(None)).order_by(Document.uploaded_at.desc()).limit(50).all()
        return jsonify([d.to_dict(include_text=False) for d in docs]), 200

    docs = Document.query.filter(
        (Document.user_id == user.id) | (Document.user_id.is_(None))
    ).order_by(Document.uploaded_at.desc()).limit(50).all()
    return jsonify([d.to_dict(include_text=False) for d in docs]), 200

@documents_bp.route("/documents/<uuid:doc_id>", methods=["GET"])
@optional_auth
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    user = getattr(g, "user", None)
    if user and doc.user_id and doc.user_id != user.id:
        return jsonify({"error": "Unauthorized access to this document."}), 403
    return jsonify(doc.to_dict(include_text=True)), 200

@documents_bp.route("/documents/<uuid:doc_id>/status", methods=["GET"])
@optional_auth
def get_document_status(doc_id):
    doc = Document.query.get_or_404(doc_id)
    user = getattr(g, "user", None)
    if user and doc.user_id and doc.user_id != user.id:
        return jsonify({"error": "Unauthorized access to this document."}), 403
    return jsonify({
        "document_id": str(doc.id),
        "status": doc.status,
        "processing_stage": doc.processing_stage,
        "error_message": doc.error_message,
        "overall_risk_score": doc.overall_risk_score,
        "risk_band": doc.risk_band,
    }), 200

@documents_bp.route("/documents/<uuid:doc_id>", methods=["DELETE"])
@optional_auth
def delete_document(doc_id):
    doc = Document.query.get(doc_id)
    if not doc:
        return jsonify({"message": f"Document {doc_id} already deleted."}), 200

    user = getattr(g, "user", None)
    if user and doc.user_id and doc.user_id != user.id:
        return jsonify({"error": "Unauthorized. You can only delete your own documents."}), 403

    try:
        from app.models.chat import ChatMessage, ChatSession
        from app.models.clause import Clause
        from app.models.missing_clause import MissingClause
        from app.models.deadline import Deadline
        from app.models.pii_finding import PIIFinding

        filename = doc.filename
        doc_id_str = str(doc.id)

        sessions = ChatSession.query.filter_by(document_id=doc.id).all()
        session_ids = [s.id for s in sessions]
        if session_ids:
            ChatMessage.query.filter(ChatMessage.session_id.in_(session_ids)).delete(synchronize_session=False)

        ChatMessage.query.filter_by(document_id=doc.id).delete(synchronize_session=False)
        ChatSession.query.filter_by(document_id=doc.id).delete(synchronize_session=False)
        Clause.query.filter_by(document_id=doc.id).delete(synchronize_session=False)
        MissingClause.query.filter_by(document_id=doc.id).delete(synchronize_session=False)
        Deadline.query.filter_by(document_id=doc.id).delete(synchronize_session=False)
        PIIFinding.query.filter_by(document_id=doc.id).delete(synchronize_session=False)

        db.session.delete(doc)
        db.session.commit()

        log_audit_event(
            action="DOC_DELETED",
            user_id=user.id if user else None,
            user_email=user.email if user else None,
            resource_type="document",
            resource_id=doc_id_str,
            details={"filename": filename}
        )

        return jsonify({"message": f"Document {doc_id} deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to delete document {doc_id}: {e}", exc_info=True)
        return jsonify({"error": f"Failed to delete document: {str(e)}"}), 500

