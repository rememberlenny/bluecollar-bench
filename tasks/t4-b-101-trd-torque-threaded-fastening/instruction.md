# T4 B-101 Tradeoff judgment

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-b-101-trd-torque-threaded-fastening`
- Tier: `T4`
- Discipline: `2.10 Assembly & Fabrication`
- Element: `B-101 Torque & threaded fastening`
- Task type: `TRD`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T4 work setting, the evaluated element is B-101 Torque & threaded fastening within 2.10 Assembly & Fabrication. The relevant subcategory is 2.10.1 Fastening & Joining. The field notes describe visible cues consistent with: visible cue visible cue visible cue upside down/uncalibrated. The work is being assessed at the in-progress lifecycle state with source anchors OEM/engineering specs.

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

- OEM/engineering specs
