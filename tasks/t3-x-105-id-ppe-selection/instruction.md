        # T3 X-105 Identification

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t3-x-105-id-ppe-selection`
        - Tier: `T3`
        - Discipline: `2.12 Safety & Rigging`
        - Element: `X-105 PPE selection`
        - Task type: `ID`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T3 work setting, the evaluated element is X-105 PPE selection within 2.12 Safety & Rigging. The relevant subcategory is 2.10.4 Quality Inspection. The observed field condition is: voltage glove class wrong or overdue. The work is being assessed at the rough-complete lifecycle state with source anchors NFPA 70E, OSHA 1910 Subpart I.

        ## Task

        Identify the component or condition shown, and name the visible defect cues.

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

        - NFPA 70E
- OSHA 1910 Subpart I
