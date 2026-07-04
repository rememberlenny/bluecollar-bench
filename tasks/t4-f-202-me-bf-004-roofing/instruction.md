        # T4 F-202 Measurement & estimation coverage backfill

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t4-f-202-me-bf-004-roofing`
        - Tier: `T4`
        - Discipline: `2.6 Carpentry & Finishes`
        - Element: `F-202 Roofing`
        - Task type: `ME`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T4 work setting, the evaluated element is F-202 Roofing within 2.6 Carpentry & Finishes. The relevant subcategory is 2.6.2 Exterior Envelope. The observed field condition is: pipe boot cracked (T4 FD). The work is being assessed at the rough-complete lifecycle state with source anchors IRC R905, mfr specs. The measurable cue is visible enough to estimate whether the condition is within tolerance. This item is a coverage backfill for a secondary taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

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

        - IRC R905
- mfr specs
