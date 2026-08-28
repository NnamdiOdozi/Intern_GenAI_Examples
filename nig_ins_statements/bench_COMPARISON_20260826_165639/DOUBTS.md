# Benchmark run — DOUBTS / autonomous decisions log

Run ID: `20260826_165639`
Task: benchmark 3 Doubleword models on the same scanned PDF (`2023 sterling FCR FINAL.pdf`, 52 pages,
colour, 300 DPI scan, no text layer) through the `dw_async_scanned_tables` 3-round pipeline.
User was away during execution and could not answer questions, so the calls below were made autonomously.

Models under test (exact Doubleword IDs, confirmed via live `/v1/models` list):
- `Qwen/Qwen3-VL-235B-A22B-Instruct-FP8`  (tag: 235b) — VL, the skill default
- `Qwen/Qwen3.5-35B-A3B-FP8-dottxt`        (tag: qwen35) — the `.txt`/dottxt structured-output variant
- `allenai/olmOCR-2-7B-1025-FP8`           (tag: olmocr2)

---

## D1 — All three models run the FULL pipeline, stages 1–3 (2026-08-26 16:56)
**Decision:** each model runs Rounds 1 (discovery), 2 (extraction), 3 (validation+audit) solo.
**Why:** user chose "All 3 do full 1-3" for a clean apples-to-apples benchmark. The skill default is
already 235B for all rounds (previously 30B did R1); so no per-model stage asymmetry.
**Affects:** three independent output folders `bench_<tag>_<ts>/`.

## D2 — Reuse the prior run's rendered images + scripts (2026-08-26 16:56)
**Decision:** symlink `images_r1` (150 DPI discovery) and `images_r2` (200 DPI q88 extraction) from the
prior single-model run `output_dw_batch_20260826_110304/`; copy its build/validate/workbook scripts,
patching only the MODEL constant per run dir.
**Why:** identical inputs to every model = fair benchmark; no wasteful re-render; the scripts are the
canonical pipeline implementation.
**Affects:** all three runs consume byte-identical page images. Image provenance (sha256) preserved in
each `round1/image_manifest.json`.

## D3 — Single-page Round 1 (not two-page windows) (2026-08-26 16:56)
**Decision:** kept the prior scripts' one-request-per-page R1 (no N/N+1 window).
**Why:** matches the reusable scripts and keeps the methodology identical across the three models. The
skill now recommends two-page windows for continuation detection; NOT using them is a known weakness,
but it is applied EQUALLY to all three, so the comparison stays fair.
**Affects:** all three may over-segment tables whose header sits at a page bottom with the body on the
next page. Flagged, equal across models.

## D4 — Bounded retry ladder, not perfection (2026-08-26 17:09)
**Decision:** cap retries (≈1–2 exception batches per round). Where a model still can't produce a
valid item, accept best-effort and flag it rather than retrying indefinitely.
**Why:** this is a comparative benchmark, and chasing 52/52 on a fragile model would triple orchestration
cost for little benchmark value. The skill explicitly allows accepting best-effort with a Review-Log flag.
**Affects:** per-model completeness (e.g. pages/tables recovered) is itself a benchmark metric, not a
defect to be hidden. Retry counts are recorded per model.

## D5 — olmOCR2 tested via a 1-page BATCH probe first (2026-08-26 16:57)
**Decision:** real-time access to `allenai/olmOCR-2-7B-1025-FP8` is blocked by a routing rule
(`PermissionDeniedError` on a synchronous call). Submitted a 1-page batch to test whether the BATCH
route is permitted before committing 52 pages.
**Why:** fast-fail; don't waste a 52-page batch if the model is fully blocked. Also olmOCR is an OCR
model that may not honour strict JSON schemas — if so, that failure is recorded as a benchmark result
(per user: "if it doesn't follow this, we'll just do the best we can with the model").
**Affects:** olmOCR2 may be dropped from the benchmark and documented as access-blocked / schema-incapable.

## D6 — Identical validators across models (2026-08-26 17:10)
**Decision:** used the prior run's `validate_round{1,2,3}.py` unchanged for all three models. Note
`validate_round2.py` HARD-REJECTS ragged rows (the skill's newer guidance routes ragged tables to
Round 3 instead). Kept as-is.
**Why:** a single fixed validator applied to all three is what makes the benchmark controlled. Changing
validation per model would confound model quality with validation policy.
**Affects:** ragged-row tables count as R2 rejects for every model equally.

## D7 — olmOCR2 dropped: access-blocked (2026-08-26 17:15)
**Decision:** `allenai/olmOCR-2-7B-1025-FP8` removed from the benchmark.
**Why:** real-time route returns HTTP 403 "blocked by a routing rule" (confirmed by user console
screenshot); the 1-page batch test never processed (stuck 0/1 ~18 min, then cancelled). Not accessible
on this account.
**Affects:** benchmark reduced to Qwen 235B vs Qwen3.5-35B (+ DeepSeek-OCR-2 pending, see D8).

