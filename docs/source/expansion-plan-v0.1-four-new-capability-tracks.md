# Expansion Plan v0.1 — Four New Capability Tracks

bluecollar-bench: audio comms · video progress · field-constraint reasoning · DIY & building science

The unifying strategy across all four tracks is the one that already worked for the instrument images: **synthetic-parametric generation first** — build items where ground truth is computed from the same parameters that generate the stimulus, then graduate to real-world media once the harness and graders are proven. Every track below has a computable core.

---

## Track 1 — Radio Communications (walkie-talkie instructions & intent)

**What it tests.** Trades run on half-duplex radio: compressed, jargon-dense, deictic ("send it," "hold what you got," "come up easy," "all stop"). Two distinct capabilities: (a) *decoding* degraded audio, and (b) *interpreting intent* — including knowing when the correct response is not to act but to request readback.

**Item archetypes**
1. **Intent extraction (DOC/ID):** transcript or audio of an instruction → structured intent: `{action, object, quantity, location, direction, urgency}`. "Boom up and swing left, load's coming to the third floor east bay" → slots. Gradable deterministically.
2. **Safety-priority handling (HAZ):** exchanges where a priority call ("ALL STOP") arrives mid-instruction. Correct answer must recognize that stop commands override everything and can be given by anyone on site.
3. **Ambiguity → readback (needs_more_info analog):** instructions with a missing or garbled critical slot ("give me [static] more inches of cable"). Correct behavior is "say again / confirm quantity," not a guess. This is the radio-domain twin of the dead-sensor gas meter item.
4. **Protocol knowledge (SEQ/CC):** number readback conventions, phonetic alphabet, who acknowledges, crane signalperson-of-record rules (only one designated signaler, but anyone can call stop).
5. **Multi-turn exchanges (TRD):** dispatcher-to-tech or operator-to-rigger dialogues where the model plays one side and must track state across turns.

**Ground-truth strategy.** Scripts are authored or generated from templates with intent labels attached at write time. Audio is synthesized: TTS → radio-effect DSP chain (band-pass ~300–3,000 Hz, hard compression, PTT click and squelch tail, additive jobsite noise at controlled SNR, occasional syllable dropouts at labeled positions). Every degradation is parameterized, so difficulty is a dial and the "garbled slot" is known exactly. Ship each item in **paired modalities**: `modality: text-transcript` and `modality: audio` versions of the same script, which measures how much the audio channel itself costs a model.

**Schema/grader.** Add `intent` object to item ground truth; grader scores slot F1 plus the existing decision/safety gates. New forbidden class: acting on an unconfirmed safety-critical slot. Answer schema gains an `intent` field and a `readback` field (what the model would say back on the radio).

**Phasing.** P1: 40 transcript-only items (pure authoring, no new tooling). P2: DSP pipeline + audio versions (ffmpeg/sox in the gen script; runs in the same container pattern as `gen_media_items`). P3: real recorded radio traffic with SME-labeled intent (highest cost, do last).

---

## Track 2 — Progress Estimation from Video

**What it tests.** The S3 state machine applied over time: % complete, what changed between observations, what comes next, and whether progress ever went *backwards* (rework detection — the interesting failure).

