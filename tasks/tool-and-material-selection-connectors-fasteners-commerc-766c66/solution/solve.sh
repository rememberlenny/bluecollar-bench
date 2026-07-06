#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "staged",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 15,
  "findings": [
    "listed fastener schedule",
    "withdrawal shear capacity uplift"
  ],
  "actions": [
    "replace",
    "select",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "Simpson catalogs",
    "IRC"
  ]
}
JSON
