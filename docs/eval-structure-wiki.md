# Eval Structure Wiki

This page is the working map for the Blue-Collar Benchmark eval stack. It describes the source material, generated item catalog, Harbor task surface, scoring contract, and run-analysis workflow as one system.

For a graph-only view, see [eval-structure-dag.mmd](eval-structure-dag.mmd).

## One-Screen Summary

The benchmark is easiest to read as a domain model first, and a build pipeline second.

Each eval item asks:

```text
In this work setting, for this trade job, at this work stage,
can the model do the task that this role would actually do?
```

The executable item shape is:

```text
work setting / role family
  -> trade job or discipline
  -> role task / cognitive skill
  -> work stage and component condition
  -> evidence modality
  -> expected answer and deterministic scoring
```

The repository then turns that model into generated Harbor tasks:

```text
docs/source/ + benchmark/items/*.json + benchmark/media/
  -> benchmark/items/items.json + reports
  -> tasks/<item-id>/
  -> Harbor run output
  -> benchmark/runs/<run-name>/
  -> comparison and scoreboard reports
```

## Current Catalog Shape

As of this checkout:

| Surface | Count |
|---|---:|
| Generated Harbor tasks | 1049 |
| Catalog items | 1049 |
| Source elements parsed into the base catalog | 95 |
| Text-only items | 921 |
| Image-backed items | 84 |
| Audio-native items | 44 |
| Fail-label items | 973 |
| Pass-label items | 63 |
| Needs-more-info items | 13 |

Generation mix:

| Generation source | Count |
|---|---:|
| Direct source-derived auto items | 651 |
| Matrix backfill items | 237 |
| Curated seed items | 12 |
| v2 control, NMI, trap, and tradeoff items | 21 |
| Synthetic image/media items | 56 |
| Synthetic CPM/resource-constraint items | 28 |
| Synthetic audio fault-signature items | 44 |

The leakage audit currently reports 874 clean, 175 partial, and 0 leaked items. Treat partial-leak items as review targets, not as blocked generated output.

## Domain Model

### 1. Work Settings And Role Families

The `tier` axis is the role context: it says what kind of worker, documentation, tools, tolerances, codes, and consequences the model should reason inside.

| Tier | Role family | What the role is usually doing | Items |
|---|---|---|---:|
| T1 | Heavy industrial craft / field engineer / inspector | Building or inspecting process-facility work from engineered drawings, specs, permits, and turnover packages | 245 |
| T2 | Commercial construction trade / inspector | Building or inspecting code-driven institutional and commercial work with submittals and inspections | 270 |
| T3 | Residential trade / DIY / remodel context | Diagnosing, installing, or inspecting light residential work with prescriptive code and manufacturer instructions | 176 |
| T4 | Field service technician / mechanic | Diagnosing and repairing installed assets from symptoms, work orders, OEM manuals, and service observations | 196 |
| T5 | Manufacturing / assembly / quality role | Executing or inspecting fixed-station production work against standard work and quality gates | 162 |

This axis answers: "What kind of job is this worker in?"

### 2. Trade Jobs Covered

The `discipline` axis is the trade job or work domain.

| Discipline | Typical roles represented | Items |
|---|---|---:|
| 2.1 Electrical | Electrician, low-voltage tech, panel/wiring inspector, service troubleshooter | 233 |
| 2.2 Piping/Plumbing | Pipefitter, plumber, plumbing inspector, hydronic/service tech | 97 |
| 2.3 HVAC-R | HVAC installer, refrigeration tech, BAS/service tech | 80 |
| 2.4 Structural & Ironwork | Ironworker, rigger, steel inspector, machinery-moving role | 91 |
| 2.5 Concrete & Masonry | Concrete finisher, formwork crew, mason, inspection role | 61 |
| 2.6 Carpentry & Finishes | Framer, finish carpenter, roofer/envelope worker, remodeler | 79 |
| 2.7 Equipment/Millwright | Millwright, rotating-equipment mechanic, conveyor/service role | 78 |
| 2.8 Instrumentation & Controls | Instrument tech, calibration tech, controls/loop-check role | 50 |
| 2.9 Automotive | Automotive technician, diagnostic tech, powertrain/EV service role | 82 |
| 2.10 Assembly & Fabrication | Assembly operator, welder/fabricator, quality inspector | 30 |
| 2.11 Sitework & Utilities | Equipment operator, utility crew, excavation/trenching inspector | 51 |
| 2.12 Safety | Safety lead, competent person, rigging/LOTO/fall-protection reviewer | 117 |

