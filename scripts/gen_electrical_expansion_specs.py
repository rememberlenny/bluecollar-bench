#!/usr/bin/env python3
"""Generate the electrical expansion v0.2 task-spec catalog (1,000 specs).

Companion to docs/source/electrical-expansion-v0.2.md. Emits
docs/source/electrical-expansion-v0.2-task-catalog.json: task specs grounded in
a free electrician-training corpus, schema-aligned with benchmark/items so
they can flow through SME review -> naturalize_items.py -> generate_tasks_v2.py.

Two generation modes:
- calc elements (2.1.9 plus PV math): parameter-sampled items whose ground
  truth is computed by the same formula the electrician would use, graded via
  expected_value / value_tolerance.
- variant elements: hand-authored defect/pass/NMI variant libraries expanded
  across tiers and slot values; fail variants with a `family` key get pass
  twins sharing a pair_id.

Deterministic under SEED. Run: python3 scripts/gen_electrical_expansion_specs.py
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "source" / "electrical-expansion-v0.2-task-catalog.json"
SEED = 20260707
GENERATION = "expansion-v0.2-training-corpus"

TASK_TYPE_NAMES = {
    "ID": "Identification",
    "FD": "Fault diagnosis",
    "CC": "Code/spec compliance",
    "SEQ": "Procedure sequencing",
    "TS": "Tool & material selection",
    "HAZ": "Hazard spotting",
    "ME": "Measurement & estimation",
    "PA": "Progress assessment",
    "DOC": "Document interpretation",
    "TRD": "Tradeoff judgment",
}

TIER_SETTINGS = {
    "T1": "at a heavy-industrial process facility",
    "T2": "on a commercial tenant-improvement project",
    "T3": "at a single-family residence",
    "T4": "during a residential service call",
    "T5": "in a shop assembly area",
}

DEFAULT_PROMPTS = {
    "CC": "Determine whether this work should pass. Identify the defects or confirm compliance, classify the risk, and list the required corrective actions.",
    "FD": "Diagnose the most likely cause, classify the risk, and list the next diagnostic or corrective actions.",
    "ID": "Identify what is shown or described, state whether it is correct for the application, and classify the risk.",
    "SEQ": "Evaluate the work sequence. Identify any step performed out of order or any missing hold point, and list the correct next actions.",
    "TS": "Evaluate the selected equipment or material for this application. State whether it is acceptable and list corrective actions if not.",
    "HAZ": "Identify the hazards present, classify the risk, and list the immediate controls or corrective actions required.",
    "ME": "Work the calculation, report the numeric result in the `value` field, and decide whether the described condition is acceptable.",
    "PA": "Assess the progress state, report percent complete where asked, and list the remaining steps.",
    "DOC": "Interpret the referenced document against the field condition, state whether they agree, and cite the governing code section in your findings.",
    "TRD": "Judge the tradeoff. State whether the approach is acceptable, document the reasoning, and list any conditions that must be met.",
}

# --------------------------------------------------------------------------
# Reference data (values an electrician would pull from the cited tables)
# --------------------------------------------------------------------------

CM = {"14": 4110, "12": 6530, "10": 10380, "8": 16510, "6": 26240, "4": 41740,
      "3": 52620, "2": 66360, "1": 83690, "1/0": 105600, "2/0": 133100}
K_CU = 12.9

AMP_90C = {"14": 25, "12": 30, "10": 40, "8": 55, "6": 75, "4": 95, "3": 110,
           "2": 130, "1": 145, "1/0": 170, "2/0": 195, "3/0": 225, "4/0": 260}
TEMP_CORR_90 = {30: 1.00, 35: 0.96, 40: 0.91, 45: 0.87, 50: 0.82}
ADJ = {3: 1.0, 4: 0.8, 5: 0.8, 6: 0.8, 7: 0.7, 8: 0.7, 9: 0.7, 10: 0.5, 12: 0.5}

BOX_VOL = {"14": 2.00, "12": 2.25}
BOXES = [("4 in. x 1-1/2 in. octagon", 15.5), ("4 in. square x 1-1/2 in.", 21.0),
         ("4 in. square x 2-1/8 in.", 30.3), ("3 x 2 x 2-1/2 in. device", 12.5),
         ("3 x 2 x 3-1/2 in. device", 18.0)]

OFFSET_MULT = {10: 6.0, 22.5: 2.6, 30: 2.0, 45: 1.4, 60: 1.2}
SHRINK_PER_IN = {10: 0.0625, 22.5: 0.1875, 30: 0.25, 45: 0.375, 60: 0.5}
STUB_DEDUCT = {"1/2": 5.0, "3/4": 6.0, "1": 8.0}

# (phases, volts, hp) -> FLC per NEC 430.248/430.250
MOTOR_FLC = {(3, 460, 5): 7.6, (3, 460, 10): 14.0, (3, 460, 20): 27.0,
             (3, 460, 25): 34.0, (3, 460, 30): 40.0, (3, 460, 50): 65.0,
             (3, 230, 5): 15.2, (3, 230, 10): 28.0, (3, 230, 15): 42.0,
             (3, 230, 25): 68.0, (1, 230, 1): 8.0, (1, 115, 1): 16.0}
STD_OCPD = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125,
            150, 175, 200, 225, 250, 300, 350, 400]

APPLIANCES = [("electric water heater", 4500, 240), ("clothes dryer heating element bank", 5600, 240),
              ("baseboard heater", 2000, 240), ("portable space heater", 1500, 120),
              ("wall oven broil element", 3400, 240), ("swimming pool resistance heater", 11000, 240)]


def cap_ok(cnt: Counter, count: int, dec: str, share: float) -> bool:
    """Keep a generator's decision mix near the target share."""
    return cnt[dec] < math.ceil(share * count)


def next_std(amps: float) -> int:
    for s in STD_OCPD:
        if s >= amps:
            return s
    return STD_OCPD[-1]


def r1(x: float) -> float:
    return round(x, 1)


# --------------------------------------------------------------------------
# Spec assembly
# --------------------------------------------------------------------------

ALL_IDS: set[str] = set()
SEEN_SCENARIOS: set[str] = set()


def push(out: list, sp: dict) -> bool:
    """Append a spec unless its scenario text already exists in the catalog."""
    if sp["scenario"] in SEEN_SCENARIOS:
        return False
    SEEN_SCENARIOS.add(sp["scenario"])
    out.append(sp)
    return True


def make_id(element_code: str, task_type: str, tier: str, seedtext: str) -> str:
    h = hashlib.sha1(seedtext.encode()).hexdigest()[:6]
    base = f"elx-{element_code.lower().replace('-', '')}-{task_type.lower()}-{tier.lower()}-{h}"
    n, out = 0, base
    while out in ALL_IDS:
        n += 1
        out = f"{base}{n}"
    ALL_IDS.add(out)
    return out


def spec(element: dict, task_type: str, tier: str, decision: str, risk: str,
         scenario: str, findings: list, actions: list, title: str,
         s1: str = "in-progress", forbidden: list | None = None,
         prompt: str | None = None, hazard_class: str = "code-only",
         pair_id: str | None = None, expected_value: float | None = None,
         value_unit: str | None = None, value_tolerance: float | None = None,
         media_plan: str | None = None, refs: list | None = None) -> dict:
    d = {
        "id": make_id(element["code"], task_type, tier, scenario + title),
        "title": title,
        "discipline": "2.1 Electrical",
        "discipline_code": "2.1",
        "subcategory": element["subcategory"],
        "element": f"{element['code']} {element['name']}",
        "element_code": element["code"],
        "tier": tier,
        "task_type": task_type,
        "task_type_name": TASK_TYPE_NAMES[task_type],
        "modality": "text",
        "decision": decision,
        "risk": risk,
        "s1_state": s1,
        "scenario": scenario,
        "prompt": prompt or DEFAULT_PROMPTS[task_type],
        "required_findings": findings,
        "required_actions": actions,
        "forbidden": forbidden or ([["pass"]] if decision == "fail" else []),
        "source_refs": refs or element["refs"],
        "corpus_source": element["source"],
        "hazard_class": hazard_class,
        "generation": GENERATION,
    }
    if pair_id:
        d["pair_id"] = pair_id
    if expected_value is not None:
        d["expected_value"] = expected_value
        d["value_unit"] = value_unit
        d["value_tolerance"] = value_tolerance
    if media_plan:
        d["media_plan"] = media_plan
    return d


# --------------------------------------------------------------------------
# Calc generators (2.1.9). Each yields `count` specs, params sampled w/o repeat
# --------------------------------------------------------------------------

def gen_e901(el, count, rng):
    out, used, cnt = [], set(), Counter()
    while len(out) < count:
        name, watts, volts = rng.choice(APPLIANCES)
        mode = rng.choice(["pass", "pass", "fail-low", "fail-high", "nmi"])
        dec = {"pass": "pass", "nmi": "needs_more_info"}.get(mode, "fail")
        if not cap_ok(cnt, count, dec, {"pass": 0.42, "fail": 0.48, "needs_more_info": 0.10}[dec]):
            continue
        tier = rng.choice(el["tiers"])
        if mode == "pass":
            dev = 1.0
        elif mode == "fail-low":
            dev = rng.choice([0.55, 0.65])
        else:
            dev = rng.choice([1.4, 1.5])
        nmi_factor = rng.choice([0.7, 1.0, 1.3])
        key = (name, mode, tier, dev if mode != "nmi" else nmi_factor)
        if key in used:
            continue
        used.add(key)
        cnt[dec] += 1
        expect = r1(watts / volts)
        if mode == "nmi":
            sc = (f"A technician {TIER_SETTINGS[tier]} clamps a {name} circuit and reads "
                  f"{r1(expect * nmi_factor)} A at {volts} V. The nameplate is painted over and "
                  "the wattage cannot be read; no submittal or cut sheet is on hand.")
            push(out, spec(el, "ME", tier, "needs_more_info", "medium", sc,
                            [["nameplate"], ["wattage", "unknown"], ["confirm"]],
                            [["obtain", "nameplate"], ["verify", "rating"]],
                            "Ohm's-law field check: unreadable nameplate",
                            expected_value=None))
            continue
        reading = r1(expect * dev)
        sc = (f"A {name} rated {watts} W at {volts} V is checked {TIER_SETTINGS[tier]}. "
              f"A clamp meter on the ungrounded conductor reads {reading} A with the load calling at full output. "
              "Compute the expected current from the nameplate and judge the reading.")
        if mode == "pass":
            push(out, spec(el, "ME", tier, "pass", "low", sc,
                            [["expected", "current"], ["normal"]], [["document"], ["release"]],
                            "Ohm's-law field check: reading matches nameplate", forbidden=[["fail"]],
                            expected_value=expect, value_unit="A", value_tolerance=0.5,
                            media_plan="meter-readout-image"))
        else:
            direction = "low" if dev < 1 else "high"
            finding = [["reading", direction]] if direction == "high" else [["reading", "low"]]
            cause = [["element", "shorted"], ["overload"]] if direction == "high" else [["element", "open"], ["failed"]]
            push(out, spec(el, "ME", tier, "fail", "medium", sc,
                            [["expected", "current"]] + finding + [cause[0]],
                            [["de-energize"], ["inspect", "element"]],
                            f"Ohm's-law field check: current {direction}",
                            hazard_class="fire" if direction == "high" else "code-only",
                            expected_value=expect, value_unit="A", value_tolerance=0.5,
                            media_plan="meter-readout-image"))
    return out


def gen_e902(el, count, rng):
    out, used = [], set()
    rvals = [10, 15, 20, 24, 30, 40, 48, 60]
    while len(out) < count:
        r1_, r2_ = rng.choice(rvals), rng.choice(rvals)
        topo = rng.choice(["parallel", "series"])
        key = (r1_, r2_, topo)
        if key in used:
            continue
        used.add(key)
        tier = rng.choice(el["tiers"])
        req = r1((r1_ * r2_) / (r1_ + r2_)) if topo == "parallel" else float(r1_ + r2_)
        ok = rng.random() < 0.45
        measured = r1(req if ok else req * rng.choice([0.45, 1.9, 2.6]))
        sc = (f"A control cabinet {TIER_SETTINGS[tier]} contains two heating elements of {r1_} ohms and {r2_} ohms "
              f"wired in {topo}. With power locked out, an ohmmeter across the pair reads {measured} ohms. "
              "Compute the expected total resistance and judge the measurement.")
        if ok:
            push(out, spec(el, "FD", tier, "pass", "low", sc,
                            [["expected", "resistance"], ["normal"]], [["document"], ["release"]],
                            f"Circuit analysis: {topo} bank reads correct", forbidden=[["fail"]],
                            expected_value=req, value_unit="ohms", value_tolerance=max(0.5, req * 0.03),
                            prompt=DEFAULT_PROMPTS["ME"], s1="tested/inspected"))
        else:
            mode = [["element", "open"]] if measured > req else [["element", "shorted"]]
            push(out, spec(el, "FD", tier, "fail", "medium", sc,
                            [["expected", "resistance"], mode[0]],
                            [["isolate", "element"], ["measure", "individually"], ["replace"]],
                            f"Circuit analysis: {topo} bank reads wrong",
                            expected_value=req, value_unit="ohms", value_tolerance=max(0.5, req * 0.03),
                            prompt=DEFAULT_PROMPTS["ME"], s1="tested/inspected", hazard_class="fire"))
    return out


