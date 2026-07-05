# T2 S-102 Compliant structural bolting (control)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-pass-s102-t2-bolting-correct`
- Tier: `T2`
- Discipline: `2.4 Structural & Ironwork`
- Element: `S-102 Structural bolting`
- Task type: `CC`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A moment connection specified as pretensioned is inspected. Bolt heads show F3125 Grade A325 markings matching the drawing callout. Every DTI washer's silicone squirts are fully extruded at all bumps. Match marks made at snug-tight show consistent nut rotation across the connection. No thread run-out sits in the shear plane at the visible bolts.

## Task

Determine whether this connection meets the specified pretension requirements. Cite the visible evidence.

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

- RCSC Specification
