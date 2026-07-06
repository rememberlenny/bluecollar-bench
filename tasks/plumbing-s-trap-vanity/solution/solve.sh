#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "rough-complete",
  "component_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "percent_complete": 70,
  "findings": [
    "s-trap",
    "siphon trap seal",
    "missing cleanout"
  ],
  "actions": [
    "reconfigure trap arm",
    "connect vent",
    "add cleanout"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "IPC/UPC",
    "P-201"
  ]
}
JSON