def gen_e903(el, count, rng):
    out, used, cnt = [], set(), Counter()
    while len(out) < count:
        size = rng.choice(list(CM))
        amps = rng.choice([12, 16, 20, 24, 28, 40, 50, 60])
        length = rng.choice([40, 60, 75, 90, 120, 150, 200, 250])
        volts = rng.choice([120, 240, 208])
        key = (size, amps, length, volts)
        if key in used:
            continue
        vd = 2 * K_CU * amps * length / CM[size]
        pct = vd / volts * 100
        if not (0.8 <= pct <= 9):
            continue
        nmi = rng.random() < 0.15
        dec = "needs_more_info" if nmi else ("fail" if pct > 3 else "pass")
        if not cap_ok(cnt, count, dec, {"pass": 0.42, "fail": 0.48, "needs_more_info": 0.10}[dec]):
            continue
        used.add(key)
        cnt[dec] += 1
        tier = rng.choice(el["tiers"])
        if nmi:
            sc = (f"A {volts} V branch circuit {TIER_SETTINGS[tier]} feeds a {amps} A load on {size} AWG copper. "
                  "The run length is not recorded on the plans and the routing cannot be traced from the evidence provided. "
                  "Decide whether the voltage-drop recommendation is met.")
            push(out, spec(el, "ME", tier, "needs_more_info", "medium", sc,
                            [["length", "unknown"], ["confirm"]], [["measure", "length"], ["recalculate"]],
                            "Voltage drop: run length unknown", s1="staged"))
            continue
        sc = (f"A {volts} V branch circuit {TIER_SETTINGS[tier]} feeds a steady {amps} A load through {length} ft of "
              f"{size} AWG copper (one-way). Using VD = 2 x 12.9 x I x L / CM, compute the voltage drop and judge it "
              "against the 3 percent branch-circuit recommendation.")
        if pct > 3:
            push(out, spec(el, "ME", tier, "fail", "medium", sc,
                            [["exceeds", "3"], ["voltage", "drop"]],
                            [["increase", "conductor", "size"], ["recalculate"]],
                            f"Voltage drop over limit: {size} AWG at {length} ft",
                            s1="staged", hazard_class="code-only",
                            expected_value=r1(vd), value_unit="V", value_tolerance=0.2))
        else:
            push(out, spec(el, "ME", tier, "pass", "low", sc,
                            [["within"], ["voltage", "drop"]], [["document"]],
                            f"Voltage drop within limit: {size} AWG at {length} ft",
                            s1="staged", forbidden=[["fail"]],
                            expected_value=r1(vd), value_unit="V", value_tolerance=0.2))
    return out


def gen_e904(el, count, rng):
    out, used, cnt = [], set(), Counter()
    while len(out) < count:
        size = rng.choice(list(AMP_90C)[:10])
        amb = rng.choice(list(TEMP_CORR_90))
        n = rng.choice(list(ADJ))
        load = rng.choice([16, 20, 24, 28, 35, 42, 50, 60, 80])
        key = (size, amb, n, load)
        if key in used:
            continue
        adj_amp = AMP_90C[size] * TEMP_CORR_90[amb] * ADJ[n]
        if abs(adj_amp - load) < 1.5:
            continue
        dec = "pass" if adj_amp >= load else "fail"
        if not cap_ok(cnt, count, dec, 0.5):
            continue
        used.add(key)
        cnt[dec] += 1
        tier = rng.choice(el["tiers"])
        sc = (f"A raceway {TIER_SETTINGS[tier]} carries {n} current-carrying THHN copper conductors, {size} AWG, "
              f"through an area with {amb} deg C ambient. The circuit serves a continuous-duty load metered at {load} A. "
              "Compute the adjusted ampacity from the 90 deg C column with the temperature correction and bundling "
              "adjustment factors, and judge whether the conductor is adequate.")
        if adj_amp >= load:
            push(out, spec(el, "ME", tier, "pass", "low", sc,
                            [["adjusted", "ampacity"], ["adequate"]], [["document"]],
                            f"Derated ampacity adequate: {size} AWG, {n} CCC",
                            s1="staged", forbidden=[["fail"]],
                            expected_value=r1(adj_amp), value_unit="A", value_tolerance=2))
        else:
            push(out, spec(el, "ME", tier, "fail", "high", sc,
                            [["adjusted", "ampacity"], ["exceeds"]],
                            [["increase", "conductor", "size"], ["reduce", "conductors"]],
                            f"Derated ampacity exceeded: {size} AWG, {n} CCC",
                            s1="staged", hazard_class="fire",
                            expected_value=r1(adj_amp), value_unit="A", value_tolerance=2))
    return out


def gen_e905(el, count, rng):
    out, used, cnt = [], set(), Counter()
    while len(out) < count:
        awg = rng.choice(list(BOX_VOL))
        cond = rng.choice([4, 5, 6, 7, 8, 9, 10])
        yokes = rng.choice([0, 1, 2])
        clamps = rng.choice([0, 1])
        box_name, box_vol = rng.choice(BOXES)
        key = (awg, cond, yokes, clamps, box_name)
        if key in used:
            continue
        counts = cond + 2 * yokes + clamps + 1  # +1 all EGCs
        req = round(counts * BOX_VOL[awg], 2)
        if abs(req - box_vol) < 0.3:
            continue
        dec = "pass" if req <= box_vol else "fail"
        if not cap_ok(cnt, count, dec, 0.5):
            continue
        used.add(key)
        cnt[dec] += 1
        tier = rng.choice(el["tiers"])
        dev = f"{yokes} device yoke(s)" if yokes else "no devices"
        cl = "internal cable clamps" if clamps else "connectors outside the box"
        sc = (f"A {box_name} box ({box_vol} cu in.) {TIER_SETTINGS[tier]} contains {cond} circuit conductors of "
              f"{awg} AWG, {dev}, {cl}, and equipment grounding conductors. Compute the required box volume per "
              "314.16 and judge the fill.")
        if req <= box_vol:
            push(out, spec(el, "ME", tier, "pass", "low", sc,
                            [["fill"], ["within"]], [["document"]],
                            f"Box fill OK: {cond} x {awg} AWG in {box_vol} cu in.",
                            s1="rough-complete", forbidden=[["fail"]],
                            expected_value=req, value_unit="cu in", value_tolerance=0.3,
                            refs=["NEC 314.16"]))
        else:
            push(out, spec(el, "ME", tier, "fail", "medium", sc,
                            [["fill", "exceeded"]],
                            [["larger", "box"], ["extension", "ring"]],
                            f"Box fill exceeded: {cond} x {awg} AWG in {box_vol} cu in.",
                            s1="rough-complete", hazard_class="fire",
                            expected_value=req, value_unit="cu in", value_tolerance=0.3,
                            refs=["NEC 314.16"]))
    return out


def gen_e906(el, count, rng):
    out, used = [], set()
    while len(out) < count:
        kind = rng.choice(["offset", "offset", "shrink", "stub"])
        tier = rng.choice(el["tiers"])
        if kind == "stub":
            trade = rng.choice(list(STUB_DEDUCT))
            stub = rng.choice([8, 10, 12, 14, 16, 18])
            key = (kind, trade, stub)
            if key in used:
                continue
            used.add(key)
            mark = stub - STUB_DEDUCT[trade]
            ok = rng.random() < 0.5
            marked = mark if ok else mark + rng.choice([-2, 2, STUB_DEDUCT[trade]])
            sc = (f"An apprentice {TIER_SETTINGS[tier]} needs a {stub} in. stub-up in {trade} in. EMT using a bender "
                  f"with a {STUB_DEDUCT[trade]:.0f} in. take-up deduct. The pencil mark is at {marked:.1f} in. from the "
                  "end. Compute the correct mark location and judge the layout.")
            title = f"Stub-up layout: {trade} in. EMT, {stub} in. rise"
            expect = mark
            unit, tol = "in", 0.1
        else:
            angle = rng.choice(list(OFFSET_MULT))
            rise = rng.choice([3, 4, 5, 6, 8, 10, 12])
            key = (kind, angle, rise)
            if key in used:
                continue
            used.add(key)
            if kind == "offset":
                expect = r1(rise * OFFSET_MULT[angle])
                asked = "distance between the two bend marks"
            else:
                expect = r1(rise * SHRINK_PER_IN[angle])
                asked = "shrink to add ahead of the first mark"
            ok = rng.random() < 0.5
            marked = expect if ok else r1(expect * rng.choice([0.6, 1.5]) + rng.choice([-1, 1]))
            sc = (f"An apprentice {TIER_SETTINGS[tier]} lays out a {angle} deg x {angle} deg offset for a {rise} in. "
                  f"rise in 3/4 in. EMT and has marked the {asked} as {marked} in. Using the standard multiplier and "
                  "shrink constants, compute the correct value and judge the layout.")
            title = f"Offset layout: {angle} deg, {rise} in. rise ({kind})"
            unit, tol = "in", 0.2
        if abs(marked - expect) <= tol:
            push(out, spec(el, "ME", tier, "pass", "low", sc,
                            [["layout", "correct"]], [["proceed", "bend"]],
                            title, s1="in-progress", forbidden=[["fail"]],
                            expected_value=expect, value_unit=unit, value_tolerance=tol,
                            refs=["Bamford conduit bending manual", "NEC Art. 358"]))
        else:
            push(out, spec(el, "ME", tier, "fail", "low", sc,
                            [["layout", "incorrect"]], [["remark"], ["recalculate"]],
                            title, s1="in-progress",
                            expected_value=expect, value_unit=unit, value_tolerance=tol,
                            refs=["Bamford conduit bending manual", "NEC Art. 358"]))
    return out


def gen_e907(el, count, rng):
    out, used, cnt = [], set(), Counter()
    keys = list(MOTOR_FLC)
    while len(out) < count:
        ph, v, hp = rng.choice(keys)
        flc = MOTOR_FLC[(ph, v, hp)]
        max_brk = next_std(flc * 2.5)
        mode = rng.choice(["brk-ok", "brk-over", "ol"])
        tier = rng.choice(el["tiers"])
        nameplate = r1(flc * 0.95)
        ol_expect = r1(nameplate * 1.25)
        setto = ol_expect if rng.random() < 0.5 else r1(ol_expect * rng.choice([0.7, 1.6]))
        if mode != "ol":
            dec = "pass" if mode == "brk-ok" else "fail"
            if not cap_ok(cnt, count, dec, 0.5):
                continue
        key = (ph, v, hp, mode, tier, setto if mode == "ol" else None)
        if key in used:
            continue
        used.add(key)
        if mode != "ol":
            cnt[dec] += 1
        phs = "three-phase" if ph == 3 else "single-phase"
        if mode == "ol":
            expect = ol_expect
            sc = (f"A {hp} hp {phs} {v} V motor {TIER_SETTINGS[tier]} has a nameplate FLA of {nameplate} A "
                  f"(service factor 1.15). The overload relay is dialed to {setto} A. Compute the maximum overload "
                  "setting per 430.32 and judge the dial setting.")
            ok = abs(setto - expect) <= 0.5
            if not cap_ok(cnt, count, "pass" if ok else "fail", 0.5):
                continue
            cnt["pass" if ok else "fail"] += 1
            push(out, spec(el, "ME", tier, "pass" if ok else "fail", "low" if ok else "medium", sc,
                            [["overload", "setting"]] + ([["correct"]] if ok else [["incorrect"]]),
                            [["document"]] if ok else [["reset", "overload"]],
                            f"Motor overload setting: {hp} hp at {v} V",
                            s1="tested/inspected", forbidden=[["fail"]] if ok else [["pass"]],
                            hazard_class="fire" if not ok else "code-only",
                            expected_value=expect, value_unit="A", value_tolerance=0.5,
                            refs=["NEC 430.32", "NEC Table 430.250"]))
            continue
        installed = max_brk if mode == "brk-ok" else next_std(max_brk + 5)
        sc = (f"A {hp} hp {phs} {v} V squirrel-cage motor {TIER_SETTINGS[tier]} is protected by a {installed} A "
              f"inverse-time breaker. Using the table FLC of {flc} A and the 250 percent rule of 430.52 with the "
              "next-standard-size allowance, compute the maximum permitted breaker and judge the installation.")
        if mode == "brk-ok":
            push(out, spec(el, "TS", tier, "pass", "low", sc,
                            [["maximum", "breaker"], ["permitted"]], [["document"]],
                            f"Motor branch OCPD: {hp} hp at {v} V, compliant",
                            s1="tested/inspected", forbidden=[["fail"]],
                            prompt=DEFAULT_PROMPTS["ME"],
                            expected_value=float(max_brk), value_unit="A", value_tolerance=0,
                            refs=["NEC 430.52", "NEC 240.6", "NEC Table 430.250"]))
        else:
            push(out, spec(el, "TS", tier, "fail", "medium", sc,
                            [["exceeds", "maximum"]], [["replace", "breaker"]],
                            f"Motor branch OCPD: {hp} hp at {v} V, oversized",
                            s1="tested/inspected", hazard_class="fire",
                            prompt=DEFAULT_PROMPTS["ME"],
                            expected_value=float(max_brk), value_unit="A", value_tolerance=0,
                            refs=["NEC 430.52", "NEC 240.6", "NEC Table 430.250"]))
    return out