## D8 — Third model swapped to DeepSeek-OCR-2 (2026-08-26 17:19)
**Decision:** user asked to try `deepseek-ai/DeepSeek-OCR-2` as the 3rd model instead of olmOCR2.
Real-time route is ALSO 403-blocked; submitted a 1-page BATCH access test to see if the batch route
is permitted (batch is a separate route). If it hangs/fails like olmOCR2, DeepSeek-OCR-2 is documented
as batch-blocked and the benchmark stands at 235B vs Qwen3.5-35B.
**Result (17:26):** batch route ALSO blocked — 1-page test stuck 0/1 for 5+ min (a comparable 1-page
Qwen completes in seconds) on top of the real-time 403; cancelled. **Both OCR models (olmOCR2,
DeepSeek-OCR-2) are inaccessible on this account.** Final benchmark: **235B vs Qwen3.5-35B**.
Both OCR runs would need the account admin to grant model access before they can be benchmarked.

## D9 — Accepted single-page R1 discovery gaps (2026-08-26 17:18)
**Decision:** after 2–3 firmer/terser exception retries, one page each remained truncated and was
ACCEPTED as a gap rather than retried further: **235B page 9**, **Qwen3.5-35B page 17**.
**Why:** both are runaway/degeneration pages (235B's page 9 produced a 317 KB single-page response and
still hit the token cap at max_tokens 16000/6000/5000). Bounded-retry rule (D4). Symmetric — one page
lost per model.
**Affects:** any table appearing only on those pages is absent from that model's extraction. Recorded
in each Page Coverage sheet.

## D10 — R1 discovery outcome (headline benchmark signal) (2026-08-26 17:18)
Both models reached 51/52 pages accepted, but discovery SENSITIVITY differs sharply:
- **235B:** 53 logical tables across 33 pages-with-tables (18 no_table).
- **Qwen3.5-35B:** 38 logical tables across 21 pages-with-tables (30 no_table).
Qwen3.5-35B also needed 3 exception batches to reach 51/52 (persistent `-dottxt` whitespace-loop
truncation), vs 235B's 2. This is a primary benchmark finding, not a bug.

