# Blue-Collar Benchmark

Blue-Collar Benchmark is a Harbor task repository for evaluating whether agents can inspect trade-work scenarios with safety- and code-aware judgment.

The uploaded v0.1 taxonomy docs are preserved under `docs/source/`. The executable layer parses those element trees, fills the v0.1 Tier x Discipline coverage matrix, and emits deterministic Harbor tasks that require an agent to write `/app/answer.json`; the verifier grades the answer for decision, risk classification, S1/S2 state handling, required findings, corrective actions, and dangerous false passes.

## Current State

- `benchmark/taxonomy.json` is the normalized taxonomy and coverage matrix.
- `benchmark/items/seed_items.json` contains curated hand-authored seed items.
- `benchmark/items/control_items_v2.json` contains pass, needs-more-info, alarmist-trap, and tradeoff control items.
- `benchmark/items/media_items_v2.json` contains synthetic image-backed instrument and rigging items.
- `benchmark/media/` contains generated PNG fixtures copied into image-backed task containers at `/app/media/`.
- `benchmark/items/items.json` is the generated comprehensive item catalog.
- `benchmark/coverage_report.md` summarizes coverage by discipline, tier, task type, and matrix cell.
- `benchmark/leakage_report.md` summarizes answer-token leakage and writes `leakage_ratio` onto each item.
- `dataset.toml` is the Harbor dataset manifest for the full benchmark.
- `tasks/` contains generated Harbor task directories.
- `scripts/build_item_catalog.py` parses the source docs and builds the comprehensive item catalog.
- `scripts/gen_media_items.py` deterministically renders synthetic media fixtures and emits `media_items_v2.json`.
- `scripts/generate_tasks_v2.py` merges v2 controls and media items, runs leakage auditing, and regenerates all Harbor tasks with `grade_v2`.
- `scripts/grade_v2.py` is the current deterministic verifier template used in generated tasks.
- `scripts/validate_tasks.py` runs local oracle/verifier checks without Docker.
- `scripts/run_harbor.sh` runs either one task or the full Harbor dataset.

Current generated size: 1005 Harbor tasks from 95 source elements, 12 curated seeds, 21 v2 control items, 56 synthetic instrument/media items, 28 synthetic CPM/resource-constraint items, 651 direct source-derived items, and 237 matrix backfill items. The v2.1 catalog adds real image evidence with deterministic ground truth, but the benchmark is still fail-heavy overall; see `GAP_ANALYSIS_v2.md` before treating aggregate scores as final. The source taxonomy still needs SME red-team validation before claims should be treated as authoritative.

## Repository Layout

```text
benchmark/items/        Machine-readable benchmark item catalog
benchmark/taxonomy.json Normalized axes, state model, and coverage matrix
benchmark/coverage_report.md
docs/source/            Uploaded v0.1 source taxonomy and element trees
scripts/                Generator, local validation, and Harbor run helper
tasks/                  Generated Harbor task directories
dataset.toml            Harbor dataset manifest
```

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

This rebuilds the 900-item base catalog, merges the v2 controls and synthetic media items, tags leakage, copies media fixtures into image-backed tasks, and writes generated tasks with the v2 grader.

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

For image-backed instrument items, `s3` is reused for numeric-value scoring: `value` must be within the item's `value_tolerance` of `expected_value`.

## Item Schema

Every item includes `modality` and `media` fields. Current generated items include 921 text-only tasks and 84 `modality: "image"` tasks. Image-backed items may also include `expected_value` and `value_tolerance` for deterministic grading of readings or computed quantities.

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
- Add SME-reviewed gold labels and jurisdiction/code-edition metadata.
- Split deterministic grading from optional LLM-judge grading for open-ended hazard lists.
- Add aggregate reporting by tier, discipline, task type, S1 state, and S2 condition.
