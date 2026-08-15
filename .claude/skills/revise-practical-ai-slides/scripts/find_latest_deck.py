#!/usr/bin/env python3
"""Find the latest matching PPTX and fail when the leading candidates are ambiguous."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def record(path: Path) -> dict:
    stat = path.stat()
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "size_bytes": stat.st_size,
        "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "modified_epoch": stat.st_mtime,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--contains", action="append", default=[])
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--ambiguity-seconds", type=float, default=2.0)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")
    required = [value.casefold() for value in args.contains]
    excluded = [value.casefold() for value in args.exclude]
    candidates = []
    for path in root.rglob("*.pptx"):
        if not path.is_file() or path.name.startswith("~$"):
            continue
        name = path.name.casefold()
        if required and not all(token in name for token in required):
            continue
        if any(token in name for token in excluded):
            continue
        candidates.append(record(path))
    candidates.sort(key=lambda row: (row["modified_epoch"], row["size_bytes"]), reverse=True)
    if not candidates:
        print(json.dumps({"selected": None, "candidates": [], "error": "No matching PPTX files"}, indent=2))
        return 1
    ambiguous = len(candidates) > 1 and abs(candidates[0]["modified_epoch"] - candidates[1]["modified_epoch"]) <= args.ambiguity_seconds
    payload = {
        "selected": None if ambiguous else candidates[0],
        "ambiguous": ambiguous,
        "candidates": candidates[:10],
    }
    if ambiguous:
        payload["error"] = "Top candidates have effectively identical modification times; ask the user which file to use"
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 2 if ambiguous else 0


if __name__ == "__main__":
    raise SystemExit(main())