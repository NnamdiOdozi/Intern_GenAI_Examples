# /extract-text Command — Design

Date: 2026-08-17
Status: Approved by user, implementing directly (no subagent pipeline — under 100 lines)

## Context

Need a reusable way to pull plain text out of documents (PDF, DOCX, HTML,
TXT/MD/JSON/CSV) or a URL, for downstream use (feeding other agents,
quick inspection, etc.) without hand-running `pdftotext`/`pandoc` each time.

## Decisions

**Interface:** `.claude/commands/extract-text.md`, invoked as
`/extract-text <path-or-url> [path-or-url ...]` — one or more
space-separated inputs per call.

**Execution model — inline in the current session, not a dispatched
subagent.** Pure text extraction is 100% mechanical format conversion; it
never needs LLM reasoning over the document content (unlike
`doc_extract_doer`, which classifies/labels). The command body runs shell
tools directly (`pdftotext`, `pandoc`, `curl`, `cp`) — the source content
never enters the model's context. Zero token cost per document regardless
of size.

**Per-input pipeline:**
1. `mkdir -p output/` once (idempotent).
2. URL (`http://`/`https://` prefix) → `curl -sL` to a `mktemp` file,
   then treat like a local file from here on; delete the temp file when
   done.
3. Format detection: by extension first; `file --mime-type` as fallback
   for extension-less/ambiguous inputs.
4. Route by type:
   - PDF → `pdftotext`
   - DOCX → `pandoc -t plain`
   - HTML → `pandoc -f html -t plain`
   - TXT/MD/JSON/CSV → `cp` as-is (already plain text)
   - Anything else → skip with `"unsupported format: <ext/mime>"`,
     continue to next input, don't guess
5. Output naming: `output/<original-basename-no-ext>_<timestamp>.txt`,
   timestamp = `TZ=Europe/London date +%Y%m%d_%H%M%S` (matches
   `doc_extract_doer`/`oscar-doer` convention). For URLs with no obvious
   filename in the path, derive a sanitized slug from domain+path.
6. Batch summary: after processing all inputs, report per-input result —
   output path (success) or skip reason (failure) — never silently drop
   one.

**Failure handling:** missing local file, failed curl (404/timeout), or a
corrupted file pandoc/pdftotext can't parse — report clearly per-input,
keep processing the rest of the batch, never abort the whole run over one
bad input.

**Out of scope (day one):** PPTX, XLSX, images/OCR.

## Files touched

| File | Change |
|---|---|
| `.claude/commands/extract-text.md` | New file, ~60-80 lines |

## Testing

Manual: run against one file of each supported type (PDF, DOCX, HTML,
TXT/MD/JSON), one URL, and one unsupported type (e.g. a `.zip`) to
confirm the skip path reports clearly instead of erroring the whole
batch.
