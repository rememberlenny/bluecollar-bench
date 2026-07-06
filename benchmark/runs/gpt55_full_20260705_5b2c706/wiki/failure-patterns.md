# Failure Patterns And Safety Gates

[Back to wiki index](README.md)

The main failure modes are clustered and therefore actionable.

## Failure pattern summary

| pattern | evidence | conclusion |
|---|---|---|
| Exact identification/diagnosis | FD contributed 20 low-score tasks and ID contributed 12. | Add or emphasize exact component, defect, and source-name checks. |
| Audio brittleness | Audio had 10 low-score tasks out of 44. | Treat audio FD as a separate benchmark capability, not just another FD variant. |
| Electrical code/detail traps | Discipline 2.1 had 24 low-score tasks. | Electrical detail cases should be kept as regression anchors. |
| Critical visual false passes | 8 dangerous false pass gate hits. | Image strength does not eliminate safety-critical visual misses. |
| Over-failing safe audio cases | 4 alarmist false fail gate hits. | Some low-risk/pass sound cases are incorrectly treated as unsafe. |

## Dangerous false pass examples

These are the highest-priority review items because the expected answer is unsafe/fail but the model missed the final safety call.

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t1-e-303-cc-terminations-splices`](../../../../tasks/t1-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T1 | fail/high | E-303 Terminations & splices |
| [`t2-e-303-cc-terminations-splices`](../../../../tasks/t2-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T2 | fail/high | E-303 Terminations & splices |
| [`t3-e-303-cc-terminations-splices`](../../../../tasks/t3-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T3 | fail/high | E-303 Terminations & splices |
| [`v2-cpm-delay-001`](../../../../tasks/v2-cpm-delay-001/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-cpm-delay-009`](../../../../tasks/v2-cpm-delay-009/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-media-sling-004`](../../../../tasks/v2-media-sling-004/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-009`](../../../../tasks/v2-media-sling-009/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-011`](../../../../tasks/v2-media-sling-011/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |

## Alarmist false fail examples

These are safe/pass items that the model treated too harshly, all from audio in this run.

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`v2-audio-hammer-000`](../../../../tasks/v2-audio-hammer-000/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-008`](../../../../tasks/v2-audio-hammer-008/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hum-002`](../../../../tasks/v2-audio-hum-002/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-audio-hum-004`](../../../../tasks/v2-audio-hum-004/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |

## Lowest-score cluster examples

| task | reward | type | modality | tier | expected | why it matters |
|---|---:|---|---|---|---|---|
| [`t1-e-303-cc-terminations-splices`](../../../../tasks/t1-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T1 | fail/high | E-303 Terminations & splices |
| [`t2-e-303-cc-terminations-splices`](../../../../tasks/t2-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T2 | fail/high | E-303 Terminations & splices |
| [`t3-e-303-cc-terminations-splices`](../../../../tasks/t3-e-303-cc-terminations-splices/task.toml) | 0.000 | CC | text | T3 | fail/high | E-303 Terminations & splices |
| [`v2-audio-hammer-000`](../../../../tasks/v2-audio-hammer-000/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hammer-008`](../../../../tasks/v2-audio-hammer-008/task.toml) | 0.000 | FD | audio | T3 | pass/low | P-301 PEX & copper installation |
| [`v2-audio-hum-002`](../../../../tasks/v2-audio-hum-002/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-audio-hum-004`](../../../../tasks/v2-audio-hum-004/task.toml) | 0.000 | FD | audio | T2 | pass/low | E-303 Terminations & splices |
| [`v2-cpm-delay-001`](../../../../tasks/v2-cpm-delay-001/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-cpm-delay-009`](../../../../tasks/v2-cpm-delay-009/task.toml) | 0.000 | RES | image | T2 | fail/medium | RES Schedule & constraint reasoning |
| [`v2-media-sling-004`](../../../../tasks/v2-media-sling-004/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-009`](../../../../tasks/v2-media-sling-009/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`v2-media-sling-011`](../../../../tasks/v2-media-sling-011/task.toml) | 0.000 | ME | image | T1 | fail/critical | S-301 Rigging configuration |
| [`t5-e-303-cc-terminations-splices`](../../../../tasks/t5-e-303-cc-terminations-splices/task.toml) | 0.300 | CC | text | T5 | fail/high | E-303 Terminations & splices |
| [`t5-e-105-doc-motor-circuits-disconnects`](../../../../tasks/t5-e-105-doc-motor-circuits-disconnects/task.toml) | 0.312 | DOC | text | T5 | fail/medium | E-105 Motor circuits & disconnects |
| [`t2-e-602-id-equipment-bonding`](../../../../tasks/t2-e-602-id-equipment-bonding/task.toml) | 0.338 | ID | text | T2 | fail/high | E-602 Equipment bonding |
| [`t3-e-204-id-boxes-fittings-fill`](../../../../tasks/t3-e-204-id-boxes-fittings-fill/task.toml) | 0.338 | ID | text | T3 | fail/medium | E-204 Boxes, fittings & fill |
| [`t4-p-401-fd-boiler-pump-piping`](../../../../tasks/t4-p-401-fd-boiler-pump-piping/task.toml) | 0.350 | FD | text | T4 | fail/high | P-401 Boiler & pump piping |
| [`v2-audio-hum-001`](../../../../tasks/v2-audio-hum-001/task.toml) | 0.350 | FD | audio | T2 | fail/critical | E-303 Terminations & splices |
| [`v2-trd-s302-t1-wind-pick`](../../../../tasks/v2-trd-s302-t1-wind-pick/task.toml) | 0.350 | TRD | text | T1 | fail/critical | S-302 Crane operations |
| [`t1-e-403-id-vfds-motor-controls`](../../../../tasks/t1-e-403-id-vfds-motor-controls/task.toml) | 0.362 | ID | text | T1 | fail/medium | E-403 VFDs & motor controls |
