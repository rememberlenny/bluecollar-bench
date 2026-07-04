        # T5 B-301 Procedure sequencing

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t5-b-301-seq-standard-work-execution`
        - Tier: `T5`
        - Discipline: `2.10 Assembly & Fabrication`
        - Element: `B-301 Standard work execution`
        - Task type: `SEQ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T5 work setting, the evaluated element is B-301 Standard work execution within 2.10 Assembly & Fabrication. The relevant subcategory is 2.10.3 Line Operations. The observed field condition is: step order deviation vs. standard work sheet (video + document = premier multimodal SEQ). The work is being assessed at the in-progress lifecycle state with source anchors site standard work, TWI.

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

        - site standard work
- TWI
