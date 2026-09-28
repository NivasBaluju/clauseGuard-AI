import os
import sys
import json
import argparse
from pathlib import Path
import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ml.common.dataset_loader import load_jsonl_dataset, build_windowed_input
from ml.common.metrics import evaluate_predictions

MODEL_CHECKPOINT = "distilbert-base-uncased"

class ClauseDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels is not None:
            item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)

def train_bert_model(document_type: str, task: str = "clause_type", use_context: bool = True, epochs: int = 4):
    """
    Fine-tunes DistilBERT with either context-windowed input or clause_text alone.
    Uses native PyTorch optimization loop (no accelerate dependency required).
    """
    splits_dir = project_root / "ml" / "datasets" / document_type / "splits"
    train_records = load_jsonl_dataset(splits_dir / "train.jsonl")
    val_records = load_jsonl_dataset(splits_dir / "val.jsonl")
    test_records = load_jsonl_dataset(splits_dir / "test.jsonl")

    all_records = train_records + val_records + test_records
    
    if task == "clause_type":
        labels_list = sorted(list(set(r["clause_type"] for r in all_records)))
    else:
        labels_list = ["fair", "needs_review", "unfavorable"]

    label2id = {l: i for i, l in enumerate(labels_list)}
    id2label = {i: l for i, l in enumerate(labels_list)}
    num_labels = len(labels_list)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)
    if use_context:
        tokenizer.add_special_tokens({"additional_special_tokens": ["[TARGET]", "[/TARGET]"]})

    def prepare_data(records):
        texts = []
        labels = []
        for r in records:
            if use_context:
                w_text = build_windowed_input(r.get("prev_clause_text"), r["clause_text"], r.get("next_clause_text"))
            else:
                w_text = r["clause_text"]
            
            l_val = r["clause_type"] if task == "clause_type" else r["adjudicated_favorability"]
            if l_val in label2id:
                texts.append(w_text)
                labels.append(label2id[l_val])
        return texts, labels

    train_texts, train_labels = prepare_data(train_records + val_records)
    test_texts, test_labels = prepare_data(test_records)

    if not torch.cuda.is_available() and len(train_texts) > 500:
        import random
        by_class = {}
        for txt, lbl in zip(train_texts, train_labels):
            by_class.setdefault(lbl, []).append(txt)
        sub_texts, sub_labels = [], []
        samples_per_class = max(10, 500 // max(1, len(by_class)))
        for lbl, txts in by_class.items():
            chosen = random.sample(txts, min(samples_per_class, len(txts)))
            sub_texts.extend(chosen)
            sub_labels.extend([lbl] * len(chosen))
        train_texts, train_labels = sub_texts, sub_labels

    if torch.get_num_threads() < 8:
        torch.set_num_threads(min(12, os.cpu_count() or 8))

    max_len = 96
    train_enc = tokenizer(train_texts, truncation=True, padding=True, max_length=max_len)
    test_enc = tokenizer(test_texts, truncation=True, padding=True, max_length=max_len)

    train_ds = ClauseDataset(train_enc, train_labels)
    test_ds = ClauseDataset(test_enc, test_labels)

    batch_size = 32 if len(train_ds) >= 32 else 16
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_CHECKPOINT,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id,
    )
    if use_context:
        model.resize_token_embeddings(len(tokenizer))

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)

    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"]
            attention_mask = batch["attention_mask"]
            labels = batch["labels"]
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"      Epoch {epoch+1}/{epochs} - loss: {epoch_loss/max(1, len(train_loader)):.4f}")

    model.eval()
    all_preds = []
    all_trues = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"]
            attention_mask = batch["attention_mask"]
            labels = batch["labels"]
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1).cpu().numpy()
            all_preds.extend(preds)
            all_trues.extend(labels.cpu().numpy())

    eval_results = evaluate_predictions(all_trues, all_preds, labels=list(range(num_labels)), target_names=labels_list)

    context_tag = "windowed" if use_context else "nocontext"
    output_dir = project_root / "ml" / "artifacts" / document_type / f"bert_{task}_{context_tag}"
    final_save_path = output_dir / "final"
    final_save_path.mkdir(parents=True, exist_ok=True)

    model.save_pretrained(str(final_save_path))
    tokenizer.save_pretrained(str(final_save_path))

    meta = {
        "document_type": document_type,
        "task": task,
        "use_context": use_context,
        "model_version": f"bert-{context_tag}-{task}-v1",
        "num_labels": num_labels,
        "label2id": label2id,
        "id2label": id2label,
        "test_metrics": {
            "accuracy": eval_results["accuracy"],
            "f1_macro": eval_results["f1_macro"],
            "f1_weighted": eval_results["f1_weighted"],
            "precision_macro": eval_results["precision_macro"],
            "recall_macro": eval_results["recall_macro"],
        },
        "artifact_path": str(final_save_path),
    }

    with open(final_save_path / "model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return meta

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--document_type", type=str, default="rental_agreement", choices=["rental_agreement", "job_offer_letter", "insurance_policy", "all"])
    parser.add_argument("--task", type=str, default="all", choices=["clause_type", "favorability", "all"])
    parser.add_argument("--use_context", type=str, default="true")
    parser.add_argument("--epochs", type=int, default=4)
    args = parser.parse_args()

    use_ctx = args.use_context.lower() in ["true", "1", "yes"]
    doc_types = ["rental_agreement", "job_offer_letter", "insurance_policy"] if args.document_type == "all" else [args.document_type]
    tasks = ["clause_type", "favorability"] if args.task == "all" else [args.task]

    for dt in doc_types:
        for t in tasks:
            print(f"\n=======================================================")
            print(f"Training BERT for {dt} [{t}] (use_context={use_ctx})...")
            print(f"=======================================================")
            meta = train_bert_model(dt, task=t, use_context=use_ctx, epochs=args.epochs)
            print(f"Test Accuracy: {meta['test_metrics']['accuracy']:.4f} | F1-Macro: {meta['test_metrics']['f1_macro']:.4f}")
