# T3 E-601 Code/spec compliance

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-e-601-cc-grounding-electrode-system`
- Tier: `T3`
- Discipline: `2.1 Electrical`
- Element: `E-601 Grounding electrode system`
- Task type: `CC`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T3 work setting, the evaluated element is E-601 Grounding electrode system within 2.1 Electrical. The relevant subcategory is 2.1.6 Grounding & Bonding. The field notes describe visible cues consistent with: not present where expected visible cue electrode. The work is being assessed at the rough-complete lifecycle state with source anchors NEC 250.50-250.68.

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

- NEC 250.50-250.68
