# T2 E-102 Compliant Progress assessment

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-text-pass-pa-t2-e-102-032`
- Tier: `T2`
- Discipline: `2.1 Electrical`
- Element: `E-102 Panelboard installation & makeup`
- Task type: `PA`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

Progress photos for E-102 Panelboard installation & makeup show the current checkpoint scope finished for this area. The remaining visible work is cleanup, labeling, or follow-on finish work outside the checkpoint being scored. Source anchors for review: NEC Art. 408, 110.26 (working clearance), 200.4.

## Task

Evaluate the described field condition and return the appropriate decision with supporting observations.

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

- NEC Art. 408
- 110.26 (working clearance)
- 200.4
