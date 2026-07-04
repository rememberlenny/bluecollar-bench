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
  "s3_percent": 45,
  "findings": [
    "6 foot trench",
    "no shoring",
    "spoil within 2 ft",
    "no ladder"
  ],
  "actions": [
    "stop work",
    "protective system",
    "move spoil",
    "provide ladder"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1926 Subpart P",
    "U-101"
  ]
}
JSON
