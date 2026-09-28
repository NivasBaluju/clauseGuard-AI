import uuid
import json
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
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
    messages = db.relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at.asc()")

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
        nullable=True,
        index=True,
    )
    document_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float, nullable=True)
    grounded = db.Column(db.Boolean, default=True)
    sources = db.Column(JSONB, default=list)
    retrieved_clause_ids = db.Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    session = db.relationship("ChatSession", back_populates="messages")
    user = db.relationship("User", back_populates="chat_messages")
    document = db.relationship("Document", back_populates="chat_messages")

    def to_dict(self):
        srcs = self.sources
        if isinstance(srcs, str):
            try:
                srcs = json.loads(srcs)
            except Exception:
                srcs = []
        elif not isinstance(srcs, list):
            srcs = []

        return {
            "id": str(self.id),
            "document_id": str(self.document_id) if self.document_id else None,
            "user_id": str(self.user_id) if self.user_id else None,
            "session_id": str(self.session_id) if self.session_id else None,
            "role": self.role,
            "content": self.content,
            "confidence": self.confidence,
            "grounded": self.grounded if self.grounded is not None else True,
            "sources": srcs,
            "retrieved_clause_ids": [str(cid) for cid in self.retrieved_clause_ids] if self.retrieved_clause_ids else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
