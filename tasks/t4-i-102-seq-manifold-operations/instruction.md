# T4 I-102 Procedure sequencing

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t4-i-102-seq-manifold-operations`
- Tier: `T4`
- Discipline: `2.8 Instrumentation & Controls`
- Element: `I-102 Manifold operations`
- Task type: `SEQ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T4 work setting, the evaluated element is I-102 Manifold operations within 2.8 Instrumentation & Controls. The relevant subcategory is 2.8.1 Field Instruments. The field notes describe visible cues consistent with: 3/5-visible cue manifold visible cue not matching the specified requirement (equalize before opening HP side - pure SEQ item, one right order). The work is being assessed at the in-progress lifecycle state with source anchors mfr procedures.

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

- mfr procedures
