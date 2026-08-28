#!/usr/bin/env python3
"""Build Round 3 (validation + document audit) batch JSONL.

Per accepted Round 2 table: one independent validation request (235B) with the provisional
JSON + page images. Plus ONE document-audit request over the inventory + all provisional tables.
"""
import base64
import json
from datetime import datetime
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = Path("/home/nodozi/projects/Intern_GenAI_Examples/.claude/skills/dw_async_scanned_tables")
MODEL = "deepseek-ai/DeepSeek-OCR-2"
DOC_ID = "sterling_fcr_2023"

val_schema = json.loads((SKILL_DIR / "schemas" / "round3-table-validation.schema.json").read_text())
audit_schema = json.loads((SKILL_DIR / "schemas" / "round3-document-audit.schema.json").read_text())
inventory = json.loads((RUN_DIR / "round1" / "table_inventory.json").read_text())
manifest = json.loads((RUN_DIR / "round1" / "page_manifest.json").read_text())
tables = [json.loads(p.read_text()) for p in sorted((RUN_DIR / "round2" / "tables").glob("*.json"))]

VAL_SYS = (
    "You are an INDEPENDENT validator. You are given a provisional table extraction (JSON) plus "
    "the original scanned page image(s). Verify every header and cell against the image. Produce a "
    "final table: keep values that are correct, correct clear OCR errors (record each in "
    "corrections with the source pdf_page), and flag anything you cannot resolve. Never invent data "
    "or insert calculated values into printed blanks. Check header/row width consistency, verify the "
    "page citations, verify continuation stitching, and check whether printed totals/ratios reconcile "
    "with the printed components (report totals_status; do NOT overwrite printed values even if they "
    "do not reconcile - flag as arithmetic_anomaly instead). Choose verdict: accepted (no changes), "
    "corrected (you changed cells), needs_human_review (material unresolved issue), or "
    "rejected_incomplete (extraction is not usable). Return ONLY JSON per the provided schema; set "
    "table_id EXACTLY to the provided value."
)


def encode(pdf_page: int):
    p = RUN_DIR / "images_r2" / f"page-{pdf_page:02d}.jpg"
    return base64.b64encode(p.read_bytes()).decode()


lines = []
for t in tables:
    tid = t["table_id"]
    pages = sorted({sp["pdf_page"] for sp in t.get("source_pages", [])} | set(t.get("pages_seen", [])))
    provisional = {k: v for k, v in t.items() if not k.startswith("_")}
    uc = [{"type": "text", "text":
           f"table_id: {tid}\nPROVISIONAL EXTRACTION JSON:\n{json.dumps(provisional, ensure_ascii=False)}\n\n"
           "Original page image(s) follow in ascending pdf_page order. Validate against them."}]
    for pg in pages:
        uc.append({"type": "text", "text": f"[pdf_page {pg}]"})
        uc.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode(pg)}"}})
    lines.append(json.dumps({
        "custom_id": f"sterlingfcr-r3v-{tid}",
        "method": "POST", "url": "/v1/chat/completions",
        "body": {"model": MODEL, "max_tokens": 16000, "temperature": 0,
                 "response_format": val_schema,
                 "messages": [{"role": "system", "content": VAL_SYS},
                              {"role": "user", "content": uc}]},
    }))

# ---- document audit (single request, JSON only) ----
AUDIT_SYS = (
    "You are a document auditor for a scanned insurance Financial Condition Report. You are given the "
    "page-coverage summary, the logical table inventory, and every provisional table (headers + "
    "normalized rows). WITHOUT inventing corrections, identify: coverage gaps (inventoried tables with "
    "no extraction, or pages that should hold tables but do not), repeated-version differences (same "
    "table appearing with different numbers), arithmetic anomalies (component vs printed total/ratio "
    "mismatches), cross-table inconsistencies (a figure disagreeing across tables), source "
    "inconsistencies, layout ambiguity, and extraction uncertainty. Report inventory_table_count and "
    "provisional_table_count and any missing_pdf_pages. Return ONLY JSON per the schema."
)
pages_summary = [{"pdf_page": p["pdf_page"], "printed_page": p.get("printed_page"),
                  "page_status": p["page_status"],
                  "table_titles": [tt.get("title_raw") for tt in p.get("tables", [])]}
                 for p in manifest["pages"]]
audit_payload = {
    "document_id": DOC_ID,
    "page_coverage": pages_summary,
    "inventory": [{"table_id": t["table_id"], "title_raw": t["title_raw"],
                   "source_pages": t["source_pages"], "possible_repeat_of": t.get("possible_repeat_of")}
                  for t in inventory],
    "provisional_tables": [{"table_id": t["table_id"], "title_raw": t.get("title_raw"),
                            "units_raw": t.get("units_raw"), "headers_raw": t.get("headers_raw"),
                            "normalized_rows": t.get("normalized_rows")} for t in tables],
}
lines.append(json.dumps({
    "custom_id": "sterlingfcr-r3-audit",
    "method": "POST", "url": "/v1/chat/completions",
    "body": {"model": MODEL, "max_tokens": 16000, "temperature": 0,
             "response_format": audit_schema,
             "messages": [{"role": "system", "content": AUDIT_SYS},
                          {"role": "user", "content": json.dumps(audit_payload, ensure_ascii=False)}]},
}))

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = RUN_DIR / "round3" / "logs" / f"batch_requests_round3_{ts}.jsonl"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} Round 3 requests ({len(tables)} validations + 1 audit) -> {out}")
print(f"JSONL size: {out.stat().st_size/1e6:.1f} MB")
