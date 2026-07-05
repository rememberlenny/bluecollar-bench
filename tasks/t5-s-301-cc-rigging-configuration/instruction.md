# T5 S-301 Code/spec compliance

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `t5-s-301-cc-rigging-configuration`
- Tier: `T5`
- Discipline: `2.4 Structural & Ironwork`
- Element: `S-301 Rigging configuration`
- Task type: `CC`
- Expected lifecycle state to assess: `rough-complete`
- Relevant S2 condition classes: `installed-defective, non-compliant`
- Modality: `text`

## Scenario

In a T5 work setting, the evaluated element is S-301 Rigging configuration within 2.4 Structural & Ironwork. The relevant subcategory is 2.4.3 Rigging & Machinery Moving. The field notes describe visible cues consistent with: visible cue visible cue visible cue edges. The work is being assessed at the rough-complete lifecycle state with source anchors ASME B30, OSHA 1926.251.

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

- ASME B30
- OSHA 1926.251
