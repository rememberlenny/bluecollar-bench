        # Duct installation: flex sag and unsealed joints

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `duct-flex-sag-cloth-tape`
        - Tier: `T3`
        - Discipline: `2.3 HVAC-R`
        - Element: `H-201 Duct installation`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        A basement supply branch uses flexible duct with visible sags between hangers. Several metal-to-flex joints are wrapped only with gray cloth duct tape; no mastic, UL-listed foil tape, or mechanical draw bands are visible. The homeowner says air comes out of the register, but the room is always cold.

        ## Task

        Assess the installation quality and name the defects.

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

        - IMC 603
- SMACNA
- Manual D
- H-201
