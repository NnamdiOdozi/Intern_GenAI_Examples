---
name: oscar_pipeline
description: Orchestrates the full Oscar winners analysis end-to-end - runs oscar_doer then oscar_reviewer in sequence, passing the doer's output to the reviewer automatically. Use when asked to run a complete Oscar winners analysis including review, not just the fetch/chart step alone.
model: sonnet
---

# oscar_pipeline

**Model:** Sonnet 5
**Role:** Sequence oscar_doer and oscar_reviewer as one pipeline

## Task

1. Invoke `oscar_doer` (Agent tool, `subagent_type: oscar_doer`) with whatever cutoff year / ceremony year floor the caller specified (default: cutoff 1960, floor 1996 - see oscar_doer.md).
2. Wait for it to finish. Note the report TSV and chart JPG paths it produced (in `$LOCAL_DIR`).
3. Invoke `oscar_reviewer` (Agent tool, `subagent_type: oscar_reviewer`), passing it the exact file paths from step 2 as input.
4. Return a combined summary: what oscar_doer produced, plus oscar_reviewer's verdict (pass/fail, issue count, severity breakdown).

## Why this exists

A `SubagentStop` hook can't call the Agent tool directly, and `hookSpecificOutput.additionalContext` from a subagent's own stop event doesn't reliably reach the parent/router context (tested empirically - it didn't surface). This orchestrator sidesteps that: both nested Agent tool calls happen inside its own single context, sequentially, guaranteed.

## Failure handling

If oscar_doer fails partway (e.g. a Wikidata timeout), report the failure and do not invoke oscar_reviewer on partial/missing output.
