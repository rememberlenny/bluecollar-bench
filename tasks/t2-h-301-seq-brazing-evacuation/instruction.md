        # T2 H-301 Procedure sequencing

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t2-h-301-seq-brazing-evacuation`
        - Tier: `T2`
        - Discipline: `2.3 HVAC-R`
        - Element: `H-301 Brazing & evacuation`
        - Task type: `SEQ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T2 work setting, the evaluated element is H-301 Brazing & evacuation within 2.3 HVAC-R. The relevant subcategory is 2.3.3 Refrigeration Circuit. The observed field condition is: brazed without nitrogen purge (black scale inside - shows in cutaway photos). The work is being assessed at the in-progress lifecycle state with source anchors mfr specs, ACCA, EPA 608.

        ## Task

        Evaluate the procedure sequence and state what must happen before work can continue.

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

        - mfr specs
- ACCA
- EPA 608
