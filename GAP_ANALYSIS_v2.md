# Gap Analysis & v2 Upgrade — bluecollar-bench

Reviewed at commit state: 900 tasks, 95 source elements. The Harbor translation is structurally strong (clean item schema, deterministic tasks, coverage matrix honored). The gaps below are about *measurement validity*, which matters more than adding items — three of them let a degenerate policy score highly without any trade knowledge.

## Findings

### 1. Every item's answer is "fail" (critical)
All 900 items had `decision: "fail"` and risk was never `low`. A constant policy — always output fail/critical plus generic "stop work, control hazard, verify" — maxes the decision, actions, and safety-gate metrics with zero domain knowledge. A defect benchmark needs compliant work in the denominator or it measures agreement with the test's mood, not inspection skill.

**Fix shipped:** 21 curated v2 text items, 56 synthetic image-backed v2.1 items, 28 CPM/Gantt image-backed v2.2 items, and 44 synthetic audio-backed v2.3 items. Catalog is now 1,049: 973 fail, 63 pass, 13 needs_more_info, with 84 image-backed items and 44 audio-backed items. The synthetic slices are healthier than the original corpus, but the overall catalog is still far too fail-heavy — target ≥25–30% pass/nmi. The v2 controls and synthetic media families are the patterns to replicate; text-item rebalance remains priority 1.

### 2. Answer leakage (critical)
0/1,049 items include ≥80% of their `required_findings` tokens verbatim in the scenario text after the current audit (see `benchmark/leakage_report.md`); 175 remain in the partial 40–79% bucket. The v2.4 repair also fixed a more serious failure mode: 888 auto-generated scenarios had been evidence-stripped to placeholder wording, so the low leakage number was previously achieved by deleting the observation. Those scenarios now restore the original observable defect phrase and re-key `required_findings` to interpretation vocabulary that a competent answer supplies but the scenario does not contain.

**Fix shipped:** `scripts/restore_scenarios.py` repairs placeholder scenarios from `original_scenarios.json`, applies `interpretation_map.json`, verifies `evidence_present`, and writes `benchmark/restore_report.md`; `scripts/leakage_audit.py` then tags every item with `leakage_ratio` and writes the full-catalog report. **Remaining:** SME-refine the element-level interpretation map and review the 175 partial items, including 83 residual partials among repaired auto items.

### 3. Grader brittleness (high)
- v1 checked `forbidden` tokens against the *entire flattened answer*, so a correct fail rationale containing the word "pass" ("this cannot pass inspection") tripped the gate and halved the reward. Verified empirically.
- Required-finding groups were AND-only exact-token matches ("bonded" ≠ "bonding"), punishing paraphrase.
- `s3_percent` existed in items but was never graded.

**Fix shipped:** `scripts/grade_v2.py` — forbidden scoped to findings/actions/s2 only; optional `findings_mode: any_per_group` for synonym groups; directional gates (`dangerous_false_pass` and `alarmist_false_fail` reported separately — these two numbers are the headline safety metrics for any model you evaluate); S2 empty-set handling for pass items; S3 graded with ±15pt tolerance; numeric `value` graded against `expected_value`/`value_tolerance` for image-backed items; set answers via `expected_set` scored by F1 for workable-backlog questions; audio/video-native hooks for `sound_source`, `event_time`, `rate`, and `order` using expected-field scoring. `scripts/generate_tasks_v2.py` regenerates all 1,049 tasks with the v2 grader while reusing the v1 render pipeline. Keyword matching remains a ceiling — the endgame is an LLM-judge rubric with these deterministic checks as a floor.

### 4. Coverage imbalances (medium)
From the coverage report: TRD 26 items, PA 35, vs. CC 203 — yet TRD (textbook-vs-field judgment) and PA (progress from partial evidence) are the task types most distinctive to this benchmark's thesis. Backfill items (237) are the thinnest: element context stretched into matrix cells the source trees didn't claim. Suggested targets: TRD ≥80, PA ≥80, with T5 station-progress photos as the PA anchor per the taxonomy notes.

