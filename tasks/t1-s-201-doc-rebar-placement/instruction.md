        # T1 S-201 Document interpretation

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t1-s-201-doc-rebar-placement`
        - Tier: `T1`
        - Discipline: `2.4 Structural & Ironwork`
        - Element: `S-201 Rebar placement`
        - Task type: `DOC`
        - Expected lifecycle state to assess: `tested/inspected`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T1 work setting, the evaluated element is S-201 Rebar placement within 2.4 Structural & Ironwork. The relevant subcategory is 2.4.2 Reinforcing. The observed field condition is: wrong bar size vs. schedule (deformation count/size - ID+DOC). The work is being assessed at the tested/inspected lifecycle state with source anchors ACI 318, ACI 117, placing drawings. A drawing, inspection checklist, equipment tag, or manufacturer instruction is available for comparison.

        ## Task

        Compare the field condition against the referenced document, tag, drawing, or standard.

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

        - ACI 318
- ACI 117
- placing drawings
