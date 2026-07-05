#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "in-progress",
  "s2_conditions": [],
  "s3_percent": 40,
  "findings": [
    "float slack absorbed non-critical"
  ],
  "actions": [
    "monitor proceed resequence document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "CPM computed ground truth",
    "expansion-plan track 3"
  ],
  "value": 0
}
JSON