This axis answers: "Which trade job is the model standing in for?"

### 3. Tasks Done In Those Roles

The `task_type` axis is the role task: what the worker or inspector has to do with the evidence.

| Code | Role task | What the model must do | Items |
|---|---|---|---:|
| ID | Identify | Name the component, material, tool, system, or condition | 126 |
| FD | Diagnose | Infer the likely fault from symptoms, photos, sounds, readings, or context | 149 |
| CC | Check compliance | Decide whether the work meets code, spec, drawing, or manufacturer requirements | 209 |
| SEQ | Sequence work | Put procedure steps in the right order or identify an order violation | 108 |
| TS | Select tool/material | Choose the correct wire, fastener, blade, fixture, tool, or method | 50 |
| HAZ | Spot hazards | Identify unsafe conditions and required immediate controls | 92 |
| ME | Measure/estimate | Read or estimate dimensions, values, tolerances, torque, levels, or quantities | 147 |
| PA | Assess progress | Estimate percent complete, lifecycle stage, defects, and remaining work | 35 |
| DOC | Interpret documents | Read P&IDs, plans, schedules, tags, cut sheets, checklists, or service data | 74 |
| TRD | Make tradeoff judgment | Choose the practical compliant action when field constraints conflict with ideal procedure | 31 |
| RES | Recover constraints | Decide what can proceed, what is blocked, and what recovery plan is valid | 28 |

This axis answers: "What job task is being evaluated?"

### 4. Stages And States

The state model tracks where the work is in its lifecycle, what condition the component is in, and how much progress should be credited.

S1 is the work-item stage:

| Stage | Meaning | Default progress credit | Items |
|---|---|---:|---:|
| planned | Scoped but not started | 5% | 31 |
| staged | Materials, tools, access, or kit are ready | 15% | 50 |
| in-progress | Physical work or diagnosis is underway | 45% | 254 |
| rough-complete | Installed or assembled, but not fully closed out | 70% | 484 |
| tested/inspected | Verification has been performed | 85% | 94 |
| rework | Failed verification and requires correction | 60% | 0 |
| accepted | Signed off or handed over | 95% | 2 |
| in-service | Operating asset in the maintenance/service world | 100% | 134 |

S2 is the thing's condition:

| Condition | Meaning |
|---|---|
| new | Not yet installed or used |
| installed-correct | Installed and compliant |
| installed-defective | Looks installed, but has a latent defect |
| non-compliant | May function, but violates code/spec/procedure |
| worn | Used or aged but not necessarily failed |
| degraded | Performance or condition has declined |
| failed | No longer performs the required function |

S3 is progress or earned value. In some media tasks, the same scoring slot also grades measured values, sound sources, event timing, rates, or ordered sequences.

This state layer answers: "Where is the work in the job, and what condition is the thing in?"

### 5. Evidence Modalities

The `modality` axis says what evidence the role gets.

| Modality | What it tests | Items |
|---|---|---:|
| text | Scenario-only reasoning from written observations | 921 |
| image | Visual reading of instruments, rigging, schedules, or work conditions | 84 |
| audio | Fault-signature recognition where sound is the signal | 44 |

Future video-native items follow the same pattern for event time, motion, rate, order, and cause-effect.

### 6. Example Item Read

An item like `T3 x 2.2 Plumbing x CC x rough-complete x image/text` means:

| Part | Meaning |
|---|---|
| `T3` | Residential / DIY role context |
| `2.2 Plumbing` | Trade job is plumbing |
| `CC` | Role task is code/spec compliance judgment |
| `rough-complete` | Work is installed but not accepted or in service |
| evidence | The model sees a scenario, image, audio, or document-style fixture |
| score | The grader checks decision, risk, state, findings, actions, and safety gates |

## Build And Evaluation Layers

### 1. Taxonomy And Source Layer

Canonical source docs live in [docs/source/](source/). They define the intended benchmark axes:

