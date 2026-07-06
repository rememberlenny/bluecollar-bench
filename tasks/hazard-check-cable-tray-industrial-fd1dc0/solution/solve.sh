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
    "installed-defective",
    "non-compliant"
  ],
  "percent_complete": 45,
  "findings": [
    "392 fill bonding",
    "overheat derating fault path"
  ],
  "actions": [
    "stop work",
    "control hazard",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC Art. 392"
  ]
}
JSON
