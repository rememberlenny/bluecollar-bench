# T4 M-201 Fault diagnosis coverage backfill

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-m-201-fd-bf-001-shaft-alignment`
- Tier: `T4`
- Discipline: `2.7 Equipment & Machinery`
- Element: `M-201 Shaft alignment`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `degraded, failed`
- Modality: `text`

## Scenario

In a T4 work setting, the evaluated element is M-201 Shaft alignment within 2.7 Equipment & Machinery. The relevant subcategory is 2.7.2 Alignment. The field notes describe visible cues consistent with: visible cue visible cue visible cue ignored on hot service. The work is being assessed at the in-service lifecycle state with source anchors API 686, laser system manuals. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

## Task

Diagnose the most likely fault or failure mode and explain what evidence supports it.

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

- API 686
- laser system manuals
