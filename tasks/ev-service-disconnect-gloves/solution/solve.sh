#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "work_stage": "in-progress",
  "component_conditions": [
    "non-compliant"
  ],
  "percent_complete": 45,
  "findings": [
    "wait time",
    "verify absence voltage",
    "gloves expired",
    "orange high voltage"
  ],
  "actions": [
    "stop work",
    "wait",
    "meter verify",
    "use tested gloves"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM HV procedures",
    "A-401"
  ]
}
JSON
