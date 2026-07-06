# Blue-Collar Benchmark

Blue-Collar Benchmark is a Harbor task repository for evaluating whether agents can inspect trade-work scenarios with safety- and code-aware judgment.

The uploaded v0.1 taxonomy docs are preserved under `docs/source/`. The executable layer parses those element trees, fills the v0.1 Tier x Discipline coverage matrix, and emits deterministic Harbor tasks that require an agent to write `/app/answer.json`; the verifier grades the answer for decision, risk classification, S1/S2 state handling, required findings, corrective actions, and dangerous false passes.

## Current State

- `benchmark/taxonomy.json` is the normalized taxonomy and coverage matrix.
- `benchmark/items/seed_items.json` contains curated hand-authored seed items.
- `benchmark/items/control_items_v2.json` contains pass, needs-more-info, alarmist-trap, and tradeoff control items.
- `benchmark/items/media_items_v2.json` contains synthetic image-backed instrument and rigging items.
- `benchmark/items/audio_items_v2.json` contains synthetic audio-native fault-signature items.
- `benchmark/items/original_scenarios.json` and `benchmark/items/interpretation_map.json` support v2.4 restoration of placeholder-stripped auto items.
- `benchmark/media/` contains generated PNG and WAV fixtures copied into media-backed task containers at `/app/media/`.
- `benchmark/items/items.json` is the generated comprehensive item catalog.
- `benchmark/coverage_report.md` summarizes coverage by discipline, tier, task type, and matrix cell.
- `benchmark/leakage_report.md` summarizes answer-token leakage and writes `leakage_ratio` onto each item.
- `benchmark/restore_report.md` summarizes restored evidence and residual partial leakage for repaired auto items.
- `dataset.toml` is the Harbor dataset manifest for the full benchmark.
- `tasks/` contains generated Harbor task directories.
- `scripts/build_item_catalog.py` parses the source docs and builds the comprehensive item catalog.
- `scripts/gen_media_items.py` deterministically renders synthetic media fixtures and emits `media_items_v2.json`.
- `scripts/gen_audio_items.py` deterministically renders synthetic audio fixtures and emits `audio_items_v2.json`.
- `scripts/gen_text_rebalance_items.py` deterministically emits text-only pass/NMI controls for decision rebalance.
- `scripts/restore_scenarios.py` restores auto-item evidence and re-keys findings to interpretation vocabulary before leakage auditing.
- `scripts/generate_tasks_v2.py` merges v2 controls, image media, CPM, audio, and text-rebalance items, restores scenarios, runs leakage auditing, and regenerates all Harbor tasks with `grade_v2`.
- `scripts/collect_run_results.py` harvests Harbor verifier rewards into versioned run directories pinned to the catalog hash.
- `scripts/compare_runs.py` compares two collected runs across shared tasks and aggregate axes.
- `scripts/grade_v2.py` is the current deterministic verifier template used in generated tasks.
- `scripts/validate_tasks.py` runs local oracle/verifier checks without Docker.
- `scripts/run_harbor.sh` runs either one task or the full Harbor dataset.
- `docs/source/modality-native-task-categories-v0.1.md` defines audio-only and video-only task categories where the modality is the signal.

Current generated size: 1299 Harbor tasks from 95 source elements, 12 curated seeds, 21 v2 control items, 56 synthetic instrument/media items, 28 synthetic CPM/resource-constraint items, 44 synthetic audio fault-signature items, 250 synthetic text rebalance items, 651 direct source-derived items, and 237 matrix backfill items. The v2.1-v2.5 catalog adds image, audio, and pass/NMI text evidence with deterministic ground truth, bringing pass/needs_more_info coverage to 326/1299 items. See `GAP_ANALYSIS_v2.md` for the remaining leakage, SME-review, and aggregate-score caveats. The source taxonomy still needs SME red-team validation before claims should be treated as authoritative.

## Key Links

Start here:

- [Eval structure wiki](docs/eval-structure-wiki.md) - role families, trade jobs, role tasks, stages/states, modalities, scoring, and run workflow.
- [Eval structure DAG](docs/eval-structure-dag.mmd) - graph of the domain model plus source, build, validation, Harbor run, collection, and comparison flow.
- [Gap analysis](GAP_ANALYSIS_v2.md) - current benchmark-health caveats and priority fixes before treating aggregate scores as final.
- [Post-merge eval report](EVAL_v2.4.md) - v2.4 repair notes, run validity caveats, and recommended next evaluation order.

