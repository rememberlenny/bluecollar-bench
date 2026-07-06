#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "work_stage": "rough-complete",
  "component_conditions": [],
  "percent_complete": 75,
  "findings": [
    "vent",
    "concealed wall hidden"
  ],
  "actions": [
    "verify vent"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "IPC"
  ]
}
JSON