## D11 — ROOT CAUSE of Qwen3.5-35B truncation: reasoning tokens crowd out the answer (2026-08-26 17:45)
**Finding (user's hypothesis, confirmed in raw data):** `Qwen3.5-35B-A3B-FP8-dottxt` is a REASONING model
(`reasoning:true`). Its hidden `reasoning_content` counts against `max_tokens` via
`completion_tokens_details.reasoning_tokens`. On hard tables it reasons for 10k–16k tokens and leaves
little/nothing for the JSON answer → `finish_reason=length`, empty/tiny content. Evidence (R2):
- T23/T20/T08: completion=16000, **reasoning=16000, content=0 chars** (100% of budget on reasoning).
- T12: completion=11680, reasoning=11470, content=489 chars. T21: 6251/6050/492.
- Successful tables (T24/T32/T28) simply reasoned briefly (~1.2–1.8k) so the answer fit.
So the failures were NOT a capability ceiling — they were an uncapped-reasoning budget blowout.
**Fix (verified):** pass `reasoning_effort:"none"` in the request body → reasoning_tokens=0, clean JSON,
no truncation (the API explicitly directs: "use 'reasoning_effort'"). `minimal` still spent ~1k reasoning
and would still risk blowups on hard tables; `none` is the safe setting for schema extraction.
**Action:** added a third benchmark variant `bench_qwen35nr_*` = Qwen3.5-35B with `reasoning_effort:"none"`
injected into every request body (R1–R3), same images/scripts, to measure the model's true ability.
**Implication for the skills:** the `dw_async_scanned_tables` skill should set `reasoning_effort:"none"`
(or a small cap) for reasoning models doing strict-schema extraction, and the model-list doc should mark
which models actually reason.
**Correction (verified 2026-08-26):** `Qwen3-VL-235B-A22B-Instruct-FP8` is NOT a reasoning model in
practice — it emitted **reasoning_tokens=0 on all 159 requests** (R1 52 / R2 53 / R3 54). The model-list
JSON's `reasoning:true` for it is WRONG (another unreliable metadata field, like `input`/`authReady`).
That zero-reasoning behaviour is exactly why 235B never truncated. Both the 235B run and the original
Qwen3.5 run had `reasoning_effort` unset, so the comparison was fair; the difference is that the 235B
Instruct model does not reason, while the Qwen3.5 `-dottxt` model reasons heavily by default.

## D14 — FIX FOUND & PROVEN: frequency_penalty breaks the tab-loop (2026-08-26 18:06)
**Controlled realtime probe on the looping page 10 (exact batch conditions: full system prompt,
max_tokens=16000):**
- reasoning=none, no penalty → LOOPS (16000 tokens, 15951 tabs, INVALID).
- reasoning=none + **frequency_penalty=0.5** → finish=stop, 86 tokens, 0 tabs, VALID JSON. **Fixed.**
So the real remedy is a repetition penalty (penalising the runaway tab token), NOT the reasoning dial.
**Fair variant `bench_qwen35fp_*` = Qwen3.5-35B + reasoning_effort=none + frequency_penalty=0.5.**
R1 result: **52/52 first pass, 0 rejects, GATE PASS, 57 tables / 34 table-pages** (MORE than 235B's
53/33), all finish=stop, reasoning_tokens=0, zero loops, zero exception batches. The model was never
incapable — it was purely crippled by the degeneration loop.
**Skill recommendation:** for `-dottxt` / repetition-prone models doing strict-schema extraction at
temperature=0, set `frequency_penalty` ~0.3-0.5 (optionally `reasoning_effort=none` to avoid the reasoning
budget tax). Add this to `dw_async_scanned_tables` guidance.

## D13 — Why the OCR models never ran: ACCOUNT ACCESS restriction (corrected) + markdown not JSON
**CORRECTION (2026-08-26 18:58, after user pointed out "async = Doubleword's 1h batch service"):**
My earlier "24h-batch-only" reading was WRONG. Per the docs the OCR models support **Async** (the 1h
service, $0.08/1M) **and Batch(24h)** ($0.05/1M) — no real-time. So they DO advertise a 1h path.
**Real cause of failure = an account access/routing restriction, not the SLA:**
- Real-time → HTTP 403 "real-time access blocked by a routing rule. Please contact your administrator to
  request access." (explicit access block).
- My 1h (async-equivalent) batch via `client.batches.create(completion_window="1h")` → stuck
  `in_progress 0/1` for >1.5h, never serviced and never expired (the routing rule blocks the batch path
  too, silently — no error). So both paths are gated by the same account routing rule.
- **To benchmark these models, the Doubleword account admin must grant access** to
  `allenai/olmOCR-2-7B-1025-FP8` and `deepseek-ai/DeepSeek-OCR-2`. The docs do not document how "Async" is
  invoked (no endpoint/example), so the exact call may also differ from the `/v1/batches` path — but the
  403 shows access is the blocker regardless.
- **Neither supports `response_format`/JSON schema.** They are OCR→markdown models with fixed prompts:
  DeepSeek `"Free OCR."` or `"<|grounding|>Convert the document to markdown."`; olmOCR a system prompt
  returning markdown + front-matter (tables→HTML, equations→LaTeX), image longest side ~1288px.
- Pricing: DeepSeek async $0.08 / batch $0.05 per 1M; olmOCR async $0.15 / batch $0.10 per 1M.
**Consequence:** these OCR models cannot slot into the existing 3-round strict-JSON pipeline on TWO
independent grounds (SLA 24h; markdown not JSON). To benchmark them at all needs a separate design:
24h batch + native OCR prompt + markdown/HTML table parsing. Left as a user decision (would break the
1h-only rule and needs a different downstream). The 1h OCR test batches were left to expire.

## D12 — REFUTED: `reasoning_effort:"none"` is NOT the fix; the real fault is a tab-loop (2026-08-26 17:56)
**The NR variant (reasoning off) performed WORSE, not better.** R1 with `reasoning_effort:"none"`:
accepted 8/52, **44/52 truncated** (`length`), reasoning_tokens=0 confirmed. vs reasoning-ON R1 first
pass: 38/52 (14 truncated). Inspecting a truncated NR response: the model writes valid JSON up to
`"page_seen":` then emits ~16,000 tokens of **literal TAB characters** (a 40-tab window repeats 99× in
the tail) until the cap — a classic degeneration/repetition loop.
**Refined root cause:** the `-dottxt` model is prone to a whitespace/tab repetition loop at temperature=0.
Reasoning tokens were merely ONE place the loop expressed itself; with reasoning off the loop hits the
answer channel directly and is worse. So the earlier "reasoning crowds out the answer" story is only half
right — the deeper fault is the repetition loop, and disabling reasoning removes a stabilising buffer.
**NR pipeline abandoned at R1** (8/52 is not worth continuing / more batches).
**Untested remedies that would actually target the loop** (would need user go-ahead — batch economy):
`frequency_penalty`/`presence_penalty` > 0 to penalise the repeated tab token, and/or a small
`temperature` (0.1–0.3) to break greedy repetition. These, not reasoning_effort, are the levers that fit
the diagnosis.
**Benchmark bottom line unchanged:** `Qwen3-VL-235B-Instruct` is the clear winner (non-reasoning, no
loops, 52 tables delivered). `Qwen3.5-35B-A3B-FP8-dottxt` is unreliable for this task under default
decoding regardless of reasoning setting.

