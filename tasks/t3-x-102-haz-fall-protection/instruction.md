        # T3 X-102 Hazard spotting

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t3-x-102-haz-fall-protection`
        - Tier: `T3`
        - Discipline: `2.12 Safety & Rigging`
        - Element: `X-102 Fall protection`
        - Task type: `HAZ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T3 work setting, the evaluated element is X-102 Fall protection within 2.12 Safety & Rigging. The relevant subcategory is 2.10.4 Quality Inspection. The observed field condition is: anchor point inadequate (guessing at 5,000-lb rating - TRD). The work is being assessed at the in-progress lifecycle state with source anchors OSHA 1926 Subpart M, 1910.140.

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

        - OSHA 1926 Subpart M
- 1910.140
