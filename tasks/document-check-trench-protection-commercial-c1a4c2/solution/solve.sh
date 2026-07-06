#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "work_stage": "tested/inspected",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 85,
  "findings": [
    "subpart p protective",
    "collapse engulfment fatality cave"
  ],
  "actions": [
    "compare",
    "correct",
    "document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1926 Subpart P"
  ]
}
JSON
