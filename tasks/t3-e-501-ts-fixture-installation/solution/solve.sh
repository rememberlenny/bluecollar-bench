#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "s1_state": "staged",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 15,
  "findings": [
    "fixture",
    "installation",
    "missing",
    "support",
    "independent"
  ],
  "actions": [
    "replace",
    "select",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 410"
  ]
}
JSON
