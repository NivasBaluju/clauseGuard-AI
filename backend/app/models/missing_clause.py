import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class MissingClause(db.Model):
    __tablename__ = "missing_clauses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    clause_type = db.Column(db.String(64), nullable=False)
    severity = db.Column(db.String(16), nullable=False)  # high | medium | low
    checklist_note = db.Column(db.Text)

    document = db.relationship("Document", back_populates="missing_clauses")

    def to_dict(self):
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "clause_type": self.clause_type,
            "severity": self.severity,
            "checklist_note": self.checklist_note,
        }
