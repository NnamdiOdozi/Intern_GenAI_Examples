#!/usr/bin/env python3
"""Build Round 1 (page discovery) batch JSONL for the dw_async_scanned_tables pipeline.

One request per PDF page. Model = Qwen3-VL-30B. Strict json_schema response_format.
Saves an image-hash manifest for provenance.
"""
import base64
import hashlib
import json
from datetime import datetime
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = Path("/home/nodozi/projects/Intern_GenAI_Examples/.claude/skills/dw_async_scanned_tables")
IMAGES = sorted((RUN_DIR / "images_r1").glob("page-*.jpg"))
DOC_ID = "sterling_fcr_2023"
MODEL = "deepseek-ai/DeepSeek-OCR-2"

schema = json.loads((SKILL_DIR / "schemas" / "round1-discovery.schema.json").read_text())

SYSTEM = (
    "You are a meticulous financial-document analyst performing PAGE DISCOVERY on ONE scanned "
    "page of a Nigerian insurance Financial Condition Report (FCR). Do NOT transcribe table "
    "contents or cell values. Your job is only to INVENTORY what tables appear on THIS page: "
    "each table's printed title, table number, stated units, approximate visible row and column "
    "counts, whether it continues from the previous page or continues to the next, whether it "
    "may be a repeat/alternate version of a table appearing elsewhere, its legibility, and any "
    "concerns (OCR uncertainty, layout ambiguity, possible source issues, continuation "
    "uncertainty). A 'table' is any gridded/tabular numeric or structured layout, including "
    "revenue accounts, triangles, ratio tables, treaty schedules, and reinsurer panels. "
    "Prose paragraphs, charts, and images are NOT tables. Return ONLY JSON conforming to the "
    "provided schema. Set document_id and pdf_page EXACTLY to the provided values. Read the "
    "printed page number from the page header/footer if visible, else null. If there is no "
    "tabular data, set page_status='no_table' and tables=[]."
)

def encode(p: Path):
    raw = p.read_bytes()
    return base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest()

lines = []
img_manifest = []
for p in IMAGES:
    pdf_page = int(p.stem.split("-")[1])
    b64, sha = encode(p)
    img_manifest.append({"pdf_page": pdf_page, "image": p.name, "sha256": sha, "bytes": p.stat().st_size})
    user_text = (
        f"document_id: {DOC_ID}\n"
        f"pdf_page: {pdf_page}\n"
        f"image_sha256: {sha}\n"
        "Read the printed page number from the page itself if visible.\n"
        "Analyze the attached page image and return the discovery JSON."
    )
    body = {
        "model": MODEL,
        "max_tokens": 16000,
        "temperature": 0,
        "response_format": schema,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ]},
        ],
    }
    lines.append(json.dumps({
        "custom_id": f"sterlingfcr-r1-p{pdf_page:02d}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": body,
    }))

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = RUN_DIR / "round1" / "logs" / f"batch_requests_round1_{ts}.jsonl"
out.write_text("\n".join(lines) + "\n")
(RUN_DIR / "round1" / "image_manifest.json").write_text(json.dumps(img_manifest, indent=2))
print(f"Wrote {len(lines)} Round 1 requests -> {out}")
print(f"JSONL size: {out.stat().st_size/1e6:.1f} MB")
print(f"Image manifest: {len(img_manifest)} pages")
