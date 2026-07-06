#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "work_stage": "tested/inspected",
  "component_conditions": [],
  "percent_complete": 90,
  "findings": [
    "illegible unreadable unknown stamp"
  ],
  "actions": [
    "specification spec lookup verify"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "OEM specs"
  ],
  "value": 26.27
}
JSON
