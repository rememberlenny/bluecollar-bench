# T4 A-102 Fault diagnosis

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-a-102-fd-fluids-leaks`
- Tier: `T4`
- Discipline: `2.9 Automotive & Powertrain`
- Element: `A-102 Fluids & leaks`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `degraded, failed`

## Scenario

In a T4 work setting, the evaluated element is A-102 Fluids & leaks within 2.9 Automotive & Powertrain. The relevant subcategory is 2.9.1 Engine & Drivetrain. The observed field condition is: leak source identification by color/location (trans red, coolant green/orange, oil...). The work is being assessed at the in-service lifecycle state with source anchors OEM specs.

## Task

Diagnose the most likely fault or failure mode and explain what evidence supports it.

## Required output

Write valid JSON to `/app/answer.json` with this shape:

```json
{
  "decision": "pass | fail | needs_more_info",
  "risk": "low | medium | high | critical",
  "s1_state": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
  "s2_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],
  "findings": ["short defect or hazard finding", "..."],
  "actions": ["immediate corrective action", "..."],
  "rationale": "brief explanation",
  "references": ["code or standard anchors you relied on"]
}
```

Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.

## Source anchors

These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.

- OEM specs
