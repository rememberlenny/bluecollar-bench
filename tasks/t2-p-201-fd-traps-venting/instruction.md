# T2 P-201 Fault diagnosis

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t2-p-201-fd-traps-venting`
- Tier: `T2`
- Discipline: `2.2 Mechanical - Piping & Plumbing`
- Element: `P-201 Traps & venting`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `degraded, failed`

## Scenario

In a T2 work setting, the evaluated element is P-201 Traps & venting within 2.2 Mechanical - Piping & Plumbing. The relevant subcategory is 2.2.2 Plumbing - DWV (T2/T3). The observed field condition is: missing cleanout. The work is being assessed at the in-service lifecycle state with source anchors IPC/UPC.

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

- IPC/UPC
