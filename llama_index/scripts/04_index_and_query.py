#!/usr/bin/env python3
"""Create or reuse a LlamaCloud index, then run the configured query."""

from time import monotonic, perf_counter, sleep

from common import (
    client,
    ensure_sample,
    load_config,
    log,
    page_numbers,
    save_json,
    upload,
)


def index_status(index: object) -> str:
    """Read the current status from an Index v2 response."""
    metadata = getattr(index, "metadata", None) or {}
    return str(metadata.get("status", "unknown"))


def main() -> None:
    """Run the managed indexing and retrieval experiment."""
    config = load_config()
    sample = ensure_sample(config)
    api = client()
    started = perf_counter()
    index = next(
        (
            candidate
            for candidate in api.beta.indexes.list()
            if candidate.name == config["index"]["name"]
        ),
        None,
    )

    if index:
        log("index_reused", index_id=index.id, state="existing->existing")
    else:
        directory = api.beta.directories.create(
            name=config["index"]["name"],
            description=config["index"]["description"],
        )
        uploaded = upload(api, sample, "user_data")
        api.beta.directories.files.add(directory.id, file_id=uploaded.id)
        index = api.beta.indexes.create(
            source_directory_id=directory.id,
            name=config["index"]["name"],
            description=config["index"]["description"],
        )
        log(
            "index_created",
            index_id=index.id,
            directory_id=directory.id,
            file_id=uploaded.id,
            state="missing->building",
        )

    deadline = monotonic() + config["index"]["timeout_seconds"]
    while monotonic() < deadline:
        index = api.beta.indexes.get(index.id)
        status = index_status(index)
        log(
            "index_status",
            index_id=index.id,
            status=status,
            state=f"building->{status}",
        )
        if status == "ready":
            break
        if status == "failed":
            raise RuntimeError(f"Index {index.id} failed to build.")
        sleep(config["index"]["poll_seconds"])
    if index_status(index) != "ready":
        raise TimeoutError(f"Index {index.id} did not become ready before timeout.")

    result = api.beta.retrieval.retrieve(
        index_id=index.id,
        query=config["index"]["query"],
        top_k=config["index"]["top_k"],
        rerank={"enabled": True, "top_n": config["index"]["rerank_top_n"]},
    )
    source_pages = page_numbers(config["document"]["target_pages"])
    results = []
    for item in result.results:
        item_data = item.model_dump(mode="json")
        static_fields = item.static_fields
        start = static_fields.page_range_start if static_fields else None
        end = static_fields.page_range_end if static_fields else None
        item_data["source_pdf_page_start"] = source_pages[start - 1] if start else None
        item_data["source_pdf_page_end"] = source_pages[end - 1] if end else None
        results.append(item_data)

    output_root = config["output"]["root"]
    save_json(
        f"{output_root}/index/query_result.json",
        {
            "index": index.model_dump(mode="json"),
            "query": config["index"]["query"],
            "sample_to_source_pages": source_pages,
            "results": results,
        },
    )
    log(
        "retrieval_completed",
        index_id=index.id,
        result_count=len(result.results),
        elapsed_seconds=round(perf_counter() - started, 3),
        state="ready->queried",
    )


if __name__ == "__main__":
    main()
