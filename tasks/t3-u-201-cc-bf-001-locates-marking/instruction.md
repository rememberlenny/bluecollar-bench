# T3 U-201 Code/spec compliance coverage backfill

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-u-201-cc-bf-001-locates-marking`
- Tier: `T3`
- Discipline: `2.11 Sitework & Utilities`
- Element: `U-201 Locates & marking`
- Task type: `CC`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective, non-compliant`

## Scenario

In a T3 work setting, the evaluated element is U-201 Locates & marking within 2.11 Sitework & Utilities. The relevant subcategory is 2.11.2 Underground Utilities. The observed field condition is: misreading mark colors (red=electric, yellow=gas, blue=water, green=sewer, orange=comm - pure ID item). The work is being assessed at the rough-complete lifecycle state with source anchors 811/CGA best practices. This item is a coverage backfill for a secondary taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

## Task

Determine whether the work meets the applicable code, spec, drawing, or manufacturer requirement.

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
