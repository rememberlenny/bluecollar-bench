#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "s1_state": "rough-complete",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 70,
  "findings": [
    "686 grout projection",
    "vibration loosening resonance movement"
  ],
  "actions": [
    "measure",
    "correct",
    "reinspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "API RP 686"
  ]
}
JSON
