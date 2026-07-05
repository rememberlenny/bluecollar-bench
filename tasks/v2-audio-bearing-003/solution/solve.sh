#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "in-service",
  "s2_conditions": [],
  "s3_percent": 100,
  "findings": [
    "smooth hum no normal"
  ],
  "actions": [
    "monitor route document"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "SKF/Timken guides"
  ],
  "sound_source": "bearing",
  "confidence": 1.0
}
JSON
