#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "work_stage": "in-progress",
  "component_conditions": [],
  "percent_complete": 40,
  "findings": [
    "illegible missing unknown duration"
  ],
  "actions": [
    "obtain confirm verify request"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "CPM computed ground truth",
    "expansion-plan track 3"
  ]
}
JSON
