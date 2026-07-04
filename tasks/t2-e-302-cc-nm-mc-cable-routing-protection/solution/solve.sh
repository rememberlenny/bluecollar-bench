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
    "cable",
    "routing",
    "within",
    "stud",
    "face",
    "non compliant"
  ],
  "actions": [
    "correct",
    "inspect",
    "before acceptance"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 300.4",
    "334",
    "330"
  ]
}
JSON
