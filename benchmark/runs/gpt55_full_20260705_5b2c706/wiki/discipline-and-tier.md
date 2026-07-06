# Discipline And Tier Breakdown

[Back to wiki index](README.md)

Discipline explains more than tier. Electrical was the weakest major discipline, while safety/rigging was the strongest. Tier means were close together and not monotonic.

## Discipline summary

| discipline | name | n | mean reward | <=0.50 | >=0.90 |
|---|---|---:|---:|---:|---:|
| 2.1 | 2.1 Electrical | 233 | 0.732 | 24 (10.3%) | 17 (7.3%) |
| 2.4 | 2.4 Structural & Ironwork | 91 | 0.741 | 6 (6.6%) | 17 (18.7%) |
| 2.11 | 2.11 Sitework & Utilities | 51 | 0.747 | 6 (11.8%) | 6 (11.8%) |
| 2.2 | 2.2 Mechanical - Piping & Plumbing | 97 | 0.754 | 7 (7.2%) | 14 (14.4%) |
| 2.7 | 2.7 Equipment & Machinery | 78 | 0.770 | 7 (9.0%) | 17 (21.8%) |
| 2.6 | 2.6 Carpentry & Finishes | 79 | 0.774 | 3 (3.8%) | 14 (17.7%) |
| 2.9 | 2.9 Automotive & Powertrain | 82 | 0.778 | 12 (14.6%) | 30 (36.6%) |
| 2.10 | 2.10 Assembly & Fabrication | 30 | 0.778 | 0 (0.0%) | 1 (3.3%) |
| 2.5 | 2.5 Concrete & Masonry | 61 | 0.779 | 1 (1.6%) | 4 (6.6%) |
| 2.3 | 2.3 HVAC-R | 80 | 0.783 | 6 (7.5%) | 16 (20.0%) |
| 2.8 | 2.8 Instrumentation & Controls | 50 | 0.784 | 3 (6.0%) | 5 (10.0%) |
| 2.12 | 2.12 Safety & Rigging | 117 | 0.818 | 4 (3.4%) | 32 (27.4%) |

## Tier summary

| tier | n | mean reward | <=0.50 | >=0.90 |
|---|---:|---:|---:|---:|
| T2 | 270 | 0.753 | 21 (7.8%) | 36 (13.3%) |
| T5 | 162 | 0.755 | 14 (8.6%) | 19 (11.7%) |
| T3 | 176 | 0.757 | 13 (7.4%) | 23 (13.1%) |
| T1 | 245 | 0.772 | 14 (5.7%) | 35 (14.3%) |
| T4 | 196 | 0.789 | 17 (8.7%) | 60 (30.6%) |

## What this means

- **Electrical is the first regression target.** It had the lowest mean and the most low-score tasks, including repeated terminations/splices failures.
- **Safety & rigging is a relative strength.** It had the best discipline mean and many high-scoring HAZ/TS examples.
- **Tier alone is a poor predictor.** T4 was the strongest tier by mean, while T2/T5/T3 were close together. Future analysis should stratify by task type before drawing conclusions from tier.

## 2.1: 2.1 Electrical

