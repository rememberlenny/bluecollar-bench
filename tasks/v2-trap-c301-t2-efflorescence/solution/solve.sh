#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "accepted",
  "s2_conditions": [],
  "s3_percent": 100,
  "findings": [
    "efflorescence salt powder"
  ],
  "actions": [
    "clean monitor brush"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "BIA tech notes"
  ]
}
JSON
