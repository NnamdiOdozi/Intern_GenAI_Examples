# LlamaCloud proof of concept

This folder compares three different LlamaCloud products against selected pages from the 2023 Sterling Financial Condition Report.

## Inputs

`config.toml` contains the source path, PDF viewer pages, shared table prompt, separate Parse and Extract settings, output root, and Index query. The current preflight rerun uses PDF pages `11-14,16-19`.

Parse and Extract upload the original PDF and send the configured page ranges to LlamaCloud. This preserves true PDF viewer page numbers and keeps continuation pages together. The older ten-page sample remains as a historical benchmark artifact, but the active scripts do not use it.

## Setup

Run these commands inside `llama_index/`:

```bash
uv sync
uv run python -m unittest discover -s tests
```

The API programs expect `LLAMA_CLOUD_API_KEY` to be injected into the process environment. They do not read or modify a secret file themselves.

## Experiments

Run one experiment at a time:

```bash
uv run python scripts/01_parse_markdown.py
uv run python scripts/02_parse_spreadsheet.py
uv run python scripts/03_extract_tables.py
uv run python scripts/04_index_and_query.py
```

Each command makes a real LlamaCloud request and can consume credits. The scripts do not automatically run one another.

Index requires a Starter, Pro, or Enterprise LlamaCloud plan. A lower-tier account receives HTTP 403 before the Index is created.

| Command | Main result |
|---|---|
| `uv run python scripts/01_parse_markdown.py` | `<output.root>/parse_markdown/result.md` |
| `uv run python scripts/02_parse_spreadsheet.py` | `<output.root>/parse_spreadsheet/tables.xlsx` |
| `uv run python scripts/03_extract_tables.py` | `<output.root>/extract_json/tables.json` |
| `uv run python scripts/04_index_and_query.py` | `<output.root>/index/query_result.json` |

Every experiment also retains its raw response where the API provides one. Structured log lines include a timestamp, run identifier, job or index identifier, elapsed time, and state transition.

## Interpretation

Markdown is best for visual reading. The generated XLSX workbook is the quickest direct table comparison. Extract JSON is the best candidate for later normalization into CSV or a consolidated workbook. Index measures retrieval quality, not complete table extraction.

Do not treat any generated workbook or JSON file as audited financial data. Check blank cells, units, multi-page continuations, conflicting headings, and page provenance against the source PDF. In particular, compare Parse's visible table inventory with Extract's table identifiers so a table that parsed successfully cannot disappear silently during structured extraction.
