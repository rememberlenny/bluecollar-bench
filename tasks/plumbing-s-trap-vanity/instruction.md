        # DWV trap and venting: vanity S-trap

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `plumbing-s-trap-vanity`
        - Tier: `T3`
        - Discipline: `2.2 Piping/Plumbing`
        - Element: `P-201 Traps & venting`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        A bathroom vanity drain drops vertically out of the sink tailpiece into a P-trap, then immediately turns downward through the cabinet floor with no horizontal trap arm before the vent connection. There is no visible cleanout. The homeowner says the trap holds water after the faucet runs but occasionally gurgles when the tub drains.

        ## Task

        Assess whether the drain configuration is acceptable and explain the likely failure mode.

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

        - IPC/UPC
- P-201
