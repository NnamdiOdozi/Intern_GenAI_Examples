---
name: oscar-winners-review
description: Use when asked to review, validate, or quality-check an Oscar winners analysis (report TSV and chart, filtered by director birth year/age) for data coverage, duplicates, missing data, and field correctness, cross-checked against TMDB/Wikipedia/Academy sources. Not for producing the analysis itself (see oscars-award-winners) or IFOA paper work.
---

# Oscar Winners Analysis Review

Reviews and validates an Oscar (Academy Award) winners-by-director-age
analysis - a report TSV and chart - for data quality, coverage, and
correctness.

## Non-negotiable requirements

- **Write the report file** (see Output below) - findings in chat only
  is an incomplete review.
- **Do not invent metrics.** Output is Summary / coverage check /
  external source findings / issue table / **Critical/Major/Minor/Info**
  severity levels only - no numeric scores, percentages, letter grades.
- Every claim must trace to something actually checked - say "not
  checked" rather than imply full coverage.
- **Cap external lookups at 10 films, no more.** The aggregate/data-field
  checks below (which read the TSV directly) cover full coverage,
  duplicates, and logic checks without needing external calls - external
  lookups are for spot-checking a small sample, not a full row-by-row
  scan. If about to make an 11th external call, stop and write up what
  you have.

## Validation checks

**Data coverage** - all ceremony years represented in the chart; film
count and award count match between report and chart; no ceremony years
duplicated/out of order; year-over-year trends plausible.

**Duplicates & omissions** - no duplicate films within the same
ceremony year; no film repeated across years unless it won in multiple
years; spot-check well-known winners in range against the cutoff (e.g.
*Titanic* 1997/James Cameron b.1954, *The English Patient*
1997/Anthony Minghella b.1954) are present.

**Missing data** - director name and birth year populated for all
included rows (filtering should already have dropped no-birth-year
rows); film title and ceremony year never blank; award count > 0.

**Data field validation:**
- Birth year: 4-digit, ≤ cutoff year, no future/impossible dates,
  plausible relative to film year (director age 18+ typically)
- Ceremony year: within configured floor..present, ceremony year ≥
  film release year
- Award count: positive integers, total sum matches the chart's total

## External source validation

Fixed sample, **max 10 films total**. Pick, in priority order: any named
spot-check examples if present in this run's range; any film flagged by
an earlier check (unresolved name, out-of-range date - highest value,
prioritize within the cap); fill remaining slots with a handful spread
across the ceremony-year range (not consecutive rows).

For each film in the sample, cross-check against:
1. **Academy Awards Official Database** - film title, ceremony year,
   director name, award category count
2. **TMDB** (free API, no auth) - director info, birth year, alternate
   titles/name variations
3. **IMDb** (if available) - director credit and birth year
4. **Wikipedia Academy Awards page** for that ceremony year - major
   winners, obvious omissions

## Definition & interpretation issues

Confirm the analysis actually answers the question asked:
- Is the cutoff checking director's birth year (not film production
  year, not director's age at ceremony)?
- Is "born before YEAR" being applied as `birth_year < YEAR` (YEAR-1
  included, YEAR excluded)?
- Award scope: every category (acting, technical, shorts, docs), or
  just major ones? Confirm it matches expectation.
- Data comes from crowd-sourced Wikidata - missing/wrong birth years for
  lesser-known films are common; flag anything that looks suspect.

## Output

Produce a **Validation Report** as markdown: Summary (pass/fail, issue
count, severity breakdown), coverage check, external source findings,
issue detail table (per row, field, problem, severity), definition
clarifications.

**Mandatory:** ensure the output folder exists (`mkdir -p`) then write
the report there. Confirm the file exists before finishing and state its
exact path.

## Review column, written in place

After the markdown report is written, add a `Review` column to the TSV:
one substantive comment per row (concerns for that row, or "No
concerns") - not a numeric score. **Reopen and rewrite via Python's
`csv` module with `delimiter="\t"`** - never hand-append text with
string concatenation, which breaks quoting on any field already
containing a tab. Overwrite the same file at the same path. The markdown
report stays the full-detail deliverable; the Review column is the short
per-row companion, not a replacement.
