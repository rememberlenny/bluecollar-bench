# Run Analysis - gpt55_full_20260706_c48_openai_merged

- Tasks scored: **1299**
- Catalog sha256: `d2fd79b23d2469a36d6a19eb8348db11a2658f9cd3118f79dcf1e5ab17b2a98e`
- Collected at: `2026-07-06T19:31:51+00:00`
- Mean reward: **0.741**
- Saturated (>=0.95): 85 (7%)
- Floored (<=0.05): 12
- **dangerous_false_pass** gate hits: 8
- **alarmist_false_fail** gate hits: 4

### By tier

| group | n | mean reward |
|---|---:|---:|
| T1 | 397 | 0.719 |
| T2 | 323 | 0.734 |
| T3 | 203 | 0.742 |
| T5 | 172 | 0.751 |
| T4 | 204 | 0.785 |

### By discipline

| group | n | mean reward |
|---|---:|---:|
| 2.1 | 360 | 0.698 |
| 2.11 | 68 | 0.715 |
| 2.4 | 119 | 0.719 |
| 2.2 | 112 | 0.739 |
| 2.10 | 40 | 0.755 |
| 2.7 | 84 | 0.761 |
| 2.5 | 72 | 0.761 |
| 2.8 | 58 | 0.766 |
| 2.6 | 82 | 0.769 |
| 2.3 | 84 | 0.775 |
| 2.9 | 84 | 0.778 |
| 2.12 | 136 | 0.791 |

### By task_type

| group | n | mean reward |
|---|---:|---:|
| TRD | 80 | 0.699 |
| ID | 146 | 0.701 |
| PA | 80 | 0.709 |
| DOC | 94 | 0.715 |
| FD | 161 | 0.725 |
| ME | 161 | 0.740 |
| CC | 229 | 0.749 |
| TS | 80 | 0.761 |
| HAZ | 112 | 0.782 |
| RES | 28 | 0.794 |
| SEQ | 128 | 0.799 |

### By decision

| group | n | mean reward |
|---|---:|---:|
| 0.0 | 24 | 0.279 |
| 1.0 | 1275 | 0.750 |

### By modality

| group | n | mean reward |
|---|---:|---:|
| text | 1171 | 0.733 |
| audio | 44 | 0.736 |
| image | 84 | 0.856 |

### By generation

| group | n | mean reward |
|---|---:|---:|
| curated-v2-trd | 5 | 0.570 |
| synthetic-text-rebalance-v2 | 250 | 0.640 |
| curated-v2-control | 8 | 0.716 |
| synthetic-audio-v2 | 44 | 0.736 |
| auto | 651 | 0.756 |
| curated | 12 | 0.766 |
| matrix-backfill | 237 | 0.768 |
| curated-v2-nmi | 5 | 0.770 |
| synthetic-cpm-v2 | 28 | 0.794 |
| synthetic-media-v2 | 56 | 0.887 |
| curated-v2-trap | 3 | 0.950 |

### Hardest 15 Items

| task | reward |
|---|---:|
| `t1-e-303-cc-terminations-splices` | 0.000 |
| `t2-e-303-cc-terminations-splices` | 0.000 |
| `t3-e-303-cc-terminations-splices` | 0.000 |
| `v2-audio-hammer-000` | 0.000 |
| `v2-audio-hammer-008` | 0.000 |
| `v2-audio-hum-002` | 0.000 |
| `v2-audio-hum-004` | 0.000 |
| `v2-cpm-delay-001` | 0.000 |
| `v2-cpm-delay-009` | 0.000 |
| `v2-media-sling-004` | 0.000 |
| `v2-media-sling-009` | 0.000 |
| `v2-media-sling-011` | 0.000 |
| `t5-e-303-cc-terminations-splices` | 0.300 |
| `v2-text-pass-haz-t1-e-102-000` | 0.300 |
| `t5-e-105-doc-motor-circuits-disconnects` | 0.312 |
