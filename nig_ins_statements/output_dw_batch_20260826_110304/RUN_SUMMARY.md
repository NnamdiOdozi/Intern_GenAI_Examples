# Run summary — sterling_fcr_2023

**Source:** `nig_ins_statements/2023 sterling FCR FINAL.pdf` (52 pages, scanned, no text layer)
**Run ID:** 20260826_110304
**Pipeline:** dw_async_scanned_tables (3 Doubleword Batch rounds → audited workbook)
**Models:** R1 Qwen3-VL-30B · R2/R3 Qwen3-VL-235B · SLA 1h · temp 0 · max_tokens 16000

## Deliverables (`output/`)
- `sterling_fcr_2023_tables_20260826_110304.xlsx` — 57 worksheets:
  Index · Page Coverage · Table Inventory · 52 table sheets · Review Log · Run Metadata
- `csv/*.csv` — 52 per-table CSVs (raw printed rows preserved)

## Round-by-round
| Round | Model | Result |
|---|---|---|
| R1 discovery | 30B, 1 req/page | 48/52 first pass; 4 pages (10,14,37,38) retried on 235B after empty/whitespace-loop/truncation → 52/52, 52 logical tables |
| R2 extraction | 235B, 1 req/table | 42/52 first pass; retry#1 (firmer prompt) → 49; retry#2 (fixed multi-page spans) → 51; T04 hand-aligned → 52/52 |
| R3 validation+audit | 235B | 52/52 validated + document audit. Verdicts: 41 corrected, 9 accepted, 2 rejected_incomplete (T07, T14) |

## Key findings for human review (see Review Log + DOUBTS.md)
- **Round 1 over-segmented multi-page tables** where title+header sit at a page bottom and the body is
  on the next page (Table 3 revenue acct = p11+12; Table 7 claims paid = p16+17). Fixed T04/T13 by
  re-extracting across both pages; this creates deliberate overlap with T05/T14/T15 which is **kept, not
  merged**, and flagged by the audit. A human should pick the canonical version.
- **T07 (p13) and T14 (p17)** flagged `rejected_incomplete` by the validator (table not fully visible /
  structural ambiguity) — verify against the PDF.
- **T04** two cells inserted by hand (a blank 2021 value + an unlabelled ratio row) after 2 retries.
- Audit raised 7 material issues: coverage gap, repeated-version difference, arithmetic anomaly,
  cross-table inconsistency, source inconsistency, layout ambiguity, extraction uncertainty.

## Provenance (all preserved)
`round{1,2,3}/*_raw.jsonl` (raw API output, unrepaired) · `*_errors.jsonl` · per-round `logs/` JSONL +
batch IDs · `round1/image_manifest.json` (sha256/page) · `page_manifest/table_inventory/extraction_plan`
· `scripts/` (every build/validate script) · `images_r1` 150dpi discovery · `images_r2` 200dpi extraction.

**Note:** `images/` holds unused 210-dpi PNGs (~142 MB) from the first render; safe to delete to reclaim space.
