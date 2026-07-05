#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "s1_state": "rough-complete",
  "s2_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "s3_percent": 70,
  "findings": [
    "slings",
    "over",
    "unprotected"
  ],
  "actions": [
    "correct",
    "inspect",
    "before acceptance"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ASME B30",
    "OSHA 1926.251"
  ]
}
JSON
