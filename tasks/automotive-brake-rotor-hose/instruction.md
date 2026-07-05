# Brake service: rotor and hose defects

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `automotive-brake-rotor-hose`
- Tier: `T4`
- Discipline: `2.9 Automotive`
- Element: `A-201 Brakes`
- Task type: `FD`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `degraded, installed-defective`
- Modality: `text`

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
  "s1_state": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
  "s2_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],
  "s3_percent": 0,
  "value": 0,
  "workable": ["activity ID", "..."],
  "findings": ["short defect or hazard finding", "..."],
  "actions": ["immediate corrective action", "..."],
  "rationale": "brief explanation",
  "references": ["code or standard anchors you relied on"]
}
```

Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.
Use `value` for the numeric reading or computed quantity when the task asks for one.
Use `workable` for a list of activity IDs when the task asks what work can still start.

## Source anchors

These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.

- OEM specs
- A-201