Mean reward: **0.732** over **233** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t4-e-103-ts-overcurrent-device-selection-coo`](../../../../tasks/t4-e-103-ts-overcurrent-device-selection-coo/task.toml) | 0.975 | TS | text | T4 | fail/high | E-103 Overcurrent device selection & coordination |
| [`v2-audio-hum-009`](../../../../tasks/v2-audio-hum-009/task.toml) | 0.925 | FD | audio | T2 | fail/critical | E-303 Terminations & splices |
| [`t4-e-303-ts-terminations-splices`](../../../../tasks/t4-e-303-ts-terminations-splices/task.toml) | 0.925 | TS | text | T4 | fail/medium | E-303 Terminations & splices |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t1-e-303-cc-terminations-splices`](../../../../tasks/t1-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T1 | fail/high | E-303 Terminations & splices |
| [`t2-e-303-cc-terminations-splices`](../../../../tasks/t2-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T2 | fail/high | E-303 Terminations & splices |
| [`t3-e-303-cc-terminations-splices`](../../../../tasks/t3-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T3 | fail/high | E-303 Terminations & splices |

## 2.4: 2.4 Structural & Ironwork

Mean reward: **0.741** over **91** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-sling-008`](../../../../tasks/v2-media-sling-008/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-sling-006`](../../../../tasks/v2-media-sling-006/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-sling-000`](../../../../tasks/v2-media-sling-000/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-sling-004`](../../../../tasks/v2-media-sling-004/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-009`](../../../../tasks/v2-media-sling-009/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-011`](../../../../tasks/v2-media-sling-011/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |

## 2.11: 2.11 Sitework & Utilities

Mean reward: **0.747** over **51** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t2-u-101-haz-bf-004-trench-protection`](../../../../tasks/t2-u-101-haz-bf-004-trench-protection/task.toml) | 0.950 | HAZ | text | T2 | fail/critical | U-101 Trench protection |
| [`t2-u-201-cc-locates-marking`](../../../../tasks/t2-u-201-cc-locates-marking/task.toml) | 0.900 | CC | text | T2 | fail/high | U-201 Locates & marking |
| [`t2-u-201-cc-bf-001-locates-marking`](../../../../tasks/t2-u-201-cc-bf-001-locates-marking/task.toml) | 0.900 | CC | text | T2 | fail/high | U-201 Locates & marking |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t1-u-201-id-locates-marking`](../../../../tasks/t1-u-201-id-locates-marking/task.toml) | 0.362 | ID | text | T1 | fail/medium | U-201 Locates & marking |
| [`t4-u-101-haz-bf-000-trench-protection`](../../../../tasks/t4-u-101-haz-bf-000-trench-protection/task.toml) | 0.425 | HAZ | text | T4 | fail/critical | U-101 Trench protection |
| [`t2-u-101-haz-bf-000-trench-protection`](../../../../tasks/t2-u-101-haz-bf-000-trench-protection/task.toml) | 0.450 | HAZ | text | T2 | fail/critical | U-101 Trench protection |

## 2.2: 2.2 Mechanical - Piping & Plumbing

Mean reward: **0.754** over **97** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-nmi-p201-t3-concealed-vent`](../../../../tasks/v2-nmi-p201-t3-concealed-vent/task.toml) | 0.950 | CC | text | T3 | needs_more_info/medium | P-201 Traps & venting |
| [`v2-audio-hammer-006`](../../../../tasks/v2-audio-hammer-006/task.toml) | 0.950 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-004`](../../../../tasks/v2-audio-hammer-004/task.toml) | 0.950 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-audio-hammer-000`](../../../../tasks/v2-audio-hammer-000/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-008`](../../../../tasks/v2-audio-hammer-008/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`t4-p-401-fd-boiler-pump-piping`](../../../../tasks/t4-p-401-fd-boiler-pump-piping/task.toml) | 0.350 | FD | text | T4 | fail/high | P-401 Boiler & pump piping |

## 2.7: 2.7 Equipment & Machinery

Mean reward: **0.770** over **78** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-audio-bearing-009`](../../../../tasks/v2-audio-bearing-009/task.toml) | 0.950 | FD | audio | T5 | pass/low | M-301 Bearings & seals |
| [`v2-audio-bearing-003`](../../../../tasks/v2-audio-bearing-003/task.toml) | 0.950 | FD | audio | T5 | pass/low | M-301 Bearings & seals |
| [`v2-audio-bearing-000`](../../../../tasks/v2-audio-bearing-000/task.toml) | 0.950 | FD | audio | T5 | pass/low | M-301 Bearings & seals |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t5-m-302-fd-belts-sheaves-couplings`](../../../../tasks/t5-m-302-fd-belts-sheaves-couplings/task.toml) | 0.362 | FD | text | T5 | fail/high | M-302 Belts, sheaves & couplings |
| [`t1-m-302-me-bf-003-belts-sheaves-couplings`](../../../../tasks/t1-m-302-me-bf-003-belts-sheaves-couplings/task.toml) | 0.375 | ME | text | T1 | fail/medium | M-302 Belts, sheaves & couplings |
| [`t4-m-302-me-bf-003-belts-sheaves-couplings`](../../../../tasks/t4-m-302-me-bf-003-belts-sheaves-couplings/task.toml) | 0.375 | ME | text | T4 | fail/medium | M-302 Belts, sheaves & couplings |

## 2.6: 2.6 Carpentry & Finishes

