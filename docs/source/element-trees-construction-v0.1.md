# Element Trees v0.1 — Construction Disciplines
### 2.2 Piping/Plumbing · 2.3 HVAC-R · 2.4 Structural/Iron · 2.5 Concrete/Masonry · 2.6 Carpentry/Finishes · 2.11 Sitework
Same schema as Electrical: **Tiers · Task fit · Defect library · Ref**. Signature elements flagged ★.

---

# 2.2 Mechanical — Piping & Plumbing

## 2.2.1 Process Piping (T1/T2)

### P-101 Spool erection & fit-up ★
- Tiers: T1 · Task fit: PA, CC, ME, DOC, ID
- Defects: flange bolt-hole rotation wrong (two-holing missed); spool installed backwards vs. isometric flow arrow; excessive cold spring to force alignment; hi-lo mismatch at weld fit-up; wrong root gap
- Ref: ASME B31.3, project iso drawings
- Note: photo + isometric drawing = premier DOC item ("does the field match the iso?").

### P-102 Flanged joints
- Tiers: T1, T2 · Task fit: CC, SEQ, ID
- Defects: incomplete bolt pattern; wrong gasket type/material for service; no torque marks/witness lines; bolt thread engagement insufficient (less than flush); star-pattern torque sequence violated
- Ref: ASME PCC-1, B16.5

### P-103 Hangers & supports
- Tiers: T1, T2 · Task fit: CC, ID, FD
- Defects: spring can travel pins not pulled after hydro; shoe off its support; missing guides near expansion loops; rod max angle exceeded
- Ref: project support standards, MSS SP-58

### P-104 Pressure testing
- Tiers: T1, T2 · Task fit: SEQ, DOC, HAZ
- Defects: instruments not isolated before hydro; expired gauge calibration; test blinds missing/not rated; pneumatic test without exclusion zone
- Ref: ASME B31.3 §345

## 2.2.2 Plumbing — DWV (T2/T3)

### P-201 Traps & venting ★
- Tiers: T2, T3 · Task fit: CC, ID, FD
- Defects: S-trap (illegal siphon-prone config); flat/horizontal vent below flood rim; missing cleanout; double-trapped fixture; AAV where prohibited
- Ref: IPC/UPC
- Note: the S-trap-under-a-sink photo is the "hello world" of DIY plumbing evals.

### P-202 Drain slope & routing
- Tiers: T2, T3 · Task fit: ME, CC
- Defects: slope under ¼ in/ft (or over — solids stranding on steep runs); back-graded section (puddle test); improper fitting direction (using a vent tee on its back for drainage)
- Ref: IPC 704

### P-203 Material transitions
- Tiers: T3, T4 · Task fit: TS, CC, ID
- Defects: unshielded (wrong) rubber coupling underground vs. shielded; ABS-to-PVC glued with wrong cement; no dielectric union copper-to-steel
- Ref: IPC, mfr listings

## 2.2.3 Plumbing — Supply

### P-301 PEX & copper installation
- Tiers: T2, T3 · Task fit: CC, ID, ME
- Defects: crimp ring fails go/no-go gauge; PEX unsleeved through slab; copper unreamed (visible burr); flux residue not wiped (green corrosion); missing nail plates
- Ref: IPC, mfr specs

### P-302 Water heaters ★
- Tiers: T3, T4 · Task fit: CC, HAZ, SEQ, FD
- Defects: T&P discharge pipe missing/trapped/reduced/terminated too high; no expansion tank on closed system; gas flex connector through cabinet wall; no drip pan where required; backdrafting flue (melted grommets — FD)
- Ref: IPC 504, IRC P2804
- Note: single most defect-dense residential photo subject after the electrical panel.

### P-303 Gas piping
- Tiers: T3, T4 · Task fit: CC, HAZ, TS
- Defects: missing sediment trap/drip leg; CSST not bonded; wrong thread sealant (not gas-rated); uncapped stub
- Ref: IFGC, NFPA 54

## 2.2.4 Hydronic & Steam

