# T1 X-103 Document interpretation (image)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-media-gasmeter-003`
- Tier: `T1`
- Discipline: `2.12 Safety & Rigging`
- Element: `X-103 Confined space`
- Task type: `DOC`
- Expected lifecycle state to assess: `planned`
- Relevant S2 condition classes: `none`
- Modality: `image`

## Scenario

The image shows the pre-entry atmospheric test screen from a 4-gas monitor at a permit-required confined space.

## Media

- `/app/media/gasmeter_003.png` (image)

## Task

Read all four channels from the image and determine whether entry can be authorized. Identify any reading outside acceptable entry limits.

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

- OSHA 1910.146
