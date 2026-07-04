        # T4 E-301 Tradeoff judgment

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-e-301-trd-conductor-selection-sizing`
        - Tier: `T4`
        - Discipline: `2.1 Electrical`
        - Element: `E-301 Conductor selection & sizing`
        - Task type: `TRD`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T4 work setting, the evaluated element is E-301 Conductor selection & sizing within 2.1 Electrical. The relevant subcategory is 2.1.3 Wire & Cable. The observed field condition is: undersized for load + length (voltage drop). The work is being assessed at the in-progress lifecycle state with source anchors NEC 310, Table 310.16.

        ## Task

        Resolve the field tradeoff: distinguish common shortcuts from acceptable journeyman practice.

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

        - NEC 310
- Table 310.16
