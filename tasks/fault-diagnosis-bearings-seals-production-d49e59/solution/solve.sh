#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "in-service",
  "component_conditions": [
    "failed",
    "degraded"
  ],
  "percent_complete": 100,
  "findings": [
    "growl knock severe loud"
  ],
  "actions": [
    "remove replace shutdown immediately"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "SKF/Timken guides"
  ],
  "sound_source": "bearing",
  "confidence": 1.0
}
JSON
