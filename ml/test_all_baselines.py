import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.baseline.train_tfidf_lr import train_baseline

for dt in ["rental_agreement", "job_offer_letter", "insurance_policy"]:
    for task in ["clause_type", "favorability"]:
        try:
            res = train_baseline(dt, task)
            acc = res["test_metrics"]["accuracy"]
            f1 = res["test_metrics"]["f1_macro"]
            print(f"{dt} [{task}]: Acc={acc:.4f}, Macro-F1={f1:.4f}")
        except Exception as e:
            print(f"ERROR on {dt} [{task}]:", e)
