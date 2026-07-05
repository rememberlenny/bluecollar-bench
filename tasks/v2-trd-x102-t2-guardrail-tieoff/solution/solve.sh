#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "in-progress",
  "s2_conditions": [
    "non-compliant"
  ],
  "s3_percent": 40,
  "findings": [
    "not rated anchorage",
    "tie off unacceptable"
  ],
  "actions": [
    "stop work",
    "relocate engineered proper"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1926.502"
  ]
}
JSON
