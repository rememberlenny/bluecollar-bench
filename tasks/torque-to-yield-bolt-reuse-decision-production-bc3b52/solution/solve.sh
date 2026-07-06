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
    "non-compliant"
  ],
  "percent_complete": 60,
  "findings": [
    "one time fastener",
    "reuse unacceptable"
  ],
  "actions": [
    "replace new",
    "andon stop hold"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "engineering specs"
  ]
}
JSON
