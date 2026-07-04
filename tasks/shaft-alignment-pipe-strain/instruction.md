        # Shaft alignment: sequence and pipe strain

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `shaft-alignment-pipe-strain`
        - Tier: `T1`
        - Discipline: `2.7 Equipment/Millwright`
        - Element: `M-201 Shaft alignment`
        - Task type: `SEQ`
        - Expected lifecycle state to assess: `in-progress`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        A pump and motor were laser-aligned while the suction and discharge piping were still disconnected. After piping was bolted up, the coupling gap changed visibly and the laser report was not repeated. The crew wants to grout the base and install the coupling guard.

        ## Task

        Evaluate the sequence and explain the likely problem before final acceptance.

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

        - API 686
- M-201
