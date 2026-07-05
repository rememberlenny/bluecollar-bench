# T2 X-106 Hazard spotting

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t2-x-106-haz-housekeeping-general-hazard-reco`
- Tier: `T2`
- Discipline: `2.12 Safety & Rigging`
- Element: `X-106 Housekeeping & general hazard recognition`
- Task type: `HAZ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T2 work setting, the evaluated element is X-106 Housekeeping & general hazard recognition within 2.12 Safety & Rigging. The relevant subcategory is 2.10.4 Quality Inspection. The field notes describe visible cues consistent with: the visible cue-visible cue "visible cue all hazards in this jobsite photo" item - cords across walkways, missing guardrails, blocked egress/extinguishers, improvised scaffolds, unattended visible cue holes. The work is being assessed at the in-progress lifecycle state with source anchors OSHA general duty, 1926 Subpart L (scaffolds).

## Task

Identify the safety hazards, their severity, and the immediate controls required.

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

- OSHA general duty
- 1926 Subpart L (scaffolds)
