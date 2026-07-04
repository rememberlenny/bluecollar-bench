        # EV high-voltage safety: incomplete isolation

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `ev-service-disconnect-gloves`
        - Tier: `T4`
        - Discipline: `2.9 Automotive`
        - Element: `A-401 High-voltage safety`
        - Task type: `HAZ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `non-compliant`

        ## Scenario

        An EV battery service photo shows the orange service disconnect removed and placed on the cowl. The technician immediately begins removing the inverter cover. The class 0 gloves in use have a test date that expired nine months ago. No meter verification of absence of voltage is shown.

        ## Task

        Evaluate whether the high-voltage work can proceed and identify the required safety steps.

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

        - OEM HV procedures
- A-401
