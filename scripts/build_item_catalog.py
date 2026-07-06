#!/usr/bin/env python3
"""Build a comprehensive item catalog from the v0.1 taxonomy source docs."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "source"
CURATED_PATH = ROOT / "benchmark" / "items" / "seed_items.json"
CATALOG_PATH = ROOT / "benchmark" / "items" / "items.json"
TAXONOMY_PATH = ROOT / "benchmark" / "taxonomy.json"
COVERAGE_PATH = ROOT / "benchmark" / "coverage_report.md"

TIERS = ["T1", "T2", "T3", "T4", "T5"]
TASK_TYPES = ["ID", "FD", "CC", "SEQ", "TS", "HAZ", "ME", "PA", "DOC", "TRD", "RES"]

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
    "RES": "Resource/constraint recovery",
}

DISCIPLINES = {
    "2.1": "Electrical",
    "2.2": "Mechanical - Piping & Plumbing",
    "2.3": "HVAC-R",
    "2.4": "Structural & Ironwork",
    "2.5": "Concrete & Masonry",
    "2.6": "Carpentry & Finishes",
    "2.7": "Equipment & Machinery",
    "2.8": "Instrumentation & Controls",
    "2.9": "Automotive & Powertrain",
    "2.10": "Assembly & Fabrication",
    "2.11": "Sitework & Utilities",
    "2.12": "Safety & Rigging",
}

PREFIX_TO_DISCIPLINE = {
    "E": "2.1",
    "P": "2.2",
    "H": "2.3",
    "S": "2.4",
    "C": "2.5",
    "F": "2.6",
    "M": "2.7",
    "I": "2.8",
    "A": "2.9",
    "B": "2.10",
    "U": "2.11",
    "X": "2.12",
}

COVERAGE_MATRIX = {
    "2.1": {"T1": "core", "T2": "core", "T3": "core", "T4": "core", "T5": "secondary"},
    "2.2": {"T1": "core", "T2": "core", "T3": "core", "T4": "core", "T5": "secondary"},
    "2.3": {"T1": "secondary", "T2": "core", "T3": "core", "T4": "core", "T5": "out"},
    "2.4": {"T1": "core", "T2": "core", "T3": "secondary", "T4": "out", "T5": "core"},
    "2.5": {"T1": "core", "T2": "core", "T3": "core", "T4": "out", "T5": "out"},
    "2.6": {"T1": "out", "T2": "core", "T3": "core", "T4": "secondary", "T5": "secondary"},
    "2.7": {"T1": "core", "T2": "secondary", "T3": "out", "T4": "core", "T5": "core"},
    "2.8": {"T1": "core", "T2": "secondary", "T3": "out", "T4": "secondary", "T5": "core"},
    "2.9": {"T1": "out", "T2": "out", "T3": "secondary", "T4": "core", "T5": "core"},
    "2.10": {"T1": "secondary", "T2": "out", "T3": "out", "T4": "out", "T5": "core"},
    "2.11": {"T1": "core", "T2": "core", "T3": "secondary", "T4": "secondary", "T5": "out"},
    "2.12": {"T1": "core", "T2": "core", "T3": "core", "T4": "core", "T5": "core"},
}

COVERAGE_TARGETS = {
    "core": 20,
    "secondary": 5,
    "out": 0,
}

S1_BY_TASK_TYPE = {
    "ID": "rough-complete",
    "FD": "in-service",
    "CC": "rough-complete",
    "SEQ": "in-progress",
    "TS": "staged",
    "HAZ": "in-progress",
    "ME": "rough-complete",
    "PA": "rough-complete",
    "DOC": "tested/inspected",
    "TRD": "in-progress",
    "RES": "in-progress",
}

S3_BY_STATE = {
    "planned": 5,
    "staged": 15,
    "in-progress": 45,
    "rough-complete": 70,
    "tested/inspected": 85,
    "rework": 60,
    "accepted": 95,
    "in-service": 100,
}

DEFAULT_MODALITY = "text"
DEFAULT_MEDIA: list[dict] = []

HIGH_RISK_TERMS = [
    "fall",
    "trench",
    "lockout",
    "tagout",
    "hazard",
    "high-voltage",
    "voltage",
    "breaker",
    "bond",
    "combustible",
    "gas",
    "crane",
    "suspended",
    "confined",
    "hot work",
    "fire",
    "pressure",
    "pneumatic",
    "brake",
]

CRITICAL_TERMS = [
    "lockout",
    "tagout",
    "high-voltage",
    "trench",
    "fall protection",
    "confined space",
    "hot work",
    "arc-flash",
    "suspended load",
    "working under",
]

FINDING_STOPWORDS = {
    "from",
    "with",
    "where",
    "that",
    "this",
    "than",
    "into",
    "near",
    "before",
    "after",
    "during",
    "without",
    "within",
    "between",
    "required",
    "visible",
    "photo",
    "item",
    "classic",
    "load",
    "chart",
    "estimate",
}

MASK_TERMS = {
    "missing": "not present where expected",
    "omitted": "left out of the assembly",
    "wrong": "not matching the specified requirement",
    "improper": "not installed in the expected manner",
    "inadequate": "not sufficient for the load or condition",
    "insufficient": "not enough for the requirement",
    "undersized": "smaller than the required size",
    "unsupported": "not held at the expected intervals",
    "unsealed": "left open at the joint or penetration",
    "unbonded": "not electrically tied together",
    "uncapped": "left open at the end",
    "expired": "past the allowed date",
    "exceeded": "beyond the allowed limit",
    "violated": "not following the required order",
    "misread": "interpreted contrary to the marked indication",
    "misused": "used contrary to the expected procedure",
    "mismatch": "does not match the adjacent reference",
    "reversed": "arranged opposite of the expected orientation",
    "backwards": "oriented opposite the reference direction",
}


@dataclass
class Element:
    code: str
    name: str
    discipline_code: str
    discipline: str
    subcategory: str
    tiers: list[str]
    task_fit: list[str]
    defects: list[str]
    refs: list[str]
    notes: list[str]
    source_file: str


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def compact_text(value: str) -> str:
    return " ".join(value.replace("—", "-").replace("–", "-").split())


def parse_tiers(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.lower() == "all":
        return TIERS.copy()
    tiers = []
    for match in re.finditer(r"T[1-5]", raw):
        tier = match.group(0)
        if tier not in tiers:
            tiers.append(tier)
    return tiers


def parse_task_fit(raw: str) -> list[str]:
    task_types = []
    for token in re.split(r"[^A-Z]+", raw):
        if token in TASK_TYPES and token not in task_types:
            task_types.append(token)
    return task_types


def parse_defects(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    return [compact_text(part) for part in re.split(r";", raw) if part.strip()]


def parse_refs(raw: str) -> list[str]:
    return [compact_text(part) for part in re.split(r",|;", raw) if part.strip()]


def discipline_for_code(code: str) -> tuple[str, str]:
    prefix = code.split("-")[0]
    discipline_code = PREFIX_TO_DISCIPLINE[prefix]
    return discipline_code, DISCIPLINES[discipline_code]


def parse_elements() -> list[Element]:
    elements: list[Element] = []
    for path in sorted(SOURCE_DIR.glob("*element*.md")):
        current_subcategory = ""
        lines = path.read_text(encoding="utf-8").splitlines()
        index = 0
        while index < len(lines):
            line = lines[index]
            subcategory_match = re.match(r"^##\s+(.+)", line)
            if subcategory_match:
                current_subcategory = compact_text(subcategory_match.group(1).replace("★", ""))
                index += 1
                continue

            element_match = re.match(r"^###\s+([A-Z]-\d{3})\s+(.+)", line)
            if not element_match:
                index += 1
                continue

            code = element_match.group(1)
            name = compact_text(element_match.group(2).replace("★", ""))
            discipline_code, discipline = discipline_for_code(code)
            block: list[str] = []
            index += 1
            while index < len(lines) and not re.match(r"^###\s+[A-Z]-\d{3}\s+", lines[index]):
                if re.match(r"^##\s+.+", lines[index]):
                    break
                block.append(lines[index])
                index += 1

            tiers: list[str] = []
            task_fit: list[str] = []
            defects: list[str] = []
            refs: list[str] = []
            notes: list[str] = []
            for block_line in block:
                if block_line.startswith("- Tiers:"):
                    tiers_part, _, task_part = block_line.partition("· Task fit:")
                    tiers = parse_tiers(tiers_part.replace("- Tiers:", ""))
                    task_fit = parse_task_fit(task_part)
                elif block_line.startswith("- Defects:"):
                    defects = parse_defects(block_line.replace("- Defects:", "", 1))
                elif block_line.startswith("- Ref:"):
                    refs = parse_refs(block_line.replace("- Ref:", "", 1))
                elif block_line.startswith("- Note:"):
                    notes.append(compact_text(block_line.replace("- Note:", "", 1)))

            if not tiers or not task_fit:
                raise ValueError(f"Could not parse tiers/task fit for {code} in {path}")

            elements.append(
                Element(
                    code=code,
                    name=name,
                    discipline_code=discipline_code,
                    discipline=f"{discipline_code} {discipline}",
                    subcategory=current_subcategory,
                    tiers=tiers,
                    task_fit=task_fit,
                    defects=defects,
                    refs=refs,
                    notes=notes,
                    source_file=str(path.relative_to(ROOT)),
                )
            )
    return elements


def risk_for(element: Element, task_type: str, defect: str) -> str:
    haystack = f"{element.name} {element.subcategory} {defect}".lower()
    if task_type == "HAZ" or any(term in haystack for term in CRITICAL_TERMS):
        return "critical"
    if any(term in haystack for term in HIGH_RISK_TERMS):
        return "high"
    if task_type in {"CC", "FD", "SEQ", "TRD", "RES"}:
        return "high"
    return "medium"


def s2_for(task_type: str) -> list[str]:
    if task_type == "FD":
        return ["degraded", "failed"]
    if task_type == "ID":
        return ["installed-defective"]
    if task_type in {"HAZ", "CC", "TRD", "RES"}:
        return ["installed-defective", "non-compliant"]
    return ["installed-defective"]


def prompt_for(task_type: str) -> str:
    prompts = {
        "ID": "Identify the component or condition shown, and name the visible defect cues.",
        "FD": "Diagnose the most likely fault or failure mode and explain what evidence supports it.",
        "CC": "Determine whether the work meets the applicable code, spec, drawing, or manufacturer requirement.",
        "SEQ": "Evaluate the procedure sequence and state what must happen before work can continue.",
        "TS": "Select the correct tool, material, or replacement approach and explain why the observed choice is wrong.",
        "HAZ": "Identify the safety hazards, their severity, and the immediate controls required.",
        "ME": "Estimate or interpret the measurable condition and state why it is out of tolerance.",
        "PA": "Assess how far along the work is, the percent complete, any defects, and the remaining work.",
        "DOC": "Compare the field condition against the referenced document, tag, drawing, or standard.",
        "TRD": "Resolve the field tradeoff: distinguish common shortcuts from acceptable journeyman practice.",
        "RES": "Assess the disrupted lookahead schedule: what can proceed, what is delayed, and which recovery plan is valid.",
    }
    return prompts[task_type]


def required_terms(element: Element, task_type: str, defect: str) -> list[list[str]]:
    context_terms = {
        word
        for word in re.findall(
            r"[A-Za-z0-9]+",
            f"{element.code} {element.name} {' '.join(element.refs)}".lower(),
        )
        if len(word) >= 4
    }
    seen: set[str] = set()
    defect_terms = [
        word
        for word in re.findall(r"[A-Za-z0-9]+", defect.lower())
        if len(word) >= 4 and word not in FINDING_STOPWORDS and word not in context_terms
    ]
    terms = []
    for term in defect_terms[:3]:
        if term not in seen:
            terms.append([term])
            seen.add(term)
    if not terms:
        terms.append(["defect"])
    return terms[:5]


def mask_finding_terms(text: str, groups: list[list[str]]) -> str:
    """Remove rewarded conclusion tokens from generated scenario text."""
    masked = text
    terms = sorted({term.lower() for group in groups for term in group}, key=len, reverse=True)
    for term in terms:
        replacement = MASK_TERMS.get(term, "visible cue")
        masked = re.sub(rf"\b{re.escape(term)}\b", replacement, masked, flags=re.IGNORECASE)
    return compact_text(masked)


def action_terms(task_type: str) -> list[list[str]]:
    actions = {
        "ID": [["identify"], ["document"], ["inspect"]],
        "FD": [["diagnose"], ["repair"], ["verify"]],
        "CC": [["correct"], ["inspect"], ["before", "acceptance"]],
        "SEQ": [["stop"], ["resequence"], ["verify"]],
        "TS": [["replace"], ["select"], ["verify"]],
        "HAZ": [["stop", "work"], ["control", "hazard"], ["verify"]],
        "ME": [["measure"], ["correct"], ["reinspect"]],
        "PA": [["complete"], ["remaining"], ["reinspect"]],
        "DOC": [["compare"], ["correct"], ["document"]],
        "TRD": [["reject", "shortcut"], ["follow"], ["document"]],
        "RES": [["hold"], ["sequence"], ["verify"]],
    }
    return actions[task_type]


def build_auto_item(element: Element, tier: str, task_type: str, ordinal: int, generation: str = "auto") -> dict:
    defect = element.defects[ordinal % len(element.defects)] if element.defects else f"defective {element.name}"
    s1_state = S1_BY_TASK_TYPE[task_type]
    risk = risk_for(element, task_type, defect)
    item_id = f"{tier.lower()}-{element.code.lower()}-{task_type.lower()}-{slug(element.name)[:32]}"
    source_refs = element.refs or [element.code]
    findings = required_terms(element, task_type, defect)
    observed_condition = mask_finding_terms(defect, findings)
    scenario = (
        f"In a {tier} work setting, the evaluated element is {element.code} {element.name} "
        f"within {element.discipline}. The relevant subcategory is {element.subcategory}. "
        f"The field notes describe visible cues consistent with: {observed_condition}. "
        f"The work is being assessed at the "
        f"{s1_state} lifecycle state with source anchors {', '.join(source_refs)}."
    )
    if task_type == "DOC":
        scenario += " A drawing, inspection checklist, equipment tag, or manufacturer instruction is available for comparison."
    if task_type == "ME":
        scenario += " The measurable cue is visible enough to estimate whether the condition is within tolerance."
    if task_type == "PA":
        scenario += f" Treat this as roughly {S3_BY_STATE[s1_state]} percent complete until defects are corrected."

    return {
        "id": item_id,
        "title": f"{tier} {element.code} {TASK_TYPE_NAMES[task_type]}",
        "tier": tier,
        "discipline": element.discipline,
        "discipline_code": element.discipline_code,
        "subcategory": element.subcategory,
        "element_code": element.code,
        "element": f"{element.code} {element.name}",
        "task_type": task_type,
        "task_type_name": TASK_TYPE_NAMES[task_type],
        "s1_state": s1_state,
        "s2_expected": s2_for(task_type),
        "s3_percent": S3_BY_STATE[s1_state],
        "modality": DEFAULT_MODALITY,
        "media": list(DEFAULT_MEDIA),
        "risk": risk,
        "decision": "fail",
        "scenario": scenario,
        "prompt": prompt_for(task_type),
        "required_findings": findings,
        "required_actions": action_terms(task_type),
        "forbidden": [["pass"], ["accept"], ["safe", "as", "is"]],
        "source_refs": source_refs,
        "source_file": element.source_file,
        "generation": generation,
    }


def build_backfill_item(element: Element, tier: str, task_type: str, ordinal: int, target_status: str) -> dict:
    item = build_auto_item(element, tier, task_type, ordinal, generation="matrix-backfill")
    item["id"] = f"{tier.lower()}-{element.code.lower()}-{task_type.lower()}-bf-{ordinal:03d}-{slug(element.name)[:24]}"
    item["title"] = f"{tier} {element.code} {TASK_TYPE_NAMES[task_type]} coverage backfill"
    item["scenario"] += (
        f" This item is a coverage backfill for a {target_status} taxonomy matrix cell; "
        "validate tier-specific details with an SME before treating it as authoritative."
    )
    return item


def normalize_curated_item(item: dict) -> dict:
    item = dict(item)
    item.setdefault("discipline_code", item.get("discipline", "").split(" ")[0] if item.get("discipline", "").startswith("2.") else "")
    item.setdefault("subcategory", "")
    element = item.get("element", "")
    element_match = re.match(r"([A-Z]-\d{3})", element)
    item.setdefault("element_code", element_match.group(1) if element_match else "")
    item.setdefault("task_type_name", TASK_TYPE_NAMES.get(item["task_type"], item["task_type"]))
    item.setdefault("s3_percent", S3_BY_STATE.get(item["s1_state"], 50))
    item.setdefault("modality", DEFAULT_MODALITY)
    item.setdefault("media", list(DEFAULT_MEDIA))
    item.setdefault("generation", "curated")
    return item


def build_taxonomy(elements: list[Element]) -> dict:
    element_counts = Counter(element.discipline_code for element in elements)
    return {
        "version": "0.1",
        "axes": {
            "tiers": {
                "T1": "Heavy Industrial",
                "T2": "Commercial / Institutional",
                "T3": "Residential / DIY",
                "T4": "Field Service & Maintenance",
                "T5": "Manufacturing / Assembly",
            },
            "disciplines": DISCIPLINES,
            "task_types": TASK_TYPE_NAMES,
            "modalities": {
                "text": "Text-only scenario; scenario text may serve as a future photo shot list.",
                "photo": "Still image fixture.",
                "image": "Still synthetic or real image fixture.",
                "audio": "Audio-only fixture where transcript reduction destroys the item.",
                "video": "Video-only or animation fixture where frame reduction destroys the item.",
                "infrared": "Thermal/IR image fixture.",
                "document": "Drawing, checklist, cut sheet, tag, or other document fixture.",
            },
            "modality_native_task_suffixes": {
                "A": "Audio-native task where sound is the signal.",
                "V": "Video-native task where motion, timing, sequence, or cause-effect is the signal.",
            },
        },
        "item_media_schema": {
            "modality": "Primary item modality. Existing v0.1/v2 generated items use text.",
            "media": "Array of media descriptors with type, path, alt, source, and license fields when fixtures are present.",
            "expected_value": "Optional numeric ground truth for instrument readings or computed visual quantities.",
            "value_tolerance": "Allowed absolute error for expected_value when the task asks for a numeric value.",
            "expected_event_time": "Optional ground-truth timestamp for temporal violations.",
            "event_time_tolerance": "Allowed absolute error for expected_event_time.",
            "expected_rate": "Optional ground-truth rate for dynamic video or audio phenomena.",
            "rate_tolerance": "Allowed absolute error for expected_rate.",
            "expected_order": "Optional expected event/procedure sequence for edit-distance grading.",
            "expected_sound_source": "Optional source/component label for audio-native fault signatures.",
            "confusable_with": "Optional linked item id for deliberate confusable-pair reporting.",
            "reduction_test": "Why transcript/frame reduction cannot preserve the answer.",
        },
        "state_model": {
            "s1_lifecycle": [
                "planned",
                "staged",
                "in-progress",
                "rough-complete",
                "tested/inspected",
                "rework",
                "accepted",
                "in-service",
            ],
            "s2_conditions": [
                "new",
                "installed-correct",
                "installed-defective",
                "non-compliant",
                "worn",
                "degraded",
                "failed",
            ],
            "s3_progress_percent_by_s1": S3_BY_STATE,
        },
        "coverage_matrix": COVERAGE_MATRIX,
        "source_element_counts": dict(sorted(element_counts.items())),
    }


def write_coverage(items: list[dict], elements: list[Element]) -> None:
    by_disc = Counter(item["discipline_code"] for item in items)
    by_tier = Counter(item["tier"] for item in items)
    by_task = Counter(item["task_type"] for item in items)
    by_cell = Counter((item["discipline_code"], item["tier"]) for item in items)
    by_generation = Counter(item.get("generation", "unknown") for item in items)

    lines = [
        "# Blue-Collar Benchmark Coverage Report",
        "",
        f"- Source elements parsed: {len(elements)}",
        f"- Runnable items generated: {len(items)}",
        "",
        "## By Generation",
        "",
        "| Generation | Items |",
        "|---|---:|",
    ]
    for generation, count in sorted(by_generation.items()):
        lines.append(f"| {generation} | {count} |")

    lines.extend(
        [
        "",
        "## By Discipline",
        "",
        "| Discipline | Items | Source elements |",
        "|---|---:|---:|",
        ]
    )
    element_counts = Counter(element.discipline_code for element in elements)
    for code, name in DISCIPLINES.items():
        lines.append(f"| {code} {name} | {by_disc[code]} | {element_counts[code]} |")

    lines.extend(["", "## By Tier", "", "| Tier | Items |", "|---|---:|"])
    for tier in TIERS:
        lines.append(f"| {tier} | {by_tier[tier]} |")

    lines.extend(["", "## By Task Type", "", "| Task type | Items |", "|---|---:|"])
    for task_type in TASK_TYPES:
        lines.append(f"| {task_type} {TASK_TYPE_NAMES[task_type]} | {by_task[task_type]} |")

    lines.extend(
        [
            "",
            "## Coverage Matrix",
            "",
            "Counts are generated items in each Tier x Discipline cell. Matrix status follows the v0.1 taxonomy: core, secondary, or out of scope.",
            "Targets: core >=20 items, secondary >=5 items, out = 0 required items.",
            "",
            "| Discipline | T1 | T2 | T3 | T4 | T5 |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for code, name in DISCIPLINES.items():
        cells = []
        for tier in TIERS:
            status = COVERAGE_MATRIX[code][tier]
            count = by_cell[(code, tier)]
            cells.append(f"{count} ({status})")
        lines.append(f"| {code} {name} | " + " | ".join(cells) + " |")

    under_target = []
    for code, tier_status in COVERAGE_MATRIX.items():
        for tier, status in tier_status.items():
            target = COVERAGE_TARGETS[status]
            if target and by_cell[(code, tier)] < target:
                under_target.append(f"{code} {DISCIPLINES[code]} x {tier}: {by_cell[(code, tier)]}/{target}")

    lines.extend(["", "## Gaps", ""])
    if under_target:
        lines.extend(f"- Under target: {cell}" for cell in under_target)
    else:
        lines.append("- No core or secondary Tier x Discipline cell is under target.")

    COVERAGE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_catalog() -> list[dict]:
    elements = parse_elements()
    auto_items = []
    for element in elements:
        for tier in element.tiers:
            for ordinal, task_type in enumerate(element.task_fit):
                auto_items.append(build_auto_item(element, tier, task_type, ordinal))

    curated_items = []
    if CURATED_PATH.exists():
        curated_items = [normalize_curated_item(item) for item in json.loads(CURATED_PATH.read_text(encoding="utf-8"))]

    items = curated_items + auto_items
    by_disc_elements = defaultdict(list)
    for element in elements:
        by_disc_elements[element.discipline_code].append(element)

    by_cell = Counter((item["discipline_code"], item["tier"]) for item in items)
    backfill_items = []
    for discipline_code, tier_status in COVERAGE_MATRIX.items():
        discipline_elements = by_disc_elements[discipline_code]
        if not discipline_elements:
            continue
        for tier, status in tier_status.items():
            target = COVERAGE_TARGETS[status]
            current = by_cell[(discipline_code, tier)]
            ordinal = 0
            while current < target:
                element = discipline_elements[ordinal % len(discipline_elements)]
                task_type = element.task_fit[ordinal % len(element.task_fit)]
                item = build_backfill_item(element, tier, task_type, ordinal, status)
                backfill_items.append(item)
                by_cell[(discipline_code, tier)] += 1
                current += 1
                ordinal += 1

    items = items + backfill_items

    seen = set()
    normalized_items = []
    for item in items:
        if item["id"] in seen:
            raise ValueError(f"Duplicate item id: {item['id']}")
        seen.add(item["id"])
        normalized_items.append(item)

    items = normalized_items
    CATALOG_PATH.write_text(json.dumps(items, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    TAXONOMY_PATH.write_text(json.dumps(build_taxonomy(elements), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_coverage(items, elements)
    return items


def main() -> int:
    items = build_catalog()
    print(f"Wrote {len(items)} items to {CATALOG_PATH}")
    print(f"Wrote taxonomy to {TAXONOMY_PATH}")
    print(f"Wrote coverage report to {COVERAGE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
