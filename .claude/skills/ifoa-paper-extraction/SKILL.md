---
name: ifoa-paper-extraction
description: Use when asked to extract, process, or catalogue metadata from actuarial ML/AI research PDFs in ifoa_downloads/ into a taxonomy-aligned CSV - topic, sub-topic, dataset, ML technique, authors, dates, etc. Not for reviewing/validating an already-extracted CSV (see ifoa-paper-review) or for Oscar winners analysis.
---

# IFOA Paper Metadata Extraction

Extracts structured metadata from actuarial ML/AI research PDFs (in
`ifoa_downloads/`) into a taxonomy-aligned CSV, one row per paper.

## Scope

Process **only** the PDFs explicitly named by whoever is asking - never
default to "every PDF in the folder." If no explicit filename list (or
exact count) is given, stop and ask for one rather than guessing scope.

## Extraction method - pdftotext + grep first, LLM read only where needed

The only thing that actually costs tokens is what a Bash command
*prints* - not which tool nominally ran it, not "how it's done
internally." Every step below is built around keeping printed output
small; these constraints are not optional suggestions.

1. `mktemp -d` once for the batch. Convert each PDF with
   `pdftotext <pdf> <tmpdir>/<pdf-original-filename-without-extension>.txt`
   - **name the temp file after the source PDF's own filename**, not a
   generic name like `tempfile.txt`, so it's traceable which excerpt
   came from which paper. **Always use the file-output form.** Never
   `pdftotext <pdf> -` (the dash/stdout form prints the whole document)
   and never pipe pdftotext's output anywhere that reaches your context.
2. Pull cheap/structured fields straight from the txt with grep - DOI,
   date patterns, `github.com`, URL. These rarely need LLM reasoning,
   and their matches are naturally short (one line each) - no extra
   bounding needed here.
3. For fields needing real comprehension (Topic, Sub-topic, Description,
   ML/AI technique, Dataset real/simulated + granularity, Dataset
   modality, Learning paradigm & task): grep-locate the Abstract block
   (and Methods/Conclusion section if Abstract alone isn't enough),
   **bounded**: `grep -m 8 -A 30 -B 3 -i "abstract" <tmpdir>/<name>.txt`
   - cap at 8 matches, 30 lines after / 3 before each, so even a paper
   that says "Abstract" repeatedly (citation lists, running headers,
   references) can't balloon into printing most of the document. Feed
   **only that bounded excerpt** to LLM reasoning - never the full
   pdftotext dump. **If those greps come back empty, or the capped
   excerpt genuinely doesn't contain enough signal**, mark the field
   "N/A" - don't fall back to reading the full dump or the raw PDF "to
   be sure," and don't re-run with a wider cap to compensate. That
   fallback is exactly the token-burning behavior this method exists to
   avoid.
4. **Never `cat`, `head -c <large>`, or otherwise print the full temp
   .txt file** - not even "to verify pdftotext worked." Check success
   with `test -s <file>` (exists and non-empty) instead, which prints
   nothing.
5. Delete the tmpdir (`rm -rf`) once done - no stray temp files.

## Taxonomy

Use the taxonomy found in
`practical-applications-of-ai-for-investment-actuaries-working-party-terms-of-reference.pdf`:

**Topics:**
- Forecasting & Asset Projections
- Portfolio & Risk Management
- Operational applications
- Ethics & Regulatory considerations

**Sub-topics** (per topic):
- Forecasting & Asset Projections: Strategic asset allocation / Asset liability modelling / Capital market assumption setting
- Portfolio & Risk Management: Hedge design / Stress testing / Scenario analysis / Risk monitoring
- Operational applications: Performance reporting / Risk reporting / Other Management Info
- Ethics & Regulatory considerations: Management of behavioural biases / Data governance / PRA/FCA considerations

## Output

Ensure the output folder exists (`mkdir -p`) then write a timestamped CSV
(local London time, `TZ=Europe/London date +%Y%m%d_%H%M%S` - never
UTC/system-default) with one data row per PDF processed, plus header row:

```
S/N | Topic | Sub-topic | URL | Description | Comments | Date of publication (dd/mm/yyyy) | Authors | Area of practice | Dataset (real/simulated; granularity) | Dataset modality | Code available? (language; link if any) | ML/AI technique (granular label) | Learning paradigm & task (supervised/unsupervised/etc; regression/classification)
```

**Always write via Python's `csv` module (RFC 4180, comma-delimited) -
never hand-assemble comma-joined strings**, so field values containing
commas stay correctly quoted.

Each field must be:
- Factual and sourced from the PDF text
- Marked "N/A" if not found in the paper
- Flagged with "Inference:" if inferred rather than stated

## Parallelizing across many PDFs

If processing more than a handful of PDFs, split the list into
near-equal batches and process them in parallel rather than one long
serial pass - roughly 3 PDFs per batch works well, capped at a sane
maximum (8) so you don't spin up more parallel work than the PDF count
justifies. Each batch produces its own CSV; merge into a single
timestamped file afterward (single header row, `S/N` renumbered
sequentially across the merge), then delete the per-batch intermediates
since they're fully superseded by the merged file.
