# Doubleword model benchmark — scanned-table extraction

**Task:** benchmark Doubleword LLMs on the `dw_async_scanned_tables` pipeline (3 batch rounds:
discovery → extraction → validation+audit) against one hard document.
**Document:** `2023 sterling FCR FINAL.pdf` — 52 pages, colour, 300 DPI **scan with no text layer**
(the largest/hardest file in `nig_ins_statements/`; 71 MB vs ~2 MB for the digital-native reports).
**Run ID:** `20260826_165639` · **SLA:** 1h · **temperature:** 0 · strict JSON `response_format` schemas.
**Method note:** all runs consumed byte-identical page images (150 DPI discovery / 200 DPI extraction,
symlinked from the prior single-model run) so differences are the model/params, not the inputs.

---

## Headline

| Model / config | R1 pages | R1 tables | R2 extracted | R3 validated | Delivered | Reasoning tokens |
|---|---|---|---|---|---|---|
| **HYBRID: 35B-fp discovery → 235B extract/validate** | 52/52 | **57** | **56/57** | **55/56** | **55** (60-sheet workbook) | 0 |
| Qwen3-VL-235B-Instruct (all rounds) | 51/52 | 53 | 53/53 | 52/53 | 52 (57-sheet workbook) | 0 |
| Qwen3.5-35B-dottxt — default | 51/52 | 38 | 32/38 | 23/32 | 23 (28-sheet workbook) | **911,492** |
| Qwen3.5-35B-dottxt — `reasoning=none` | 8/52 | 10 | — | — | abandoned @R1 | 0 |
| Qwen3.5-35B-dottxt — `reasoning=none + frequency_penalty` (fp) | **52/52** | **57** | 26/57 | 23/26 | 23 (28-sheet workbook) | 0 |

*Columns read as a funnel: **R1 tables** discovered → **R2 extracted** (strict-JSON tables accepted, `x/discovered`) → **R3 validated** (survived independent re-check, `x/extracted`) → **Delivered** (worksheets in the final workbook). The next block explains every drop.*
| olmOCR-2-7B / DeepSeek-OCR-2 | — | — | — | — | **access-blocked** | — |
| **Codex agentic (ChatGPT 5.6, high reasoning)** — *different method, not this batch pipeline* | n/a | n/a | n/a | n/a | **47** (9 thematic sheets) | n/a |

> **The Codex row is not apples-to-apples.** The five rows above are one Doubleword model
> (or model-pair) driving the *same 3-round batch pipeline* (discovery → extraction →
> validation), so their columns line up. Codex/ChatGPT-5.6 is a **different architecture**:
> an *iterative agentic* run that reads rendered page images, reasons visually, and writes the
> workbook directly — there are no R1/R2/R3 rounds, so those columns are n/a. Its **47** is also
> a *consolidated* count (one logical table per financial statement, grouped into 8 thematic
> sheets + an Index), whereas the pipeline's 52–55 deliberately over-segments (header stubs and
> per-year versions counted as separate tables). So "47 < 55" does **not** mean Codex captured
> less — on page coverage it did **better** (see Finding 5). Count across the two methods with care.

**Winner: the HYBRID** — Qwen3.5-35B (reasoning=none + frequency_penalty=0.5) for the cheap, broad R1
discovery, then Qwen3-VL-235B-Instruct for R2 extraction + R3 validation. It delivered **55 tables vs
pure-235B's 52**, because it inherited the 35B's richer 57-table discovery, and it did so **more cheaply**:
its R2/R3 cost 738k prompt / 221k completion tokens while *replacing 235B's expensive 235B-run discovery
round* (which alone spent ~160k prompt / 198k completion) with the near-free 35B discovery. Both quality
(more tables, 43 independently corrected) and cost favour the hybrid. Pure-235B is the best *single* model
and the simplest to operate. **But the real payoff of this exercise is understanding *why* each config
behaved as it did — see the findings.**

---

## Where the tables are lost between rounds (plain English)

**First, two bits of terminology used below:**
- **Looping / degeneration.** At `temperature:0` a model can fall into a repetition loop —
  emitting the same token or character run over and over (e.g. thousands of literal TAB characters,
  or one string repeated) until it exhausts the output budget. The response is then a wall of
  garbage instead of a table.
