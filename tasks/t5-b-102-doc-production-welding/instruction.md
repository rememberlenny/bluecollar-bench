        # T5 B-102 Document interpretation

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t5-b-102-doc-production-welding`
        - Tier: `T5`
        - Discipline: `2.10 Assembly & Fabrication`
        - Element: `B-102 Production welding`
        - Task type: `DOC`
        - Expected lifecycle state to assess: `tested/inspected`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T5 work setting, the evaluated element is B-102 Production welding within 2.10 Assembly & Fabrication. The relevant subcategory is 2.10.1 Fastening & Joining. The observed field condition is: parameters outside WPS window (DOC: compare machine settings photo to WPS). The work is being assessed at the tested/inspected lifecycle state with source anchors AWS D1.1/D1.3, shop WPS. A drawing, inspection checklist, equipment tag, or manufacturer instruction is available for comparison.

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

        - AWS D1.1/D1.3
- shop WPS
