#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "s1_state": "in-progress",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 45,
  "findings": [
    "replacing",
    "parts",
    "codes"
  ],
  "actions": [
    "stop",
    "resequence",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM service info",
    "OBD-II standards"
  ]
}
JSON
