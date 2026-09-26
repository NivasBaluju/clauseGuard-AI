import re
import logging
from datetime import date
from dateutil import parser as date_parser
import spacy

logger = logging.getLogger(__name__)

_spacy_ner = None

def get_spacy_ner():
    global _spacy_ner
    if _spacy_ner is None:
        try:
            _spacy_ner = spacy.load("en_core_web_sm")
        except Exception:
            _spacy_ner = spacy.blank("en")
    return _spacy_ner

DURATION_PATTERNS = [
    # "30 days", "60-day written notice", "within 15 days of", "5 business days"
    r"(?i)\b(?:within\s+)?(\d{1,3})[\s-]*(calendar|business|working)?\s*days?\b(?:\s+(?:written\s+)?notice)?",
    # "two weeks", "2 weeks"
    r"(?i)\b(?:within\s+)?(\d{1,2})\s*weeks?\b",
    # "30-day notice"
    r"(?i)\b(\d{1,3})-day\b",
    # "6 months", "1 year"
    r"(?i)\b(\d{1,2})\s*months?\b",
]

DEADLINE_TYPE_KEYWORDS = [
    ("offer_acceptance_deadline", [r"accept\s+(?:this\s+)?offer", r"valid\s+(?:through|until)", r"acceptance\s+deadline", r"respond\s+by"]),
    ("contingency_deadline", [r"background\s+check", r"drug\s+(?:screen|test)", r"contingenc", r"right-to-work", r"i-9\s+verification"]),
    ("claims_filing_deadline", [r"proof\s+of\s+loss", r"file\s+(?:a\s+)?claim", r"notice\s+of\s+(?:loss|claim)", r"report\s+(?:the\s+)?loss"]),
    ("grace_period_end", [r"grace\s+period", r"before\s+a\s+late\s+fee", r"grace\s+window"]),
    ("renewal", [r"renew", r"renewal", r"extension", r"auto(?:matic)?\s+renew"]),
    ("termination", [r"terminat", r"vacat", r"surrender", r"quit", r"cancel"]),
    ("payment_due", [r"rent\s+(?:is\s+)?due", r"payment\s+due", r"payable\s+on", r"delinquent"]),
    ("notice_period", [r"written\s+notice", r"advance\s+notice", r"prior\s+notice", r"notice\s+to\s+vacate"]),
]

def classify_deadline_type(sentence_text: str) -> str:
    text_lower = sentence_text.lower()
    for d_type, patterns in DEADLINE_TYPE_KEYWORDS:
        for p in patterns:
            if re.search(p, text_lower):
                return d_type
    return "other"

WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "fourteen": 14, "fifteen": 15, "twenty": 20,
    "twenty-one": 21, "thirty": 30, "forty-five": 45, "sixty": 60, "ninety": 90,
}

def parse_relative_days(text: str) -> int | None:
    # Check digits with optional parentheses, e.g. "(10) days", "21) days", "30 days"
    m = re.search(r"\(?(\d{1,3})\)?[\s-]*(?:calendar|business|working)?\s*days?\b", text, re.IGNORECASE)
    if m:
        return int(m.group(1))

    # Check words, e.g. "thirty days", "five business days"
    for word, val in WORD_NUMBERS.items():
        if re.search(rf"\b{word}\b[\s-]*(?:calendar|business|working)?\s*days?\b", text, re.IGNORECASE):
            return val
    
    # Check weeks
    m_w = re.search(r"\(?(\d{1,2})\)?\s*weeks?\b", text, re.IGNORECASE)
    if m_w:
        return int(m_w.group(1)) * 7
        
    # Check months
    m_m = re.search(r"\(?(\d{1,2})\)?\s*months?\b", text, re.IGNORECASE)
    if m_m:
        return int(m_m.group(1)) * 30

    return None

def extract_deadlines_from_clause(clause_text: str, clause_id=None) -> list[dict]:
    """
    Extracts deadlines and date-bound obligations from a single clause text.
    Combines spaCy NER (DATE) and duration regex.
    """
    if not clause_text or not clause_text.strip():
        return []

    nlp = get_spacy_ner()
    doc = nlp(clause_text)
    deadlines = []
    seen_phrases = set()

    for sent in doc.sents:
        sent_str = sent.text.strip()
        sent_lower = sent_str.lower()
        
        # 1. Check relative durations with regex
        for p in DURATION_PATTERNS:
            for match in re.finditer(p, sent_str):
                matched_phrase = match.group(0).strip()
                if matched_phrase.lower() in seen_phrases:
                    continue
                seen_phrases.add(matched_phrase.lower())

                days = parse_relative_days(matched_phrase)
                d_type = classify_deadline_type(sent_str)
                
                # Confidence: confident if clear type and number of days <= 180, otherwise needs_review
                confidence = "confident" if d_type != "other" and days and days > 0 else "needs_review"
                
                deadlines.append({
                    "clause_id": clause_id,
                    "deadline_type": d_type,
                    "raw_text": f"{matched_phrase} ({sent_str[:120]}...)" if len(sent_str) > 120 else f"{matched_phrase} in '{sent_str}'",
                    "parsed_date": None,
                    "relative_days": days,
                    "confidence": confidence,
                })

        # 2. Check absolute dates via spaCy DATE entities
        for ent in sent.ents:
            if ent.label_ == "DATE":
                phrase = ent.text.strip()
                if phrase.lower() in seen_phrases or len(phrase) < 4:
                    continue
                seen_phrases.add(phrase.lower())

                parsed_dt = None
                confidence = "needs_review"
                try:
                    # Parse with fuzzy matching
                    parsed_candidate = date_parser.parse(phrase, fuzzy=True, default=None)
                    if parsed_candidate:
                        parsed_dt = parsed_candidate.date()
                        # If year is explicit (e.g. 2024-2030), mark confident
                        if re.search(r"\b202[0-9]\b", phrase):
                            confidence = "confident"
                        else:
                            confidence = "needs_review"
                except Exception:
                    parsed_dt = None
                    confidence = "needs_review"

                d_type = classify_deadline_type(sent_str)
                rel_days = parse_relative_days(phrase)

                # Avoid duplicate if this was already captured by regex
                if parsed_dt or rel_days or d_type != "other":
                    deadlines.append({
                        "clause_id": clause_id,
                        "deadline_type": d_type,
                        "raw_text": phrase,
                        "parsed_date": parsed_dt,
                        "relative_days": rel_days,
                        "confidence": confidence,
                    })

    return deadlines

def extract_all_deadlines(clauses: list[dict]) -> list[dict]:
    """
    Extracts deadlines across all clauses in a document.
    """
    all_deadlines = []
    for c in clauses:
        c_id = c.get("id")
        c_text = c.get("redacted_text") or c.get("text", "")
        found = extract_deadlines_from_clause(c_text, clause_id=c_id)
        all_deadlines.extend(found)
    return all_deadlines
