# T1 H-101 Code/spec compliance coverage backfill

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t1-h-101-cc-bf-000-condenser-heat-pump-sett`
- Tier: `T1`
- Discipline: `2.3 HVAC-R`
- Element: `H-101 Condenser/heat pump setting`
- Task type: `CC`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T1 work setting, the evaluated element is H-101 Condenser/heat pump setting within 2.3 HVAC-R. The relevant subcategory is 2.3.1 Equipment Installation. The observed field condition is: clearance to wall/other units below mfr minimum. The work is being assessed at the rough-complete lifecycle state with source anchors mfr install manual, IMC/IRC M1401. This item is a coverage backfill for a secondary taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

## Task

Determine whether the work meets the applicable code, spec, drawing, or manufacturer requirement.

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

- mfr install manual
- IMC/IRC M1401
