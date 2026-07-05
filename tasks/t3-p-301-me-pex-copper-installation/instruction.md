# T3 P-301 Measurement & estimation

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-p-301-me-pex-copper-installation`
- Tier: `T3`
- Discipline: `2.2 Mechanical - Piping & Plumbing`
- Element: `P-301 PEX & copper installation`
- Task type: `ME`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T3 work setting, the evaluated element is P-301 PEX & copper installation within 2.2 Mechanical - Piping & Plumbing. The relevant subcategory is 2.2.3 Plumbing - Supply. The field notes describe visible cues consistent with: copper visible cue (visible visible cue). The work is being assessed at the rough-complete lifecycle state with source anchors IPC, mfr specs. The measurable cue is visible enough to estimate whether the condition is within tolerance.

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

- IPC
- mfr specs
