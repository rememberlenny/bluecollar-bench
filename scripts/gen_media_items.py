#!/usr/bin/env python3
"""gen_media_items — render synthetic instrument images and emit multimodal
benchmark items whose ground truth is computed from the same parameters that
drew the image. Four families:

  rotor    Brake rotor micrometer vs. stamped minimum (A-201, ME)
  micron   Evacuation decay test on a micron gauge (H-301, FD)
  gasmeter Confined-space 4-gas meter screen (X-103, DOC)
  sling    Two-leg sling angle/tension diagram vs. WLL (S-301, ME)

Outputs: benchmark/media/*.png and benchmark/items/media_items_v2.json.
Decisions are naturally mixed (pass / fail / needs_more_info).
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "benchmark" / "media"
OUT = ROOT / "benchmark" / "items" / "media_items_v2.json"
rng = random.Random(20260704)


def lcd_panel(ax, x, y, w, h, label, value, unit=""):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                fc="#101418", ec="#444"))
    ax.text(x + 0.02, y + h - 0.05, label, color="#9adcf0", fontsize=9,
            family="monospace", va="top")
    ax.text(x + w / 2, y + h / 2 - 0.03, f"{value}{unit}", color="#38ff6e",
            fontsize=22, family="monospace", ha="center", va="center", weight="bold")


def base_fig():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#d8d8d0")
    return fig, ax


def render_rotor(path, min_th, measured, stamp_ok):
    fig, ax = base_fig()
    ax.text(0.5, 0.95, "FRONT ROTOR — OUTBOARD MEASUREMENT", ha="center", fontsize=11, weight="bold")
    lcd_panel(ax, 0.08, 0.45, 0.5, 0.3, "DIGITAL MICROMETER  mm", f"{measured:.2f}")
    stamp = f"MIN TH {min_th:.1f} mm" if stamp_ok else "MIN TH --.- mm (illegible)"
    ax.add_patch(FancyBboxPatch((0.63, 0.45), 0.3, 0.3, boxstyle="round,pad=0.02", fc="#8a8a86", ec="#333"))
    ax.text(0.78, 0.6, stamp, ha="center", va="center", fontsize=10, family="monospace", color="#111")
    ax.text(0.78, 0.4, "rotor hat casting", ha="center", fontsize=8, color="#333")
    ax.text(0.5, 0.15, "Measurement taken at pad contact area, four points averaged.",
            ha="center", fontsize=9, style="italic")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def render_micron(path, r0, r1):
    fig, ax = base_fig()
    ax.text(0.5, 0.95, "EVACUATION DECAY TEST — PUMP ISOLATED", ha="center", fontsize=11, weight="bold")
    lcd_panel(ax, 0.06, 0.45, 0.42, 0.3, "MICRONS @ ISOLATION (t=0)", f"{r0}")
    lcd_panel(ax, 0.52, 0.45, 0.42, 0.3, "MICRONS @ t=10 min", f"{r1}")
    ax.text(0.5, 0.15, "Micron gauge at far port. Cores removed. System isolated from pump at t=0.",
            ha="center", fontsize=9, style="italic")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def render_gasmeter(path, o2, lel, h2s, co):
    fig, ax = base_fig()
    ax.add_patch(FancyBboxPatch((0.2, 0.08), 0.6, 0.84, boxstyle="round,pad=0.02", fc="#2a2d31", ec="#111"))
    ax.text(0.5, 0.86, "4-GAS MONITOR", ha="center", fontsize=11, color="#ddd", weight="bold")
    rows = [("O2  %VOL", o2), ("LEL  %", lel), ("H2S  ppm", h2s), ("CO  ppm", co)]
    y = 0.66
    for label, val in rows:
        ax.text(0.27, y, label, fontsize=11, color="#9adcf0", family="monospace")
        ax.text(0.73, y, str(val), fontsize=15, color="#38ff6e", family="monospace",
                ha="right", weight="bold")
        y -= 0.15
    ax.text(0.5, 0.03, "Pre-entry test at vessel manway, probe lowered to mid-depth.",
            ha="center", fontsize=9, style="italic")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def render_sling(path, load, angle, wll):
    fig, ax = base_fig()
    ax.text(0.5, 0.95, "TWO-LEG SLING ARRANGEMENT", ha="center", fontsize=11, weight="bold")
    hx, hy = 0.5, 0.82
    half = 0.28 / math.tan(math.radians(angle)) if angle < 89 else 0.01
    half = min(half, 0.42)
    lx, rx = hx - half, hx + half
    ly = 0.42
    ax.plot([hx, lx], [hy, ly], color="#333", lw=3)
    ax.plot([hx, rx], [hy, ly], color="#333", lw=3)
    ax.plot([hx], [hy], marker="o", color="#111", markersize=10)
    ax.add_patch(FancyBboxPatch((lx - 0.02, 0.28), (rx - lx) + 0.04, 0.14,
                                boxstyle="round,pad=0.01", fc="#7f8c8d", ec="#333"))
    ax.text(hx, 0.35, f"LOAD  {load:,} lb", ha="center", fontsize=11, weight="bold", color="#111")
    ax.text(lx + 0.05, ly + 0.03, f"{angle}°", fontsize=11, color="#b03020", weight="bold")
    ax.plot([lx, lx + 0.12], [ly, ly], color="#b03020", lw=1, ls="--")
    ax.text(0.5, 0.14, f"Each sling leg tagged WLL {wll:,} lb (vertical rating).",
            ha="center", fontsize=10)
    ax.text(0.5, 0.07, "Horizontal sling angle shown at the load.", ha="center",
            fontsize=9, style="italic")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def skeleton(fam, idx, tier, disc, dcode, el, ecode, sub, ttype, tname, refs, src):
    return {
        "id": f"v2-media-{fam}-{idx:03d}",
        "title": f"{tier} {ecode} {tname} (image)",
        "tier": tier, "discipline": disc, "discipline_code": dcode,
        "element": el, "element_code": ecode, "subcategory": sub,
        "task_type": ttype, "task_type_name": tname,
        "s1_state": "tested/inspected", "s3_percent": 90,
        "source_refs": refs, "source_file": src,
        "generation": "synthetic-media-v2",
        "modality": "image",
    }


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    items: list[dict] = []

    # --- rotor family: 14 items ---
    for i in range(14):
        min_th = rng.choice([22.0, 24.0, 26.0, 28.0])
        kind = "nmi" if i % 7 == 6 else ("fail" if i % 2 else "pass")
        delta = rng.uniform(-1.4, -0.1) if kind == "fail" else rng.uniform(0.6, 3.0)
        measured = round(min_th + delta, 2)
        fname = f"rotor_{i:03d}.png"
        render_rotor(MEDIA / fname, min_th, measured, stamp_ok=(kind != "nmi"))
        it = skeleton("rotor", i, "T4", "2.9 Automotive & Powertrain", "2.9",
                      "A-201 Brakes", "A-201", "2.9.2 Chassis", "ME",
                      "Measurement & estimation", ["OEM specs"],
                      "docs/source/element-trees-industrial-service-v0.1.md")
        it["media"] = [fname]
        it["scenario"] = ("The image shows a digital micrometer reading taken on a front brake rotor "
                          "and the specification stamp on the rotor hat.")
        it["prompt"] = ("Read the measurement and the stamped minimum from the image. Report the measured "
                        "thickness in the `value` field (mm) and decide whether the rotor may remain in service.")
        it["expected_value"] = measured
        it["value_tolerance"] = 0.05
        it["findings_mode"] = "any_per_group"
        if kind == "pass":
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["above", "exceeds", "greater"]],
                      required_actions=[["service", "release", "document", "remain"]],
                      forbidden=[["replace", "rotor"]])
        elif kind == "fail":
            it.update(decision="fail", risk="high", s2_expected=["worn"],
                      required_findings=[["below", "under", "less"]],
                      required_actions=[["replace"]],
                      forbidden=[["remain", "in", "service"]])
        else:
            it.update(decision="needs_more_info", risk="medium", s2_expected=[],
                      required_findings=[["illegible", "unreadable", "unknown", "stamp"]],
                      required_actions=[["specification", "spec", "lookup", "verify"]],
                      forbidden=[["release"]])
            it["expected_value"] = measured  # reading is still legible on the mic
        items.append(it)

    # --- micron family: 14 items ---
    for i in range(14):
        r0 = rng.randint(320, 480)
        mode = ["pass", "leak", "moisture"][i % 3]
        if mode == "pass":
            r1 = r0 + rng.randint(20, 120)
            dec, risk = "pass", "low"
            rf = [["holds", "held", "tight", "acceptable"]]
            ra = [["charge", "proceed", "document"]]
            forb = [["leak"], ["moisture"]]
            s2 = []
        elif mode == "leak":
            r1 = rng.randint(2600, 6000)
            dec, risk = "fail", "high"
            rf = [["leak"]]
            ra = [["locate", "repair", "pressurize", "nitrogen"]]
            forb = [["charge", "system", "now"]]
            s2 = ["installed-defective"]
        else:
            r1 = rng.randint(1200, 1900)
            dec, risk = "fail", "medium"
            rf = [["moisture", "dehydrate", "stall"]]
            ra = [["evacuate", "triple", "continue"]]
            forb = [["charge", "system", "now"]]
            s2 = ["non-compliant"]
        fname = f"micron_{i:03d}.png"
        render_micron(MEDIA / fname, r0, r1)
        it = skeleton("micron", i, "T4", "2.3 HVAC-R", "2.3",
                      "H-301 Brazing & evacuation", "H-301", "2.3.3 Refrigeration Circuit",
                      "FD", "Fault diagnosis", ["EPA 608", "mfr specs"],
                      "docs/source/element-trees-construction-v0.1.md")
        it["media"] = [fname]
        it["scenario"] = ("The image shows micron gauge readings at pump isolation and ten minutes later "
                          "during a standing decay test on an evacuated refrigeration system.")
        it["prompt"] = ("Read both values from the image, report the 10-minute reading in `value`, diagnose "
                        "what the decay behavior indicates, and give the disposition.")
        it["expected_value"] = r1
        it["value_tolerance"] = 0
        it["findings_mode"] = "any_per_group"
        it.update(decision=dec, risk=risk, s2_expected=s2, required_findings=rf,
                  required_actions=ra, forbidden=forb)
        items.append(it)

    # --- gasmeter family: 14 items ---
    for i in range(14):
        o2, lel, h2s, co = 20.9, 0, 0, 0
        mode = ["pass", "o2low", "lel", "h2s", "co", "nmi", "pass"][i % 7]
        if mode == "pass":
            o2 = round(rng.uniform(20.4, 21.2), 1); lel = rng.randint(0, 3)
            h2s = rng.randint(0, 4); co = rng.randint(0, 15)
            dec, risk, s2 = "pass", "low", []
            rf = [["within", "acceptable", "limits", "normal"]]
            ra = [["entry", "proceed", "monitor", "continuous"]]
            forb = [["ventilate", "before", "entry"]]
        elif mode == "nmi":
            o2 = 20.9; lel = 1; h2s = "--"; co = 8
            dec, risk, s2 = "needs_more_info", "high", []
            rf = [["h2s", "missing", "blank", "sensor"]]
            ra = [["retest", "repair", "complete", "bump"]]
            forb = [["authorize", "entry", "now"]]
        else:
            if mode == "o2low": o2 = round(rng.uniform(17.0, 19.4), 1); lel, h2s, co = 1, 2, 10
            if mode == "lel": lel = rng.randint(12, 40); h2s, co = 1, 5
            if mode == "h2s": h2s = rng.randint(15, 60); lel, co = 2, 5
            if mode == "co": co = rng.randint(60, 300); lel, h2s = 1, 2
            dec, risk, s2 = "fail", "critical", []
            key = {"o2low": ["oxygen", "o2", "deficient"], "lel": ["flammable", "lel", "explosive"],
                   "h2s": ["h2s", "hydrogen", "sulfide"], "co": ["co", "carbon", "monoxide"]}[mode]
            rf = [key]
            ra = [["no", "entry", "ventilate", "prohibit"]]
            forb = [["authorize", "entry", "now"]]
        fname = f"gasmeter_{i:03d}.png"
        render_gasmeter(MEDIA / fname, o2, lel, h2s, co)
        it = skeleton("gasmeter", i, "T1", "2.12 Safety & Rigging", "2.12",
                      "X-103 Confined space", "X-103", "2.12 Cross-cutting",
                      "DOC", "Document interpretation", ["OSHA 1910.146"],
                      "docs/source/element-trees-industrial-service-v0.1.md")
        it["media"] = [fname]
        it["s1_state"] = "planned"
        it["s3_percent"] = 5
        it["scenario"] = ("The image shows the pre-entry atmospheric test screen from a 4-gas monitor "
                          "at a permit-required confined space.")
        it["prompt"] = ("Read all four channels from the image and determine whether entry can be "
                        "authorized. Identify any reading outside acceptable entry limits.")
        it["findings_mode"] = "any_per_group"
        it.update(decision=dec, risk=risk, s2_expected=s2, required_findings=rf,
                  required_actions=ra, forbidden=forb)
        items.append(it)

    # --- sling family: 14 items ---
    for i in range(14):
        load = rng.choice([2000, 3000, 4000, 5000, 6000, 8000])
        angle = rng.choice([25, 30, 35, 45, 60])
        tension = load / (2 * math.sin(math.radians(angle)))
        if i % 2 == 0:
            wll = int(math.ceil(tension / 500) * 500 + rng.choice([500, 1000]))
        else:
            wll = int(max(500, math.floor(tension / 500) * 500 - rng.choice([0, 500])))
        overloaded = tension > wll
        too_flat = angle < 30
        dec = "fail" if (overloaded or too_flat) else "pass"
        fname = f"sling_{i:03d}.png"
        render_sling(MEDIA / fname, load, angle, wll)
        it = skeleton("sling", i, "T1", "2.4 Structural & Ironwork", "2.4",
                      "S-301 Rigging configuration", "S-301", "2.4.3 Rigging & Machinery Moving",
                      "ME", "Measurement & estimation", ["ASME B30.9", "OSHA 1926.251"],
                      "docs/source/element-trees-construction-v0.1.md")
        it["media"] = [fname]
        it["s1_state"] = "planned"
        it["s3_percent"] = 0
        it["scenario"] = ("The image shows a two-leg sling arrangement with the load weight, the sling "
                          "angle at the load, and the tagged working load limit of each leg.")
        it["prompt"] = ("Compute the tension in each sling leg from the image, report it in `value` "
                        "(pounds), and judge whether this rigging arrangement may be used for the lift.")
        it["expected_value"] = round(tension)
        it["value_tolerance"] = max(25, round(tension * 0.03))
        it["findings_mode"] = "any_per_group"
        if dec == "pass":
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["within", "below", "under", "acceptable"]],
                      required_actions=[["proceed", "lift", "document"]],
                      forbidden=[["do", "not", "lift"]])
        else:
            key = ["exceeds", "over", "above", "overload"] if overloaded else ["angle", "flat", "30"]
            it.update(decision="fail", risk="critical", s2_expected=[],
                      required_findings=[key],
                      required_actions=[["rerig", "shorten", "longer", "higher", "rated", "stop"]],
                      forbidden=[["proceed", "with", "lift"]])
        items.append(it)

    OUT.write_text(json.dumps(items, indent=2, sort_keys=True), encoding="utf-8")
    from collections import Counter
    print(f"Wrote {len(items)} media items to {OUT}")
    print("decisions:", Counter(i["decision"] for i in items))
    print(f"Rendered {len(list(MEDIA.glob('*.png')))} images in {MEDIA}")


if __name__ == "__main__":
    main()
