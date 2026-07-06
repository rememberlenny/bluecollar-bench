#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "s1_state": "tested/inspected",
  "s2_conditions": [],
  "s3_percent": 50,
  "findings": [
    "unverified",
    "document missing",
    "confirm"
  ],
  "actions": [
    "request",
    "verify",
    "document"
  ],
  "rationale": "The available evidence is insufficient to make the requested determination without additional information.",
  "references": [
    "ASME B31.3 \u00a7345"
  ]
}
JSON
