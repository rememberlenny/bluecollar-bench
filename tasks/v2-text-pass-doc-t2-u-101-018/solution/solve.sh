#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "tested/inspected",
  "s2_conditions": [],
  "s3_percent": 90,
  "findings": [
    "traceable",
    "consistent",
    "approved"
  ],
  "actions": [
    "document",
    "release"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "OSHA 1926 Subpart P"
  ]
}
JSON
