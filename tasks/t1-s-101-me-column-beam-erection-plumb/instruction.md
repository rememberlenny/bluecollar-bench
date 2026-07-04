        # T1 S-101 Measurement & estimation

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t1-s-101-me-column-beam-erection-plumb`
        - Tier: `T1`
        - Discipline: `2.4 Structural & Ironwork`
        - Element: `S-101 Column/beam erection & plumb`
        - Task type: `ME`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T1 work setting, the evaluated element is S-101 Column/beam erection & plumb within 2.4 Structural & Ironwork. The relevant subcategory is 2.4.1 Steel Erection. The observed field condition is: anchor bolts field-bent to fit. The work is being assessed at the rough-complete lifecycle state with source anchors AISC 303, OSHA 1926 Subpart R. The measurable cue is visible enough to estimate whether the condition is within tolerance.

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