def gen_e908(el, count, rng):
    out, used = [], set()
    while len(out) < count:
        kva = rng.choice([15, 30, 45, 75, 112.5, 150])
        ph = rng.choice([1, 3])
        v = 480 if ph == 3 else 240
        fla = kva * 1000 / (1.732 * v) if ph == 3 else kva * 1000 / v
        maxp = next_std(fla * 1.25)
        installed = maxp if rng.random() < 0.5 else next_std(maxp + 5)
        tier = rng.choice(el["tiers"])
        key = (kva, ph, installed, tier)
        if key in used:
            continue
        used.add(key)
        phs = "three-phase 480 V" if ph == 3 else "single-phase 240 V"
        sc = (f"A {kva} kVA {phs} dry-type transformer {TIER_SETTINGS[tier]} has primary-only protection from a "
              f"{installed} A breaker. Compute the primary full-load current and the maximum primary OCPD at 125 "
              "percent with the next-standard-size allowance, and judge the protection.")
        ok = installed <= maxp
        push(out, spec(el, "ME", tier, "pass" if ok else "fail", "low" if ok else "high", sc,
                        [["full-load", "current"]] + ([["permitted"]] if ok else [["exceeds"]]),
                        [["document"]] if ok else [["replace", "breaker"]],
                        f"Transformer primary OCPD: {kva} kVA {phs}",
                        s1="tested/inspected", forbidden=[["fail"]] if ok else [["pass"]],
                        hazard_class="fire" if not ok else "code-only",
                        expected_value=r1(fla), value_unit="A", value_tolerance=0.5,
                        refs=["NEC 450.3(B)", "NEC 240.6"]))
    return out


def gen_e909(el, count, rng):
    out, used, cnt = [], set(), Counter()
    while len(out) < count:
        sqft = rng.choice([1100, 1400, 1600, 1900, 2200, 2600, 3000, 3400])
        has_ac = rng.random() < 0.7
        has_dryer = rng.random() < 0.7
        has_strip = rng.random() < 0.4
        if has_strip:
            has_ac = False  # strip heat displaces the AC load in the scenario
        service = rng.choice([100, 100, 125, 125, 150, 200])
        key = (sqft, has_ac, has_dryer, has_strip, service)
        if key in used:
            continue
        general = sqft * 3 + 3000 + 1500
        demand = 3000 + (general - 3000) * 0.35
        total = (demand + 8000 + (5000 if has_dryer else 0) + 4500
                 + (9600 if has_strip else (4200 if has_ac else 0)))
        amps = total / 240
        dec = "pass" if amps <= service else "fail"
        if not cap_ok(cnt, count, dec, 0.5):
            continue
        used.add(key)
        cnt[dec] += 1
        tier = "T3"
        parts = ["an electric range (8 kW demand per Table 220.55)", "a 4.5 kW water heater"]
        if has_dryer:
            parts.append("a 5 kW dryer")
        if has_strip:
            parts.append("9.6 kW of electric strip heat (larger than the AC load)")
        elif has_ac:
            parts.append("a 4.2 kW air conditioner")
        sc = (f"A {sqft} sq ft dwelling with two small-appliance circuits and a laundry circuit includes "
              f"{', '.join(parts)}. Using the standard method of Article 220 (3 VA per sq ft, first 3 kVA at 100 "
              f"percent, remainder at 35 percent), compute the service load in amperes at 240 V and judge whether "
              f"the existing {service} A service is adequate.")
        ok = amps <= service
        push(out, spec(el, "ME", tier, "pass" if ok else "fail", "low" if ok else "medium", sc,
                        [["calculated", "load"]] + ([["adequate"]] if ok else [["exceeds", "service"]]),
                        [["document"]] if ok else [["service", "upgrade"]],
                        f"Dwelling load calc: {sqft} sq ft on {service} A",
                        s1="staged", forbidden=[["fail"]] if ok else [["pass"]],
                        hazard_class="fire" if not ok else "code-only",
                        expected_value=r1(amps), value_unit="A", value_tolerance=2,
                        refs=["NEC Art. 220", "NEC Table 220.55"]))
    return out


def gen_e910(el, count, rng):
    out, used, cnt = [], set(), Counter()
    while len(out) < count:
        kw = rng.choice([40, 60, 75, 90, 120, 150])
        pf = rng.choice([0.72, 0.78, 0.83, 0.87, 0.91, 0.93, 0.95, 0.97])
        key = (kw, pf)
        if key in used:
            continue
        dec = "pass" if round(kw / r1(kw / pf) * 100, 1) >= 90 else "fail"
        if not cap_ok(cnt, count, dec, 0.5):
            continue
        used.add(key)
        cnt[dec] += 1
        kva = r1(kw / pf)
        tier = rng.choice(el["tiers"])
        sc = (f"A facility meter {TIER_SETTINGS[tier]} logs a steady {kw} kW real power draw while the demand "
              f"register shows {kva} kVA apparent power. The utility tariff assesses penalties below 0.90 power "
              "factor. Compute the power factor as a percentage and judge the billing exposure.")
        pfpct = round(kw / kva * 100, 1)
        ok = pfpct >= 90
        push(out, spec(el, "ME", tier, "pass" if ok else "fail", "low", sc,
                        [["power", "factor"]] + ([["above", "0.90"]] if ok else [["below", "0.90"]]),
                        [["document"]] if ok else [["capacitor", "bank"], ["correction"]],
                        f"Power factor check: {kw} kW at {pf} PF",
                        s1="accepted/in-service", forbidden=[["fail"]] if ok else [["pass"]],
                        expected_value=pfpct, value_unit="percent", value_tolerance=1,
                        refs=["Power-factor formulas (training-corpus equations chart)"]))
    return out


# --------------------------------------------------------------------------
# Variant libraries for 2.1.10 - 2.1.14
# Variant keys: tt, dec, risk, s1, hz, t (title), p (premise, {setting}/{slot}),
# slots, find, act, forb, family (pair twin key), prompt, media
# --------------------------------------------------------------------------

def V(tt, dec, risk, t, p, find, act, s1="in-progress", hz="code-only",
      slots=None, forb=None, family=None, prompt=None, media=None, refs=None):
    return {"tt": tt, "dec": dec, "risk": risk, "t": t, "p": p, "find": find,
            "act": act, "s1": s1, "hz": hz, "slots": slots or {},
            "forb": forb, "family": family, "prompt": prompt, "media": media,
            "refs": refs}


VARIANTS: dict[str, list] = {}

VARIANTS["E-1001"] = [
    V("DOC", "fail", "medium", "Wrong article cited for {slot}",
      "A permit submittal {setting} justifies the wiring method for {slot} by citing {wrong}. Review whether the citation actually governs this work and identify the correct article.",
      [["incorrect", "citation"], ["correct"]], [["revise", "submittal"], ["cite"]],
      slots={"slot": ["a swimming pool underwater luminaire", "a dock power pedestal", "a standby generator feeder",
                      "a fire alarm initiating circuit", "an antenna mast ground"],
             "wrong": ["Article 210", "Article 408", "Article 300"]},
      family="cite"),
    V("DOC", "pass", "low", "Correct article cited for {slot}",
      "A permit submittal {setting} cites {right} as the governing article for {slot}. Review whether the citation is correct for this work.",
      [["citation", "correct"]], [["approve"], ["document"]], forb=[["fail"]],
      slots={"slot": ["a swimming pool underwater luminaire", "a dock power pedestal", "a standby generator feeder"],
             "right": ["Article 680", "Article 555", "Article 702"]},
      family="cite"),
    V("CC", "fail", "medium", "Rule applied outside its scope",
      "An installer {setting} applied the {slot} requirement to equipment that the article's scope statement excludes, and flagged compliant work as a violation on the punch list. Judge the punch item.",
      [["scope"], ["does", "not", "apply"]], [["remove", "punch", "item"], ["cite", "scope"]],
      slots={"slot": ["Article 680 pool bonding", "Article 555 marina GFPE", "Article 760 fire alarm cable"]}),
    V("DOC", "needs_more_info", "medium", "Adopted code edition not stated",
      "A plan reviewer {setting} must confirm whether {slot} is required, but the project documents never state which NEC edition the jurisdiction has adopted and the rule changed between editions. Decide.",
      [["edition", "unknown"], ["confirm"]], [["verify", "adopted", "edition"]],
      slots={"slot": ["an emergency disconnect at the service", "GFCI protection for the 250 V dryer receptacle",
                      "surge protection at the dwelling service"]}),
    V("DOC", "pass", "low", "Index-driven lookup verified",
      "A foreman {setting} used the NEC index to trace {slot} to its governing section and posted the section number on the task plan. The section cited matches the subject. Judge the lookup.",
      [["section", "correct"]], [["document"]], forb=[["fail"]],
      slots={"slot": ["working-clearance depth at a panelboard", "receptacle spacing in a dwelling",
                      "conductor identification colors"]}),
]

VARIANTS["E-1002"] = [
    V("CC", "fail", "high", "New-cycle rule missed: {slot}",
      "A contractor {setting} completed work in a jurisdiction that has adopted the 2023 NEC, but built to habit from an older cycle: {slot} was omitted. Judge the installation for the adopted cycle.",
      [["required", "2023"], ["omitted"]], [["install"], ["correct"]],
      hz="shock", family="cycle",
      slots={"slot": ["GFCI protection for the 250 V dryer receptacle", "an outdoor emergency disconnect at the service",
                      "a surge-protective device at the service equipment", "GFCI protection for the basement receptacles"]}),
    V("CC", "pass", "low", "Old-cycle rule correctly not enforced",
      "An inspector {setting} works in a jurisdiction still enforcing the 2017 NEC. The installation omits {slot}, which later cycles require but the 2017 edition does not. Judge for the adopted cycle.",
      [["not", "required", "2017"]], [["document", "edition"]], forb=[["fail"]],
      family="cycle",
      slots={"slot": ["GFCI protection for the 250 V dryer receptacle", "an outdoor emergency disconnect at the service",
                      "a surge-protective device at the service"]}),
    V("TRD", "fail", "medium", "Bid priced to the wrong cycle",
      "An estimator {setting} priced a project from a checklist written for the {slot} NEC, but the jurisdiction adopted the newer cycle last year; the bid excludes the newer protection requirements. Judge the bid basis.",
      [["wrong", "edition"], ["underpriced"]], [["reprice"], ["verify", "adopted", "edition"]],
      s1="staged", slots={"slot": ["2014", "2017"]}),
    V("DOC", "needs_more_info", "medium", "Amendment status unknown",
      "A service electrician {setting} finds work that violates the model NEC but may be allowed by a local amendment the customer mentions; the amendment text is not available on site. Decide.",
      [["amendment", "unverified"], ["confirm"]], [["obtain", "amendment"], ["verify", "jurisdiction"]]),
]