- **De-looping.** The mitigations that stop that: a **`frequency_penalty`** (down-weights tokens
  the model has already emitted, so it can't spam the same one) paired with **`reasoning_effort:"none"`**
  on the 35B. "35B-fp" in the table above means the 35B run *with* this de-looping applied.

Every row loses some tables from discovery to delivery. There are only **two loss mechanisms**,
and knowing which one bit which model is the whole story:

- **(A) Response truncation at the 16,000-token output cap** (`finish_reason: length`). The
  response is cut off mid-JSON and rejected as incomplete. This happens for **two different
  reasons**: *(A1)* the reasoning-heavy **35B-default** spends the budget *thinking* before it
  finishes the answer (its 911k reasoning tokens); *(A2)* even a non-reasoning model can overflow
  if the **output itself is verbose** — the R3 validator writes a justification sentence *per cell*,
  so on a large table that no-op commentary alone exceeds 16k tokens (this, not reasoning, is what
  cost the hybrid its one R3 table — see below).
- **(B) Ragged / degenerate rows.** A returned table has rows whose cell-count ≠ the header width
  (a dropped cell, or the 35B's decoding pathology corrupting dense repeated figures). The reused
  `validate_round2.py` *hard-rejects* these rather than routing them to R3 re-alignment (a
  documented harness caveat), so a nearly-complete table can still be dropped at R2.

Per row:

- **Hybrid 57 → 56 → 55.** R2 lost **1** — `T57`, the **page-48 Agriculture loss-ratio table**,
  came back ragged (rows of 1–2 cells vs the header) on both the first pass *and* the retry, so it
  was rejected (mechanism B). *Irony worth noting: this is the exact table the Codex run missed —
  the 35B discovery **found** it, but extraction couldn't transcribe it cleanly.* R3 lost **1
  more** — `T23` is Table 1, the five-year version on page 23 (6 columns × 27 rows ≈ **162 cells**).
  Its validation response hit the cap by mechanism **A2**, *not* because the page holds 16k tokens
  of data: the validator emitted a "correct — no change" justification sentence for every one of
  those ~162 cells, and that per-cell prose overran the 16,000-token cap (`finish_reason=length`,
  **0 reasoning tokens** — the 235B does not reason, so it really was 16k *completion* tokens of
  validation commentary). It was cut off mid-`corrections` array → invalid JSON → rejected. The
  provisional R2 table is intact in the raw files; only the R3-validated copy was lost. **This is a
  wasteful-schema problem, not a real content limit** — the cheap fix is to make the validator emit
  a `corrections` entry only for cells it actually *changed*, not a no-op reason for every cell.
- **235B 53 → 53 → 52.** No R2 loss — every discovered table extracted cleanly. R3 lost exactly
  **1** — `T21`'s validation response truncated (mechanism A). One drop in the whole run; this is
  why 235B is the boringly-reliable baseline.
- **35B default 38 → 32 → 23.** Discovery was already low (38) because reasoning/loops swallowed
  pages. R2 lost **6** — 3 the model self-reported incomplete, 3 truncated (mechanism A) — all 6
  failing the retry too. R3 lost **9 more**, *every one a truncated validator response* (mechanism
  A again): the reasoning tax compounds at each round.
- **35B-fp 57 → 26 → 23.** De-looping fixed *discovery* (57, tied with the hybrid) but wrecked
  *extraction*: R2 lost **31** — 26 ragged/degenerate (mechanism B — `frequency_penalty` corrupts
  legitimately repeated cells) plus 5 self-reported incomplete. R3 lost **3 more** to truncation.
  This row is the proof that the 35B is a *discoverer, not an extractor*.

---

## Finding 1 — 235B is not a reasoning model (metadata is wrong)

The model-list metadata flags `Qwen3-VL-235B-…-Instruct` as `reasoning:true`, but it emitted
**0 reasoning tokens on all 159 requests** (R1 52 / R2 53 / R3 54). That is exactly why it never
truncated: nothing competed with the answer for the `max_tokens` budget. (The metadata `input`,
`authReady` and `reasoning` fields have all proven unreliable — verify from actual usage, not the flag.)

## Finding 2 — Qwen3.5-35B's failures were decoding pathologies, not capability

The `-dottxt` model discovered only 38 tables and delivered 23 at defaults — but not because it is weak.
Two compounding pathologies:

**(a) Reasoning tax.** `Qwen3.5-35B-dottxt` IS a reasoning model, and reasoning tokens count against
`max_tokens` (one shared budget). On hard tables it "thought" for 10k-16k tokens and left nothing for the
JSON — e.g. R2 tables T23/T20/T08 spent **16000/16000 completion tokens entirely on reasoning, 0 chars of
answer**. Across the default run it burned **911k reasoning tokens (72% of its 1.27M completion tokens)**.
The tables that succeeded simply happened to reason briefly (~1-2k).

**(b) Tab/whitespace degeneration loop.** At `temperature:0` the model falls into a run of literal TAB
characters mid-JSON until it hits the cap (verified: one response was 16,061 chars of which **15,951 were
tabs**). Reasoning *masks* this by absorbing the loop into the hidden reasoning channel.

**Turning reasoning off is NOT the fix** — it removes the buffer and the loop hits the answer directly:
`reasoning_effort:"none"` made R1 **worse** (8/52 accepted, 44 truncated). The user's "reasoning crowds out
the answer" hypothesis was half right (reasoning does consume the budget) but the deeper fault is the
repetition loop.

## Finding 3 — the real remedy is a repetition penalty (proven), but only for discovery

A controlled real-time probe on a looping page (identical batch conditions, one variable changed):

| Config | Result |
|---|---|
| `reasoning=none`, no penalty | loops → 16000 tokens, 15,951 tabs, INVALID |
| `reasoning=none` + **`frequency_penalty=0.5`** | finish=stop, 86 tokens, 0 tabs, **VALID** |

With `reasoning_effort:"none" + frequency_penalty:0.5`, Qwen3.5-35B's **R1 hit 52/52 on the first pass
with 57 tables / 34 table-pages — more than 235B's 53/33**, zero loops, zero exception batches. So for
*discovery* the model is excellent once de-looped, and cheaper than 235B.

**Extraction is a different story.** `frequency_penalty=0.5` is too aggressive for dense tables — it
penalises legitimately repeated cell values (0, –, recurring figures) and produced **27/57 ragged rows**.
Lowering to `0.25` only partly helped (23 ragged) and triggered a *new* degeneration — a runaway repeating
string in the `table_id` field. **The model degenerates in whichever field carries repetitive content;
penalty tuning moves the problem rather than solving it.** Best achieved: ~26/57 extracted.

## Finding 4 — the OCR models are access-restricted on this account

Per their Doubleword docs pages, `allenai/olmOCR-2-7B-1025-FP8` and `deepseek-ai/DeepSeek-OCR-2` support
**Async** (Doubleword's 1h batch service, $0.08/1M) **and Batch(24h)** ($0.05/1M) — no real-time. So they
*do* advertise a 1h path; the blocker is **account access, not the SLA**:
- Real-time → HTTP 403 "blocked by a routing rule. Please contact your administrator to request access."
- 1h batch (`client.batches.create`, `completion_window=1h`) → stuck `in_progress 0/1` for >1.5h, never
  serviced, never expired — the routing rule gates the batch path too, silently.
- **Action to include them: have the Doubleword account admin grant access** to both model ids.

Separately, even once granted they emit **markdown/HTML, not schema-JSON** (no `response_format`; native
prompts like `"<|grounding|>Convert the document to markdown."`), so they need a different downstream
(markdown-table parsing) and cannot drive this strict-JSON pipeline as-is.

## Finding 5 — the Codex agentic run (a different method, and a useful contrast)

`nig_ins_statements/codex/` holds an extraction of the **same PDF** by **ChatGPT 5.6 (high
reasoning) driven by the Codex CLI** — an *iterative agentic* process, not the batch pipeline.
It produced `2023_sterling_FCR_tables_chatgpt_5.6_sol_high.xlsx` (**9 sheets: 8 thematic groups +
an Index cataloguing 47 logical tables/blocks**, pages 3–46) plus a hand-written **Review Log**.

**Where it beat the batch pipeline:**
- **Coverage of pages 27–29.** It captured the five table groups there — asset/liability
  NPV+duration+convexity, SoFP liabilities, SoFP assets, the investment-yield table, and asset
  quality — which the *old naïve* Doubleword batch (2 giant requests × 8k tokens, in
  `output_dw_batch/`) truncated and dropped entirely. (My benchmark pipeline, one request/page,
  also covers this region; the Review Log predates it and critiques the naïve batch.)
- **Cross-table reconciliation and anomaly handling.** It *found and preserved without
  correcting* the –61,042,762 post-tax profit, the 1,120,394-vs-1,810,266 reinsurance-asset
  conflict, the Table 15/17 double-label, and the treaty capacity/line-count contradictions —
  each logged with page cite, a confidence/materiality classification, and a recommended human
  check. This whole-document reconciliation is something no single batch round does.
- **Source-fidelity discipline:** printed anomalies retained verbatim; blanks stored as blanks.

**Where it fell short (from its own Review Log):**
- **Missed the Agriculture loss-ratio table on PDF page 48** — a genuine completeness gap.
- **Over-consolidated Table 1:** kept only the p23 five-year version and dropped the p3
  three-year version, which carries materially different 2023 liability figures — both should
  have been retained and compared.
- **Collapsed cell states:** blank / dash / explicit-zero / illegible were all flattened to
  blank cells, losing the distinction the pipeline's Round-2 schema keeps.
- **Slower and costlier:** iterative visual review does not scale like a batch submission.

**Net:** Codex is the strongest at *reconciliation and judgement* and matched-or-beat the
pipeline on *coverage of the hard middle pages*, but it consolidates by hand (so it can silently
bury a conflicting version) and it too missed a table. Its own Review Log lands on the same
conclusion this benchmark did: **batch-first for cheap broad discovery/extraction, then
exception-led agentic verification** — i.e. a hybrid, just drawn at the method level rather than
the model level.

---

## Recommendations

1. **Best overall → the HYBRID** (proven, not hypothetical): `Qwen3.5-35B-dottxt`
   `[reasoning_effort:"none", frequency_penalty:0.5]` for R1 discovery, then
   `Qwen3-VL-235B-A22B-Instruct-FP8` (defaults) for R2 extraction + R3 validation. Delivered 55 tables
   (vs 52) at lower token cost. Pairs the cheapest strong discoverer with the only reliable extractor.
2. **Simplest single model → `Qwen3-VL-235B-Instruct`.** Ran all rounds reliably (53/53 → 52 delivered),
   no pathologies, no special params. Choose this when operational simplicity beats squeezing the last
   few tables/cost out.
3. **Do NOT use `Qwen3.5-35B-dottxt` for extraction.** Even de-looped it manages ~23 delivered — it
   degenerates on dense numeric tables regardless of `frequency_penalty`. It is a *discovery* model.
4. **OCR models** (olmOCR-2, DeepSeek-OCR-2): **access-blocked on this account** (routing rule; admin must
   grant access). Even once granted they output markdown, not schema-JSON, so they need a separate
   markdown-parsing design — they are page-digitisers, not structured-table extractors.

## Per-variant token usage (all rounds)

| Variant | prompt tok | completion tok | reasoning tok |
|---|---|---|---|
| 235B | 886,153 | 429,287 | 0 |
| 35B default | 728,650 | 1,271,925 | 911,492 |
| 35B reason=none (R1 only) | 131,747 | 706,364 | 0 |

## Artifacts

- Workbooks: `bench_235b_*/output/*.xlsx` (57 sheets, 52 tables) · `bench_qwen35_*/output/*.xlsx`
  (28 sheets, 23 tables).
- Per-run provenance: `bench_<variant>_*/round{1,2,3}/*_raw.jsonl` (raw API output), `page_manifest`,
  `table_inventory`, `extraction_plan`, validated tables, document audit, batch IDs, image hashes.
- `DOUBTS.md` (this folder) — full decision/《why》log, D1-D14.
- Skill updates from this exercise: `dw_batch/doubleword-models.md` (dated model list + caveats),
  `dw_batch/model-tuning-notes.md` (per-stage params), and pre-start instructions added to both
  `dw_batch/SKILL.md` and `dw_async_scanned_tables/SKILL.md`.

## Caveats / honesty notes

- The reused `validate_round2.py` **hard-rejects ragged rows** (the skill's newer guidance would route them
  to R3 re-alignment). Applied identically to every variant, so the comparison is fair, but it understates
  raw extraction where a table is nearly complete.
- Complete audited workbooks exist for four configs: **hybrid (60 sheets/55 tables)**, 235B (57/52),
  35B-default (28/23), 35B-fp (28/23). The `reasoning=none` (no-penalty) run was abandoned at R1 (8/52).
- One page per model (235B p9, default-35B p17) never discovered — runaway pages accepted as gaps.
- The hybrid's token totals above cover its 235B R2/R3 only; its R1 discovery cost sits in the 35B-fp run
  (cheap). Even summing both, the hybrid is cheaper than pure-235B because 35B discovery << 235B discovery.
- The 35B-fp run produced one degenerate field value (a table with `pdf_page = -1`); the R3 builder was
  hardened to drop out-of-range pages. A reminder that this model needs defensive parsing.
