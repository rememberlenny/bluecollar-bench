# Furnace installation: venting and return-air hazards

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `hvac-furnace-venting-garage-return`
- Tier: `T3`
- Discipline: `2.3 HVAC-R`
- Element: `H-102 Furnace & venting`
- Task type: `HAZ`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

A gas furnace is installed in a closet that opens to an attached garage. The return-air grille is cut into the garage-facing wall. The single-wall metal vent connector passes within about one inch of exposed wood framing. The condensate tube from the coil runs upward for several inches before dropping to a floor drain.

## Task

Identify the safety and compliance issues and state whether the system should remain in service.

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

- IRC M1801
- NFPA 54
- H-102
