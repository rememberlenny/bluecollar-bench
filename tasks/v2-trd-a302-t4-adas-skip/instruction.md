# T4 A-302 Skipped ADAS calibration (judgment)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-trd-a302-t4-adas-skip`
- Tier: `T4`
- Discipline: `2.9 Automotive & Powertrain`
- Element: `A-302 ADAS & post-repair calibration`
- Task type: `TRD`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `non-compliant`
- Modality: `text`

## Scenario

A windshield with a forward-facing camera bracket was replaced. The glass installer road-tested the vehicle, confirmed no dash warnings, and released it, noting the shop lacks calibration targets and the customer declined a dealer visit. The OEM procedure for this model specifies a static target calibration after glass replacement.

## Task

Judge whether releasing this vehicle was acceptable. Weigh the absence of warning lights against the OEM requirement, and state the correct disposition.

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

- OEM position statements