VARIANTS["E-1003"] = [
    V("CC", "fail", "high", "Field modification voids listing: {slot}",
      "A crew {setting} field-modified listed equipment: {slot}. No field-evaluation body was involved. Judge the modification against the listing requirements.",
      [["listing", "violated"], ["field", "evaluation"]], [["restore"], ["field", "evaluation"]],
      hz="fire", family="listing",
      slots={"slot": ["drilled extra knockouts through a panelboard's wiring gutter and bent the bus support",
                      "installed a breaker brand not on the panelboard's listing label",
                      "replaced a luminaire lens with unrated acrylic sheet",
                      "bypassed a thermal cutout in a listed heater to stop nuisance tripping"]}),
    V("CC", "pass", "low", "Listed accessory used per instructions",
      "A crew {setting} installed {slot} identified in the equipment's listing documentation, following the manufacturer's instructions. Judge the modification.",
      [["listed"], ["instructions"]], [["document"]], forb=[["fail"]], family="listing",
      slots={"slot": ["a classified replacement breaker documented for use in that panelboard",
                      "a manufacturer hub kit in the panel's designated opening",
                      "a listed retrofit LED kit matched to the luminaire"]}),
    V("TS", "fail", "medium", "Recognized component misused as listed equipment",
      "A purchaser {setting} sourced {slot} carrying only a UL Recognized Component mark and installed it as stand-alone field equipment. Judge the selection using the White Book category rules.",
      [["recognized", "component"], ["not", "listed"]], [["replace", "listed"]],
      slots={"slot": ["a bare relay module", "an open-frame power supply", "an unenclosed terminal block assembly"]}),
    V("ID", "needs_more_info", "medium", "Label unreadable, listing unverified",
      "An inspector {setting} finds equipment whose listing label is painted over; the manufacturer and file number cannot be read, and no documentation is on site. Decide whether the equipment is acceptable.",
      [["label", "unreadable"], ["confirm"]], [["obtain", "documentation"], ["verify", "listing"]]),
]

VARIANTS["E-1004"] = [
    V("DOC", "fail", "medium", "Panel schedule does not match field",
      "The panel schedule {setting} lists circuit {slot} as spare, but the field wire is landed, energized, and feeds a load. Two other circuits are labeled for rooms that were re-partitioned. Judge the documentation.",
      [["schedule", "mismatch"], ["energized", "spare"]], [["update", "schedule"], ["trace", "circuits"]],
      s1="accepted/in-service", family="sched",
      slots={"slot": ["14", "22", "31"]}),
    V("DOC", "pass", "low", "As-built schedule verified",
      "A closeout review {setting} samples {slot} circuits from the panel schedule against field tracing; each breaker, wire size, and served load matches the schedule and the one-line. Judge the documentation.",
      [["matches"], ["verified"]], [["approve", "closeout"]], forb=[["fail"]],
      s1="accepted/in-service", family="sched",
      slots={"slot": ["five", "eight", "ten"]}),
    V("ME", "fail", "medium", "Connected load exceeds feeder on one-line",
      "The one-line {setting} shows a {slot} A feeder breaker, but the panel schedule totals a connected continuous load above the breaker's continuous rating. Total the schedule and judge the feeder.",
      [["exceeds"], ["continuous"]], [["rebalance"], ["increase", "feeder"]],
      hz="fire", slots={"slot": ["100", "150", "225"]}),
    V("ID", "needs_more_info", "medium", "Revision conflict between sheets",
      "Two drawing sheets {setting} disagree on a piece of equipment's rating, and the revision blocks show the same revision letter with different dates. No RFI response is attached. Decide which governs.",
      [["revision", "conflict"], ["confirm"]], [["issue", "rfi"], ["verify", "revision"]], s1="staged"),
]

VARIANTS["E-1005"] = [
    V("SEQ", "fail", "high", "Cover-up before rough inspection",
      "A GC {setting} directed the drywall crew to hang board in {slot} before the electrical rough inspection was performed; the wiring is now concealed. Judge the sequence.",
      [["concealed"], ["before", "inspection"]], [["stop"], ["expose"], ["schedule", "inspection"]],
      family="gate", slots={"slot": ["two bedrooms", "the corridor", "the entire second floor"]}),
    V("SEQ", "pass", "low", "Hold point honored",
      "A crew {setting} finished rough-in in {slot} and stopped, leaving the wiring exposed while insulation and drywall wait for the passed rough-inspection card. Other trades continue in released areas. Judge the sequence.",
      [["hold", "point"], ["inspection"]], [["document"], ["proceed", "released"]],
      forb=[["fail"]], family="gate",
      slots={"slot": ["the bedroom wing", "the tenant suite", "the second floor"]}),
    V("TRD", "fail", "high", "Work started beyond permit scope",
      "A remodel permit {setting} covers a kitchen circuit extension, but the crew also {slot} without an amended permit. Judge the scope decision.",
      [["beyond", "permit", "scope"]], [["amend", "permit"], ["stop", "unpermitted"]],
      slots={"slot": ["replaced the service panel", "added a hot-tub circuit", "rewired the detached garage"]}),
    V("SEQ", "needs_more_info", "medium", "Inspection status unrecorded",
      "A follow-on crew {setting} arrives to insulate, but the inspection card is missing from the site board and the permit portal is down; nobody on site can confirm the rough inspection passed. Decide.",
      [["inspection", "unverified"], ["confirm"]], [["verify", "inspection"], ["hold", "work"]]),
    V("DOC", "pass", "low", "Re-inspection after correction properly documented",
      "After a red tag {setting} for a missing nail plate, the crew corrected the work, photographed it, and the re-inspection record shows the correction accepted. Judge the closeout.",
      [["corrected"], ["re-inspection"]], [["close", "punch"]], forb=[["fail"]], s1="tested/inspected"),
]

VARIANTS["E-1101"] = [
    V("CC", "fail", "critical", "Missing GFCI: {slot}",
      "During a dwelling final {setting}, the receptacle {slot} has no GFCI protection at the device or upstream. Judge per 210.8(A).",
      [["gfci", "required"], ["missing"]], [["install", "gfci"]],
      hz="shock", family="gfciA", s1="tested/inspected",
      slots={"slot": ["within 3 ft of the powder-room lavatory", "serving the kitchen countertop",
                      "in the unfinished basement", "at the exterior patio", "in the garage behind the workbench",
                      "beneath the crawl-space access", "within 6 ft of the laundry sink"]}),
    V("CC", "pass", "low", "GFCI not required: {slot}",
      "During a dwelling final {setting}, a standard receptacle {slot} has no GFCI protection. Judge per the 210.8(A) location list.",
      [["not", "required"]], [["document"]], forb=[["fail"]], family="gfciA", s1="tested/inspected",
      slots={"slot": ["in the living room 15 ft from any sink", "in a second-floor hallway",
                      "in a bedroom", "in the dining room"]}),
    V("ID", "fail", "high", "GFCI protecting wrong locations",
      "A homeowner {setting} reports the bathroom receptacle is dead. Investigation shows a single GFCI device in the {slot} feeds through to the bathroom, and the device has tripped from a garage load. Judge the arrangement and restore power safely.",
      [["feed", "through"], ["tripped"]], [["reset"], ["label"], ["dedicated", "gfci"]],
      hz="shock", s1="accepted/in-service",
      slots={"slot": ["garage", "exterior", "basement"]}),
    V("CC", "needs_more_info", "medium", "Protection point not visible",
      "A receptacle {setting} at a kitchen countertop is a standard duplex with no test button. Whether a GFCI breaker or an upstream GFCI device protects it cannot be determined from the evidence provided. Decide.",
      [["upstream", "unverified"], ["confirm"]], [["test"], ["trace", "circuit"]], s1="tested/inspected",
      media="tester-readout-image"),
]

VARIANTS["E-1102"] = [
    V("CC", "fail", "critical", "Non-dwelling GFCI missing: {slot}",
      "On a commercial final {setting}, receptacles {slot} lack GFCI protection required by 210.8(B). Judge the installation.",
      [["gfci", "required"], ["missing"]], [["install", "gfci"]],
      hz="shock", family="gfciB", s1="tested/inspected",
      slots={"slot": ["on the rooftop serving HVAC service", "in the commercial kitchen prep line",
                      "within 6 ft of the mop-sink", "at the loading-dock exterior wall",
                      "in the indoor damp-rated wash-down bay"]}),
    V("CC", "pass", "low", "Non-dwelling GFCI not required: {slot}",
      "On a commercial final {setting}, a receptacle {slot} has no GFCI protection. Judge per the 210.8(B) list.",
      [["not", "required"]], [["document"]], forb=[["fail"]], family="gfciB", s1="tested/inspected",
      slots={"slot": ["in a dry open-plan office area", "in a carpeted conference room",
                      "in a dry storage room with no sink within 6 ft"]}),
    V("TRD", "fail", "high", "GFCI removed to stop nuisance trips",
      "A maintenance tech {setting} replaced a repeatedly tripping GFCI breaker on the {slot} circuit with a standard breaker so the equipment stays on. The trips were never diagnosed. Judge the decision.",
      [["protection", "removed"], ["undiagnosed"]], [["restore", "gfci"], ["diagnose", "leakage"]],
      hz="shock", s1="accepted/in-service",
      slots={"slot": ["kitchen ice machine", "rooftop receptacle", "car-wash bay"]}),
    V("CC", "needs_more_info", "medium", "Sink distance not determinable",
      "A receptacle {setting} may be within 6 ft of a sink, which would require GFCI protection, but the photo set gives no scale reference and the distance is not recorded. Decide.",
      [["distance", "unverified"], ["confirm"]], [["measure", "distance"]], s1="tested/inspected"),
]

VARIANTS["E-1103"] = [
    V("CC", "fail", "high", "AFCI omitted on {slot}",
      "A remodel final {setting} shows new branch circuits serving {slot} on standard breakers with no AFCI protection, in a jurisdiction enforcing the 2023 NEC without amendment. Judge per 210.12.",
      [["afci", "required"], ["missing"]], [["install", "afci"]],
      hz="fire", family="afci", s1="tested/inspected",
      slots={"slot": ["the bedrooms", "the family room and hallway", "the finished basement living space"]}),
    V("CC", "pass", "low", "AFCI retrofit path used correctly",
      "A service electrician {setting} extended a bedroom circuit and provided a listed outlet branch-circuit AFCI at the first outlet of the extension, one of the permitted 210.12 retrofit methods. Judge the work.",
      [["permitted", "method"]], [["document"]], forb=[["fail"]], family="afci", s1="tested/inspected"),
    V("FD", "fail", "medium", "AFCI nuisance trips from shared neutral",
      "After a panel upgrade {setting}, two new single-pole AFCI breakers trip within minutes of loading. Investigation notes the two circuits share a neutral as a multiwire branch circuit. Diagnose.",
      [["shared", "neutral"], ["multiwire"]], [["two-pole", "afci"], ["separate", "neutrals"]],
      s1="tested/inspected"),
    V("TRD", "fail", "high", "AFCI defeated for a freezer",
      "A homeowner {setting} asked that the garage freezer circuit's tripping AFCI/GFCI breaker be swapped for a standard breaker to protect the food; the tech complied and closed the ticket without diagnosis. Judge.",
      [["protection", "removed"], ["undiagnosed"]], [["restore"], ["diagnose"]],
      hz="fire", s1="accepted/in-service"),
    V("FD", "needs_more_info", "medium", "Trip cause not yet isolatable",
      "An AFCI {setting} trips intermittently, roughly weekly. No load list, no event capture, and no megger reading are available, and the trips cannot be reproduced during the visit. Decide the disposition.",
      [["intermittent"], ["insufficient", "data"]], [["log", "loads"], ["megger"], ["schedule", "retest"]],
      s1="accepted/in-service"),
]

VARIANTS["E-1104"] = [
    V("FD", "fail", "critical", "GFCI dead after test-button check: {slot}",
      "Following the CPSC field-study protocol {setting}, a GFCI receptacle {slot} does not trip when the test button is pressed, and a plug-in tester confirms power stays on through a simulated fault. Judge the device.",
      [["fails", "test"], ["end", "of", "life"]], [["replace", "gfci"]],
      hz="shock", s1="tested/inspected", media="tester-readout-image",
      slots={"slot": ["installed outdoors for over a decade", "in a coastal garage", "on a well-pump circuit"]}),
    V("SEQ", "fail", "medium", "Line/load reversed on GFCI",
      "A replacement GFCI {setting} was wired with the incoming feed on the LOAD terminals. The face indicator shows the miswire pattern and downstream receptacles have no protection. Judge the wiring.",
      [["line", "load", "reversed"]], [["rewire"], ["retest"]],
      hz="shock", s1="tested/inspected", family="gfciwire", media="tester-readout-image"),
    V("SEQ", "pass", "low", "GFCI replacement verified end to end",
      "A tech {setting} replaced a GFCI, landed the feed on LINE, restored power, pressed TEST to confirm the trip, verified downstream receptacles went dead, then RESET and confirmed protection with a plug-in tester. Judge the procedure.",
      [["tested"], ["downstream", "verified"]], [["document"]], forb=[["fail"]],
      s1="tested/inspected", family="gfciwire", media="tester-readout-image"),
    V("HAZ", "fail", "high", "Monthly test skipped fleet-wide",
      "A property walk {setting} finds no GFCI in the building has been test-button checked since installation; the NEMA field data on silent end-of-life failures applies directly. Two units fail when tested. Judge the maintenance state.",
      [["untested"], ["failed"]], [["replace", "failed"], ["establish", "test", "schedule"]],
      hz="shock", s1="accepted/in-service"),
    V("FD", "needs_more_info", "medium", "No tester available to classify failure",
      "A receptacle {setting} is dead and a GFCI upstream will not reset, but the tech has no plug-in tester or meter on hand to distinguish a failed device from a persistent ground fault. Decide the disposition.",
      [["cannot", "distinguish"], ["confirm"]], [["obtain", "tester"], ["measure", "leakage"]],
      s1="accepted/in-service"),
]

