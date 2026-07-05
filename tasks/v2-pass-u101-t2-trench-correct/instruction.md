# T2 U-101 Compliant trench protection (control)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-pass-u101-t2-trench-correct`
- Tier: `T2`
- Discipline: `2.11 Sitework & Utilities`
- Element: `U-101 Trench protection`
- Task type: `HAZ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A 6-foot-deep utility trench has workers inside a trench shield whose certification plate and tabulated data are visible. Shield walls extend above grade, the spoil pile sits roughly four feet back from the edge, and an extension ladder inside the shield extends three rungs above grade about ten feet from the workers. A competent-person daily inspection log dated today is shown.

## Task

Identify any hazards requiring immediate control, or confirm the protective system is adequate as observed.

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

- OSHA 1926 Subpart P
