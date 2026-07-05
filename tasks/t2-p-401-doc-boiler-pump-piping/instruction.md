# T2 P-401 Document interpretation

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t2-p-401-doc-boiler-pump-piping`
- Tier: `T2`
- Discipline: `2.2 Mechanical - Piping & Plumbing`
- Element: `P-401 Boiler & pump piping`
- Task type: `DOC`
- Expected lifecycle state to assess: `tested/inspected`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T2 work setting, the evaluated element is P-401 Boiler & pump piping within 2.2 Mechanical - Piping & Plumbing. The relevant subcategory is 2.2.4 Hydronic & Steam. The field notes describe visible cues consistent with: not present where expected visible cue visible cue causing gravity flow. The work is being assessed at the tested/inspected lifecycle state with source anchors mfr manuals, hydronics references. A drawing, inspection checklist, equipment tag, or manufacturer instruction is available for comparison.

## Task

Compare the field condition against the referenced document, tag, drawing, or standard.

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

- mfr manuals
- hydronics references