### P-401 Boiler & pump piping
- Tiers: T2, T4 · Task fit: FD, CC, DOC
- Defects: pump pumping toward expansion tank (point-of-no-pressure-change violated); air separator in wrong location; missing check valve causing gravity flow; steam trap installed backwards (arrow visible — ID)
- Ref: mfr manuals, hydronics references

**State hooks (piping):** Staged = spools in laydown with heat numbers · Rough-complete = erected & fit-up, not welded out / DWV before cover inspection · Tested = hydro gauge + filled test package · Rework = cut-out weld, repair stencil.

---

# 2.3 HVAC-R

## 2.3.1 Equipment Installation

### H-101 Condenser/heat pump setting
- Tiers: T2, T3 · Task fit: CC, ME, ID
- Defects: clearance to wall/other units below mfr minimum; pad not level (oil return); line set uninsulated suction; no service disconnect within sight
- Ref: mfr install manual, IMC/IRC M1401

### H-102 Furnace & venting ★
- Tiers: T3, T4 · Task fit: CC, HAZ, FD
- Defects: condensate line without trap or sloped wrong; PVC flue slope back-pitched (condensing); single-wall vent clearance to combustibles; return air from garage (HAZ); flame rollout evidence (FD)
- Ref: IRC M1801, NFPA 54

## 2.3.2 Distribution

### H-201 Duct installation
- Tiers: T2, T3 · Task fit: CC, ME, PA
- Defects: unsealed joints (no mastic/foil tape — cloth duct tape is the classic wrong answer, great ID item); crushed or excessively long flex duct; sagging flex (>½ in/ft between supports); panned joist returns leaking
- Ref: IMC 603, SMACNA, Manual D

### H-202 Terminations & balancing
- Tiers: T2 · Task fit: ME, DOC, FD
- Defects: damper positions vs. balance report mismatch; supply short-circuiting to return; missing balancing dampers at branch takeoffs
- Ref: SMACNA, TAB reports

## 2.3.3 Refrigeration Circuit ★

### H-301 Brazing & evacuation
- Tiers: T2, T3, T4 · Task fit: SEQ, CC, FD
- Defects: brazed without nitrogen purge (black scale inside — shows in cutaway photos); vacuum not held at target microns (decay test — read the gauge, FD); Schrader cores left in during evacuation (SEQ)
- Ref: mfr specs, ACCA, EPA 608

### H-302 Charging & diagnostics
- Tiers: T4 · Task fit: FD, ME, DOC
- Defects: charged to "beer-can cold" instead of subcool/superheat targets; gauge readout interpretation (low charge vs. TXV starving vs. dirty coil — classic FD triple); sight-glass bubbles misread
- Ref: mfr charging charts

## 2.3.4 Controls

### H-401 Thermostats & sequences
- Tiers: T3, T4 · Task fit: FD, SEQ, DOC
- Defects: heat pump O/B reversing valve config wrong (heats when calling cool); no C-wire (power-stealing issues); aux heat locked on; sensor over a supply register
- Ref: mfr manuals

**State hooks (HVAC):** Rough-complete = duct up before insulation/cover, line set run uncharged · Tested = pressure/vacuum gauges in frame, startup sheet · In-service = charged, panels on, disconnect labeled.

---

# 2.4 Structural & Ironwork

## 2.4.1 Steel Erection

### S-101 Column/beam erection & plumb
- Tiers: T1, T2 · Task fit: PA, ME, HAZ
- Defects: temporary bracing removed before decking/permanent stability; anchor bolts field-bent to fit; shims missing under base plate; column out of plumb (estimate from photo — ME)
- Ref: AISC 303, OSHA 1926 Subpart R

### S-102 Structural bolting ★
- Tiers: T1, T2, T5 · Task fit: CC, ID, ME
- Defects: DTI squirter washers not fully crushed; turn-of-nut match marks absent or not rotated; wrong bolt grade (head markings — ID from photo); bolts snug-tight where pretension specified; thread not excluded from shear plane where required
- Ref: RCSC Specification
- Note: bolt head markings + match marks make dense, objective vision items.

