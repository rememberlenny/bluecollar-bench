#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "tested/inspected",
  "s2_conditions": [
    "non-compliant"
  ],
  "s3_percent": 90,
  "findings": [
    "calibration",
    "oem procedure required"
  ],
  "actions": [
    "calibrate schedule return"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM position statements"
  ]
}
JSON
