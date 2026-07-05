# T2 RES Field constraint: nmi (image)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-cpm-nmi-002`
- Tier: `T2`
- Discipline: `2.6 Carpentry & Finishes`
- Element: `RES Schedule & constraint reasoning`
- Task type: `RES`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `none`
- Modality: `image`

## Scenario

The image shows the lookahead schedule, but one duration is illegible, and a disruption affects that same activity.

## Media

- `/app/media/cpm_nmi_002.png` (image)

## Task

Determine the project delay caused by the disruption, or state precisely what information is missing and what you need to compute it.

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

- CPM computed ground truth
- expansion-plan track 3
