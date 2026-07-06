#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "high",
  "s1_state": "in-progress",
  "s2_conditions": [],
  "s3_percent": 50,
  "findings": [
    "unverified",
    "exposure unknown",
    "confirm"
  ],
  "actions": [
    "request",
    "verify",
    "document"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "NEC 300.4",
    "334",
    "330"
  ]
}
JSON
