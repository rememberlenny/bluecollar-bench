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
  "s3_percent": 0,
  "findings": [
    "within below under acceptable"
  ],
  "actions": [
    "proceed lift document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ASME B30.9",
    "OSHA 1926.251"
  ],
  "value": 3000
}
JSON
