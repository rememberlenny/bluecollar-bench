#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "in-progress",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 45,
  "findings": [
    "standard work instruction",
    "deviation escape defect downstream"
  ],
  "actions": [
    "stop",
    "resequence",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "site standard work",
    "TWI"
  ]
}
JSON
