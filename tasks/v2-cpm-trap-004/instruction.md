# T2 RES Field constraint: trap (image)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-cpm-trap-004`
- Tier: `T2`
- Discipline: `2.6 Carpentry & Finishes`
- Element: `RES Schedule & constraint reasoning`
- Task type: `RES`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `non-compliant`
- Modality: `image`

## Scenario

The image shows the schedule and a proposed schedule-recovery plan in the note. Hard constraints are marked in the legend: cure lags cannot be compressed and inspection holds cannot be bypassed.

## Media

- `/app/media/cpm_trap_004.png` (image)

## Task

Evaluate the proposed recovery plan. Approve it or reject it, and explain which constraint, if any, it violates.

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
  "sound_source": "component or source of the sound, when asked",
  "confidence": 0.0,
  "event_time": 0.0,
  "rate": 0.0,
  "order": ["step-id", "..."],
  "workable": ["activity ID", "..."],
  "findings": ["short defect or hazard finding", "..."],
  "actions": ["immediate corrective action", "..."],
  "rationale": "brief explanation",
  "references": ["code or standard anchors you relied on"]
}
```

Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.
Use `value` for the numeric reading or computed quantity when the task asks for one.
Use `sound_source`, `event_time`, `rate`, and `order` for audio/video-native tasks when requested.
Use `workable` for a list of activity IDs when the task asks what work can still start.

## Source anchors

These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.

- CPM computed ground truth
- expansion-plan track 3
