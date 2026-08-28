# Review Log — 2023 Sterling FCR Table Extraction

## Record metadata

- **Source report:** `nig_ins_statements/2023 sterling FCR FINAL.pdf`
- **Agentic workbook:** `nig_ins_statements/output/2023_sterling_FCR_tables_chatgpt_5.6_sol_high.xlsx`
- **Doubleword batch outputs:** `nig_ins_statements/output_dw_batch/`
- **Workbook creation timestamp supplied by the user:** **23 August 2026, 14:34 (Europe/London)**. This agrees with the workbook's recorded last-modified time of 14:34:36 on that date; it should not be confused with the file-system creation time of 14:32:07.
- **Review log creation date:** **24 August 2026** (no exact creation time recorded)
- **Page convention in this log:** “PDF page” means the page number shown by the PDF viewer, not necessarily the page number printed in the report.

## Purpose and status terminology

This log preserves material observations made while extracting and comparing tables from the scanned report. It is not a replacement for checking the source images or audited financial records.

- **Confirmed source issue:** the cited figures or labels are visibly present in the scanned report and conflict internally, fail an arithmetic check, or are incomplete.
- **Extraction uncertainty:** the source is unclear, unlabelled, split across pages, or susceptible to OCR/transcription error.
- **Inference:** a likely explanation or reconstructed value that is not explicitly printed in the source.
- **Process limitation:** a weakness in the extraction, consolidation, validation, or output workflow rather than necessarily an error in the report.

## Material source-report findings

