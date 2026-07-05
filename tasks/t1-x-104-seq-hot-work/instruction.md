# T1 X-104 Procedure sequencing

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t1-x-104-seq-hot-work`
- Tier: `T1`
- Discipline: `2.12 Safety & Rigging`
- Element: `X-104 Hot work`
- Task type: `SEQ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T1 work setting, the evaluated element is X-104 Hot work within 2.12 Safety & Rigging. The relevant subcategory is 2.10.4 Quality Inspection. The field notes describe visible cues consistent with: hot work visible cue visible cue/visible cue. The work is being assessed at the in-progress lifecycle state with source anchors NFPA 51B, OSHA 1926 Subpart J.

## Task

Evaluate the procedure sequence and state what must happen before work can continue.

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

- NFPA 51B
- OSHA 1926 Subpart J
