import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ml.baseline.train_tfidf_lr import train_baseline
from ml.bert.train_bert import train_bert_model

def run_comprehensive_evaluation(doc_types=None, epochs: int = 2):
    """
    Executes the full evaluation comparison required by Sections 10, 11.4, and 11.5:
    Compares Baseline vs BERT-no-context vs BERT-windowed on the same held-out test split.
    """
    if doc_types is None:
        doc_types = ["rental_agreement", "job_offer_letter", "insurance_policy"]
    tasks = ["clause_type", "favorability"]

    comparison_results = {}

    for dt in doc_types:
        comparison_results[dt] = {}
        for t in tasks:
            print(f"\n=======================================================")
            print(f"Comparing Models for {dt} -> Task: {t}")
            print(f"=======================================================")

            # 1. Baseline (TF-IDF + LR)
            print("Running 1/3: Baseline (TF-IDF + LR)...")
            base_meta = train_baseline(dt, t)

            # 2. BERT Ablation (No Context)
            print(f"Running 2/3: BERT (No Context Ablation, {epochs} epochs)...")
            bert_no_ctx = train_bert_model(dt, task=t, use_context=False, epochs=epochs)

            # 3. BERT Primary (Context Windowed)
            print(f"Running 3/3: BERT (Context Windowed, {epochs} epochs)...")
            bert_win = train_bert_model(dt, task=t, use_context=True, epochs=epochs)

            # Record metrics
            task_comp = {
                "baseline_tfidf_lr": base_meta["test_metrics"],
                "bert_no_context": bert_no_ctx["test_metrics"],
                "bert_windowed": bert_win["test_metrics"],
            }

            # Determine winner
            models = ["baseline_tfidf_lr", "bert_no_context", "bert_windowed"]
            f1_scores = {m: task_comp[m]["f1_macro"] for m in models}
            winner = max(f1_scores, key=f1_scores.get)

            task_comp["selected_model"] = winner
            task_comp["delta_vs_baseline"] = round(f1_scores[winner] - f1_scores["baseline_tfidf_lr"], 4)
            task_comp["context_window_lift"] = round(f1_scores["bert_windowed"] - f1_scores["bert_no_context"], 4)

            comparison_results[dt][t] = task_comp

            print(f"\nResults for {dt} [{t}]:")
            print(f"  Baseline Macro-F1:     {f1_scores['baseline_tfidf_lr']:.4f}")
            print(f"  BERT-no-ctx Macro-F1:  {f1_scores['bert_no_context']:.4f}")
            print(f"  BERT-windowed Macro-F1:{f1_scores['bert_windowed']:.4f}")
            print(f"  --> Winner: {winner} (Lift over baseline: +{task_comp['delta_vs_baseline']:.4f})")

    summary_file = project_root / "ml" / "artifacts" / "model_comparison_report.json"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    
    existing_data = {}
    if summary_file.exists():
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception:
            existing_data = {}
    
    existing_data.update(comparison_results)
    
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)

    print(f"\n=======================================================")
    print(f"All model comparisons completed successfully!")
    print(f"Full report written to: {summary_file}")
    print(f"=======================================================")

    return existing_data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--document_type", type=str, default="all", choices=["rental_agreement", "job_offer_letter", "insurance_policy", "all"])
    parser.add_argument("--epochs", type=int, default=2)
    args = parser.parse_args()

    doc_types = ["rental_agreement", "job_offer_letter", "insurance_policy"] if args.document_type == "all" else [args.document_type]
    
    run_comprehensive_evaluation(doc_types=doc_types, epochs=args.epochs)
