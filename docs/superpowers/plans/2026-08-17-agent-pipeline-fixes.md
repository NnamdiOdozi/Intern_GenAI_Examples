# Agent Pipeline Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 5 gaps across `doc_pipeline`/`doc_extract_doer`/`doc_reviewer` and `oscar-doer`/`oscar-reviewer`: variable sub-agent count, output/ folder, pdftotext+grep-first extraction, in-place Review column, and CSV/TSV schema-rigor consistency.

**Architecture:** All changes are edits to existing agent instruction files (`.claude/agents/*.md`) and one user notes file (`ifoa_downloads/prompt.txt`). No application code, no test suite — these are markdown specs interpreted by Claude at agent-run time. Verification is by re-reading the edited file (grep the changed string) and, for the last task, one live run of each pipeline.

**Tech Stack:** Markdown agent specs (Claude Code `.claude/agents/`), bash (`pdftotext`, `grep`, `mktemp`), Python `csv` module (already used by `report.py`, referenced not rewritten).

**Spec:** `docs/superpowers/specs/2026-08-17-agent-pipeline-fixes-design.md`

---

### Task 1: `ifoa_downloads/prompt.txt` — output folder

**Files:**
- Modify: `ifoa_downloads/prompt.txt:1-2`

- [ ] **Step 1: Edit the output-location line**

Old string:
```
Extract the following information from the PDF docs in this folder and place each of them in its own field in a timestamped csv file called IFOA_AI_Papers_Timestamp 
that you should ouptut to the same folder.  You can find the topic and subtopics in the pdf document called 
```

New string:
```
Extract the following information from the PDF docs in this folder and place each of them in its own field in a timestamped csv file called IFOA_AI_Papers_Timestamp 
that you should output to $LOCAL_DIR/output/ (create the folder with mkdir -p if it doesn't exist).  You can find the topic and subtopics in the pdf document called 
```

- [ ] **Step 2: Verify**

Run: `grep -n "output to" ifoa_downloads/prompt.txt`
Expected: line shows `$LOCAL_DIR/output/`

---

### Task 2: `doc_pipeline.md` — variable batch count + output folder

**Files:**
- Modify: `.claude/agents/doc_pipeline.md:14-30`

- [ ] **Step 1: Replace fixed-4 batching (steps 2-3) with variable formula**

Old string:
```
2. Split that list into 4 near-equal batches (batch tags `1`-`4`; if fewer than 4 PDFs, use fewer batches - one PDF per doer minimum, don't spin up empty batches).
3. **Fan out**: in a single message, issue 4 parallel Agent tool calls (`subagent_type: doc_extract_doer`, **`run_in_background: false`**), one per batch, each prompt giving that batch's exact filename list and its batch tag. Sending all 4 in one message is what makes them run concurrently; `run_in_background: false` on each still makes this step overall block until all 4 return.
```

New string:
```
2. **Compute batch count**: `batches = min(8, max(1, ceil(N / 3)))` where N = number of PDFs in scope. Examples: N=1 → 1 batch, N=10 → 4 batches, N=24+ → caps at 8. Split the PDF list into `batches` near-equal groups (batch tags `1`-`<batches>`; one PDF per doer minimum, don't spin up empty batches).
3. **Fan out**: in a single message, issue `batches` parallel Agent tool calls (`subagent_type: doc_extract_doer`, **`run_in_background: false`**), one per batch, each prompt giving that batch's exact filename list and its batch tag. Sending all calls in one message is what makes them run concurrently; `run_in_background: false` on each still makes this step overall block until all return.
```

- [ ] **Step 2: Ensure output folder + update merged-CSV path (step 5)**

Old string:
```
5. **Merge**: concatenate the 4 CSVs into one file at `$LOCAL_DIR/IFOA_AI_Papers_<timestamp>.csv` (single header row, renumber the `S/N` column sequentially across the merged rows).
6. **Clean up batch intermediates**: once the merge is written and verified (row count matches the sum of the 4 batches), delete the 4 per-batch CSV files - they're pure intermediates, fully superseded by the merged file, and always regenerable by rerunning the batch. Only the merged CSV should remain on disk.
```

New string:
```
5. **Ensure output folder exists**: `mkdir -p $LOCAL_DIR/output` (idempotent, safe every run). **Merge**: concatenate the batch CSVs into one file at `$LOCAL_DIR/output/IFOA_AI_Papers_<timestamp>.csv` (single header row, renumber the `S/N` column sequentially across the merged rows).
6. **Clean up batch intermediates**: once the merge is written and verified (row count matches the sum of the batches), delete the per-batch CSV files - they're pure intermediates, fully superseded by the merged file, and always regenerable by rerunning the batch. Only the merged CSV should remain on disk.
```

