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
    "non-compliant"
  ],
  "percent_complete": 100,
  "findings": [
    "hammer thump bang"
  ],
  "actions": [
    "arrestor arrester air chamber secure"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "IPC"
  ],
  "sound_source": "fixture valve",
  "confidence": 1.0
}
JSON
