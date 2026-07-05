#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "needs_more_info",
  "risk": "medium",
  "s1_state": "planned",
  "s2_conditions": [
    "degraded"
  ],
  "s3_percent": 10,
  "findings": [
    "oxygen o2",
    "waveform data test"
  ],
  "actions": [
    "test verify measure"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM service info"
  ]
}
JSON
