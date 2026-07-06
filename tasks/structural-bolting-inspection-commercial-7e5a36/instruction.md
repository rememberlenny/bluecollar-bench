# Structural bolting inspection (commercial project)

You are assessing real trade work the way a competent tradesperson or inspector would.
Read the situation below and write your conclusions to `/app/answer.json`.

## Context

- Setting: a commercial construction project governed by building codes, submittals, and third-party inspections
- Trade: Structural & Ironwork
- Scope under review: Structural bolting
- Your task: decide whether the work complies with the applicable code, specification, or manufacturer requirements
- Stage of the work when observed: `tested/inspected` (through its testing or inspection step)
- Component condition categories that may apply: none flagged — judge from the evidence

## Scenario

A moment connection specified as pretensioned is inspected. Bolt heads show F3125 Grade A325 markings matching the drawing callout. Every DTI washer's silicone squirts are fully extruded at all bumps. Match marks made at snug-tight show consistent nut rotation across the connection. No thread run-out sits in the shear plane at the visible bolts.

## Task

Determine whether this connection meets the specified pretension requirements. Cite the visible evidence.

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
