# Run Analysis - deepseek_v4_pro_text_natural_20260706

- Tasks scored: **1171**
- Catalog sha256: `aa0631b805deaf095fb665a82992fb11102cba6e1c7b38752726b5d3d2f8cb77`
- Collected at: `2026-07-06T21:28:07+00:00`
- Mean reward: **0.681**
- Saturated (>=0.95): 26 (2%)
- Floored (<=0.05): 91
- **dangerous_false_pass** gate hits: 85
- **alarmist_false_fail** gate hits: 89

### By tier

| group | n | mean reward |
|---|---:|---:|
| T4 | 164 | 0.642 |
| T1 | 369 | 0.669 |
| T3 | 193 | 0.686 |
| T2 | 285 | 0.690 |
| T5 | 160 | 0.722 |

### By discipline

| group | n | mean reward |
|---|---:|---:|
| 2.9 | 58 | 0.641 |
| 2.1 | 350 | 0.651 |
| 2.10 | 40 | 0.661 |
| 2.12 | 122 | 0.673 |
| 2.11 | 68 | 0.678 |
| 2.7 | 72 | 0.685 |
| 2.3 | 70 | 0.697 |
| 2.6 | 54 | 0.699 |
| 2.4 | 105 | 0.711 |
| 2.5 | 72 | 0.713 |
| 2.2 | 102 | 0.721 |
| 2.8 | 58 | 0.722 |

### By task_type

| group | n | mean reward |
|---|---:|---:|
| SEQ | 128 | 0.570 |
| PA | 80 | 0.610 |
| TRD | 80 | 0.619 |
| FD | 103 | 0.661 |
| DOC | 80 | 0.674 |
| TS | 80 | 0.682 |
| ME | 133 | 0.683 |
| ID | 146 | 0.727 |
| HAZ | 112 | 0.730 |
| CC | 229 | 0.745 |

### By decision

| group | n | mean reward |
|---|---:|---:|
| 0.0 | 107 | 0.058 |
| 1.0 | 1064 | 0.743 |

### By modality

| group | n | mean reward |
|---|---:|---:|
| text | 1171 | 0.681 |

### By generation

| group | n | mean reward |
|---|---:|---:|
| synthetic-text-rebalance-v2 | 250 | 0.605 |
| curated-v2-nmi | 5 | 0.650 |
| curated | 12 | 0.686 |
| auto | 651 | 0.688 |
| matrix-backfill | 237 | 0.732 |
| curated-v2-control | 8 | 0.758 |
| curated-v2-trd | 5 | 0.790 |
| curated-v2-trap | 3 | 0.942 |

### Hardest 15 Items

| task | reward |
|---|---:|
| `compliance-check-high-voltage-safety-service-d3ddff` | 0.000 |
| `compliance-check-locates-marking-industrial-760e80` | 0.000 |
| `compliance-check-terminations-splices-commercial-e403fc` | 0.000 |
| `compliance-check-terminations-splices-production-bd611e` | 0.000 |
| `compliance-check-terminations-splices-residential-a32022` | 0.000 |
| `document-check-charging-diagnostics-service-8421d1` | 0.000 |
| `document-check-confined-space-industrial-d74543` | 0.000 |
| `document-check-crane-operations-commercial-d54b51` | 0.000 |
| `document-check-crane-operations-industrial-2886a2` | 0.000 |
| `document-check-diagnostics-production-f65a3a` | 0.000 |
| `drain-vent-path-assessment-residential-371dee` | 0.000 |
| `fault-diagnosis-bearings-seals-service-dd6e49` | 0.000 |
| `fault-diagnosis-calibration-production-90332d` | 0.000 |
| `fault-diagnosis-calibration-service-d0eafe` | 0.000 |
| `fault-diagnosis-charging-diagnostics-service-e3b4dc` | 0.000 |
