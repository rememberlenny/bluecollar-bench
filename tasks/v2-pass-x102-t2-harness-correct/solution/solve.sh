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
  "s3_percent": 50,
  "findings": [
    "fall arrest gear intact",
    "inspection tag current",
    "rated tie off"
  ],
  "actions": [
    "monitor",
    "document"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "OSHA 1926 Subpart M"
  ]
}
JSON
