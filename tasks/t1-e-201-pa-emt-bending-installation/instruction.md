        # T1 E-201 Progress assessment

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t1-e-201-pa-emt-bending-installation`
        - Tier: `T1`
        - Discipline: `2.1 Electrical`
        - Element: `E-201 EMT bending & installation`
        - Task type: `PA`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T1 work setting, the evaluated element is E-201 EMT bending & installation within 2.1 Electrical. The relevant subcategory is 2.1.2 Raceway. The observed field condition is: improper coupling engagement. The work is being assessed at the rough-complete lifecycle state with source anchors NEC Art. 358, Ch. 9 (fill). Treat this as roughly 70 percent complete until defects are corrected.

        ## Task

        Assess lifecycle state, percent complete, defects, and remaining work.

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

        - NEC Art. 358
- Ch. 9 (fill)
