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
    "installed-defective"
  ],
  "s3_percent": 70,
  "findings": [
    "identification 200.6 pull",
    "damage insulation phase confusion"
  ],
  "actions": [
    "complete",
    "remaining",
    "reinspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 200.6",
    "210.5 (identification)"
  ]
}
JSON