Source taxonomy and roadmap:

- [Source-doc index](docs/source/README.md) - entrypoint for the original taxonomy and expansion docs.
- [Benchmark taxonomy v0.1](docs/source/blue-collar-benchmark-taxonomy-v0.1.md) - tiers, disciplines, task types, and unified S1/S2/S3 state model.
- [Electrical element tree](docs/source/electrical-element-tree-v0.1.md) - detailed electrical source elements.
- [Construction element trees](docs/source/element-trees-construction-v0.1.md) - construction trade source elements.
- [Industrial service element trees](docs/source/element-trees-industrial-service-v0.1.md) - industrial/service source elements.
- [Modality-native task categories](docs/source/modality-native-task-categories-v0.1.md) - audio/video-native task design.
- [Four-track expansion plan](docs/source/expansion-plan-v0.1-four-new-capability-tracks.md) - roadmap for synthetic-parametric expansion.

Generated benchmark artifacts:

- [Generated item catalog](benchmark/items/items.json) - full machine-readable catalog used to generate tasks.
- [Normalized taxonomy](benchmark/taxonomy.json) - generated axes, state model, media schema, and coverage matrix.
- [Coverage report](benchmark/coverage_report.md) - item counts by discipline, tier, task type, and matrix cell.
- [Leakage report](benchmark/leakage_report.md) - answer-token leakage buckets and remediation notes.
- [Restore report](benchmark/restore_report.md) - evidence restoration and residual partial-leak summary.
- [Harbor dataset manifest](dataset.toml) - published dataset/task manifest.

Run results and analysis:

- [Run index](benchmark/runs/index.json) - versioned run registry.
- [Latest run pointer](benchmark/runs/latest.json) - current latest collected run metadata.
- [Latest collected analysis](benchmark/runs/gpt55_full_20260705_5b2c706/analysis.md) - collected run scoreboard and axis rollups.
- [Prior full-suite run report](benchmark/runs/codex_full_suite_2026-07-04.md) - earlier full-suite run summary.

Main workflow scripts:

- [Build item catalog](scripts/build_item_catalog.py)
- [Generate v2 tasks](scripts/generate_tasks_v2.py)
- [Grade template](scripts/grade_v2.py)
- [Validate generated tasks](scripts/validate_tasks.py)
- [Run Harbor](scripts/run_harbor.sh)
- [Collect run results](scripts/collect_run_results.py)
- [Compare collected runs](scripts/compare_runs.py)
- [Plot run results](scripts/plot_run_results.py)

## Repository Layout

```text
benchmark/items/        Machine-readable benchmark item catalog
benchmark/taxonomy.json Normalized axes, state model, and coverage matrix
benchmark/coverage_report.md
docs/eval-structure-wiki.md
docs/eval-structure-dag.mmd
docs/source/            Uploaded v0.1 source taxonomy and element trees
scripts/                Generator, local validation, and Harbor run helper
tasks/                  Generated Harbor task directories
dataset.toml            Harbor dataset manifest
```

For the overall eval architecture, read `docs/eval-structure-wiki.md`. For a graph-only view of the build, validation, Harbor run, and result-collection flow, render `docs/eval-structure-dag.mmd`.

Each Harbor task follows the current Harbor task structure:

```text
instruction.md
task.toml
environment/Dockerfile
solution/solve.sh
tests/test.sh
tests/grade.py
tests/item.json
```

## Quick Start

Regenerate tasks:

```bash
make generate
```

This rebuilds the 900-item base catalog, merges the v2 controls plus synthetic image, CPM, and audio items, restores placeholder-stripped evidence, tags leakage, copies media fixtures into media-backed tasks, and writes generated tasks with the v2 grader.

Validate the generated tasks locally:

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

Run the full benchmark dataset:

```bash
scripts/run_harbor.sh --agent codex --model openai/gpt-5 --n-concurrent 8
```

You can also run directly with Harbor:

