#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "rough-complete",
  "component_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "percent_complete": 70,
  "findings": [
    "flex duct sag",
    "cloth duct tape",
    "joints unsealed"
  ],
  "actions": [
    "support flex",
    "seal mastic",
    "draw bands"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "IMC 603",
    "SMACNA",
    "Manual D",
    "H-201"
  ]
}
JSON