| PDF page(s) | Classification | Finding | Recommended check |
|---|---|---|---|
| 21–22 | Confirmed source inconsistency | Table 12 prints 2020 post-tax profit as **–61,042,762** (NGN'000), alongside profit before tax of **1,128,728** and return on capital of **–178%**. These figures do not reconcile naturally. | Compare with the 2020 audited accounts and determine whether the post-tax value has a scale, digit, punctuation, or sign error. |
| 22 | Confirmed source inconsistency | The solvency-ratio note says net assets should be divided by net written premium. The reported ratios instead appear to match net assets divided by the NGN3bn minimum capital; for example, **4,346,721 ÷ 3,000,000 = 144.89%**. | Confirm that the explanatory formula, rather than the displayed ratio, is wrong. |
| 16 | Suspicious repetition in source | Every 2023 reinsurance-premium amount in Table 6 is identical to the 2022 amount, class by class, including the **1,480,940** total. | Check whether the 2022 row was copied forward accidentally or whether the equality is genuine. |
| 16 | Confirmed blank plus inference | For 2021 Agriculture, GWP is **147,892** and reinsurance premium is **103,000**, implying net premium of **44,892**. The source cell is blank and the printed total excludes this amount, while Table 12's total effectively includes it. The implied **44,892** is an inference, not a printed value. | Confirm whether 44,892 belongs in the Agriculture net-premium cell and which total is authoritative. |
| 23 and 28 | Cross-table inconsistency or basis difference | Table 1 gives 2023 gross non-life insurance contract liabilities of **951,927**, whereas Tables 11/14 give gross technical reserves of **2,176,599**. The Table 1 components also do not obviously reconcile to its displayed total. | Establish whether the tables use different accounting bases or whether Table 1 contains stale or carried-forward figures. |
| 28–29 | Confirmed cross-table inconsistency | Table 14 reports 2023 reinsurance assets of **1,120,394**, while the asset-allocation table reports **1,810,266**. The surrounding narrative also refers to approximately NGN1.81bn. | Reconcile both figures to the management accounts and identify the intended figure/basis. |
| 29 | Confirmed labelling issue | The investment-yield table is headed both **Table 15** and **Table 17**. | Confirm its intended table number and any downstream references. |
| 11–12 and 21–22 | Confirmed labelling or measure inconsistency | Table 3 reports 2023 “overall result before tax” of **794,305**. Table 12 reports profit before tax of **1,007,254** and post-tax profit of **794,305**. | Confirm whether Table 3's label should say “after tax” or whether it uses another measure. |
| 32 and 34 | Confirmed treaty-table/narrative conflicts | Fire/Terrorism capacity and line counts conflict across the narrative and tables. One passage describes **13.2bn** capacity while the table shows **5.25bn**; one comparison shows current **20 lines** versus prior **22**, while later text says the movement was from 20 to 22. The printed gross total of **4.475bn** also does not equal the visible components. | Check the underlying 2023 treaty slips and confirm the intended current/prior direction, line count, components, and capacity. |
| 34 | Possible definition/heading issue | Several “Treaty Capacity” figures appear to include the insurer's retention. For example, a **250m** retention with **20 lines** ordinarily implies **5.0bn** treaty capacity and **5.25bn** total capacity, but 5.25bn appears under Treaty Capacity. | Confirm whether the column actually represents total capacity including retention. |
| 15 | Confirmed analytical limitation | Table 5's `TOTAL` row sums class averages, maximum claims, and delay measures. Although the arithmetic may be reproducible, totals of averages/maxima are not meaningful portfolio averages or maxima. | Recalculate weighted or portfolio-level measures before using the row analytically. |
| 44 | Confirmed incomplete wording | The Oil & Gas premium wording ends mid-sentence: “63% of original net premiums on risks of”. | Check the original treaty wording or an untruncated source document. |
| 11–12 | Extraction uncertainty in source | Table 3 contains a wholly unlabelled row with values **–0.56, –0.34 and –0.35**. Its meaning cannot safely be inferred from the scan alone. | Identify the missing row label from another version of the report or the source working papers. |

### Representation caveat

The agentic workbook generally stored printed dashes and visually empty cells as blank spreadsheet cells. Where the distinction matters, a future revision should preserve separate states for **blank**, **dash**, **explicit zero**, **not applicable**, and **unresolved/illegible**.

## Limitations in the original agentic workbook

1. **Conflicting Table 1 versions were consolidated too aggressively.** The workbook retained the more complete five-year version on PDF page 23 instead of also retaining the shorter three-year version on PDF page 3. The two versions contain materially different 2023 liability figures. Both should have been preserved or compared explicitly in the Review Log rather than treating the longer version as authoritative.
2. **The Agriculture loss-ratio table on PDF page 48 was missed.** This is a genuine completeness failure in the agentic table inventory.
3. **Uncertainties were not prominent enough.** Some anomalies were noted in the workbook, but it lacked a dedicated, visible Review Log explaining confidence, materiality, source-versus-extraction status, and recommended checks.
4. **Manual consolidation involved judgement.** Combining repeated or continued tables generally produced a more usable workbook, but every consolidation decision should retain all source-page appearances and surface conflicting versions rather than silently choosing one.

## Doubleword batch review

### Batch design and truncation

- The JSONL batch request contains only **two very large requests**: one carrying **30 scanned pages** and the other **22 scanned pages**.
- Each request was limited to **8,000 output tokens**.
- The first response ends abruptly partway through the Marine row of the table on printed page 22, without closing its CSV block. This is strong evidence that the first output was truncated at the response limit.
- The workflow should check the API stop reason and completeness markers before accepting a response.

### Missing content caused by truncation/coverage failure

Five table groups on PDF pages 27–29 were absent from the resulting CSV set:

1. Asset/liability NPV, duration, and convexity.
2. Statement of financial position — liabilities.
3. Statement of financial position — assets.
4. Investment-yield table.
5. Asset-allocation table.

The Doubleword issues report described pages 21–29 as a possible legitimate coverage gap, but the source visibly contains tables there.

### Malformed CSV design

The prompt simultaneously requested comma-separated CSV and preservation of comma thousands separators, without requiring quotation of fields. A row such as:

```text
Total Admissible assets,4,881,036,5,428,290,7,109,012
```

is therefore parsed as ten fields rather than four. A lightweight raw-field-count check found **25 of 41 CSV files** with inconsistent row widths. The remaining 16 having consistent widths does not, by itself, establish semantic correctness.

Recommended alternatives are structured JSON arrays, tab-separated values, or rigorously quoted RFC-compliant CSV.

### Incomplete and fragmented logical tables

- The solvency-cover CSV contains only one data row; the continuation on the next page was not stitched into the same logical table.
- The Motor and Liability treaty was split into separate Layer 1 and Layer 2 files instead of being reconstructed as one table.
- Asking for “this page's portion” made page-local extraction easier but left the downstream process without reliable responsibility for detecting and joining continuations.

### Silent inference presented as transcription

For 2021 Agriculture, the source leaves net written premium blank. The Doubleword CSV inserts **44.892**, apparently calculated as 147.892 minus 103.000. The arithmetic inference is plausible, but it is not a verbatim transcription and the printed total still excludes it. This creates an internally inconsistent extracted table while concealing that one cell was inferred.

Future structured output should keep separate fields for `printed_value`, `normalized_value`, `inferred_value`, `inference_reason`, and `confidence`.

### Ambiguous page citations

The Doubleword filenames use the report's printed page number, while the agentic workbook uses PDF-viewer page numbers. For example, a filename containing `p19` corresponds to PDF page 20. Both conventions can be valid, but the batch prompt did not define which was required. Future citations should give both where available, for example: **PDF page 20; printed page 19**.

### Weaknesses in the generated issues report

The Doubleword issues report was useful as an initial screening document, but it appears not to have been systematically checked against the source images. Examples include:

- It speculated that **59.28** and **56.22** might mean 59,280 and 56,220, although the scan prints decimal values.
- It guessed that “199 to 2023” should be “1999 to 2023”; the source says **2019 to 2023**.
- It did not identify the truncation of the first response.
- It did not identify that Table 11 contained only one extracted row.
- It did not flag the silently inferred Agriculture value.
- It understated the scale of malformed CSV rows.

These points are a mixture of false positives and missed issues, showing why uncertainty analysis must return to the page images rather than relying only on extracted text.

### Agriculture table: discovery strength but incomplete extraction

Doubleword detected the Agriculture loss-ratio table on PDF page 48, which the original agentic workbook missed. However, its CSV omitted the current-period first row—**393% loss ratio, 58% expense ratio, and 451% combined ratio**—and retained only the 2022 and 2021 rows. This is a useful example where Doubleword performed better at table discovery but still produced an incomplete table.

## Comparative assessment

| Dimension | Doubleword batch process | Iterative agentic process |
|---|---|---|
| Speed and scaling | Strong; many pages can be submitted cheaply and quickly. | Slower and more expensive because inspection and correction are iterative. |
| Initial table discovery | Generally useful and, in one case, found a table the agentic process missed. | Good but not immune to omissions. |
| Raw output structure | Weak in this run because of conflicting CSV instructions and no schema validation. | Stronger: typed, formatted, Excel-ready data. |
| Multi-page reconstruction | Weak; continuations were fragmented or omitted. | Stronger when pages are visually reviewed and logical tables are reconstructed. |
| Cross-table reconciliation | Essentially absent. | Capable of detecting repeated-value, formula, label, and cross-table inconsistencies. |
| Source fidelity | Can silently infer or normalize despite “verbatim” instructions. | Can distinguish source text from interpretation, provided that this is made an explicit requirement. |
| Repeated versions | Preserves page-local material but may fragment it. | Can consolidate usefully, but judgement can hide conflicting versions if not logged. |
| Auditability | Raw batch requests/responses are preserved, which is valuable. | Better final citations and review commentary, especially with a dedicated Review Log. |

## Recommended hybrid workflow

Use Doubleword as a fast discovery and first-pass extraction layer, followed by targeted agentic verification:

1. Produce a page-by-page table inventory before extracting data.
2. Send one logical table, or at most one to three related pages, per model request.
3. Require schema-validated JSON rather than unquoted comma-separated text.
4. Record both PDF-viewer and printed-page numbers.
5. Store raw text separately from normalized, inferred, or calculated values.
6. Require an explicit response-complete marker and check the API stop reason for truncation.
7. Compare the page inventory with returned table IDs to expose coverage gaps.
8. Detect and join table continuations deterministically, while preserving their individual source pages.
9. Compare repeated table versions cell by cell before consolidation; retain both when they disagree materially.
10. Run automated checks for row widths, totals, subtotals, ratios, year consistency, and cross-table reconciliation.
11. Route only uncertain, contradictory, incomplete, or material tables to high-resolution agentic visual review.
12. Deliver the workbook with a prominent Review Log containing finding type, confidence, materiality, page citation, affected cells/table, and recommended user check.

## Overall conclusion

The Doubleword approach is valuable for speed, scale, and initial discovery, but this run demonstrates that its output should not flow directly into a final workbook without structural validation and source-image review. The iterative agentic approach produced a more coherent and auditable workbook, but it also missed a table and made an overconfident consolidation choice. A hybrid workflow—batch extraction first, then exception-led visual verification and reconciliation—would combine the strongest aspects of both approaches.
