#!/usr/bin/env python3
"""Inventory presentation-course source files deterministically."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

KINDS = {
    ".pptx": "powerpoint", ".ppt": "powerpoint",
    ".pdf": "pdf",
    ".docx": "word", ".doc": "word",
    ".png": "image", ".jpg": "image", ".jpeg": "image",
    ".webp": "image", ".gif": "image", ".svg": "image",
    ".txt": "notes", ".md": "notes", ".url": "link",
}
SKIP_PARTS = {".git", "node_modules", ".codex_tmp", "__pycache__"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    records = []
    for item in root.rglob("*"):
        if not item.is_file() or item.name.startswith("~$"):
            continue
        rel = item.relative_to(root)
        if any(part.lower() in SKIP_PARTS for part in rel.parts):
            continue
        ext = item.suffix.lower()
        if ext not in KINDS:
            continue
        stat = item.stat()
        records.append({
            "relative_path": rel.as_posix(),
            "category": KINDS[ext],
            "extension": ext,
            "size_bytes": stat.st_size,
            "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        })
    records.sort(key=lambda row: (row["category"], row["relative_path"].lower()))
    counts = {}
    for row in records:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    payload = {"root": str(root), "file_count": len(records), "counts": counts, "files": records}
    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(json.dumps({"output": str(output), "file_count": len(records), "counts": counts}))
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())