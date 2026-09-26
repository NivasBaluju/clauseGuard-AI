import os
import tempfile
import threading
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.document import Document
from app.utils.validators import allowed_file, validate_document_type
from app.services.pipeline import process_document_pipeline

logger = logging.getLogger(__name__)
documents_bp = Blueprint("documents", __name__)

def run_pipeline_async(app, document_id, file_path, ext):
    with app.app_context():
        try:
            process_document_pipeline(document_id, file_path, ext)
        except Exception as e:
            logger.error(f"Async pipeline processing failed for {document_id}: {e}")

@documents_bp.route("/documents", methods=["POST"])
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

    # Save to temp file
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"cg_{filename}")
    file.save(temp_path)

    # Create document record
    doc = Document(
        filename=filename,
        original_format=ext,
        document_type=doc_type,
        status="uploaded",
        processing_stage="queued",
    )
    db.session.add(doc)
    db.session.commit()

    # Launch pipeline in background thread with application context
    app = current_app._get_current_object()
    thread = threading.Thread(target=run_pipeline_async, args=(app, str(doc.id), temp_path, ext))
    thread.daemon = True
    thread.start()

    return jsonify({
        "id": str(doc.id),
        "document_id": str(doc.id),
        "status": doc.status,
        "processing_stage": doc.processing_stage,
        "filename": doc.filename,
        "document_type": doc.document_type,
    }), 201

@documents_bp.route("/documents", methods=["GET"])
def list_documents():
    docs = Document.query.order_by(Document.uploaded_at.desc()).all()
    return jsonify([d.to_dict(include_text=False) for d in docs]), 200

@documents_bp.route("/documents/<uuid:doc_id>", methods=["GET"])
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    return jsonify(doc.to_dict(include_text=True)), 200

@documents_bp.route("/documents/<uuid:doc_id>/status", methods=["GET"])
def get_document_status(doc_id):
    doc = Document.query.get_or_404(doc_id)
    return jsonify({
        "document_id": str(doc.id),
        "status": doc.status,
        "processing_stage": doc.processing_stage,
        "error_message": doc.error_message,
        "overall_risk_score": doc.overall_risk_score,
        "risk_band": doc.risk_band,
    }), 200

@documents_bp.route("/documents/<uuid:doc_id>", methods=["DELETE"])
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"message": f"Document {doc_id} deleted successfully."}), 200
