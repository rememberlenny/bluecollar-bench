# T4 M-301 Identification

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-m-301-id-bearings-seals`
- Tier: `T4`
- Discipline: `2.7 Equipment & Machinery`
- Element: `M-301 Bearings & seals`
- Task type: `ID`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T4 work setting, the evaluated element is M-301 Bearings & seals within 2.7 Equipment & Machinery. The relevant subcategory is 2.7.3 Rotating Equipment. The field notes describe visible cues consistent with: visible cue during visible cue (visible cue - ID). The work is being assessed at the rough-complete lifecycle state with source anchors SKF/Timken mounting guides.

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

- SKF/Timken mounting guides
