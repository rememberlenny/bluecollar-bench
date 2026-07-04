        # T1 E-102 Identification

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t1-e-102-id-panelboard-installation-makeup`
        - Tier: `T1`
        - Discipline: `2.1 Electrical`
        - Element: `E-102 Panelboard installation & makeup`
        - Task type: `ID`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T1 work setting, the evaluated element is E-102 Panelboard installation & makeup within 2.1 Electrical. The relevant subcategory is 2.1.1 Power Distribution. The observed field condition is: missing knockout filler. The work is being assessed at the rough-complete lifecycle state with source anchors NEC Art. 408, 110.26 (working clearance), 200.4.

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

        - NEC Art. 408
- 110.26 (working clearance)
- 200.4
