        # Structural bolting: pretension evidence

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `structural-bolting-pretension`
        - Tier: `T2`
        - Discipline: `2.4 Structural & Ironwork`
        - Element: `S-102 Structural bolting`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        A beam splice detail calls for pretensioned A325 bolts. The field photo shows several bolts with head markings that do not match the submitted bolt grade. No turn-of-nut match marks or DTI washer indications are visible. The inspector notes the crew described the joint as 'snug tight only' because the connection looked stable.

        ## Task

        Decide if this connection can be accepted and list what evidence or rework is needed.

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

        - RCSC Specification
- S-102
