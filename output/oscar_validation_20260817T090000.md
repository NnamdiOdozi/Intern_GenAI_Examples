# Oscar Winners Analysis — Validation Report

- **Reviewed report:** `output/oscar_report_20260817T082447.tsv`
- **Reviewed chart:** `output/oscar_wins_by_year_20260817T082509.jpg`
- **Intermediates consulted:** `output/oscar_filtered_20260817T082443.tsv`, `output/oscar_raw_20260816T160707.tsv`
- **Run config:** birth-year cutoff 1960 (born before 1960), ceremony-year floor 1996
- **Reported result:** 151 qualifying films, 267 total award wins
- **Review date:** 2026-08-17

---

## Summary

**Verdict: PASS with issues.** The aggregate structure of the report is sound — the film count (151), award total (267), ceremony-year coverage (all 31 years 1996–2026, no gaps or duplicates), sort order, birth-year cutoff, and ceremony-year range all check out against the TSV directly. All 6 externally cross-checked films matched the report on director, ceremony year, and birth year. Two substantive issues were found, both traceable to the upstream Wikidata source rather than the pipeline logic: one unresolved director entity ID (the known Fences flag) and one undercounted award total (Emilia Pérez). One cosmetic chart-labeling issue was also found.

**Issue count: 4** (0 Critical, 1 Major, 2 Minor, 1 Info)

| Severity | Count |
|----------|-------|
| Critical | 0 |
| Major    | 1 |
| Minor    | 2 |
| Info     | 1 |

---

## Coverage check

Checks below were run programmatically against the TSV (not via external calls).

- **Row count:** 151 data rows — matches reported film count.
- **Award total:** sum of "Awards Won" = 267 — matches reported total and the chart's blue "Award wins" line.
- **Ceremony-year coverage:** all years 1996–2026 present (31 distinct years), no missing years in the span, none out of the 1996–2026 range.
- **Ordering:** rows are in strictly non-decreasing ceremony-year order.
- **Duplicates:** no film appears twice within the same ceremony year; no film appears in more than one ceremony year.
- **Blanks:** no blank film, director, ceremony-year, or birth-year fields; every award count is a positive integer (≥ 1).
- **Birth-year logic:** all birth years are 4-digit values in the range 1925–1959, i.e. all strictly < 1960 (cutoff honoured). No future or impossible dates. Multi-director rows (e.g. Fargo `1957; 1954`, Pocahontas `1955; 1954`) parse cleanly and all component years are < 1960.
- **Ceremony ≥ release:** spot-confirmed via external checks (e.g. Titanic released 1997, ceremony 1998; English Patient 1996 release, 1997 ceremony) — consistent.

**Chart vs report consistency:** The blue "Award wins" line matches per-year win sums exactly (peaks of 20/21/20/20 in 1996–1999, trough of 1 in 2014 and 2026). Year-over-year trend is plausible and explained: the visible long decline is an artifact of the *born-before-1960* filter — as ceremonies get more recent, fewer winning films have directors born before 1960, so counts fall. No unexplained spikes.

---

## External source findings

Six films cross-checked against Wikipedia / Wikidata (within the 10-lookup cap). Priority given to the two named examples and the flagged Fences row, then a spread across the ceremony-year range.

| Film | Report (year / awards / dir b.yr) | External source | Result |
|------|-----------------------------------|-----------------|--------|
| Fences | 2017 / 1 / 1954 | Wikidata Q42101 = Denzel Washington, b. 28 Dec 1954; Wikipedia: 1 win (Best Supporting Actress, 89th ceremony) | Data correct; **director name unresolved** (see MAJOR-1 / MINOR-1) |
| Titanic | 1998 / 11 / 1954 | Wikipedia: James Cameron, 11 wins, 70th ceremony (1998) | Match |
| The English Patient | 1997 / 9 / 1954 | Wikipedia: Anthony Minghella, 9 wins, 69th ceremony (1997) | Match |
| The Hurt Locker | 2010 / 6 / 1951 | Wikipedia: Kathryn Bigelow, 6 wins, 82nd ceremony (2010) | Match |
| The Power of the Dog | 2022 / 1 / 1954 | Wikipedia: Jane Campion, 1 win (Best Director), 94th ceremony (2022) | Match |
| Emilia Pérez | 2025 / 1 / 1952 | Wikipedia: Jacques Audiard, **2 wins** (Best Supporting Actress + Best Original Song), 97th ceremony (2025) | **Undercount** (see MAJOR-1) |

