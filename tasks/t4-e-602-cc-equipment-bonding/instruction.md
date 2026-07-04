        # T4 E-602 Code/spec compliance

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-e-602-cc-equipment-bonding`
        - Tier: `T4`
        - Discipline: `2.1 Electrical`
        - Element: `E-602 Equipment bonding`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T4 work setting, the evaluated element is E-602 Equipment bonding within 2.1 Electrical. The relevant subcategory is 2.1.6 Grounding & Bonding. The observed field condition is: missing bonding jumper around water meter. The work is being assessed at the rough-complete lifecycle state with source anchors NEC 250.104, 250.30.

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

        - NEC 250.104
- 250.30
