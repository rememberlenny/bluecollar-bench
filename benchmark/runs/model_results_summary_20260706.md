# Model Results Summary - 2026-07-06

Scope: collected benchmark runs under `benchmark/runs/` after the naturalized-catalog reruns. The registry currently contains 13 collected runs. The static viewer snapshot contains the 6 naturalized-catalog runs and 7,622 scored result entries; superseded and stale coded-catalog runs are excluded because their task ids no longer match the current catalog.

## Current Collected Runs

| run | catalog | scope | scored | mean reward | saturated >=0.95 | floored <=0.05 | dangerous false pass | alarmist false fail |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Sonnet 5 (`sonnet5_20260706_064841`) | coded | full | 1,299 | 0.779 | 189 | 18 | 3 | 17 |
| Gemini 3.5 Flash (`gemini35_flash_natural_20260706`) | naturalized | full | 1,299 | 0.747 | 96 | 28 | 2 | 26 |
| GPT-5.5 full merged (`gpt55_full_20260706_c48_openai_merged`) | coded | full | 1,299 | 0.741 | 85 | 12 | 8 | 4 |
| Gemini 3.5 Flash (`gemini35_flash_full_20260706_185933`) | coded | full | 1,299 | 0.727 | 69 | 25 | 5 | 20 |
| GLM 5.2 (`glm52_natural_20260706`) | naturalized | full | 1,299 | 0.676 | 117 | 176 | 46 | 47 |
| GLM 5.2 (`openrouter_glm52_2026-07-06`) | coded | full | 1,299 | 0.656 | 28 | 164 | 36 | 34 |
| DeepSeek v4 Pro (`deepseek_v4_pro_text_natural_20260706`) | naturalized | text | 1,171 | 0.681 | 26 | 91 | 85 | 89 |
| DeepSeek v4 Pro (`deepseek_v4_pro_text_20260706_182042`) | coded | text | 1,171 | 0.669 | 11 | 64 | 63 | 64 |
| Kimi K2.7 Code (`kimi_k27_code_natural_20260706`) | naturalized | text+image | 1,255 | 0.550 | 101 | 331 | 265 | 266 |

Older GPT-5.5 partial runs are still retained in the registry but excluded from the static viewer as superseded:

- `gpt55_full_20260705_5b2c706`: 1,049 scored, mean 0.765, pre-merge full-run subset.
- `gpt55_missing_text_rebalance_20260706_c48_openai_delta`: 250 scored, mean 0.640, direct-OpenAI text-rebalance delta.
- `gpt55_full_20260706_c48_openai_merged`: merged 1,299-task GPT-5.5 result used for the current coded-catalog comparison.

## Main Callouts

- Sonnet 5 remains the strongest full-suite run on the coded catalog at 0.779, with low floor count and only 3 dangerous false-pass gate hits.
- Naturalized Gemini 3.5 Flash is now the strongest fully comparable naturalized run at 0.747. It improves over the coded Gemini run by about +0.020 and has only 2 dangerous false-pass hits.
- GPT-5.5 full merged is still a strong coded-catalog baseline at 0.741, but it has not yet been rerun on the naturalized catalog in the current registry.
- Naturalized GLM 5.2 improves over coded GLM by about +0.020 overall and reaches 0.750 on text, but image/audio/CPM remain zero through the OpenRouter route.
- Naturalized DeepSeek v4 Pro text improves modestly over coded DeepSeek text, 0.669 to 0.681, but its safety-gate profile worsens: 85 dangerous false passes and 89 alarmist false fails.
- Kimi K2.7 Code is the latest collected run and the weakest new run at 0.550 over 1,255 scored tasks. It has high floor count and high directional-gate failure counts, especially on resource planning and sequencing.

## Naturalized Run Modality Notes

| model | text | image | audio |
|---|---:|---:|---:|
| Gemini 3.5 Flash naturalized | 0.749 | 0.854 | 0.489 |
| GLM 5.2 naturalized | 0.750 | 0.000 | 0.000 |
| DeepSeek v4 Pro naturalized | 0.681 | n/a | n/a |
| Kimi K2.7 Code naturalized | 0.560 | 0.404 | n/a |

The strongest non-text result in the current naturalized set is Gemini image at 0.854. Audio remains weak even for Gemini at 0.489, and GLM still has no usable image/audio path through the collected OpenRouter run.

## Kimi K2.7 Code Failure Shape

Kimi scored 1,255 tasks because the current run covers text plus image but not audio. Its lowest task-type means were:

| task type | n | mean reward |
|---|---:|---:|
| RES | 28 | 0.095 |
| SEQ | 128 | 0.428 |
| TRD | 80 | 0.475 |
| PA | 80 | 0.512 |
| FD | 117 | 0.535 |

Kimi does best on code/spec compliance among its task types at 0.658, but the combination of 331 floored items, 265 dangerous false-pass hits, and 266 alarmist false-fail hits makes it unsuitable as a safety-sensitive baseline without further diagnosis.

## Reading The Rankings

Do not read the table as one perfectly apples-to-apples leaderboard:

- Coded and naturalized catalogs contain the same logical 1,299 items, but the model-visible task ids/titles/scenario wrappers changed.
- Full-suite, text-only, and text+image runs have different modality coverage.
- Naturalized reruns exist for Gemini, GLM, DeepSeek text, and Kimi; Sonnet and GPT-5.5 have not yet been rerun on the naturalized catalog in this registry.
- Aggregate reward hides important gate differences. DeepSeek naturalized improves mean reward while worsening both directional safety gates.

For pre/post naturalization deltas, see `benchmark/runs/naturalization_comparison_20260706.md`.

## Collection Notes

- `benchmark/runs/latest.json` currently points to `kimi_k27_code_natural_20260706`, collected at `2026-07-06T21:30:06+00:00`.
- The latest naturalized catalog hash in the registry is `aa0631b805deaf095fb665a82992fb11102cba6e1c7b38752726b5d3d2f8cb77`.
- The static viewer payload currently includes 9 compatible runs, 2,670 scored result entries, and 2,492 extracted model-answer payloads.
- Failed GPT-5.5 OpenRouter attempts from the missing text-rebalance slice were infrastructure/auth failures and remain excluded from model comparisons.
