        # T2 F-102 Tool & material selection

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t2-f-102-ts-connectors-fasteners`
        - Tier: `T2`
        - Discipline: `2.6 Carpentry & Finishes`
        - Element: `F-102 Connectors & fasteners`
        - Task type: `TS`
        - Expected lifecycle state to assess: `staged`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T2 work setting, the evaluated element is F-102 Connectors & fasteners within 2.6 Carpentry & Finishes. The relevant subcategory is 2.6.1 Rough Framing. The observed field condition is: wrong hanger for joist size. The work is being assessed at the staged lifecycle state with source anchors Simpson catalogs, IRC.

        ## Task

        Select the correct tool, material, or replacement approach and explain why the observed choice is wrong.

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

        - Simpson catalogs
- IRC
