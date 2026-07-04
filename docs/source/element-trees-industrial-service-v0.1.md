# Element Trees v0.1 — Industrial, Service & Manufacturing Disciplines
### 2.7 Equipment/Millwright · 2.8 Instrumentation · 2.9 Automotive · 2.10 Assembly/Fab · 2.12 Safety (cross-cutting)
Same schema: **Tiers · Task fit · Defect library · Ref**. Signature elements flagged ★.

---

# 2.7 Equipment & Machinery (Millwright)

## 2.7.1 Setting & Grouting

### M-101 Baseplates & anchor bolts
- Tiers: T1 · Task fit: CC, ME, SEQ
- Defects: insufficient anchor bolt projection; grout without vent holes (voids — sounding test); epoxy vs. cementitious grout misapplied; shim packs exceeding count/height limits; jack bolts left engaged after grout
- Ref: API RP 686

## 2.7.2 Alignment ★

### M-201 Shaft alignment
- Tiers: T1, T4, T5 · Task fit: ME, FD, SEQ, DOC
- Defects: soft foot uncorrected (dial reading in photo — ME); thermal growth offset ignored on hot service; coupling gap out of spec; alignment done before final pipe connection (pipe strain — SEQ/TRD)
- Ref: API 686, laser system manuals
- Note: reading a dial indicator or laser display from a photo is a dense, objective ME item; misalignment consequences (coupling/bearing wear patterns) make matching FD items.

## 2.7.3 Rotating Equipment

### M-301 Bearings & seals ★
- Tiers: T4, T5 · Task fit: FD, ID, SEQ, TS
- Defects: pressing force through rolling elements (wrong race); overheated during install (bluing — ID); over-greasing (purged seal); mechanical seal face contamination from bare-hand touch; wear pattern diagnosis (fluting = electrical, spalling = fatigue, false brinelling = vibration at standstill — premier FD set)
- Ref: SKF/Timken mounting guides
- Note: bearing failure-pattern photos are the automotive-adjacent FD goldmine of industrial maintenance.

### M-302 Belts, sheaves & couplings
- Tiers: T4, T5 · Task fit: ME, FD, TS
- Defects: sheave misalignment (straightedge in photo); mixed old/new belts on multi-groove; belt tension off (deflection measurement — ME); worn sheave grooves (belt riding low — ID)
- Ref: mfr guides

## 2.7.4 Conveyors

### M-401 Conveyor systems
- Tiers: T5, T1 · Task fit: FD, HAZ, CC
- Defects: belt mistracking causes (loading off-center vs. idler skew — FD); missing nip-point guards (HAZ); skirtboard gap wear; pull-cord e-stop slack/inoperable
- Ref: CEMA, OSHA 1910.212

**State hooks (millwright):** Staged = machine on blocks, alignment kit out · In-progress = rough-aligned, ungrouted · Tested = final alignment record (DOC), uncoupled run · In-service = coupled, guards on · Degraded/Failed = the T4 entry point — wear/failure photos.

---

# 2.8 Instrumentation & Controls

## 2.8.1 Field Instruments ★

### I-101 Transmitter installation
- Tiers: T1 · Task fit: CC, FD, ID
- Defects: DP impulse lines sloped wrong for service (gas taps below pipe / liquid taps on top — the classic); missing heat trace on freeze-prone impulse lines; transmitter above taps on liquid service; blocked-in with equalizer open
- Ref: API RP 551, mfr manuals

### I-102 Manifold operations
- Tiers: T1, T4 · Task fit: SEQ
- Defects: 3/5-valve manifold sequence wrong (equalize before opening HP side — pure SEQ item, one right order); venting trapped pressure to face level (HAZ)
- Ref: mfr procedures

## 2.8.2 Calibration & Loop Checks

### I-201 Calibration
- Tiers: T1, T5 · Task fit: DOC, ME, FD
- Defects: as-found/as-left not recorded; 5-point cal skipped (hysteresis missed); zero vs. span error diagnosis from cal sheet (FD+DOC); expired standard used
- Ref: ISA standards, site QC

### I-202 Loop checks & wiring
- Tiers: T1 · Task fit: DOC, ID, PA
- Defects: shield grounded both ends (ground loop); wire labels vs. loop drawing mismatch (DOC compare); landed on wrong terminal; missing surge protection on field side
- Ref: loop drawings, ISA 5.1
- Note: P&ID and loop-drawing interpretation is the deepest DOC well in the whole benchmark.

**State hooks (instrumentation):** Rough-complete = mounted & tubed, not terminated · Tested = cal stickers, loop check sheets · Accepted = commissioned, in DCS.

---

# 2.9 Automotive & Powertrain (T4-dominant)

## 2.9.1 Engine & Drivetrain ★

