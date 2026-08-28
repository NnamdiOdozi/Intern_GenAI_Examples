# Doubleword model tuning notes (per-model, per-pipeline-stage)

Hand-curated from real runs. Not auto-generated (unlike `doubleword-models.md`). Update as you learn more.
**Always confirm a model's real behaviour from `usage.completion_tokens_details.reasoning_tokens` and the
Doubleword docs page for that model — the model-list metadata flags (`reasoning`, `input`, `authReady`)
have all proven unreliable.**

---

## `Qwen/Qwen3.5-35B-A3B-FP8-dottxt` — scanned-table extraction pipeline (`dw_async_scanned_tables`)

**Context:** 128000 · **max output:** 16384 · **modality:** text+image (verified) · **reasoning:** YES (heavy).

### The two failure modes (both must be controlled)
1. **Reasoning tax.** Reasoning tokens count against `max_tokens` (shared budget). At default reasoning it
   spends 10k-16k tokens *thinking* on hard tables and truncates the JSON answer. Fix: `reasoning_effort:"none"`.
2. **Tab/whitespace degeneration loop.** At `temperature:0` it can fall into a run of literal TAB characters
   mid-JSON until it hits `max_tokens` (verified: 15,951 tabs in one 16k response). Reasoning masks this by
   absorbing the loop into the (hidden) reasoning channel; turning reasoning off WITHOUT a penalty makes R1
   *worse* (44/52 truncations). Fix: a repetition penalty, `frequency_penalty`.

### Ideal params by stage (temperature=0 throughout; strict `response_format` JSON schema)
| Stage | reasoning_effort | frequency_penalty | max_tokens | Notes / evidence |
|---|---|---|---|---|
| R1 discovery | `none` | **0.5** | 16000 (4000 fine) | **Solved.** Verified: 52/52 first pass, 57 tables, 0 loops, 0 reasoning tokens. Discovery output is terse so a strong penalty is safe and works well. |
| R2 extraction | `none` | 0.25-0.5 all imperfect | 16000 | **NOT reliably solved on this model.** `0.5` → 27/57 ragged rows (penalises legit repeated cells). `0.25` → still 23 ragged AND a new degeneration (a runaway repeating string in the `table_id` field). Only ~26/57 pass the strict validator at best. The model degenerates in whichever field carries repetitive content; penalty tuning just moves the problem. **Recommendation: use `Qwen3-VL-235B-Instruct` for extraction** (53/53 clean), or route ragged tables to R3 re-alignment and accept lower yield. |
| R3 validation/audit | `none` | ~0.25 | 16000 | Same shape as R2 → same caveat. |

**Rule of thumb:** a strong `frequency_penalty` rescues terse/inventory outputs (R1 discovery) but does NOT
make this model reliable for dense numeric transcription (R2/R3) — repetition is legitimate there and the
model degenerates regardless of the penalty value. Always pair with `reasoning_effort:"none"`. **Net: this
model is a good, cheap DISCOVERY model when de-looped, but not a dependable extraction model; prefer 235B
for the extraction/validation rounds.**

**RECOMMENDED PRODUCTION CONFIG (proven on the Sterling FCR benchmark, 2026-08-26): a HYBRID —**
- **R1 discovery:** `Qwen3.5-35B-A3B-FP8-dottxt` with `reasoning_effort:"none"` + `frequency_penalty:0.5`
  (cheap; found 57 tables vs 235B's 53).
- **R2 extraction + R3 validation/audit:** `Qwen3-VL-235B-A22B-Instruct-FP8` at defaults (reliable).
This delivered 55 tables (vs 52 for pure-235B) at lower total token cost. Also harden downstream parsing
against degenerate field values from the 35B (e.g. it once emitted `pdf_page = -1` and a runaway string in
`table_id`) — clamp page numbers to the valid range and reject nonsensical ids.

### R3 validator schema: log only CHANGED cells, not every cell

The Round 3 validation prompt/schema must emit a `corrections` entry only for cells the validator
actually changed. Do NOT ask it to write a per-cell justification for every cell.

Why: on the Sterling FCR benchmark, table T23 (Table 1, 6 columns x 27 rows, about 162 cells) was
lost at R3. The 235B validator wrote a "correct - no change" sentence for every one of the ~162
cells. That no-op commentary alone ran past the 16,000-token output cap. The response was cut off
mid-`corrections` array, so the JSON was invalid and the table was rejected. This was not a
reasoning model and there were 0 reasoning tokens. It was 16,000 completion tokens of validation
prose on a table that would otherwise fit easily.

Fix: restrict `corrections` to changed cells. This roughly quarters the R3 output size on dense
tables and stops large tables truncating at the cap.

### Contrast: `Qwen/Qwen3-VL-235B-A22B-Instruct-FP8`
Does NOT reason in practice (reasoning_tokens=0 on 159 requests despite `reasoning:true` in metadata) and
does NOT loop — needs no special params. Ran the whole pipeline cleanly at defaults (temp 0, no penalty).

### OCR models (`allenai/olmOCR-2-7B-1025-FP8`, `deepseek-ai/DeepSeek-OCR-2`)
Per their Doubleword docs pages they support **Async (the 1h service) + Batch(24h)**, no real-time. But on
THIS account they are **access-restricted by a routing rule**: real-time returns HTTP 403 ("contact your
administrator to request access") and a 1h batch sits `in_progress 0/1` indefinitely (routing rule blocks
the batch path silently). **Fix = have the Doubleword admin grant account access to the model id.** Even
once granted they emit **markdown/HTML, not schema-JSON** (no `response_format`) — native prompts:
DeepSeek `"<|grounding|>Convert the document to markdown."`; olmOCR a markdown+front-matter system prompt,
image longest side ~1288px. They cannot slot into the strict-JSON pipeline; benchmark them separately.