Mean reward: **0.774** over **79** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-cpm-delay-007`](../../../../tasks/v2-cpm-delay-007/task.toml) | 1.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-cpm-delay-005`](../../../../tasks/v2-cpm-delay-005/task.toml) | 1.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-trap-f301-t3-screw-pops`](../../../../tasks/v2-trap-f301-t3-screw-pops/task.toml) | 0.950 | CC | text | T3 | pass/low | F-301 Drywall & finishing |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-cpm-delay-001`](../../../../tasks/v2-cpm-delay-001/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-cpm-delay-009`](../../../../tasks/v2-cpm-delay-009/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-cpm-delay-010`](../../../../tasks/v2-cpm-delay-010/task.toml) | 0.425 | RES | image | T2 | pass/low | RES Schedule & constraint reasoning |

## 2.9: 2.9 Automotive & Powertrain

Mean reward: **0.778** over **82** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-rotor-013`](../../../../tasks/v2-media-rotor-013/task.toml) | 1.000 | ME | image | T4 | needs_more_info/medium | A-201 Brakes |
| [`v2-media-rotor-012`](../../../../tasks/v2-media-rotor-012/task.toml) | 1.000 | ME | image | T4 | pass/low | A-201 Brakes |
| [`v2-media-rotor-010`](../../../../tasks/v2-media-rotor-010/task.toml) | 1.000 | ME | image | T4 | pass/low | A-201 Brakes |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t4-a-401-id-high-voltage-safety`](../../../../tasks/t4-a-401-id-high-voltage-safety/task.toml) | 0.362 | ID | text | T4 | fail/critical | A-401 High-voltage safety |
| [`t5-a-102-id-bf-009-fluids-leaks`](../../../../tasks/t5-a-102-id-bf-009-fluids-leaks/task.toml) | 0.362 | ID | text | T5 | fail/medium | A-102 Fluids & leaks |
| [`t4-a-102-id-fluids-leaks`](../../../../tasks/t4-a-102-id-fluids-leaks/task.toml) | 0.400 | ID | text | T4 | fail/medium | A-102 Fluids & leaks |

## 2.10: 2.10 Assembly & Fabrication

Mean reward: **0.778** over **30** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t5-b-301-trd-standard-work-execution`](../../../../tasks/t5-b-301-trd-standard-work-execution/task.toml) | 0.900 | TRD | text | T5 | fail/high | B-301 Standard work execution |
| [`t5-b-302-seq-andon-quality-response`](../../../../tasks/t5-b-302-seq-andon-quality-response/task.toml) | 0.875 | SEQ | text | T5 | fail/high | B-302 Andon & quality response |
| [`t5-b-101-seq-torque-threaded-fastening`](../../../../tasks/t5-b-101-seq-torque-threaded-fastening/task.toml) | 0.875 | SEQ | text | T5 | fail/high | B-101 Torque & threaded fastening |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t4-b-101-cc-torque-threaded-fastening`](../../../../tasks/t4-b-101-cc-torque-threaded-fastening/task.toml) | 0.650 | CC | text | T4 | fail/high | B-101 Torque & threaded fastening |
| [`v2-trd-b101-t5-tty-reuse`](../../../../tasks/v2-trd-b101-t5-tty-reuse/task.toml) | 0.650 | TRD | text | T5 | fail/high | B-101 Torque & threaded fastening |
| [`t5-b-102-id-production-welding`](../../../../tasks/t5-b-102-id-production-welding/task.toml) | 0.675 | ID | text | T5 | fail/medium | B-102 Production welding |

## 2.5: 2.5 Concrete & Masonry

Mean reward: **0.779** over **61** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-trap-c301-t2-efflorescence`](../../../../tasks/v2-trap-c301-t2-efflorescence/task.toml) | 0.950 | ID | text | T2 | pass/low | C-301 Block/brick laying |
| [`t3-c-101-haz-bf-000-form-build-bracing`](../../../../tasks/t3-c-101-haz-bf-000-form-build-bracing/task.toml) | 0.950 | HAZ | text | T3 | fail/critical | C-101 Form build & bracing |
| [`t3-c-201-haz-concrete-placement`](../../../../tasks/t3-c-201-haz-concrete-placement/task.toml) | 0.900 | HAZ | text | T3 | fail/critical | C-201 Concrete placement |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t3-c-101-haz-form-build-bracing`](../../../../tasks/t3-c-101-haz-form-build-bracing/task.toml) | 0.400 | HAZ | text | T3 | fail/critical | C-101 Form build & bracing |
| [`t1-c-201-fd-bf-001-concrete-placement`](../../../../tasks/t1-c-201-fd-bf-001-concrete-placement/task.toml) | 0.600 | FD | text | T1 | fail/high | C-201 Concrete placement |
| [`t2-c-201-fd-concrete-placement`](../../../../tasks/t2-c-201-fd-concrete-placement/task.toml) | 0.600 | FD | text | T2 | fail/high | C-201 Concrete placement |

