# T1 U-101 Code/spec compliance

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t1-u-101-cc-trench-protection`
- Tier: `T1`
- Discipline: `2.11 Sitework & Utilities`
- Element: `U-101 Trench protection`
- Task type: `CC`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T1 work setting, the evaluated element is U-101 Trench protection within 2.11 Sitework & Utilities. The relevant subcategory is 2.11.1 Excavation & Trenching. The field notes describe visible cues consistent with: no visible cue within 25 ft visible cue visible cue. The work is being assessed at the rough-complete lifecycle state with source anchors OSHA 1926 Subpart P.

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

- OSHA 1926 Subpart P
