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
    "steady hum magnetic normal"
  ],
  "actions": [
    "no monitor document"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "NEC 110.14"
  ],
  "sound_source": "electrical panel",
  "confidence": 1.0
}
JSON
