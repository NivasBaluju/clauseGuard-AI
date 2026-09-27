import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = db.Column(db.String(255), nullable=False)
    original_format = db.Column(db.String(10), nullable=False)  # pdf | docx | txt
    document_type = db.Column(
        db.String(32),
        nullable=False,
    )  # rental_agreement | job_offer_letter | insurance_policy
    status = db.Column(db.String(20), nullable=False, default="uploaded")  # uploaded | processing | analyzed | failed
    processing_stage = db.Column(db.String(64))  # e.g. ocr, redaction, classification
    error_message = db.Column(db.Text)
    page_count = db.Column(db.Integer)
    raw_text_encrypted = db.Column(db.LargeBinary)  # audit-only, never sent downstream
    redacted_text = db.Column(db.Text)
    overall_risk_score = db.Column(db.Float)
    risk_band = db.Column(db.String(16))  # low | medium | high | critical
    model_version = db.Column(db.String(64))
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    analyzed_at = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    user = db.relationship("User", backref=db.backref("documents", cascade="all, delete-orphan", lazy="dynamic"))
    clauses = db.relationship("Clause", back_populates="document", cascade="all, delete-orphan", order_by="Clause.clause_index")
    missing_clauses = db.relationship("MissingClause", back_populates="document", cascade="all, delete-orphan")
    deadlines = db.relationship("Deadline", back_populates="document", cascade="all, delete-orphan")
    pii_findings = db.relationship("PIIFinding", back_populates="document", cascade="all, delete-orphan")
    chat_sessions = db.relationship("ChatSession", back_populates="document", cascade="all, delete-orphan")

    def to_dict(self, include_text=False):
        data = {
            "id": str(self.id),
            "filename": self.filename,
            "original_format": self.original_format,
            "document_type": self.document_type,
            "status": self.status,
            "processing_stage": self.processing_stage,
            "error_message": self.error_message,
            "page_count": self.page_count,
            "overall_risk_score": self.overall_risk_score,
            "risk_band": self.risk_band,
            "model_version": self.model_version,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "user_id": str(self.user_id) if self.user_id else None,
        }
        if include_text:
            data["redacted_text"] = self.redacted_text
        return data
