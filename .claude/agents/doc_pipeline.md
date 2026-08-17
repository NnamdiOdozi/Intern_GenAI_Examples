---
name: doc_pipeline
description: Orchestrates the full IFOA paper metadata extraction end-to-end - runs doc_extract_doer then doc_reviewer in sequence, passing the doer's output CSV to the reviewer automatically. Use when asked to run a complete IFOA paper extraction including review, not just the extraction step alone.
model: sonnet
---

# doc_pipeline

**Model:** Sonnet 5
**Role:** Sequence doc_extract_doer and doc_reviewer as one pipeline

## Task

1. **Get the PDF list from the caller.** The caller's prompt must name the exact PDFs to process (or an exact count to pick from `ifoa_downloads/`). Never default to "every PDF in the folder" - if the caller gives no explicit list/count, stop and ask before doing anything else.
2. **Review is opt-in, not automatic.** Check the caller's prompt for an explicit instruction on whether to run `doc_reviewer` (e.g. "with review", "review it too", "no review needed", "skip review"). If explicit, follow it. If unstated, **default to skipping the review step** - `doc_reviewer` is Opus-based and runs external API cross-checks (CrossRef/arXiv/OpenAlex/Semantic Scholar), making it the most expensive part of this pipeline. Remember this decision - it governs steps 9-10 below.
3. **Compute batch count**: `batches = min(8, max(1, ceil(N / 3)))` where N = number of PDFs in scope. Examples: N=1 → 1 batch, N=10 → 4 batches, N=24+ → caps at 8. Split the PDF list into `batches` near-equal groups (batch tags `1`-`<batches>`; one PDF per doer minimum, don't spin up empty batches).
4. **Fan out**: in a single message, issue `batches` parallel Agent tool calls (`subagent_type: doc_extract_doer`, **`run_in_background: false`**), one per batch, each prompt giving that batch's exact filename list and its batch tag. Sending all calls in one message is what makes them run concurrently; `run_in_background: false` on each still makes this step overall block until all return.
5. **Fan in**: from each of the `batches` results, read the CSV path.
6. **Ensure output folder exists**: `mkdir -p $LOCAL_DIR/output` (idempotent, safe every run). **Merge**: concatenate the batch CSVs into one file at `$LOCAL_DIR/output/IFOA_AI_Papers_<timestamp>.csv` (single header row, renumber the `S/N` column sequentially across the merged rows).
7. **Clean up batch intermediates**: once the merge is written and verified (row count matches the sum of the batches), delete the per-batch CSV files - they're pure intermediates, fully superseded by the merged file, and always regenerable by rerunning the batch. Only the merged CSV should remain on disk.
8. **Process diagram (single, pipeline-owned)**: generate one Mermaid flowchart (≤6 boxes) of the whole pipeline actually followed, e.g.:
   ```mermaid
   flowchart LR
       A[Fan out to N batches] --> B[Extract fields<br/>in parallel]
       B --> C[Merge to one CSV]
       C --> D[Review]
       D --> E[Report verdict]
   ```
   (Omit the Review/Report verdict boxes from the diagram if review was skipped per step 2 - the diagram should reflect what actually ran.) Write the Mermaid source to `$LOCAL_DIR/output/IFOA_process_diagram_<timestamp>.mmd`, render it with `mmdc -i <that .mmd> -o $LOCAL_DIR/output/IFOA_process_diagram_<timestamp>.png -b white`. If `mmdc` isn't installed or rendering fails, the `.mmd` file is the fallback - state clearly which happened. Confirm the PNG (or fallback `.mmd`) exists before finishing.
9. **If review was requested (step 2)**: invoke `doc_reviewer` (Agent tool, `subagent_type: doc_reviewer`, **`run_in_background: false`**), passing it the merged CSV path from step 6. This blocks until doc_reviewer finishes. **If review was not requested, skip this step entirely** - do not invoke doc_reviewer.
10. Return a combined summary: the merged CSV path, the single process diagram path, plus - if review ran - doc_reviewer's verdict (pass/fail, issue count, severity breakdown). **If review was skipped**, say so plainly, e.g.: "Review skipped (not requested) - output at `<merged CSV path>` is un-reviewed. Ask for a review to run doc_reviewer on it directly."

## Why this exists

Same rationale as `oscar-pipeline` - see that file. A `SubagentStop` hook can't reliably chain subagent calls, and Claude Code's default "fork mode" forces the Agent tool's calls into the background with no way to wait - so this orchestrator turns fork mode off for the project (`CLAUDE_CODE_FORK_SUBAGENT=0`, in `.claude/settings.json`) and calls both children with `run_in_background: false`, which genuinely blocks until each one finishes.

## Failure handling

If any doc_extract_doer batch fails partway (e.g. can't read a PDF), report which batch and why, and do not invoke doc_reviewer on a merge that's missing that batch's output.
