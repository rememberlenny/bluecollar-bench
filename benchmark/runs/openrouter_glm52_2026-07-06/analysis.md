# Run Analysis - openrouter_glm52_2026-07-06

- Tasks scored: **1299**
- Catalog sha256: `d2fd79b23d2469a36d6a19eb8348db11a2658f9cd3118f79dcf1e5ab17b2a98e`
- Collected at: `2026-07-06T18:27:35+00:00`
- Mean reward: **0.656**
- Saturated (>=0.95): 28 (2%)
- Floored (<=0.05): 164
- **dangerous_false_pass** gate hits: 36
- **alarmist_false_fail** gate hits: 34

### By tier

| group | n | mean reward |
|---|---:|---:|
| T4 | 204 | 0.610 |
| T1 | 397 | 0.646 |
| T2 | 323 | 0.655 |
| T5 | 172 | 0.670 |
| T3 | 203 | 0.711 |

### By discipline

| group | n | mean reward |
|---|---:|---:|
| 2.9 | 84 | 0.510 |
| 2.6 | 82 | 0.511 |
| 2.7 | 84 | 0.594 |
| 2.4 | 119 | 0.609 |
| 2.3 | 84 | 0.646 |
| 2.12 | 136 | 0.654 |
| 2.1 | 360 | 0.690 |
| 2.11 | 68 | 0.694 |
| 2.10 | 40 | 0.704 |
| 2.2 | 112 | 0.707 |
| 2.8 | 58 | 0.739 |
| 2.5 | 72 | 0.773 |

### By task_type

| group | n | mean reward |
|---|---:|---:|
| RES | 28 | 0.000 |
| FD | 161 | 0.447 |
| ME | 161 | 0.555 |
| DOC | 94 | 0.590 |
| TRD | 80 | 0.659 |
| PA | 80 | 0.698 |
| ID | 146 | 0.726 |
| TS | 80 | 0.731 |
| SEQ | 128 | 0.741 |
| CC | 229 | 0.781 |
| HAZ | 112 | 0.790 |

### By decision

| group | n | mean reward |
|---|---:|---:|
| pass | 51 | 0.000 |
| fail | 69 | 0.000 |
| needs_more_info | 8 | 0.000 |
| 0.0 | 40 | 0.046 |
| 1.0 | 1131 | 0.751 |

### By modality

| group | n | mean reward |
|---|---:|---:|
| audio | 44 | 0.000 |
| image | 84 | 0.000 |
| text | 1171 | 0.727 |

### By generation

| group | n | mean reward |
|---|---:|---:|
| synthetic-audio-v2 | 44 | 0.000 |
| synthetic-cpm-v2 | 28 | 0.000 |
| synthetic-media-v2 | 56 | 0.000 |
| synthetic-text-rebalance-v2 | 250 | 0.628 |
| curated-v2-trd | 5 | 0.670 |
| curated | 12 | 0.737 |
| curated-v2-control | 8 | 0.745 |
| auto | 651 | 0.754 |
| matrix-backfill | 237 | 0.756 |
| curated-v2-trap | 3 | 0.792 |
| curated-v2-nmi | 5 | 0.900 |

### Hardest 15 Items

| task | reward |
|---|---:|
| `t1-c-302-cc-bf-004-flashing-weeps` | 0.000 |
| `t1-e-202-seq-rigid-pvc-conduit` | 0.000 |
| `t1-e-203-haz-cable-tray` | 0.000 |
| `t1-e-303-cc-terminations-splices` | 0.000 |
| `t1-m-101-me-baseplates-anchor-bolts` | 0.000 |
| `t1-m-101-seq-baseplates-anchor-bolts` | 0.000 |
| `t1-m-401-fd-conveyor-systems` | 0.000 |
| `t1-u-202-me-bf-002-pipe-bedding-backfill` | 0.000 |
| `t1-x-105-ts-ppe-selection` | 0.000 |
| `t2-e-103-me-overcurrent-device-selection-coo` | 0.000 |
| `t2-e-303-cc-terminations-splices` | 0.000 |
| `t2-f-201-id-flashing-wrb-integration` | 0.000 |
| `t2-m-101-cc-bf-000-baseplates-anchor-bolts` | 0.000 |
| `t2-s-101-me-column-beam-erection-plumb` | 0.000 |
| `t2-u-101-haz-bf-000-trench-protection` | 0.000 |
