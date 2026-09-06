"""Inventory table items and source pages in the completed Parse response."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "llama_index/output/rerun_11_14_16_19/parse_markdown/raw_result.json"
result = json.loads(RAW.read_text(encoding="utf-8"))
pages = (result.get("items") or {}).get("pages") or []

print(f"Item pages: {len(pages)}")
print(f"Page numbers: {[page.get('page_number') for page in pages]}")

type_counts: Counter[str] = Counter()
table_count = 0
for page in pages:
    page_number = page.get("page_number")
    for item in page.get("items") or []:
        item_type = str(item.get("type", "unknown"))
        type_counts[item_type] += 1
        if item_type != "table":
            continue
        table_count += 1
        markdown = str(item.get("md") or item.get("markdown") or "")
        first_line = next((line for line in markdown.splitlines() if line.strip()), "")
        rows = item.get("rows") or []
        print(
            f"- table={table_count} page={page_number} rows={len(rows)} "
            f"first_line={first_line[:180]!r}"
        )

print(f"Item types: {dict(sorted(type_counts.items()))}")
print(f"Tables: {table_count}")
