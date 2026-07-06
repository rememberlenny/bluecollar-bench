# Shaft alignment review (industrial site)

You are assessing real trade work the way a competent tradesperson or inspector would.
Read the situation below and write your conclusions to `/app/answer.json`.

## Context

- Setting: a heavy-industrial construction or process site where work follows engineered drawings, specifications, and permits
- Trade: Equipment & Machinery
- Scope under review: Shaft alignment
- Your task: check the order of the work and catch any sequence violation
- Stage of the work when observed: `tested/inspected` (through its testing or inspection step)
- Component condition categories that may apply: none flagged — judge from the evidence

## Scenario

A pump-motor alignment record shows soft foot checked and corrected to 0.001 inch at each foot, final laser alignment performed after the suction and discharge flanges were bolted up, and the as-left readings within the 1800-rpm tolerance table posted on the job card. Cold offsets for hot service were applied per the OEM growth chart.

## Task

Evaluate whether the alignment procedure was sequenced and completed correctly.

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

- API RP 686
