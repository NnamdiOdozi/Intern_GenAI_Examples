---
name: revise-practical-ai-slides
description: Make focused revisions to an existing Practical AI PowerPoint while preserving the user's manual rearrangements, design, notes, links, and unrelated content. Use when asked to update, correct, replace, reorder, or polish part of the latest AI training deck without rebuilding it from an older source.
---

# Revise Practical AI Slides

Edit the latest relevant PowerPoint directly and preserve the user's unrelated changes.

## Route the work

1. Use the available presentations skill and follow its imported-deck workflow.
2. Read `references/revision-workflow.md` before touching the deck.
3. Read `references/artifact-tool-edit-patterns.md` before writing edit code.
4. Read `references/visual-qa.md` before validation.

## Select the source safely

Run:

```text
python scripts/find_latest_deck.py <folder> --contains practical --contains ai
```

Inspect the returned candidates and confirm that the selected file matches the user's description. If the script reports ambiguity, stop and ask. Never infer that an older generator source represents the user's latest manual edits.

Export a new copy unless the user explicitly requests an in-place overwrite.

## Inspect before editing

Import the selected PPTX with `@oai/artifact-tool`. Search for the exact visible phrase, slide title, note, or object. Render the complete affected slide before making changes. Inspect all its text, images, diagrams, links, footers, and speaker notes.

Use `scripts/inspect_deck.mjs` from an initialized artifact-tool workspace when helpful. Resolve exact inspection IDs; never guess them.

## Make the smallest defensible change

Modify only the requested objects and any directly necessary layout adjustments. Preserve masters, layouts, manual ordering, theme, hyperlinks, notes, comments, and unrelated slide content. Do not allow multiple agents to write to the deck concurrently.

Update speaker notes and source blocks when the visible claim or evidence changes. Do not remove unrelated citations.

## Verify preservation

Render both source and revised decks using the presentations skill. Compare them with:

```text
python scripts/compare_rendered_slides.py <source-render-dir> <revised-render-dir> --expected-change <slide-number>
```

If unexpected slides changed, investigate and fix the export or edit before delivery. Run the presentations overflow test and:

```text
python scripts/audit_pptx.py <revised.pptx> --require-text "new phrase" --forbid "old phrase"
```

Inspect every changed slide at full size. Confirm the new copy opens, contains all expected slides and notes, and preserves working hyperlinks.

Deliver the revised PPTX, state which slide positions changed, and mention any deliberately preserved inconsistency such as stale manual footer numbering.