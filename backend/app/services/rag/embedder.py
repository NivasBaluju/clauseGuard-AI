import os
import logging
from google import genai
from flask import current_app

logger = logging.getLogger(__name__)

_genai_client = None

def get_genai_client():
    global _genai_client
    if _genai_client is None:
        api_key = current_app.config.get("GEMINI_API_KEY") if current_app else os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        _genai_client = genai.Client(api_key=api_key)
    return _genai_client

def get_embed_model_name() -> str:
    if current_app:
        return current_app.config.get("GEMINI_EMBED_MODEL", "gemini-embedding-001")
    return os.environ.get("GEMINI_EMBED_MODEL", "gemini-embedding-001")

def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """
    Generates a 768-dimensional embedding vector using Gemini API via google-genai SDK.
    """
    if not text or not text.strip():
        return [0.0] * 768

    client = get_genai_client()
    model = get_embed_model_name()

    try:
        result = client.models.embed_content(
            model=model,
            contents=[text],
            config={
                "output_dimensionality": 768,
                "task_type": task_type,
            },
        )
        if result.embeddings and len(result.embeddings) > 0:
            return result.embeddings[0].values
    except Exception as e:
        logger.error(f"Error generating embedding with model {model}: {e}")
        raise e

    return [0.0] * 768

def embed_query(query_text: str) -> list[float]:
    """
    Convenience method to embed a search query.
    """
    return embed_text(query_text, task_type="RETRIEVAL_QUERY")

def embed_document_clauses(clauses: list[dict]) -> list[list[float]]:
    """
    Embeds multiple clauses.
    """
    embeddings = []
    for c in clauses:
        txt = c.get("redacted_text") or c.get("text", "")
        vec = embed_text(txt, task_type="RETRIEVAL_DOCUMENT")
        embeddings.append(vec)
    return embeddings
