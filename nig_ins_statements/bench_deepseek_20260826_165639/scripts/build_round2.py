#!/usr/bin/env python3
"""Build Round 2 (targeted extraction) batch JSONL.

One request per logical table from round1/extraction_plan.json. Attaches the 200 DPI
q88 JPEG(s) for the table's source pages. Model = Qwen3-VL-235B. Strict json_schema.
"""
import base64
import json
from datetime import datetime
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = Path("/home/nodozi/projects/Intern_GenAI_Examples/.claude/skills/dw_async_scanned_tables")
MODEL = "deepseek-ai/DeepSeek-OCR-2"
DOC_ID = "sterling_fcr_2023"

schema = json.loads((SKILL_DIR / "schemas" / "round2-extraction.schema.json").read_text())
plan = json.loads((RUN_DIR / "round1" / "extraction_plan.json").read_text())

SYSTEM = (
    "You are a meticulous financial-document analyst performing EXACT TABLE EXTRACTION from a "
    "scanned Nigerian insurance Financial Condition Report. You are given the full page image(s) "
    "that contain ONE logical table (identified by table_id and title). Transcribe THAT table only.\n"
    "Rules:\n"
    "- headers_raw: the column headers exactly as printed (top to bottom, left to right).\n"
    "- rows_raw: every data row EXACTLY as printed, one array of cell strings per row, preserving "
    "order, signs, %, parentheses, commas, currency, dashes and blanks. Do NOT reformat numbers.\n"
    "- normalized_rows: a parallel machine-usable version (numbers as JSON numbers where the printed "
    "value is unambiguously numeric; keep labels as strings; null where blank/illegible).\n"
    "- cell_flags: record any cell that is blank, a dash, an explicit zero, illegible, ambiguous, or a "
    "value you can infer but must NOT insert. NEVER put a calculated/inferred number into a printed "
    "blank — use status 'inferred_not_inserted' and place the guess in inferred_value only.\n"
    "- Distinguish blank vs dash vs zero precisely.\n"
    "- footnotes_raw: any footnotes/notes attached to the table.\n"
    "- Keep header width and every row width consistent with the printed column count; if the table "
    "spans multiple pages, stitch the rows in printed order and set continues_* / pages_seen.\n"
    "- source_pages: the pdf_page(s) provided (and printed_page if visible).\n"
    "Return ONLY JSON conforming to the provided schema. Set table_id EXACTLY to the provided value. "
    "If you cannot finish the whole table, set table_complete=false rather than truncating silently."
)


def encode(pdf_page: int):
    p = RUN_DIR / "images_r2" / f"page-{pdf_page:02d}.jpg"
    return base64.b64encode(p.read_bytes()).decode()


lines = []
for t in plan:
    tid = t["table_id"]
    pages = t["source_pages"]
    user_content = [{
        "type": "text",
        "text": (
            f"document_id: {DOC_ID}\n"
            f"table_id: {tid}\n"
            f"expected_title: {t.get('title_raw')}\n"
            f"expected_units: {t.get('units_raw')}\n"
            f"source_pdf_pages: {pages}\n"
            "Extract this single logical table exactly per the rules. The images below are the "
            "full page(s) in ascending pdf_page order."
        )
    }]
    for pg in pages:
        user_content.append({"type": "text", "text": f"[pdf_page {pg}]"})
        user_content.append({"type": "image_url",
                             "image_url": {"url": f"data:image/jpeg;base64,{encode(pg)}"}})
    body = {
        "model": MODEL,
        "max_tokens": 16000,
        "temperature": 0,
        "response_format": schema,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_content},
        ],
    }
    lines.append(json.dumps({
        "custom_id": f"sterlingfcr-r2-{tid}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": body,
    }))

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = RUN_DIR / "round2" / "logs" / f"batch_requests_round2_{ts}.jsonl"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} Round 2 requests -> {out}")
print(f"JSONL size: {out.stat().st_size/1e6:.1f} MB")
