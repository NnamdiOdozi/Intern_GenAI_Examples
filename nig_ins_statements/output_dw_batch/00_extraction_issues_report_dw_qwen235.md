# Table Extraction Issues Report — 2023 sterling FCR FINAL.pdf

**Model:** Qwen/Qwen3-VL-235B-A22B-Instruct-FP8 (via Doubleword batch API, scanned-PDF OCR path)
**Source:** 52-page scanned PDF (no extractable text layer), processed in 2 chunks (pages 1-30, pages 31-52)
**Output:** 41 CSV files in this folder, one per detected table, each suffixed `_dw_qwen235`

This is a verbatim OCR extraction — no values were corrected or interpreted by the agent. Below are issues an actuary/reviewer should check against the source PDF before using this data.

## 1. CSV structure breaks (commas inside unquoted fields)

Several rows contain a comma inside a text field that was NOT quoted, so the row has one extra column when parsed as CSV — will misalign in Excel/pandas.

- `23_p35_engineering_surplus_treaty_reinsurers`: row `ARB/WAICA RE, SERRA LEONE,10%,` — "ARB/WAICA RE" and "SERRA LEONE" split across two cells.
- `29_p38_bond_treaty_reinsurers` and `32_p40_marine_cargo_treaty_reinsurers`: same "ARB/WAICA Re, SIERRA LEONE" issue.
- `37_p43_multi_line_package_facility_for_oil_and_gas`: badly broken — every data cell contains embedded commas (e.g. "each and every loss or 7%, whichever is the lesser"), so the row is unusable as parsed CSV. **This table needs manual re-extraction from the source PDF page 43.**

## 2. Inconsistent number formatting within/across tables

- `01_p2` and `17_p20` use comma as thousands separator (e.g. `4,646,308`).
- `02_p7_trend_of_key_non_life...`, `03_p8_average_premium`, and several others use **period** as thousands separator (e.g. `877,1.263,1.251`), consistent with a different source page's number style — but this means downstream code parsing "all these CSVs the same way" will get wrong magnitudes unless it checks per-file.
- Some individual cells look like decimal artifacts rather than clean integers, e.g. in `01_p2`: `Aviation,-,59.28,56.22` and `Loss Component,0,41.40,4,650` — plausible the source has `59,280` / `4,650` etc. and the model inserted a decimal point where a thousands-comma should be. **Recommend spot-checking these specific cells against PDF page 2.**

## 3. Row/column count mismatches

- `15_p19_accident_year_2023_as_reported`: header has 5 columns but the "Aviation" row (`Aviation,0,59,56,Deterioration`) only has 4 values — a field is missing/shifted.
- `12_p15_general_insurance_claims_paid`: "Aviation" row has 6 values (`-,0,0,0,0,0`) vs. 5-column header — extra/duplicate cell.
- `19_p30_analysis_of_epi_gwp_and_treaty_capacity`: header row has 4 columns but several data rows have 3 or 5 — table likely has merged/spanning header cells in the source that didn't OCR cleanly.

## 4. Possible OCR misreads in titles/labels

- `16_p19_trend_in_solvency_cover_in_each_year_199_to_2023_statements`: title says "199 to 2023" — almost certainly "1999 to 2023" with a digit dropped.
- `08_p14`: header starts with `Table 5,Number of claims,...` — "Table 5" looks like a caption/label that got merged into the header row rather than being a real column header.

## 5. Page-number attribution at chunk boundary

Two tables (`18_p30` and `19_p30`) are attributed to page 30, but they came from the **second** batch chunk, which was assigned pages 31-52. Either:
(a) these tables are genuinely on page 30 and the model correctly read the printed page number despite the chunk split, or
(b) the model mislabeled them as page 30 when they're actually page 31.
**Recommend verifying against the source PDF** — chunk boundaries (page 30/31 split) are the highest-risk zone for page-number errors since a table spanning the boundary could be read by either request.

## 6. Coverage gaps (no tables extracted)

No tables were found on: pages 1, 3-6, 9-10, 18, 21-29, 32, 34, 46, 48-52. Not necessarily an error — these may be narrative/cover pages — but worth a quick manual check if you expect financial statement tables (e.g. balance sheet, income statement appendices) in the 48-52 range, which is common at the back of an FCR.

## Recommendation

Treat this as a first-pass extraction. Before using in analysis: (1) fix the unquoted-comma rows manually, (2) spot-check the flagged decimal-looking cells against source page 2, (3) manually re-key table `37_p43` and the page 19/30 mismatched rows, (4) confirm page 30 vs 31 attribution.
