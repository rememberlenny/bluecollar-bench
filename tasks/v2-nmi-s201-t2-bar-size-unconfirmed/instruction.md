# T2 S-201 Rebar size not confirmable

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-nmi-s201-t2-bar-size-unconfirmed`
- Tier: `T2`
- Discipline: `2.4 Structural & Ironwork`
- Element: `S-201 Rebar placement`
- Task type: `ME`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A pre-pour photo of a grade beam shows bars on chairs with consistent spacing and clear cover to the forms. The photo is taken from too far away to read bar deformation patterns or count ribs, and the placing drawings specify different bar sizes for the top and bottom mats. No scale reference is in frame.

## Task

Can bar size compliance be confirmed from this evidence? State what measurement or reference is needed.

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

- ACI 117
- placing drawings
