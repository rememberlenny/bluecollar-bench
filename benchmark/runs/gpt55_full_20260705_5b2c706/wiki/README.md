# Full Suite Synthesis Wiki

This wiki synthesizes the `gpt55_full_20260705_5b2c706` full-suite run.
It is meant to be read as an interpretation layer above the raw metrics, plots, and per-task artifacts.

## Navigation

- [Task type breakdown](task-types.md)
- [Modality and media breakdown](modality-and-media.md)
- [Discipline and tier breakdown](discipline-and-tier.md)
- [Failure patterns and safety gates](failure-patterns.md)
- [Example index](example-index.md)
- [Plots dashboard](../plots/index.html)
- [Original analysis](../analysis.md)

## At a glance

| metric | value |
|---|---:|
| tasks scored | 1049 |
| mean reward | 0.765 |
| saturated tasks, reward >= 0.95 | 85 (8.1%) |
| floored tasks, reward <= 0.05 | 12 (1.1%) |
| dangerous false pass gate hits | 8 |
| alarmist false fail gate hits | 4 |
| catalog sha256 | `3d917f30ba6d3ee7` |

## Component diagnosis

| component | mean | interpretation |
|---|---:|---|
| schema | 1.000 | Output shape is not the problem. |
| decision | 0.977 | Top-level pass/fail/NMI decisions are usually right. |
| risk | 0.804 | Risk level is weaker than decision, especially in false-pass cases. |
| findings | 0.841 | The model often notices relevant facts. |
| actions | 0.429 | The largest actionable gap is specifying the right next steps. |
| s3 | 0.167 | Final-state/completion evidence is rarely captured completely. |

## Important conclusions

1. **Task format matters more than nominal tier.** Tier means were tightly clustered, while task-type means ranged from 0.709 for ID to 0.841 for TS. Treat the benchmark as a test of task shape, not just task difficulty.
2. **The model is good at the top-level call but weaker at the work plan.** Schema, decision, and safety-gate scores were high; actions and the final-state component were the main drag. In practice it often knows whether to pass/fail but is less consistent about the concrete next steps.
3. **Structured safety recognition is a strength.** HAZ, SEQ, and TS were among the best task types. These formats reward standard jobsite reasoning: identify the hazard, sequence the control, or choose the right tool/material.
4. **Precise identification and diagnosis are the main weakness.** ID was the lowest task type, FD had the most low-score items, and audio FD had the highest low-score rate. The model is much less reliable when it must name the exact component, sound source, or defect from sparse cues.
5. **Image results are strong but not uniformly safe.** Image tasks had the best mean reward and many perfect scores, but critical sling/load and CPM delay tasks also produced zero-score false-pass cases. The visual modality is powerful, not automatically safe.
6. **Electrical detail remains the highest-priority domain weakness.** Electrical had the lowest discipline mean and the largest count of low-score tasks. Terminations/splices and motor-circuit document cases are especially useful regression examples.

## Representative examples

#### Strongest examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-sling-008`](../../../../tasks/v2-media-sling-008/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-sling-006`](../../../../tasks/v2-media-sling-006/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-sling-000`](../../../../tasks/v2-media-sling-000/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-rotor-013`](../../../../tasks/v2-media-rotor-013/task.toml) | 1.000 | ME | image | T4 | needs_more_info/medium | A-201 Brakes |
| [`v2-media-rotor-012`](../../../../tasks/v2-media-rotor-012/task.toml) | 1.000 | ME | image | T4 | pass/low | A-201 Brakes |
| [`v2-media-rotor-010`](../../../../tasks/v2-media-rotor-010/task.toml) | 1.000 | ME | image | T4 | pass/low | A-201 Brakes |

#### Weakest examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t1-e-303-cc-terminations-splices`](../../../../tasks/t1-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T1 | fail/high | E-303 Terminations & splices |
| [`t2-e-303-cc-terminations-splices`](../../../../tasks/t2-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T2 | fail/high | E-303 Terminations & splices |
| [`t3-e-303-cc-terminations-splices`](../../../../tasks/t3-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T3 | fail/high | E-303 Terminations & splices |
| [`v2-audio-hammer-000`](../../../../tasks/v2-audio-hammer-000/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-008`](../../../../tasks/v2-audio-hammer-008/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hum-002`](../../../../tasks/v2-audio-hum-002/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-audio-hum-004`](../../../../tasks/v2-audio-hum-004/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-cpm-delay-001`](../../../../tasks/v2-cpm-delay-001/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