### S-103 Structural welding
- Tiers: T1, T2, T5 · Task fit: ID, ME, CC, DOC
- Defects: visible undercut/porosity/incomplete fusion; fillet undersized vs. callout (gauge in photo — ME); missing weld per drawing (DOC: compare to detail); welding without qualified WPS parameters
- Ref: AWS D1.1

## 2.4.2 Reinforcing

### S-201 Rebar placement ★
- Tiers: T1, T2, T3 · Task fit: CC, ME, PA, DOC
- Defects: insufficient cover (bars touching form/ground); lap splice too short (count bar diameters — ME); missing chairs/supports (mat on dirt); wrong bar size vs. schedule (deformation count/size — ID+DOC); congestion blocking concrete flow
- Ref: ACI 318, ACI 117, placing drawings
- Note: pre-pour photos are abundant online and inspection-critical — high-volume item source.

### S-202 Post-tensioning
- Tiers: T2 · Task fit: SEQ, HAZ, DOC
- Defects: stressing before concrete strength verified; standing in line with tendon during stressing (HAZ); elongation record vs. calculated mismatch (DOC)
- Ref: PTI

## 2.4.3 Rigging & Machinery Moving ★

### S-301 Rigging configuration
- Tiers: T1, T2, T5 · Task fit: HAZ, ME, TS, CC
- Defects: shackle side-loaded; sling angle under 30° (tension math — ME); hook latch missing/tied back; slings over unprotected edges; using damaged sling (cut strands — ID)
- Ref: ASME B30, OSHA 1926.251

### S-302 Crane operations
- Tiers: T1, T2 · Task fit: DOC, ME, HAZ, TRD
- Defects: load + rigging vs. load chart at radius (DOC+ME); outriggers not fully extended on mats; working under suspended load; power line clearance
- Ref: OSHA 1926.1400, load charts

**State hooks (structural):** In-progress = iron up, bolts snug, bracing on · Rough-complete = bolted out/welded out, decking down · Tested/Inspected = bolt inspection marks, weld inspection stencils/NDE reports · Accepted = fireproofing/paint touch-up done.

---

# 2.5 Concrete & Masonry

## 2.5.1 Formwork

### C-101 Form build & bracing
- Tiers: T1, T2, T3 · Task fit: HAZ, ME, PA
- Defects: inadequate bracing/kickers for pour pressure; forms not oiled; blowout evidence; penetrations/blockouts missing vs. drawings (DOC)
- Ref: ACI 347

## 2.5.2 Placement & Finishing ★

### C-201 Concrete placement
- Tiers: T1, T2, T3 · Task fit: ID, FD, SEQ, HAZ
- Defects: cold joint visible between lifts; honeycomb from missed vibration; segregation from excessive drop height; adding water on site (slump manipulation — TRD: common but wrong); rain on fresh finish
- Ref: ACI 301, 304

### C-202 Finishing & curing
- Tiers: T2, T3 · Task fit: SEQ, FD, ID
- Defects: troweling bleed water back in (dusting/scaling later — FD from failed-surface photos); no cure (blankets/compound absent in photo); sawcut joints late (random cracking — FD); plastic shrinkage cracks (diagnose cause)
- Ref: ACI 302, 308

## 2.5.3 Masonry

### C-301 Block/brick laying
- Tiers: T2, T3 · Task fit: CC, ID, ME
- Defects: head joints unfilled (visible voids); joints not tooled concave (water entry); bond pattern broken; ladder reinforcement spacing exceeded; grout lift too tall without cleanouts
- Ref: TMS 402/602

### C-302 Flashing & weeps ★
- Tiers: T2, T3 · Task fit: CC, ID
- Defects: weep holes missing/blocked at bottom course; flashing not lapped/sealed; mortar bridging the cavity (droppings on ties)
- Ref: TMS 402, BIA tech notes
- Note: invisible-after-completion defect class — pairs well with in-progress vs. finished photo comparisons.

**State hooks (concrete):** Staged = forms/rebar staged, pour scheduled · Rough-complete = placed & finished, forms on · Tested = cylinders cast (visible molds), break reports (DOC) · Accepted = stripped, patched, cured.

---

# 2.6 Carpentry & Finishes

## 2.6.1 Rough Framing ★

