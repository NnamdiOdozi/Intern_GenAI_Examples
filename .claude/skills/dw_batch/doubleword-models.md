# Doubleword models — reference list

**Source:** `~/.pi/agent/doubleword-models.json` (cachedAt `2026-08-20T16:05:20.931Z`)  
**This table generated:** 2026-08-26  
**Base URL:** `https://api.doubleword.ai/v1`  
**Model count:** 31

> Regenerate after Doubleword adds/removes models — this is a point-in-time snapshot, not live.

## Read-me caveats (learned the hard way, 2026-08-26)

- **`contextWindow` = 128000 and `maxTokens` (max output) = 16384 for every model** in the source. For this batch pipeline that means Round-1 discovery `max_tokens` ~4000 and Round-2/3 ~16000 sit inside the cap — but a runaway/whitespace-looping model can still hit 16384 and truncate.

- **The source JSON originally labelled EVERY model `input:text`.** As of 2026-08-26 the three verified vision Qwen models (`Qwen3-VL-235B`, `Qwen3-VL-30B`, `Qwen3.5-35B-A3B-FP8-dottxt`) have been corrected to `text+image` in the source. The **OCR models still read `text` in the source but are image models** (see Modality). Trust the `Modality` column here over the raw `input`.

- **The source JSON's `authReady: true` / `fanout.batch: true` are NOT proof of access.** `allenai/olmOCR-2-7B-1025-FP8` and `deepseek-ai/DeepSeek-OCR-2` return **HTTP 403 "real-time access blocked by a routing rule"**, and their batch jobs sat unprocessed. `ok*` below means "not observed blocked", not "guaranteed". Access is account/routing-specific — confirm with a 1-request probe before committing a big batch.

- **The `-dottxt` variants** (e.g. `Qwen3.5-35B-A3B-FP8-dottxt`) are structured-output builds: good at JSON-schema conformance, but observed to **whitespace-loop and truncate** on some scanned pages, needing firmer/terser prompts and retries.

- **The `reasoning` flag is ALSO unreliable, and reasoning eats your `max_tokens`.** Reasoning tokens count against `max_tokens` (they share one budget with the answer), so a heavy reasoner can spend the whole 16384 on hidden thinking and truncate the JSON. Verified 2026-08-26: `Qwen3-VL-235B-A22B-Instruct-FP8` is flagged `reasoning:true` but emitted **0 reasoning tokens** on 159 requests (it does not reason), whereas `Qwen3.5-35B-A3B-FP8-dottxt` reasoned 10k-16k tokens on hard tables and truncated. **For strict-schema extraction on a reasoning model, pass `reasoning_effort:"none"`** (the supported dial is categorical: none/minimal/low/medium/high/xhigh -- there is no separate reasoning-token cap). Confirm a model's real reasoning behaviour by checking `usage.completion_tokens_details.reasoning_tokens`, not the flag.


## Models

| Model ID | Reasoning | Context | Max out | Modality | Access |
|---|---|---|---|---|---|
| `Qwen/Qwen3-14B-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3-Embedding-8B` | no | 128000 | 16384 | text (embeddings) | ok* |
| `Qwen/Qwen3-VL-235B-A22B-Instruct-FP8` | yes | 128000 | 16384 | text+image (verified) | ok* |
| `Qwen/Qwen3-VL-30B-A3B-Instruct-FP8` | yes | 128000 | 16384 | text+image (verified) | ok* |
| `Qwen/Qwen3.5-35B-A3B-FP8-dottxt` | yes | 128000 | 16384 | text+image (verified) | ok* |
| `Qwen/Qwen3.5-397B-A17B-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3.5-397B-A17B-FP8-dottxt` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3.5-4B` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3.5-9B` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3.5-9B-dottxt` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3.6-35B-A3B-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |
| `Qwen/Qwen3.8-27B-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |
| `allenai/olmOCR-2-7B-1025-FP8` | no | 128000 | 16384 | image OCR (source still says text) | BLOCKED (403) |
| `deepseek-ai/DeepSeek-OCR-2` | no | 128000 | 16384 | image OCR (source still says text) | BLOCKED (403) |
| `deepseek-ai/DeepSeek-V4-Flash` | yes | 128000 | 16384 | text (image untested) | ok* |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | yes | 128000 | 16384 | text (image untested) | ok* |
| `deepseek-ai/DeepSeek-V4-Pro` | yes | 128000 | 16384 | text (image untested) | ok* |
| `google/gemma-4-26B-A4B-it` | yes | 128000 | 16384 | text (image untested) | ok* |
| `google/gemma-4-31B-it` | yes | 128000 | 16384 | text (image untested) | ok* |
| `lightonai/LightOnOCR-2-1B-bbox-soup` | no | 128000 | 16384 | image OCR (source still says text) | ok* |
| `meta-models/Muse-Glimmer-30B` | yes | 128000 | 16384 | text (image untested) | ok* |
| `moonshotai/Kimi-K2.6` | yes | 128000 | 16384 | text (image untested) | ok* |
| `moonshotai/kimi-k3` | yes | 128000 | 16384 | text (image untested) | ok* |
| `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4` | yes | 128000 | 16384 | text (image untested) | ok* |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4` | yes | 128000 | 16384 | text (image untested) | ok* |
| `openai/gpt-oss-120b` | yes | 128000 | 16384 | text (image untested) | ok* |
| `openai/gpt-oss-20b` | yes | 128000 | 16384 | text (image untested) | ok* |
| `tencent/Hy3-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |
| `thinkingmachines/Inkling-NVFP4` | yes | 128000 | 16384 | text (image untested) | ok* |
| `zai-org/GLM-5.1-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |
| `zai-org/GLM-5.2-FP8` | yes | 128000 | 16384 | text (image untested) | ok* |

\* `Access = ok*` means not observed blocked during use; always probe before a large batch.

**Raw source:** `doubleword-models.json` in this folder is a dated COPY of `~/.pi/agent/doubleword-models.json` (kept as a plain file, not a symlink, so it is visible in the repo on GitHub). Both this `.md` and that `.json` are point-in-time snapshots — re-copy the source and regenerate this `.md` if Doubleword's model set changes.

