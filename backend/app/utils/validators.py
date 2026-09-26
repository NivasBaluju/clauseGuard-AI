import re
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
ALLOWED_DOCUMENT_TYPES = {"rental_agreement", "job_offer_letter", "insurance_policy"}

PROMPT_INJECTION_PATTERNS = [
    r"(?i)\bignore\s+(all\s+)?(previous|prior|above)\s+instructions\b",
    r"(?i)\byou\s+are\s+now\b",
    r"(?i)\breveal\s+(your\s+)?(system\s+prompt|instructions)\b",
    r"(?i)\bdisregard\s+(all\s+)?(previous|prior)\s+rules\b",
    r"(?i)\bact\s+as\s+(an?\s+)?(unrestricted|jailbroken|developer)\b",
    r"(?i)\bpretend\s+you\s+are\b",
    r"(?i)\bsystem\s*:\s*",
    r"(?i)\bDAN\s+mode\b",
]

def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def validate_document_type(doc_type: str) -> bool:
    return doc_type in ALLOWED_DOCUMENT_TYPES

def sanitize_chat_input(user_input: str) -> tuple[str, bool, list[str]]:
    """
    Best-effort defensive scan for prompt-injection patterns in user input.
    Returns: (sanitized_text, was_flagged, detected_patterns)
    """
    detected = []
    sanitized = user_input
    
    for pattern in PROMPT_INJECTION_PATTERNS:
        matches = re.findall(pattern, sanitized)
        if matches:
            detected.append(pattern)
            logger.warning(f"Prompt injection pattern detected: {pattern} in user input")
            # Defensively defang or redact the offending span
            sanitized = re.sub(pattern, "[DEFANGED_INSTRUCTION]", sanitized)
            
    was_flagged = len(detected) > 0
    return sanitized, was_flagged, detected
