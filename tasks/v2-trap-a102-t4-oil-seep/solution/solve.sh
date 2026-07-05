#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "in-service",
  "s2_conditions": [
    "worn"
  ],
  "s3_percent": 100,
  "findings": [
    "seep dampness minor"
  ],
  "actions": [
    "monitor recheck note"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "OEM specs"
  ]
}
JSON
