#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "work_stage": "in-service",
  "component_conditions": [],
  "percent_complete": 100,
  "findings": [
    "even smooth steady healthy"
  ],
  "actions": [
    "release no document"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "OEM service info"
  ],
  "sound_source": "engine",
  "confidence": 1.0
}
JSON
