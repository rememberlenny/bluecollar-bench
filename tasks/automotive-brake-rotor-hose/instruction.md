# Brake service: rotor and hose defects

You are assessing real trade work the way a competent tradesperson or inspector would.
Read the situation below and write your conclusions to `/app/answer.json`.

## Context

- Setting: a field-service visit to an installed, operating asset, working from symptoms, the work order, and OEM service information
- Trade: Automotive
- Scope under review: Brakes
- Your task: diagnose the most likely fault from the evidence
- Stage of the work when observed: `tested/inspected` (through its testing or inspection step)
- Component condition categories that may apply: `degraded`, `installed-defective`

## Scenario

After a front brake job, the left rotor measures 23.4 mm with a stamped minimum thickness of 24.0 mm. The caliper hose makes a half twist between the hard line and caliper when the wheels are straight. The pads are new and the pedal feels firm during a short parking-lot test.

## Task

Decide if the repair passes quality control and list the defects that matter.

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

- OEM specs
