# T3 E-303 Backstabbed receptacles (judgment)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-trd-e303-t3-backstab`
- Tier: `T3`
- Discipline: `2.1 Electrical`
- Element: `E-303 Terminations & splices`
- Task type: `TRD`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A living-room circuit uses receptacles wired via push-in backstab connections with 14 AWG solid copper on a 15 A circuit, consistent with the device listing. The homeowner asks whether the work must be redone. Local amendments add nothing beyond the model code.

## Task

Give the inspection decision, then explain the difference between what the code permits here and what experienced electricians typically prefer, and why.

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

- NEC 110.14
- device listings
