# Electrical Discipline Expansion v0.2 — Training-Corpus Analysis
### Source analysis, evaluation-method upgrades, and a 1,000-task expansion plan · Blue-Collar AI Benchmark

**Basis:** full inventory of a national electrical-training publisher's free-publications
library (63 resources; referred to below as **Corpus A**), a review of a master-electrician
CEU trainer's site (**Corpus B**), content review of eight representative PDFs, and a
quantitative audit of the current 2.1 Electrical catalog slice. Source identities are kept
out of this document and the generated items by design; the raw URL inventory lives in the
maintainers' notes, not the repo.

**Companion artifacts:**
- `scripts/gen_electrical_expansion_specs.py` — deterministic generator
- `docs/source/electrical-expansion-v0.2-task-catalog.json` — 1,000 task specs emitted by the generator

---

## 1. What the free training corpus actually contains

The 63 free resources cluster into eight content families. Each family maps to a distinct
stage of the electrician process, and most map to evaluation capabilities the current
benchmark does not exercise.

| # | Content family | Key resources | Process stage | Currently evaluated? |
|---|---|---|---|---|
| 1 | Electrical theory & math | *Electrician's Math and Basic Electrical Formulas* (units 10–15: fractions/percentages, trig, Ohm's law, Watt's law, series & parallel circuits), *Equations Chart*, 4 Ohm's-law posters | Training / exam prep / daily field math | **No** — no formula-driven items exist |
| 2 | NEC article deep-dives | GFCI & AFCI (210.8/210.12, 5 cycles), Fire Alarm (760), Generators & Standby (445/700/701/702), Marinas (555), Pools/Spas (680), Radio & TV (Ch. 8/810) — each published per code cycle 2011→2023 | Design, rough-in, trim, inspection | **Partial** — E-402/E-603/E-701 exist but hold 2–16 items each |
| 3 | Code-cycle change guides | Top-10 rule changes for 2011/2014/2017/2023, 2020 summary | Jurisdiction awareness, continuing education | **No** — no cycle-delta items |
| 4 | Code navigation aids | NEC Index (5 cycles), code-book tabbing guides (6 cycles), Code Organizing Drawing | Exam prep, document lookup speed | **No** — DOC items never test "which article governs X" |
| 5 | Installation technique | *Hand Bending Conduit and Tubing* (Bamford): stub-up deducts, offset multipliers, shrink per inch of rise, 3-point/4-point saddles, segment bending | Rough-in craft skill | **Partial** — E-201 has bend-defect items but no bend-math items |
| 6 | Specialized system design | *Guide to PV System Design and Installation* (CEC): string sizing, mounting, output estimation, interconnection | Design & renewables retrofit | **No** — zero PV items |
| 7 | Forensic / failure studies | CPSC GFCI failure analysis, NEMA GFCI failure study, NEMA *Evaluating Fire and Heat-Damaged Electrical Equipment*, NEMA GD-1 *Evaluating Water-Damaged Electrical Equipment*, UL White Book | Service, insurance/restoration work | **No** — no damage-triage items |
| 8 | Business operations | Electrical proposal template, employee handbook sample, customer & employee surveys, social-media marketing guide, emergency-backup customer flyer | Estimating, contracting, customer relations | **No** — the trade's business half is absent |

