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

def redact(raw_text: str) -> tuple[str, list[dict]]:
    """
    Redact personally identifiable information (PII) before any model or frontend sees it.
    Returns: (redacted_text, pii_findings_list)
    """
    if not raw_text or not raw_text.strip():
        return raw_text, []

    analyzer, anonymizer = get_analyzer_and_anonymizer()
    
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
