        # T1 M-201 Procedure sequencing coverage backfill

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t1-m-201-seq-bf-006-shaft-alignment`
        - Tier: `T1`
        - Discipline: `2.7 Equipment & Machinery`
        - Element: `M-201 Shaft alignment`
        - Task type: `SEQ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T1 work setting, the evaluated element is M-201 Shaft alignment within 2.7 Equipment & Machinery. The relevant subcategory is 2.7.2 Alignment. The observed field condition is: coupling gap out of spec. The work is being assessed at the in-progress lifecycle state with source anchors API 686, laser system manuals. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

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

        - API 686
- laser system manuals
