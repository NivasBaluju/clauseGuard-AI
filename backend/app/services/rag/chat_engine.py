import re
import os
import logging
from google import genai
from flask import current_app
from app.extensions import db
from app.models.chat import ChatSession, ChatMessage
from app.services.rag.embedder import embed_query, get_genai_client
from app.services.rag.retriever import retrieve_relevant_clauses
from app.utils.validators import sanitize_chat_input

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are ClauseGuard AI's document analysis assistant.
Answer the user's question STRICTLY AND SOLELY using the retrieved document clauses provided below.

CRITICAL GROUNDING RULES:
1. ONLY use facts and terms explicitly stated in the provided clauses. Never hallucinate, invent details, or assume terms not in the text.
2. ALWAYS cite the specific clause you rely on using the format [Clause X] (e.g., "[Clause 2]").
3. If the retrieved clauses DO NOT contain the answer, you MUST say plainly:
   "The provided document does not contain information addressing this question."
   Do NOT guess, hypothesize, or introduce external legal principles.
4. Keep answers factual, concise, and objective.
5. Reminder: ClauseGuard AI provides automated, non-expert analysis for informational purposes only. It is not legal advice.
"""

def answer_document_question(document_id, question: str, session_id=None) -> dict:
    """
    RAG pipeline:
    1. Scan question for prompt injection.
    2. Embed question with Gemini embedding model.
    3. Retrieve top clauses via pgvector.
    4. Generate grounded answer via Gemini API.
    5. Track citations and verify grounding.
    """
    # 1. Defend against prompt injection
    sanitized_question, was_flagged, patterns = sanitize_chat_input(question)
    if was_flagged:
        logger.warning(f"Sanitized injection patterns {patterns} in user question")

    # 2. Get or create chat session
    if session_id:
        session = db.session.get(ChatSession, session_id)
    else:
        session = None

    if not session:
        session = ChatSession(document_id=document_id)
        db.session.add(session)
        db.session.commit()

    # Save user message
    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=question,
        retrieved_clause_ids=[],
        grounded=True,
    )
    db.session.add(user_msg)
    db.session.commit()

    # 3. Embed query and retrieve relevant clauses
    query_vector = embed_query(sanitized_question)
    retrieved_clauses = retrieve_relevant_clauses(document_id, query_vector, top_k=5)

    if not retrieved_clauses:
        fallback_answer = "No clauses found for this document to answer your question."
        asst_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=fallback_answer,
            retrieved_clause_ids=[],
            grounded=False,
        )
        db.session.add(asst_msg)
        db.session.commit()
        return {
            "session_id": str(session.id),
            "message_id": str(asst_msg.id),
            "answer": fallback_answer,
            "cited_clause_ids": [],
            "grounded": False,
            "retrieved_clauses": [],
        }

    # 4. Construct context with clause references
    context_blocks = []
    index_to_id = {}
    for c in retrieved_clauses:
        idx = c["clause_index"]
        c_id = c["clause_id"]
        index_to_id[idx] = c_id
        context_blocks.append(
            f"[Clause {idx}] (Type: {c['clause_type']}, Risk: {c['risk_score']}):\n{c['redacted_text']}"
        )

    context_str = "\n\n".join(context_blocks)
    full_prompt = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"--- RETRIEVED CLAUSES FROM THIS DOCUMENT ---\n"
        f"{context_str}\n\n"
        f"--- USER QUESTION ---\n"
        f"{sanitized_question}\n\n"
        f"ANSWER (cite [Clause X] or declare ungrounded):"
    )

    # 5. Call Gemini API
    client = get_genai_client()
    chat_model = current_app.config.get("GEMINI_CHAT_MODEL", "gemini-3.8-flash") if current_app else "gemini-3.8-flash"

    try:
        response = client.models.generate_content(
            model=chat_model,
            contents=full_prompt,
        )
        answer_text = response.text.strip()
    except Exception as e:
        logger.error(f"Error calling Gemini model {chat_model}: {e}")
        answer_text = f"An error occurred while communicating with the AI service: {str(e)}"

    # 6. Verify grounding and extract citations
    # Check if answer claims no information
    ungrounded_phrases = [
        "does not contain information",
        "no information addressing",
        "not mentioned in the provided",
        "cannot answer",
        "not addressed in the clauses",
    ]
    is_unsupported = any(phrase in answer_text.lower() for phrase in ungrounded_phrases)

    # Extract cited clause indices like [Clause 3]
    cited_indices = re.findall(r"\[Clause\s+(\d+)\]", answer_text, re.IGNORECASE)
    cited_clause_ids = []
    for idx_str in cited_indices:
        idx_int = int(idx_str)
        if idx_int in index_to_id:
            cited_clause_ids.append(index_to_id[idx_int])

    grounded = (not is_unsupported) and (len(cited_clause_ids) > 0)

    # If the model didn't cite an explicit [Clause X] but answered from retrieved clauses, check overlap
    if not cited_clause_ids and not is_unsupported:
        grounded = False

    # 7. Save assistant message to database
    asst_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=answer_text,
        retrieved_clause_ids=[c["clause_id"] for c in retrieved_clauses],
        grounded=grounded,
    )
    db.session.add(asst_msg)
    db.session.commit()

    return {
        "session_id": str(session.id),
        "message_id": str(asst_msg.id),
        "answer": answer_text,
        "cited_clause_ids": cited_clause_ids,
        "grounded": grounded,
        "retrieved_clauses": retrieved_clauses,
    }
