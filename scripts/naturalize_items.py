#!/usr/bin/env python3
"""naturalize_items — rewrite the merged catalog into standalone, natural language.

The raw generators emit items whose ids, titles, and scenario wrappers are
written in internal taxonomy shorthand ("In a T2 work setting, the evaluated
element is E-101 ... within 2.1 Electrical", titles like "T2 E-101 Code/spec
compliance", ids like "t1-c-101-haz-bf-000-form-build-bracing"). A model that
sees one task cold has no way to interpret those codes, and several titles
even leak the expected decision ("Compliant ... (control)", "alarmist trap").

This stage runs inside generate_tasks_v2 after scenario restoration and
before the leakage audit. It:
  1. Rebuilds coded scenario wrappers into plain field language, preserving
     the observed-evidence text verbatim.
  2. Rewrites coded or decision-leaking titles from the item's own fields.
  3. Replaces coded ids with readable slugs plus a short stable hash of the
     legacy id, keeps the old id in `legacy_id`, and writes
     benchmark/items/id_map.json for joining older runs.
  4. Drops internal source refs (element codes, expansion-plan notes) from
     model-visible text while leaving `source_refs` metadata intact.
  5. Fails loudly if any taxonomy shorthand survives in model-visible text.

Idempotent: items that already carry `legacy_id` are left alone.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "benchmark" / "items" / "items.json"
ID_MAP = ROOT / "benchmark" / "items" / "id_map.json"

TIER_SETTING = {
    "T1": "a heavy-industrial construction or process site where work follows engineered drawings, specifications, and permits",
    "T2": "a commercial construction project governed by building codes, submittals, and third-party inspections",
    "T3": "a residential job — a service call, remodel, or homeowner installation with prescriptive code and manufacturer instructions",
    "T4": "a field-service visit to an installed, operating asset, working from symptoms, the work order, and OEM service information",
    "T5": "a manufacturing or assembly floor running standard work with quality gates",
}

TIER_SHORT = {
    "T1": "industrial site",
    "T2": "commercial project",
    "T3": "residential job",
    "T4": "service call",
    "T5": "production floor",
}

TIER_ID_WORD = {
    "T1": "industrial",
    "T2": "commercial",
    "T3": "residential",
    "T4": "service",
    "T5": "production",
}

TASK_PHRASE = {
    "ID": "identify the component, material, or condition involved",
    "FD": "diagnose the most likely fault from the evidence",
    "CC": "decide whether the work complies with the applicable code, specification, or manufacturer requirements",
    "SEQ": "check the order of the work and catch any sequence violation",
    "TS": "choose the correct tool, material, or method for the job",
    "HAZ": "spot the unsafe conditions and state the immediate controls required",
    "ME": "read or estimate the relevant measurement and judge whether it is within tolerance",
    "PA": "assess how far along the work is, what is defective, and what remains",
    "DOC": "compare the work against the controlling document",
    "TRD": "choose the practical, compliant course of action given the field constraints",
    "RES": "decide what work can proceed, what is blocked, and what recovery plan is valid",
}

TASK_TITLE_WORD = {
    "ID": "Identification",
    "FD": "Fault diagnosis",
    "CC": "Compliance check",
    "SEQ": "Sequence check",
    "TS": "Tool and material selection",
    "HAZ": "Hazard check",
    "ME": "Measurement check",
    "PA": "Progress assessment",
    "DOC": "Document check",
    "TRD": "Judgment call",
    "RES": "Recovery planning",
}

S1_PHRASE = {
    "planned": "scoped but not yet started",
    "staged": "staged — materials, tools, and access are ready, but work has not begun",
    "in-progress": "actively in progress",
    "rough-complete": "roughed in — installed or assembled, but not yet closed out",
    "tested/inspected": "through its testing or inspection step",
    "rework": "in rework after a failed verification",
    "accepted": "accepted and signed off",
    "in-service": "in service as an operating asset",
}

# Titles for the hand-authored v2 control/NMI/trap/tradeoff items, keyed by
# legacy id. The originals name their own expected outcome ("Compliant ...
# (control)", "(alarmist trap)", "unverifiable"), which both leaks the answer
# and reads as internal bookkeeping.
CURATED_TITLE_OVERRIDES = {
    "v2-pass-e102-t3-subpanel-correct": "Subpanel makeup inspection",
    "v2-pass-p102-t1-flange-correct": "Flanged joint closure inspection",
    "v2-pass-h301-t4-evacuation-correct": "Brazing and evacuation review",
    "v2-pass-s102-t2-bolting-correct": "Structural bolting inspection",
    "v2-pass-a201-t4-brakes-correct": "Brake service check",
    "v2-pass-u101-t2-trench-correct": "Trench protection review",
    "v2-pass-m201-t1-alignment-correct": "Shaft alignment review",
    "v2-pass-x102-t2-harness-correct": "Fall protection review",
    "v2-nmi-e303-t2-termination-torque": "Feeder termination acceptance",
    "v2-nmi-p201-t3-concealed-vent": "Drain vent path assessment",
    "v2-nmi-a301-t4-p0420-diagnosis": "Catalyst efficiency code diagnosis",
    "v2-nmi-x103-t1-incomplete-gas-test": "Confined-space atmosphere review",
    "v2-nmi-s201-t2-bar-size-unconfirmed": "Rebar size verification",
    "v2-trap-f301-t3-screw-pops": "Drywall screw pops assessment",
    "v2-trap-a102-t4-oil-seep": "Valve cover seep assessment",
    "v2-trap-c301-t2-efflorescence": "Masonry efflorescence assessment",
    "v2-trd-e303-t3-backstab": "Backstabbed receptacles decision",
    "v2-trd-a302-t4-adas-skip": "ADAS calibration decision",
    "v2-trd-b101-t5-tty-reuse": "Torque-to-yield bolt reuse decision",
    "v2-trd-s302-t1-wind-pick": "Crane pick in gusty wind decision",
    "v2-trd-x102-t2-guardrail-tieoff": "Guardrail anchor decision",
}

REBUILT_SCENARIO_GENERATIONS = {"auto", "matrix-backfill"}

# Single-letter prefix distinguishes internal element codes (P-201, X-103)
# from real standards that look similar (TIA-568, GA-216).
ELEMENT_CODE_RE = re.compile(r"^[A-Z]-\d{3}$")

AUTO_WRAPPER_RE = re.compile(
    r"^In a (?P<tier>T\d) work setting, the evaluated element is "
    r"(?P<elcode>[A-Z]-\d{3}) .+? within .+?\. "
    r"The relevant subcategory is .+?\. "
    r"(?:The observed field condition is:|The field notes describe visible cues consistent with:) "
    r"(?P<obs>.+?) "
    r"The work is being assessed at the ",
    re.S,
)

# Task-type extras appended after the closer sentence; the closer itself
# ("... lifecycle state with source anchors <refs>.") is discarded because the
# refs contain periods (e.g. "NEC Art. 230") and are rebuilt from source_refs.
AUTO_EXTRA_RES = [
    re.compile(r"A drawing, inspection checklist, equipment tag, or manufacturer instruction is available for comparison\."),
    re.compile(r"The measurable cue is visible enough to estimate whether the condition is within tolerance\."),
    re.compile(r"Treat this as roughly \d+ percent complete until defects are corrected\."),
]

LEFTOVER_CODE_RE = re.compile(
    r"\b(?:T[1-5]|[A-Z]-\d{3}|2\.\d{1,2}(?:\.\d+)?|bf-\d{3})\b|taxonomy|matrix cell|lifecycle state"
)


def slug(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", text)


def short_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:6]


def element_name(item: dict) -> str:
    return re.sub(r"^(?:[A-Z]-\d{3}|RES)\s+", "", item.get("element", "")).strip()


def discipline_name(item: dict) -> str:
    name = re.sub(r"^2\.\d{1,2}\s+", "", item.get("discipline", "")).strip()
    # "Mechanical - Piping & Plumbing" -> "Piping & Plumbing"
    if " - " in name:
        name = name.split(" - ", 1)[1]
    return name


def is_internal_ref(ref: str) -> bool:
    return bool(
        ELEMENT_CODE_RE.fullmatch(ref.strip())
        or "expansion-plan" in ref
        or "computed ground truth" in ref
    )


def external_refs(item: dict) -> list[str]:
    return [ref for ref in item.get("source_refs", []) if not is_internal_ref(ref)]


def natural_title(item: dict) -> str:
    legacy = item["id"]
    if legacy in CURATED_TITLE_OVERRIDES:
        base = CURATED_TITLE_OVERRIDES[legacy]
    else:
        generation = item.get("generation", "")
        base = f"{TASK_TITLE_WORD[item['task_type']]}: {element_name(item)}"
        if generation == "synthetic-cpm-v2":
            base = "Schedule impact assessment"
    qualifiers = []
    if item.get("modality") == "image":
        qualifiers.append("photo")
    elif item.get("modality") == "audio":
        qualifiers.append("audio")
    qualifiers.append(TIER_SHORT[item["tier"]])
    return f"{base} ({', '.join(qualifiers)})"


def natural_id(item: dict, title: str) -> str:
    base = re.sub(r"\s*\([^)]*\)", "", title)  # drop parenthetical qualifiers
    words = slug(f"{base}-{TIER_ID_WORD[item['tier']]}")[:56].strip("-")
    return f"{words}-{short_hash(item['id'])}"


def refs_sentence(item: dict) -> str:
    refs = external_refs(item)
    return f" Reference material on hand: {', '.join(refs)}." if refs else ""


def rebuild_auto_scenario(item: dict) -> str:
    match = AUTO_WRAPPER_RE.match(item["scenario"])
    if not match:
        raise ValueError(f"unexpected auto scenario shape for {item['id']}: {item['scenario'][:120]!r}")
    # Source element trees occasionally annotate defects with taxonomy
    # shorthand like "pipe boot cracked (T4 FD)" — strip those parentheticals.
    observed = re.sub(r"\s*\(T[1-5][^)]*\)", "", match.group("obs")).strip()
    tail = item["scenario"][match.end():]
    rest = " ".join(m.group(0) for pattern in AUTO_EXTRA_RES for m in [pattern.search(tail)] if m)
    s1 = S1_PHRASE.get(item.get("s1_state", ""), item.get("s1_state", ""))
    scenario = (
        f"You are on {TIER_SETTING[item['tier']]}. "
        f"The work under review is {element_name(item)}, part of the {discipline_name(item)} scope. "
        f"The observed field condition is: {observed} "
        f"The work is {s1}.{refs_sentence(item)}"
    )
    if rest:
        scenario += f" {rest}"
    return scenario


def rewrite_text_rebalance_scenario(item: dict) -> str:
    scenario = item["scenario"]
    code = item.get("element_code", "")
    if code:
        scenario = scenario.replace(f"{code} ", "")
    scenario = re.sub(r"\s*Source anchors for review: .+?\.$", "", scenario, flags=re.S)
    return scenario + refs_sentence(item)


def naturalize_item(item: dict) -> dict:
    if item.get("legacy_id"):
        return item
    item = dict(item)
    legacy = item["id"]
    item["legacy_id"] = legacy

    generation = item.get("generation", "")
    if generation in REBUILT_SCENARIO_GENERATIONS:
        item["scenario"] = rebuild_auto_scenario(item)
    elif generation == "synthetic-text-rebalance-v2":
        item["scenario"] = rewrite_text_rebalance_scenario(item)

    if generation != "curated":  # hand-authored seeds are already natural
        item["title"] = natural_title(item)
        item["id"] = natural_id(item, item["title"])
    return item


def scan_for_codes(items: list[dict]) -> list[str]:
    offenders = []
    for item in items:
        for field in ("title", "scenario", "prompt"):
            text = item.get(field) or ""
            hit = LEFTOVER_CODE_RE.search(text)
            if hit:
                offenders.append(f"{item['id']} {field}: ...{text[max(0, hit.start() - 40):hit.end() + 40]}...")
    return offenders


def main() -> None:
    items = json.loads(ITEMS.read_text(encoding="utf-8"))
    naturalized = [naturalize_item(item) for item in items]

    ids = [item["id"] for item in naturalized]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"duplicate naturalized ids: {sorted(dupes)[:10]}")

    offenders = scan_for_codes(naturalized)
    if offenders:
        listing = "\n".join(offenders[:20])
        raise SystemExit(f"{len(offenders)} items still contain taxonomy shorthand:\n{listing}")

    ITEMS.write_text(json.dumps(naturalized, indent=2, sort_keys=True), encoding="utf-8")
    id_map = {item["legacy_id"]: item["id"] for item in naturalized}
    ID_MAP.write_text(json.dumps(id_map, indent=2, sort_keys=True), encoding="utf-8")
    renamed = sum(1 for item in naturalized if item["id"] != item["legacy_id"])
    print(f"Naturalized {len(naturalized)} items ({renamed} renamed); id map at {ID_MAP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
