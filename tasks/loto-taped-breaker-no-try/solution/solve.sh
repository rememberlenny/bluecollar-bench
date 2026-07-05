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
    "unlocked breaker",
    "tape is not lock",
    "try step omitted",
    "uncontrolled stored energy"
  ],
  "actions": [
    "apply lock",
    "tag",
    "verify zero energy",
    "control stored energy"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1910.147",
    "X-101"
  ]
}
JSON
