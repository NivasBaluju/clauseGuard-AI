import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class PIIFinding(db.Model):
    __tablename__ = "pii_findings"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    entity_type = db.Column(db.String(32), nullable=False)  # PERSON, EMAIL_ADDRESS, etc.
    start_offset = db.Column(db.Integer)
    end_offset = db.Column(db.Integer)
    confidence = db.Column(db.Float)

    document = db.relationship("Document", back_populates="pii_findings")

    def to_dict(self):
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "entity_type": self.entity_type,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "confidence": self.confidence,
        }
