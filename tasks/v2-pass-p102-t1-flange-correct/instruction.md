# T1 P-102 Compliant flanged joint (control)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-pass-p102-t1-flange-correct`
- Tier: `T1`
- Discipline: `2.2 Mechanical - Piping & Plumbing`
- Element: `P-102 Flanged joints`
- Task type: `CC`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A 6-inch Class 150 flanged joint is inspected after bolt-up. All eight studs are installed with hardened washers, torque witness lines are marked across every nut, and stud ends project one to three threads past each nut. The gasket visible at the joint edge matches the spiral-wound type called out on the line class sheet. The torque record sheet shows a completed star-pattern sequence in three passes.

## Task

Assess this joint against the bolted-joint assembly requirements. Cite the observations supporting your decision.

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

- ASME PCC-1
- ASME B16.5
