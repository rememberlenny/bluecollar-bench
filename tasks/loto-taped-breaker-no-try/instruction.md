# Lockout/tagout: taped breaker and no try step

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `loto-taped-breaker-no-try`
- Tier: `T4`
- Discipline: `2.12 Safety`
- Element: `X-101 Lockout/Tagout`
- Task type: `SEQ`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `non-compliant`
- Modality: `text`

## Scenario

A technician is preparing to service a conveyor. The disconnecting breaker is switched off and held with red tape but has no lock. A paper tag is taped to the panel door. The work order checklist skips verification of zero energy and does not mention stored mechanical energy in the raised conveyor section.

## Task

Evaluate the LOTO sequence and state the minimum corrections before work can continue.

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

- OSHA 1910.147
- X-101