### 5. Synthetic multimodal layer (strategic)
The benchmark is now genuinely multimodal. **v2.1 shipped:** `scripts/gen_media_items.py` renders 56 synthetic instrument/diagram images and emits items whose ground truth is computed from the same parameters that drew the image — zero labeling cost, deterministic answer keys, and a natural decision mix. Four families are included: brake-rotor micrometer vs. stamped minimum, micron-gauge decay tests, confined-space 4-gas screens, and two-leg sling diagrams. Items carry `modality`, `media`, `expected_value`, and `value_tolerance`; generated task metadata preserves those fields and image fixtures are copied into `/app/media/`.

**v2.2 shipped:** `scripts/gen_cpm_items.py` adds Track 3 field-constraint reasoning. It renders 28 residential CPM/Gantt chart items with cure lags and inspection holds as hard constraints, covering delay quantification, workable backlog, recovery traps, and illegible-duration needs_more_info variants. New task type: `RES`.

**v2.3 shipped:** `scripts/gen_audio_items.py` adds 44 audio-native synthetic fault-signature items across engine rhythm, bearing condition, panel hum versus arcing, and water hammer. WAV fixtures are generated from the same parameters that determine the labels and are copied into `/app/media/` like image fixtures.

**v2.4 shipped:** `scripts/restore_scenarios.py` restores evidence to 888 placeholder-stripped auto items and re-keys findings to the interpretation map. `scripts/collect_run_results.py` preserves per-task verifier metrics in versioned run directories, snapshots the evaluated `items.json`, and pins each result set to a catalog hash so future scoreboards are reproducible against the catalog they evaluated. `scripts/compare_runs.py` compares collected runs without overwriting prior results.

## Priority order
1. Rebalance decisions (extend v2 control pattern to ~250 pass/nmi items)
2. Review the 175 partial-leakage items, with SME focus on the 83 repaired auto items still at >=40% overlap
3. Adopt grade_v2 everywhere (done via generate_tasks_v2) and track the two directional gates as headline metrics
4. Extend synthetic media families: psychrometric calculators, dial indicators, torque/spec-plate comparisons, panel schedules, P&ID excerpts, and photo-realistic variants seeded from synthetic parameters
5. SME red-team pass on code refs (still open from taxonomy v0.1)
6. Extend the modality-native layer with animated video primitives: drip rate, torque-sequence order, belt drift, and wobble/runout

## Files in this delta
- `benchmark/items/control_items_v2.json` — 21 curated items (pass / nmi / trap / trd)
- `benchmark/items/media_items_v2.json` — 56 synthetic image-backed items
- `benchmark/items/cpm_items_v2.json` — 28 CPM/Gantt image-backed RES items
- `benchmark/items/audio_items_v2.json` — 44 synthetic audio-native fault-signature items
- `benchmark/items/original_scenarios.json` — source observations used to repair placeholder-stripped auto items
- `benchmark/items/interpretation_map.json` — element-level interpretation vocabulary for restored findings
- `benchmark/media/` — generated PNG and WAV fixtures used by media-backed tasks
- `benchmark/items/items.json` — merged catalog (1,049), tagged with `leakage_ratio`
- `benchmark/leakage_report.md` — audit output
- `benchmark/restore_report.md` — scenario restoration audit output
- `scripts/gen_media_items.py` — deterministic synthetic media renderer
- `scripts/gen_cpm_items.py` — deterministic CPM schedule/item renderer
- `scripts/gen_audio_items.py` — deterministic synthetic audio renderer with self-verification
- `scripts/restore_scenarios.py` — restores evidence and re-keys findings before leakage audit
- `scripts/collect_run_results.py` — collects per-task Harbor verifier rewards into versioned run directories
- `scripts/compare_runs.py` — compares collected runs and reports shared-task/axis deltas
- `scripts/grade_v2.py` — upgraded verifier (tested: good-fail=1.0, dangerous false pass=0.0, alarmist false fail=0.0, numeric value in tolerance=1.0, numeric value out of tolerance loses the numeric component)
- `scripts/generate_tasks_v2.py` — merge controls, media items, CPM items, and audio items; tag leakage; normalize modality/media; copy media fixtures; and regenerate with v2 grader
- `scripts/leakage_audit.py` — leakage tagging/report
- `docs/source/modality-native-task-categories-v0.1.md` — audio-only and video-only task categories where the modality is the signal
- Regenerate tasks after pulling: `make generate`

