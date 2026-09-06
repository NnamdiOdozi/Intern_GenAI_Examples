#!/usr/bin/env python3
"""Strict validation for Round 2 (targeted extraction). No JSON repair.

Accepts -> round2/tables/<table_id>.json
Rejects (truncated / invalid / ragged rows / missing id) -> round2/rejections.json
Gate: every extraction_plan table has a disposition.
"""
import json
from collections import Counter
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
R2 = RUN_DIR / "round2"
plan = json.loads((RUN_DIR / "round1" / "extraction_plan.json").read_text())
plan_by_id = {t["table_id"]: t for t in plan}
plan_ids = {t["table_id"] for t in plan}
expected_pages = json.loads((RUN_DIR / "round1" / "page_manifest.json").read_text())["expected_pages"]

REQUIRED = {"table_id", "title_raw", "headers_raw", "rows_raw", "normalized_rows",
            "cell_flags", "footnotes_raw", "concerns", "continues_from_previous",
            "continues_to_next", "pages_seen", "table_complete", "source_pages"}

# original + any exception batches; later files (retries) override earlier ones.
# order by mtime so retry#2 wins over retry#1 (alphabetical sort mis-orders exc2 vs exc).
raw_files = sorted(R2.glob("round2*_raw.jsonl"), key=lambda p: p.stat().st_mtime)
raw_lines = []
for rf in raw_files:
    raw_lines += [l for l in rf.read_text().splitlines() if l.strip()]

accepted = {}          # table_id -> data (last valid wins)
fail_by_tid = {}       # table_id -> reason (only matters if never accepted)

def cid_tid(cid):
    return cid.split("-r2-")[-1]

for line in raw_lines:
    rec = json.loads(line)
    cid = rec.get("custom_id", "?")
    tid = cid_tid(cid)
    resp = rec.get("response") or {}
    body = resp.get("body") or {}
    if rec.get("error") or resp.get("status_code", 200) != 200:
        fail_by_tid[tid] = f"api_error:{rec.get('error') or resp.get('status_code')}"
        continue
    choice = (body.get("choices") or [{}])[0]
    if choice.get("finish_reason") == "length":
        fail_by_tid[tid] = "truncated_finish_length"
        continue
    content = (choice.get("message") or {}).get("content", "")
    try:
        data = json.loads(content)
    except Exception as e:
        fail_by_tid[tid] = f"invalid_json:{e}"
        continue
    if not REQUIRED.issubset(data):
        fail_by_tid[tid] = f"missing_fields:{sorted(REQUIRED - set(data))}"
        continue
    rows = data["rows_raw"]
    if not rows:
        fail_by_tid[tid] = "header_only_missing_body" if data["headers_raw"] else "empty_table"
        continue
    planned_pages = set(plan_by_id[tid]["source_pages"])
    if not planned_pages.issubset(data["pages_seen"]):
        fail_by_tid[tid] = f"missing_planned_pages:{sorted(planned_pages - set(data['pages_seen']))}"
        continue
    widths = Counter(len(r) for r in rows)
    if len(widths) > 1:
        fail_by_tid[tid] = f"ragged_rows:{dict(widths)}"
        continue
    if not data.get("table_complete", False):
        fail_by_tid[tid] = "table_complete_false"
        continue
    data["_header_width"] = len(data["headers_raw"])
    data["_row_width"] = widths.most_common(1)[0][0] if rows else 0
    accepted[data["table_id"]] = data
    (R2 / "tables" / f"{data['table_id']}.json").write_text(json.dumps(data, indent=2))

rejections = []
for tid, reason in fail_by_tid.items():
    if tid in accepted:
        continue
    retry_pages = list(plan_by_id[tid]["source_pages"])
    if (
        reason == "header_only_missing_body"
        and len(retry_pages) == 1
        and retry_pages[0] < expected_pages
    ):
        retry_pages.append(retry_pages[0] + 1)
    rejections.append({"table_id": tid, "reason": reason, "retry_pages": retry_pages})
no_disposition = sorted(plan_ids - set(accepted) - {r["table_id"] for r in rejections})

(R2 / "rejections.json").write_text(json.dumps(rejections, indent=2))
print(f"Round2: accepted={len(accepted)}/{len(plan_ids)} rejected={len(rejections)}")
if rejections:
    for r in rejections:
        print(f"  REJECT {r['table_id']} :: {r['reason']}")
print(f"Plan tables with no disposition (missing from results): {no_disposition}")
gate = (len(no_disposition) == 0 and len(rejections) == 0)
print(f"GATE {'PASS' if gate else 'ATTN - resolve rejects/missing via exception batch before Round 3'}")
