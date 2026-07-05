# T5 A-201 Code/spec compliance coverage backfill

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t5-a-201-cc-bf-018-brakes`
- Tier: `T5`
- Discipline: `2.9 Automotive & Powertrain`
- Element: `A-201 Brakes`
- Task type: `CC`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T5 work setting, the evaluated element is A-201 Brakes within 2.9 Automotive & Powertrain. The relevant subcategory is 2.9.2 Chassis. The field notes describe visible cues consistent with: lug visible cue visible cue & visible cue (star pattern - SEQ. The work is being assessed at the rough-complete lifecycle state with source anchors OEM specs, FMVSS-adjacent shop practice. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

## Task

Determine whether the work meets the applicable code, spec, drawing, or manufacturer requirement.

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

- OEM specs
- FMVSS-adjacent shop practice
