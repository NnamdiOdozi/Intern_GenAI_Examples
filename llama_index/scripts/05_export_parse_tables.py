#!/usr/bin/env python3
"""Export native LlamaParse table rows and CSV files with page provenance."""

from __future__ import annotations

import json

from common import from_root, load_config, log, save_json


def main() -> None:
    """Export every native table item from the saved Parse response.

    Returns
    -------
    None
        Writes one CSV per table, a row-oriented JSON file, and a manifest.
    """
    config = load_config()
    output_root = config["output"]["root"]
    raw_path = from_root(f"{output_root}/parse_markdown/raw_result.json")
    result = json.loads(raw_path.read_text(encoding="utf-8"))
    pages = (result.get("items") or {}).get("pages") or []
    csv_root = from_root(f"{output_root}/parse_tables/csv")
    csv_root.mkdir(parents=True, exist_ok=True)

    manifest = []
    native_rows = []
    table_number = 0
    for page in pages:
        page_number = page.get("page_number")
        table_on_page = 0
        for item in page.get("items") or []:
            if item.get("type") != "table":
                continue
            table_number += 1
            table_on_page += 1
            rows = item.get("rows") or []
            filename = f"page_{page_number:03d}_table_{table_on_page:02d}.csv"
            csv_text = item.get("csv") or ""
            (csv_root / filename).write_text(
                f"{csv_text}{'\n' if csv_text and not csv_text.endswith(chr(10)) else ''}",
                encoding="utf-8",
            )
            table = {
                "table_number": table_number,
                "source_pdf_page": page_number,
                "table_on_page": table_on_page,
                "rows": rows,
                "merged_from_pages": item.get("merged_from_pages"),
                "merged_into_page": item.get("merged_into_page"),
                "parse_concerns": item.get("parse_concerns") or [],
            }
            native_rows.append(table)
            manifest.append(
                {
                    **{key: value for key, value in table.items() if key != "rows"},
                    "csv_file": f"csv/{filename}",
                    "row_count": len(rows),
                    "column_counts": [len(row) for row in rows],
                }
            )

    save_json(f"{output_root}/parse_tables/native_rows.json", native_rows)
    save_json(f"{output_root}/parse_tables/manifest.json", manifest)
    log(
        "parse_tables_exported",
        page_count=len(pages),
        table_count=table_number,
        output_path=str(csv_root.parent),
        state="raw_parse->native_rows_and_csv",
    )


if __name__ == "__main__":
    main()