| Axis | Meaning | Stored in |
|---|---|---|
| Tier | Work setting / worker context from T1 through T5 | `docs/source/*.md`, `benchmark/taxonomy.json` |
| Discipline | Trade domain such as electrical, HVAC-R, rigging, instrumentation | `docs/source/*.md`, `benchmark/taxonomy.json` |
| Task type | Cognitive skill such as ID, FD, CC, SEQ, HAZ, ME, DOC, TRD, RES | `docs/source/*.md`, `scripts/build_item_catalog.py` |
| State | S1 lifecycle, S2 condition, S3 progress / measured value | `benchmark/taxonomy.json`, generated item JSON |
| Modality | Text, image, audio, and future video-like task evidence | `benchmark/items/*.json`, `benchmark/media/` |

`scripts/build_item_catalog.py` parses the source docs into `benchmark/taxonomy.json`, base items, and `benchmark/coverage_report.md`.

### 2. Item Source Layer

The generated catalog is assembled from several inputs:

| Input | Purpose |
|---|---|
| `docs/source/*.md` | Human-readable taxonomy and element trees |
| `benchmark/items/seed_items.json` | Hand-authored curated tasks |
| `benchmark/items/control_items_v2.json` | Pass, needs-more-info, alarmist-trap, and tradeoff controls |
| `benchmark/items/media_items_v2.json` | Synthetic image-backed measurement and rigging tasks |
| `benchmark/items/cpm_items_v2.json` | Synthetic CPM and resource-constraint tasks |
| `benchmark/items/audio_items_v2.json` | Synthetic audio fault-signature tasks |
| `benchmark/items/original_scenarios.json` | Restored observation text for auto items |
| `benchmark/items/interpretation_map.json` | Interpretation vocabulary used to avoid reward-token echoing |
| `benchmark/media/` | PNG and WAV fixtures copied into media-backed task containers |

The final executable item catalog is [benchmark/items/items.json](../benchmark/items/items.json).

### 3. Build And Audit Layer

The normal build command is:

```bash
make generate
```

It runs:

```text
scripts/build_item_catalog.py
  -> scripts/generate_tasks_v2.py
       -> scripts/restore_scenarios.py
       -> scripts/leakage_audit.py
       -> task directory generation
```

Outputs:

| Output | Role |
|---|---|
| `benchmark/items/items.json` | Full item catalog |
| `benchmark/taxonomy.json` | Normalized axes, state model, and coverage matrix |
| `benchmark/coverage_report.md` | Coverage by discipline, tier, task type, and matrix cell |
| `benchmark/leakage_report.md` | Answer-token leakage buckets and item annotations |
| `benchmark/restore_report.md` | Evidence restoration and residual partial-leak summary |
| `tasks/` | Generated Harbor task directories |

### 4. Harbor Task Layer

Every catalog item becomes one generated task directory:

```text
tasks/<item-id>/
  instruction.md
  task.toml
  environment/Dockerfile
  solution/solve.sh
  tests/test.sh
  tests/grade.py
  tests/item.json
```

The task gives an agent a trade-work scenario and requires it to write `/app/answer.json`. Media-backed tasks copy fixtures into `/app/media/` inside the container.

The generated task is intentionally redundant:

| File | Why it exists |
|---|---|
| `instruction.md` | Human/agent-facing prompt |
| `tests/item.json` | Ground truth item payload used by the grader |
| `tests/grade.py` | Deterministic verifier copied from `scripts/grade_v2.py` |
| `solution/solve.sh` | Oracle answer used by local validation |
| `tests/test.sh` | Harbor test wrapper |
| `environment/Dockerfile` | Minimal execution environment and media copy instructions |
| `task.toml` | Harbor task metadata |

### 5. Answer And Scoring Layer

Agents must write JSON to `/app/answer.json`. The core slots are:

| Slot | Meaning |
|---|---|
| `decision` | `pass`, `fail`, or `needs_more_info` |
| `risk` | `low`, `medium`, `high`, or `critical` |
| `work_stage` | Work lifecycle state (legacy answers may still use `s1_state`) |
| `component_conditions` | Component or compliance condition tags (legacy `s2_conditions`) |
| `percent_complete` | Progress estimate, reused for some numeric grading (legacy `s3_percent`) |
| `value`, `sound_source`, `event_time`, `rate`, `order` | Modality-specific expected outputs |
| `findings` | Defect, hazard, or condition findings |
| `actions` | Corrective or escalation actions |
| `rationale`, `references` | Explanation and code/spec anchors |

