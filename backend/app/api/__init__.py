from app.api.health import health_bp
from app.api.documents import documents_bp
from app.api.analysis import analysis_bp
from app.api.chat import chat_bp

__all__ = ["health_bp", "documents_bp", "analysis_bp", "chat_bp"]
