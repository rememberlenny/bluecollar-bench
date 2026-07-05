# T1 E-801 Tool & material selection

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t1-e-801-ts-classified-area-wiring-methods`
- Tier: `T1`
- Discipline: `2.1 Electrical`
- Element: `E-801 Classified-area wiring methods`
- Task type: `TS`
- Expected lifecycle state to assess: `staged`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T1 work setting, the evaluated element is E-801 Classified-area wiring methods within 2.1 Electrical. The relevant subcategory is 2.1.8 Hazardous Locations (T1 overlay). The field notes describe visible cues consistent with: non-visible cue visible cue in visible cue I Div 2. The work is being assessed at the staged lifecycle state with source anchors NEC 500-516.

## Task

Select the correct tool, material, or replacement approach and explain why the observed choice is wrong.

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

- NEC 500-516