The two named example films (Titanic, The English Patient) are both present and correct. The Fences flag from oscar-doer is confirmed genuine — Q42101 does resolve to Denzel Washington, so the underlying facts are right and only the label failed to resolve.

---

## Issue detail table

| ID | Row(s) | Field | Problem | Severity |
|----|--------|-------|---------|----------|
| MAJOR-1 | 150 (Emilia Pérez, 2025) | Awards Won | Report shows 1 award; the film actually won 2 (Best Supporting Actress + Best Original Song "El Mal"). Verified against the raw pull (`oscar_raw_20260816T160707.tsv`), which itself contains only the Best Supporting Actress row — so this is a **completeness gap in the upstream Wikidata source**, faithfully propagated. Effect: 2025 total wins and the grand total (267) are understated by 1. | Major |
| MINOR-1 | 133 (Fences, 2017) | Director | Director field shows raw Wikidata entity ID `Q42101` instead of the resolved name "Denzel Washington". Confirmed genuine label-resolution gap (present identically in raw and filtered intermediates). Facts (b.1954, 1 award, 2017) are all correct; only the display label is wrong. | Minor |
| MINOR-2 | chart | legend label | The green line is labelled "Distinct directors" but actually plots **films per year**, not distinct director individuals. At 1996 it reads 14 (= film count) whereas there are 15 distinct directors (Pocahontas credits two: Goldberg + Gabriel); similarly 1997 reads 11 vs 12 distinct. Cosmetic — the plotted values are internally consistent, the label just overstates what is counted. | Minor |
| INFO-1 | multi-director rows | Director / Birth Year | Several rows carry two directors and two birth years separated by "; " (Pocahontas, Fargo, No Country for Old Men, Little Miss Sunshine, Slumdog Millionaire, Strangers No More). All parse cleanly and all component birth years satisfy the cutoff. Noted for awareness; no defect. | Info |

---

## Definition clarifications

- **Question interpretation:** The filter is on the **director's birth year** (Wikidata P569), which is the correct reading of "directors born before 1960." It is *not* the film's production year nor the director's age at the ceremony. Confirmed correct.
- **Cutoff semantics:** "Born before 1960" is implemented as birth year **< 1960** (1959 included, 1960 excluded). The observed max birth year in the report is 1959, consistent with this rule. Correct.
- **Ceremony-year floor:** 1996 floor honoured — no ceremony year below 1996 appears. Correct.
- **Award scope:** All categories are included, not just the majors — the filtered intermediate contains shorts (Best Animated Short), documentaries (Best Documentary Feature), international feature, film editing, sound, etc. This matches the skill's "wide, unfiltered pull of every award category" design. If the user intended only the "big" categories, this scope should be confirmed with them; as-is it is the broad interpretation.
- **Wikidata data quality:** Two of the found issues (MAJOR-1 undercount, MINOR-1 unresolved label) both originate upstream in crowd-sourced Wikidata, not in the pipeline transforms. This is the expected failure mode for lesser-covered / very recent films and should be treated as a known limitation of the data source.

---

## Recommendations

1. **MAJOR-1:** Add a reconciliation/sanity step for recent ceremonies (last ~3 years) against the Academy's official results, since Wikidata lags on new wins. At minimum, flag films where the win count differs from an authoritative source.
2. **MINOR-1:** Add a label-resolution fallback in the pipeline — any Director value still matching `^Q\d+$` after the SPARQL join should be re-queried for its `rdfs:label`, and unresolved cases surfaced as a warning rather than written through silently.
3. **MINOR-2:** Rename the chart's green series to "Films per year" (or make it genuinely count distinct directors) so the legend matches the plotted quantity.
