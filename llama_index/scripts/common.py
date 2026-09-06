"""Shared configuration, file, logging, and LlamaCloud helpers."""

from __future__ import annotations

import json
import tomllib
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from dotenv import find_dotenv, load_dotenv
from llama_cloud import LlamaCloud
from PyPDF2 import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = str(uuid.uuid4())


def log(event: str, **metadata: object) -> None:
    """Write one structured run event as JSON."""
    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "run_id": RUN_ID,
        "event": event,
        **metadata,
    }
    print(json.dumps(record, default=str), flush=True)


def load_config() -> dict[str, Any]:
    """Load the proof-of-concept configuration."""
    with (ROOT / "config.toml").open("rb") as config_file:
        return tomllib.load(config_file)


def from_root(path: str) -> Path:
    """Resolve a configured path from the LlamaIndex folder."""
    return (ROOT / path).resolve()


def configured_prompt(config: dict[str, Any], section: str) -> str:
    """Return the named document-table prompt for a service.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed project configuration.
    section : str
        Service section containing the prompt name.

    Returns
    -------
    str
        Shared prompt text selected by the service.
    """
    prompt_name = config[section]["prompt"]
    return config["prompts"][prompt_name]


def normalize_page_number(value: object, valid_pages: list[int]) -> int:
    """Normalize an integral API page value and validate its provenance.

    Parameters
    ----------
    value : object
        Page value returned by the extraction service.
    valid_pages : list[int]
        PDF viewer pages included in the request.

    Returns
    -------
    int
        Validated PDF viewer page number.

    Raises
    ------
    ValueError
        If the value is non-integral or outside the requested pages.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid source PDF page: {value!r}")
    page = int(value)
    if page != value or page not in valid_pages:
        raise ValueError(f"Invalid source PDF page: {value!r}")
    return page


def page_numbers(specification: str) -> list[int]:
    """Expand a page specification such as ``3,8,12-14``."""
    pages: list[int] = []
    for part in specification.split(","):
        bounds = [int(value) for value in part.split("-")]
        start = bounds[0]
        end = bounds[-1]
        pages.extend(range(start, end + 1))
    return pages


def source_page_for_sample(sample_page: int, source_pages: list[int]) -> int:
    """Map a one-based sample page to its original PDF viewer page."""
    if sample_page < 1 or sample_page > len(source_pages):
        raise ValueError(f"Sample page {sample_page} is outside the page manifest.")
    return source_pages[sample_page - 1]


def ensure_sample(config: dict[str, Any]) -> Path:
    """Create the configured sample PDF and its source-page manifest once."""
    target = from_root(config["document"]["sample_pdf"])
    source = from_root(config["document"]["source_pdf"])
    pages = page_numbers(config["document"]["target_pages"])
    manifest_path = target.parent / "page_manifest.json"
    manifest = [
        {"sample_page": offset, "source_pdf_page": source_page}
        for offset, source_page in enumerate(pages, start=1)
    ]
    expected_manifest = json.dumps(manifest, indent=2) + "\n"

    if target.exists():
        if not manifest_path.exists() or manifest_path.read_text() != expected_manifest:
            message = (
                "The existing sample PDF does not match config.toml. "
                "Choose a new sample_pdf path."
            )
            raise ValueError(message)
        log(
            "sample_reused",
            document_id=config["document"]["id"],
            path=str(target),
            state="existing->existing",
        )
        return target

    reader = PdfReader(source)
    writer = PdfWriter()
    for page in pages:
        writer.add_page(reader.pages[page - 1])

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as sample_file:
        writer.write(sample_file)
    manifest_path.write_text(expected_manifest, encoding="utf-8")
    log(
        "sample_created",
        document_id=config["document"]["id"],
        pages=pages,
        path=str(target),
        state="missing->created",
    )
    return target


def client() -> LlamaCloud:
    """Create a client after loading user-managed local credentials."""
    # Keep existing shell values authoritative while allowing VS Code runs to use the
    # nearest project .env file. Secret names and values are never inspected or logged.
    load_dotenv(find_dotenv(usecwd=True), override=False)
    return LlamaCloud()


def upload(
    api: LlamaCloud,
    file_path: Path,
    purpose: Literal["parse", "extract", "user_data"],
) -> object:
    """Upload a local file for one LlamaCloud product."""
    uploaded = api.files.create(file=file_path, purpose=purpose)
    log(
        "file_uploaded",
        file_id=uploaded.id,
        purpose=purpose,
        path=str(file_path),
        state="local->cloud",
    )
    return uploaded


def json_ready(value: object) -> object:
    """Convert an SDK response model into JSON-compatible data."""
    model_dump = getattr(value, "model_dump", None)
    return model_dump(mode="json") if model_dump else value


def save_json(path: str, value: object) -> None:
    """Save indented JSON beneath the LlamaIndex folder."""
    target = from_root(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_ready(value), indent=2) + "\n", encoding="utf-8")
    log("output_saved", path=str(target), state="missing_or_existing->written")


def save_text(path: str, value: str) -> None:
    """Save text beneath the LlamaIndex folder."""
    target = from_root(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")
    log("output_saved", path=str(target), state="missing_or_existing->written")


def save_bytes(path: str, value: bytes) -> None:
    """Save binary content beneath the LlamaIndex folder."""
    target = from_root(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(value)
    log("output_saved", path=str(target), state="missing_or_existing->written")