### F-101 Structural framing
- Tiers: T2, T3 · Task fit: CC, ME, DOC
- Defects: undersized header (span vs. table — ME+DOC); notching/boring beyond IRC limits (notch depth vs. joist depth — measurable in photo); missing jack studs; load path discontinuity; crowns down
- Ref: IRC R502, R602

### F-102 Connectors & fasteners
- Tiers: T2, T3 · Task fit: ID, CC, TS
- Defects: roofing nails in joist hangers (the classic — ID by head size/pattern); missing hanger nails (empty holes); wrong hanger for joist size; hurricane ties absent where required; over-driven nails in shear panels
- Ref: Simpson catalogs, IRC

### F-103 Fireblocking & draftstopping
- Tiers: T2, T3 · Task fit: CC, ID
- Defects: open stud bays at floor transitions; unblocked soffits; foam where fire-rated sealant required (ID by color/label)
- Ref: IRC R302

## 2.6.2 Exterior Envelope ★

### F-201 Flashing & WRB integration
- Tiers: T2, T3 · Task fit: SEQ, CC, ID
- Defects: reverse-lapped WRB (upper layer behind lower); window pan flashing absent; tape sequence wrong at sill; kick-out flashing missing at roof-wall
- Ref: IRC R703, mfr instructions
- Note: shingle-lap logic is a perfect SEQ item — order the layers.

### F-202 Roofing
- Tiers: T2, T3 · Task fit: CC, ME, ID
- Defects: nail placement high/exposed; insufficient overhang; ice barrier missing in cold climate; improper valley weave; pipe boot cracked (T4 FD)
- Ref: IRC R905, mfr specs

## 2.6.3 Interior Finish

### F-301 Drywall & finishing
- Tiers: T2, T3 · Task fit: CC, ME, ID
- Defects: screw spacing exceeded; joints not staggered; no gap at floor; wrong board in wet area (ID by color); fire-rated assembly penetrations unsealed
- Ref: GA-216, IRC

### F-302 Trim, cabinets, flooring
- Tiers: T3 · Task fit: TS, ME, FD
- Defects: cabinets not hitting studs (screw pattern — ME); floating floor without expansion gap (buckling — FD); tile on single-layer subfloor deflection
- Ref: mfr instructions, TCNA

**State hooks (carpentry):** Rough-complete = framed, pre-insulation inspection · Tested/Inspected = framing inspection tag · In-progress finish = hung/taped/primed stages read cleanly for PA items.

---

# 2.11 Sitework & Utilities

## 2.11.1 Excavation & Trenching ★

### U-101 Trench protection
- Tiers: T1, T2 · Task fit: HAZ, ME, CC, DOC
- Defects: unprotected trench ≥5 ft with workers in it; spoil pile within 2 ft of edge; no ladder within 25 ft lateral travel; trench box void behind shield; sloping wrong for soil type (DOC: tabulated data)
- Ref: OSHA 1926 Subpart P
- Note: the highest-fatality-rate defect class in the file — HAZ items write themselves from real citation photos.

## 2.11.2 Underground Utilities

### U-201 Locates & marking ★
- Tiers: T1, T2, T3 · Task fit: ID, CC
- Defects: digging without 811 locate; misreading mark colors (red=electric, yellow=gas, blue=water, green=sewer, orange=comm — pure ID item); mechanical digging inside tolerance zone
- Ref: 811/CGA best practices

### U-202 Pipe bedding & backfill
- Tiers: T1, T2 · Task fit: CC, SEQ, ME
- Defects: rocks against pipe (no bedding sand); missing tracer wire on non-metallic; lifts too thick for compactor; no warning tape at depth
- Ref: project specs, IPC 306

## 2.11.3 Heavy Equipment Operation

### U-301 Equipment safety
- Tiers: T1, T2 · Task fit: HAZ, TRD
- Defects: personnel in swing radius; no spotter while backing near trench; bucket raised while traveling; riding in bucket
- Ref: OSHA 1926 Subpart O

**State hooks (sitework):** In-progress = open trench, protection in · Rough-complete = pipe laid, bedding placed, pre-backfill inspection · Accepted = compaction reports (DOC), surface restored.
