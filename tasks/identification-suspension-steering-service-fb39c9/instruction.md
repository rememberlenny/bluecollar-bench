# Identification: Suspension & steering (service call)

You are assessing real trade work the way a competent tradesperson or inspector would.
Read the situation below and write your conclusions to `/app/answer.json`.

## Context

- Setting: a field-service visit to an installed, operating asset, working from symptoms, the work order, and OEM service information
- Trade: Automotive & Powertrain
- Scope under review: Suspension & steering
- Your task: identify the component, material, or condition involved
- Stage of the work when observed: `rough-complete` (roughed in — installed or assembled, but not yet closed out)
- Component condition categories that may apply: `installed-defective`

## Scenario

You are on a field-service visit to an installed, operating asset, working from symptoms, the work order, and OEM service information. The work under review is Suspension & steering, part of the Automotive & Powertrain scope. The observed field condition is: tire wear pattern diagnosis (inner edge = camber/toe, cupping = dampers - premier ID/FD). The work is roughed in — installed or assembled, but not yet closed out. Reference material on hand: OEM, alignment specs.

## Task

Identify the component or condition shown, and name the visible defect cues.

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

- OEM
- alignment specs
