#!/usr/bin/env python3
"""Extract table rows from the selected Sterling FCR pages as structured JSON."""

from time import perf_counter

from common import (
    client,
    configured_prompt,
    from_root,
    load_config,
    log,
    normalize_page_number,
    page_numbers,
    save_json,
    upload,
)


def table_row_schema(source_pages: list[int]) -> dict[str, object]:
    """Build the bounded schema used for table-row extraction."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "source_pdf_page": {
                "type": "integer",
                "enum": source_pages,
                "description": "PDF viewer page on which this row is visible.",
            },
            "table_source_pdf_pages": {
                "type": "array",
                "items": {"type": "integer", "enum": source_pages},
                "description": (
                    "All PDF viewer pages containing this logical table, in order."
                ),
            },
            "table_title": {
                "type": "string",
                "description": "Exact visible table title, or an empty string.",
            },
            "table_number": {
                "type": "string",
                "description": "Exact visible table number, or an empty string.",
            },
            "units": {
                "type": "string",
                "description": "Exact visible units, or an empty string.",
            },
            "row_label": {
                "type": "string",
                "description": "Exact label for this logical table row.",
            },
            "cells": {
                "type": "array",
                "description": "Cells in left-to-right order, preserving blank values.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "column_label": {
                            "type": "string",
                            "description": "Exact column header carried across pages.",
                        },
                        "value": {
                            "type": "string",
                            "description": (
                                "Visible value verbatim, or an empty string."
                            ),
                        },
                        "state": {
                            "type": "string",
                            "enum": ["value", "blank", "dash", "zero", "illegible"],
                            "description": "Printed state of the source cell.",
                        },
                    },
                    "required": ["column_label", "value", "state"],
                },
            },
            "notes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Visible row or table footnotes.",
            },
        },
        "required": [
            "source_pdf_page",
            "table_source_pdf_pages",
            "table_title",
            "table_number",
            "units",
            "row_label",
            "cells",
            "notes",
        ],
    }


def main() -> None:
    """Run the structured table extraction experiment."""
    config = load_config()
    source = from_root(config["document"]["source_pdf"])
    source_pages = page_numbers(config["document"]["target_pages"])
    data_schema = table_row_schema(source_pages)
    api = client()
    started = perf_counter()
    uploaded = upload(api, source, "extract")
    api.extract.validate_schema(data_schema=data_schema)
    result = api.extract.run(
        file_input=uploaded.id,
        configuration={
            "data_schema": data_schema,
            "extraction_target": config["extract"]["target"],
            "tier": config["extract"]["tier"],
            "version": config["extract"]["version"],
            "parse_tier": config["extract"]["parse_tier"],
            "target_pages": config["document"]["target_pages"],
            "cite_sources": config["extract"]["cite_sources"],
            "confidence_scores": config["extract"]["confidence_scores"],
            "system_prompt": configured_prompt(config, "extract"),
        },
        polling_interval=config["cloud"]["poll_seconds"],
        max_interval=config["cloud"]["max_poll_seconds"],
        polling_timeout=config["cloud"]["timeout_seconds"],
    )
    output_root = config["output"]["root"]
    save_json(f"{output_root}/extract_json/raw_result.json", result)
    extracted_rows = (
        result.extract_result if isinstance(result.extract_result, list) else []
    )
    rows_with_provenance = []
    for row in extracted_rows:
        row_with_provenance = dict(row)
        row_with_provenance["source_pdf_page"] = normalize_page_number(
            row_with_provenance.get("source_pdf_page"), source_pages
        )
        row_with_provenance["table_source_pdf_pages"] = [
            normalize_page_number(page, source_pages)
            for page in row_with_provenance.get("table_source_pdf_pages", [])
        ]
        rows_with_provenance.append(row_with_provenance)
    save_json(f"{output_root}/extract_json/tables.json", rows_with_provenance)
    log(
        "extract_completed",
        job_id=result.id,
        elapsed_seconds=round(perf_counter() - started, 3),
        state="uploaded->completed",
    )


if __name__ == "__main__":
    main()