**Item archetypes**
1. **Frame-pair delta (PA):** two photos of the same work area, T and T+Δ → what changed, updated % complete, earned quantity (for example, "three more tray sections hung").
2. **Frame-sequence trajectory (PA/SEQ):** 4–8 ordered frames → per-frame S1 state labels + monotonic progress curve. Insert one out-of-order or rework frame as a trap.
3. **Rules-of-credit application (PA/DOC):** frames plus the project's rules-of-credit table → computed earned %. Grading is arithmetic once milestone recognition is right, so partial credit separates "saw the milestones" from "did the math."
4. **Next-step prediction (SEQ):** given the latest frame, what must happen before the next milestone (drywall can't start → insulation inspection not yet passed — visible from the frame).

**Ground-truth strategy.** Synthetic first: render progressive build states programmatically — a parametric wall-frame/conduit-run/assembly-station drawing at N stages, where % complete is by construction. The T5 assembly cell is the cleanest: unit at station 4 of 9 is 44% by definition, matching the taxonomy note. Then semi-real: public timelapse videos sliced into frames, annotated once per video against rules of credit — one annotation yields many frame-pair and sequence items. Video proper (motion, temporal reasoning) is P3; almost all the signal is available from frame sequences at a fraction of the harness complexity, since the media field already accepts lists.

**Schema/grader.** `media` = ordered frame list with `t` timestamps; `expected_value` = percent (already supported, tolerance band per item); add `expected_sequence` for per-frame state labels and `rework_present: bool`. Headline metrics: percent MAE, state-sequence accuracy, rework detection rate.

---

## Track 3 — Field Constraint Diagnosis (labor, supply, sequencing)

**What it tests.** The foreman/superintendent layer: given a disrupted plan, reason about critical path, trade precedence, and valid recovery options. This is the most *underrated* computable track — scheduling is math.

**Item archetypes**
1. **Disruption triage (new task type RES):** a two-week lookahead schedule (activities, durations, crew assignments, precedence links, inspection holds) plus a disruption (2 of 6 crew no-show; drywall delivery slips 4 days; inspector unavailable). Questions: what's the critical-path impact in days, which activities can still proceed (workable backlog), which resequencings are valid?
2. **Hard-constraint traps:** proposed recovery plans that violate physics or code sequencing — tile before waterproofing cure, cover before rough inspection, energize before AHJ release, concrete pour with insufficient cure before stressing (ties to S-202). Model must reject the fast-but-invalid option. This is the scheduling twin of `dangerous_false_pass`.
3. **Substitution judgment (TRD/CC):** specified material unavailable; candidate substitute on the shelf. When is it a like-for-like swap, when does it need a submittal/RFI, when is it a code problem (for example, substituting non-rated assembly components)?
4. **Trade-stacking & sequencing (SEQ):** order a set of trades through a room/zone respecting wet-before-dry, overhead-before-below, cure and inspection holds.

**Ground-truth strategy.** Generate synthetic project graphs: activities with durations, finish-to-start (+lag) precedence, resource pools, and hold points. Critical path, float, and feasible-set answers are **computed by CPM** — exact ground truth, infinite variants, difficulty controlled by graph size and disruption type. Hard constraints (cure times, inspection precedence) come from a curated rules table drawn from the element trees, which doubles as the trap library.

**Schema/grader.** Item carries the schedule as structured JSON *and* rendered as a Gantt image (reuse the matplotlib pipeline → this track is multimodal for free: read the schedule off the chart). Grader checks numeric answers (delay days, float) with tolerance, set answers (workable activities) with F1, and hard-constraint traps as forbidden conclusions.

---

## Track 4 — DIY Problem Solving & Building Science (T3 deep expansion)

**What it tests.** Homeowner-facing reasoning across plumbing, heating, envelope/building science, and indoor environment (air quality, lighting, EMF) — plus the meta-skill that defines responsible DIY guidance: **knowing where DIY ends** (gas, structural, service equipment, permits).

### New taxonomy branch: 2.13 Building Science & Indoor Environment

- **Moisture & condensation** — dew point and surface-condensation prediction, vapor-drive direction by climate, crawlspace/attic moisture, mold-conducive conditions. *Psychrometrics is computable:* given indoor T/RH and surface temperature, condensation risk is arithmetic → same synthetic-parametric pattern, rendered as hygrometer/IR-thermometer screens.
- **Air sealing & insulation** — stack effect reasoning, where the air barrier is, thermal bridging identification (IR-image items later), R-value/assembly questions.
- **Ventilation & combustion safety** — ASHRAE 62.2-style CFM requirements (computable from house size/bedrooms), bath/kitchen exhaust sizing, backdrafting risk when adding exhaust to homes with natural-draft appliances (a genuinely dangerous DIY interaction — prime HAZ item), CO alarm placement.
- **Indoor air quality** — CO2/PM2.5/VOC/radon meter-screen items (direct reuse of the 4-gas render pattern with residential thresholds); humidity targets; filter MERV tradeoffs vs. system static pressure.
- **Lighting** — lumen/level calcs for a room (computable), color temperature and CRI selection, flicker complaints diagnosis.
- **EMF** — measurement-literacy items: reading a milligauss meter, what typical household levels are, and *evidence-calibration judgment*: distinguishing well-established residential hazards (CO, radon, PM2.5) from concerns where major health bodies find no established risk at household levels. Grading rewards accurate representation of the evidence, not validation or dismissal of the worry — this is an epistemics eval wearing a home-inspection costume.

**DIY-specific eval axes**
1. **Diagnose-from-symptoms (FD):** "banging pipes when the washer stops" (water hammer), "one room always cold," "musty smell in closet on exterior wall," "tripping breaker when microwave + toaster run." Ground truth = defect libraries already in the element trees, rewritten as homeowner symptom language.
2. **Escalation boundary (new decision dimension):** every DIY item carries `escalation: none | diy-with-permit | licensed-pro | emergency`. The dangerous errors are asymmetric: telling someone to DIY a gas leak is catastrophic; telling them to call a pro for a running toilet is merely unhelpful. Grader gets a `dangerous_diy_encouragement` gate parallel to `dangerous_false_pass`.
3. **Sequencing home projects (SEQ):** renovation order respecting building science (air-seal before insulating, fix bulk water before finishes, envelope before HVAC sizing since load changes).
4. **Tool/material selection at DIY skill level (TS):** the wire-nut and PEX-fitting questions from the taxonomy's skill-level discussion — tagged `skill: diy` to finally implement that open question.

**Ground-truth strategy.** Three sources: (a) computable physics (psychrometrics, ventilation CFM, lumen math, voltage drop) via the synthetic pipeline; (b) defect libraries inverted into symptom narratives; (c) escalation labels from a curated jurisdiction-neutral rules table (gas/structural/service-panel/roof-height = pro, with a `jurisdiction_sensitive` flag where permits vary).

---

## Cross-track infrastructure (build once)

| Need | Serves | Approach |
|---|---|---|
| `modality` expansion: audio, frame-sequence, chart | 1, 2, 3 | extend item schema + `generate_tasks_v2` media handling (already accepts lists) |
| DSP audio pipeline | 1 | TTS + sox/ffmpeg effect chain in a gen script, parameterized degradation |
| Parametric renderers v2 | 2, 3, 4 | progressive-state drawings, Gantt charts, meter screens (pattern exists) |
| CPM engine | 3 | ~150 lines: forward/backward pass, float, feasibility checker |
| Psychrometric calc lib | 4 | dew point / RH / condensation-risk functions, ~80 lines |
| New gates: `unconfirmed_safety_action`, `hard_constraint_violation`, `dangerous_diy_encouragement` | 1, 3, 4 | `grade_v2` pattern: directional multiplicative gates |
| `skill` and `escalation` tags | 4 | resolves taxonomy v0.1 open question #1 |

## Suggested build order

1. **Track 3 CPM core** — highest novelty-per-effort; fully computable; multimodal via Gantt renders on day one.
2. **Track 4 physics items + escalation gate** — reuses the meter-screen renderer; the escalation gate is the benchmark's most societally relevant metric.
3. **Track 1 transcripts** (authoring only) → then the DSP audio layer.
4. **Track 2 synthetic frame sequences** → then annotated real timelapse.

Each track lands ~50 items in its P1 synthetic form before any real-world media or SME time is spent — proving graders on computable ground truth first, exactly as the instrument images did.
