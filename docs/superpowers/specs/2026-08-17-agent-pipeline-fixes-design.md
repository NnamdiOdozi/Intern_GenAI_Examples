# Agent Pipeline Fixes — Design

Date: 2026-08-17
Status: Approved by user, pending implementation

## Context

Two agent pipelines exist in this project: `doc_pipeline` (doc_extract_doer →
doc_reviewer, for IFOA paper metadata extraction) and `oscar-pipeline`
(oscar-doer → oscar-reviewer, for Oscar winners analysis). Both were built
and exercised over the last two days. Five gaps identified through use:

1. `doc_pipeline` always spins up exactly 4 `doc_extract_doer` sub-agents
   regardless of how many PDFs are in scope — wasteful for small batches,
   insufficient for large ones.
2. Output artifacts (CSVs, TSVs, reports, charts, diagrams) are written to
   the project root (`$LOCAL_DIR/`) instead of a dedicated `output/` folder.
3. `doc_extract_doer` reads whole PDFs via the Read tool, burning tokens.
   `ifoa_downloads/prompt.txt` already specifies a cheaper approach
   (pdftotext + grep for structured fields, LLM read reserved for fields
   needing real comprehension) but the agent spec never adopted it.
4. `doc_reviewer` and `oscar-reviewer` are documented as read-only
   ("no CSV modifications") — the user wants a `Review` column added to
   the CSV/TSV itself, not just a separate markdown report.
5. Schema rigor is inconsistent across the two output formats. The doc CSV
   side has an explicit rule (in `prompt.txt`): always use Python's `csv`
   module, never hand-assemble delimited strings, so embedded commas/tabs
   in fields don't break parsing. `oscar-doer.md` doesn't state this rule
   inline (though `report.py` already follows it in practice), and
   mislabels its own tab-delimited output as "CSV report".

## Decisions

### 1. Variable doer count (doc_pipeline.md)

`batches = min(8, max(1, ceil(N / 3)))` where N = number of PDFs in scope.
Examples: N=1 → 1 batch, N=10 → 4 batches, N=24+ → caps at 8 batches.
Split the PDF list into that many near-equal batches, tag `1..batches`,
fan out that many parallel Agent calls (was hardcoded at 4).

### 2. Output folder (all 5 agent .md files + prompt.txt)

All output paths move from `$LOCAL_DIR/<file>` to `$LOCAL_DIR/output/<file>`.
Each agent runs `mkdir -p $LOCAL_DIR/output` before its first write
(idempotent — safe to run every time, never overwrites existing files by
running it). `ifoa_downloads/prompt.txt` updated to match (currently says
"output to the same folder", i.e. ifoa_downloads/ — changes to
`$LOCAL_DIR/output/`).

### 3. pdftotext+grep-first extraction (doc_extract_doer.md)

Per assigned PDF:
- `pdftotext <pdf> <tmpfile>.txt` (mktemp -d for the batch, cleaned up
  when the batch finishes — no stray temp files left on disk)
- grep cheap/structured fields directly from the txt: DOI, date patterns,
  `github.com`, URL
- For fields needing comprehension (Topic, Sub-topic, Description, ML/AI
  technique, Dataset real/simulated + granularity, Dataset modality,
  Learning paradigm & task): grep-locate the Abstract block (and
  Methods/Conclusion sections if needed) with `-A`/`-B` context, feed only
  that excerpt to Read/LLM reasoning — never the full pdftotext dump
- Delete the temp .txt files once the batch is done

### 4. Review column, written in place (doc_reviewer.md, oscar-reviewer.md)

Reviewer appends a `Review` column to the CSV/TSV it validated — one
substantive comment per row (or "No concerns"), not a numeric score.
Overwrites the same file it read (in place, same path). This replaces the
current "no modifications, report only" rule in both files. The markdown
report (full findings, severity levels, external validation) is still
produced separately — the Review column is the short per-row companion,
not a replacement.

### 5. Schema consistency (doc_extract_doer.md, oscar-doer.md, both reviewers)

- `oscar-doer.md`: fix "CSV report" label → "TSV report"; add explicit
  line stating tab-delimited via Python `csv` module (`delimiter="\t"`),
  never hand-assemble strings — mirrors the rule `prompt.txt` already
  states for the doc CSV side.
- `doc_extract_doer.md`: state the same csv-module rule inline (currently
  only lives in `prompt.txt`, which is user notes rather than the agent's
  own spec).
- `doc_reviewer.md` / `oscar-reviewer.md`: the Review-column write step
  must reopen the file via the `csv` module with the matching delimiter
  (comma for CSV, tab for TSV) — never hand-append text, which would
  break quoting on any field containing the delimiter character.

## Files touched (estimate)

| File | Change | Est. lines |
|---|---|---|
| `.claude/agents/doc_pipeline.md` | batch formula, dynamic fan-out | ~15 |
| `.claude/agents/doc_extract_doer.md` | extraction method rewrite, csv-module rule, output path | ~30 |
| `.claude/agents/doc_reviewer.md` | review column (in place), csv-module rule, output path | ~20 |
| `.claude/agents/oscar-doer.md` | output path, TSV label fix | ~5 |
| `.claude/agents/oscar-reviewer.md` | review column (in place), csv-module rule, output path | ~20 |
| `ifoa_downloads/prompt.txt` | output folder | ~2 |

No application code changes — all edits are to agent instruction files
(markdown) and one user notes file. Total ~90 new/changed lines across 6
files.

## Out of scope (separate project, not this spec)

The new `/extract-text` command (extract text from any document type or
URL into `output/`) is a separate, unrelated build — tracked as its own
brainstorm/spec, not part of this one.

## Testing

No automated test suite for these agents (they're markdown instruction
files executed by Claude, not code). Verification is a live run:
`doc_pipeline` against a small PDF set (to exercise the new batch formula
at N<4 and confirm output lands in `output/`), and `oscar-pipeline`
end-to-end (to confirm output folder + review column land correctly on
the TSV side). Both pipelines' reviewer output should show a populated
`Review` column in the actual CSV/TSV file, not just the markdown report.
