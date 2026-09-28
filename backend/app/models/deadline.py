import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Deadline(db.Model):
    __tablename__ = "deadlines"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    clause_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("clauses.id", ondelete="SET NULL"),
        nullable=True,
    )
    deadline_type = db.Column(db.String(64))
    raw_text = db.Column(db.Text, nullable=False)
    parsed_date = db.Column(db.Date)
    relative_days = db.Column(db.Integer)
    confidence = db.Column(db.String(16), nullable=False, default="needs_review")

    document = db.relationship("Document", back_populates="deadlines")
    clause = db.relationship("Clause", back_populates="deadlines")

    def to_dict(self):
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "clause_id": str(self.clause_id) if self.clause_id else None,
            "deadline_type": self.deadline_type,
            "raw_text": self.raw_text,
            "parsed_date": self.parsed_date.isoformat() if self.parsed_date else None,
            "relative_days": self.relative_days,
            "confidence": self.confidence,
        }
