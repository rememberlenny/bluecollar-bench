# T5 P-104 Procedure sequencing coverage backfill

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t5-p-104-seq-bf-003-pressure-testing`
- Tier: `T5`
- Discipline: `2.2 Mechanical - Piping & Plumbing`
- Element: `P-104 Pressure testing`
- Task type: `SEQ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective`

## Scenario

In a T5 work setting, the evaluated element is P-104 Pressure testing within 2.2 Mechanical - Piping & Plumbing. The relevant subcategory is 2.2.1 Process Piping (T1/T2). The observed field condition is: pneumatic test without exclusion zone. The work is being assessed at the in-progress lifecycle state with source anchors ASME B31.3 §345. This item is a coverage backfill for a secondary taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

## Task

Evaluate the procedure sequence and state what must happen before work can continue.

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

- ASME B31.3 §345
