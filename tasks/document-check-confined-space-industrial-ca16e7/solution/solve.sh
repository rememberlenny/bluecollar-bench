#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "high",
  "work_stage": "planned",
  "component_conditions": [],
  "percent_complete": 5,
  "findings": [
    "h2s missing blank sensor"
  ],
  "actions": [
    "retest repair complete bump"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "OSHA 1910.146"
  ]
}
JSON