## 2.3: 2.3 HVAC-R

Mean reward: **0.783** over **80** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-micron-012`](../../../../tasks/v2-media-micron-012/task.toml) | 1.000 | FD | image | T4 | pass/low | H-301 Brazing & evacuation |
| [`v2-media-micron-009`](../../../../tasks/v2-media-micron-009/task.toml) | 1.000 | FD | image | T4 | pass/low | H-301 Brazing & evacuation |
| [`v2-media-micron-008`](../../../../tasks/v2-media-micron-008/task.toml) | 1.000 | FD | image | T4 | fail/medium | H-301 Brazing & evacuation |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t3-h-301-fd-brazing-evacuation`](../../../../tasks/t3-h-301-fd-brazing-evacuation/task.toml) | 0.388 | FD | text | T3 | fail/high | H-301 Brazing & evacuation |
| [`t1-h-101-cc-bf-000-condenser-heat-pump-sett`](../../../../tasks/t1-h-101-cc-bf-000-condenser-heat-pump-sett/task.toml) | 0.400 | CC | text | T1 | fail/high | H-101 Condenser/heat pump setting |
| [`t3-h-101-cc-bf-000-condenser-heat-pump-sett`](../../../../tasks/t3-h-101-cc-bf-000-condenser-heat-pump-sett/task.toml) | 0.400 | CC | text | T3 | fail/high | H-101 Condenser/heat pump setting |

## 2.8: 2.8 Instrumentation & Controls

Mean reward: **0.784** over **50** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t5-i-102-seq-bf-001-manifold-operations`](../../../../tasks/t5-i-102-seq-bf-001-manifold-operations/task.toml) | 0.900 | SEQ | text | T5 | fail/high | I-102 Manifold operations |
| [`t4-i-102-seq-bf-001-manifold-operations`](../../../../tasks/t4-i-102-seq-bf-001-manifold-operations/task.toml) | 0.900 | SEQ | text | T4 | fail/high | I-102 Manifold operations |
| [`t4-i-101-cc-bf-000-transmitter-installation`](../../../../tasks/t4-i-101-cc-bf-000-transmitter-installation/task.toml) | 0.900 | CC | text | T4 | fail/high | I-101 Transmitter installation |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t5-i-101-fd-bf-004-transmitter-installation`](../../../../tasks/t5-i-101-fd-bf-004-transmitter-installation/task.toml) | 0.375 | FD | text | T5 | fail/high | I-101 Transmitter installation |
| [`t1-i-201-fd-bf-002-calibration`](../../../../tasks/t1-i-201-fd-bf-002-calibration/task.toml) | 0.450 | FD | text | T1 | fail/high | I-201 Calibration |
| [`t4-i-201-fd-bf-002-calibration`](../../../../tasks/t4-i-201-fd-bf-002-calibration/task.toml) | 0.500 | FD | text | T4 | fail/high | I-201 Calibration |

## 2.12: 2.12 Safety & Rigging

Mean reward: **0.818** over **117** tasks.

#### Success examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-gasmeter-013`](../../../../tasks/v2-media-gasmeter-013/task.toml) | 1.000 | DOC | image | T1 | pass/low | X-103 Confined space |
| [`v2-media-gasmeter-007`](../../../../tasks/v2-media-gasmeter-007/task.toml) | 1.000 | DOC | image | T1 | pass/low | X-103 Confined space |
| [`v2-media-gasmeter-006`](../../../../tasks/v2-media-gasmeter-006/task.toml) | 1.000 | DOC | image | T1 | pass/low | X-103 Confined space |

#### Failure examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t2-x-101-id-lockout-tagout`](../../../../tasks/t2-x-101-id-lockout-tagout/task.toml) | 0.362 | ID | text | T2 | fail/critical | X-101 Lockout/Tagout |
| [`t3-x-101-cc-lockout-tagout`](../../../../tasks/t3-x-101-cc-lockout-tagout/task.toml) | 0.425 | CC | text | T3 | fail/critical | X-101 Lockout/Tagout |
| [`t4-x-106-haz-bf-005-housekeeping-general-haz`](../../../../tasks/t4-x-106-haz-bf-005-housekeeping-general-haz/task.toml) | 0.425 | HAZ | text | T4 | fail/critical | X-106 Housekeeping & general hazard recognition |
