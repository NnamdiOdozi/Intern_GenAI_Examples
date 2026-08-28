#!/usr/bin/env python3
"""Strict validation for Round 3 (table validation + document audit). No JSON repair.

Validations -> round3/validated_tables/<table_id>.json
Audit       -> round3/document_audit.json
Gate: every Round 2 accepted table has a Round 3 verdict.
"""
import json
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
R3 = RUN_DIR / "round3"
r2_ids = {p.stem for p in (RUN_DIR / "round2" / "tables").glob("*.json")}

VAL_REQ = {"table_id", "verdict", "source_pages", "final_title_raw", "final_headers_raw",
           "final_rows_raw", "final_normalized_rows", "corrections", "issues", "checks",
           "table_complete"}
AUDIT_REQ = {"document_id", "page_coverage_complete", "missing_pdf_pages",
             "inventory_table_count", "provisional_table_count", "issues", "audit_complete"}

raw_lines = [l for l in (R3 / "round3_raw.jsonl").read_text().splitlines() if l.strip()]
val_ok, rejections, audit = {}, [], None

for line in raw_lines:
    rec = json.loads(line)
    cid = rec.get("custom_id", "?")
    resp = rec.get("response") or {}
    body = resp.get("body") or {}
    if rec.get("error") or resp.get("status_code", 200) != 200:
        rejections.append({"custom_id": cid, "reason": f"api_error:{rec.get('error') or resp.get('status_code')}"})
        continue
    choice = (body.get("choices") or [{}])[0]
    if choice.get("finish_reason") == "length":
        rejections.append({"custom_id": cid, "reason": "truncated_finish_length"})
        continue
    try:
        data = json.loads((choice.get("message") or {}).get("content", ""))
    except Exception as e:
        rejections.append({"custom_id": cid, "reason": f"invalid_json:{e}"})
        continue
    if cid == "sterlingfcr-r3-audit":
        if not AUDIT_REQ.issubset(data):
            rejections.append({"custom_id": cid, "reason": f"missing_fields:{sorted(AUDIT_REQ - set(data))}"})
            continue
        audit = data
        (R3 / "document_audit.json").write_text(json.dumps(data, indent=2))
        continue
    if not VAL_REQ.issubset(data):
        rejections.append({"custom_id": cid, "reason": f"missing_fields:{sorted(VAL_REQ - set(data))}"})
        continue
    tid = data["table_id"]
    val_ok[tid] = data
    (R3 / "validated_tables" / f"{tid}.json").write_text(json.dumps(data, indent=2))

no_verdict = sorted(r2_ids - set(val_ok))
verdicts = {}
for d in val_ok.values():
    verdicts[d["verdict"]] = verdicts.get(d["verdict"], 0) + 1

(R3 / "rejections.json").write_text(json.dumps(rejections, indent=2))
print(f"Round3: validations_ok={len(val_ok)}/{len(r2_ids)} rejected={len(rejections)} audit={'yes' if audit else 'MISSING'}")
print(f"Verdicts: {verdicts}")
if rejections:
    for r in rejections:
        print(f"  REJECT {r['custom_id']} :: {r['reason']}")
print(f"Tables with no verdict: {no_verdict}")
gate = (len(no_verdict) == 0 and audit is not None and len(rejections) == 0)
print(f"GATE {'PASS' if gate else 'ATTN - resolve before building workbook'}")
