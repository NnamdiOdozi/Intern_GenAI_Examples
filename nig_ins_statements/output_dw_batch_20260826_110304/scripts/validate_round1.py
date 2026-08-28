#!/usr/bin/env python3
"""Strict validation + planning for Round 1 (page discovery).

Rejects truncated (finish_reason=length) or schema-invalid results WITHOUT repair.
Requires every PDF page present exactly once. Builds:
  round1/page_manifest.json      - per-page discovery (accepted)
  round1/rejections.json         - rejected pages (for exception batch)
  round1/table_inventory.json    - stable logical table IDs (continuations merged, repeats linked)
  round1/extraction_plan.json    - drives Round 2 (one logical table -> source pages)
"""
import json
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
R1 = RUN_DIR / "round1"
EXPECTED_PAGES = 52

REQUIRED = {"document_id", "pdf_page", "printed_page", "page_seen", "page_legibility",
            "page_status", "tables", "page_complete"}


def app_summary(app):
    return {
        "appearance_id": app.get("appearance_id"),
        "visible_row_count": app.get("visible_row_count"),
        "visible_column_count": app.get("visible_column_count"),
        "concerns": app.get("concerns", []),
    }


# Read original + any exception batches; later files (retries) override earlier ones.
raw_files = sorted((R1).glob("round1_raw.jsonl")) + sorted((R1).glob("round1_exc*_raw.jsonl"))
raw_lines = []
for rf in raw_files:
    raw_lines += [l for l in rf.read_text().splitlines() if l.strip()]

accepted = {}     # pdf_page -> discovery dict (last valid wins)
errors_by_page = {}  # pdf_page(or cid) -> list of failure reasons

def note_error(cid, reason):
    errors_by_page.setdefault(cid, []).append(reason)

for line in raw_lines:
    rec = json.loads(line)
    cid = rec.get("custom_id", "?")
    resp = rec.get("response") or {}
    body = resp.get("body") or {}
    err = rec.get("error")
    if err or resp.get("status_code", 200) != 200:
        note_error(cid, f"api_error: {err or resp.get('status_code')}")
        continue
    choice = (body.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content", "")
    if choice.get("finish_reason") == "length":
        note_error(cid, "truncated_finish_length")
        continue
    try:
        data = json.loads(content)   # strict: no repair
    except Exception as e:
        note_error(cid, f"invalid_json: {e}")
        continue
    if not REQUIRED.issubset(data):
        note_error(cid, f"missing_fields: {sorted(REQUIRED - set(data))}")
        continue
    accepted[data["pdf_page"]] = data   # retry overrides earlier failure

missing = [p for p in range(1, EXPECTED_PAGES + 1) if p not in accepted]
# rejections = only pages that never produced a valid record
rejections = [{"custom_id": cid, "reasons": rs} for cid, rs in errors_by_page.items()
              if int(cid.split("-p")[-1]) not in accepted]

# ---- table inventory: merge continuations, link repeats ----
inventory = []
tid_counter = 0
open_by_page = {}       # pdf_page -> list of table_ids that continue_to_next


def new_tid():
    global tid_counter
    tid_counter += 1
    return f"T{tid_counter:02d}"


for pg in range(1, EXPECTED_PAGES + 1):
    disc = accepted.get(pg)
    if not disc:
        continue
    prev_open = open_by_page.get(pg - 1, [])
    cur_open = []
    for app in disc.get("tables", []):
        linked = prev_open[-1] if (app.get("continues_from_previous") and prev_open) else None
        if linked:
            t = next(t for t in inventory if t["table_id"] == linked)
            t["source_pages"].append(pg)
            t["printed_pages"].append(disc.get("printed_page"))
            t["appearances"].append({"pdf_page": pg, **app_summary(app)})
        else:
            tid = new_tid()
            t = {
                "table_id": tid,
                "title_raw": app.get("title_raw"),
                "table_number_raw": app.get("table_number_raw"),
                "units_raw": app.get("units_raw"),
                "source_pages": [pg],
                "printed_pages": [disc.get("printed_page")],
                "complexity": app.get("complexity"),
                "possible_repeat_of": app.get("possible_repeat_of"),
                "appearances": [{"pdf_page": pg, **app_summary(app)}],
            }
            inventory.append(t)
            linked = tid
        if app.get("continues_to_next"):
            cur_open.append(linked)
    open_by_page[pg] = cur_open

# ---- extraction plan (one entry per logical table) ----
plan = [{
    "table_id": t["table_id"],
    "title_raw": t["title_raw"],
    "units_raw": t["units_raw"],
    "source_pages": sorted(set(t["source_pages"])),
    "complexity": t["complexity"],
    "possible_repeat_of": t["possible_repeat_of"],
} for t in inventory]

# ---- write artifacts ----
(R1 / "page_manifest.json").write_text(json.dumps(
    {"expected_pages": EXPECTED_PAGES, "accepted": len(accepted), "missing": missing,
     "pages": [accepted[p] for p in sorted(accepted)]}, indent=2))
(R1 / "rejections.json").write_text(json.dumps(rejections, indent=2))
(R1 / "table_inventory.json").write_text(json.dumps(inventory, indent=2))
(R1 / "extraction_plan.json").write_text(json.dumps(plan, indent=2))

gate_ok = (len(missing) == 0 and len(rejections) == 0)
print(f"Round1: accepted={len(accepted)}/{EXPECTED_PAGES} rejections={len(rejections)} missing={missing}")
print(f"Logical tables inventoried: {len(inventory)}")
status = sum(1 for p in accepted.values() if p['page_status'] != 'no_table')
print(f"Pages with tables: {status} | no_table pages: {len(accepted)-status}")
print(f"GATE {'PASS' if gate_ok else 'FAIL - fix rejections/missing before Round 2'}")
