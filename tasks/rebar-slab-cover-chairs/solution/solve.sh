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
  "findings": [
    "insufficient cover",
    "missing chairs",
    "bars touching form"
  ],
  "actions": [
    "add chairs",
    "restore cover",
    "reinspect before pour"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ACI 318",
    "placing drawings",
    "S-201"
  ]
}
JSON
