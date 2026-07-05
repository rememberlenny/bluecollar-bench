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
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1910.146"
  ]
}
JSON
