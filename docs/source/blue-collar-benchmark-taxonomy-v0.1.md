# Blue-Collar AI Benchmark — Taxonomy v0.1 (First Pass)

A three-axis taxonomy plus a unified state model. Every eval item gets coded on all three axes and (where applicable) one or more states. This lets you slice results by setting, by discipline, by cognitive skill, and by lifecycle stage.

---

## Axis 1 — Work Setting (Tier)

The same discipline (e.g., electrical) looks radically different across tiers: different codes, tolerances, materials, documentation, and consequence-of-error. Tier is the biggest driver of what "correct" means.

| Tier | Name | Description | Reference frameworks | Example environments |
|------|------|-------------|----------------------|----------------------|
| T1 | Heavy Industrial | Capital projects & process facilities. Engineered drawings, specs, ITPs, permits-to-work. | CII BM&M disciplines, AWP/IWPs, ASME, API, NEC Art. 500 (hazardous locations) | Refineries, power plants, chemical, mining, offshore |
| T2 | Commercial / Institutional | Code-driven building construction with inspections and submittals. | CSI MasterFormat, IBC, NEC, NFPA | Offices, hospitals, schools, warehouses, mid/high-rise |
| T3 | Residential / DIY | Light construction and homeowner-grade work. Prescriptive code paths, big-box materials, mixed skill levels. | IRC, NEC residential articles, manufacturer instructions | Single-family homes, remodels, DIY repairs |
| T4 | Field Service & Maintenance | Mobile diagnostic/repair work on installed assets. Work orders, not drawings. | OEM service manuals, flat-rate guides, PM schedules | Auto shops, HVAC service calls, appliance repair, utility line work, elevator service |
| T5 | Manufacturing / Assembly | Fixed-station, repetitive production work. Standard work instructions, takt time, quality gates. | MOST/MTM, standard work, AIAG/PPAP quality docs | Assembly lines, fab shops, panel shops, prefab/modular yards |

**Note:** T5 also captures the growing prefab overlap — a pipe spool welded in a shop is T5 work that becomes T1 work when erected in the field.

---

## Axis 2 — Work Discipline (What is being worked on)

Adapted from CII's 8 construction disciplines (concrete, structural steel, electrical, piping, instrumentation, equipment, insulation, scaffolding), extended to cover tiers CII doesn't reach. Three levels: **Discipline → Sub-category → Element**.

### 2.1 Electrical
- **Power distribution** — services/switchgear, panelboards, transformers, feeders
- **Raceway** — conduit (EMT/RMC/PVC), cable tray, wireways, boxes & fittings
- **Wire & cable** — pulling, terminations, splices, MC/NM cable
- **Devices & equipment** — receptacles, switches, motors, VFDs, disconnects
- **Lighting** — fixtures, controls, emergency/egress
- **Grounding & bonding** — electrodes, bonding jumpers, equipotential
- **Low voltage / specialty** — fire alarm, data, security, heat trace
- Tier notes: T1 adds hazardous-location classification; T3 swaps conduit for NM cable and AFCI/GFCI rules; T4 = troubleshooting live systems.

### 2.2 Mechanical — Piping & Plumbing
- **Process piping (T1/T2)** — large bore, small bore, spools, hangers/supports, welded vs. threaded vs. flanged
- **Plumbing (T2/T3)** — DWV, supply (copper/PEX/CPVC), fixtures, venting, gas piping
- **Hydronic & steam** — boilers, pumps, valves, traps
- **Testing** — hydro/pneumatic tests, leak checks
- Tier notes: T1 measured by diameter-inch of weld; T3 measured by "does the trap hold water."

### 2.3 HVAC-R
- **Equipment** — furnaces, AHUs, RTUs, condensers, heat pumps, chillers
- **Distribution** — ductwork fab & install, dampers, VAV boxes
- **Refrigeration circuit** — brazing, evacuation, charging, recovery (EPA 608)
- **Controls** — thermostats, BAS points, sequences of operation
- Spans T2 install, T3 residential, T4 service diagnostics.

### 2.4 Structural & Ironwork
- **Structural steel** — erection, bolting (snug vs. pretensioned), welding, decking
- **Reinforcing** — rebar placement, ties, post-tensioning
- **Ornamental/misc.** — stairs, rails, gates
- **Rigging & machinery moving** — crane picks, load charts, signals
- Primarily T1/T2; T5 for shop fabrication.

