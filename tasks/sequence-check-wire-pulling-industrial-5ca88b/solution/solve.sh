#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "in-progress",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 45,
  "findings": [
    "identification 200.6 pull",
    "damage insulation phase confusion"
  ],
  "actions": [
    "stop",
    "resequence",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 200.6",
    "210.5 (identification)"
  ]
}
JSON
