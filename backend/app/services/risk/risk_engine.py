import json
from pathlib import Path

_config_cache = None

def get_risk_config() -> dict:
    global _config_cache
    if _config_cache is None:
        config_path = Path(__file__).resolve().parent / "risk_config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
    return _config_cache

def compute_clause_risk(
    clause_type: str,
    favorability_label: str,
    favorability_confidence: float = 1.0,
    prior_clause_type: str = None,
    config: dict = None,
) -> float:
    """
    Computes a 0-100 risk score for an individual clause based on transparent defaults.
    formula: base_weight * (severity_multiplier + sequence_bump) * confidence * 100
    """
    if config is None:
        config = get_risk_config()

    base = config["clause_type_base_weight"].get(clause_type, 0.5)
    multiplier = config["favorability_severity_multiplier"].get(favorability_label, 0.5)

    if prior_clause_type:
        pair_key = f"{prior_clause_type}->{clause_type}"
        seq_bump = config.get("sequence_adjustment_pairs", {}).get(pair_key, 0.0)
        multiplier += seq_bump

    multiplier = min(1.0, max(0.0, multiplier))
    conf = favorability_confidence if favorability_confidence is not None else 1.0
    conf = max(0.0, min(1.0, conf))

    score = round(base * multiplier * conf * 100, 1)
    return max(0.0, min(100.0, score))

def compute_document_risk(
    clause_scores: list[float],
    missing_clauses: list[dict],
    config: dict = None,
) -> float:
    """
    Computes document-level risk score combining average clause risk and missing clause penalties.
    """
    if config is None:
        config = get_risk_config()

    mean_clause_risk = sum(clause_scores) / len(clause_scores) if clause_scores else 0.0
    missing_penalty = sum(
        config["missing_clause_penalty_by_severity"].get(m.get("severity", "medium"), 0)
        for m in missing_clauses
    )
    missing_penalty = min(100.0, missing_penalty)

    w = config["composite_weights"]
    overall = (
        w["mean_clause_risk_weight"] * mean_clause_risk
        + w["missing_clause_penalty_weight"] * missing_penalty
    )
    return round(min(100.0, max(0.0, overall)), 1)

def compute_risk_band(score: float, config: dict = None) -> str:
    """
    Maps 0-100 risk score to low, medium, high, or critical band.
    """
    if config is None:
        config = get_risk_config()

    for band, (low, high) in config["risk_bands"].items():
        if low <= score <= high:
            return band
    return "critical" if score > 75 else "low"
