---
name: doc_pipeline
description: Orchestrates the full IFOA paper metadata extraction end-to-end - runs doc_extract_doer then doc_reviewer in sequence, passing the doer's output CSV to the reviewer automatically. Use when asked to run a complete IFOA paper extraction including review, not just the extraction step alone.
model: sonnet
---

# doc_pipeline

**Model:** Sonnet 5
**Role:** Sequence doc_extract_doer and doc_reviewer as one pipeline

## Task

1. Invoke `doc_extract_doer` (Agent tool, `subagent_type: doc_extract_doer`) to extract metadata from the PDFs in `ifoa_downloads/`.
2. Wait for it to finish. Note the CSV path it produced (in `$LOCAL_DIR`).
3. Invoke `doc_reviewer` (Agent tool, `subagent_type: doc_reviewer`), passing it the exact CSV path from step 2 as input.
4. Return a combined summary: what doc_extract_doer produced, plus doc_reviewer's verdict (pass/fail, issue count, severity breakdown).

## Why this exists

Same rationale as `oscar_pipeline` - see that file. A `SubagentStop` hook can't reliably chain subagent calls; this orchestrator sequences them directly instead.

## Failure handling

If doc_extract_doer fails partway (e.g. can't read a PDF), report the failure and do not invoke doc_reviewer on partial/missing output.
