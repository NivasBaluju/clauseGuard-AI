import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.extensions import db

class Clause(db.Model):
    __tablename__ = "clauses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    clause_index = db.Column(db.Integer, nullable=False)
    clause_type = db.Column(db.String(64))
    clause_type_confidence = db.Column(db.Float)
    favorability_label = db.Column(db.String(16))  # fair | needs_review | unfavorable
    favorability_confidence = db.Column(db.Float)
    risk_score = db.Column(db.Float)
    redacted_text = db.Column(db.Text, nullable=False)
    raw_text_encrypted = db.Column(db.LargeBinary)
    start_offset = db.Column(db.Integer)
    end_offset = db.Column(db.Integer)
    embedding = db.Column(Vector(768))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    document = db.relationship("Document", back_populates="clauses")
    deadlines = db.relationship("Deadline", back_populates="clause")

    def to_dict(self):
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "clause_index": self.clause_index,
            "clause_type": self.clause_type,
            "clause_type_confidence": self.clause_type_confidence,
            "favorability_label": self.favorability_label,
            "favorability_confidence": self.favorability_confidence,
            "risk_score": self.risk_score,
            "redacted_text": self.redacted_text,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
