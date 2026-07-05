#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "s1_state": "in-service",
  "s2_conditions": [
    "degraded"
  ],
  "s3_percent": 100,
  "findings": [
    "single one regular repeating"
  ],
  "actions": [
    "cylinder identify coil plug test"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM service info"
  ],
  "sound_source": "engine",
  "confidence": 1.0
}
JSON
