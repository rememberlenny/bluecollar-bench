# T4 A-201 Measurement & estimation (image)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-media-rotor-011`
- Tier: `T4`
- Discipline: `2.9 Automotive & Powertrain`
- Element: `A-201 Brakes`
- Task type: `ME`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `worn`
- Modality: `image`

## Scenario

The image shows a digital micrometer reading taken on a front brake rotor and the specification stamp on the rotor hat.

## Media

- `/app/media/rotor_011.png` (image)

## Task

Read the measurement and the stamped minimum from the image. Report the measured thickness in the `value` field (mm) and decide whether the rotor may remain in service.

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

- OEM specs
