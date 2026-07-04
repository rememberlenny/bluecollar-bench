        # T2 H-301 Code/spec compliance coverage backfill

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t2-h-301-cc-bf-004-brazing-evacuation`
        - Tier: `T2`
        - Discipline: `2.3 HVAC-R`
        - Element: `H-301 Brazing & evacuation`
        - Task type: `CC`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective, non-compliant`

        ## Scenario

        In a T2 work setting, the evaluated element is H-301 Brazing & evacuation within 2.3 HVAC-R. The relevant subcategory is 2.3.3 Refrigeration Circuit. The observed field condition is: vacuum not held at target microns (decay test - read the gauge, FD). The work is being assessed at the rough-complete lifecycle state with source anchors mfr specs, ACCA, EPA 608. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

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

        - mfr specs
- ACCA
- EPA 608