```bash
harbor run -p . --agent codex --model openai/gpt-5 --n-concurrent 8
```

Collect and version run results:

```bash
python3 scripts/collect_run_results.py <harbor-runs-dir> gpt5_2026-07-05
```

This writes an immutable run directory:

```text
benchmark/runs/gpt5_2026-07-05/
manifest.json
metrics.json
analysis.md
catalog.snapshot.json
```

It also updates `benchmark/runs/index.json` and `benchmark/runs/latest.json`. Reusing a run name is rejected unless `--overwrite` is passed, so previous measurements are not lost accidentally. Each run stores the full `items.json` snapshot and catalog SHA used at collection time.

Compare two collected runs:

```bash
python3 scripts/compare_runs.py gpt5_2026-07-05 gpt5_2026-07-06 \
  --output benchmark/runs/gpt5_2026-07-05_vs_2026-07-06.md
```

The comparison report warns if catalog hashes differ, then reports shared-task reward deltas, safety-gate changes, axis rollups, largest regressions, and largest improvements.

Install Harbor if needed:

```bash
uv tool install harbor
```

## Answer Contract

Agents must write valid JSON to `/app/answer.json`:

```json
{
  "decision": "pass | fail | needs_more_info",
  "risk": "low | medium | high | critical",
  "s1_state": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
  "s2_conditions": ["installed-defective", "non-compliant"],
  "s3_percent": 70,
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

The verifier emits `/logs/verifier/reward.json` with component metrics:

- `decision`
- `risk`
- `s1`
- `s2`
- `s3`
- `findings`
- `actions`
- `schema`
- `forbidden_clean`
- `dangerous_false_pass`
- `alarmist_false_fail`
- `reward`

The two directional safety metrics are intended as headline measures: `dangerous_false_pass` catches passing unsafe/non-compliant work, while `alarmist_false_fail` catches failing compliant controls.

For image-backed instrument items, `s3` is reused for numeric-value scoring: `value` must be within the item's `value_tolerance` of `expected_value`. For audio/video-native items, the same slot can grade `sound_source`, `event_time`, `rate`, and `order` when corresponding expected fields exist.

## Item Schema

Every item includes `modality` and `media` fields. Current generated items include 921 text-only tasks, 84 `modality: "image"` tasks, and 44 `modality: "audio"` tasks. Image-backed items may include `expected_value` and `value_tolerance` for deterministic grading of readings or computed quantities. Audio-native items may include `expected_sound_source` and `reduction_test`; future video-native items use the same pattern with `expected_event_time`, `expected_rate`, `expected_order`, and `confusable_with`.

## Publishing

Before publishing to the Harbor registry, update task org names if needed:

```bash
harbor task update tasks --org "<your-org>" --scan
```

Then authenticate and publish:

```bash
harbor auth login
harbor publish tasks --public -t v0.1
```

Publish the dataset manifest after tasks are published:

```bash
harbor publish . --public -t v0.1
```

The default generated task names use the org `bluecollar-bench`.

## Adding Items

1. Add a curated object to `benchmark/items/seed_items.json`, or update the Markdown element trees under `docs/source/`.
2. Run `make generate`.
3. Run `make validate`.
4. Inspect `benchmark/leakage_report.md` and avoid scenarios that repeat required conclusion tokens verbatim.
5. Run `make dataset` if the task set changed and you want to refresh `dataset.toml`.
6. Inspect the generated `tasks/<item-id>/instruction.md`.
7. Run the task or dataset through Harbor with at least one real agent.

Keep items small and objectively gradable. If an item requires jurisdiction-specific judgment, include the code edition or jurisdiction in the scenario and `source_refs`.

## Roadmap

- Extend synthetic media families: dial indicators, torque wrench/spec plates, panel schedules, P&ID excerpts, and photo-realistic variants seeded from the same ground-truth parameters.
- Add animated video primitives for drip rate, torque-sequence order, belt drift, and wobble/runout tests.
- Add SME-reviewed gold labels and jurisdiction/code-edition metadata.
- Split deterministic grading from optional LLM-judge grading for open-ended hazard lists.
- Add aggregate reporting by tier, discipline, task type, S1 state, and S2 condition.
