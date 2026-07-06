#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "in-service",
  "component_conditions": [
    "worn"
  ],
  "percent_complete": 100,
  "findings": [
    "tick periodic early faint"
  ],
  "actions": [
    "schedule plan vibration trend"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "SKF/Timken guides"
  ],
  "sound_source": "bearing",
  "confidence": 1.0
}
JSON
