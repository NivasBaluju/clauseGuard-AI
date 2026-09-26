"""
Corpus expansion script to ensure balanced, complete representation of all clause types
across the 67 genuine public documents in ClauseGuard AI.
"""

from pathlib import Path

# Path to corpus files
corpus_dir = Path(__file__).resolve().parent

print("Checking corpus directory:", corpus_dir)
