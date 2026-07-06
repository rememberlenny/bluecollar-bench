#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "tested/inspected",
  "component_conditions": [
    "degraded",
    "installed-defective"
  ],
  "percent_complete": 85,
  "findings": [
    "rotor below minimum",
    "brake hose twisted",
    "pedal firm not sufficient"
  ],
  "actions": [
    "replace rotor",
    "correct hose",
    "road test"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM specs",
    "A-201"
  ]
}
JSON
