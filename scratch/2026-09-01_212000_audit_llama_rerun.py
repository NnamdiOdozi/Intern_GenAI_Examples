"""Summarize the focused Llama Parse and Extract rerun without changing outputs."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "llama_index/output/rerun_11_14_16_19"
rows = json.loads((RUN / "extract_json/tables.json").read_text(encoding="utf-8"))
markdown = (RUN / "parse_markdown/result.md").read_text(encoding="utf-8")

groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
for row in rows:
    key = (str(row["table_number"]), str(row["table_title"]))
    groups[key].append(row)

print(f"Extract rows: {len(rows)}")
print(f"Logical table labels: {len(groups)}")
print(f"Source-page row counts: {dict(sorted(Counter(row['source_pdf_page'] for row in rows).items()))}")
print(f"Cell states: {dict(sorted(Counter(cell['state'] for row in rows for cell in row['cells']).items()))}")
print("\nExtract inventory:")
for (number, title), table_rows in sorted(groups.items()):
    pages = sorted({page for row in table_rows for page in row["table_source_pdf_pages"]})
    source_pages = sorted({row["source_pdf_page"] for row in table_rows})
    print(
        f"- {number or '(none)'} | {title} | rows={len(table_rows)} "
        f"| table_pages={pages} | row_pages={source_pages}"
    )

print("\nCritical Markdown markers:")
for marker in (
    "2022",
    "Table 7",
    "Table 8",
    "Source PDF page 19",
):
    print(f"- {marker}: {marker in markdown}")

print("\nCritical Extract markers:")
serialized = json.dumps(rows)
for marker in ("2022", "Table 7", "Table 8"):
    print(f"- {marker}: {marker in serialized}")

bad_pages = [
    (row["table_number"], row["row_label"], row["source_pdf_page"])
    for row in rows
    if row["source_pdf_page"] not in {11, 12, 13, 14, 16, 17, 18, 19}
]
print(f"\nRows with invalid provenance: {len(bad_pages)}")
