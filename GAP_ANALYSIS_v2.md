# Gap Analysis & v2 Upgrade — bluecollar-bench

Reviewed at commit state: 900 tasks, 95 source elements. The Harbor translation is structurally strong (clean item schema, deterministic tasks, coverage matrix honored). The gaps below are about *measurement validity*, which matters more than adding items — three of them let a degenerate policy score highly without any trade knowledge.

## Findings

### 1. Every item's answer is "fail" (critical)
All 900 items had `decision: "fail"` and risk was never `low`. A constant policy — always output fail/critical plus generic "stop work, control hazard, verify" — maxes the decision, actions, and safety-gate metrics with zero domain knowledge. A defect benchmark needs compliant work in the denominator or it measures agreement with the test's mood, not inspection skill.

**Fix shipped:** 21 curated v2 text items, 56 synthetic image-backed v2.1 items, and 28 CPM/Gantt image-backed v2.2 items. Catalog is now 1,005: 947 fail, 45 pass, 13 needs_more_info, with 84 image-backed items. The synthetic slices are healthier than the original corpus, but the overall catalog is still far too fail-heavy — target ≥25–30% pass/nmi. The v2 controls and synthetic media families are the patterns to replicate; text-item rebalance remains priority 1.

### 2. Answer leakage (critical)
11/1,005 items include ≥80% of their `required_findings` tokens verbatim in the scenario text after the current audit (see `benchmark/leakage_report.md`). The original risk remains: auto-generated scenarios can name the defect ("The observed field condition is: isolated metal parts") and hand the agent the code anchors, so echoing the prompt scores the findings metric. The synthetic media items are mostly clean because the decisive evidence is in the image; the text scenario stays generic. The curated seeds show the right text-only style — describe *observations* (green bonding screw installed) and reserve *conclusions* (improper neutral-ground bond) for the grader.

**Fix shipped:** `scripts/leakage_audit.py` tags every item with `leakage_ratio` and writes the report. **Remaining:** rewrite or review the 11 leaked scenarios; that's authoring work (human or LLM-assisted with SME review), not scripting work. The v2 control items model the target style.

### 3. Grader brittleness (high)
- v1 checked `forbidden` tokens against the *entire flattened answer*, so a correct fail rationale containing the word "pass" ("this cannot pass inspection") tripped the gate and halved the reward. Verified empirically.
- Required-finding groups were AND-only exact-token matches ("bonded" ≠ "bonding"), punishing paraphrase.
- `s3_percent` existed in items but was never graded.

**Fix shipped:** `scripts/grade_v2.py` — forbidden scoped to findings/actions/s2 only; optional `findings_mode: any_per_group` for synonym groups; directional gates (`dangerous_false_pass` and `alarmist_false_fail` reported separately — these two numbers are the headline safety metrics for any model you evaluate); S2 empty-set handling for pass items; S3 graded with ±15pt tolerance; numeric `value` graded against `expected_value`/`value_tolerance` for image-backed items; set answers via `expected_set` scored by F1 for workable-backlog questions. `scripts/generate_tasks_v2.py` regenerates all 1,005 tasks with the v2 grader while reusing the v1 render pipeline. Keyword matching remains a ceiling — the endgame is an LLM-judge rubric with these deterministic checks as a floor.

### 4. Coverage imbalances (medium)
From the coverage report: TRD 26 items, PA 35, vs. CC 203 — yet TRD (textbook-vs-field judgment) and PA (progress from partial evidence) are the task types most distinctive to this benchmark's thesis. Backfill items (237) are the thinnest: element context stretched into matrix cells the source trees didn't claim. Suggested targets: TRD ≥80, PA ≥80, with T5 station-progress photos as the PA anchor per the taxonomy notes.

### 5. Synthetic multimodal layer (strategic)
The benchmark is now genuinely multimodal. **v2.1 shipped:** `scripts/gen_media_items.py` renders 56 synthetic instrument/diagram images and emits items whose ground truth is computed from the same parameters that drew the image — zero labeling cost, deterministic answer keys, and a natural decision mix. Four families are included: brake-rotor micrometer vs. stamped minimum, micron-gauge decay tests, confined-space 4-gas screens, and two-leg sling diagrams. Items carry `modality`, `media`, `expected_value`, and `value_tolerance`; generated task metadata preserves those fields and image fixtures are copied into `/app/media/`.

**v2.2 shipped:** `scripts/gen_cpm_items.py` adds Track 3 field-constraint reasoning. It renders 28 residential CPM/Gantt chart items with cure lags and inspection holds as hard constraints, covering delay quantification, workable backlog, recovery traps, and illegible-duration needs_more_info variants. New task type: `RES`.

## Priority order
1. Rebalance decisions (extend v2 control pattern to ~250 pass/nmi items)
2. De-leak the 11 flagged scenarios (observation-style rewrites)
3. Adopt grade_v2 everywhere (done via generate_tasks_v2) and track the two directional gates as headline metrics
4. Extend synthetic media families: psychrometric calculators, dial indicators, torque/spec-plate comparisons, panel schedules, P&ID excerpts, and photo-realistic variants seeded from synthetic parameters
5. SME red-team pass on code refs (still open from taxonomy v0.1)

## Files in this delta
- `benchmark/items/control_items_v2.json` — 21 curated items (pass / nmi / trap / trd)
- `benchmark/items/media_items_v2.json` — 56 synthetic image-backed items
- `benchmark/items/cpm_items_v2.json` — 28 CPM/Gantt image-backed RES items
- `benchmark/media/` — generated PNG fixtures used by the image-backed tasks
- `benchmark/items/items.json` — merged catalog (1,005), tagged with `leakage_ratio`
- `benchmark/leakage_report.md` — audit output
- `scripts/gen_media_items.py` — deterministic synthetic media renderer
- `scripts/gen_cpm_items.py` — deterministic CPM schedule/item renderer
- `scripts/grade_v2.py` — upgraded verifier (tested: good-fail=1.0, dangerous false pass=0.0, alarmist false fail=0.0, numeric value in tolerance=1.0, numeric value out of tolerance loses the numeric component)
- `scripts/generate_tasks_v2.py` — merge controls, media items, and CPM items; tag leakage; normalize modality/media; copy image fixtures; and regenerate with v2 grader
- `scripts/leakage_audit.py` — leakage tagging/report
- Regenerate tasks after pulling: `make generate`

## Addendum — synthetic multimodal layer (v2.1)
`scripts/gen_media_items.py` renders instrument images with matplotlib and emits items whose ground truth is computed from the same parameters that drew the image. The four current families test different skills: rotor micrometer reading against a stamped minimum (including illegible-stamp needs_more_info variants), micron decay interpretation (tight system vs. leak vs. moisture), 4-gas meter entry authorization (including a dead-H2S-sensor trap), and two-leg sling trig against WLL and the 30-degree floor. This pattern should be extended before collecting expensive real-world media because it gives perfect labels and catches both visual reading and trade judgment.

## Addendum — Track 3 CPM layer (v2.2)
`scripts/gen_cpm_items.py` implements the field-constraint track from the expansion plan: a CPM engine generates synthetic 18-activity residential schedules with cure lags and inspection holds, renders each as a Gantt image, and computes ground truth exactly. Four families, 28 items: delay quantification (float-absorbed pass vs. critical-path fail; exact day count in `value`), workable-backlog sets (`expected_set` + `workable`, graded by F1), hard-constraint recovery traps (for example drywall-before-inspection and load-before-cure), and illegible-duration needs_more_info variants. Catalog: 1,005 items, 84 image-backed, decision mix 947/45/13.
