        # T4 P-302 Code/spec compliance

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-p-302-cc-water-heaters`
        - Tier: `T4`
        - Discipline: `2.2 Mechanical - Piping & Plumbing`
        - Element: `P-302 Water heaters`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T4 work setting, the evaluated element is P-302 Water heaters within 2.2 Mechanical - Piping & Plumbing. The relevant subcategory is 2.2.3 Plumbing - Supply. The observed field condition is: T&P discharge pipe missing/trapped/reduced/terminated too high. The work is being assessed at the rough-complete lifecycle state with source anchors IPC 504, IRC P2804.

        ## Task

        Determine whether the work meets the applicable code, spec, drawing, or manufacturer requirement.

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

        - IPC 504
- IRC P2804