`scripts/grade_v2.py` scores deterministic components, including:

| Component | What it protects |
|---|---|
| `decision` | Correct pass/fail/NMI classification |
| `risk` | Correct severity |
| `s1`, `s2`, `s3` | State and progress/value reasoning |
| `findings`, `actions` | Required observation and remediation content |
| `schema` | Valid answer shape |
| `forbidden_clean` | Avoids saying unsafe work is clean |
| `dangerous_false_pass` | Headline safety gate for passing unsafe/non-compliant work |
| `alarmist_false_fail` | Headline safety gate for failing compliant controls |

### 6. Validation Layer

Run local validation before treating generated tasks as usable:

```bash
make validate
```

`scripts/validate_tasks.py` checks required task files, parses `tests/item.json`, verifies media fixtures, runs the oracle `solution/solve.sh`, runs `tests/grade.py`, and requires a near-perfect oracle reward. This does not replace a real Harbor run, but it catches broken generated artifacts quickly without Docker.

### 7. Harbor Run Layer

Run one task:

```bash
scripts/run_harbor.sh --agent codex --model openai/gpt-5 --task <item-id>
```

Run the full dataset:

```bash
scripts/run_harbor.sh --agent codex --model openai/gpt-5 --n-concurrent 8
```

In this checkout, the robust local Harbor invocation has been the module form:

```bash
.venv/bin/python -m harbor.cli.main
```

Use filesystem reconciliation against `tasks/*/task.toml` and successful `result.json` files before assuming a large Harbor summary is complete.

### 8. Result Collection And Comparison Layer

Collect a Harbor run into immutable benchmark results:

```bash
make collect-run RUNS_DIR=<harbor-runs-dir> RUN_NAME=<run-name>
```

This writes:

```text
benchmark/runs/<run-name>/
  manifest.json
  metrics.json
  analysis.md
  catalog.snapshot.json
```

It also updates:

```text
benchmark/runs/index.json
benchmark/runs/latest.json
```

Compare two collected runs:

```bash
make compare-runs BASE_RUN=<old-run> CANDIDATE_RUN=<new-run>
```

Run comparisons report shared-task reward deltas, catalog hash mismatches, axis rollups, safety-gate deltas, largest regressions, and largest improvements.

## Operating Playbooks

### Add Or Change Text Items

1. Edit `docs/source/*.md` for source-tree changes or `benchmark/items/seed_items.json` for curated items.
2. Run `make generate`.
3. Inspect `benchmark/coverage_report.md`, `benchmark/leakage_report.md`, and one or more generated `tasks/<item-id>/instruction.md` files.
4. Run `make validate`.
5. Run `make dataset` if the task set changed and `dataset.toml` needs to be refreshed.

### Add Or Change Media Items

1. Update the generator or source JSON for the media family.
2. Run `make media` or `make audio` when the media fixtures need to be regenerated.
3. Run `make generate`.
4. Verify generated media exists under both `benchmark/media/` and the relevant `tasks/<item-id>/environment/media/` directory.
5. Run `make validate`.

### Produce A Scoreboard

1. Run the benchmark through Harbor.
2. Reconcile completed task coverage against `tasks/*/task.toml`.
3. Run `make collect-run RUNS_DIR=<harbor-runs-dir> RUN_NAME=<run-name>`.
4. Review `benchmark/runs/<run-name>/analysis.md`.
5. Compare against prior runs with `make compare-runs`.

## Maintenance Notes

- `benchmark/items/items.json` is generated. Do not hand-edit it unless you are doing controlled repair work and will regenerate afterward.
- `tasks/` is generated from the catalog and grader template. Treat task diffs as generated artifacts.
- Keep `README.md`, `dataset.toml`, `benchmark/coverage_report.md`, `benchmark/leakage_report.md`, and `benchmark/restore_report.md` aligned after generation changes.
- Preserve `benchmark/runs/<run-name>/catalog.snapshot.json` for reproducibility. Comparisons across different catalog hashes are model-plus-catalog comparisons, not pure model comparisons.
- The current catalog is fail-heavy. Use `GAP_ANALYSIS_v2.md` before making claims from aggregate rewards.
