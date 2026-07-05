#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "high",
  "s1_state": "planned",
  "s2_conditions": [],
  "s3_percent": 5,
  "findings": [
    "h2s missing blank sensor"
  ],
  "actions": [
    "retest repair complete bump"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1910.146"
  ]
}
JSON
