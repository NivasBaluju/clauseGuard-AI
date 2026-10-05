import logging
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

logger = logging.getLogger(__name__)

ENTITIES_TO_REDACT = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "LOCATION",
    "US_SSN",
    "CREDIT_CARD",
    "IBAN_CODE",
    "IP_ADDRESS",
]

_analyzer = None
_anonymizer = None

def get_analyzer_and_anonymizer():
    global _analyzer, _anonymizer
    if _analyzer is None:
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        config = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
        }
        provider = NlpEngineProvider(nlp_configuration=config)
        nlp_engine = provider.create_engine()
        _analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
    if _anonymizer is None:
        _anonymizer = AnonymizerEngine()
    return _analyzer, _anonymizer

def redact(raw_text: str, chunk_size: int = 4000) -> tuple[str, list[dict]]:
    """
    Redact personally identifiable information (PII) before any model or frontend sees it.
    Uses lightweight chunked processing for documents exceeding 4,000 characters
    to prevent spaCy from allocating excessive memory (>200MB) on 20+ page documents.
    Returns: (redacted_text, pii_findings_list)
    """
    if not raw_text or not raw_text.strip():
        return raw_text, []

    analyzer, anonymizer = get_analyzer_and_anonymizer()
    
    if len(raw_text) <= chunk_size:
        results = analyzer.analyze(
            text=raw_text,
            entities=ENTITIES_TO_REDACT,
            language="en"
        )
        anonymized = anonymizer.anonymize(
            text=raw_text,
            analyzer_results=results
        )
        findings = [
            {
                "entity_type": r.entity_type,
                "start": r.start,
                "end": r.end,
                "confidence": float(r.score)
            }
            for r in results
        ]
        return anonymized.text, findings

    all_findings = []
    redacted_parts = []
    current_pos = 0
    lines = raw_text.splitlines(keepends=True)
    current_chunk = []
    current_len = 0

    for line in lines:
        if current_len + len(line) > chunk_size and current_chunk:
            chunk_str = "".join(current_chunk)
            results = analyzer.analyze(text=chunk_str, entities=ENTITIES_TO_REDACT, language="en")
            anon = anonymizer.anonymize(text=chunk_str, analyzer_results=results)
            redacted_parts.append(anon.text)
            for r in results:
                all_findings.append({
                    "entity_type": r.entity_type,
                    "start": current_pos + r.start,
                    "end": current_pos + r.end,
                    "confidence": float(r.score)
                })
            current_pos += len(chunk_str)
            current_chunk = [line]
            current_len = len(line)
        else:
            current_chunk.append(line)
            current_len += len(line)

    if current_chunk:
        chunk_str = "".join(current_chunk)
        results = analyzer.analyze(text=chunk_str, entities=ENTITIES_TO_REDACT, language="en")
        anon = anonymizer.anonymize(text=chunk_str, analyzer_results=results)
        redacted_parts.append(anon.text)
        for r in results:
            all_findings.append({
                "entity_type": r.entity_type,
                "start": current_pos + r.start,
                "end": current_pos + r.end,
                "confidence": float(r.score)
            })

    return "".join(redacted_parts), all_findings
