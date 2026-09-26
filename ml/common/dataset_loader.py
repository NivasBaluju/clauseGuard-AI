import json
from pathlib import Path

def build_windowed_input(prev_clause_text: str | None, clause_text: str, next_clause_text: str | None, max_length: int = 256) -> str:
    """
    Constructs a single input sequence with the target clause explicitly marked,
    so the model can use surrounding context without losing track of which
    clause it's actually classifying.
    Truncates context first, preserving the target clause.
    """
    prev_part = (prev_clause_text or "").strip()
    next_part = (next_clause_text or "").strip()
    target_part = (clause_text or "").strip()

    # Budget rough character counts (approx 4 chars per token)
    max_chars = max_length * 4
    target_chars = len(target_part)

    if target_chars + len(prev_part) + len(next_part) > max_chars:
        # Keep target intact, trim context from outer edges
        remaining_budget = max(0, max_chars - target_chars - 30)
        half_budget = remaining_budget // 2
        if len(prev_part) > half_budget:
            prev_part = "..." + prev_part[-half_budget:]
        if len(next_part) > half_budget:
            next_part = next_part[:half_budget] + "..."

    return f"{prev_part} [TARGET] {target_part} [/TARGET] {next_part}".strip()

def load_jsonl_dataset(file_path: str | Path) -> list[dict]:
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                records.append(json.loads(line_str))
    return records

def save_jsonl_dataset(records: list[dict], file_path: str | Path):
    with open(file_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
