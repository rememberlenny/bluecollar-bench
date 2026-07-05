# T4 X-105 Identification coverage backfill

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-x-105-id-bf-004-ppe-selection`
- Tier: `T4`
- Discipline: `2.12 Safety & Rigging`
- Element: `X-105 PPE selection`
- Task type: `ID`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T4 work setting, the evaluated element is X-105 PPE selection within 2.12 Safety & Rigging. The relevant subcategory is 2.10.4 Quality Inspection. The field notes describe visible cues consistent with: arc-visible cue visible cue visible cue task category (label vs. clothing - DOC+ID). The work is being assessed at the rough-complete lifecycle state with source anchors NFPA 70E, OSHA 1910 Subpart I. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

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

- NFPA 70E
- OSHA 1910 Subpart I
