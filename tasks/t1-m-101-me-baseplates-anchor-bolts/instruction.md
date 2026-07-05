# T1 M-101 Measurement & estimation

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t1-m-101-me-baseplates-anchor-bolts`
- Tier: `T1`
- Discipline: `2.7 Equipment & Machinery`
- Element: `M-101 Baseplates & anchor bolts`
- Task type: `ME`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T1 work setting, the evaluated element is M-101 Baseplates & anchor bolts within 2.7 Equipment & Machinery. The relevant subcategory is 2.7.1 Setting & Grouting. The field notes describe visible cues consistent with: visible cue without visible cue visible cue (voids - sounding test). The work is being assessed at the rough-complete lifecycle state with source anchors API RP 686. The measurable cue is visible enough to estimate whether the condition is within tolerance.

## Task

Estimate or interpret the measurable condition and state why it is out of tolerance.

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

- API RP 686
