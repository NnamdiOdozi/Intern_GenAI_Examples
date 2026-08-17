---
name: ifoa-paper-review
description: Use when asked to review, validate, or quality-check an IFOA paper metadata extraction CSV (topic, sub-topic, dataset, authors, dates, etc.) for date accuracy, coverage, data quality, and inference flags, cross-checked against CrossRef/arXiv/OpenAlex/Semantic Scholar and the raw PDF text. Not for performing the extraction itself (see ifoa-paper-extraction) or for Oscar winners analysis.
---

# IFOA Paper Extraction Review

Reviews and validates a metadata-extraction CSV (produced from actuarial
ML/AI research PDFs) for accuracy and completeness, cross-checked
against external sources and the source PDFs themselves.

## Non-negotiable requirements

- **Write the report file** (see Output below) - findings in chat only,
  without writing the file, is an incomplete review.
- **Also add the `Review` column to the CSV in place** - this is part of
  the deliverable, not optional post-hoc cleanup.
- **Do not invent metrics.** Output format is Summary / per-row table /
  findings / **Critical/Major/Minor/Info** severity levels only. No
  numeric scores, percentages, or letter grades - if you want to convey
  "how good," use the defined severity levels in words.
- Every claim must trace to something actually checked (a CSV field, a
  line in a PDF, an API response). If not checked, say "not checked" -
  don't imply full coverage.

## What to check

1. **Date accuracy** - dates match paper's publication/submission
   metadata (title page, headers, footers); format is dd/mm/yyyy; flag
   inferred vs. stated dates, and any ranges/approximations.
2. **Coverage** - every PDF that should have been processed is present
   (no gaps, no duplicated S/N, no obviously skipped PDFs).
3. **Data quality** - author names match paper attribution (not
   hallucinated); URLs/DOIs valid and present in the PDF (or marked
   N/A); Topic/Sub-topic fit the IFOA taxonomy; ML/AI techniques are
   specific and factual, not vague.
4. **Bugs & omissions** - missing fields that should be filled (vs.
   legitimately N/A); inconsistent formatting (semicolon vs. comma,
   capitalization); typos/truncated text; contradictions within a row
   (e.g. "no dataset" but dataset modality is filled).
5. **Inference flags** - is inferred content marked "Inference:"? Any
   guesses presented as fact?

## External data validation

### Internal CSV checks (no API cost)
- No duplicate S/N, no gaps, S/N range matches expected count
- No duplicate (Author + Date) pairs - catches copy-paste errors
- URL format valid (`http://`, `https://`, or exactly `N/A`)
- Date format valid (`dd/mm/yyyy` or `N/A`)

### Free API checks (if DOI/arXiv ID present)
- **CrossRef** (`https://api.crossref.org/works/{DOI}`) - compare
  extracted authors/date against the CrossRef record, flag mismatches
- **arXiv API** - verify authors/submission date against arXiv metadata
- **OpenAlex** (free, ~10K/day) - spot-check author list completeness
- **Semantic Scholar** - quick author/date validation

### Text validation (grep the PDFs)
- `pdftotext` each PDF, grep the extracted author names/publication
  year/DOI in the raw text to verify they actually appear in the paper

## Output

Produce a **Quality Review Report** as markdown: Summary (pass/fail,
issue count), per-row validation table, detailed findings per issue (row
number, field, problem, recommendation), severity levels
(Critical/Major/Minor/Info).

**Mandatory:** ensure the output folder exists (`mkdir -p`) then write
the report there. Confirm the file exists before finishing and state its
exact path.

## Review column, written in place

After the markdown report is written, add a `Review` column to the CSV:
one substantive comment per row (concerns for that row, or "No
concerns") - not a numeric score. **Reopen and rewrite via Python's
`csv` module** (same comma delimiter, RFC 4180 quoting) - never
hand-append text with string concatenation, which breaks quoting on any
field already containing a comma. Overwrite the same file at the same
path. The markdown report stays the full-detail deliverable; the Review
column is the short per-row companion, not a replacement.
