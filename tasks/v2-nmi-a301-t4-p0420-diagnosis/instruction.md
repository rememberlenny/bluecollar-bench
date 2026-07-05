# T4 A-301 Catalyst code without waveform data

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-nmi-a301-t4-p0420-diagnosis`
- Tier: `T4`
- Discipline: `2.9 Automotive & Powertrain`
- Element: `A-301 Diagnostics`
- Task type: `FD`
- Expected lifecycle state to assess: `planned`
- Relevant S2 condition classes: `degraded`
- Modality: `text`

## Scenario

A scan report shows stored code P0420 with a freeze frame captured at steady 45 mph cruise. The service writer has quoted a catalytic converter replacement. No upstream or downstream oxygen sensor waveform data, fuel trim values, or exhaust leak inspection results are attached to the ticket.

## Task

Assess whether the quoted repair is justified by the evidence provided. State what testing should occur before parts are ordered.

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

- OEM service info
