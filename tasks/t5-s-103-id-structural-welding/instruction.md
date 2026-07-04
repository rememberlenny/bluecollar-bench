# T5 S-103 Identification

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t5-s-103-id-structural-welding`
- Tier: `T5`
- Discipline: `2.4 Structural & Ironwork`
- Element: `S-103 Structural welding`
- Task type: `ID`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`

## Scenario

In a T5 work setting, the evaluated element is S-103 Structural welding within 2.4 Structural & Ironwork. The relevant subcategory is 2.4.1 Steel Erection. The observed field condition is: visible undercut/porosity/incomplete fusion. The work is being assessed at the rough-complete lifecycle state with source anchors AWS D1.1.

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

- AWS D1.1
