# Run Analysis - gpt55_full_20260705_5b2c706

- Tasks scored: **1049**
- Catalog sha256: `3d917f30ba6d3ee7811c082f3839aa0e2c3cc9e42578b1b7320a058b68901373`
- Collected at: `2026-07-05T23:21:23+00:00`
- Mean reward: **0.765**
- Saturated (>=0.95): 85 (8%)
- Floored (<=0.05): 12
- **dangerous_false_pass** gate hits: 8
- **alarmist_false_fail** gate hits: 4

### By tier

| group | n | mean reward |
|---|---:|---:|
| T2 | 270 | 0.753 |
| T5 | 162 | 0.755 |
| T3 | 176 | 0.757 |
| T1 | 245 | 0.772 |
| T4 | 196 | 0.789 |

### By discipline

| group | n | mean reward |
|---|---:|---:|
| 2.1 | 233 | 0.732 |
| 2.4 | 91 | 0.741 |
| 2.11 | 51 | 0.747 |
| 2.2 | 97 | 0.754 |
| 2.7 | 78 | 0.770 |
| 2.6 | 79 | 0.774 |
| 2.9 | 82 | 0.778 |
| 2.10 | 30 | 0.778 |
| 2.5 | 61 | 0.779 |
| 2.3 | 80 | 0.783 |
| 2.8 | 50 | 0.784 |
| 2.12 | 117 | 0.818 |

### By task_type

| group | n | mean reward |
|---|---:|---:|
| ID | 126 | 0.709 |
| FD | 149 | 0.730 |
| DOC | 74 | 0.735 |
| TRD | 31 | 0.752 |
| ME | 147 | 0.752 |
| CC | 209 | 0.760 |
| PA | 35 | 0.792 |
| RES | 28 | 0.794 |
| SEQ | 108 | 0.827 |
| HAZ | 92 | 0.828 |
| TS | 50 | 0.841 |

### By decision

| group | n | mean reward |
|---|---:|---:|
| 0.0 | 24 | 0.279 |
| 1.0 | 1025 | 0.777 |

### By modality

| group | n | mean reward |
|---|---:|---:|
| audio | 44 | 0.736 |
| text | 921 | 0.758 |
| image | 84 | 0.856 |

### By generation

| group | n | mean reward |
|---|---:|---:|
| curated-v2-trd | 5 | 0.570 |
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
| `t5-e-105-doc-motor-circuits-disconnects` | 0.312 |
| `t2-e-602-id-equipment-bonding` | 0.338 |
