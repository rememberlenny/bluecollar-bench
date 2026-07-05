# Modality-Native Task Categories v0.1 - Audio-Only & Video-Only

Bluecollar-bench expansion: tasks where the modality is the signal.

Design rule: an item belongs in these categories only if removing the modality destroys it. If a transcript or a single frame preserves the answer, it is a text or photo item wearing a costume. Every item below fails that reduction test on purpose.

Item coding gains a modality suffix: `T4 x A-101 x FD-A` for audio, `T5 x B-301 x SEQ-V` for video.

## Part 1 - Audio-Native Categories

The trades run on ears more than any office job: mechanics diagnose by sound before they touch a wrench, millwrights hear bearings dying weeks before failure, welders judge a MIG arc by its sizzle. These are real journeyman skills with no text equivalent.

### A1. Mechanical fault signatures (FD-A)

The flagship. Sound -> component -> failure mode -> urgency.

- Automotive (A-101/A-201): rod knock vs. lifter tick vs. exhaust leak tick; belt squeal vs. bearing chirp; brake squeal vs. grind; single-cylinder misfire rhythm; CV click on turns; wheel-bearing drone that changes with steering load.
- Millwright/industrial (M-301): bearing stages from smooth to whine to growl to knock; pump cavitation; compressor valve slap; gearbox tooth-mesh anomalies; steam trap live-blow vs. proper cycling.
- Building systems (H-101/P-401): water hammer signature; furnace ignition roll-out whoomph vs. normal light-off; refrigerant flood-back slugging; ductwork oil-canning; short-cycling cadence.
- Electrical (E-102/E-303): 60/120 Hz transformer hum vs. irregular crackle-buzz of arcing; loose-connection sizzle in a panel.

### A2. Process-quality-by-ear (CC-A / ME-A)

- MIG weld: steady bacon-sizzle vs. popping from wrong voltage or stickout.
- Fastening: impact gun hammering to stall vs. torque-wrench click; drill vs. hammer-drill engagement in concrete.
- Engine tune: even idle cadence vs. lope; two-stroke rich four-stroking.

### A3. Radio communications (DOC-A / SEQ-A / HAZ-A)

Intent under degradation, readback protocol, and ALL-STOP priority. Audio-native because the degradation itself carries the task, especially which slot got garbled.

### A4. Environmental hazard sounds (HAZ-A)

Gas hiss near a meter, compressed-air leak vs. steam leak, backup alarms and horn signal patterns, abnormal silence such as a conveyor that should be running and is not.

### Audio Ground Truth

1. Synthesized signatures: many faults are parametrically constructible. Misfire is a periodic gap in an even firing pattern at known rpm; bearing fault is an impulse train at defect frequency over shaft hum; water hammer is a decaying thump transient; arcing is broadband irregular crackle vs. clean 120 Hz hum. Label by construction and expose difficulty as an SNR dial.
2. Licensed/public recordings: mechanic-education channels and maintenance-training libraries have labeled fault audio; labels need SME re-verification, not creation.
3. Field capture: contributor kit addition - 15-second phone clips with a three-tap label, parallel to the photo pipeline.

Audio grading should score component, failure mode, and urgency slots. Confusion matrices on deliberately confusable pairs are the headline result: squeal/grind, hum/arcing, knock/tick, and other pairs where getting it wrong reverses the safety call. Answer schema gains `sound_source` and `confidence`; escalation gates still apply, for example arcing requires do-not-energize action.

## Part 2 - Video-Native Categories

Video earns its cost only when the answer lives in motion, timing, sequence, or cause-and-effect.

### V1. Play, wobble & runout tests (FD-V / ME-V)

Ball-joint play under pry, wheel-bearing rock at 12-and-6, pulley wobble at speed, shaft runout, tire cupping vibration. The answer is the delta between frames.

### V2. Process technique & procedure execution (SEQ-V / CC-V)

- Torque sequence: did the bolts get hit in the star pattern or around the clock?
- Weld technique: travel speed steadiness, puddle control, rod angle drift over a pass.
- Standard work (B-301): operator step order vs. the standard work instruction.
- Safe practice: three points of contact on a ladder, LOTO try-step actually performed, harness donned and buckled in order.

### V3. Dynamic system behavior (FD-V)

- Flame character: lazy yellow vs. crisp blue, rollout at ignition, flame lift-off.
- Fluid dynamics: drip rate, drain swirl vs. glug, burner short-cycling period.
- Belt/conveyor tracking drift (M-401): direction and rate of wander to choose the idler adjustment.
- Electrical cause-effect: breaker flipped, then which lights respond.

### V4. Progress & rework over time (PA-V)

Frame sequences first. True-video additions include crew-count and activity-classification over timelapse for earned-hours estimation, plus detecting undo/rework signatures when material flow reverses.

### V5. Rigging & lift dynamics (HAZ-V)

Load swing amplitude growing vs. damping, tagline control, snap-loading, and personnel drifting into the fall zone during the lift. Single frames show geometry; video shows judgment moments.

### Video Ground Truth

1. Synthetic animation: extend the matplotlib pipeline to GIF/MP4 for animated drip counters, oscillating pulleys, torque-sequence dot animations, and belt-drift simulations. Ground truth by construction.
2. Scripted capture: technique items need a correct execution plus scripted violations per element.
3. Fixed-station footage (T5): a single assembly-station camera plus SWI document yields many SEQ-V items.

Video grading should support temporal fields:

- `event_time`: when a violation occurred, scored with tolerance.
- `rate`: drips/min or equivalent dynamic rate via expected numeric value.
- `order`: sequence edit distance against expected order.

Frame-count budgets become a difficulty axis: the same item at 4 fps vs. 1 fps vs. three keyframes measures how much temporal resolution the model needs.

## Taxonomy Integration

| Addition | Change |
|---|---|
| Modality suffix on task types (`FD-A`, `SEQ-V`, etc.) | Item coding and coverage matrix gain a modality dimension. |
| `media` supports `.wav`, `.mp3`, `.mp4`, `.gif` | `generate_tasks_v2` media copying is file-agnostic; instruction template notes media type. |
| New answer fields: `sound_source`, `event_time`, `rate`, `order` | `grade_v2` extensions follow the `expected_value` / expected-set pattern. |
| Confusable-pair tagging: `confusable_with: item_id` | Enables confusion-matrix headline analysis. |
| Reduction test as review gate | Every audio/video item must state why a transcript/frame cannot answer it. |

## Build Order

1. Synthetic audio signatures: misfire rhythm, bearing stages, hum-vs-arc, water hammer. DSP can be kept small with NumPy/SciPy and gives the same day-one payoff as synthetic gauges.
2. Animated video primitives: drip rate, torque-sequence order, belt drift through matplotlib animation with ground truth by construction.
3. Radio audio layer on the Track 1 transcripts: TTS plus degradation chain.
4. Scripted capture kit: shot/sound list for the first tradesperson session so real media lands pre-labeled.
