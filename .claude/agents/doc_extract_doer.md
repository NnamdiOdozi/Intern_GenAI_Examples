---
name: doc_extract_doer
description: Extracts structured metadata (topic, sub-topic, dataset, ML technique, authors, dates, etc.) from actuarial ML/AI research PDFs in ifoa_downloads/ into a taxonomy-aligned CSV. Use when asked to extract, process, or catalogue IFOA research papers.
model: sonnet
---

# doc_extract_doer

**Model:** Sonnet 5  
**Role:** Extract metadata from actuarial ML research papers

## Task

Read the 10 PDFs in `/home/nodozi/projects/Intern_GenAI_Examples/ifoa_downloads/` and extract structured metadata following the specification in `ifoa_downloads/prompt.txt`.

Output a timestamped CSV file to `$LOCAL_DIR/IFOA_AI_Papers_<timestamp>.csv` (project root) with the following columns. Timestamp must be **local London time** (Europe/London — auto BST/GMT), format `YYYYMMDD_HHMMSS`, e.g. via `TZ=Europe/London date +%Y%m%d_%H%M%S` — never UTC/system-default:

```
S/N | Topic | Sub-topic | URL | Description | Comments | Date of publication (dd/mm/yyyy) | Authors | Area of practice | Dataset (real/simulated; granularity) | Dataset modality | Code available? (language; link if any) | ML/AI technique (granular label) | Learning paradigm & task (supervised/unsupervised/etc; regression/classification)
```

## Taxonomy

Use the taxonomy found in `practical-applications-of-ai-for-investment-actuaries-working-party-terms-of-reference.pdf`:

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

CSV file with exactly 10 data rows (one per PDF), plus header row. Each field must be:
- Factual and sourced from the PDF text
- Marked as "N/A" if not found in the paper
- Flagged with "Inference:" if inferred rather than stated

## Next step

After extraction completes, hand off to `doc_reviewer` for quality review.