### A-101 Timing & mechanical
- Tiers: T4 · Task fit: ME, ID, FD, SEQ
- Defects: timing marks misaligned by a tooth (photo of marks — ME/ID); belt routing wrong vs. diagram (DOC); compression/leak-down interpretation (low two adjacent cylinders = head gasket — classic FD from gauge numbers); plastigauge reading (ME)
- Ref: OEM service info

### A-102 Fluids & leaks
- Tiers: T4 · Task fit: FD, ID
- Defects: leak source identification by color/location (trans red, coolant green/orange, oil...); milkshake oil cap (FD); overfilled crankcase; wrong spec fluid (TRD: "any ATF" vs. spec)
- Ref: OEM specs

## 2.9.2 Chassis ★

### A-201 Brakes
- Tiers: T4, T3(DIY) · Task fit: ME, SEQ, CC, FD
- Defects: rotor below minimum thickness (mic reading in photo — ME); pad wear indicator contact; caliper guide pins dry/seized; brake hose twisted; lug torque sequence & spec (star pattern — SEQ; impact-gun-only = TRD); pulsation diagnosis (DTV vs. deposits — FD)
- Ref: OEM specs, FMVSS-adjacent shop practice
- Note: the DIY-to-pro difficulty ramp is smoothest here — perfect for the skill-level tagging experiment.

### A-202 Suspension & steering
- Tiers: T4 · Task fit: FD, ID, ME
- Defects: ball joint play (video item — pry test); tire wear pattern diagnosis (inner edge = camber/toe, cupping = dampers — premier ID/FD); torquing rubber bushings at full droop (TRD — preload error); cotter pin omitted on castle nut
- Ref: OEM, alignment specs

## 2.9.3 Electrical & Electronics

### A-301 Diagnostics ★
- Tiers: T4 · Task fit: DOC, FD, SEQ
- Defects: freeze-frame interpretation (DOC: read the scan tool screenshot); parasitic draw procedure order (SEQ); replacing parts on codes without testing (P0420 → cat vs. O2 sensor — the canonical TRD/FD item); voltage-drop testing vs. resistance testing grounds
- Ref: OEM service info, OBD-II standards

### A-302 ADAS & post-repair calibration
- Tiers: T4 · Task fit: CC, TRD
- Defects: windshield replaced without camera calibration; alignment done without ADAS recal; missing target-based static cal (often skipped — TRD with safety stakes)
- Ref: OEM position statements

## 2.9.4 EV & A/C Systems

### A-401 High-voltage safety ★
- Tiers: T4 · Task fit: SEQ, HAZ, CC, ID
- Defects: service disconnect pulled but no wait time/verification (SEQ); glove class wrong or test date expired (ID from stamp); orange cable handling violations; insulation resistance test skipped after repair
- Ref: OEM HV procedures, NFPA 70E-adjacent
- Note: transfers directly from electrical LOTO — good cross-discipline consistency check for models.

### A-402 A/C service
- Tiers: T4 · Task fit: FD, ME, CC
- Defects: pressure readings interpretation (both low vs. high-high — FD); sealed with stop-leak before service (TRD); venting refrigerant (EPA 609 violation); wrong oil for compressor type
- Ref: EPA 609, OEM specs

**State hooks (automotive):** Planned = work order/estimate · In-progress = on lift, disassembled · Tested = road test, post-scan printout (DOC) · Rework = comeback · S2 states dominate: most items are Worn/Degraded/Failed diagnosis rather than install.

---

# 2.10 Assembly & Fabrication (T5-dominant)

## 2.10.1 Fastening & Joining ★

### B-101 Torque & threaded fastening
- Tiers: T5, T4 · Task fit: SEQ, ID, CC, TRD
- Defects: torque sequence pattern violated (spiral/star from center — SEQ); torque-to-yield bolts reused (TRD/CC — one-time use); thread locker color misapplied (blue vs. red — ID); click wrench used upside down/uncalibrated; missing torque stripe (witness mark — ID)
- Ref: OEM/engineering specs

### B-102 Production welding
- Tiers: T5 · Task fit: DOC, ME, ID, CC
- Defects: parameters outside WPS window (DOC: compare machine settings photo to WPS); fillet gauge fail (ME); spatter/cleanliness reject; missed weld per drawing (DOC)
- Ref: AWS D1.1/D1.3, shop WPS

## 2.10.2 Fitment & Tolerance