VARIANTS["E-1105"] = [
    V("CC", "fail", "high", "Fire alarm circuit integrity defeated: {slot}",
      "On a fire alarm rough review {setting}, the initiating-device circuit shows {slot}, defeating the supervision that Article 760 and NFPA 72 require. Judge the circuit.",
      [["supervision", "defeated"]], [["rewire"], ["end-of-line", "correct"]],
      hz="fire", family="fa", s1="rough-complete",
      slots={"slot": ["a T-tap splice mid-run on a Class B loop", "the end-of-line resistor installed inside the panel",
                      "two device branches paralleled at a junction box"]}),
    V("CC", "pass", "low", "Class B loop correctly supervised",
      "On a fire alarm rough review {setting}, a Class B initiating loop serving {slot} devices runs device to device with no branches, the end-of-line resistor is at the final device, and the panel shows normal supervisory current. Judge the circuit.",
      [["supervised"], ["end-of-line"]], [["document"]], forb=[["fail"]], family="fa", s1="tested/inspected",
      slots={"slot": ["twelve", "eighteen", "twenty-four"]}),
    V("FD", "fail", "medium", "Trouble signal traced to circuit fault",
      "A fire alarm panel {setting} shows a trouble condition on one zone. Loop resistance measures open at a device that was {slot}. Diagnose and disposition.",
      [["open", "circuit"]], [["repair"], ["retest", "zone"]],
      s1="accepted/in-service",
      slots={"slot": ["removed during painting and never reconnected", "damaged by a ceiling trade", "left unterminated at a swap"]}),
    V("DOC", "fail", "medium", "Wrong cable type in air plenum",
      "Submittal review {setting} shows FPL-rated fire alarm cable routed through a ceiling space used for environmental air, where plenum-rated FPLP is required. Judge the submittal.",
      [["plenum"], ["fplp"]], [["substitute", "plenum", "rated"]],
      hz="fire", s1="staged"),
    V("CC", "needs_more_info", "medium", "Secondary power capacity unverified",
      "A fire alarm closeout {setting} lacks the battery calculation sheet; standby and alarm loads cannot be checked against the installed battery capacity. Decide.",
      [["battery", "calculation", "missing"], ["confirm"]], [["obtain", "calculation"], ["load", "test"]],
      s1="tested/inspected"),
]

VARIANTS["E-1106"] = [
    V("HAZ", "fail", "critical", "Backfeed without transfer equipment",
      "A service call {setting} finds a portable generator connected through {slot}, with no transfer switch or interlock. Utility linework is exposed to backfeed. Judge the installation.",
      [["backfeed"], ["no", "transfer"]], [["disconnect"], ["install", "transfer"]],
      hz="shock", family="gen", s1="accepted/in-service",
      slots={"slot": ["a double-male cord into a dryer receptacle", "a breaker back-fed with no interlock kit",
                      "a homemade cord into the range receptacle"]}),
    V("CC", "pass", "low", "Interlocked backfeed breaker done right",
      "A standby hookup for {slot} generator {setting} uses a listed mechanical interlock kit for the panel, a back-fed breaker retained by the manufacturer's clip, an inlet box with the correct cord, and a generator bonded per its manual. Judge per Articles 702 and 445.",
      [["interlock", "listed"], ["retained"]], [["document"], ["label"]],
      forb=[["fail"]], family="gen", s1="tested/inspected",
      slots={"slot": ["a 7.5 kW portable", "a 9 kW portable", "a 12 kW portable"]}),
    V("SEQ", "fail", "high", "Transfer test skipped at commissioning",
      "A standby generator project {setting} was closed out without {slot}; the owner's first real outage will be the first test. Judge the commissioning sequence.",
      [["test", "skipped"]], [["schedule", "test"], ["verify", "transfer"]],
      s1="tested/inspected",
      slots={"slot": ["a load-transfer test under building load", "verification of the neutral switching configuration",
                      "a full-load run of rated duration"]}),
    V("ID", "fail", "high", "Neutral bonding mismatch at generator",
      "A floating-neutral portable generator {setting} feeds a transfer switch that does not switch the neutral, but the generator's bonding jumper was also left in place, creating parallel neutral paths and tripping the inlet GFCI. Judge the configuration.",
      [["neutral", "bond"], ["parallel", "path"]], [["remove", "jumper"], ["match", "transfer", "type"]],
      hz="shock", s1="tested/inspected"),
    V("CC", "needs_more_info", "medium", "Load class of standby system unstated",
      "A generator feeds selected circuits {setting}, but the documents never state whether the system is optional standby or legally required; the wiring separation rules differ. Decide.",
      [["classification", "unknown"], ["confirm"]], [["verify", "classification"]], s1="staged"),
]

VARIANTS["E-1107"] = [
    V("TRD", "fail", "high", "Optional loads on the emergency system",
      "A design review {setting} finds {slot} connected to the Article 700 emergency system alongside egress lighting. Judge the load assignment.",
      [["emergency", "system"], ["not", "permitted"]], [["move", "loads"], ["separate", "transfer"]],
      hz="fire", family="standby",
      slots={"slot": ["the lobby decorative lighting", "the tenant server room", "the parking-lot sign"]}),
    V("CC", "pass", "low", "Load classes correctly separated",
      "A design review for {slot} {setting} shows egress lighting on the emergency transfer switch, the fire pump on its own service arrangement, and owner convenience loads on an optional-standby switch, each with the required wiring separation. Judge.",
      [["separated"], ["classification"]], [["document"]], forb=[["fail"]], family="standby",
      slots={"slot": ["a hospital wing", "a high-rise office", "a convention hall"]}),
    V("DOC", "fail", "medium", "Emergency circuits mixed in common raceway",
      "As-builts {setting} show Article 700 emergency circuits sharing a raceway with normal branch circuits for a stretch of corridor. Judge per the separation requirement.",
      [["separation"], ["same", "raceway"]], [["reroute"]], s1="rough-complete"),
    V("TRD", "needs_more_info", "medium", "Occupancy trigger for Article 700 unclear",
      "A tenant fit-out {setting} may or may not make the assembly occupancy large enough to trigger legally required emergency power; the occupant-load calculation is not in the package. Decide.",
      [["occupant", "load", "unknown"], ["confirm"]], [["obtain", "occupant", "load"]], s1="staged"),
]

VARIANTS["E-1201"] = [
    V("CC", "fail", "critical", "Pool clearance violation: {slot}",
      "A pool final {setting} finds {slot}. Judge against the Article 680 clearance and location rules.",
      [["clearance"], ["violation"]], [["relocate"], ["correct"]],
      hz="shock", family="pool", s1="tested/inspected",
      slots={"slot": ["a receptacle 4 ft from the inside pool wall", "a ceiling fan directly over the water",
                      "a cord-connected pump with a 12 ft cord", "an existing overhead service drop crossing the pool"]}),
    V("CC", "pass", "low", "Pool receptacle placement correct",
      "A pool final {setting} shows the required convenience receptacle {slot} from the inside pool wall, GFCI-protected and weather-resistant with an in-use cover, and the pump receptacle within its permitted band with GFCI. Judge.",
      [["within", "permitted"], ["gfci"]], [["document"]], forb=[["fail"]], family="pool", s1="tested/inspected",
      slots={"slot": ["8 ft", "12 ft", "18 ft"]}),
    V("ME", "fail", "high", "Luminaire too shallow / wrong rating",
      "An underwater luminaire {setting} is installed with the top of its lens {slot} below the normal water level, and the fixture documentation does not show a listing for that depth class. Judge.",
      [["depth"], ["listing"]], [["verify", "listing"], ["reinstall"]],
      hz="shock", s1="tested/inspected", slots={"slot": ["8 in.", "12 in."]}),
    V("HAZ", "needs_more_info", "medium", "Buried bonding grid not observable",
      "A deck was poured {setting} before any photo or inspection record of the perimeter equipotential bonding was made; the grid cannot be observed now. Decide the disposition of the bonding question.",
      [["bonding", "unverified"], ["confirm"]], [["records"], ["continuity", "test"]],
      s1="tested/inspected", hz="shock"),
]

VARIANTS["E-1202"] = [
    V("CC", "fail", "high", "Spa disconnect missing or misplaced",
      "A packaged hot tub install {setting} has {slot}. Judge against the 680 maintenance-disconnect and GFCI rules.",
      [["disconnect"], ["gfci"]], [["install", "disconnect"], ["gfci"]],
      hz="shock", family="spa", s1="tested/inspected",
      slots={"slot": ["no maintenance disconnect within sight of the tub", "the disconnect mounted behind the tub skirt within reach of the water",
                      "a non-GFCI 50 A feed from the panel"]}),
    V("CC", "pass", "low", "Spa package installed per instructions",
      "A packaged hot tub install on {slot} feeder {setting} shows GFCI protection, a maintenance disconnect within sight and beyond the required reach distance, bonding per the manual, and the manufacturer's wiring diagram followed. Judge.",
      [["per", "instructions"], ["gfci"]], [["document"]], forb=[["fail"]], family="spa", s1="tested/inspected",
      slots={"slot": ["a 40 A", "a 50 A", "a 60 A"]}),
    V("SEQ", "fail", "medium", "Energized before bonding verified",
      "A spa {setting} was filled and energized for the customer the same day, before the bonding connections behind the skirt were inspected; the punch list still shows the bonding check open. Judge the sequence.",
      [["energized", "before"], ["bonding"]], [["de-energize"], ["verify", "bonding"]],
      hz="shock", s1="tested/inspected"),
    V("CC", "needs_more_info", "medium", "Interior spa rules depend on missing facts",
      "An indoor spa {setting} may need different receptacle and luminaire treatment than the outdoor default, but ceiling height and fixture ratings are not recorded. Decide.",
      [["unverified"], ["confirm"]], [["measure"], ["obtain", "ratings"]], s1="staged"),
]

VARIANTS["E-1203"] = [
    V("HAZ", "fail", "critical", "ESD risk: leakage at the dock",
      "A marina walkdown {setting} finds {slot}. Fresh-water swimming areas adjoin the slips. Judge against Article 555 and the electric-shock-drowning guidance.",
      [["leakage"], ["shock", "drowning"]], [["de-energize"], ["repair"], ["signage"]],
      hz="shock", family="marina", s1="accepted/in-service",
      slots={"slot": ["a pedestal GFPE device jumpered out after nuisance trips", "an older dock feeder with no ground-fault protection",
                      "shore-power cords with cracked jackets draped into the water"]}),
    V("CC", "pass", "low", "Dock power compliant",
      "A marina walkdown {setting} shows {slot} pedestal receptacles with the required ground-fault protection at the marina main and pedestals, no-swimming signage posted, and shore-power assemblies listed and intact. Judge.",
      [["ground-fault", "protection"], ["signage"]], [["document"]], forb=[["fail"]], family="marina", s1="accepted/in-service",
      slots={"slot": ["30 A", "50 A", "mixed 30 A and 50 A"]}),
    V("ME", "fail", "high", "Leakage current above threshold",
      "Clamp measurements on a dock feeder {setting} read {slot} mA of ground-fault leakage with all boats connected; the marina main GFPE is set per 555.35. Report the reading and judge.",
      [["exceeds"], ["leakage"]], [["isolate", "slip"], ["repair"]],
      hz="shock", s1="tested/inspected", slots={"slot": ["45", "80", "120"]},
      prompt=DEFAULT_PROMPTS["ME"]),
    V("FD", "fail", "medium", "Tingle traced to a boat, not the dock",
      "Swimmers report tingling near a slip {setting}. Pedestal wiring checks clean; the leakage disappears when one boat's shore cord is lifted. Diagnose the source and disposition the slip.",
      [["boat"], ["source"]], [["notify", "owner"], ["prohibit", "connection"]],
      hz="shock", s1="accepted/in-service"),
    V("CC", "needs_more_info", "medium", "Datum plane data missing",
      "Electrical equipment heights on a fixed pier {setting} must clear the electrical datum plane, but the flood/water-level datum for the site is not in the package. Decide.",
      [["datum", "unknown"], ["confirm"]], [["obtain", "datum"]], s1="staged"),
]

