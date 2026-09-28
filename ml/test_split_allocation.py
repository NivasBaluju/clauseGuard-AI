import sys
from pathlib import Path
from collections import defaultdict
import random

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.enrich_corpus import RENTAL_SOURCES, OFFER_SOURCES, INSURANCE_SOURCES

def test_allocation(sources, doc_type_name, n_train, n_val, n_test):
    doc_types = {d["doc_id"]: set(c[1] for c in d["clauses"]) for d in sources}
    doc_favs = {d["doc_id"]: set(c[2] for c in d["clauses"]) for d in sources}
    all_types = sorted(list(set(c[1] for d in sources for c in d["clauses"])))
    all_favs = sorted(list(set(c[2] for d in sources for c in d["clauses"])))
    
    best_split = None
    best_score = -1000
    
    doc_ids = [d["doc_id"] for d in sources]
    
    for seed in range(5000):
        rng = random.Random(seed)
        shuffled = list(doc_ids)
        rng.shuffle(shuffled)
        
        train_ids = set(shuffled[:n_train])
        val_ids = set(shuffled[n_train:n_train + n_val])
        test_ids = set(shuffled[n_train + n_val:])
        
        train_types = set()
        for did in train_ids:
            train_types.update(doc_types[did])
            
        test_types = set()
        for did in test_ids:
            test_types.update(doc_types[did])
            
        val_types = set()
        for did in val_ids:
            val_types.update(doc_types[did])
            
        train_favs = set()
        for did in train_ids:
            train_favs.update(doc_favs[did])
            
        test_favs = set()
        for did in test_ids:
            test_favs.update(doc_favs[did])
            
        if not test_types.issubset(train_types):
            continue
        if not test_favs.issubset(train_favs):
            continue
            
        score = (len(train_types) * 10) + (len(test_types) * 5) + (len(val_types) * 2) + len(test_favs) * 10
        if score > best_score:
            best_score = score
            best_split = {
                "seed": seed,
                "train_ids": sorted(list(train_ids)),
                "val_ids": sorted(list(val_ids)),
                "test_ids": sorted(list(test_ids)),
                "train_types_count": len(train_types),
                "test_types_count": len(test_types),
                "all_types_count": len(all_types),
                "train_favs_count": len(train_favs),
                "test_favs_count": len(test_favs),
            }
            if len(train_types) == len(all_types) and len(test_types) == len(all_types) and len(test_favs) == len(all_favs):
                break
                
    print(f"\n=== Best Split for {doc_type_name.upper()} ===")
    print("Seed:", best_split["seed"])
    print(f"Train Docs ({len(best_split['train_ids'])}):", best_split["train_ids"])
    print(f"Val Docs ({len(best_split['val_ids'])}):", best_split["val_ids"])
    print(f"Test Docs ({len(best_split['test_ids'])}):", best_split["test_ids"])
    print(f"Types in Train: {best_split['train_types_count']}/{best_split['all_types_count']}")
    print(f"Types in Test: {best_split['test_types_count']}/{best_split['all_types_count']}")
    print(f"Favs in Train: {best_split['train_favs_count']}/{len(all_favs)}")
    print(f"Favs in Test: {best_split['test_favs_count']}/{len(all_favs)}")
    return best_split

if __name__ == "__main__":
    test_allocation(RENTAL_SOURCES, "rental_agreement", 17, 4, 4)
    test_allocation(OFFER_SOURCES, "job_offer_letter", 16, 3, 3)
    test_allocation(INSURANCE_SOURCES, "insurance_policy", 14, 3, 3)
