#!/usr/bin/env python3
"""Parse the selected Sterling FCR pages into an XLSX workbook."""

from time import perf_counter

import requests
from common import (
    client,
    configured_prompt,
    from_root,
    load_config,
    log,
    save_bytes,
    save_json,
    upload,
)


def main() -> None:
    """Run the spreadsheet parsing experiment."""
    config = load_config()
    source = from_root(config["document"]["source_pdf"])
    target_pages = config["document"]["target_pages"]
    api = client()
    started = perf_counter()
    uploaded = upload(api, source, "parse")
    result = api.parsing.parse(
        file_id=uploaded.id,
        tier=config["parse"]["tier"],
        version=config["parse"]["version"],
        page_ranges={"target_pages": target_pages},
        agentic_options={"custom_prompt": configured_prompt(config, "parse")},
        output_options={
            "tables_as_spreadsheet": {"enable": True, "guess_sheet_name": True}
        },
        expand=["xlsx_content_metadata"],
        polling_interval=config["cloud"]["poll_seconds"],
        max_interval=config["cloud"]["max_poll_seconds"],
        timeout=config["cloud"]["timeout_seconds"],
    )
    output_root = config["output"]["root"]
    save_json(f"{output_root}/parse_spreadsheet/raw_result.json", result)
    content_metadata = result.result_content_metadata or {}
    metadata_keys = sorted(content_metadata)
    log(
        "spreadsheet_parse_completed",
        job_id=result.job.id,
        artifact_keys=metadata_keys,
        elapsed_seconds=round(perf_counter() - started, 3),
        state="uploaded->parsed",
    )
    xlsx = content_metadata.get("xlsx_content_metadata")
    if not xlsx:
        xlsx = next(
            (
                artifact
                for name, artifact in content_metadata.items()
                if "xlsx" in name.lower()
            ),
            None,
        )
    if not xlsx or not xlsx.presigned_url:
        message = (
            f"Parse job {result.job.id} returned no XLSX download URL. "
            f"Available artifact keys: {metadata_keys}"
        )
        raise ValueError(message)
    response = requests.get(
        xlsx.presigned_url,
        timeout=config["cloud"]["download_timeout_seconds"],
    )
    response.raise_for_status()
    save_bytes(f"{output_root}/parse_spreadsheet/tables.xlsx", response.content)
    log(
        "spreadsheet_completed",
        job_id=result.job.id,
        elapsed_seconds=round(perf_counter() - started, 3),
        size_bytes=xlsx.size_bytes,
        state="uploaded->downloaded",
    )


if __name__ == "__main__":
    main()