VARIANTS["E-1204"] = [
    V("ME", "fail", "high", "String voltage over limit cold",
      "A rooftop PV design {setting} strings {slot} modules of 40 V open-circuit each in series. Site record low is -10 deg C, giving a 1.12 low-temperature correction. The inverter and wiring are rated 600 V. Compute the corrected string Voc and judge.",
      [["exceeds", "600"]], [["reduce", "modules"], ["recalculate"]],
      hz="fire", family="pvstring", s1="staged",
      slots={"slot": ["14", "15", "16"]},
      refs=["NEC 690.7", "CEC PV Install Guide"]),
    V("ME", "pass", "low", "String voltage within limit",
      "A rooftop PV design {setting} strings {slot} modules of 40 V open-circuit each in series, with a 1.12 low-temperature correction and 600 V equipment. Compute the corrected string Voc and judge.",
      [["within", "600"]], [["document"]], forb=[["fail"]], family="pvstring", s1="staged",
      slots={"slot": ["11", "12", "13"]},
      refs=["NEC 690.7", "CEC PV Install Guide"]),
    V("TS", "fail", "medium", "Unrated components in the DC circuit",
      "A PV punch walk {setting} finds {slot} in the rooftop DC circuit. Judge the component selection for a PV source circuit.",
      [["not", "rated"], ["pv"]], [["replace", "listed"]],
      s1="tested/inspected",
      slots={"slot": ["indoor-rated NM cable run under the array", "an unlisted DC combiner box",
                      "standard AC breakers used for DC string protection"]}),
    V("CC", "fail", "medium", "Rapid shutdown / labeling absent",
      "A completed rooftop array {setting} has no rapid-shutdown initiation device or the required labeling at the service equipment; first responders would have no array-level control. Judge.",
      [["rapid", "shutdown"], ["label"]], [["install"], ["label"]],
      hz="fire", s1="tested/inspected"),
    V("ME", "needs_more_info", "medium", "Shading assessment missing",
      "A PV production estimate {setting} promises output, but no shading study or horizon data exists for the site and the roof faces are unrecorded. Decide whether the estimate can be accepted.",
      [["shading", "unknown"], ["confirm"]], [["site", "survey"]], s1="staged"),
]

VARIANTS["E-1205"] = [
    V("ME", "fail", "high", "120 percent rule violated",
      "A load-side PV interconnection {setting} lands a {inv} A inverter breaker at the opposite end of a {bus} A busbar whose main is {main} A. Check the 705.12 120 percent allowance and judge.",
      [["120", "percent"], ["exceeds"]], [["reduce", "inverter", "breaker"], ["derate", "main"]],
      hz="fire", family="pv120", s1="staged",
      slots={"inv": ["60", "70"], "bus": ["200"], "main": ["200"]},
      refs=["NEC 705.12"]),
    V("ME", "pass", "low", "120 percent rule satisfied",
      "A load-side PV interconnection {setting} lands a {inv} A inverter breaker at the opposite end of a {bus} A busbar whose main is {main} A. Check the 705.12 120 percent allowance and judge.",
      [["within"], ["120", "percent"]], [["document"], ["label"]], forb=[["fail"]],
      family="pv120", s1="staged",
      slots={"inv": ["30", "40"], "bus": ["200"], "main": ["200"]},
      refs=["NEC 705.12"]),
    V("CC", "fail", "medium", "Interconnection breaker location/retention wrong",
      "A PV interconnection {setting} has the inverter breaker {slot}. Judge against the 705.12 conditions.",
      [["opposite", "end"], ["retained"]], [["relocate", "breaker"], ["fasten"]],
      s1="tested/inspected",
      slots={"slot": ["installed adjacent to the main instead of the opposite end", "without the required hold-down kit",
                      "on a feeder tap with no OCPD at the tap"]}),
    V("ID", "fail", "low", "Required PV placards missing",
      "A final walk {setting} finds the PV system operating but with no directory placard at the service showing the second power source, and no DC disconnect labeling. Judge.",
      [["placard"], ["missing"]], [["install", "labels"]], s1="tested/inspected"),
    V("DOC", "needs_more_info", "medium", "Busbar rating unreadable",
      "A PV design package {setting} assumes a 225 A busbar, but the panel label is corroded and the model number is not legible in any photo; the rating cannot be confirmed. Decide.",
      [["busbar", "unverified"], ["confirm"]], [["verify", "rating"]], s1="staged"),
]

VARIANTS["E-1206"] = [
    V("CC", "fail", "high", "Antenna mast not grounded",
      "A rooftop antenna installation {setting} shows {slot}. Judge against the Article 810 grounding rules.",
      [["ground"], ["missing"]], [["install", "grounding"], ["bond"]],
      hz="shock", family="ant", s1="tested/inspected",
      slots={"slot": ["a mast with no grounding conductor at all", "a lead-in with no antenna discharge unit",
                      "a ground rod driven for the mast but not bonded to the building electrode system"]}),
    V("CC", "pass", "low", "Antenna grounding complete",
      "A rooftop {slot} installation {setting} shows the mast grounded with the required conductor size, a discharge unit on the lead-in near the entry point, and the electrode bonded to the building grounding electrode system. Judge.",
      [["bonded"], ["discharge"]], [["document"]], forb=[["fail"]], family="ant", s1="tested/inspected",
      slots={"slot": ["TV antenna", "amateur-radio antenna", "satellite dish"]}),
    V("ID", "fail", "medium", "Comm cable violating separation",
      "A satellite/coax drop {setting} runs {slot}. Judge the routing.",
      [["separation"], ["clearance"]], [["reroute"]], s1="rough-complete",
      slots={"slot": ["stapled alongside a service-entrance cable down the mast", "through the same bored holes as NM branch wiring with jackets abraded",
                      "across the roof surface where it blocks a service walkway"]}),
    V("CC", "needs_more_info", "medium", "Bond path concealed",
      "An antenna ground {setting} disappears into a finished soffit and its connection to the building electrode system cannot be observed; no photo record exists. Decide.",
      [["bond", "unverified"], ["confirm"]], [["continuity", "test"], ["expose"]], s1="tested/inspected"),
]

VARIANTS["E-1301"] = [
    V("CC", "fail", "critical", "Submerged gear returned to service: {slot}",
      "After flood cleanup {setting}, {slot} that was under water is dried, wiped down, and re-energized. Apply the NEMA water-damage replace/recondition table and judge.",
      [["replace"], ["water", "damage"]], [["replace"], ["do", "not", "energize"]],
      hz="fire", family="water", s1="accepted/in-service",
      slots={"slot": ["a molded-case breaker panel", "a run of NM cable and its devices", "a GFCI receptacle bank",
                      "a residential load center with its breakers"]}),
    V("CC", "pass", "low", "Water-exposure triage done right",
      "After {slot} {setting}, the contractor replaced all submerged molded-case breakers, devices, and NM cable per the NEMA table, and referred the equipment that was only splashed to the manufacturer for evaluation before re-energizing. Judge the triage.",
      [["replaced"], ["manufacturer"]], [["document"]], forb=[["fail"]], family="water", s1="tested/inspected",
      slots={"slot": ["a basement flood", "a storm-surge event", "a burst supply-line flood"]}),
    V("TRD", "fail", "high", "Insurance pressure to reuse flooded equipment",
      "An adjuster {setting} asks the electrician to megger a submerged panelboard and reuse it if the reading is acceptable, to reduce claim cost. The NEMA table calls for replacement regardless of test results. Judge the request.",
      [["replace", "regardless"]], [["decline"], ["document", "nema"]],
      hz="fire", s1="rework"),
    V("TS", "fail", "medium", "Wrong replacement class after water event",
      "Replacing flood-damaged gear {setting}, the crew installed {slot}. Judge the selection for the post-flood environment.",
      [["rating"], ["environment"]], [["replace", "rated"]],
      slots={"slot": ["interior-rated equipment in the still-damp crawl space", "a standard receptacle where the flood line dictates WR/GFCI",
                      "recovered used breakers of unknown history"]}),
    V("CC", "needs_more_info", "medium", "Water line vs equipment height unknown",
      "A flood claim {setting} hinges on whether the water reached the panel interior; the high-water mark is disputed and no interior corrosion photos exist. Decide the disposition.",
      [["water", "level", "unverified"], ["confirm"]], [["inspect", "interior"], ["establish", "water", "line"]],
      s1="rework"),
]

VARIANTS["E-1302"] = [
    V("CC", "fail", "critical", "Heat-exposed protective devices reused",
      "After a {slot} fire {setting}, breakers and fuses that saw the heat but 'look fine' are reinstalled. The NEMA fire/heat guide requires replacement of overcurrent devices exposed to elevated temperature. Judge.",
      [["replace"], ["heat"]], [["replace", "devices"]],
      hz="fire", family="heat", s1="rework",
      slots={"slot": ["kitchen", "attic", "shop"]}),
    V("CC", "pass", "low", "Heat-damage evaluation done right",
      "After {slot} {setting}, the contractor replaced all overcurrent devices and thermoplastic-insulated wiring in the heat-affected zone, and had the switchboard evaluated by the manufacturer's service group before reuse. Judge.",
      [["replaced"], ["evaluated"]], [["document"]], forb=[["fail"]], family="heat", s1="tested/inspected",
      slots={"slot": ["a contained electrical-room fire", "a kitchen fire two rooms away", "a small shop fire"]}),
    V("HAZ", "fail", "high", "Smoke-contaminated gear energized",
      "Restoration {setting} re-energized a panel whose interior shows soot film and acrid residue from PVC combustion; corrosive chlorides attack contacts and conductors over time. Judge the decision.",
      [["soot"], ["corrosive"]], [["clean", "evaluate"], ["replace", "contaminated"]],
      hz="fire", s1="accepted/in-service"),
    V("TRD", "needs_more_info", "medium", "Extent of thermal exposure unknown",
      "A melted fixture {setting} sits above a panel, but nobody can establish how hot the panel interior got; there is no thermal indicator, discoloration is ambiguous, and the manufacturer has not been consulted. Decide.",
      [["exposure", "unknown"], ["manufacturer"]], [["consult", "manufacturer"], ["inspect"]],
      s1="rework"),
]

VARIANTS["E-1303"] = [
    V("TRD", "fail", "high", "Known-defective legacy panel kept in service: {slot}",
      "A service call {setting} finds {slot}. The customer wants only the immediate symptom fixed. Judge the disposition recommendation.",
      [["replace", "panel"], ["known", "hazard"]], [["recommend", "replacement"], ["document"]],
      hz="fire", family="legacy", s1="accepted/in-service",
      slots={"slot": ["an FPE Stab-Lok panel with a breaker that did not trip during a fault",
                      "a Zinsco panel with bus corrosion and a melted breaker stab",
                      "a fuse box with pennies behind two fuses"]}),
    V("TRD", "pass", "low", "Legacy system serviced within its limits",
      "A service call {setting} on {slot} in good condition documents its state, avoids burying it in new insulation, refuses to extend it, and quotes a circuit replacement path; the immediate repair used compatible methods. Judge the approach.",
      [["documented"], ["not", "extended"]], [["document"], ["quote", "replacement"]],
      forb=[["fail"]], family="legacy", s1="accepted/in-service",
      slots={"slot": ["knob-and-tube wiring", "cloth-insulated NM cable", "an early conduit-and-cloth system"]}),
    V("CC", "fail", "high", "Aluminum branch wiring patched wrong",
      "A flickering-lights call {setting} finds 1970s aluminum branch conductors pigtailed to copper with standard twist connectors not rated for the purpose. Judge the repair method.",
      [["not", "rated"], ["aluminum"]], [["listed", "connector"], ["co/alr"]],
      hz="fire", s1="rework"),
    V("HAZ", "fail", "medium", "Cloth-insulated NM crumbling in attic",
      "An attic inspection {setting} finds cloth-and-rubber insulated cable with insulation flaking off at every disturbed point, buried under new blown-in insulation with junction points unboxed. Judge.",
      [["insulation", "deteriorated"], ["unboxed"]], [["junction", "boxes"], ["replace", "deteriorated"]],
      hz="fire", s1="accepted/in-service"),
    V("TRD", "needs_more_info", "medium", "Panel brand/state not identifiable",
      "A buyer's inspection {setting} flags an old panel, but the label is gone, the deadfront is painted shut, and the inspector could not open it; the brand and interior condition are unknown. Decide.",
      [["unidentified"], ["confirm"]], [["open", "inspect"], ["identify"]], s1="accepted/in-service"),
]

