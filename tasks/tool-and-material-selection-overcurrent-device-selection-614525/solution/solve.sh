#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "staged",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 15,
  "findings": [
    "240 ampacity protection",
    "overload overheat fire"
  ],
  "actions": [
    "replace",
    "select",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 240",
    "210.8",
    "210.12",
    "110.14(C) termination temp ratings"
  ]
}
JSON
