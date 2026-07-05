# T2 E-702 Measurement & estimation

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t2-e-702-me-data-comm-security`
- Tier: `T2`
- Discipline: `2.1 Electrical`
- Element: `E-702 Data/comm & security`
- Task type: `ME`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T2 work setting, the evaluated element is E-702 Data/comm & security within 2.1 Electrical. The relevant subcategory is 2.1.7 Low Voltage & Specialty. The field notes describe visible cues consistent with: visible cue vs. visible cue visible cue in wrong space. The work is being assessed at the rough-complete lifecycle state with source anchors TIA-568, NEC 800. The measurable cue is visible enough to estimate whether the condition is within tolerance.

## Task

Estimate or interpret the measurable condition and state why it is out of tolerance.

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

- TIA-568
- NEC 800
