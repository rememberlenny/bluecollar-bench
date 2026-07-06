#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "rough-complete",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 70,
  "findings": [
    "incomplete bolt pattern",
    "uneven thread projection",
    "no torque witness"
  ],
  "actions": [
    "install all bolts",
    "torque sequence",
    "mark witness",
    "inspect before test"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ASME PCC-1",
    "B16.5",
    "P-102"
  ]
}
JSON
