#!/usr/bin/env python3
"""Parse the selected Sterling FCR pages into Markdown and raw JSON."""

from time import perf_counter

from common import (
    client,
    configured_prompt,
    from_root,
    load_config,
    log,
    save_json,
    save_text,
    upload,
)


def main() -> None:
    """Run the Markdown parsing experiment."""
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
            "extract_printed_page_number": True,
            "markdown": {
                "tables": {
                    "output_tables_as_markdown": True,
                    "merge_continued_tables": True,
                }
            },
        },
        expand=["markdown", "items"],
        polling_interval=config["cloud"]["poll_seconds"],
        max_interval=config["cloud"]["max_poll_seconds"],
        timeout=config["cloud"]["timeout_seconds"],
    )
    pages = result.markdown.pages if result.markdown else []
    markdown_sections = []
    for page in pages:
        heading = f"Source PDF page {page.page_number}"
        content = page.markdown if page.success else f"Parse failed: {page.error}"
        markdown_sections.append(f"# {heading}\n\n{content}")
    markdown = "\n\n---\n\n".join(markdown_sections)
    output_root = config["output"]["root"]
    save_text(f"{output_root}/parse_markdown/result.md", markdown)
    save_json(f"{output_root}/parse_markdown/raw_result.json", result)
    log(
        "parse_completed",
        job_id=result.job.id,
        elapsed_seconds=round(perf_counter() - started, 3),
        state="uploaded->completed",
    )


if __name__ == "__main__":
    main()