- [ ] **Step 3: Update diagram paths (step 7)**

Old string:
```
   Write the Mermaid source to `$LOCAL_DIR/IFOA_process_diagram_<timestamp>.mmd`, render it with `mmdc -i <that .mmd> -o $LOCAL_DIR/IFOA_process_diagram_<timestamp>.png -b white`. If `mmdc` isn't installed or rendering fails, the `.mmd` file is the fallback - state clearly which happened. Confirm the PNG (or fallback `.mmd`) exists before finishing.
```

New string:
```
   Write the Mermaid source to `$LOCAL_DIR/output/IFOA_process_diagram_<timestamp>.mmd`, render it with `mmdc -i <that .mmd> -o $LOCAL_DIR/output/IFOA_process_diagram_<timestamp>.png -b white`. If `mmdc` isn't installed or rendering fails, the `.mmd` file is the fallback - state clearly which happened. Confirm the PNG (or fallback `.mmd`) exists before finishing.
```

- [ ] **Step 4: Verify**

Run: `grep -n "batches\|output/" .claude/agents/doc_pipeline.md`
Expected: batch formula present, all three output paths (`IFOA_AI_Papers`, `.mmd`, `.png`) show `output/`

---

### Task 3: `doc_extract_doer.md` — pdftotext+grep-first extraction, csv-module rule, output folder

**Files:**
- Modify: `.claude/agents/doc_extract_doer.md:14,18`

- [ ] **Step 1: Replace the extraction method (line 14)**

Old string:
```
Read exactly the PDFs listed by filename in the caller's prompt (all in `/home/nodozi/projects/Intern_GenAI_Examples/ifoa_downloads/`) and extract structured metadata following the specification in `ifoa_downloads/prompt.txt`. **Do not read any PDF not named in your assigned list** — never fall back to "every PDF in the folder." If the caller's prompt gives no explicit filename list, stop and ask the caller for one rather than guessing scope.
```

New string:
```
Process exactly the PDFs listed by filename in the caller's prompt (all in `/home/nodozi/projects/Intern_GenAI_Examples/ifoa_downloads/`) — **do not read any PDF not named in your assigned list**, never fall back to "every PDF in the folder." If the caller's prompt gives no explicit filename list, stop and ask the caller for one rather than guessing scope.

**Extraction method — pdftotext + grep first, LLM read only where needed:**
1. `mktemp -d` once for this batch; convert each assigned PDF with `pdftotext <pdf> <tmpdir>/<pdf_stem>.txt`.
2. Pull cheap/structured fields straight from the txt with grep — DOI, date patterns, `github.com`, URL. These rarely need LLM reasoning.
3. For fields that need real comprehension (Topic, Sub-topic, Description, ML/AI technique, Dataset real/simulated + granularity, Dataset modality, Learning paradigm & task): grep-locate the Abstract block (and Methods/Conclusion section if the Abstract alone isn't enough) with `-A`/`-B` context, and feed **only that excerpt** to Read/LLM reasoning — never the full pdftotext dump of a long paper.
4. Delete the batch's tmpdir (`rm -rf`) once all assigned PDFs are processed — no stray temp files left on disk.

Extract structured metadata following the specification in `ifoa_downloads/prompt.txt`.
```

- [ ] **Step 2: Update output path + add csv-module rule (line 18)**

Old string:
```
Output a timestamped CSV file to `$LOCAL_DIR/IFOA_AI_Papers_<timestamp>_batch<tag>.csv` (project root; drop `_batch<tag>` if no tag given) with the following columns. Timestamp must be **local London time** (Europe/London — auto BST/GMT), format `YYYYMMDD_HHMMSS`, e.g. via `TZ=Europe/London date +%Y%m%d_%H%M%S` — never UTC/system-default:
```

New string:
```
Ensure `$LOCAL_DIR/output/` exists (`mkdir -p`, idempotent) then output a timestamped CSV file to `$LOCAL_DIR/output/IFOA_AI_Papers_<timestamp>_batch<tag>.csv` (drop `_batch<tag>` if no tag given) with the following columns. Timestamp must be **local London time** (Europe/London — auto BST/GMT), format `YYYYMMDD_HHMMSS`, e.g. via `TZ=Europe/London date +%Y%m%d_%H%M%S` — never UTC/system-default. **Always write via Python's `csv` module (RFC 4180, comma-delimited) — never hand-assemble comma-joined strings**, so field values containing commas stay correctly quoted.
```

- [ ] **Step 3: Verify**

Run: `grep -n "pdftotext\|mktemp\|csv.*module\|output/" .claude/agents/doc_extract_doer.md`
Expected: extraction method block present, csv-module rule present, output path shows `output/`

---

### Task 4: `doc_reviewer.md` — Review column in place, csv-module rule, output folder

