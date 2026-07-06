#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "in-progress",
  "s2_conditions": [],
  "s3_percent": 90,
  "findings": [
    "permissible",
    "preference",
    "document"
  ],
  "actions": [
    "document",
    "proceed"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "NEC 210.8",
    "210.12"
  ]
}
JSON
