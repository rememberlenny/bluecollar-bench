        # T5 B-401 Measurement & estimation

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t5-b-401-me-visual-acceptance`
        - Tier: `T5`
        - Discipline: `2.10 Assembly & Fabrication`
        - Element: `B-401 Visual acceptance`
        - Task type: `ME`
        - Expected lifecycle state to assess: `rough-complete`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T5 work setting, the evaluated element is B-401 Visual acceptance within 2.10 Assembly & Fabrication. The relevant subcategory is 2.10.4 Quality Inspection. The observed field condition is: first-article dims vs. drawing (DOC+ME). The work is being assessed at the rough-complete lifecycle state with source anchors site visual standards, AIAG PPAP. The measurable cue is visible enough to estimate whether the condition is within tolerance.

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

        - site visual standards
- AIAG PPAP
