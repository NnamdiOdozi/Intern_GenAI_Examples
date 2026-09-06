# Design choices

## 2026-08-31 — Tables split across PDF pages

Round 1 now sends page `N+1` as context while inventorying page `N`. This lets the
discovery model see when a title or header at the bottom of one page belongs to rows
on the next page. Tables found only on the context page must not be inventoried.

Round 2 still receives one logical table per request. Its extraction plan expands to
two pages only when the discovery record marks a continuation. This avoids the cost
and table-contamination risk of sending two pages for every ordinary table.

A response containing headers but no rows is rejected locally as
`header_only_missing_body`. The model's `table_complete` value cannot override this
structural contradiction. The rejection records the widened `retry_pages`, ensuring
that a retry receives new page evidence rather than only a revised prompt.

### Understanding checklist

- [ ] Round 1 uses the second page only as continuation context.
- [ ] Round 2 widens the request only for a table that crosses a boundary.
- [ ] Header-only output cannot pass as a complete table.
- [ ] A continuation retry changes the supplied pages.

## 2026-09-01 — Reusable implementation boundary

The continuation fix now has canonical, generic scripts in the user-level
`dw_async_scanned_tables` skill. New runs supply their run folder, document identifier,
page count, models, and token limits at invocation time. The scripts contain no Sterling
or `nig_ins_statements` paths.

`DW_ASYNC` owns document images, table discovery, continuation planning, extraction,
and strict validation. `DW_BATCH` owns authentication, submission, polling, and raw
result retrieval. Normal `DW_ASYNC` runs use that narrow command interface instead of
reading and reconstructing the full generic batch implementation.

### Understanding checklist

- [ ] Historical run folders are evidence, not reusable source code.
- [ ] Canonical scripts live with the skill and receive each run folder as input.
- [ ] `DW_ASYNC` does not duplicate Doubleword transport code.
- [ ] Strict table results bypass the generic JSON-repair processor.

## 2026-09-01 — JSON repair is opt-in

Generic `DW_BATCH` processing now treats text as the default output format and disables
JSON repair. JSON validation is selected explicitly. Invalid JSON is preserved unchanged
unless the caller enables repair in configuration or with the per-run command flag.

This protects audit-sensitive work from silently reconstructed model responses while
retaining repair as an explicit option for low-risk tasks. `DW_ASYNC` continues to use
raw-result retrieval and its own strict validators.

### Understanding checklist

- [ ] JSON output is declared explicitly rather than inferred from prompt words.
- [ ] Validation can run without repair.
- [ ] Repair is an opt-in mutation of model output.
- [ ] `DW_ASYNC` still bypasses generic result processing entirely.
