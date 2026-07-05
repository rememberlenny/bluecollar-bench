# T1 X-103 Incomplete atmospheric testing

You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

## Item metadata

- ID: `v2-nmi-x103-t1-incomplete-gas-test`
- Tier: `T1`
- Discipline: `2.12 Safety & Rigging`
- Element: `X-103 Confined space`
- Task type: `DOC`
- Expected lifecycle state to assess: `planned`
- Relevant S2 condition classes: `none`
- Modality: `text`

## Scenario

A confined-space entry permit for a process vessel shows an oxygen reading of 20.9 percent logged thirty minutes ago. The LEL, H2S, and CO fields on the permit are blank, and the meter's bump-test record for today is not attached. The attendant and rescue plan sections are complete.

## Task

Determine whether entry can be authorized on this permit as documented. Identify exactly what is missing.

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
  "sound_source": "component or source of the sound, when asked",
  "confidence": 0.0,
  "event_time": 0.0,
  "rate": 0.0,
  "order": ["step-id", "..."],
  "workable": ["activity ID", "..."],
  "findings": ["short defect or hazard finding", "..."],
  "actions": ["immediate corrective action", "..."],
  "rationale": "brief explanation",
  "references": ["code or standard anchors you relied on"]
}
```

Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.
Use `value` for the numeric reading or computed quantity when the task asks for one.
Use `sound_source`, `event_time`, `rate`, and `order` for audio/video-native tasks when requested.
Use `workable` for a list of activity IDs when the task asks what work can still start.

## Source anchors

These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.

- OSHA 1910.146
