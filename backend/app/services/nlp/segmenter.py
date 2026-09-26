import re
import spacy
import logging

logger = logging.getLogger(__name__)

_nlp = None

def get_spacy():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer"])
            _nlp.enable_pipe("senter")
        except Exception:
            _nlp = spacy.blank("en")
            _nlp.add_pipe("sentencizer")
    return _nlp

# Common heading / clause demarcation patterns
CLAUSE_HEADING_PATTERNS = [
    # Article / Section / Clause / Paragraph headers: e.g. "SECTION 4.1", "ARTICLE IV", "Clause 2:"
    r"^(?:\s*)(?:ARTICLE|SECTION|CLAUSE|PARAGRAPH)\s+[0-9IVXLCDM]+(?:\.[0-9]+)*[:.\s-]*",
    # Numbered list items at line start: e.g. "1.", "1.1", "(1)", "1)"
    r"^(?:\s*)(?:\([0-9]+\)|[0-9]+(?:\.[0-9]+)*[.)\s])\s+",
    # Lettered items: e.g. "(a)", "A.", "a)"
    r"^(?:\s*)(?:\([a-zA-Z]\)|[a-zA-Z][.)\s])\s+",
    # Common bold / uppercase section title markers: e.g. "TERMINATION:", "SECURITY DEPOSIT - "
    r"^(?:\s*)(?:[A-Z\s]{3,40})(?:\s*[:\-\u2013\u2014])\s+",
]

# Offer letter patterns: often bullet-based or salutation/header sections
OFFER_LETTER_PATTERNS = [
    r"^(?:\s*)(?:Position|Salary|Compensation|Benefits|Start Date|At-Will|Confidentiality|Contingencies|Vacation|Termination|Governing Law)[:\-\s]+",
    r"^(?:\s*)(?:[\u2022\u2023\u25E6\u2043\u2219*-])\s+",
]

# Insurance policy patterns: Coverage, Exclusion, Endorsement, Condition
INSURANCE_PATTERNS = [
    r"^(?:\s*)(?:SECTION\s+[A-Z0-9]+|COVERAGE\s+[A-Z0-9]+|EXCLUSIONS?|CONDITIONS?|ENDORSEMENT)[:.\s-]*",
    r"^(?:\s*)(?:[0-9]+(?:\.[0-9]+)*)\s+",
]

def segment_clauses(text: str, document_type: str = "rental_agreement") -> list[dict]:
    """
    Segments document text into sequential clauses with start/end offsets and clause_index.
    Uses regex heading split refined with spaCy sentence boundary detection.
    
    Returns list of dicts:
    [
        {
            "clause_index": 0,
            "text": "...",
            "start_offset": 0,
            "end_offset": 120
        }, ...
    ]
    """
    if not text or not text.strip():
        return []

    # Select heading patterns based on document type
    patterns = list(CLAUSE_HEADING_PATTERNS)
    if document_type == "job_offer_letter":
        patterns = OFFER_LETTER_PATTERNS + patterns
    elif document_type == "insurance_policy":
        patterns = INSURANCE_PATTERNS + patterns

    combined_regex = re.compile("|".join(f"(?:{p})" for p in patterns), flags=re.MULTILINE)
    
    # Find all heading match positions
    matches = list(combined_regex.finditer(text))
    
    segments = []
    if matches:
        # Text before first heading (if substantial)
        if matches[0].start() > 40:
            pre_chunk = text[:matches[0].start()].strip()
            if len(pre_chunk) > 30:
                segments.append((text[:matches[0].start()], 0, matches[0].start()))

        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            clause_str = text[start:end].strip()
            if len(clause_str) > 15:  # Ignore tiny noise headers
                segments.append((clause_str, start, end))
    else:
        # Fallback to paragraph splitting if no numbered headings found
        paragraphs = re.split(r"\n\s*\n+", text)
        cur_pos = 0
        for p in paragraphs:
            p_strip = p.strip()
            if not p_strip:
                cur_pos += len(p)
                continue
            idx = text.find(p_strip, cur_pos)
            if idx == -1:
                idx = cur_pos
            segments.append((p_strip, idx, idx + len(p_strip)))
            cur_pos = idx + len(p_strip)

    # Refine overly long segments (> 800 chars) using spaCy sentence boundaries
    nlp = get_spacy()
    refined_clauses = []
    clause_counter = 0

    for seg_text, s_off, e_off in segments:
        seg_clean = seg_text.strip()
        if len(seg_clean) < 20:
            continue

        # If segment is moderately sized (standard clause), keep as single unit
        if len(seg_clean) <= 1200:
            refined_clauses.append({
                "clause_index": clause_counter,
                "text": seg_clean,
                "start_offset": s_off,
                "end_offset": e_off,
            })
            clause_counter += 1
        else:
            # Segment is very long (e.g. an entire mega-section); split on sentence boundaries
            doc = nlp(seg_clean)
            cur_chunk = []
            chunk_start = s_off
            cur_len = 0
            
            for sent in doc.sents:
                s_text = sent.text.strip()
                if not s_text:
                    continue
                cur_chunk.append(s_text)
                cur_len += len(s_text)
                if cur_len >= 500:
                    merged = " ".join(cur_chunk)
                    refined_clauses.append({
                        "clause_index": clause_counter,
                        "text": merged,
                        "start_offset": chunk_start,
                        "end_offset": chunk_start + len(merged),
                    })
                    clause_counter += 1
                    cur_chunk = []
                    cur_len = 0
                    chunk_start = chunk_start + len(merged)
                    
            if cur_chunk:
                merged = " ".join(cur_chunk)
                refined_clauses.append({
                    "clause_index": clause_counter,
                    "text": merged,
                    "start_offset": chunk_start,
                    "end_offset": chunk_start + len(merged),
                })
                clause_counter += 1

    return refined_clauses
