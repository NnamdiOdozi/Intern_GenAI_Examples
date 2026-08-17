# Quality Review Report — IFOA AI Papers Extraction

- **CSV reviewed:** `/home/nodozi/projects/Intern_GenAI_Examples/output/IFOA_AI_Papers_20260817_082507.csv`
- **Rows:** 7 (S/N 1–7), merged from a 3-batch parallel extraction run
- **Reviewer:** doc_reviewer (Opus 4.8)
- **Review date:** 2026-08-17
- **Verdict:** **PASS** (with minor advisory findings — no Critical or Major issues)

## Summary

| Metric | Result |
|---|---|
| Overall verdict | PASS |
| Total issues found | 5 |
| Critical | 0 |
| Major | 0 |
| Minor | 3 |
| Info | 2 |

All 7 rows were validated against the raw PDF text (via `pdftotext`). Every author name, date, title and URL that I checked traces to text actually present in the corresponding source PDF — no hallucinated authors or fabricated dates were found. Internal CSV integrity (S/N uniqueness, URL format, date format, no duplicate Author+Date pairs) passed cleanly. Inference flags are used appropriately and consistently ("Inference:" prefix, "N/A" for genuinely absent fields).

### Scope note on external APIs
All 7 source documents are **IFoA grey literature** (a blog post, two consultation responses, a webinar-listing page, a slide deck, and joint RSS/IFoA guidance). **No DOIs or arXiv IDs appear in any source PDF** (verified by grep), so CrossRef/arXiv/OpenAlex/Semantic Scholar lookups by identifier are **not applicable** for 6 of 7 rows. The one exception — the Allan/Cantle 2011 ERM paper (Row 2) — was cross-checked against CrossRef by bibliographic query and **confirmed** (see Finding 1).

### Coverage note
This run covers **7 papers (S/N 1–7)**, not the "all 10 PDFs" pattern in the generic checklist. The `ifoa_downloads/` folder contains ~30+ PDFs; this batch deliberately processed a 7-document subset. Within the delivered set, coverage is complete: no gaps, no duplicate S/N, no duplicated rows. I did **not** audit whether the "right" 7 were selected from the larger pool — that is a scoping decision upstream of this review.

## Per-row validation table

| S/N | Source PDF | Title match | Authors match | Date match | URL valid | Inference flags | Row status |
|---|---|---|---|---|---|---|---|
| 1 | Using natural language processing...reg-tech | Yes | Yes (Muqiu Liu, Estelle Xu, Chengcheng Wang) | Yes (01/09/2023 on p.1) | Yes | OK | PASS |
| 2 | review-use-complex-systems...erm-practice | Yes | Yes (Allan, Cantle, Godfrey, Yin) — CrossRef confirmed | Presentation date 28/11/2011 (see F1) | Yes | OK (pre-ML-era flagged) | PASS (Minor) |
| 3 | Key findings from the data science thematic review | Yes (webinar page) | Yes (Marshall, Gordon, Buckley) | Yes (19/03/2024 webinar date; see F2) | Yes | OK (non-paper flagged) | PASS (Info) |
| 4 | ifoa-response-to-treasury-select-committee...ai | Yes | Yes (IFoA organisational) | Yes (11/04/2025 on p.1) | Yes | OK | PASS |
| 5 | ifoa-response-to-bank-of-england...dp522 | Yes | Yes (IFoA; Steven Graham contact) | Yes (17/02/2023 on p.1) | Yes | OK | PASS |
| 6 | IFoA Research Deep Dive 2025 slides | Yes | Mostly (see F3: "Dylan Lieu/Liew") | Yes (28/08/2025 on p.1) | Yes | OK (non-paper flagged) | PASS (Minor) |
| 7 | guide-ethical-data-science | Yes | Yes (RSS + IFoA joint) | N/A — only "August 2019" in doc (see F4) | Yes | OK | PASS (Minor) |

## Detailed findings

### Finding 1 — Row 2, Date of publication — Minor
- **Problem:** The CSV date `28/11/2011` is the date the paper was **presented** to the Institute and Faculty of Actuaries (per the PDF title page: "Presented to The Institute and Faculty of Actuaries — 28 November 2011 (London)"). CrossRef shows the paper was formally **published in the British Actuarial Journal Vol. 18(1), March 2013 (online 14 Nov 2012), DOI 10.1017/s135732171200030x**. The extracted date is therefore a presentation/submission date, not the journal publication date.
- **Why this is only Minor:** The date is correctly and verifiably sourced from the PDF title page, which is the document actually processed. This is a legitimate reading, not an error. But it is a *presentation* date presented as a *publication* date without qualification.
- **Recommendation:** Optionally annotate as "28/11/2011 (Inference: presentation date; BAJ publication 2013)" or add a note in Comments. Authors are fully confirmed by CrossRef — no action needed there.

### Finding 2 — Row 3, Date of publication — Info
- **Problem:** Date `19/03/2024` is the **webinar event date** ("Tue 19 Mar 2024"), whereas the PDF also states the underlying thematic review report "was published on 26 February" (2024). Since the processed PDF is the webinar-listing page (not the report), the webinar date is the defensible choice.
- **Recommendation:** No change required. The Comments field already correctly explains this is an event-listing page and that the report itself is a separate document. Acceptable as-is.

### Finding 3 — Row 6, Authors — Minor
- **Problem:** The Authors field records the AI & Data Science presenter as **"Dylan Lieu/Liew"** (hedged spelling). The source PDF (slide 2, "Presenters") reads **"Dylan Lieu"** unambiguously. The alternative "Liew" spelling is an unsourced hedge not supported by the document text.
- **Recommendation:** Change to "Dylan Lieu" to match the PDF exactly, or, if there is external reason to believe the surname is "Liew", mark it explicitly as "Inference:". As written it presents a guess alongside the sourced value.

### Finding 4 — Row 7, Date of publication — Minor
- **Problem:** Date is `N/A` with an inline inference note that the document states "August 2019" but gives no day, so `dd/mm/yyyy` cannot be populated. Verified: the PDF cover and copyright line both read "August 2019" / "© 2019". The N/A is honest, but a month-precision date is available and is being discarded entirely.
- **Recommendation:** Consider a convention for month-only dates (e.g. `01/08/2019` with an explicit "Inference: day unknown, month = August 2019" note) so the temporal information is not lost. Current handling is defensible and correctly flagged; this is a data-completeness improvement, not a correctness fix.

### Finding 5 — Cross-row, Authors formatting — Info
- **Problem:** Author-list separators are inconsistent across rows: Row 1 uses semicolons ("Muqiu Liu (...); Estelle Xu (...)"), Row 2 uses the PDF's raw "N. Allan; N. Cantle; P. Godfrey; Y. Yin" (initials only, no separator normalisation vs. full names elsewhere), Row 6 uses a long semicolon list with parenthetical practice areas. This is cosmetic and does not affect correctness, but reduces machine-parseability.
- **Recommendation:** Optional — standardise on a single separator (semicolon) and a consistent "Name (affiliation)" pattern if the CSV will be parsed downstream.

## What was checked vs. not checked

- **Checked:** all 7 rows' author names, dates, titles against raw PDF text (`pdftotext`); DOI/arXiv presence in all 7 PDFs (none found); internal CSV integrity (S/N range/uniqueness, URL regex, date regex, Author+Date duplicate detection); CrossRef bibliographic lookup for Row 2.
- **Not checked:** full ML-technique factual depth for every row beyond the title/abstract region read; whether the 7-document subset is the "correct" selection from the ~30+ PDFs in `ifoa_downloads/`; live-fetch of each URL (URLs validated for format only, not HTTP reachability).
