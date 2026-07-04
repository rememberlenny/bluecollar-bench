        # T4 A-401 Hazard spotting

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-a-401-haz-high-voltage-safety`
        - Tier: `T4`
        - Discipline: `2.9 Automotive & Powertrain`
        - Element: `A-401 High-voltage safety`
        - Task type: `HAZ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T4 work setting, the evaluated element is A-401 High-voltage safety within 2.9 Automotive & Powertrain. The relevant subcategory is 2.9.4 EV & A/C Systems. The observed field condition is: glove class wrong or test date expired (ID from stamp). The work is being assessed at the in-progress lifecycle state with source anchors OEM HV procedures, NFPA 70E-adjacent.

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

        - OEM HV procedures
- NFPA 70E-adjacent
