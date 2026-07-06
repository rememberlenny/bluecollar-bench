# Run Analysis - deepseek_v4_pro_text_20260706_182042

- Tasks scored: **1171**
- Catalog sha256: `d2fd79b23d2469a36d6a19eb8348db11a2658f9cd3118f79dcf1e5ab17b2a98e`
- Collected at: `2026-07-06T18:26:26+00:00`
- Mean reward: **0.669**
- Saturated (>=0.95): 11 (1%)
- Floored (<=0.05): 64
- **dangerous_false_pass** gate hits: 63
- **alarmist_false_fail** gate hits: 64

### By tier

| group | n | mean reward |
|---|---:|---:|
| T5 | 160 | 0.653 |
| T1 | 369 | 0.655 |
| T4 | 164 | 0.673 |
| T3 | 193 | 0.681 |
| T2 | 285 | 0.686 |

### By discipline

| group | n | mean reward |
|---|---:|---:|
| 2.8 | 58 | 0.568 |
| 2.9 | 58 | 0.628 |
| 2.7 | 72 | 0.644 |
| 2.4 | 105 | 0.655 |
| 2.10 | 40 | 0.660 |
| 2.1 | 350 | 0.661 |
| 2.2 | 102 | 0.680 |
| 2.6 | 54 | 0.681 |
| 2.12 | 122 | 0.697 |
| 2.11 | 68 | 0.701 |
| 2.3 | 70 | 0.704 |
| 2.5 | 72 | 0.742 |

### By task_type

| group | n | mean reward |
|---|---:|---:|
| SEQ | 128 | 0.611 |
| FD | 103 | 0.616 |
| PA | 80 | 0.629 |
| DOC | 80 | 0.633 |
| TRD | 80 | 0.643 |
| ME | 133 | 0.650 |
| TS | 80 | 0.662 |
| ID | 146 | 0.695 |
| CC | 229 | 0.714 |
| HAZ | 112 | 0.763 |

### By decision

| group | n | mean reward |
|---|---:|---:|
| 0.0 | 75 | 0.061 |
| 1.0 | 1096 | 0.711 |

### By modality

| group | n | mean reward |
|---|---:|---:|
| text | 1171 | 0.669 |

### By generation

| group | n | mean reward |
|---|---:|---:|
| curated | 12 | 0.567 |
| synthetic-text-rebalance-v2 | 250 | 0.617 |
| matrix-backfill | 237 | 0.672 |
| auto | 651 | 0.688 |
| curated-v2-trap | 3 | 0.692 |
| curated-v2-control | 8 | 0.734 |
| curated-v2-trd | 5 | 0.770 |
| curated-v2-nmi | 5 | 0.790 |

### Hardest 15 Items

| task | reward |
|---|---:|
| `ev-service-disconnect-gloves` | 0.000 |
| `loto-taped-breaker-no-try` | 0.000 |
| `structural-bolting-pretension` | 0.000 |
| `t1-c-201-seq-bf-006-concrete-placement` | 0.000 |
| `t1-e-102-pa-panelboard-installation-makeup` | 0.000 |
| `t1-e-201-me-emt-bending-installation` | 0.000 |
| `t1-e-204-me-boxes-fittings-fill` | 0.000 |
| `t1-i-101-fd-bf-004-transmitter-installation` | 0.000 |
| `t1-i-102-seq-bf-009-manifold-operations` | 0.000 |
| `t1-i-201-doc-calibration` | 0.000 |
| `t1-m-201-seq-bf-006-shaft-alignment` | 0.000 |
| `t1-m-301-ts-bf-007-bearings-seals` | 0.000 |
| `t1-m-302-ts-bf-008-belts-sheaves-couplings` | 0.000 |
| `t1-m-401-fd-conveyor-systems` | 0.000 |
| `t1-p-103-fd-bf-002-hangers-supports` | 0.000 |
