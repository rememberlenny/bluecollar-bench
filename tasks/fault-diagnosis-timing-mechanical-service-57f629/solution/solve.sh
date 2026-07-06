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
    "degraded"
  ],
  "percent_complete": 100,
  "findings": [
    "random irregular intermittent"
  ],
  "actions": [
    "fuel vacuum test investigate"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM service info"
  ],
  "sound_source": "engine",
  "confidence": 1.0
}
JSON
