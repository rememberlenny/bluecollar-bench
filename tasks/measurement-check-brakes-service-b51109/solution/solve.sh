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
    "worn"
  ],
  "percent_complete": 90,
  "findings": [
    "below under less"
  ],
  "actions": [
    "replace"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM specs"
  ],
  "value": 26.77
}
JSON
