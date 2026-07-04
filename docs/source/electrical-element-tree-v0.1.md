# Electrical Discipline — Element-Level Tree v0.1
### Template for all disciplines · Blue-Collar AI Benchmark

**Design rule for an "element":** the smallest unit of work that is (a) photographable/recordable as a discrete thing, (b) has an objectively gradable right/wrong, and (c) maps to at least one lifecycle state. If tradespeople would argue about what "done" means for it, it's still a sub-category — split it further.

**Per-element fields:**
- **Tiers** — which settings it appears in (T1 Heavy / T2 Commercial / T3 Residential / T4 Service / T5 Shop)
- **Task fit** — which task types generate strong items (ID, FD, CC, SEQ, TS, HAZ, ME, PA, DOC, TRD)
- **Defect library** — seed list of *installed-defective* / *non-compliant* conditions for vision items
- **Ref** — primary code/standard anchor (US model codes; NEC 2023 numbering)

---

## 2.1.1 Power Distribution

### E-101 Service entrance & metering
- Tiers: T2, T3 · Task fit: CC, ID, HAZ, DOC
- Defects: undersized service conductors; missing drip loop; unsealed weatherhead penetration; meter jaws burned/corroded; improper mast support
- Ref: NEC Art. 230

### E-102 Panelboard installation & makeup
- Tiers: T1, T2, T3 · Task fit: CC, HAZ, ID, PA, TRD
- Defects: double-tapped breakers (non-listed); neutrals & grounds mixed in subpanel; missing knockout filler; no panel schedule; conductors crossing bus gutter space; multi-wire branch circuit without handle tie
- Ref: NEC Art. 408, 110.26 (working clearance), 200.4
- Note: single best photo-eval element in residential — every defect is visible with the deadfront off.

### E-103 Overcurrent device selection & coordination
- Tiers: T1, T2, T3, T4 · Task fit: TS, CC, ME, DOC
- Defects: breaker/conductor ampacity mismatch; wrong breaker type for panel (listing); missing AFCI/GFCI where required
- Ref: NEC 240, 210.8, 210.12, 110.14(C) termination temp ratings

### E-104 Transformers (dry-type & pad-mount)
- Tiers: T1, T2 · Task fit: CC, ID, SEQ, ME
- Defects: primary/secondary landed reversed; missing secondary bonding jumper (SDS); inadequate ventilation clearance
- Ref: NEC Art. 450, 250.30

### E-105 Motor circuits & disconnects
- Tiers: T1, T2, T5 · Task fit: CC, TS, FD, DOC
- Defects: disconnect not within sight; undersized motor overloads; missing lockable disconnect for maintenance
- Ref: NEC Art. 430

## 2.1.2 Raceway

### E-201 EMT bending & installation
- Tiers: T1, T2 · Task fit: ME, CC, SEQ, ID, PA
- Defects: kinked/flattened bend; >360° of bends between pull points; missing support within 3 ft of box; unreamed cut ends; improper coupling engagement
- Ref: NEC Art. 358, Ch. 9 (fill)
- Note: bend geometry from a photo (estimate angle, spot the dog-leg) is a great ME item; offset/saddle math is a classic apprentice test.

### E-202 Rigid & PVC conduit
- Tiers: T1, T2 · Task fit: CC, TS, SEQ
- Defects: PVC expansion fitting omitted on long exterior run; no bushing on RMC where required; wrong glue/no primer on PVC joints
- Ref: NEC Art. 344, 352

### E-203 Cable tray
- Tiers: T1 · Task fit: CC, ME, PA, HAZ
- Defects: fill ratio exceeded; missing bonding across expansion joints; cable not secured on vertical runs; tray used as walkway (HAZ)
- Ref: NEC Art. 392
- Note: strong PA element — tray runs read progress cleanly in photos.

### E-204 Boxes, fittings & fill
- Tiers: T1, T2, T3 · Task fit: CC, ME, ID
- Defects: box fill exceeded (calculable from photo!); missing box extension on deep finish; <6 in. free conductor; NM cable without connector/clamp; open knockouts
- Ref: NEC 314.16, 300.14, 314.28 (pull box sizing)

## 2.1.3 Wire & Cable

### E-301 Conductor selection & sizing
- Tiers: all · Task fit: TS, ME, CC, TRD
- Defects: undersized for load + length (voltage drop); aluminum on device not rated CO/ALR; wrong insulation type for wet location
- Ref: NEC 310, Table 310.16

### E-302 NM/MC cable routing & protection
- Tiers: T2, T3 · Task fit: CC, HAZ
- Defects: NM within 1¼ in. of stud face without nail plate; unsupported runs; NM exposed where subject to damage; MC without anti-short bushing (mfr-dependent — good TRD item)
- Ref: NEC 300.4, 334, 330

