#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "s1_state": "rough-complete",
  "s2_conditions": [],
  "s3_percent": 70,
  "findings": [
    "bar size",
    "scale reference closeup measure"
  ],
  "actions": [
    "measure verify confirm"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "ACI 117",
    "placing drawings"
  ]
}
JSON
