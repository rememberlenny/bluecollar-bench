# Modality And Media Breakdown

[Back to wiki index](README.md)

The modality story is not simply text versus media.
Image tasks were the best group on average, but the severe misses were also visually grounded.
Audio was the most volatile modality.

| modality | n | mean reward | <=0.50 | >=0.90 |
|---|---:|---:|---:|---:|
| audio | 44 | 0.736 | 10 (22.7%) | 19 (43.2%) |
| text | 921 | 0.758 | 62 (6.7%) | 99 (10.7%) |
| image | 84 | 0.856 | 7 (8.3%) | 55 (65.5%) |

## Image

Image tasks had the highest mean and many perfect scores, especially gas-meter reads, HVAC-R micron-gauge examples, rotor measurements, and several CPM constraints. The weak side is critical measurement and scheduling interpretation, where the wrong final decision can zero the task.

#### Image successes

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-media-sling-008`](../../../../tasks/v2-media-sling-008/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-sling-006`](../../../../tasks/v2-media-sling-006/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-sling-000`](../../../../tasks/v2-media-sling-000/task.toml) | 1.000 | ME | image | T1 | pass/low | S-301 Rigging configuration |
| [`v2-media-rotor-013`](../../../../tasks/v2-media-rotor-013/task.toml) | 1.000 | ME | image | T4 | needs_more_info/medium | A-201 Brakes |
| [`v2-media-rotor-012`](../../../../tasks/v2-media-rotor-012/task.toml) | 1.000 | ME | image | T4 | pass/low | A-201 Brakes |
| [`v2-media-rotor-010`](../../../../tasks/v2-media-rotor-010/task.toml) | 1.000 | ME | image | T4 | pass/low | A-201 Brakes |

#### Image failures

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-cpm-delay-001`](../../../../tasks/v2-cpm-delay-001/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-cpm-delay-009`](../../../../tasks/v2-cpm-delay-009/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-media-sling-004`](../../../../tasks/v2-media-sling-004/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-009`](../../../../tasks/v2-media-sling-009/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-011`](../../../../tasks/v2-media-sling-011/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-cpm-delay-010`](../../../../tasks/v2-cpm-delay-010/task.toml) | 0.425 | RES | image | T2 | pass/low | RES Schedule & constraint reasoning |

## Audio

Audio tasks had the highest low-score rate. Bearing and engine examples often scored well, but hum/hammer items show that sound-source and low-risk/pass judgments are brittle.

#### Audio successes

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-audio-hammer-006`](../../../../tasks/v2-audio-hammer-006/task.toml) | 0.950 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-004`](../../../../tasks/v2-audio-hammer-004/task.toml) | 0.950 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-002`](../../../../tasks/v2-audio-hammer-002/task.toml) | 0.950 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-001`](../../../../tasks/v2-audio-hammer-001/task.toml) | 0.950 | FD | audio | T3 | fail/medium | P-301 PEX & copper installation |
| [`v2-audio-engine-011`](../../../../tasks/v2-audio-engine-011/task.toml) | 0.950 | FD | audio | T4 | fail/medium | A-101 Timing & mechanical |
| [`v2-audio-engine-010`](../../../../tasks/v2-audio-engine-010/task.toml) | 0.950 | FD | audio | T4 | fail/medium | A-101 Timing & mechanical |

#### Audio failures

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-audio-hammer-000`](../../../../tasks/v2-audio-hammer-000/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-008`](../../../../tasks/v2-audio-hammer-008/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hum-002`](../../../../tasks/v2-audio-hum-002/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-audio-hum-004`](../../../../tasks/v2-audio-hum-004/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-audio-hum-001`](../../../../tasks/v2-audio-hum-001/task.toml) | 0.350 | FD | audio | T2 | fail/critical | E-303 Terminations & splices |
| [`v2-audio-hammer-009`](../../../../tasks/v2-audio-hammer-009/task.toml) | 0.463 | FD | audio | T3 | fail/medium | P-301 PEX & copper installation |

## Text

Text tasks are broad and therefore average out near the overall mean. The strongest text examples are structured hazard, sequence, and tool-selection tasks. The weakest are detailed electrical code/spec, identification, and document interpretation cases.

#### Text successes

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t4-e-103-ts-overcurrent-device-selection-coo`](../../../../tasks/t4-e-103-ts-overcurrent-device-selection-coo/task.toml) | 0.975 | TS | text | T4 | fail/high | E-103 Overcurrent device selection & coordination |
| [`v2-trap-f301-t3-screw-pops`](../../../../tasks/v2-trap-f301-t3-screw-pops/task.toml) | 0.950 | CC | text | T3 | pass/low | F-301 Drywall & finishing |
| [`v2-trap-c301-t2-efflorescence`](../../../../tasks/v2-trap-c301-t2-efflorescence/task.toml) | 0.950 | ID | text | T2 | pass/low | C-301 Block/brick laying |
| [`v2-trap-a102-t4-oil-seep`](../../../../tasks/v2-trap-a102-t4-oil-seep/task.toml) | 0.950 | FD | text | T4 | pass/low | A-102 Fluids & leaks |
| [`v2-nmi-s201-t2-bar-size-unconfirmed`](../../../../tasks/v2-nmi-s201-t2-bar-size-unconfirmed/task.toml) | 0.950 | ME | text | T2 | needs_more_info/medium | S-201 Rebar placement |
| [`v2-nmi-p201-t3-concealed-vent`](../../../../tasks/v2-nmi-p201-t3-concealed-vent/task.toml) | 0.950 | CC | text | T3 | needs_more_info/medium | P-201 Traps & venting |

#### Text failures

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t1-e-303-cc-terminations-splices`](../../../../tasks/t1-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T1 | fail/high | E-303 Terminations & splices |
| [`t2-e-303-cc-terminations-splices`](../../../../tasks/t2-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T2 | fail/high | E-303 Terminations & splices |
| [`t3-e-303-cc-terminations-splices`](../../../../tasks/t3-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T3 | fail/high | E-303 Terminations & splices |
| [`t5-e-303-cc-terminations-splices`](../../../../tasks/t5-e-303-cc-terminations-splices/task.toml) | 0.300 | CC | text | T5 | fail/high | E-303 Terminations & splices |
| [`t5-e-105-doc-motor-circuits-disconnects`](../../../../tasks/t5-e-105-doc-motor-circuits-disconnects/task.toml) | 0.312 | DOC | text | T5 | fail/medium | E-105 Motor circuits & disconnects |
| [`t2-e-602-id-equipment-bonding`](../../../../tasks/t2-e-602-id-equipment-bonding/task.toml) | 0.338 | ID | text | T2 | fail/high | E-602 Equipment bonding |
