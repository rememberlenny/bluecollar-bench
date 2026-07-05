# T2 C-301 Light efflorescence (alarmist trap)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-trap-c301-t2-efflorescence`
- Tier: `T2`
- Discipline: `2.5 Concrete & Masonry`
- Element: `C-301 Block/brick laying`
- Task type: `ID`
- Expected lifecycle state to assess: `accepted`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

Three months after completion, a new CMU veneer shows a light white powdery haze across several courses after a wet winter. Joints are tooled concave and intact, weep holes at the bottom course are open and unobstructed, and interior humidity readings behind the wall are normal.

## Task

Identify this condition and determine whether corrective masonry work is warranted.

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

- BIA tech notes