**Files:**
- Modify: `.claude/agents/doc_reviewer.md:24,63-65,105-107`

- [ ] **Step 1: Update input path (line 24)**

Old string:
```
Reads: `$LOCAL_DIR/IFOA_AI_Papers_<timestamp>.csv` (from doc_extract_doer)  
```

New string:
```
Reads: `$LOCAL_DIR/output/IFOA_AI_Papers_<timestamp>.csv` (from doc_extract_doer)  
```

- [ ] **Step 2: Update report file location (lines 63-65)**

Old string:
```
**Mandatory action, not a suggestion:** write the report to `$LOCAL_DIR/IFOA_AI_Papers_REVIEW_<timestamp>.md` (project root) using the Write tool. Before returning your final response, confirm the file exists (e.g. re-read it or `ls` it) and state its exact path in your response.
```

New string:
```
**Mandatory action, not a suggestion:** ensure `$LOCAL_DIR/output/` exists (`mkdir -p`), then write the report to `$LOCAL_DIR/output/IFOA_AI_Papers_REVIEW_<timestamp>.md` using the Write tool. Before returning your final response, confirm the file exists (e.g. re-read it or `ls` it) and state its exact path in your response.
```

- [ ] **Step 3: Replace "No modifications to CSV" section with in-place Review column**

Old string:
```
## No modifications to CSV

Report findings only. Do not edit the CSV. Extraction doer will address issues in a second pass if needed.
```

New string:
```
## Review column, written in place

After the markdown report is written, add a `Review` column (15th column) to the CSV you validated: one substantive comment per row (your concerns for that specific row, or "No concerns" if none) — not a numeric score. **Reopen and rewrite the file via Python's `csv` module** (same comma delimiter, RFC 4180 quoting) — never hand-append text with string concatenation, which would break quoting on any field already containing a comma. Overwrite the same file at the same path (in place). The markdown report remains the full-detail deliverable; the Review column is the short per-row companion, not a replacement.
```

- [ ] **Step 4: Verify**

Run: `grep -n "output/\|Review column\|csv.*module" .claude/agents/doc_reviewer.md`
Expected: input/output paths show `output/`, Review-column section present with csv-module instruction

---

### Task 5: `oscar-doer.md` — output folder, fix TSV mislabel, csv-module rule

**Files:**
- Modify: `.claude/agents/oscar-doer.md:22,38-42`

- [ ] **Step 1: Update output location (line 22)**

Old string:
```
- **Output location:** `$LOCAL_DIR/` (project root)
```

New string:
```
- **Output location:** `$LOCAL_DIR/output/` (ensure with `mkdir -p` before first write, idempotent)
```

- [ ] **Step 2: Fix mislabeled "CSV report", add csv-module rule, update all output paths**

Old string:
```
## Output

- CSV report: `$LOCAL_DIR/oscar_report_<timestamp>.tsv` (project root, tabular deliverable)
- Chart: `$LOCAL_DIR/oscar_wins_by_year_<timestamp>.jpg` (project root, visual deliverable)
- Process diagram: `$LOCAL_DIR/oscar_process_diagram_<timestamp>.png` (falls back to `.mmd` if rendering isn't available)
- Raw/filtered intermediate files for audit trail in project root
```

New string:
```
## Output

- TSV report: `$LOCAL_DIR/output/oscar_report_<timestamp>.tsv` (tabular deliverable). **Always write via Python's `csv` module with `delimiter="\t"` — never hand-assemble tab-joined strings**, so field values containing a tab stay correctly quoted (report.py already does this — keep it that way).
- Chart: `$LOCAL_DIR/output/oscar_wins_by_year_<timestamp>.jpg` (visual deliverable)
- Process diagram: `$LOCAL_DIR/output/oscar_process_diagram_<timestamp>.png` (falls back to `.mmd` if rendering isn't available)
- Raw/filtered intermediate files for audit trail in `$LOCAL_DIR/output/`
```

- [ ] **Step 3: Update process-diagram paths in step 5**

Old string:
```
   1. Write the Mermaid source to `$LOCAL_DIR/oscar_process_diagram_<timestamp>.mmd`
   2. Render it: `mmdc -i $LOCAL_DIR/oscar_process_diagram_<timestamp>.mmd -o $LOCAL_DIR/oscar_process_diagram_<timestamp>.png -b white`
```

New string:
```
   1. Write the Mermaid source to `$LOCAL_DIR/output/oscar_process_diagram_<timestamp>.mmd`
   2. Render it: `mmdc -i $LOCAL_DIR/output/oscar_process_diagram_<timestamp>.mmd -o $LOCAL_DIR/output/oscar_process_diagram_<timestamp>.png -b white`
```

- [ ] **Step 4: Verify**

