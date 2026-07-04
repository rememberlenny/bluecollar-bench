        # T4 A-202 Measurement & estimation

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-a-202-me-suspension-steering`
        - Tier: `T4`
        - Discipline: `2.9 Automotive & Powertrain`
        - Element: `A-202 Suspension & steering`
        - Task type: `ME`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T4 work setting, the evaluated element is A-202 Suspension & steering within 2.9 Automotive & Powertrain. The relevant subcategory is 2.9.2 Chassis. The observed field condition is: torquing rubber bushings at full droop (TRD - preload error). The work is being assessed at the rough-complete lifecycle state with source anchors OEM, alignment specs. The measurable cue is visible enough to estimate whether the condition is within tolerance.

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

        - OEM
- alignment specs
