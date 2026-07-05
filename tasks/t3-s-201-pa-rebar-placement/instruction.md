# T3 S-201 Progress assessment

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t3-s-201-pa-rebar-placement`
- Tier: `T3`
- Discipline: `2.4 Structural & Ironwork`
- Element: `S-201 Rebar placement`
- Task type: `PA`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective`
- Modality: `text`

## Scenario

In a T3 work setting, the evaluated element is S-201 Rebar placement within 2.4 Structural & Ironwork. The relevant subcategory is 2.4.2 Reinforcing. The field notes describe visible cues consistent with: not present where expected visible cue/visible cue (mat on dirt). The work is being assessed at the rough-complete lifecycle state with source anchors ACI 318, ACI 117, placing drawings. Treat this as roughly 70 percent complete until defects are corrected.

## Task

Assess lifecycle state, percent complete, defects, and remaining work.

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

- ACI 318
- ACI 117
- placing drawings
