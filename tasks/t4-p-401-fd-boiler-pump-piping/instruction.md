# T4 P-401 Fault diagnosis

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-p-401-fd-boiler-pump-piping`
- Tier: `T4`
- Discipline: `2.2 Mechanical - Piping & Plumbing`
- Element: `P-401 Boiler & pump piping`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `degraded, failed`
- Modality: `text`

## Scenario

In a T4 work setting, the evaluated element is P-401 Boiler & pump piping within 2.2 Mechanical - Piping & Plumbing. The relevant subcategory is 2.2.4 Hydronic & Steam. The observed field condition is: pump pumping toward expansion tank (point-of-no-pressure-change violated). The work is being assessed at the in-service lifecycle state with source anchors mfr manuals, hydronics references.

## Task

Diagnose the most likely fault or failure mode and explain what evidence supports it.

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

- mfr manuals
- hydronics references
