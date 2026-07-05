# T3 E-402 Fault diagnosis

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-e-402-fd-gfci-afci-function-troubleshooti`
- Tier: `T3`
- Discipline: `2.1 Electrical`
- Element: `E-402 GFCI/AFCI function & troubleshooting`
- Task type: `FD`
- Expected lifecycle state to assess: `in-service`
- Relevant S2 condition classes: `degraded, failed`
- Modality: `text`

## Scenario

In a T3 work setting, the evaluated element is E-402 GFCI/AFCI function & troubleshooting within 2.1 Electrical. The relevant subcategory is 2.1.4 Devices & Equipment. The field notes describe visible cues consistent with: visible cue/load arranged opposite of the expected orientation on GFCI. The work is being assessed at the in-service lifecycle state with source anchors NEC 210.8, 210.12.

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

- NEC 210.8
- 210.12
