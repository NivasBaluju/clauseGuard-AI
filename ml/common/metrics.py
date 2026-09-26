import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
    cohen_kappa_score,
)

def evaluate_predictions(y_true, y_pred, labels=None, target_names=None):
    """
    Evaluates predictions returning comprehensive metrics:
    accuracy, macro-F1, per-class precision/recall, and confusion matrix.
    """
    acc = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    prec_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
    rec_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    report = classification_report(
        y_true, y_pred, labels=labels, target_names=target_names, zero_division=0, output_dict=True
    )

    return {
        "accuracy": round(acc, 4),
        "f1_macro": round(f1_macro, 4),
        "f1_weighted": round(f1_weighted, 4),
        "precision_macro": round(prec_macro, 4),
        "recall_macro": round(rec_macro, 4),
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }

def compute_inter_annotator_agreement(annotator_1: list, annotator_2: list) -> float:
    """
    Computes Cohen's Kappa score between two independent annotators.
    """
    return round(cohen_kappa_score(annotator_1, annotator_2), 4)
