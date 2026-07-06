#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "rough-complete",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 70,
  "findings": [
    "347 bracing pressure",
    "blowout collapse deflection failure"
  ],
  "actions": [
    "complete",
    "remaining",
    "reinspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ACI 347"
  ]
}
JSON
