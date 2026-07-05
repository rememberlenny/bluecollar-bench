#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "s1_state": "tested/inspected",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 85,
  "findings": [
    "expired",
    "gauge",
    "calibration"
  ],
  "actions": [
    "compare",
    "correct",
    "document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ASME B31.3 \u00a7345"
  ]
}
JSON
