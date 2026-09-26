import sys
from pathlib import Path
from collections import defaultdict
import random

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.dataset_corpus_data import RENTAL_SOURCES
from ml.dataset_corpus_offer import OFFER_SOURCES
from ml.dataset_corpus_insurance import INSURANCE_SOURCES

def analyze_splits(sources, n_train, n_val, n_test, name):
    print(f"\n=======================================================")
    print(f"Optimizing Document Split for {name} ({len(sources)} docs)")
    print(f"Target: {n_train} train, {n_val} val, {n_test} test")
    
    # Clause types per document
    doc_types = {d["doc_id"]: set(c[1] for c in d["clauses"]) for d in sources}
    all_types = sorted(list(set(c[1] for d in sources for c in d["clauses"])))
    
    print(f"Total unique clause types: {len(all_types)}")
    for t in all_types:
        docs_with_t = [d["doc_id"] for d in sources if t in doc_types[d["doc_id"]]]
        print(f"  {t:32s}: {len(docs_with_t)} docs -> {docs_with_t[:3]}")

if __name__ == "__main__":
    analyze_splits(RENTAL_SOURCES, 17, 4, 4, "RENTAL")
    analyze_splits(OFFER_SOURCES, 16, 3, 3, "OFFER")
    analyze_splits(INSURANCE_SOURCES, 14, 3, 3, "INSURANCE")
