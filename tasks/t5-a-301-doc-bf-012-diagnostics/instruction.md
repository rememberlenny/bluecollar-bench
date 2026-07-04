        # T5 A-301 Document interpretation coverage backfill

        You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.

        ## Item metadata

        - ID: `t5-a-301-doc-bf-012-diagnostics`
        - Tier: `T5`
        - Discipline: `2.9 Automotive & Powertrain`
        - Element: `A-301 Diagnostics`
        - Task type: `DOC`
        - Expected lifecycle state to assess: `tested/inspected`
        - Relevant S2 condition classes: `installed-defective`

        ## Scenario

        In a T5 work setting, the evaluated element is A-301 Diagnostics within 2.9 Automotive & Powertrain. The relevant subcategory is 2.9.3 Electrical & Electronics. The observed field condition is: freeze-frame interpretation (DOC: read the scan tool screenshot). The work is being assessed at the tested/inspected lifecycle state with source anchors OEM service info, OBD-II standards. A drawing, inspection checklist, equipment tag, or manufacturer instruction is available for comparison. This item is a coverage backfill for a core taxonomy matrix cell; validate tier-specific details with an SME before treating it as authoritative.

        ## Task

        Compare the field condition against the referenced document, tag, drawing, or standard.

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

        - OEM service info
- OBD-II standards
