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

WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "fourteen": 14, "fifteen": 15, "twenty": 20,
    "twenty-one": 21, "twenty one": 21, "thirty": 30, "forty-five": 45, "forty five": 45,
    "sixty": 60, "ninety": 90, "one hundred twenty": 120, "one-hundred twenty": 120,
    "one hundred eighty": 180, "one-hundred eighty": 180, "365": 365,
}

# Rich regex patterns for catching all types of legal durations
DURATION_PATTERNS = [
    # "thirty (30) days", "at least 30 days", "within 60 calendar days", "15 business days"
    r"(?i)\b(?:at\s+least|not\s+less\s+than|within|giving|upon|prior\s+to|no\s+later\s+than)?\s*\(?(\d{1,3})\)?[\s-]*(?:calendar|business|working)?\s*days?\b",
    # Spelled out numbers: "thirty days", "twenty-one days", "seven business days"
    r"(?i)\b(?:at\s+least|not\s+less\s+than|within|giving|upon|prior\s+to)?\s*(one|two|three|four|five|six|seven|eight|nine|ten|fourteen|fifteen|twenty|twenty-one|thirty|forty-five|sixty|ninety)\s*\(?\d{1,3}\)?[\s-]*(?:calendar|business|working)?\s*days?\b",
    # Weeks: "two (2) weeks", "within 4 weeks"
    r"(?i)\b(?:within|giving|at\s+least)?\s*\(?(\d{1,2})\)?\s*weeks?\b",
    r"(?i)\b(one|two|three|four)\s*weeks?\b",
    # Months: "6 months", "within 12 months", "1 year"
    r"(?i)\b(?:within|at\s+least)?\s*\(?(\d{1,2})\)?\s*months?\b",
    r"(?i)\b(one|two|three|six|twelve)\s*months?\b",
    # Hours notice: "24 hours", "48 hours advance written notice"
    r"(?i)\b\(?(\d{1,2})\)?[\s-]*(?:hours?|hrs?)\s*(?:written\s+)?notice\b",
    # Hyphenated modifiers: "30-day notice", "60-day period"
    r"(?i)\b(\d{1,3})-day\b",
    # Specific payment days: "on or before the 1st day", "due on the 5th of each month"
    r"(?i)\b(?:on\s+or\s+before\s+the|due\s+on\s+the|payable\s+on\s+the)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(?:day\s+of\s+(?:each\s+)?month|of\s+each\s+month)\b",
]

DEADLINE_TYPE_PATTERNS = [
    ("offer_acceptance_deadline", [
        r"accept\s+(?:this\s+)?offer", r"valid\s+(?:through|until)", r"acceptance\s+deadline",
        r"respond\s+by", r"offer\s+expires", r"return\s+signed\s+copy"
    ]),
    ("security_deposit_return", [
        r"security\s+deposit", r"return\s+(?:the\s+)?deposit", r"deposit\s+refund",
        r"after\s+(?:vacating|surrender|move-out|termination\s+of\s+tenancy)", r"itemized\s+deductions"
    ]),
    ("cure_period", [
        r"cure\s+such\s+default", r"remedy\s+(?:the\s+)?breach", r"notice\s+to\s+cure",
        r"pay\s+or\s+quit", r"correct\s+the\s+violation", r"cure\s+period"
    ]),
    ("claims_filing_deadline", [
        r"proof\s+of\s+loss", r"file\s+(?:a\s+)?claim", r"notice\s+of\s+(?:loss|claim)",
        r"report\s+(?:the\s+)?loss", r"report\s+theft", r"sworn\s+statement\s+in\s+proof"
    ]),
    ("grace_period_end", [
        r"grace\s+period", r"before\s+a\s+late\s+fee", r"grace\s+window",
        r"delinquent\s+after", r"late\s+charge\s+assessed"
    ]),
    ("payment_due", [
        r"rent\s+(?:is\s+)?due", r"payment\s+due", r"payable\s+on",
        r"on\s+or\s+before\s+the", r"first\s+day\s+of\s+each\s+month", r"monthly\s+installment"
    ]),
    ("contingency_deadline", [
        r"background\s+check", r"drug\s+(?:screen|test)", r"contingenc",
        r"right-to-work", r"i-9\s+verification", r"probationary\s+period", r"initial\s+90\s+days"
    ]),
    ("renewal", [
        r"renew", r"renewal", r"extension", r"auto(?:matic)?\s+renew",
        r"prior\s+to\s+(?:the\s+)?expiration", r"option\s+to\s+extend"
    ]),
    ("termination", [
        r"terminat", r"vacat", r"surrender", r"quit", r"cancel",
        r"notice\s+to\s+vacate", r"move-out\s+notice", r"end\s+of\s+term"
    ]),
    ("inspection_notice", [
        r"landlord\s+entry", r"inspect\s+the\s+premises", r"entry\s+notice",
        r"24\s+hours\s+notice", r"48\s+hours\s+notice", r"right\s+of\s+entry"
    ]),
    ("notice_period", [
        r"written\s+notice", r"advance\s+notice", r"prior\s+notice",
        r"calendar\s+days\s+notice", r"business\s+days\s+notice"
    ]),
]

def classify_deadline_type(sentence_text: str) -> str:
    text_lower = sentence_text.lower()
    for d_type, patterns in DEADLINE_TYPE_PATTERNS:
        for p in patterns:
            if re.search(p, text_lower):
                return d_type
    return "notice_period"

