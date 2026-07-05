# Rebar placement: cover and support

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `rebar-slab-cover-chairs`
- Tier: `T2`
- Discipline: `2.4 Structural & Ironwork`
- Element: `S-201 Rebar placement`
- Task type: `PA`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

A pre-pour photo shows a slab mat with reinforcing bars resting directly on the vapor barrier and soil in multiple areas. Chairs are missing along the near edge, and several bars are touching the side form. The placement drawing requires continuous bottom cover and lap splices are otherwise visible.

## Task

Assess readiness for concrete placement, identify the defects, and estimate the lifecycle state.

## Required output

Write valid JSON to `/app/answer.json` with this shape:

```json
{
  "decision": "pass | fail | needs_more_info",
  "risk": "low | medium | high | critical",
  "s1_state": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
  "s2_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],
  "s3_percent": 0,
  "value": 0,
  "workable": ["activity ID", "..."],
  "findings": ["short defect or hazard finding", "..."],
  "actions": ["immediate corrective action", "..."],
  "rationale": "brief explanation",
  "references": ["code or standard anchors you relied on"]
}
```

Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.
Use `value` for the numeric reading or computed quantity when the task asks for one.
Use `workable` for a list of activity IDs when the task asks what work can still start.

## Source anchors

These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.

- ACI 318
- placing drawings
- S-201
