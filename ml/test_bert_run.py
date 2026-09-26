import sys
import time
from pathlib import Path
import torch

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.bert.train_bert import train_bert_model

# Update batch_size in train_bert_model to 16
import ml.bert.train_bert as tb

t0 = time.time()
print("Starting BERT test with batch_size=16...")
meta = train_bert_model("insurance_policy", task="favorability", use_context=True, epochs=2)
dt = time.time() - t0
acc = meta["test_metrics"]["accuracy"]
f1 = meta["test_metrics"]["f1_macro"]
print(f"Completed in {dt:.1f}s | Acc={acc:.4f}, Macro-F1={f1:.4f}")
