from flask import Blueprint, request, jsonify
from app.models.document import Document
from app.models.chat import ChatSession, ChatMessage
from app.services.rag.chat_engine import answer_document_question

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/documents/<uuid:doc_id>/chat", methods=["POST"])
def chat_with_document(doc_id):
    Document.query.get_or_404(doc_id)
    data = request.get_json() or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question field cannot be empty."}), 400

    session_id = data.get("session_id")

    result = answer_document_question(
        document_id=doc_id,
        question=question,
        session_id=session_id,
    )

    return jsonify(result), 200

@chat_bp.route("/documents/<uuid:doc_id>/chat/history", methods=["GET"])
def get_chat_history(doc_id):
    Document.query.get_or_404(doc_id)
    sessions = (
        ChatSession.query.filter_by(document_id=doc_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )

    return jsonify([s.to_dict() for s in sessions]), 200
