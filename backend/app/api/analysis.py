import io
from flask import Blueprint, jsonify, send_file, current_app
from app.models.document import Document
from app.models.clause import Clause
from app.models.missing_clause import MissingClause
from app.models.deadline import Deadline
from app.models.pii_finding import PIIFinding
from app.reports.pdf_report import generate_pdf_report

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/documents/<uuid:doc_id>/clauses", methods=["GET"])
def get_document_clauses(doc_id):
    Document.query.get_or_404(doc_id)
    clauses = Clause.query.filter_by(document_id=doc_id).order_by(Clause.clause_index.asc()).all()
    return jsonify([c.to_dict() for c in clauses]), 200

@analysis_bp.route("/documents/<uuid:doc_id>/missing-clauses", methods=["GET"])
def get_missing_clauses(doc_id):
    Document.query.get_or_404(doc_id)
    missing = MissingClause.query.filter_by(document_id=doc_id).all()
    return jsonify([m.to_dict() for m in missing]), 200

@analysis_bp.route("/documents/<uuid:doc_id>/deadlines", methods=["GET"])
def get_deadlines(doc_id):
    Document.query.get_or_404(doc_id)
    deadlines = Deadline.query.filter_by(document_id=doc_id).order_by(
        Deadline.relative_days.asc().nulls_last(),
        Deadline.parsed_date.asc().nulls_last()
    ).all()
    return jsonify([d.to_dict() for d in deadlines]), 200

@analysis_bp.route("/documents/<uuid:doc_id>/pii-summary", methods=["GET"])
def get_pii_summary(doc_id):
    Document.query.get_or_404(doc_id)
    findings = PIIFinding.query.filter_by(document_id=doc_id).all()
    
    counts = {}
    details = []
    for f in findings:
        counts[f.entity_type] = counts.get(f.entity_type, 0) + 1
        details.append(f.to_dict())

    return jsonify({
        "document_id": str(doc_id),
        "total_redactions": len(findings),
        "total_findings": len(findings),
        "entity_counts": counts,
        "findings": details,
    }), 200

@analysis_bp.route("/documents/<uuid:doc_id>/report.pdf", methods=["GET"])
def download_pdf_report(doc_id):
    doc = Document.query.get_or_404(doc_id)
    clauses = Clause.query.filter_by(document_id=doc_id).order_by(Clause.clause_index.asc()).all()
    missing = MissingClause.query.filter_by(document_id=doc_id).all()
    deadlines = Deadline.query.filter_by(document_id=doc_id).order_by(
        Deadline.relative_days.asc().nulls_last()
    ).all()
    findings = PIIFinding.query.filter_by(document_id=doc_id).all()

    pdf_bytes = generate_pdf_report(doc, clauses, missing, deadlines, findings)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"clauseguard_report_{doc.filename.rsplit('.', 1)[0]}.pdf",
    )
