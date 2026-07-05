# T3 E-302 Hazard spotting

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-e-302-haz-nm-mc-cable-routing-protection`
- Tier: `T3`
- Discipline: `2.1 Electrical`
- Element: `E-302 NM/MC cable routing & protection`
- Task type: `HAZ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T3 work setting, the evaluated element is E-302 NM/MC cable routing & protection within 2.1 Electrical. The relevant subcategory is 2.1.3 Wire & Cable. The field notes describe visible cues consistent with: not held at the expected intervals visible cue. The work is being assessed at the in-progress lifecycle state with source anchors NEC 300.4, 334, 330.

## Task

Identify the safety hazards, their severity, and the immediate controls required.

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

- NEC 300.4
- 334
- 330
