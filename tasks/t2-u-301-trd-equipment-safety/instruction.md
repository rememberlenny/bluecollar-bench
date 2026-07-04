# T2 U-301 Tradeoff judgment

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t2-u-301-trd-equipment-safety`
- Tier: `T2`
- Discipline: `2.11 Sitework & Utilities`
- Element: `U-301 Equipment safety`
- Task type: `TRD`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective, non-compliant`

## Scenario

In a T2 work setting, the evaluated element is U-301 Equipment safety within 2.11 Sitework & Utilities. The relevant subcategory is 2.11.3 Heavy Equipment Operation. The observed field condition is: no spotter while backing near trench. The work is being assessed at the in-progress lifecycle state with source anchors OSHA 1926 Subpart O.

## Task

Resolve the field tradeoff: distinguish common shortcuts from acceptable journeyman practice.

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

- OSHA 1926 Subpart O
