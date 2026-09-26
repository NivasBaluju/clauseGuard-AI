import os
import sys
import json
import argparse
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ml.common.dataset_loader import load_jsonl_dataset
from ml.common.metrics import evaluate_predictions

def train_baseline(document_type: str, task: str = "clause_type"):
    """
    Trains TF-IDF + Logistic Regression baseline model on target clause_text alone (no context).
    task: 'clause_type' or 'favorability'
    """
    data_dir = project_root / "ml" / "datasets" / document_type / "splits"
    train_records = load_jsonl_dataset(data_dir / "train.jsonl")
    val_records = load_jsonl_dataset(data_dir / "val.jsonl")
    test_records = load_jsonl_dataset(data_dir / "test.jsonl")

    # Combine train and val for training, test for evaluation
    train_val_records = train_records + val_records

    X_train = [r["clause_text"] for r in train_val_records]
    y_train = [r["clause_type"] if task == "clause_type" else r["adjudicated_favorability"] for r in train_val_records]

    X_test = [r["clause_text"] for r in test_records]
    y_test = [r["clause_type"] if task == "clause_type" else r["adjudicated_favorability"] for r in test_records]

    unique_labels = sorted(list(set(y_train + y_test)))

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_df=1.0, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
    ])

    param_grid = {
        "tfidf__max_features": [500, 1000, 2000],
        "clf__C": [0.1, 1.0, 5.0, 10.0],
    }

    # If small sample size, cv=min(3, min_class_count)
    from collections import Counter
    min_class_count = min(Counter(y_train).values()) if y_train else 2
    cv = min(3, len(X_train) // max(1, len(unique_labels)), min_class_count)
    cv = max(2, cv)

    search = GridSearchCV(pipeline, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1, error_score="raise")
    search.fit(X_train, y_train)

    best_model = search.best_estimator_

    # Evaluate on held-out test split
    y_pred = best_model.predict(X_test)
    eval_results = evaluate_predictions(y_test, y_pred, labels=unique_labels, target_names=unique_labels)

    # Save artifact
    artifact_dir = project_root / "ml" / "artifacts" / document_type
    artifact_dir.mkdir(parents=True, exist_ok=True)
    model_filename = f"baseline_tfidf_lr_{task}.joblib"
    joblib.dump(best_model, artifact_dir / model_filename)

    results_summary = {
        "document_type": document_type,
        "task": task,
        "best_params": search.best_params_,
        "test_metrics": {
            "accuracy": eval_results["accuracy"],
            "f1_macro": eval_results["f1_macro"],
            "f1_weighted": eval_results["f1_weighted"],
            "precision_macro": eval_results["precision_macro"],
            "recall_macro": eval_results["recall_macro"],
        },
        "artifact_path": str(artifact_dir / model_filename),
    }

    return results_summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--document_type", type=str, default="rental_agreement", choices=["rental_agreement", "job_offer_letter", "insurance_policy", "all"])
    parser.add_argument("--task", type=str, default="all", choices=["clause_type", "favorability", "all"])
    args = parser.parse_args()

    doc_types = ["rental_agreement", "job_offer_letter", "insurance_policy"] if args.document_type == "all" else [args.document_type]
    tasks = ["clause_type", "favorability"] if args.task == "all" else [args.task]

    all_results = []
    for dt in doc_types:
        for t in tasks:
            print(f"\n--- Training Baseline (TF-IDF + LR) for {dt} [{t}] ---")
            res = train_baseline(dt, t)
            print(f"Accuracy: {res['test_metrics']['accuracy']:.4f} | F1-Macro: {res['test_metrics']['f1_macro']:.4f}")
            all_results.append(res)

    results_file = project_root / "ml" / "artifacts" / "baseline_evaluation_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nBaseline training complete. Results saved to {results_file}")
