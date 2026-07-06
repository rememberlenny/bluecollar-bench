# Pre/Post Naturalization Comparison - 2026-07-06

Reruns of Gemini 3.5 Flash, GLM 5.2, and DeepSeek v4 Pro on the naturalized catalog compared against the same models' runs on the pre-naturalization catalog. Tasks are joined across the rename via `benchmark/items/id_map.json`; the full catalog has 1,299 logical items. Kimi K2.7 Code was collected only on the naturalized catalog and is included as a new baseline rather than a pre/post pair.

| Run | Catalog | Collected run |
|---|---|---|
| Gemini 3.5 Flash (old) | coded | `gemini35_flash_full_20260706_185933` |
| Gemini 3.5 Flash (new) | naturalized | `gemini35_flash_natural_20260706` |
| GLM 5.2 (old) | coded | `openrouter_glm52_2026-07-06` |
| GLM 5.2 (new) | naturalized | `glm52_natural_20260706` |
| DeepSeek v4 Pro text (old) | coded | `deepseek_v4_pro_text_20260706_182042` |
| DeepSeek v4 Pro text (new) | naturalized | `deepseek_v4_pro_text_natural_20260706` |
| Kimi K2.7 Code | naturalized only | `kimi_k27_code_natural_20260706` |

Both runs used the same harness parameters as their predecessors
(Gemini: Vertex global, max 8192 tokens; GLM: OpenRouter, temp 0.0,
max 1200 tokens; concurrency 48). GLM fails the 84 image and 44 audio tasks with endpoint 404s in both runs (no multimodal route on OpenRouter), so its text-only behavior should be read separately from its full-suite aggregate. DeepSeek is text-only in both runs.

## Headline

| Component | Gemini old -> new | GLM full old -> new | DeepSeek text old -> new |
|---|---|---|---|
| reward | 0.7272 -> 0.7468 (+0.020) | 0.6557 -> 0.6760 (+0.020) | 0.6693 -> 0.6806 (+0.011) |
| decision | 0.9769 -> 0.9677 (-0.009) | 0.9658 -> 0.9488 (-0.017) | 0.9360 -> 0.9086 (-0.027) |
| risk | 0.8048 -> 0.8064 (+0.002) | 0.8079 -> 0.7822 (-0.026) | 0.7447 -> 0.6990 (-0.046) |
| findings | 0.6286 -> 0.6386 (+0.010) | 0.6376 -> 0.6425 (+0.005) | 0.5585 -> 0.5649 (+0.006) |
| actions | 0.2384 -> 0.2644 (+0.026) | 0.3190 -> 0.3428 (+0.024) | 0.1835 -> 0.1946 (+0.011) |
| s3 (progress/value) | 0.2794 -> 0.5812 (+0.302) | 0.1597 -> 0.8147 (+0.655) | 0.0974 -> 0.6610 (+0.564) |
| dangerous_false_pass tripped | 5 -> 2 | 36 -> 46 | 63 -> 85 |
| alarmist_false_fail tripped | 20 -> 26 | 34 -> 47 | 64 -> 89 |

Kimi K2.7 Code naturalized baseline: 1,255 scored tasks, mean reward 0.5496, 331 floors, 265 dangerous false-pass hits, and 266 alarmist false-fail hits. Its run covers text plus image, not audio.

## Reading

1. **The dominant effect is schema clarity, not content difficulty.**
   Renaming `s3_percent` to `percent_complete` (with a one-line
   explanation in the instruction) moved the s3 component by +0.30
   (Gemini), +0.66 (GLM), and +0.56 (DeepSeek text). Models understood
   the task before; they did not understand the field. The old scores
   understated these models by roughly 1-2 points of aggregate reward
   for a presentation/schema reason.

2. **Decision accuracy was never mainly protected by the coded wrappers.**
   Gemini and GLM decision scores stay high after naturalization, while
   DeepSeek drops from 0.936 to 0.909. The taxonomy shorthand was not
   the main source of decision accuracy for the stronger models; the
   fail-skewed label prior remains a larger validity concern.

3. **De-leaked titles made control items honestly harder.** The eight
   pass-label control items dropped ~0.05 for both models after
   titles like "Compliant subpanel makeup (control)" became neutral
   ("Subpanel makeup inspection"). Directional-gate trips (dangerous
   false passes, alarmist false fails) rose for GLM and DeepSeek. This
   is the intended effect of removing decision hints from titles, and
   it suggests some pre-naturalization gate numbers were flattered.

4. **Mean reward can improve while safety gates worsen.** DeepSeek is
   the clearest example: reward rises from 0.669 to 0.681, but
   dangerous false-pass hits rise from 63 to 85 and alarmist false-fail
   hits rise from 64 to 89. Aggregate score alone is not enough for
   model selection.

5. **Kimi is a weak naturalized baseline.** Kimi's mean reward is 0.550
   over 1,255 tasks, with especially poor RES (0.095) and SEQ (0.428).
   It is useful as a contrast run, not as a leading model.

## Caveats

- One run per model per catalog; deltas under ~0.02 are within
  plausible run-to-run noise for nondeterministic providers.
- Gemini's first naturalized pass hit Vertex 429s on 288 tasks at
  concurrency 48; those tasks were cleanly retried to completion
  before collection (final: 1,299 ok, 0 failed).
- The comparison joins by `legacy_id`; both catalogs contain the same
  1,299 logical items with identical ground truth, so component
  deltas are attributable to presentation, not item substance.
- Sonnet 5 and GPT-5.5 do not yet have naturalized-catalog reruns in
  this registry, so their current leaderboard rows are still coded
  catalog results.
- Kimi has no coded-catalog predecessor in this registry.
