        # Trench protection: missing protective system

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `trench-protection-spoil-ladder`
        - Tier: `T2`
        - Discipline: `2.11 Sitework & Utilities`
        - Element: `U-101 Trench protection`
        - Task type: `HAZ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `non-compliant`

        ## Scenario

        Workers are installing a sewer lateral in an approximately 6-foot-deep trench. The trench walls are nearly vertical with no trench box, shoring, or sloping. Spoil is piled within one foot of the edge. No ladder is visible within the photographed work area.

        ## Task

        Identify the hazards and state whether work may continue.

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

        - OSHA 1926 Subpart P
- U-101
