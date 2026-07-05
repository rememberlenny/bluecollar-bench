# T5 B-102 Identification

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t5-b-102-id-production-welding`
- Tier: `T5`
- Discipline: `2.10 Assembly & Fabrication`
- Element: `B-102 Production welding`
- Task type: `ID`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T5 work setting, the evaluated element is B-102 Production welding within 2.10 Assembly & Fabrication. The relevant subcategory is 2.10.1 Fastening & Joining. The field notes describe visible cues consistent with: visible cue/visible cue visible cue. The work is being assessed at the rough-complete lifecycle state with source anchors AWS D1.1/D1.3, shop WPS.

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

- AWS D1.1/D1.3
- shop WPS
