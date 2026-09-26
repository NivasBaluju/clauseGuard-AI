import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.extensions import db

class ChatSession(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    document = db.relationship("Document", back_populates="chat_sessions")
    messages = db.relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at")

    def to_dict(self):
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "messages": [m.to_dict() for m in self.messages] if self.messages else [],
        }

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = db.Column(db.String(10), nullable=False)  # user | assistant
    content = db.Column(db.Text, nullable=False)
    retrieved_clause_ids = db.Column(ARRAY(UUID(as_uuid=True)))
    grounded = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    session = db.relationship("ChatSession", back_populates="messages")

    def to_dict(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "role": self.role,
            "content": self.content,
            "retrieved_clause_ids": [str(cid) for cid in self.retrieved_clause_ids] if self.retrieved_clause_ids else [],
            "grounded": self.grounded,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
