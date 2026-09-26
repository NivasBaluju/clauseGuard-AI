import os
import sys
import json
import logging
from pathlib import Path
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.services.nlp.classifier_baseline import predict_baseline

def build_windowed_input(prev_clause_text: str | None, clause_text: str, next_clause_text: str | None, max_length: int = 256) -> str:
    prev_part = (prev_clause_text or "").strip()
    next_part = (next_clause_text or "").strip()
    target_part = (clause_text or "").strip()

    max_chars = max_length * 4
    target_chars = len(target_part)

    if target_chars + len(prev_part) + len(next_part) > max_chars:
        remaining_budget = max(0, max_chars - target_chars - 30)
        half_budget = remaining_budget // 2
        if len(prev_part) > half_budget:
            prev_part = "..." + prev_part[-half_budget:]
        if len(next_part) > half_budget:
            next_part = next_part[:half_budget] + "..."

    return f"{prev_part} [TARGET] {target_part} [/TARGET] {next_part}".strip()

logger = logging.getLogger(__name__)

_bert_models = {}
_bert_tokenizers = {}
_bert_metadata = {}

project_root = Path(__file__).resolve().parents[4]

def get_bert_model_and_tokenizer(document_type: str, task: str = "clause_type"):
    key = f"{document_type}_{task}"
    if key in _bert_models:
        return _bert_models[key], _bert_tokenizers[key], _bert_metadata[key]

    ml_dir = project_root / "ml" / "artifacts" / document_type
    report_file = project_root / "ml" / "artifacts" / "model_comparison_report.json"
    
    # Check evaluation report to see which model won for this task
    winning_model_type = None
    if report_file.exists():
        try:
            with open(report_file, "r", encoding="utf-8") as rf:
                report = json.load(rf)
                winning_model_type = report.get(document_type, {}).get(task, {}).get("selected_model")
        except Exception:
            pass

    # If baseline won for this task (e.g. clause_type with strong keyword n-grams), return None so caller uses baseline
    if winning_model_type == "baseline_tfidf_lr":
        return None, None, {"model_version": f"baseline-tfidf-lr-{task}-v1"}

    # Otherwise look for BERT final weights
    candidate_paths = [
        ml_dir / f"bert_{task}_nocontext" / "final",
        ml_dir / f"bert_{task}_windowed" / "final",
    ]

    model_dir = None
    for cp in candidate_paths:
        if (cp / "model.safetensors").exists() or (cp / "pytorch_model.bin").exists():
            model_dir = cp
            break

    if not model_dir:
        return None, None, None

    try:
        tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
        model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
        model.eval()

        meta_path = model_dir / "model_metadata.json"
        metadata = {}
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

        _bert_models[key] = model
        _bert_tokenizers[key] = tokenizer
        _bert_metadata[key] = metadata
        return model, tokenizer, metadata
    except Exception as e:
        logger.error(f"Error loading BERT model from {model_dir}: {e}")
        return None, None, None

def classify_clause(
    clause_text: str,
    document_type: str,
    prev_clause_text: str = None,
    next_clause_text: str = None,
    task: str = "clause_type",
) -> tuple[str, float, str]:
    """
    Classifies a clause using the fine-tuned BERT model (with context windowing).
    Gracefully falls back to TF-IDF+LR baseline if BERT is not yet loaded.
    
    Returns: (predicted_label, confidence_score, model_version)
    """
    model, tokenizer, meta = get_bert_model_and_tokenizer(document_type, task)

    if model is None:
        # Fallback to Baseline TF-IDF + Logistic Regression
        label, conf = predict_baseline(clause_text, document_type, task)
        return label, conf, f"baseline-tfidf-lr-{task}"

    use_context = meta.get("use_context", True)
    if use_context:
        input_text = build_windowed_input(prev_clause_text, clause_text, next_clause_text)
    else:
        input_text = clause_text

    try:
        inputs = tokenizer(input_text, truncation=True, max_length=256, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)[0]
            pred_idx = torch.argmax(probs).item()
            conf = round(float(probs[pred_idx].item()), 4)

        id2label = meta.get("id2label", {})
        # id2label keys in json might be strings
        pred_label = id2label.get(str(pred_idx)) or id2label.get(pred_idx, "unknown")
        model_version = meta.get("model_version", f"bert-{task}-v1")
        return pred_label, conf, model_version
    except Exception as e:
        logger.error(f"Error running BERT inference: {e}")
        label, conf = predict_baseline(clause_text, document_type, task)
        return label, conf, f"baseline-tfidf-lr-{task}"
