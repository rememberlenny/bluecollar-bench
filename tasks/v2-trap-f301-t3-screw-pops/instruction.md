# T3 F-301 Cosmetic screw pops (alarmist trap)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-trap-f301-t3-screw-pops`
- Tier: `T3`
- Discipline: `2.6 Carpentry & Finishes`
- Element: `F-301 Drywall & finishing`
- Task type: `CC`
- Expected lifecycle state to assess: `accepted`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A one-year warranty walkthrough of a non-fire-rated interior partition notes three small circular bumps in the paint film along one stud line, consistent with seasonal lumber shrinkage. Fastener spacing on the original inspection photos met the schedule, and the wall shows no cracking, movement, or moisture staining.

## Task

Classify this condition and determine whether it represents a defect requiring corrective construction work.

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

- GA-216