## Addendum — synthetic multimodal layer (v2.1)
`scripts/gen_media_items.py` renders instrument images with matplotlib and emits items whose ground truth is computed from the same parameters that drew the image. The four current families test different skills: rotor micrometer reading against a stamped minimum (including illegible-stamp needs_more_info variants), micron decay interpretation (tight system vs. leak vs. moisture), 4-gas meter entry authorization (including a dead-H2S-sensor trap), and two-leg sling trig against WLL and the 30-degree floor. This pattern should be extended before collecting expensive real-world media because it gives perfect labels and catches both visual reading and trade judgment.

## Addendum — Track 3 CPM layer (v2.2)
`scripts/gen_cpm_items.py` implements the field-constraint track from the expansion plan: a CPM engine generates synthetic 18-activity residential schedules with cure lags and inspection holds, renders each as a Gantt image, and computes ground truth exactly. Four families, 28 items: delay quantification (float-absorbed pass vs. critical-path fail; exact day count in `value`), workable-backlog sets (`expected_set` + `workable`, graded by F1), hard-constraint recovery traps (for example drywall-before-inspection and load-before-cure), and illegible-duration needs_more_info variants. Catalog after v2.2: 1,005 items, 84 image-backed, decision mix 947/45/13.

## Addendum — modality-native audio/video categories (v0.1)
`docs/source/modality-native-task-categories-v0.1.md` adds the reduction-test gate for audio-only and video-only items: if a transcript or single frame preserves the answer, the item does not belong in these categories. Audio-native suffixes such as `FD-A`, `CC-A`, and `HAZ-A` cover mechanical fault signatures, process-quality-by-ear, radio communication degradation, and environmental hazard sounds. Video-native suffixes such as `SEQ-V`, `FD-V`, `ME-V`, and `HAZ-V` cover play/wobble/runout tests, procedure execution, dynamic system behavior, progress/rework over time, and rigging/lift dynamics. Schema hooks are now present for `sound_source`, `confidence`, `event_time`, `rate`, `order`, `confusable_with`, and `reduction_test`; the next implementation step is animated video primitives with ground truth by construction.

## Addendum — audio-native layer (v2.3)
`scripts/gen_audio_items.py` delivers the first audio track: 44 fault-signature items across four families — engine idle rhythm (even fire vs. single-cylinder vs. random misfire), bearing condition on a slow conveyor drive (healthy hum vs. early periodic tick vs. severe growl/roughness), panel sound triage (steady 120 Hz magnetic hum = normal vs. irregular broadband crackle = arcing, de-energize), and valve-closure diagnosis (clean stop vs. decaying water-hammer thump train). All signals are DSP-constructed so labels are by construction, and a self-verification pass re-detects labels from rendered audio using onset counts and band-energy ratios before items are written. Catalog after v2.3: 1,049 items; modalities are now text/image/audio; decision mix is 973 fail, 63 pass, 13 needs_more_info. Next per the modality plan: animated video primitives.

## Addendum — scenario restoration and run collection (v2.4)
`scripts/restore_scenarios.py` is now part of the generation path: after v2 source merging and before leakage audit, it repairs placeholder-stripped auto items using `benchmark/items/original_scenarios.json`, stores the restored defect phrase in `defect`, and replaces echo-prone required findings with element-level interpretation vocabulary from `benchmark/items/interpretation_map.json`. Current repair report: 888 repaired, 888 evidence-present, 83 repaired items still partially leaky, 0 missing originals, 0 missing map entries. Full-catalog leakage after audio plus restoration: 874 clean, 175 partial, 0 leaked.

`scripts/collect_run_results.py` adds the missing run-analysis layer: it walks a Harbor runs directory for verifier `reward.json` files, keeps the best trial per task, joins rows to the current catalog, and writes `benchmark/runs/<run>/manifest.json`, `metrics.json`, `analysis.md`, and `catalog.snapshot.json`. The manifest stores the source run directory, full catalog hash, git metadata, collection time, and task count; `benchmark/runs/index.json` and `latest.json` track accumulated runs. Reusing a run name is refused unless `--overwrite` is explicit. `scripts/compare_runs.py` compares two collected runs, warns on catalog-hash mismatch, and reports mean reward deltas, safety-gate changes, axis rollups, largest regressions, and largest improvements.
