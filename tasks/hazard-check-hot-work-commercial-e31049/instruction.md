# Hazard check: Hot work (commercial project)

You are assessing real trade work the way a competent tradesperson or inspector would.
Read the situation below and write your conclusions to `/app/answer.json`.

## Context

- Setting: a commercial construction project governed by building codes, submittals, and third-party inspections
- Trade: Safety & Rigging
- Scope under review: Hot work
- Your task: spot the unsafe conditions and state the immediate controls required
- Stage of the work when observed: `in-progress` (actively in progress)
- Component condition categories that may apply: `installed-defective`, `non-compliant`

## Scenario

You are on a commercial construction project governed by building codes, submittals, and third-party inspections. The work under review is Hot work, part of the Safety & Rigging scope. The observed field condition is: combustibles within radius uncovered. The work is actively in progress. Reference material on hand: NFPA 51B, OSHA 1926 Subpart J.

## Task

Identify the safety hazards, their severity, and the immediate controls required.

## Required output

Write valid JSON to `/app/answer.json` with this shape:

```json
{
  "decision": "pass | fail | needs_more_info",
  "risk": "low | medium | high | critical",
  "work_stage": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
  "component_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],
  "percent_complete": 0,
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
`work_stage` is how far the work has progressed; `percent_complete` is your numeric estimate of overall progress.
`component_conditions` lists the condition categories that apply to the component; use an empty list if none apply.
Use `value` for the numeric reading or computed quantity when the task asks for one.
Use `sound_source`, `event_time`, `rate`, and `order` for audio/video-native tasks when requested.
Use `workable` for a list of activity IDs when the task asks what work can still start.

## Reference material

Apply these to the scenario rather than quoting them mechanically.

- NFPA 51B
- OSHA 1926 Subpart J
