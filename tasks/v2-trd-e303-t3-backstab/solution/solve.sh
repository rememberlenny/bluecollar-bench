#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "rough-complete",
  "s2_conditions": [],
  "s3_percent": 90,
  "findings": [
    "listed permitted compliant",
    "side screw clamp"
  ],
  "actions": [
    "document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 110.14",
    "device listings"
  ]
}
JSON
