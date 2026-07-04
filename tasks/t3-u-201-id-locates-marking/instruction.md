# T3 U-201 Identification

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-u-201-id-locates-marking`
- Tier: `T3`
- Discipline: `2.11 Sitework & Utilities`
- Element: `U-201 Locates & marking`
- Task type: `ID`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`

## Scenario

In a T3 work setting, the evaluated element is U-201 Locates & marking within 2.11 Sitework & Utilities. The relevant subcategory is 2.11.2 Underground Utilities. The observed field condition is: digging without 811 locate. The work is being assessed at the rough-complete lifecycle state with source anchors 811/CGA best practices.

## Task

Identify the component or condition shown, and name the visible defect cues.

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

- 811/CGA best practices
