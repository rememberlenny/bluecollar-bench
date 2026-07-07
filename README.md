# Blue-Collar Benchmark

A Harbor benchmark for testing whether AI agents can make practical, safety-aware judgments in trade-work scenarios.

The benchmark covers electrical, plumbing, HVAC-R, rigging, concrete, carpentry, machinery, instrumentation, automotive, fabrication, sitework, and safety work. Items ask the model to inspect written, image, or audio evidence and return a structured answer that can be graded deterministically.

## Start Here

| Need | Read |
|---|---|
| Understand what this benchmark measures | [Eval structure wiki](docs/eval-structure-wiki.md) |
| See the taxonomy and coverage counts | [Coverage report](benchmark/coverage_report.md) |
| Run the benchmark | [Running benchmarks runbook](docs/running-benchmarks.md) |
| Browse task/results UI | [Static task/result viewer](https://rememberlenny.github.io/bluecollar-bench/) |
| Inspect current model results | [Model results summary](benchmark/runs/model_results_summary_20260706.md) |
| Find the current latest collected run | [Latest run pointer](benchmark/runs/latest.json) |
| Review known caveats | [Gap analysis](GAP_ANALYSIS_v2.md) and [EVAL v2.4 report](EVAL_v2.4.md) |

## What Is Being Evaluated

Each item is a trade-work situation:

```text
role family / work setting
  -> trade job or discipline
  -> task the role actually performs
  -> work stage and component condition
  -> evidence modality
  -> expected answer and deterministic scoring
```

The model must write `/app/answer.json` with a decision, risk level, work stage, component conditions, progress/value fields when relevant, findings, corrective actions, rationale, and references.

The grader scores the answer for:

- correct `pass`, `fail`, or `needs_more_info` decision
- risk classification
- work-stage and component-condition handling
- measured values, progress, event ordering, or sound source when relevant
- required findings and corrective actions
- schema validity
- dangerous false passes and alarmist false fails

## Current Benchmark Shape

Current generated catalog:

| Surface | Count |
|---|---:|
| Harbor task directories | 1299 |
| Catalog items | 1299 |
| Source elements parsed into the base catalog | 95 |
| Text-only items | 1171 |
| Image-backed items | 84 |
| Audio-native items | 44 |
| Fail-label items | 973 |
| Pass-label items | 252 |
| Needs-more-info items | 74 |

Coverage by role family:

| Tier | Role family | Items |
|---|---|---:|
| T1 | Heavy industrial craft / field engineer / inspector | 397 |
| T2 | Commercial construction trade / inspector | 323 |
| T3 | Residential trade / DIY / remodel context | 203 |
| T4 | Field service technician / mechanic | 204 |
| T5 | Manufacturing / assembly / quality role | 172 |

Coverage by task type:

| Code | Role task | Items |
|---|---|---:|
| ID | Identify | 146 |
| FD | Diagnose | 161 |
| CC | Check compliance | 229 |
| SEQ | Sequence work | 128 |
| TS | Select tool/material | 80 |
| HAZ | Spot hazards | 112 |
| ME | Measure/estimate | 161 |
| PA | Assess progress | 80 |
| DOC | Interpret documents | 94 |
| TRD | Make tradeoff judgment | 80 |
| RES | Recover constraints | 28 |

See [benchmark/coverage_report.md](benchmark/coverage_report.md) for the full Tier x Discipline coverage matrix.

## Repository Map

| Path | Purpose |
|---|---|
| [docs/eval-structure-wiki.md](docs/eval-structure-wiki.md) | Human-readable map of the domain model, build flow, scoring contract, and result workflow |
| [docs/eval-structure-dag.mmd](docs/eval-structure-dag.mmd) | Mermaid graph of the eval stack |
| [docs/source/](docs/source/) | Source taxonomy, element trees, modality notes, and expansion roadmap |
| [benchmark/taxonomy.json](benchmark/taxonomy.json) | Normalized taxonomy and coverage matrix |
| [benchmark/items/items.json](benchmark/items/items.json) | Full generated item catalog |
| [benchmark/media/](benchmark/media/) | Deterministic PNG and WAV fixtures copied into media-backed tasks |
| [tasks/](tasks/) | Generated Harbor task directories |
| [benchmark/runs/](benchmark/runs/) | Immutable collected run results, model summaries, comparisons, and plots |
| [scripts/](scripts/) | Catalog generation, task generation, local validation, provider harnesses, and result collection |
| [dataset.toml](dataset.toml) | Harbor dataset manifest |

## Main Workflows

Install Python dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Install Harbor if you will run agentic Harbor tasks:

```bash
uv tool install harbor
```

Smoke-test the generated benchmark without Docker or provider API keys:

```bash
make validate
```

Regenerate all tasks:

```bash
make generate
```

After regeneration, validate the generated tasks again:

```bash
make validate
```

Run one task with Harbor:

```bash
scripts/run_harbor.sh \
  --agent codex \
  --model openai/gpt-5 \
  --task electrical-panel-subpanel-defects
```

Run the full Harbor dataset:

```bash
scripts/run_harbor.sh --agent codex --model openai/gpt-5 --n-concurrent 8
```

Run one task directly through OpenRouter:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
python3 scripts/run_openrouter.py \
  --model openai/gpt-5.2 \
  --task v2-cpm-trap-001
```

Run one task directly through Gemini:

```bash
export GEMINI_API_KEY="..."
python3 scripts/run_gemini.py \
  --model gemini-2.5-pro \
  --task v2-cpm-trap-001
```

Collect and version a completed run:

```bash
python3 scripts/collect_run_results.py <harbor-runs-dir> gpt5_2026-07-05
```

Compare two collected runs:

```bash
python3 scripts/compare_runs.py gpt5_2026-07-05 gpt5_2026-07-06 \
  --output benchmark/runs/gpt5_2026-07-05_vs_2026-07-06.md
```

The run collector writes immutable directories under `benchmark/runs/<run-name>/`, stores the catalog snapshot and SHA, updates `benchmark/runs/index.json`, and updates `benchmark/runs/latest.json`.

## Important Files

Source taxonomy and roadmap:

- [Source-doc index](docs/source/README.md)
- [Benchmark taxonomy v0.1](docs/source/blue-collar-benchmark-taxonomy-v0.1.md)
- [Electrical element tree](docs/source/electrical-element-tree-v0.1.md)
- [Construction element trees](docs/source/element-trees-construction-v0.1.md)
- [Industrial service element trees](docs/source/element-trees-industrial-service-v0.1.md)
- [Modality-native task categories](docs/source/modality-native-task-categories-v0.1.md)
- [Four-track expansion plan](docs/source/expansion-plan-v0.1-four-new-capability-tracks.md)

Generated benchmark artifacts:

- [Generated item catalog](benchmark/items/items.json)
- [Normalized taxonomy](benchmark/taxonomy.json)
- [Coverage report](benchmark/coverage_report.md)
- [Leakage report](benchmark/leakage_report.md)
- [Restore report](benchmark/restore_report.md)
- [Harbor dataset manifest](dataset.toml)

Run results:

- [Run index](benchmark/runs/index.json)
- [Latest run pointer](benchmark/runs/latest.json)
- [Model results summary](benchmark/runs/model_results_summary_20260706.md)
- [Naturalization comparison](benchmark/runs/naturalization_comparison_20260706.md)
- [Latest collected analysis in this checkout](benchmark/runs/minimax_m3_natural_20260707/analysis.md)
- [Prior full-suite run report](benchmark/runs/codex_full_suite_2026-07-04.md)

Core scripts:

- [Build item catalog](scripts/build_item_catalog.py)
- [Generate v2 tasks](scripts/generate_tasks_v2.py)
- [Grade template](scripts/grade_v2.py)
- [Validate generated tasks](scripts/validate_tasks.py)
- [Run Harbor](scripts/run_harbor.sh)
- [Run OpenRouter](scripts/run_openrouter.py)
- [Run Gemini](scripts/run_gemini.py)
- [Collect run results](scripts/collect_run_results.py)
- [Compare collected runs](scripts/compare_runs.py)
- [Plot run results](scripts/plot_run_results.py)

## Answer Contract

Agents must write valid JSON to `/app/answer.json`:

```json
{
  "decision": "pass | fail | needs_more_info",
  "risk": "low | medium | high | critical",
  "work_stage": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
  "component_conditions": ["installed-defective", "non-compliant"],
  "percent_complete": 70,
  "value": 0,
  "sound_source": "component or source of the sound, when asked",
  "confidence": 0.0,
  "event_time": 0.0,
  "rate": 0.0,
  "order": ["step-id", "..."],
  "findings": ["short defect or hazard finding"],
  "actions": ["immediate corrective action"],
  "rationale": "brief explanation",
  "references": ["code or standard anchors"]
}
```

The verifier emits `/logs/verifier/reward.json` with component metrics for decision, risk, S1/S2/S3 state handling, required findings, required actions, schema validity, forbidden-token cleanliness, dangerous false passes, alarmist false fails, and aggregate reward.

## Adding Items

1. Add a curated object to `benchmark/items/seed_items.json`, or update the Markdown element trees under `docs/source/`.
2. Run `make generate`.
3. Run `make validate`.
4. Inspect `benchmark/leakage_report.md`.
5. Run `make dataset` if the task set changed and `dataset.toml` needs to be refreshed.
6. Inspect the generated `tasks/<item-id>/instruction.md`.
7. Run the task or dataset through Harbor or a direct provider harness.

Keep items small and objectively gradable. If an item requires jurisdiction-specific judgment, include the code edition or jurisdiction in the scenario and `source_refs`.

## Publishing

Before publishing to the Harbor registry, update task org names if needed:

```bash
harbor task update tasks --org "<your-org>" --scan
```

Then authenticate and publish:

```bash
harbor auth login
harbor publish tasks --public -t v0.1
harbor publish . --public -t v0.1
```

The default generated task org is `bluecollar-bench`.

## Caveats

This is still an eval under active development. The source taxonomy and many labels are generated or synthetic and need SME red-team review before the benchmark should be treated as authoritative. Use aggregate model scores as directional evidence, and read the linked reports before making claims from them.