### B-201 Gauging & GD&T basics
- Tiers: T5 · Task fit: ME, DOC, ID
- Defects: go/no-go misread (go doesn't go = undersize... reasoning item); caliper/mic misread (photo of scale — pure ME); datum scheme misunderstood (part checked off wrong surface — DOC)
- Ref: ASME Y14.5 (basic), gauge instructions

## 2.10.3 Line Operations ★

### B-301 Standard work execution
- Tiers: T5 · Task fit: SEQ, PA, TRD
- Defects: step order deviation vs. standard work sheet (video + document = premier multimodal SEQ); skipped verification step under takt pressure (TRD); wrong-part-similar-part (ID from bin photo)
- Ref: site standard work, TWI

### B-302 Andon & quality response
- Tiers: T5 · Task fit: SEQ, TRD
- Defects: defect passed downstream instead of pulled; rework without disposition; andon triggered late
- Ref: site quality procedures

## 2.10.4 Quality Inspection

### B-401 Visual acceptance
- Tiers: T5 · Task fit: ID, ME, DOC
- Defects: scratch/dent classification vs. boundary samples (ID against acceptance standard photos); first-article dims vs. drawing (DOC+ME); missed flash/burr on molded parts
- Ref: site visual standards, AIAG PPAP

**State hooks (assembly):** Staged = kitted parts vs. BOM (ID item: what's missing from the kit?) · In-progress = station N of M (PA from photo of partially built unit — the purest progress items in the benchmark) · Tested = EOL test printout (DOC) · Rework = red-tagged, quarantine area.

---

# 2.12 Safety & Rigging (Cross-cutting overlay)

Applies to every discipline; items here get double-coded (Safety + host discipline).

### X-101 Lockout/Tagout ★
- Tiers: all · Task fit: SEQ, CC, HAZ, ID
- Defects: lock without tag / tag without lock; energy source missed (stored hydraulic/gravity/capacitor); no try-step verification (SEQ); group lockbox misused; breaker taped instead of locked (ID)
- Ref: OSHA 1910.147

### X-102 Fall protection ★
- Tiers: T1, T2, T3 · Task fit: ID, CC, HAZ, ME
- Defects: harness impact indicator deployed (ID from photo — webbing tag); frayed/burned webbing; anchor point inadequate (guessing at 5,000-lb rating — TRD); 6-ft trigger ignored; ladder angle wrong (4:1 — ME from photo); top two rungs occupied
- Ref: OSHA 1926 Subpart M, 1910.140

### X-103 Confined space
- Tiers: T1, T4 · Task fit: DOC, FD, SEQ
- Defects: gas meter readout interpretation (O₂ 19.0% — enter or not? FD/DOC); no attendant posted; permit expired mid-shift; ventilation intake near exhaust source
- Ref: OSHA 1910.146

### X-104 Hot work
- Tiers: T1, T2, T5 · Task fit: CC, HAZ, SEQ
- Defects: no fire watch during + post-work period; combustibles within radius uncovered; hot work over sewer/drain; permit scope exceeded
- Ref: NFPA 51B, OSHA 1926 Subpart J

### X-105 PPE selection
- Tiers: all · Task fit: TS, ID, CC
- Defects: arc-flash rating below task category (label vs. clothing — DOC+ID); voltage glove class wrong or overdue; respirator wrong cartridge color (ID); safety glasses vs. goggles vs. face shield mismatch to task
- Ref: NFPA 70E, OSHA 1910 Subpart I

### X-106 Housekeeping & general hazard recognition ★
- Tiers: all · Task fit: HAZ
- Defects: the open-ended "find all hazards in this jobsite photo" item — cords across walkways, missing guardrails, blocked egress/extinguishers, improvised scaffolds, unattended open holes
- Ref: OSHA general duty, 1926 Subpart L (scaffolds)
- Note: best free-response HAZ format; grade with a keyed hazard list + severity weighting, penalize confident false positives.

---

## Rollup — v0.1 element inventory

| Discipline | Elements | Signature ★ |
|---|---|---|
| 2.1 Electrical | 30 | Panel makeup, hazardous-location seals |
| 2.2 Piping/Plumbing | 11 | Spool fit-up, traps/venting, water heaters |
| 2.3 HVAC-R | 7 | Furnace venting, refrigeration circuit |
| 2.4 Structural/Iron | 7 | Bolting, rebar, rigging |
| 2.5 Concrete/Masonry | 5 | Placement, flashing/weeps |
| 2.6 Carpentry/Finishes | 7 | Framing, envelope flashing |
| 2.7 Millwright | 5 | Alignment, bearings |
| 2.8 Instrumentation | 4 | Transmitter install |
| 2.9 Automotive | 8 | Engine, brakes, diagnostics, EV HV |
| 2.10 Assembly/Fab | 6 | Torque, line ops |
| 2.11 Sitework | 4 | Trench protection, locates |
| 2.12 Safety | 6 | LOTO, fall protection, housekeeping |
| **Total** | **~100** | **~20 signature** |

Every element carries ≥3 seed defects → **~350 installed-defective/non-compliant conditions** as the starting corpus for vision items, before SME expansion.
