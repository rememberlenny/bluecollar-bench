        # Electrical panel makeup: subpanel defects

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `electrical-panel-subpanel-defects`
        - Tier: `T3`
        - Discipline: `2.1 Electrical`
        - Element: `E-102 Panelboard installation & makeup`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        A residential garage subpanel is shown with the deadfront removed during rough inspection. The feeder includes separate insulated neutral and bare equipment grounding conductors. The neutral bar is bonded to the cabinet with the green bonding screw installed. Several bare equipment grounding conductors and white neutral conductors terminate on the same bar. One 20 A breaker has two branch-circuit conductors under a single terminal. An unused knockout opening is visible on the lower right side of the enclosure. Working clearance is otherwise clear.

        ## Task

        Determine whether this installation should pass inspection. Identify the visible defects, classify the risk, and list the immediate corrective actions.

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

        - NEC Art. 408
- NEC 110.26
- NEC 200.4