### E-303 Terminations & splices
- Tiers: all · Task fit: CC, ID, FD, TS
- Defects: backstabbed device on 20A circuit (TRD: legal but journeymen won't); insufficient torque (thermal signature — IR modality); splice outside box; wrong wirenut size; nicked conductors
- Ref: NEC 110.14

### E-304 Wire pulling (feeders & branch)
- Tiers: T1, T2 · Task fit: SEQ, TS, ME, PA
- Defects: exceeded sidewall pressure/jamming (planning item); no lubricant on long pull; phase tape colors wrong
- Ref: NEC 200.6, 210.5 (identification)

## 2.1.4 Devices & Equipment

### E-401 Receptacles & switches
- Tiers: T2, T3, T4 · Task fit: CC, ID, FD
- Defects: reversed polarity; open ground; GFCI missing in wet/kitchen/garage locations; non-WR receptacle outdoors; ungrounded 3-prong replacement
- Ref: NEC 210.8, 406.4, 406.9
- Note: pairs perfectly with tester-readout photos (multimodal: photo + plug-in tester lights).

### E-402 GFCI/AFCI function & troubleshooting
- Tiers: T3, T4 · Task fit: FD, SEQ, TRD
- Defects: line/load reversed on GFCI; AFCI nuisance-trip diagnosis (shared neutral); protecting downstream vs. single-location wiring
- Ref: NEC 210.8, 210.12

### E-403 VFDs & motor controls
- Tiers: T1, T5, T4 · Task fit: FD, DOC, SEQ, ID
- Defects: missing load reactor on long motor leads; control wiring in same raceway as power; wrong overload class setting
- Ref: NEC 430, mfr manuals

## 2.1.5 Lighting

### E-501 Fixture installation
- Tiers: T2, T3 · Task fit: CC, ID, TS
- Defects: non-IC can in insulation contact; fixture over tub without wet/damp rating; missing support independent of ceiling grid
- Ref: NEC 410

### E-502 Lighting controls & emergency egress
- Tiers: T2 · Task fit: CC, FD, DOC
- Defects: emergency fixture on switched leg; exit sign dead battery (test-button item); 3-way miswire diagnosis
- Ref: NEC 700, NFPA 101

## 2.1.6 Grounding & Bonding

### E-601 Grounding electrode system
- Tiers: T1, T2, T3 · Task fit: CC, ID, ME
- Defects: missing supplemental electrode; GEC spliced improperly; clamp not listed for direct burial
- Ref: NEC 250.50–250.68

### E-602 Equipment bonding
- Tiers: all · Task fit: CC, ID, HAZ
- Defects: missing bonding jumper around water meter; CSST gas line not bonded; isolated metal parts; missing bond at separately derived system
- Ref: NEC 250.104, 250.30
- Note: highest-stakes invisible-defect category — everything works fine until a fault. Core "installed-defective" territory.

### E-603 Pool/spa equipotential bonding
- Tiers: T3 · Task fit: CC, HAZ
- Defects: missing perimeter bond grid; unbonded pump motor; wrong wire (insulated where solid bare #8 required)
- Ref: NEC Art. 680

## 2.1.7 Low Voltage & Specialty

### E-701 Fire alarm devices & circuits
- Tiers: T2 · Task fit: CC, DOC, FD, SEQ
- Defects: smoke detector spacing/placement; missing end-of-line resistor; T-tapping on Class B circuit
- Ref: NFPA 72

### E-702 Data/comm & security
- Tiers: T2, T3 · Task fit: ID, TS, ME
- Defects: bend radius violations; untwisted pairs at termination >½ in.; plenum vs. riser cable in wrong space
- Ref: TIA-568, NEC 800

### E-703 Heat trace
- Tiers: T1 · Task fit: CC, FD, PA
- Defects: missing end seal; crossed circuits at insulation; no GFPE breaker
- Ref: NEC 427

## 2.1.8 Hazardous Locations (T1 overlay)

### E-801 Classified-area wiring methods
- Tiers: T1 · Task fit: CC, ID, TS, HAZ
- Defects: missing seal-off fitting at boundary; unpoured seal (visible fill hole plug); non-rated fixture in Class I Div 2; flexible cord where not permitted
- Ref: NEC 500–516
- Note: unpoured seal-offs are a famous "looks done, isn't" defect — ideal S2 installed-defective items.

---

## State hooks (S1 lifecycle → what a photo shows, Electrical edition)

| S1 state | Visible evidence in photos |
|----------|---------------------------|
| Staged | Material laydown: conduit bundles, wire reels, boxed devices with matching BOM |
| In-progress | Raceway up, no wire; boxes mounted, open |
| Rough-complete | Wire pulled, free conductors coiled in boxes, no devices, mud rings on — this is the "rough inspection" photo |
| Tested/Inspected | Megger/tester in frame, inspection sticker, panel schedule filled |
| Rework | Green tags/red tags, cut-out splices, abandoned raceway |
| Accepted/In-service | Deadfronts on, labeled, energized indicators |

**PA item recipe:** rules-of-credit for a branch circuit ≈ raceway 30% → wire pulled 25% → devices 20% → terminated at panel 15% → tested 10%. Show a photo, ask for % complete + remaining steps. (Percentages are placeholders — validate with estimators.)

---

## What to replicate for the other 11 disciplines
1. 5–8 sub-categories, 3–6 elements each (~30–45 elements/discipline)
2. Every element gets a defect library of ≥3 installed-defective conditions — this is the seed corpus for vision items
3. One "signature element" per discipline flagged like E-102/E-801 — visually rich, defect-dense, tier-spanning
4. State-hook table translating S1 states into visible evidence for that discipline
5. SME validation pass: a journeyman marks each defect as (a) real/common, (b) visible in a photo, (c) correctly attributed to the code section
