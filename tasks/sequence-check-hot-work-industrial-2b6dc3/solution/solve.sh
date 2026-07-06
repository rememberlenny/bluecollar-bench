#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "work_stage": "in-progress",
  "component_conditions": [],
  "percent_complete": 90,
  "findings": [
    "sequenced",
    "prerequisites",
    "ready"
  ],
  "actions": [
    "document",
    "release"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "NFPA 51B",
    "OSHA 1926 Subpart J"
  ]
}
JSON
