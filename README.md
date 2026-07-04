# Blue-Collar Benchmark

Blue-Collar Benchmark is an early Harbor task repository for evaluating whether agents can inspect trade-work scenarios with safety- and code-aware judgment.

The uploaded v0.1 taxonomy docs are preserved under `docs/source/`. The executable layer in this repository turns selected seed scenarios into deterministic Harbor tasks that require an agent to write `/app/answer.json`; the verifier grades the answer for decision, risk classification, required findings, corrective actions, and dangerous false passes.

## Current State

- `benchmark/items/seed_items.json` is the editable source of truth for the runnable seed set.
- `tasks/` contains generated Harbor task directories.
- `scripts/generate_tasks.py` regenerates all Harbor tasks from the seed item catalog.
- `scripts/validate_tasks.py` runs local oracle/verifier checks without Docker.
- `scripts/run_harbor.sh` runs one or all tasks with Harbor.

This is v0.1 scaffolding: the source taxonomy still needs SME red-team validation before claims should be treated as authoritative.

## Repository Layout

```text
benchmark/items/        Machine-readable benchmark item catalog
docs/source/            Uploaded v0.1 source taxonomy and element trees
scripts/                Generator, local validation, and Harbor run helper
tasks/                  Generated Harbor task directories
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

Run all tasks sequentially:

```bash
scripts/run_harbor.sh --agent codex --model openai/gpt-5
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
  "findings": ["short defect or hazard finding"],
  "actions": ["immediate corrective action"],
  "rationale": "brief explanation",
  "references": ["code or standard anchors"]
}
```

The verifier emits `/logs/verifier/reward.json` with component metrics:

- `decision`
- `risk`
- `findings`
- `actions`
- `schema`
- `safety_gate`
- `reward`

Critical items cap reward below passing when the answer misses the safety-critical finding or incorrectly passes dangerous work.

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

The default generated task names use the org `bluecollar-bench`.

## Adding Items

1. Add a new object to `benchmark/items/seed_items.json`.
2. Run `make generate`.
3. Run `make validate`.
4. Inspect the generated `tasks/<item-id>/instruction.md`.
5. Run the task through Harbor with at least one real agent.

Keep items small and objectively gradable. If an item requires jurisdiction-specific judgment, include the code edition or jurisdiction in the scenario and `source_refs`.

## Roadmap

- Add real multimodal fixtures once image/video licensing is settled.
- Add SME-reviewed gold labels and jurisdiction/code-edition metadata.
- Split deterministic grading from optional LLM-judge grading for open-ended hazard lists.
- Add aggregate reporting by tier, discipline, task type, S1 state, and S2 condition.
