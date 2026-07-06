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
    "unprotected excavation",
    "protective system absent",
    "spoil too close",
    "egress ladder absent"
  ],
  "actions": [
    "stop work",
    "protective system",
    "move spoil",
    "provide ladder"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1926 Subpart P",
    "U-101"
  ]
}
JSON
