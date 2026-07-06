# Structural bolting: pretension evidence

You are assessing real trade work the way a competent tradesperson or inspector would.
Read the situation below and write your conclusions to `/app/answer.json`.

## Context

- Setting: a commercial construction project governed by building codes, submittals, and third-party inspections
- Trade: Structural & Ironwork
- Scope under review: Structural bolting
- Your task: decide whether the work complies with the applicable code, specification, or manufacturer requirements
- Stage of the work when observed: `rough-complete` (roughed in — installed or assembled, but not yet closed out)
- Component condition categories that may apply: `installed-defective`, `non-compliant`

## Scenario

A beam splice detail calls for pretensioned A325 bolts. The field photo shows several bolts with head markings that do not match the submitted bolt grade. No turn-of-nut match marks or DTI washer indications are visible. The inspector notes the crew described the joint as 'snug tight only' because the connection looked stable.

## Task

Decide if this connection can be accepted and list what evidence or rework is needed.

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

- RCSC Specification
