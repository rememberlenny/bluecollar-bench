# T5 B-101 Torque-to-yield reuse (judgment)

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-trd-b101-t5-tty-reuse`
- Tier: `T5`
- Discipline: `2.10 Assembly & Fabrication`
- Element: `B-101 Torque & threaded fastening`
- Task type: `TRD`
- Expected lifecycle state to assess: `in-progress`
- Relevant S2 condition classes: `non-compliant`
- Modality: `text`

## Scenario

During a line-side rework, an operator reinstalls the same stretch bolts that were removed an hour earlier, reasoning that they were only torqued once and the replacement kit would stop the line for twenty minutes. The engineering spec marks these fasteners single-use with an angle-tightening step.

## Task

Judge the operator's reasoning against the specification. State the correct disposition and the cost-versus-risk tradeoff involved.

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

- engineering specs
