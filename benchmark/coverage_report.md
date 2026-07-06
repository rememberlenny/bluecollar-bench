# Blue-Collar Benchmark Coverage Report

- Source elements parsed: 95
- Runnable items generated: 1299

## By Generation

| Generation | Items |
|---|---:|
| auto | 651 |
| curated | 12 |
| curated-v2-control | 8 |
| curated-v2-nmi | 5 |
| curated-v2-trap | 3 |
| curated-v2-trd | 5 |
| matrix-backfill | 237 |
| synthetic-audio-v2 | 44 |
| synthetic-cpm-v2 | 28 |
| synthetic-media-v2 | 56 |
| synthetic-text-rebalance-v2 | 250 |

## By Discipline

| Discipline | Items | Source elements |
|---|---:|---:|
| 2.1 Electrical | 360 | 25 |
| 2.2 Mechanical - Piping & Plumbing | 112 | 11 |
| 2.3 HVAC-R | 84 | 7 |
| 2.4 Structural & Ironwork | 119 | 7 |
| 2.5 Concrete & Masonry | 72 | 5 |
| 2.6 Carpentry & Finishes | 82 | 7 |
| 2.7 Equipment & Machinery | 84 | 5 |
| 2.8 Instrumentation & Controls | 58 | 4 |
| 2.9 Automotive & Powertrain | 84 | 8 |
| 2.10 Assembly & Fabrication | 40 | 6 |
| 2.11 Sitework & Utilities | 68 | 4 |
| 2.12 Safety & Rigging | 136 | 6 |

## By Tier

| Tier | Items |
|---|---:|
| T1 | 397 |
| T2 | 323 |
| T3 | 203 |
| T4 | 204 |
| T5 | 172 |

## By Task Type

| Task type | Items |
|---|---:|
| ID Identification | 146 |
| FD Fault diagnosis | 161 |
| CC Code/spec compliance | 229 |
| SEQ Procedure sequencing | 128 |
| TS Tool & material selection | 80 |
| HAZ Hazard spotting | 112 |
| ME Measurement & estimation | 161 |
| PA Progress assessment | 80 |
| DOC Document interpretation | 94 |
| TRD Tradeoff judgment | 80 |
| RES Resource/constraint recovery | 28 |

## Coverage Matrix

Counts are generated items in each Tier x Discipline cell. Matrix status follows the v0.1 taxonomy: core, secondary, or out of scope.
Targets: core >=20 items, secondary >=5 items, out = 0 required items.

| Discipline | T1 | T2 | T3 | T4 | T5 |
|---|---:|---:|---:|---:|---:|
| 2.1 Electrical | 132 (core) | 113 (core) | 65 (core) | 29 (core) | 21 (secondary) |
| 2.2 Mechanical - Piping & Plumbing | 33 (core) | 21 (core) | 33 (core) | 20 (core) | 5 (secondary) |
| 2.3 HVAC-R | 5 (secondary) | 22 (core) | 22 (core) | 35 (core) | 0 (out) |
| 2.4 Structural & Ironwork | 55 (core) | 37 (core) | 7 (secondary) | 0 (out) | 20 (core) |
| 2.5 Concrete & Masonry | 27 (core) | 23 (core) | 22 (core) | 0 (out) | 0 (out) |
| 2.6 Carpentry & Finishes | 0 (out) | 49 (core) | 23 (core) | 5 (secondary) | 5 (secondary) |
| 2.7 Equipment & Machinery | 27 (core) | 5 (secondary) | 0 (out) | 20 (core) | 32 (core) |
| 2.8 Instrumentation & Controls | 28 (core) | 5 (secondary) | 0 (out) | 5 (secondary) | 20 (core) |
| 2.9 Automotive & Powertrain | 0 (out) | 0 (out) | 5 (secondary) | 59 (core) | 20 (core) |
| 2.10 Assembly & Fabrication | 5 (secondary) | 0 (out) | 0 (out) | 6 (out) | 29 (core) |
| 2.11 Sitework & Utilities | 33 (core) | 25 (core) | 5 (secondary) | 5 (secondary) | 0 (out) |
| 2.12 Safety & Rigging | 52 (core) | 23 (core) | 21 (core) | 20 (core) | 20 (core) |

## Gaps

- No core or secondary Tier x Discipline cell is under target.
