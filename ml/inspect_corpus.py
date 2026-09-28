import sys
from pathlib import Path
from collections import defaultdict

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.dataset_corpus_data import RENTAL_SOURCES
from ml.dataset_corpus_offer import OFFER_SOURCES
from ml.dataset_corpus_insurance import INSURANCE_SOURCES

for name, sources in [("rental", RENTAL_SOURCES), ("offer", OFFER_SOURCES), ("insurance", INSURANCE_SOURCES)]:
    print(f"\n=== {name.upper()} DOCS ({len(sources)}) ===")
    for d in sources:
        print(f"  {d['doc_id']}: {len(d['clauses'])} clauses | {d['source'][:60]}...")
