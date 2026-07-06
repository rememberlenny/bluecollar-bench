#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "in-progress",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 45,
  "findings": [
    "aligned before piping",
    "pipe strain",
    "coupling gap changed",
    "alignment not repeated"
  ],
  "actions": [
    "repeat alignment",
    "relieve pipe strain",
    "verify coupling gap"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "API 686",
    "M-201"
  ]
}
JSON