VARIANTS["E-1304"] = [
    V("SEQ", "fail", "medium", "Troubleshooting by parts-swapping",
      "A dead-circuit ticket {setting} shows the tech replaced {slot} in sequence without any measurement between swaps; the fault persists and three parts were consumed. Judge the method.",
      [["no", "measurement"], ["parts"]], [["measure"], ["half-split"], ["isolate"]],
      family="ts-method", s1="accepted/in-service",
      slots={"slot": ["the receptacle, the breaker, and then the switch", "two GFCIs and a breaker", "the fixture, the dimmer, and the breaker"]}),
    V("SEQ", "pass", "low", "Systematic half-split diagnosis",
      "A dead-circuit ticket {setting} shows the tech verified the symptom, checked the breaker and voltage at the panel, split the circuit at {slot}, measured each half, and isolated the fault to one cable segment before opening anything else. Judge the method.",
      [["systematic"], ["isolated"]], [["repair", "segment"], ["document"]],
      forb=[["fail"]], family="ts-method", s1="accepted/in-service",
      slots={"slot": ["an accessible midpoint junction", "the mid-run receptacle", "a ceiling box near the middle of the run"]}),
    V("FD", "fail", "high", "Open neutral misdiagnosed",
      "Lights {setting} brighten and dim as large loads cycle, and a plug-in tester shows normal on some receptacles. The tech blamed the dimmer and replaced it. Diagnose the actual condition and judge the disposition.",
      [["open", "neutral"]], [["inspect", "service", "neutral"], ["utility"]],
      hz="fire", s1="accepted/in-service", media="meter-readout-image"),
    V("ME", "fail", "medium", "Meter misuse produced a phantom reading",
      "A tech {setting} measured {slot} and concluded the circuit was live, then found no load would run. Identify the measurement error and judge the conclusion.",
      [["phantom", "voltage"], ["high", "impedance"]], [["low-impedance", "test"], ["retest"]],
      s1="accepted/in-service", media="meter-readout-image",
      slots={"slot": ["120 V on a disconnected conductor with a high-impedance digital meter", "full voltage across an open switch with no load connected"]}),
    V("FD", "needs_more_info", "medium", "Intermittent cannot be reproduced",
      "A once-a-week breaker trip {setting} cannot be reproduced during the visit; no event data, load log, or thermal image exists yet. Decide the disposition.",
      [["intermittent"], ["insufficient"]], [["logger"], ["schedule", "monitoring"]],
      s1="accepted/in-service"),
]

VARIANTS["E-1305"] = [
    V("FD", "fail", "high", "IR hot spot dismissed",
      "An IR scan {setting} shows one lug running {slot} deg C above the adjacent same-load phase. The finding was logged as 'monitor' with no torque check or load verification. Judge the disposition against common delta-T severity criteria.",
      [["delta"], ["investigate"]], [["de-energize"], ["torque", "check"]],
      hz="fire", family="ir", s1="tested/inspected", media="infrared-image",
      slots={"slot": ["35", "48", "60"]}),
    V("FD", "pass", "low", "IR anomaly triaged correctly",
      "An IR scan {setting} found a {slot} deg C rise on a lightly loaded lug; the tech verified load balance, scheduled a torque check at the next shutdown, and documented the trend baseline. Judge the disposition.",
      [["trended"], ["scheduled"]], [["document"]], forb=[["fail"]], family="ir",
      s1="tested/inspected", media="infrared-image",
      slots={"slot": ["10", "12", "14"]}),
    V("PA", "fail", "medium", "PM program exists on paper only",
      "A reliability audit {setting} finds the electrical PM plan calls for annual IR scans and breaker exercising, but records show {slot}. Judge the program state.",
      [["overdue"], ["records"]], [["schedule", "pm"], ["update", "records"]],
      s1="accepted/in-service",
      slots={"slot": ["no scan performed in three years", "breakers never exercised since commissioning", "scans done but findings never closed"]}),
    V("ME", "needs_more_info", "medium", "IR image lacks reference data",
      "A submitted IR image {setting} shows a bright connection but records no emissivity setting, no load at the time, and no comparison phase. Decide whether severity can be assigned.",
      [["load", "unknown"], ["confirm"]], [["rescan"], ["record", "load"]],
      s1="tested/inspected", media="infrared-image"),
]

VARIANTS["E-1401"] = [
    V("ME", "fail", "medium", "Takeoff missed scope: {slot}",
      "Comparing a bid takeoff {setting} to the plans shows the count for {slot} is materially short; the plans call for more than the proposal includes. Judge the takeoff.",
      [["undercount"], ["takeoff"]], [["recount"], ["revise", "bid"]],
      s1="staged", family="takeoff",
      slots={"slot": ["home runs on the second floor", "site lighting circuits", "data drops in the open office"]}),
    V("ME", "pass", "low", "Takeoff reconciles with plans",
      "A bid review {setting} samples {slot} from the takeoff against the drawings; device counts, fixture counts, and feeder lengths reconcile within normal waste allowances. Judge the takeoff.",
      [["reconciles"], ["counts"]], [["approve", "bid"]], forb=[["fail"]],
      s1="staged", family="takeoff",
      slots={"slot": ["three systems", "the lighting and receptacle scopes", "two floors"]}),
    V("DOC", "fail", "medium", "Labor units misapplied",
      "An estimate {setting} prices overhead branch conduit at slab-on-grade labor units and ignores the {slot} condition noted on the general notes. Judge the estimate basis.",
      [["labor", "unit"], ["condition"]], [["reprice"]], s1="staged",
      slots={"slot": ["occupied-facility night-work", "high-ceiling scissor-lift", "asbestos-adjacent containment"]}),
    V("PA", "needs_more_info", "medium", "Percent-complete billing unsupported",
      "A progress invoice {setting} claims 70 percent complete on the electrical scope, but no schedule of values breakdown or field verification accompanies it. Decide whether the claim can be certified.",
      [["unsupported"], ["confirm"]], [["schedule", "of", "values"], ["field", "verify"]],
      s1="in-progress"),
]

VARIANTS["E-1402"] = [
    V("DOC", "fail", "medium", "Work performed outside contract scope",
      "A dispute review {setting} shows the signed proposal covers {slot}, but the crew also performed additional work on verbal direction with no change order; payment is now contested. Judge the documentation practice.",
      [["no", "change", "order"]], [["written", "change", "order"], ["document"]],
      s1="accepted/in-service", family="scope",
      slots={"slot": ["a panel swap only", "kitchen circuits only", "the garage subpanel only"]}),
    V("DOC", "pass", "low", "Change handled with a written CO",
      "During a remodel {setting}, the owner requested {slot}; the contractor priced it, obtained a signed change order describing scope and price, and invoiced against it. Judge the practice.",
      [["signed", "change", "order"]], [["document"]], forb=[["fail"]], family="scope",
      s1="accepted/in-service",
      slots={"slot": ["added recessed lighting", "a hot-tub circuit addition", "an EV-charger circuit"]}),
    V("TRD", "fail", "medium", "Exclusion buried, customer expectation mismatch",
      "A proposal {setting} excludes {slot} in fine print while the cover letter promises a 'complete, code-compliant installation'; the customer reasonably expected the excluded work. Judge the proposal drafting.",
      [["exclusion"], ["misleading"]], [["clarify", "scope"], ["revise", "proposal"]],
      s1="staged",
      slots={"slot": ["patching and painting", "permit fees and inspections", "utility coordination charges"]}),
    V("DOC", "needs_more_info", "medium", "Contract version in force unclear",
      "Two signed proposal revisions {setting} exist with different prices and scopes, both dated the same week; which version governs the disputed work cannot be determined from the documents provided. Decide.",
      [["version", "conflict"], ["confirm"]], [["obtain", "correspondence"]], s1="accepted/in-service"),
]

VARIANTS["E-1403"] = [
    V("TRD", "fail", "high", "Customer pressure to skip {slot}",
      "A customer {setting} pushes hard to {slot}, offering to sign a waiver and pay cash. Judge the correct professional response.",
      [["decline"], ["required"]], [["decline"], ["explain", "requirement"]],
      hz="shock", family="ethics", s1="staged",
      slots={"slot": ["skip the permit on a service upgrade", "reuse the flooded panel to save the claim deductible",
                      "leave the ungrounded three-prong receptacles for the home sale", "energize the addition before inspection"]}),
    V("TRD", "pass", "low", "Line held with a documented alternative",
      "A customer {setting} asked to {slot}; the contractor declined, explained the requirement and the risk, offered a compliant alternative with a phased price, and recorded the conversation in the job file. Judge the response.",
      [["declined"], ["documented"]], [["document"]], forb=[["fail"]], family="ethics", s1="staged",
      slots={"slot": ["skip permitting", "reuse the flooded panel", "energize before inspection"]}),
    V("HAZ", "fail", "critical", "Emergency 'just get it on' bypass",
      "During a storm outage {setting}, a customer demands power be restored tonight; the tech bypasses {slot} to energize, planning to 'come back later.' Judge the decision.",
      [["bypass"], ["temporary"]], [["restore", "protection"], ["do", "not", "energize"]],
      hz="shock", s1="rework",
      slots={"slot": ["the damaged meter enclosure inspection", "a tripping main breaker with a direct jumper", "the utility's required disconnect verification"]}),
    V("TRD", "needs_more_info", "medium", "Scope of customer-supplied gear unknown",
      "A customer {setting} supplies their own fixture 'bought online' and insists on installation; the listing mark and ratings cannot be verified from the packaging provided. Decide.",
      [["listing", "unverified"], ["confirm"]], [["verify", "listing"]], s1="staged"),
]

VARIANTS["E-1404"] = [
    V("TRD", "fail", "high", "Unqualified worker assigned energized task",
      "A foreman {setting} sends {slot} to troubleshoot inside an energized 480 V panel to keep the schedule. Judge the assignment against qualified-person requirements.",
      [["qualified"], ["energized"]], [["reassign"], ["de-energize"]],
      hz="shock", family="crew", s1="in-progress",
      slots={"slot": ["a first-year apprentice alone", "a laborer with a borrowed meter", "a second-year apprentice without PPE or supervision"]}),
    V("TRD", "pass", "low", "Task matched to skill with supervision",
      "A foreman {setting} pairs a third-year apprentice with a journeyman for {slot} on a de-energized, locked-out board, walks the task plan first, and reserves the energized diagnostics for the qualified journeyman with PPE. Judge the crew plan.",
      [["supervised"], ["qualified"]], [["document"]], forb=[["fail"]], family="crew", s1="in-progress",
      slots={"slot": ["panel makeup", "feeder terminations", "device trim"]}),
    V("SEQ", "fail", "medium", "Crew sequenced into each other",
      "A two-crew day {setting} put the wire-pulling crew and the termination crew on the same feeder simultaneously; the pullers re-tensioned conductors the terminators had already landed, damaging {slot}. Judge the coordination.",
      [["coordination"], ["rework"]], [["sequence", "crews"], ["re-terminate"]],
      s1="rework", slots={"slot": ["two lugs", "a panel's neutral bar", "several terminations"]}),
    V("HAZ", "needs_more_info", "medium", "Certification records not on site",
      "An audit {setting} asks whether the crew members working the lift and the energized testing hold current certifications; the records are 'at the office' and cannot be produced. Decide.",
      [["records", "unavailable"], ["confirm"]], [["produce", "records"], ["suspend", "restricted", "tasks"]],
      s1="in-progress"),
]


# --------------------------------------------------------------------------
# Element registry
# --------------------------------------------------------------------------

def E(code, name, sub, tiers, refs, source, gen=None, count=0):
    return {"code": code, "name": name, "subcategory": sub, "tiers": tiers,
            "refs": refs, "source": source, "gen": gen, "count": count}


SUB9 = "2.1.9 Theory & Calculation"
SUB10 = "2.1.10 Code Navigation & Documents"
SUB11 = "2.1.11 Protection & Life Safety"
SUB12 = "2.1.12 Special Occupancies & Renewables"
SUB13 = "2.1.13 Forensics, Service & Maintenance"
SUB14 = "2.1.14 Business, Estimating & Customer Process"