def parse_relative_days(text: str) -> int | None:
    text_clean = text.lower().strip()

    # Hours check (24h -> 1 day, 48h -> 2 days)
    m_h = re.search(r"\(?(\d{1,2})\)?[\s-]*(?:hours?|hrs?)", text_clean)
    if m_h:
        hours = int(m_h.group(1))
        return max(1, hours // 24)

    # Digits with optional parens: "30 days", "thirty (30) days"
    m_d = re.search(r"\(?(\d{1,3})\)?[\s-]*(?:calendar|business|working)?\s*days?", text_clean)
    if m_d:
        return int(m_d.group(1))

    # Spelled out words: "thirty days"
    for word, val in WORD_NUMBERS.items():
        if re.search(rf"\b{word}\b", text_clean):
            return val

    # Weeks
    m_w = re.search(r"\(?(\d{1,2})\)?\s*weeks?", text_clean)
    if m_w:
        return int(m_w.group(1)) * 7

    for w_word in ["one", "two", "three", "four"]:
        if re.search(rf"\b{w_word}\s+weeks?", text_clean):
            return WORD_NUMBERS[w_word] * 7

    # Months
    m_m = re.search(r"\(?(\d{1,2})\)?\s*months?", text_clean)
    if m_m:
        return int(m_m.group(1)) * 30

    return None

def clean_deadline_phrase(phrase: str) -> str:
    """Cleans punctuation, dangling parens, and extracts clean duration phrasing."""
    cleaned = phrase.strip(" ()-\t\n\r")
    # Fix phrases like "21) days" or "10) days" -> "21 days"
    cleaned = re.sub(r"^(\d+)\)\s*", r"\1 ", cleaned)
    if "(" not in cleaned and ")" in cleaned:
        cleaned = cleaned.replace(")", "")
    return cleaned.strip()


def extract_deadlines_from_clause(clause_text: str, clause_id=None) -> list[dict]:
    """
    Enhanced extraction of deadlines and date-bound obligations from clause text.
    Combines expanded regex patterns, legal terminology dictionaries, and calendar parsing.
    """
    if not clause_text or not clause_text.strip():
        return []

    nlp = get_spacy_ner()
    doc = nlp(clause_text)
    deadlines = []
    seen_keys = set()

    for sent in doc.sents:
        sent_str = sent.text.strip()
        if len(sent_str) < 10:
            continue

        # 1. Regex duration pattern matching (e.g. 5 days, 21 days, 30 days)
        for p in DURATION_PATTERNS:
            for match in re.finditer(p, sent_str):
                matched_phrase = match.group(0).strip()
                days = parse_relative_days(matched_phrase)
                if not days:
                    continue

                d_type = classify_deadline_type(sent_str)
                # Deduplicate by days within this clause
                key = f"{clause_id}_{d_type}_{days}"
                if key in seen_keys:
                    continue
                seen_keys.add(key)

                clean_phrase = clean_deadline_phrase(matched_phrase)
                clean_snippet = sent_str[:140] + "..." if len(sent_str) > 140 else sent_str
                confidence = "confident" if d_type != "notice_period" and days <= 180 else "needs_review"

                deadlines.append({
                    "clause_id": clause_id,
                    "deadline_type": d_type,
                    "raw_text": f"{clean_phrase} — {clean_snippet}",
                    "parsed_date": None,
                    "relative_days": days,
                    "confidence": confidence,
                })

        # 2. Check absolute calendar dates via spaCy NER (e.g. "January 15, 2026")
        for ent in sent.ents:
            if ent.label_ == "DATE":
                phrase = ent.text.strip()
                if len(phrase) < 5:
                    continue

                # Skip if this is a relative duration phrase (already captured in step 1)
                if re.search(r"\b(?:days?|weeks?|months?|hours?|calendar|business)\b", phrase, re.I):
                    continue

                # Only treat as genuine calendar date if containing month name or explicit date/year format
                is_calendar_candidate = bool(
                    re.search(r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b", phrase, re.I)
                    or re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", phrase)
                    or re.search(r"\b202[4-9]|203[0-9]\b", phrase)
                )
                if not is_calendar_candidate:
                    continue

                parsed_dt = None
                confidence = "needs_review"
                try:
                    parsed_candidate = date_parser.parse(phrase, fuzzy=False, default=None)
                    if parsed_candidate:
                        parsed_dt = parsed_candidate.date()
                        if re.search(r"\b202[4-9]|203[0-9]\b", phrase):
                            confidence = "confident"
                except Exception:
                    parsed_dt = None

                if not parsed_dt:
                    continue

                d_type = classify_deadline_type(sent_str)
                date_key = f"{clause_id}_{d_type}_{parsed_dt}"
                if date_key in seen_keys:
                    continue
                seen_keys.add(date_key)

                clean_phrase = clean_deadline_phrase(phrase)
                clean_snippet = sent_str[:140] + "..." if len(sent_str) > 140 else sent_str
                deadlines.append({
                    "clause_id": clause_id,
                    "deadline_type": d_type,
                    "raw_text": f"{clean_phrase} — {clean_snippet}",
                    "parsed_date": parsed_dt,
                    "relative_days": None,
                    "confidence": confidence,
                })

    return deadlines


def extract_all_deadlines(clauses: list[dict]) -> list[dict]:
    """
    Extracts deadlines across all clauses in a document, deduplicating
    and sorting with high-priority time-sensitive obligations first.
    """
    all_deadlines = []
    seen = set()

    for c in clauses:
        c_id = c.get("id")
        c_text = c.get("redacted_text") or c.get("text", "")
        found = extract_deadlines_from_clause(c_text, clause_id=c_id)
        for d in found:
            sig = (c_id, d.get("deadline_type"), d.get("relative_days"), str(d.get("parsed_date")))
            if sig not in seen:
                seen.add(sig)
                all_deadlines.append(d)

    # Sort deadlines by relative_days ascending (most immediate first)
    all_deadlines.sort(key=lambda x: (x.get("relative_days") or 9999))
    return all_deadlines
