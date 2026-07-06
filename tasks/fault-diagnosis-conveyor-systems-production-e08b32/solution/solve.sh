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
    "degraded",
    "failed"
  ],
  "percent_complete": 100,
  "findings": [
    "cema guarding tracking",
    "nip entanglement spillage amputation"
  ],
  "actions": [
    "diagnose",
    "repair",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "CEMA",
    "OSHA 1910.212"
  ]
}
JSON
