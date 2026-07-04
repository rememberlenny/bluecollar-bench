# T5 M-302 Fault diagnosis

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t5-m-302-fd-belts-sheaves-couplings`
- Tier: `T5`
- Discipline: `2.7 Equipment & Machinery`
- Element: `M-302 Belts, sheaves & couplings`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `degraded, failed`

## Scenario

In a T5 work setting, the evaluated element is M-302 Belts, sheaves & couplings within 2.7 Equipment & Machinery. The relevant subcategory is 2.7.3 Rotating Equipment. The observed field condition is: mixed old/new belts on multi-groove. The work is being assessed at the in-service lifecycle state with source anchors mfr guides.

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

- mfr guides
