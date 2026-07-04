        # T2 E-304 Progress assessment

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t2-e-304-pa-wire-pulling-feeders-branch`
        - Tier: `T2`
        - Discipline: `2.1 Electrical`
        - Element: `E-304 Wire pulling (feeders & branch)`
        - Task type: `PA`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T2 work setting, the evaluated element is E-304 Wire pulling (feeders & branch) within 2.1 Electrical. The relevant subcategory is 2.1.3 Wire & Cable. The observed field condition is: exceeded sidewall pressure/jamming (planning item). The work is being assessed at the rough-complete lifecycle state with source anchors NEC 200.6, 210.5 (identification). Treat this as roughly 70 percent complete until defects are corrected.

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

        - NEC 200.6
- 210.5 (identification)
