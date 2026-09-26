import os
import re
import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

def ask_gemini_or_fallback(question: str, context_text: str = "") -> dict:
    """
    LLM Integration with Grounded Context and Local Heuristic Fallback.
    Matches Deciva AI / Gemini API specifications.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    configured_model = os.environ.get("GEMINI_MODEL") or os.environ.get("GEMINI_CHAT_MODEL") or "gemini-1.5-flash"

    # 1. If no API key is provided, execute local keyword/heuristic match
    if not api_key:
        logger.info("[AI Chat] No GEMINI_API_KEY detected. Using local heuristic engine.")
        return local_heuristic_search(question, context_text)

    # 2. Strict system prompt forcing factual answers based on provided text
    prompt = f"""You are Deciva, an elite intelligent assistant.
Analyze the following context and answer the user's question accurately, clearly, and concisely.
CONTEXT:
{context_text[:15000] if context_text and context_text.strip() else 'General website copilot mode.'}
USER QUESTION:
{question}
Instructions:
1. Provide a direct, authoritative, and helpful answer.
2. If context is provided, ground your answer strictly in that context.
3. If the answer cannot be found in the context, explicitly state: "I could not find sufficient information in the provided document to answer that question."
"""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{configured_model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024,
            },
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                answer_text = candidates[0]["content"]["parts"][0].get("text", "")
                if answer_text:
                    is_grounded = "could not find sufficient information" not in answer_text.lower()
                    sources = []
                    if context_text and context_text.strip():
                        sources = [{
                            "section": "Document Content",
                            "excerpt": context_text[:180].strip() + "..."
                        }]
                    return {
                        "answer": answer_text.strip(),
                        "engine": "gemini",
                        "provider": "google",
                        "model": configured_model,
                        "grounded": is_grounded,
                        "confidence": 0.94 if is_grounded else 0.25,
                        "sources": sources,
                        "fallbackUsed": False,
                    }
    except Exception as err:
        logger.warning(f"[Gemini API Fetch Exception]: {err}")

    # Fallback if LLM fails or network error occurs
    return local_heuristic_search(question, context_text)

def local_heuristic_search(question: str, doc_text: str = "") -> dict:
    """
    Deterministic local search fallback when offline or without API key.
    """
    q_lower = (question or "").lower().strip()

    # Basic greeting
    if re.search(r"^(hi|hello|hey|greetings|help)\b", q_lower, re.IGNORECASE):
        return {
            "answer": "Hello! I am your AI Copilot. Ask me any question regarding your documents, obligations, fees, or account details.",
            "engine": "deterministic",
            "grounded": True,
            "confidence": 1.0,
            "sources": [],
        }

    if not doc_text or not doc_text.strip():
        return {
            "answer": "No specific document context found. Please upload or open a document to ask grounded questions.",
            "engine": "deterministic",
            "grounded": False,
            "confidence": 0.0,
            "sources": [],
        }

    # Find sentences matching search words in question
    words = [w for w in re.split(r"\W+", q_lower) if len(w) > 3]
    sentences = [s.strip() for s in re.split(r"[.!?\n]+", doc_text) if s.strip()]
    matches = [s for s in sentences if any(w in s.lower() for w in words)]

    if matches:
        return {
            "answer": f"Based on your document:\n\n\"{'. '.join(matches[:2])}.\"",
            "engine": "deterministic",
            "grounded": True,
            "confidence": 0.82,
            "sources": [
                {"section": f"Segment {i + 1}", "excerpt": m[:150]}
                for i, m in enumerate(matches[:2])
            ],
        }

    return {
        "answer": "I could not find sufficient information in this document to answer that question.",
        "engine": "deterministic",
        "grounded": False,
        "confidence": 0.2,
        "sources": [],
    }
