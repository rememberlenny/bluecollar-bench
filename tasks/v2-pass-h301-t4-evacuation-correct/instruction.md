# T4 H-301 Compliant brazing and evacuation (control)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-pass-h301-t4-evacuation-correct`
- Tier: `T4`
- Discipline: `2.3 HVAC-R`
- Element: `H-301 Brazing & evacuation`
- Task type: `SEQ`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A line-set replacement is documented with photos: a nitrogen regulator connected and flowing during each braze, Schrader cores removed and set aside before evacuation, and a micron gauge at the far port reading 320 microns. The tech's log shows the system isolated from the pump and holding below 500 microns for fifteen minutes before charging began.

## Task

Evaluate whether the documented procedure was performed correctly and in the right order.

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

- EPA 608
- mfr specs