**Corpus B** (the CEU trainer's site) is smaller but adds three things Corpus A does not:

1. **Continuing education as a process stage.** State re-licensure runs on CEU hours and
   live code-update classes. That makes "current-cycle awareness under a re-licensure
   deadline" a realistic scenario frame for the code-cycle items (§4.5), not just an
   abstract jurisdiction fact.
2. **A bonding decision flow chart** — a printable yes/no decision tree for
   grounding-vs-bonding questions. Decision-tree walks are directly gradable with the
   existing `expected_order` machinery (§4.13).
3. **Field-photo-derived training graphics.** The trainer builds teaching graphics from
   installation photographs collected nationwide — exactly the shot-list model the image
   conversion pass (§4.8) should follow: one real-world scene, one rule, one visible
   determination.

Two structural observations about Corpus A itself:

1. **The library is organized by code cycle.** Every NEC-article guide exists for 3–5
   editions. Real electricians work across cycles — a service electrician in a 2017
   jurisdiction must not apply 2023 rules and vice versa. This is a *judgment skill* the
   benchmark can test deterministically (see §4.5).
2. **The forensic studies are decision *tables*.** NEMA GD-1 and the fire/heat guide give
   explicit replace-vs-recondition verdicts per equipment class (e.g. molded-case breakers
   exposed to water: **replace, always**; larger switchgear: recondition only with
   manufacturer involvement). Decision tables translate directly into deterministic
   pass/fail/NMI items with zero grading ambiguity.

## 2. The electrician process, end to end

The current element tree (E-101…E-801) models electrical work as *installed hardware in a
lifecycle state*. That covers the middle of the process well but misses both ends. The full
process an electrician actually moves through:

```text
P0  Training & licensure ......... theory, math, code navigation, exam prep, CEUs
P1  Estimating & bidding ......... takeoff, labor units, proposal writing
P2  Design & calculation ......... load calcs, conductor/OCPD sizing, voltage drop
P3  Planning & permitting ........ permit scope, inspection scheduling, AHJ cycle
P4  Rough-in ..................... raceway, bending, boxes, pulling      [covered]
P5  Trim & finish ................ devices, fixtures, plates, labeling   [covered]
P6  Testing & verification ....... megger, GFCI test, torque, polarity   [partial]
P7  Inspection & correction ...... AHJ walk, red tags, re-inspection     [covered]
P8  Energize & commission ........ transfer tests, load bank, sequence   [partial]
P9  Troubleshooting & service .... systematic FD, meter method           [partial]
P10 Maintenance & monitoring ..... IR scans, PM programs, trending       [thin]
P11 Forensics & restoration ...... water/fire damage triage, aged gear   [absent]
P12 Special systems .............. PV, pools, marinas, fire alarm,
                                   generators, comms                     [thin/absent]
P13 Business & customer .......... change orders, ethics under pressure,
                                   crew supervision                      [absent]
```

The training corpus supplies authoritative source material for exactly the stages marked
absent or thin: P0–P2 (math/theory/navigation), P11 (NEMA/CPSC studies), P12 (article
guides + PV guide), P13 (business documents).

## 3. Quantitative audit of the current electrical slice

From the live item catalog (`benchmark/items/*.json`, discipline 2.1, 500 items):

**Element concentration.** Three elements (E-102 panelboards, E-301 conductor sizing,
E-303 terminations) hold 170 items — 34% of the slice — while E-603 pool bonding has **2**,
E-502 lighting controls **5**, E-302 NM routing **6**, E-701 fire alarm **8**, E-401
receptacles **9**. The elements with the most source depth in the corpus (GFCI, pools, fire
alarm) are the thinnest.

**Tier skew.** T1 203 / T2 158 / T3 83 / T4 33 / T5 23. The service electrician (T4) — the
role most exposed to ambiguous, judgment-heavy work and the primary audience of the
forensic studies — is the least represented.

**Task-type mix.** ME = 40 items (8%), and none require computing anything; they are
read-a-value items. SEQ = 34, mostly ordering named steps rather than gated hold points.

**Modality.** 480 text / 20 audio / **0 image** — electrical is the discipline whose
defects are most photographable (the element tree itself calls E-102 "the single best
photo-eval element"), yet it has no image item at all.

**Decision balance.** 230 fail / 204 pass / 66 NMI — acceptable overall, but NMI is
concentrated in generated boilerplate ("photo is blocked by glare") rather than
*domain-motivated* insufficiency (e.g. "cannot determine GFCI requirement without knowing
the code cycle in force").

## 4. Better ways to evaluate each part of the process

The grader (`scripts/grade_v2.py`) already supports numeric answers
(`expected_value`/`value_tolerance`), ordering (`expected_order`), percent tolerance, and
forbidden-phrase traps. The upgrades below need **no grader changes** unless noted.

### 4.1 Computed-answer ME items (P0/P2 — theory & design math)
Today's ME items ask the model to *read* a value. The corpus's math material enables items
where the model must *compute* one, graded with `expected_value` ± tolerance:

- Ohm's/Watt's law sanity checks: "heater nameplate 4,800 W at 240 V; clamp meter reads
  31 A — is the reading normal?" (compute 20 A, decision = fail, value = 20).
- Voltage drop: VD = 2·K·I·L/CM against the 3%/5% recommendation, with the *decision*
  derived from the computed value — a single item grades both the arithmetic and the
  judgment.
- Ampacity with 310.15 correction *and* adjustment factors chained.
- Box fill per 314.16 (count × volume allowance vs. box cubic inches).
- Bend math from the Bamford manual: offset multipliers, shrink per inch of rise,
  stub-up deducts — the classic apprentice-exam item family.
- Motor FLC → OCPD percentage → next-standard-size (430.52 + 240.6): a three-hop chain
  where a plausible one-hop answer is wrong. Multi-hop chains are the strongest
  discriminator between pattern-matching and working the method.
- Dwelling load calculation (Art. 220): general lighting VA → demand factors → service size.

**Why this is better:** keyword grading rewards mentioning the right nouns;
computed-answer grading is immune to verbal fluency. It also produces items whose ground
truth is *provably* correct (generated and verified by the same formula), eliminating the
SME-labeling error channel for a third of the expansion.

### 4.2 Decision-table forensics (P11 — NEMA/CPSC studies)
Encode the NEMA GD-1 and fire/heat tables directly: equipment class × exposure →
replace / recondition-with-manufacturer / evaluate. The model sees a restoration scenario
("flood water reached 18 in.; panelboard, MCCBs, NM cable, and a dry-type transformer were
submerged") and must produce per-component verdicts. Grading is exact because the source
*is* a table. Dangerous-false-pass weighting applies naturally — "dry it out and re-energize"
on a submerged MCCB is the canonical dangerous pass.

### 4.3 Paired counterfactuals (all task types)
For every fail item generated from a defect, emit a minimally-different pass twin (the same
scene with the defect corrected) under a shared `pair_id`. Reporting per-pair discrimination
(both right vs. systematic bias) separates *knowing the rule* from *always saying fail* —
the current fail-heavy catalog can't distinguish a calibrated model from an alarmist one at
the item level. **Grader change:** none; add pair-aware aggregation in
`collect_run_results.py`.

### 4.4 Code-citation grading (P0/P7 — navigation)
The NEC Index and tabbing guides exist because *finding* the rule is a tested trade skill.
Add DOC items whose required finding is the governing article/section itself
(`required_findings: [["min", "680.22"], ...]` with accepted aliases). This measures whether
the model's justification is grounded in the actual rule rather than plausible boilerplate —
today references are collected but never graded.

### 4.5 Code-cycle awareness (P3/P9 — jurisdiction judgment)
The corpus ships every guide in 3–5 editions precisely because the answer changes by cycle.
Items state the adopted cycle in the scenario ("this jurisdiction enforces the 2017 NEC")
and pick rules that flipped between cycles (e.g. GFCI for 250 V dwelling ranges/dryers —
2020 change; emergency disconnects, 230.85). Correct answers require *conditioning on
stated jurisdiction*, an NMI generator that is domain-motivated rather than "photo blurry":
if the cycle isn't stated and the rule flipped, the right decision is `needs_more_info`.

### 4.6 Legal-but-won't tradeoffs (P4/P5 — craft judgment)
The element tree already flags backstabbing as "legal but journeymen won't." Extend the
family with corpus-grounded cases: reconditioning water-exposed devices the NEMA table
technically allows with manufacturer sign-off; sharing a neutral on AFCI circuits (works
with 2-pole AFCI, nuisance-trips otherwise); PVC where legal but heat-inappropriate. TRD
items should grade the *documented tradeoff*, with `forbidden` phrases blocking both
absolutist answers ("never permitted") and rubber-stamps.

### 4.7 Sequenced hold points (P3/P6/P8 — process gating)
Current SEQ items order visible steps. Better: sequences with **inspection/permit/test
gates** where the failure is doing compliant work *out of gate order* (insulating before
rough inspection passes; energizing a generator transfer switch before the load-bank test;
pouring the pool deck before the bonding-grid inspection). Grade with `expected_order` plus
a forbidden early-step trap.

### 4.8 Tester-readout multimodal (P6 — verification)
The receptacle-tester light pattern, multimeter display, megger reading, or GFCI-tester
result *is* the evidence. These are cheap synthetic images (existing
`gen_media_items.py` pattern — the brake-rotor micrometer items prove the pipeline) and fix
the 0-image gap with images whose information content is unambiguous.

### 4.9 Audio-native protection behavior (P9 — service)
Extend the 20 existing audio items with protection-device signatures: AFCI trip-click vs.
thermal-trip hum, generator transfer-switch sequence timing (V suffix), arcing vs. loose-
lamination buzz. The CPSC/NEMA GFCI studies document failure modes (end-of-life, reversed
line/load) that have distinct test-button behavior — an audio+sequence hybrid family.

### 4.10 Estimating/takeoff DOC-ME hybrids (P1 — business math)
From a described one-line or panel schedule: count devices, total VA per circuit, or check
a proposal quantity against the plan. Deterministic (counts and sums), and it evaluates the
half of the trade — P1/P13 — that the benchmark currently ignores entirely.

### 4.11 Customer-pressure ethics (P13 — the human process)
The proposal/handbook/marketing documents frame the contractor reality: customers ask to
skip permits, reuse flooded panels, "just make it work by Friday." These are TRD/HAZ items
with the *decision* anchored to objective rules (permit required; NEMA says replace) but
the scenario framed as social pressure — measuring whether the model holds the line when
the prompt pushes back. `forbidden` phrases catch capitulation ("since the customer
insists…").

### 4.12 Risk-taxonomy sharpening (all)
Electrical fails conflate three severity families: shock/electrocution (GFCI, bonding,
marina ESD), fire (AFCI, terminations, overload), and code-only (workmanship). Tag each
expansion item with `hazard_class` metadata so dangerous-false-pass analysis can report
"model misses shock hazards specifically" — a materially more actionable finding than a
flat false-pass rate. **Grader change:** metadata only, no scoring change.

### 4.13 Decision-tree walk grading (P0/P4 — bonding logic)
Corpus B's bonding flow chart shows that working electricians navigate
grounding-vs-bonding questions as a yes/no decision tree, not as freeform recall. Items can
present a scenario and require the *traversal* — the ordered gate questions and the branch
taken — graded with `expected_order`, with the terminal verdict graded as the decision.
This catches models that reach the right answer through the wrong logic, which keyword
grading cannot.

## 5. New element tree — six subcategories, 32 elements

Numbering continues the existing scheme (subcategory 2.1.9 → E-9xx, 2.1.10 → E-10xx, …).
Existing elements E-101…E-801 are unchanged; where an expansion element deepens an existing
one (e.g. E-1104 vs. E-402), the expansion element is scoped to the *process skill* (field
testing protocol) rather than the hardware.

### 2.1.9 Theory & Calculation *(source: Basic Math PDF, Equations Chart, Ohm's-law posters, Bamford manual)*
| Element | Name | Tiers | Task fit | Ground truth |
|---|---|---|---|---|
| E-901 | Ohm's & Watt's law field checks | T3 T4 T5 | ME FD | computed, ±2% |
| E-902 | Series/parallel circuit analysis | T4 T5 | ME FD | computed, ±2% |
| E-903 | Voltage drop & remediation | T1 T2 T3 | ME TS CC | computed, ±0.2 V |
| E-904 | Ampacity w/ correction & adjustment | T1 T2 | ME CC TS | computed, table-derived |
| E-905 | Box & raceway fill calculations | T2 T3 | ME CC | computed per 314.16 |
| E-906 | Bend geometry (offset/saddle/shrink) | T1 T2 | ME SEQ TS | computed, Bamford multipliers |
| E-907 | Motor FLC / OCPD / overload sizing | T1 T5 | ME TS CC | computed, 430 tables |
| E-908 | Transformer FLA & OCPD sizing | T1 T2 | ME CC | computed, 450.3 |
| E-909 | Dwelling service load calculation | T3 | ME DOC | computed, Art. 220 |
| E-910 | Power factor & efficiency | T1 T5 | ME TRD | computed, ±1% |

### 2.1.10 Code Navigation & Documents *(source: NEC Index ×5, tabbing guides ×6, Code Organizer, UL White Book)*
| Element | Name | Tiers | Task fit | Notes |
|---|---|---|---|---|
| E-1001 | Governing-article identification | T2 T3 T4 | DOC CC | citation-graded (§4.4) |
| E-1002 | Code-cycle deltas & jurisdiction | T2 T3 T4 | DOC TRD CC | cycle-conditioned (§4.5) |
| E-1003 | Listing, labeling & field modification | T1 T2 T5 | CC TS TRD | UL White Book categories |
| E-1004 | Panel schedules, one-lines & plans | T1 T2 | DOC ID ME | takeoff-adjacent |
| E-1005 | Permit & inspection workflow | T2 T3 | SEQ DOC TRD | gated sequences (§4.7) |

### 2.1.11 Protection & Life Safety *(source: GFCI/AFCI guides ×3, Fire Alarm 760 ×4, Generators 445/700–702 ×5, CPSC & NEMA GFCI studies)*
| Element | Name | Tiers | Task fit | Notes |
|---|---|---|---|---|
| E-1101 | GFCI placement — dwelling (210.8(A)) | T3 | CC ID | location matrix |
| E-1102 | GFCI placement — non-dwelling/special (210.8(B)) | T2 T4 | CC TRD | |
| E-1103 | AFCI requirements & retrofit paths (210.12) | T3 T4 | CC TRD FD | shared-neutral traps |
| E-1104 | GFCI/AFCI field testing & end-of-life | T3 T4 | FD SEQ HAZ | CPSC/NEMA failure modes |
| E-1105 | Fire alarm circuits & supervision (760/NFPA 72) | T2 | CC FD DOC | class A/B, EOL resistor |
| E-1106 | Generator install & transfer equipment (445/702) | T2 T3 T4 | CC SEQ ID | backfeed = signature hazard |
| E-1107 | Standby classification & load priority (700/701/702) | T1 T2 | TRD CC DOC | emergency vs optional |

### 2.1.12 Special Occupancies & Renewables *(source: Pools 680 ×5, Marinas 555 ×4, PV guide, Radio/TV Ch. 8 ×5)*
| Element | Name | Tiers | Task fit | Notes |
|---|---|---|---|---|
| E-1201 | Pool/spa wiring, clearances & receptacle distances | T2 T3 | CC ME HAZ | complements E-603 bonding |
| E-1202 | Hot tub/spa packaged-unit installs | T3 T4 | CC SEQ | disconnect within sight |
| E-1203 | Marina/dock power & ESD | T2 T4 | CC HAZ FD ME | leakage measurement items |
| E-1204 | PV array design & stringing | T2 T3 | ME TS CC | Voc temp correction math |
| E-1205 | PV interconnection, rapid shutdown, labeling | T2 T3 | CC ID DOC | 120% rule computed |
| E-1206 | Antenna/comm grounding (800/810) | T2 T3 | CC ID | mast grounding conductor |

### 2.1.13 Forensics, Service & Maintenance *(source: NEMA GD-1, NEMA fire/heat guide, CPSC & NEMA GFCI studies)*
| Element | Name | Tiers | Task fit | Notes |
|---|---|---|---|---|
| E-1301 | Water-damaged equipment triage | T3 T4 | CC TRD TS | NEMA GD-1 decision table |
| E-1302 | Fire/heat-damaged equipment evaluation | T2 T4 | CC TRD HAZ | replace vs recondition |
| E-1303 | Legacy-system service decisions | T3 T4 | TRD HAZ CC | FPE/Zinsco, K&T, cloth NM, Al branch |
| E-1304 | Systematic troubleshooting with meters | T3 T4 T5 | FD SEQ ME | half-split method sequences |
| E-1305 | Thermal/PM inspection programs | T1 T5 | FD ME PA | IR delta-T thresholds |

### 2.1.14 Business, Estimating & Customer Process *(source: proposal template, handbook, surveys, marketing guide, emergency-backup flyer)*
| Element | Name | Tiers | Task fit | Notes |
|---|---|---|---|---|
| E-1401 | Takeoff & estimating | T2 T3 | ME DOC PA | count/sum-graded |
| E-1402 | Proposals, scope & change orders | T2 T3 T4 | DOC TRD | scope-boundary reading |
| E-1403 | Customer-pressure ethics | T3 T4 | TRD HAZ | §4.11 pattern |
| E-1404 | Crew planning & apprentice supervision | T1 T2 | SEQ TRD HAZ | qualified-person rules |

Defect/variant libraries for all 32 elements live in the generator
(`scripts/gen_electrical_expansion_specs.py`) as reviewable data.

## 6. The 1,000-task expansion

The generator emits exactly 1,000 specs, deterministic under a fixed seed, schema-aligned
with the live catalog (same field names the grader consumes: `decision`, `risk`,
`required_findings`, `required_actions`, `forbidden`, `expected_value`/`value_tolerance`,
`source_refs`, plus `pair_id` and `hazard_class` metadata from §4.3/§4.12).

Achieved distribution (printed by the generator run, seed 20260707):

| Subcategory | Items | Ground truth |
|---|---:|---|
| 2.1.9 Theory & Calculation | 320 | formula-computed, self-verifying |
| 2.1.10 Code Navigation & Documents | 126 | citation/keyword |
| 2.1.11 Protection & Life Safety | 192 | keyword + decision-table |
| 2.1.12 Special Occupancies & Renewables | 148 | keyword + computed (PV, 120% rule) |
| 2.1.13 Forensics, Service & Maintenance | 120 | NEMA decision tables + keyword |
| 2.1.14 Business & Customer Process | 94 | count/sum + keyword |

Achieved mixes: decisions 499 fail / 390 pass / 111 NMI (50/39/11%); tiers weighted toward
T2–T4 (T3 303, T4 189) to correct the current T4 skew; 312 items numerically graded via
`expected_value`; 77 items carry a `media_plan` hint for the §4.8/§4.9 image/audio
conversion pass; 58 counterfactual family groups (§4.3, `pair_id` = element + family +
tier) each contain both a fail and its corrected pass scene. All 1,000 scenario texts are
unique; every spec id is unique and deterministic.

**Pipeline path:** specs → SME review pass (§7) → `naturalize_items.py` for scenario
polish → merge into `benchmark/items/` → regenerate Harbor task dirs via the existing
`generate_tasks_v2.py` flow.

## 7. Validation checklist before promotion

1. Journeyman/SME pass on each element's variant library: defect is real & common, verdict
   is correct for the *stated* code cycle, citation is right.
2. Spot-verify 5% of computed answers by hand (independent of the generating formula).
3. Leakage audit (`leakage_audit.py`) — calc items embed their inputs, so premise/finding
   overlap needs the same ratio screen as the base catalog.
4. Counterfactual-pair audit: confirm each pass twin is genuinely compliant, not merely
   defect-free-by-omission.
5. NMI audit: every NMI item must name the *specific* missing fact (cycle, cutout sheet,
   test record), never generic occlusion.
