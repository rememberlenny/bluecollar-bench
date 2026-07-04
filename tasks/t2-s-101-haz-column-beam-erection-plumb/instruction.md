        # T2 S-101 Hazard spotting

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t2-s-101-haz-column-beam-erection-plumb`
        - Tier: `T2`
        - Discipline: `2.4 Structural & Ironwork`
        - Element: `S-101 Column/beam erection & plumb`
        - Task type: `HAZ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T2 work setting, the evaluated element is S-101 Column/beam erection & plumb within 2.4 Structural & Ironwork. The relevant subcategory is 2.4.1 Steel Erection. The observed field condition is: shims missing under base plate. The work is being assessed at the in-progress lifecycle state with source anchors AISC 303, OSHA 1926 Subpart R.

        ## Task

        Identify the safety hazards, their severity, and the immediate controls required.

        ## Required output

        Write valid JSON to `/app/answer.json` with this shape:

        ```json
        {
          "decision": "pass | fail | needs_more_info",
          "risk": "low | medium | high | critical",
          "s1_state": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",
          "s2_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],
          "findings": ["short defect or hazard finding", "..."],
          "actions": ["immediate corrective action", "..."],
          "rationale": "brief explanation",
          "references": ["code or standard anchors you relied on"]
        }
        ```

        Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.

        ## Source anchors

        These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.

        - AISC 303
- OSHA 1926 Subpart R
