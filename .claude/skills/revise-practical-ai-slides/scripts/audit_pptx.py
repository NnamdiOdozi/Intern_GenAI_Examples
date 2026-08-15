#!/usr/bin/env python3
"""Audit PPTX structure, notes, hyperlinks, and required/forbidden text."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

SLIDE_RE = re.compile(r"^ppt/slides/slide\d+\.xml$")
NOTES_RE = re.compile(r"^ppt/notesSlides/notesSlide\d+\.xml$")
RELS_RE = re.compile(r"^ppt/slides/_rels/slide\d+\.xml\.rels$")


def xml_text(data: bytes) -> str:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return data.decode("utf-8", errors="ignore")
    return " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--require-source-blocks", action="store_true")
    parser.add_argument("--forbid", action="append", default=[])
    parser.add_argument("--require-text", action="append", default=[])
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    pptx = args.pptx.expanduser().resolve()
    if not pptx.is_file():
        raise SystemExit(f"Not a file: {pptx}")

    with zipfile.ZipFile(pptx) as archive:
        names = archive.namelist()
        slides = [name for name in names if SLIDE_RE.match(name)]
        notes = [name for name in names if NOTES_RE.match(name)]
        note_texts = [xml_text(archive.read(name)) for name in notes]
        notes_with_sources = sum("[Sources]" in text and "[/Sources]" in text for text in note_texts)
        external_links = 0
        searchable = []
        for name in names:
            if name.endswith((".xml", ".rels")):
                data = archive.read(name)
                searchable.append(xml_text(data))
                if RELS_RE.match(name):
                    external_links += data.count(b'TargetMode="External"')
    all_text = "\n".join(searchable)
    lowered = all_text.casefold()
    failures = []
    if args.require_source_blocks and notes_with_sources != len(notes):
        failures.append(f"Only {notes_with_sources} of {len(notes)} notes slides contain complete source blocks")
    forbidden_found = [term for term in args.forbid if term.casefold() in lowered]
    required_missing = [term for term in args.require_text if term.casefold() not in lowered]
    if forbidden_found:
        failures.append("Forbidden text present: " + ", ".join(forbidden_found))
    if required_missing:
        failures.append("Required text missing: " + ", ".join(required_missing))
    payload = {
        "pptx": str(pptx), "slides": len(slides), "notes": len(notes),
        "notes_with_source_blocks": notes_with_sources,
        "external_hyperlinks": external_links,
        "forbidden_found": forbidden_found, "required_missing": required_missing,
        "passed": not failures, "failures": failures,
    }
    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    print(rendered)
    if args.json_output:
        output = args.json_output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())