### 2.5 Concrete & Masonry
- **Formwork** — build, brace, strip
- **Placement & finishing** — pour, consolidate, screed, cure
- **Masonry** — brick/block/CMU, mortar, grouting, flashing
- **Foundations/slabs/structures** (CII's three concrete sub-categories)

### 2.6 Carpentry & Finishes
- **Rough framing** — walls, floors, roofs, headers, shear
- **Exterior envelope** — roofing, siding, windows/doors, WRB/flashing
- **Interior finish** — drywall, trim, cabinets, flooring, paint
- Heavily T2/T3; the biggest DIY category.

### 2.7 Equipment & Machinery (Millwright scope)
- **Setting & alignment** — anchor bolts, grout, laser/dial alignment
- **Rotating equipment** — pumps, compressors, gearboxes, bearings, seals
- **Conveyors & material handling**
- T1 install, T4/T5 maintenance.

### 2.8 Instrumentation & Controls
- **Field instruments** — transmitters, gauges, analyzers, tubing
- **Calibration & loop checks**
- **PLC/DCS I/O** — panel wiring, point-to-point checks
- Mostly T1; overlaps T5 (industrial maintenance techs).

### 2.9 Automotive & Powertrain (T4-dominant)
- **Engine & drivetrain** — diagnostics, timing, internals, transmissions
- **Chassis** — brakes, suspension, steering, alignment
- **Electrical & electronics** — OBD-II diagnostics, wiring, modules, ADAS
- **HVAC & fluids** — A/C service, cooling systems
- **EV systems** — high-voltage safety, battery service

### 2.10 Assembly & Fabrication (T5-dominant)
- **Fastening & joining** — torque specs, welding (SMAW/MIG/TIG/spot), adhesives, riveting
- **Fitment & tolerance** — gauging, GD&T basics, shimming
- **Line operations** — standard work execution, andon response, changeovers
- **Quality inspection** — visual standards, go/no-go, first-article

### 2.11 Sitework & Utilities
- **Excavation & trenching** — shoring, sloping, spoil placement
- **Underground utilities** — water/sewer/storm, duct banks, locates (811)
- **Heavy equipment operation** — grading, lifting, compaction

### 2.12 Cross-cutting: Safety & Rigging (applies to all)
- LOTO, confined space, fall protection, hot work, PPE selection, housekeeping/hazard recognition

### 2.13 Building Science & Indoor Environment (T3 expansion candidate)
- **Moisture & condensation** — dew point, surface-condensation risk, vapor drive, attic/crawlspace moisture, mold-conducive conditions
- **Air sealing & insulation** — stack effect, air-barrier continuity, thermal bridging, R-value/assembly reasoning
- **Ventilation & combustion safety** — residential ventilation sizing, bath/kitchen exhaust, backdrafting risk, CO alarm placement
- **Indoor air quality** — CO2/PM2.5/VOC/radon meter readings, humidity targets, filtration tradeoffs
- **Lighting** — lumen/illuminance calculations, color temperature, CRI, flicker diagnosis
- **EMF measurement literacy** — meter interpretation and evidence-calibrated risk communication
- Primarily T3 Residential / DIY; strongest fit for FD, HAZ, ME, SEQ, TS, and TRD.

---

## Axis 3 — Task Type (Cognitive skill the eval item tests)

| Code | Task type | Prototype multimodal question |
|------|-----------|-------------------------------|
| ID | Identification | "What component/tool/material is this?" |
| FD | Fault diagnosis | "Given this photo/sound/symptom set, what's the most likely failure?" |
| CC | Code/spec compliance | "Does this installation meet NEC 314.28 / the spec / the drawing?" |
| SEQ | Procedure sequencing | "Order these steps for a brake job / pipe test / panel swap." |
| TS | Tool & material selection | "Which fastener/wire size/blade is correct here, and why?" |
| HAZ | Hazard spotting | "Identify all safety violations in this jobsite photo." |
| ME | Measurement & estimation | "Estimate the conduit bend angle / board feet / torque from the image." |
| PA | Progress assessment | "What % complete is this work item? What's left?" |
| DOC | Document interpretation | "Read this P&ID / blueprint / wiring diagram and answer..." |
| TRD | Tradeoff judgment | "Textbook says X; field conditions show Y. What does a journeyman actually do?" |
| RES | Resource/constraint recovery | "Given a disrupted lookahead schedule, what can proceed, what is delayed, and which recovery plan is valid?" |

Every item = **Tier × Discipline.Sub-category × Task type** (e.g., `T3 × 2.2-Plumbing.DWV × CC`).

---

## Unified State Model

The glue across work, products, and overall progress. Three linked state machines that apply in every tier — this is what lets the *same question templates* run against a refinery pipe rack and a bathroom remodel.

### S1 — Work-Item Lifecycle (the task)

```
PLANNED → STAGED → IN-PROGRESS → ROUGH-COMPLETE → TESTED/INSPECTED → ACCEPTED → IN-SERVICE
                        ↓                                  ↓
                    ON-HOLD (constraint)              REWORK ← FAILED INSPECTION
```

| State | Definition | Tier-specific expression |
|-------|-----------|--------------------------|
| Planned | Scoped, not started | IWP issued (T1) / permit pulled (T3) / work order opened (T4) / job queued (T5) |
| Staged | Materials, tools, access ready | Kitted (T1/T5), parts on truck (T4) |
| In-progress | Physical work underway | — |
| Rough-complete | Installed but not closed in / finished | Rough-in (T2/T3), fit-up before weld-out (T1), sub-assembly (T5) |
| Tested/Inspected | Verification performed | Hydro test, megger, rough inspection, road test, first-article |
| Rework | Failed verification; redo | Punch list, comeback (T4), scrap/repair (T5) |
| Accepted | Signed off | Turnover package (T1), final inspection (T3), customer pickup (T4) |
| In-service | Operating; enters maintenance world | Handoff point from construction tiers to T4 |

### S2 — Component/Product Condition (the thing)

```
NEW → INSTALLED-CORRECT → WORN → DEGRADED → FAILED
         ↓
   INSTALLED-DEFECTIVE (latent — the money category for vision evals)
NON-COMPLIANT (correct function, violates code) — orthogonal flag
```

- **Installed-defective** is the highest-value eval state: looks done, is wrong (missing bonding jumper, backwards trap, under-torqued bolts). Tests whether a model sees what an inspector sees.
- **Non-compliant** is distinct from broken — a double-tapped breaker works fine until it doesn't.

### S3 — Progress / Earned Value (the project)

Borrowed from construction "rules of credit" — pre-agreed % credit per lifecycle milestone. Example, T1 piping: hangers 10%, spools erected 40%, welded 30%, tested 20%. Same logic ports everywhere:

| Tier | Progress vocabulary |
|------|---------------------|
| T1/T2 | Rules of credit, earned hours, % complete by quantity |
| T3 | Milestone draws (foundation / rough / final), inspection gates |
| T4 | Diagnosis → estimate approved → repair → QC/road test |
| T5 | Station completion, takt adherence, yield/first-pass quality |

**Eval use:** show a photo or short video → ask the model to (a) name the S1 state, (b) flag any S2 defect/non-compliance, (c) estimate S3 % complete and list remaining steps. That triple is a single reusable item template covering all tiers.

---

## Coverage Matrix (where to seed items first)

|  | T1 Heavy | T2 Comm. | T3 Res/DIY | T4 Field Svc | T5 Mfg |
|---|---|---|---|---|---|
| Electrical | ● | ● | ● | ● | ○ |
| Piping/Plumbing | ● | ● | ● | ● | ○ |
| HVAC-R | ○ | ● | ● | ● | — |
| Structural/Iron | ● | ● | ○ | — | ● |
| Concrete/Masonry | ● | ● | ● | — | — |
| Carpentry/Finishes | — | ● | ● | ○ | ○ |
| Equipment/Millwright | ● | ○ | — | ● | ● |
| Instrumentation | ● | ○ | — | ○ | ● |
| Automotive | — | — | ○ | ● | ● |
| Assembly/Fab | ○ | — | — | — | ● |
| Sitework/Utilities | ● | ● | ○ | ○ | — |
| Building Science / Indoor Environment | — | ○ | ● | ○ | — |
| Safety (cross-cut) | ● | ● | ● | ● | ● |

● = core cell (seed 20–50 items) ○ = secondary — = out of scope

---

## Open Questions for v0.2

1. **Sub-tier for DIY vs. licensed residential?** A homeowner question ("which wire nut?") and a residential journeyman question ("service upgrade load calc") differ hugely in difficulty. The expansion plan proposes `skill` tags (DIY / apprentice / journeyman / master) plus `escalation` labels (`none`, `diy-with-permit`, `licensed-pro`, `emergency`) rather than splitting T3.
2. **Jurisdiction handling** — NEC vs. CEC vs. IRC amendments. Tag items with code edition + jurisdiction, or keep v1 US/model-code only?
3. **Modality tags** — photo, video, audio (engine/arc sounds), thermal/IR, document scan. The expansion plan keeps modality as item metadata and adds paired transcript/audio, ordered frame sequences, and chart media.
4. **CII element-level detail** — full definitions are member-gated; if you or a collaborator has CII access, we can true-up 2.1–2.8 against their metric definitions.
