# IFOA AI Papers — Quality Review Report

- **Reviewed CSV:** `/home/nodozi/projects/Intern_GenAI_Examples/output/IFOA_AI_Papers_20260817_082525.csv`
- **Review timestamp:** 2026-08-17 08:30:00
- **Scope of this run:** 2 PDFs only (small verification run), so coverage expectation is **S/N 1–2**, not the usual 1–10.
- **Source PDFs:**
  1. `ifoa_downloads/AI, data science and emerging technologies.pdf` (S/N 1)
  2. `ifoa_downloads/Actuarial Modelling in the Age of AI Agents.pdf` (S/N 2)

## Summary

- **Overall verdict: PASS.** Both rows are accurate against their source PDFs and against external cross-checks. No Critical or Major issues found.
- **Issues found: 3** — 0 Critical, 0 Major, 2 Minor, 1 Info.
- Both extracted rows are legitimately dominated by `N/A` because neither source is an empirical ML/AI research paper (one is an organisational governance webpage, the other a discursive thought-leadership article). The `N/A` values are correctly justified in the Description/Comments fields, not left as unexplained blanks — this is the correct behaviour, not an omission.

### Checks performed (traceability)

| Check | Method | Result |
|---|---|---|
| Column count / header integrity | Python `csv` (14 cols) | Pass — 14 columns, headers intact |
| S/N uniqueness & range (1–2) | Python `csv` | Pass — `[1, 2]`, unique, no gaps |
| Duplicate (Author + Date) pairs | Python `csv` | Pass — none |
| Date format (dd/mm/yyyy or N/A) | regex | Pass — both valid |
| URL format (http/https or N/A) | regex | Pass — both valid |
| Row 2 author in raw PDF text | `pdftotext` + grep | Pass — "DANIEL CRAIG RAMSAY" present |
| Row 2 date in raw PDF text | `pdftotext` + grep | Pass — "MAY 08, 2025" present on title page |
| Row 1 date | `pdftotext` | Pass — no publication date on page; N/A correct |
| Row 1 URL live | WebFetch | Pass — HTTP OK, page loads, content matches |
| Row 2 URL | VLE resource link | Not fetched live (auth-gated VLE); link form valid |
| CrossRef title lookup (Row 2) | CrossRef API via WebFetch | No record — consistent with a Substack/VLE article having no DOI |
| arXiv / OpenAlex / Semantic Scholar | — | Not applicable — neither source has a DOI/arXiv ID; Row 2 is a non-indexed Substack article, Row 1 is a webpage |

## Per-row validation table

| S/N | Source | Author check | Date check | URL check | Topic/Sub-topic fit | Inference flags | Row verdict |
|---|---|---|---|---|---|---|---|
| 1 | AI, data science and emerging technologies (webpage) | N/A — no single author (org page); correct | N/A — no publication date on page; correct | Live, content matches (WebFetch) | Reasonable; flagged as Inference | Properly marked "Inference:" | PASS |
| 2 | Actuarial Modelling in the Age of AI Agents (article) | "Daniel Craig Ramsay" — verified in PDF | 08/05/2025 — verified ("MAY 08, 2025") | VLE resource, valid form | Reasonable; flagged as Inference | Properly marked "Inference:" | PASS |

## Detailed findings

### Finding 1 — Minor — Row 1, Authors field
- **Field:** Authors
- **Problem:** Author is `N/A`. The source webpage does list named board members (Asif John – Chair, John Ng – Deputy Chair, etc.), so "no attribution available" is not strictly true. However, board members are not *authors* of the page in any meaningful sense.
- **Assessment:** `N/A` is defensible and arguably the correct call for an authorless governance webpage. Not a data error.
- **Recommendation:** Optionally note in Comments that named board members exist but are not page authors. No change required to the Authors value.

### Finding 2 — Minor — Row 2, potential DOI confusion source
- **Field:** URL / Code available?
- **Problem:** The PDF's reference list contains a DOI (`https://doi.org/10.48550/arXiv.2302.06590`) and several tool links (CrewAI, LangGraph, GitHub Next). These belong to *cited third-party works*, not to this paper.
- **Assessment:** The extraction correctly did **not** adopt the cited DOI as the paper's own URL, and correctly marked "Code available?" as N/A (external tools are examples, not accompanying code). This is the right behaviour — flagged only to document that the trap was checked and avoided.
- **Recommendation:** None. Confirmed correct.

### Finding 3 — Info — Row 2, date provenance
- **Field:** Date of publication (dd/mm/yyyy)
- **Problem:** Date `08/05/2025` is a stated date (title page "MAY 08, 2025" and footer "© 2025 Daniel Ramsay"), correctly converted US-format month/day to dd/mm/yyyy. Not inferred, not a range.
- **Recommendation:** None. Optional: the article states it is "second in a series"; the series context is captured in Description.

## External data validation notes

- **CrossRef:** No matching record for the AI Agents article — expected, as it is a Substack post republished on the IFoA VLE, with no assigned DOI. Absence of a CrossRef record is therefore *not* a defect.
- **arXiv / OpenAlex / Semantic Scholar:** Not queried — no DOI/arXiv ID exists for either source, so these indexes are not applicable. (Not checked = genuinely N/A here, not skipped coverage.)
- **Raw PDF text (pdftotext):** Author and date for Row 2 both grep-confirmed in the source. Row 1 has no author/date to confirm; its factual claims (Nov 2025 formation, four pillars, 2018 working-party origin) match both the PDF and the live webpage.

## Inference flags audit

- Both rows use the explicit `Inference:` prefix on genuinely inferred fields (Topic, Sub-topic, Area of practice, ML/AI technique where synthesised). No guesses are presented as fact.
- Factual `N/A` fields are each accompanied by a justification in Description or Comments — no unexplained blanks.

## Bottom line

The 2-row verification run is clean. Coverage (S/N 1–2) is complete, formatting is valid, dates and the one real author are confirmed against source text, and inference is properly flagged. No blocking or must-fix issues.
