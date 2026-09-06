"""Audit full-document LlamaParse table coverage and focused-run consistency."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FULL_ROOT = ROOT / "llama_index/output/full_document_20260901"
FOCUSED_ROOT = ROOT / "llama_index/output/rerun_11_14_16_19"


def load_table_items(raw_path: Path) -> tuple[list[int], list[dict[str, object]]]:
    """Load page numbers and native table items from one Parse response.

    Parameters
    ----------
    raw_path : pathlib.Path
        Saved LlamaParse response containing an ``items`` expansion.

    Returns
    -------
    tuple[list[int], list[dict[str, object]]]
        Returned page numbers and table items carrying source-page provenance.
    """
    result = json.loads(raw_path.read_text(encoding="utf-8"))
    pages = (result.get("items") or {}).get("pages") or []
    tables = []
    for page in pages:
        page_number = page.get("page_number")
        for item in page.get("items") or []:
            if item.get("type") == "table":
                tables.append({"source_pdf_page": page_number, **item})
    return [page.get("page_number") for page in pages], tables


full_pages, full_tables = load_table_items(
    FULL_ROOT / "parse_markdown/raw_result.json"
)
focused_pages, focused_tables = load_table_items(
    FOCUSED_ROOT / "parse_markdown/raw_result.json"
)
full_result = json.loads(
    (FULL_ROOT / "parse_markdown/raw_result.json").read_text(encoding="utf-8")
)
markdown_by_page = {
    page.get("page_number"): page.get("markdown") or ""
    for page in (full_result.get("markdown") or {}).get("pages") or []
}
csv_row_matches = sum(
    list(csv.reader(StringIO(table.get("csv") or ""))) == (table.get("rows") or [])
    for table in full_tables
)
markdown_item_matches = sum(
    not table.get("md")
    or table.get("md") in markdown_by_page.get(table["source_pdf_page"], "")
    for table in full_tables
)

concerns = Counter(
    concern.get("type", "unknown")
    for table in full_tables
    for concern in table.get("parse_concerns") or []
)
concern_pages: dict[str, set[int]] = defaultdict(set)
for table in full_tables:
    for concern in table.get("parse_concerns") or []:
        concern_pages[concern.get("type", "unknown")].add(table["source_pdf_page"])
empty_tables = [table for table in full_tables if not table.get("rows")]
uneven_tables = []
for table in full_tables:
    widths = [len(row) for row in table.get("rows") or []]
    if len(set(widths)) > 1:
        uneven_tables.append((table["source_pdf_page"], widths))

tables_by_page: dict[int, int] = Counter(
    table["source_pdf_page"] for table in full_tables
)
full_by_page: dict[int, list[object]] = defaultdict(list)
focused_by_page: dict[int, list[object]] = defaultdict(list)
for table in full_tables:
    full_by_page[table["source_pdf_page"]].append(table.get("rows"))
for table in focused_tables:
    focused_by_page[table["source_pdf_page"]].append(table.get("rows"))

print(f"Pages returned: {len(full_pages)} ({full_pages[0]}-{full_pages[-1]})")
print(f"Missing pages: {sorted(set(range(1, 53)) - set(full_pages))}")
print(f"Native tables: {len(full_tables)}")
print(f"Pages with tables: {len(tables_by_page)}")
print(f"Native rows: {sum(len(table.get('rows') or []) for table in full_tables)}")
print(f"CSV files exactly matching native rows: {csv_row_matches}/{len(full_tables)}")
print(
    "Native Markdown tables present in page Markdown: "
    f"{markdown_item_matches}/{len(full_tables)}"
)
print(
    "Empty tables: "
    f"{[(table['source_pdf_page'], table.get('md', '')[:80]) for table in empty_tables]}"
)
print(f"Tables with uneven row widths: {uneven_tables}")
print(f"Parse concerns: {dict(sorted(concerns.items()))}")
print(
    "Concern pages: "
    f"{ {name: sorted(pages) for name, pages in sorted(concern_pages.items())} }"
)
print(
    "Merged table fields populated: "
    f"{sum(bool(table.get('merged_from_pages') or table.get('merged_into_page')) for table in full_tables)}"
)
print("Focused-page comparison:")
for page in focused_pages:
    full_page_tables = full_by_page[page]
    focused_page_tables = focused_by_page[page]
    print(
        f"- page {page}: full={len(full_page_tables)} focused={len(focused_page_tables)} "
        f"exact_rows={full_page_tables == focused_page_tables}"
    )
    for table_index, (full_rows, focused_rows) in enumerate(
        zip(full_page_tables, focused_page_tables, strict=True), start=1
    ):
        if full_rows == focused_rows:
            continue
        print(
            f"  table {table_index}: full_rows={len(full_rows)} "
            f"focused_rows={len(focused_rows)}"
        )
        for row_index, (full_row, focused_row) in enumerate(
            zip(full_rows, focused_rows), start=1
        ):
            if full_row != focused_row:
                print(f"    row {row_index} full={full_row!r}")
                print(f"    row {row_index} focused={focused_row!r}")
