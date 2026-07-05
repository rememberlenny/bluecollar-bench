# Repo Evaluation — post-merge, post-Codex-run (v2.4 delta)

## What's healthy
grade_v2 is live in all 1,049 tasks; CPM/media/control/audio items are merged; reference solutions validate per-decision and per-modality. A prior GPT-5 suite run completed and validated before these catalog repairs, but it cannot be treated as the current scoreboard.

## Finding 1 — CRITICAL: 888 scenarios were evidence-stripped
During the v2 merge, auto-item defect text was replaced with the placeholder "visible cue visible cue visible cue". Leakage_ratio went to 0 because the *evidence* was deleted, not because grading was fixed: graders still required defect-specific tokens the scenario no longer contained. 88% of the catalog became label-guessing from metadata (element name + task type), rewarding memorization of the item bank and punishing honest needs-more-info reasoning.

**Fixed in this delta** (`scripts/restore_scenarios.py` + `benchmark/items/original_scenarios.json` + `benchmark/items/interpretation_map.json`): original observations restored (the defect phrase IS the observable evidence), and required_findings re-keyed to element-level interpretation vocabulary — consequence and code-concept terms a competent answer supplies but the scenario doesn't contain. Every repaired item now verifies `evidence_present`; full-catalog leakage is 0 leaked / 175 partial / 874 clean after the audio layer is included. Among repaired auto items, 83 remain partial (element-name overlap; flagged). The `defect` field preserves ground truth for SME review and future LLM-judge rubrics. Interpretation vocab is element-level v1 — defect-level refinement is the SME follow-up.

## Finding 2 — The $34 run's measurements were discarded
`benchmark/runs/*` retains job counts and cost only; no per-task rewards. Nothing psychometric — saturation, discrimination, per-axis rollups, whether the constant-fail exploit paid, safety-gate rates — is recoverable. Additionally, the run predates the placeholder merge, so its task content differs from HEAD; results aren't reproducible against the current tree and nothing records that.

**Fixed forward** (`scripts/collect_run_results.py`): walks a Harbor runs dir for verifier reward.json files, keeps best trial per task, joins with the catalog, and emits a versioned `benchmark/runs/<run>/` directory with `manifest.json`, `metrics.json`, `analysis.md`, and `catalog.snapshot.json`. `scripts/compare_runs.py` compares collected runs and warns when catalog hashes differ. Re-running the suite post-repair through this collector is the highest-value next spend — the repaired catalog invalidates the old run anyway.

## Finding 3 — Run flakiness burned ~40% of spend
203 superseded exception files and jobs with 100+ errored/cancelled trials suggest timeouts/infra retries consumed a large cost share. Worth capturing agent timeout settings and per-trial wall time in the run record (collector will retain whatever the verifier logs).

## Recommended order
1. Re-run the suite on the repaired 1,049-task catalog.
2. Collect the run through `scripts/collect_run_results.py` — first real scoreboard, including the two safety-gate headline numbers.
3. SME-red-team the interpretation vocabulary and defect attributions, especially the 83 repaired auto items still in the partial-leak bucket.
4. Continue the standing priorities: decision rebalance (~250 pass/nmi) and a held-out split before any public announcement.
