        # T2 H-101 Measurement & estimation coverage backfill

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t2-h-101-me-bf-007-condenser-heat-pump-sett`
        - Tier: `T2`
        - Discipline: `2.3 HVAC-R`
        - Element: `H-101 Condenser/heat pump setting`
        - Task type: `ME`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T2 work setting, the evaluated element is H-101 Condenser/heat pump setting within 2.3 HVAC-R. The relevant subcategory is 2.3.1 Equipment Installation. The observed field condition is: no service disconnect within sight. The work is being assessed at the rough-complete lifecycle state with source anchors mfr install manual, IMC/IRC M1401. The measurable cue is visible enough to estimate whether the condition is within tolerance. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

        ## Task

        Estimate or interpret the measurable condition and state why it is out of tolerance.

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

        - mfr install manual
- IMC/IRC M1401