ELEMENTS = [
    E("E-901", "Ohm's & Watt's law field checks", SUB9, ["T3", "T4", "T5"],
      ["Ohm's law", "Watt's law"], "basic-math & theory guide / equations chart", gen_e901, 35),
    E("E-902", "Series/parallel circuit analysis", SUB9, ["T4", "T5"],
      ["Series/parallel circuit rules"], "basic-math & theory guide", gen_e902, 30),
    E("E-903", "Voltage drop & remediation", SUB9, ["T1", "T2", "T3"],
      ["NEC 210.19 IN", "Ch. 9 Table 8"], "basic-math & theory guide / equations chart", gen_e903, 40),
    E("E-904", "Ampacity w/ correction & adjustment", SUB9, ["T1", "T2"],
      ["NEC 310.15", "Table 310.16"], "Equations Chart / NEC guides", gen_e904, 35),
    E("E-905", "Box & raceway fill calculations", SUB9, ["T2", "T3"],
      ["NEC 314.16"], "basic-math & theory guide", gen_e905, 35),
    E("E-906", "Bend geometry (offset/saddle/shrink)", SUB9, ["T1", "T2"],
      ["Bamford conduit bending manual"], "Hand_bending_conduit_and_tubing_by_Bill_Bamford.pdf", gen_e906, 35),
    E("E-907", "Motor FLC / OCPD / overload sizing", SUB9, ["T1", "T5"],
      ["NEC Art. 430"], "Equations Chart / NEC guides", gen_e907, 35),
    E("E-908", "Transformer FLA & OCPD sizing", SUB9, ["T1", "T2"],
      ["NEC 450.3"], "Equations Chart", gen_e908, 25),
    E("E-909", "Dwelling service load calculation", SUB9, ["T3"],
      ["NEC Art. 220"], "basic-math & theory guide", gen_e909, 30),
    E("E-910", "Power factor & efficiency", SUB9, ["T1", "T5"],
      ["Power factor formulas"], "basic-math & theory guide / equations chart", gen_e910, 20),

    E("E-1001", "Governing-article identification", SUB10, ["T2", "T3", "T4"],
      ["NEC Index"], "NEC Index PDFs / Code Organizer", count=28),
    E("E-1002", "Code-cycle deltas & jurisdiction", SUB10, ["T2", "T3", "T4"],
      ["NEC 2017/2020/2023 changes"], "Top-10 Code Changes PDFs", count=26),
    E("E-1003", "Listing, labeling & field modification", SUB10, ["T1", "T2", "T5"],
      ["UL White Book", "NEC 110.3(B)"], "UL Whitebook", count=24),
    E("E-1004", "Panel schedules, one-lines & plans", SUB10, ["T1", "T2"],
      ["NEC 408.4"], "Code Organizing Drawing", count=26),
    E("E-1005", "Permit & inspection workflow", SUB10, ["T2", "T3"],
      ["Local permit process"], "contractor business-forms library", count=22),

    E("E-1101", "GFCI placement - dwelling", SUB11, ["T3"],
      ["NEC 210.8(A)"], "23_GFCI_and_AFCI_Protection.pdf", count=30),
    E("E-1102", "GFCI placement - non-dwelling", SUB11, ["T2", "T4"],
      ["NEC 210.8(B)"], "23_GFCI_and_AFCI_Protection.pdf", count=26),
    E("E-1103", "AFCI requirements & retrofit paths", SUB11, ["T3", "T4"],
      ["NEC 210.12"], "23_GFCI_and_AFCI_Protection.pdf", count=26),
    E("E-1104", "GFCI/AFCI field testing & end-of-life", SUB11, ["T3", "T4"],
      ["CPSC GFCI study", "NEMA GFCI study"], "CPS-GFCI-Study.pdf / NEMA-GFCI-Study.pdf", count=28),
    E("E-1105", "Fire alarm circuits & supervision", SUB11, ["T2"],
      ["NEC Art. 760", "NFPA 72"], "23_FREE_PDF_Fire_Alarm_Systems.pdf", count=28),
    E("E-1106", "Generator install & transfer equipment", SUB11, ["T2", "T3", "T4"],
      ["NEC 445", "NEC 702"], "23_FREE_PDF_Generators_and_Standby_Power_Systems.pdf", count=30),
    E("E-1107", "Standby classification & load priority", SUB11, ["T1", "T2"],
      ["NEC 700", "NEC 701", "NEC 702"], "23_FREE_PDF_Generators_and_Standby_Power_Systems.pdf", count=24),

    E("E-1201", "Pool/spa wiring & clearances", SUB12, ["T2", "T3"],
      ["NEC Art. 680"], "23_FREE_PDF_Swimming_Pools_Hot_Tubs_and_Fountains.pdf", count=28),
    E("E-1202", "Hot tub packaged-unit installs", SUB12, ["T3", "T4"],
      ["NEC 680.42"], "23_FREE_PDF_Swimming_Pools_Hot_Tubs_and_Fountains.pdf", count=22),
    E("E-1203", "Marina/dock power & ESD", SUB12, ["T2", "T4"],
      ["NEC Art. 555"], "FREE_PDF_Marinas_and_Docks_2023.pdf", count=28),
    E("E-1204", "PV array design & stringing", SUB12, ["T2", "T3"],
      ["NEC 690.7", "CEC PV guide"], "PV_Install_Guide-Latest_CEC.pdf", count=26),
    E("E-1205", "PV interconnection & labeling", SUB12, ["T2", "T3"],
      ["NEC 705.12", "NEC 690.56"], "PV_Install_Guide-Latest_CEC.pdf", count=26),
    E("E-1206", "Antenna/comm grounding", SUB12, ["T2", "T3"],
      ["NEC Art. 810", "NEC Art. 800"], "23_FREE_PDF_Communications_Systems.pdf", count=18),

    E("E-1301", "Water-damaged equipment triage", SUB13, ["T3", "T4"],
      ["NEMA GD-1"], "NEMA water-damage guide", count=26),
    E("E-1302", "Fire/heat-damaged equipment evaluation", SUB13, ["T2", "T4"],
      ["NEMA fire/heat guide", "NEC 110.11"], "NEMA-Evaluating-Fire-and-Heat-Damaged-Electrical-Equipment.pdf", count=24),
    E("E-1303", "Legacy-system service decisions", SUB13, ["T3", "T4"],
      ["NEC 110.3(B)", "field history"], "trade service literature", count=26),
    E("E-1304", "Systematic troubleshooting with meters", SUB13, ["T3", "T4", "T5"],
      ["Troubleshooting method"], "basic-math & theory guide", count=26),
    E("E-1305", "Thermal/PM inspection programs", SUB13, ["T1", "T5"],
      ["NETA MTS delta-T", "NFPA 70B"], "NEMA heat-damage guide", count=18),

    E("E-1401", "Takeoff & estimating", SUB14, ["T2", "T3"],
      ["Estimating practice"], "Electrical_Proposal template", count=24),
    E("E-1402", "Proposals, scope & change orders", SUB14, ["T2", "T3", "T4"],
      ["Contract practice"], "Electrical_Proposal template", count=24),
    E("E-1403", "Customer-pressure ethics", SUB14, ["T3", "T4"],
      ["Permit law", "NEMA GD-1"], "contractor business-forms library", count=24),
    E("E-1404", "Crew planning & supervision", SUB14, ["T1", "T2"],
      ["NFPA 70E qualified person"], "Handbook_Sample.doc", count=22),
]


CONTEXT_CLAUSES = [
    "The building remains occupied while the work proceeds.",
    "The work was performed on a weekend shutdown with a reduced crew.",
    "The area had been re-worked once before under an earlier punch item.",
    "Weather delayed the schedule and the crew is under time pressure.",
    "A different crew performed the earlier phase of this work.",
    "The customer has already been invoiced for this phase.",
    "This is the last open item before the area can be turned over.",
    "The evidence was collected during a routine quality walk.",
    "The job file shows no prior corrections at this address.",
    "A trainee documented the visit for the company's QA program.",
    "The general contractor has asked for a same-day disposition.",
    "The work order was opened after an unrelated warranty visit.",
    "Photographs were taken before and after the observation.",
    "The site superintendent disputes the finding informally.",
    "An insurance representative has requested the written outcome.",
    "The crew that did the work is no longer on this project.",
]

DECISION_SHARES = {"fail": 0.50, "pass": 0.35, "needs_more_info": 0.15}


def expand_variants(el: dict, count: int, rng: random.Random) -> list[dict]:
    """Expand a variant library to `count` specs with a balanced decision mix.

    Base combos are variant x tier x slot values; when a decision bucket needs
    more items than it has base combos, combos repeat with a distinct context
    clause appended so no two premises are identical.
    """
    vlist = VARIANTS[el["code"]]
    by_dec: dict[str, list] = defaultdict(list)
    for vi, v in enumerate(vlist):
        slot_names = sorted(v["slots"])
        slot_lists = [v["slots"][s] for s in slot_names]
        for tier in el["tiers"]:
            for values in itertools.product(*slot_lists) if slot_lists else [()]:
                by_dec[v["dec"]].append((vi, tier, dict(zip(slot_names, values))))
    for lst in by_dec.values():
        rng.shuffle(lst)

    shares = {d: s for d, s in DECISION_SHARES.items() if by_dec.get(d)}
    total = sum(shares.values())
    targets = {d: s / total * count for d, s in shares.items()}

    picked, counts, seen_vi = [], Counter(), set()
    for d, lst in by_dec.items():
        for c in lst:
            if c[0] not in seen_vi:
                seen_vi.add(c[0])
                picked.append(c)
                counts[d] += 1
    cursor = {d: 0 for d in by_dec}
    while len(picked) < count:
        d = max(shares, key=lambda x: targets[x] - counts[x])
        lst = by_dec[d]
        c = lst[cursor[d] % len(lst)]
        cursor[d] += 1
        picked.append(c)
        counts[d] += 1
    picked = picked[:count]

    out, uses = [], Counter()
    for vi, tier, slotvals in picked:
        key = (vi, tier, tuple(sorted(slotvals.items())))
        n = uses[key]
        uses[key] += 1
        if n > len(CONTEXT_CLAUSES):
            raise SystemExit(f"{el['code']}: combo reused past context capacity")
        ctx_idx = None if n == 0 else n - 1
        v = VARIANTS[el["code"]][vi]
        fmt = dict(slotvals)
        fmt["setting"] = TIER_SETTINGS[tier]
        scenario = v["p"].format(**fmt)
        if ctx_idx is not None:
            scenario = f"{scenario} {CONTEXT_CLAUSES[ctx_idx]}"
        title = v["t"].format(**{k: fmt.get(k, "") for k in fmt})
        # Counterfactual family group: fail variants and their pass twins in the
        # same family and tier share a pair_id (slot vocabularies differ between
        # the defective and corrected scenes, so grouping is per family+tier).
        pair_id = None
        if v["family"]:
            pair_id = f"{el['code'].lower()}-{v['family']}-{tier.lower()}"
        push(out, spec(el, v["tt"], tier, v["dec"], v["risk"], scenario,
                        v["find"], v["act"], title, s1=v["s1"], forbidden=v["forb"],
                        prompt=v["prompt"], hazard_class=v["hz"], pair_id=pair_id,
                        media_plan=v["media"], refs=v["refs"]))
    return out


def main() -> None:
    rng = random.Random(SEED)
    specs: list[dict] = []
    for el in ELEMENTS:
        el_rng = random.Random(f"{SEED}-{el['code']}")
        if el["gen"]:
            specs.extend(el["gen"](el, el["count"], el_rng))
        else:
            specs.extend(expand_variants(el, el["count"], el_rng))

    assert len(specs) == 1000, f"expected 1000 specs, got {len(specs)}"
    assert len({s["id"] for s in specs}) == len(specs), "duplicate ids"

    OUT.write_text(json.dumps(specs, indent=1, sort_keys=True) + "\n")

    dec = Counter(s["decision"] for s in specs)
    tt = Counter(s["task_type"] for s in specs)
    tiers = Counter(s["tier"] for s in specs)
    subs = Counter(s["subcategory"] for s in specs)
    hz = Counter(s["hazard_class"] for s in specs)
    numeric = sum(1 for s in specs if "expected_value" in s)
    paired = len({s["pair_id"] for s in specs if "pair_id" in s})
    media = Counter(s.get("media_plan", "none") for s in specs)

    print(f"wrote {len(specs)} specs -> {OUT.relative_to(ROOT)}")
    print("decisions:", dict(dec))
    print("task types:", dict(sorted(tt.items())))
    print("tiers:", dict(sorted(tiers.items())))
    print("hazard classes:", dict(hz))
    by_pair: dict[str, set] = defaultdict(set)
    for s in specs:
        if "pair_id" in s:
            by_pair[s["pair_id"]].add(s["decision"])
    both = sum(1 for v in by_pair.values() if len(v) > 1)
    print(f"numeric (expected_value) items: {numeric}")
    print(f"counterfactual family groups: {paired} ({both} contain both decisions)")
    print("media plans:", dict(media))
    print("by subcategory:")
    for k, v in sorted(subs.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
