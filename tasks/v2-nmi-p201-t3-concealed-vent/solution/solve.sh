#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "s1_state": "rough-complete",
  "s2_conditions": [],
  "s3_percent": 75,
  "findings": [
    "vent",
    "concealed wall hidden"
  ],
  "actions": [
    "verify vent"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "IPC"
  ]
}
JSON
