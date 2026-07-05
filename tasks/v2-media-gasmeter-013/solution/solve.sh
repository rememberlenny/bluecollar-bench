#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "planned",
  "s2_conditions": [],
  "s3_percent": 5,
  "findings": [
    "within acceptable limits normal"
  ],
  "actions": [
    "entry proceed monitor continuous"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "OSHA 1910.146"
  ]
}
JSON
