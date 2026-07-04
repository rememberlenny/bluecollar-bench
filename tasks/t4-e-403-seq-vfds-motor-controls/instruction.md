        # T4 E-403 Procedure sequencing

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-e-403-seq-vfds-motor-controls`
        - Tier: `T4`
        - Discipline: `2.1 Electrical`
        - Element: `E-403 VFDs & motor controls`
        - Task type: `SEQ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T4 work setting, the evaluated element is E-403 VFDs & motor controls within 2.1 Electrical. The relevant subcategory is 2.1.4 Devices & Equipment. The observed field condition is: wrong overload class setting. The work is being assessed at the in-progress lifecycle state with source anchors NEC 430, mfr manuals.

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

        - NEC 430
- mfr manuals
