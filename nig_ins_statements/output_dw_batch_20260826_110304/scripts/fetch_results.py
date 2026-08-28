#!/usr/bin/env python3
"""Poll a Doubleword batch to completion, then download RAW output + error files.

Deliberately does NOT parse or repair. Saves raw JSONL exactly as returned so the
strict validator (validate_round.py) can reject truncated/invalid results. Reuses the
canonical dw_batch config + token loading pattern.
"""
import argparse
import sys
import time
from pathlib import Path
import tomllib
from openai import OpenAI
from dotenv import load_dotenv
import os

DW = Path("/home/nodozi/projects/Intern_GenAI_Examples/.claude/skills/dw_batch")
config = tomllib.loads((DW / "config.toml").read_text())
load_dotenv(dotenv_path=DW / ".env.dw")
client = OpenAI(api_key=os.getenv("DOUBLEWORD_AUTH_TOKEN"), base_url=config["api"]["base_url"])

ap = argparse.ArgumentParser()
ap.add_argument("--batch-id", required=True)
ap.add_argument("--out-prefix", required=True, help="path prefix; writes <prefix>_raw.jsonl / <prefix>_errors.jsonl")
ap.add_argument("--interval", type=int, default=30)
args = ap.parse_args()

while True:
    b = client.batches.retrieve(args.batch_id)
    rc = b.request_counts
    print(f"[{time.strftime('%H:%M:%S')}] {b.status} | {rc.completed}/{rc.total} (failed={rc.failed})", flush=True)
    if b.status in ("completed", "failed", "expired", "cancelled"):
        break
    time.sleep(args.interval)

if b.output_file_id:
    raw = client.files.content(b.output_file_id).text
    Path(f"{args.out_prefix}_raw.jsonl").write_text(raw)
    print(f"Saved raw -> {args.out_prefix}_raw.jsonl ({len(raw)} bytes)")
if b.error_file_id:
    err = client.files.content(b.error_file_id).text
    Path(f"{args.out_prefix}_errors.jsonl").write_text(err)
    print(f"Saved errors -> {args.out_prefix}_errors.jsonl ({len(err)} bytes)")
else:
    print("No error file.")

print(f"FINAL_STATUS={b.status}")
sys.exit(0 if b.status == "completed" else 1)
