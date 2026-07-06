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
    "shield single drawing",
    "ground loop noise wrong"
  ],
  "actions": [
    "complete",
    "remaining",
    "reinspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "loop drawings",
    "ISA 5.1"
  ]
}
JSON