Run: `grep -n "output/\|TSV report\|csv.*module" .claude/agents/oscar-doer.md`
Expected: all output paths show `output/`, "TSV report" (not "CSV report"), csv-module rule present

---

### Task 6: `oscar-reviewer.md` — Review column in place, csv-module rule, output folder

**Files:**
- Modify: `.claude/agents/oscar-reviewer.md:24-25,65,108-110`

- [ ] **Step 1: Update input/output paths (lines 24-25)**

Old string:
```
Reads: `$LOCAL_DIR/oscar_report_<timestamp>.tsv` and `$LOCAL_DIR/oscar_wins_by_year_<timestamp>.jpg` (from oscar-doer)  
```

New string:
```
Reads: `$LOCAL_DIR/output/oscar_report_<timestamp>.tsv` and `$LOCAL_DIR/output/oscar_wins_by_year_<timestamp>.jpg` (from oscar-doer)  
```

- [ ] **Step 2: Update report file location (line 65)**

Old string:
```
**Mandatory action, not a suggestion:** write the report to `$LOCAL_DIR/oscar_validation_<timestamp>.md` (project root) using the Write tool. Before returning your final response, confirm the file exists (e.g. re-read it or `ls` it) and state its exact path in your response.
```

New string:
```
**Mandatory action, not a suggestion:** ensure `$LOCAL_DIR/output/` exists (`mkdir -p`), then write the report to `$LOCAL_DIR/output/oscar_validation_<timestamp>.md` using the Write tool. Before returning your final response, confirm the file exists (e.g. re-read it or `ls` it) and state its exact path in your response.
```

- [ ] **Step 3: Replace "No CSV modifications" section with in-place Review column**

Old string:
```
## No CSV modifications

Report only. `oscar-doer` will address critical issues in a second run if needed.
```

New string:
```
## Review column, written in place

After the markdown report is written, add a `Review` column to the TSV you validated: one substantive comment per row (your concerns for that row, or "No concerns" if none) — not a numeric score. **Reopen and rewrite the file via Python's `csv` module with `delimiter="\t"`** (matching `report.py`'s convention) — never hand-append text with string concatenation, which would break quoting on any field already containing a tab. Overwrite the same file at the same path (in place). The markdown report remains the full-detail deliverable; the Review column is the short per-row companion, not a replacement.
```

- [ ] **Step 4: Verify**

Run: `grep -n "output/\|Review column\|delimiter" .claude/agents/oscar-reviewer.md`
Expected: input/output paths show `output/`, Review-column section present with csv-module + tab-delimiter instruction

---

### Task 7: Full-diff review (no auto-commit)

**Files:** none new — review only

- [ ] **Step 1: Show the full diff for user review**

Run: `git diff --stat .claude/agents/ ifoa_downloads/prompt.txt`
Expected: 6 files changed (doc_pipeline.md, doc_extract_doer.md, doc_reviewer.md, oscar-doer.md, oscar-reviewer.md, prompt.txt)

- [ ] **Step 2: Ask user to review diff and confirm before any commit**

Per project CLAUDE.md: "Only create commits when requested by the user." Do not run `git commit` in this task — present the diff and wait for explicit go-ahead.

---

### Task 8: Live verification (per spec's Testing section)

**Files:** none — this is a live pipeline run, not a file edit

- [ ] **Step 1: Run `doc_pipeline` against a small PDF set (N<4, e.g. 2 PDFs)**

Confirms: batch formula produces 1 batch (not the old fixed 4), output lands in `$LOCAL_DIR/output/`, extraction uses pdftotext+grep (spot-check no full-PDF Read-tool token spike in transcript), reviewer writes a populated `Review` column into the CSV in place.

- [ ] **Step 2: Run `oscar-pipeline` end-to-end**

Confirms: output lands in `$LOCAL_DIR/output/`, `oscar-reviewer` writes a populated `Review` column into the TSV in place, TSV still parses correctly (`csv.DictReader` with `delimiter="\t"` round-trips with no column-count drift).

- [ ] **Step 3: Report results to user**

State: batch counts observed, output/ folder contents, confirmation both Review columns are populated in the actual CSV/TSV files (not just the markdown reports).

---

## Self-Review Notes

- **Spec coverage:** All 5 spec decisions map 1:1 to tasks — Task 2 (batching), Tasks 1-6 (output folder, spread across every file that writes output), Task 3 (extraction method), Tasks 4+6 (review column), Tasks 3+4+5+6 (schema consistency). Task 8 covers the spec's Testing section.
- **Placeholder scan:** No TBD/TODO; every edit step shows exact old/new string content.
- **Type/path consistency:** `$LOCAL_DIR/output/` used identically across all 6 files; CSV always comma+`csv` module, TSV always tab+`csv` module — no cross-contamination between the two formats.
