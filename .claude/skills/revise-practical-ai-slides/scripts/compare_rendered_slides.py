#!/usr/bin/env python3
"""Compare two rendered-slide directories and enforce an expected change set."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from PIL import Image, ImageChops

    COMPARISON_MODE = "pixel"
except ImportError:  # Pillow is optional; byte comparison needs only the standard library.
    Image = None
    ImageChops = None
    COMPARISON_MODE = "png-bytes"

NUMBER = re.compile(r"slide-(\d+)\.png$", re.I)


def slides(folder: Path) -> dict[int, Path]:
    result = {}
    for path in folder.glob("slide-*.png"):
        match = NUMBER.search(path.name)
        if match:
            result[int(match.group(1))] = path
    return result


def different(left: Path, right: Path) -> bool:
    if Image is None:
        return left.read_bytes() != right.read_bytes()
    with Image.open(left).convert("RGB") as a, Image.open(right).convert("RGB") as b:
        if a.size != b.size:
            return True
        return ImageChops.difference(a, b).getbbox() is not None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--expected-change", action="append", type=int, default=[])
    args = parser.parse_args()
    source = slides(args.source.expanduser().resolve())
    revised = slides(args.revised.expanduser().resolve())
    all_numbers = sorted(set(source) | set(revised))
    missing_source = [n for n in all_numbers if n not in source]
    missing_revised = [n for n in all_numbers if n not in revised]
    changed = [n for n in all_numbers if n in source and n in revised and different(source[n], revised[n])]
    expected = sorted(set(args.expected_change))
    failures = []
    if missing_source or missing_revised:
        failures.append("Rendered slide sets differ")
    if expected and changed != expected:
        failures.append(f"Changed slides {changed} do not match expected {expected}")
    payload = {
        "comparison_mode": COMPARISON_MODE,
        "source_count": len(source),
        "revised_count": len(revised),
        "changed": changed,
        "identical": [n for n in all_numbers if n not in changed and n in source and n in revised],
        "missing_source": missing_source,
        "missing_revised": missing_revised,
        "expected_change": expected,
        "passed": not failures,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
