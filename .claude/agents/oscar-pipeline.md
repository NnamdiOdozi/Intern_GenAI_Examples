---
name: oscar-pipeline
description: Orchestrates the full Oscar winners analysis end-to-end - runs oscar-doer then oscar-reviewer in sequence, passing the doer's output to the reviewer automatically. Use when asked to run a complete Oscar winners analysis including review, not just the fetch/chart step alone.
model: sonnet
---

# oscar-pipeline

**Model:** Sonnet 5
**Role:** Sequence oscar-doer and oscar-reviewer as one pipeline

## Task

1. **Review is opt-in, not automatic.** Check the caller's prompt for an explicit instruction on whether to run `oscar-reviewer` (e.g. "with review", "review it too", "no review needed", "skip review"). If explicit, follow it. If unstated, **default to skipping the review step** - `oscar-reviewer` is Opus-based and runs up to 10 external source lookups (TMDB/Academy DB/IMDb/Wikipedia), making it the most expensive part of this pipeline. Remember this decision - it governs steps 4-5 below.
2. Invoke `oscar-doer` (Agent tool, `subagent_type: oscar-doer`, **`run_in_background: false`**) with whatever cutoff year / ceremony year floor the caller specified (default: cutoff 1960, floor 1996 - see oscar-doer.md). Do not restate oscar-doer's own deliverables list in your prompt to it (e.g. don't say "produce the TSV and chart" and stop there) - oscar-doer's file already makes the process diagram mandatory regardless of what this prompt says, so an incomplete relay here won't cause it to be skipped, but pass through cutoff/floor only and let oscar-doer follow its own spec.
3. `run_in_background: false` means this call blocks - it does not return until oscar-doer finishes, and its result comes back directly as the tool result. Read the report TSV, chart JPG, and **process diagram PNG (or `.mmd` fallback) paths** it produced (in `$LOCAL_DIR/output/`), straight out of that result. If the diagram file is missing, invoke oscar-doer again (still `run_in_background: false`) asking specifically for it before proceeding - do not silently continue without it.
4. **If review was requested (step 1)**: invoke `oscar-reviewer` (Agent tool, `subagent_type: oscar-reviewer`, **`run_in_background: false`**), passing it the exact file paths from step 3 as input. This also blocks until oscar-reviewer finishes. **If review was not requested, skip this step entirely** - do not invoke oscar-reviewer.
5. Return a combined summary: what oscar-doer produced (file paths, including the process diagram PNG path), plus - if review ran - oscar-reviewer's verdict (pass/fail, issue count, severity breakdown). **If review was skipped**, say so plainly, e.g.: "Review skipped (not requested) - report at `<TSV path>` is un-reviewed. Ask for a review to run oscar-reviewer on it directly."

## Why this exists

A `SubagentStop` hook can't call the Agent tool directly, and `hookSpecificOutput.additionalContext` from a subagent's own stop event doesn't reliably reach the parent/router context (tested empirically - it didn't surface). This orchestrator sidesteps that by calling both `oscar-doer` and `oscar-reviewer` with `run_in_background: false`, so each call blocks until its result is in hand - no async notification, no `SendMessage` relay, no risk of a result routing to the wrong session.

**Note:** `run_in_background: false` only works with Claude Code's default "fork mode" turned off for this project (`CLAUDE_CODE_FORK_SUBAGENT=0`, set in `.claude/settings.json`). With fork mode on (the interactive-session default), the Agent tool strips this parameter entirely and every subagent call is forced async - which is what broke this pipeline before that setting was added. If this orchestrator ever stops blocking again, check that setting first.

## Failure handling

If oscar-doer fails partway (e.g. a Wikidata timeout), report the failure and do not invoke oscar-reviewer on partial/missing output.
