# T4 A-102 Valve cover seep (alarmist trap)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-trap-a102-t4-oil-seep`
- Tier: `T4`
- Discipline: `2.9 Automotive & Powertrain`
- Element: `A-102 Fluids & leaks`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `worn`
- Modality: `text`

## Scenario

During an oil change on a 140,000-mile vehicle, the tech photographs slight dampness with dust accumulation along the lower edge of the valve cover gasket. There are no drips on the undertray or the ground, oil level is at the full mark, and the customer reports no oil consumption between changes.

## Task

Assess this observation and recommend an appropriate disposition for the customer.

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
