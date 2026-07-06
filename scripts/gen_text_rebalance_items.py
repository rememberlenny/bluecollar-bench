#!/usr/bin/env python3
"""Generate text-only pass/NMI controls to rebalance catalog decisions.

The original generated catalog is intentionally defect-heavy. This v2 text
slice adds compliant and insufficient-information cases across the existing
taxonomy, with extra weight on PA and TRD because those are benchmark-defining
task types and were underrepresented in the fail-only corpus.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_item_catalog as catalog  # noqa: E402

OUT = ROOT / "benchmark" / "items" / "text_rebalance_items_v2.json"

TARGETS_BY_TASK_TYPE = {
    "PA": 45,
    "TRD": 49,
    "TS": 30,
    "HAZ": 20,
    "ID": 20,
    "CC": 20,
    "SEQ": 20,
    "DOC": 20,
    "ME": 14,
    "FD": 12,
}

PASS_FINDINGS = {
    "ID": [["recognized"], ["serviceable"], ["undamaged"]],
    "FD": [["normal"], ["serviceable"], ["release"]],
    "CC": [["conforming"], ["ready"], ["acceptance"]],
    "SEQ": [["sequenced"], ["prerequisites"], ["ready"]],
    "TS": [["suitable"], ["compatible"], ["approved"]],
    "HAZ": [["controlled"], ["authorized"], ["protected"]],
    "ME": [["tolerance"], ["verified"], ["acceptable"]],
    "PA": [["milestone"], ["substantially"], ["ready"]],
    "DOC": [["traceable"], ["consistent"], ["approved"]],
    "TRD": [["permissible"], ["preference"], ["document"]],
}

NMI_FINDINGS = {
    "ID": [["unverified"], ["obscured"], ["confirm"]],
    "FD": [["unverified"], ["ambiguous"], ["test"]],
    "CC": [["unverified"], ["missing", "record"], ["confirm"]],
    "SEQ": [["unverified"], ["sequence", "unknown"], ["confirm"]],
    "TS": [["unverified"], ["specification", "missing"], ["confirm"]],
    "HAZ": [["unverified"], ["exposure", "unknown"], ["confirm"]],
    "ME": [["unverified"], ["measurement", "missing"], ["confirm"]],
    "PA": [["unverified"], ["quantity", "unknown"], ["confirm"]],
    "DOC": [["unverified"], ["document", "missing"], ["confirm"]],
    "TRD": [["unverified"], ["constraint", "unknown"], ["confirm"]],
}

PASS_ACTIONS = {
    "HAZ": [["monitor"], ["document"]],
    "TRD": [["document"], ["proceed"]],
    "PA": [["document"], ["release"]],
}

PASS_SCENARIOS = {
    "ID": (
        "A field review of {element} shows the expected unit in the intended location. "
        "Nameplates and orientation marks can be read, the housing and adjacent work show no damage, "
        "and the item matches the referenced detail for this stage."
    ),
    "FD": (
        "{element} is observed during operation after the reported concern was checked. "
        "Readings are steady, no abnormal sound or heat is noted, and the maintenance log shows the "
        "standard functional check was completed with no open punch note."
    ),
    "CC": (
        "Closeout photos for {element} show the installed work following the referenced detail. "
        "Clearances, labels, supports, and terminations shown for this element are in place, and the "
        "inspection card has no open correction note."
    ),
    "SEQ": (
        "The crew log for {element} shows the required preparatory steps finished before the current operation. "
        "Hold points are signed, materials are staged in order, and no skipped step is visible in the photo set."
    ),
    "TS": (
        "The selected tool and material package for {element} matches the size, rating, and application shown on "
        "the referenced sheet. The staged parts are clean, intact, and sized for the work shown."
    ),
    "HAZ": (
        "Pre-task photos for {element} show the exposure area set up with the planned guards, access control, "
        "and crew protection in place. The daily briefing form is signed and no active exposure is visible."
    ),
    "ME": (
        "The measurement record for {element} shows the as-left reading inside the posted limit. "
        "The gauge or scale is readable, the setup is stable, and the same value is entered on the inspection form."
    ),
    "PA": (
        "Progress photos for {element} show the current checkpoint scope finished for this area. "
        "The remaining visible work is cleanup, labeling, or follow-on finish work outside the checkpoint being scored."
    ),
    "DOC": (
        "The field condition for {element} is compared with the referenced drawing or manufacturer sheet. "
        "Tags, ratings, and layout callouts line up with the installed work, and the revision block shown is current."
    ),
    "TRD": (
        "A crew used a field method for {element} that is less tidy than the preferred shop approach but still "
        "matches the listed product instructions and the project requirement. No local amendment or drawing note forbids it."
    ),
}

NMI_SCENARIOS = {
    "ID": (
        "The only photo of {element} is blocked by packaging and glare. The visible outline suggests the right area, "
        "but the identifying mark and connection details cannot be read from the provided evidence."
    ),
    "FD": (
        "{element} is reported as intermittent, but the clip starts after the symptom has stopped. No trend log, "
        "load reading, or repeat test is included, so the failure mode cannot be separated from normal cycling."
    ),
    "CC": (
        "The work around {element} is photographed from one angle only. The critical label, torque sheet, or clearance "
        "dimension needed for the referenced requirement is outside the frame."
    ),
    "SEQ": (
        "The current photo set for {element} shows the work after a hold point, but the earlier prerequisite step is not "
        "shown and no signoff page is attached."
    ),
    "TS": (
        "Parts for {element} are staged in sealed packaging with the rating side turned away. The drawing calls for a "
        "specific size or class, but the submitted evidence does not show that marking."
    ),
    "HAZ": (
        "The view of {element} cuts off the area where the exposure control would be visible. The crew location and "
        "energy or fall-protection boundary cannot be determined from the provided frame."
    ),
    "ME": (
        "A gauge is shown near {element}, but the needle and scale are out of focus. The work order references a limit, "
        "yet no readable value or second measurement is provided."
    ),
    "PA": (
        "Photos of {element} show several completed pieces, but the area count and remaining scope are not listed. "
        "The submitted package does not include the quantity takeoff needed to score the checkpoint."
    ),
    "DOC": (
        "The field photo for {element} is paired with a cropped sheet excerpt. The title block, revision, and matching "
        "callout are not visible, so the installed condition cannot be tied to the controlling page."
    ),
    "TRD": (
        "The crew proposes a shortcut for {element}, but the submittal omits the product listing page and project note "
        "that would decide whether the shortcut is allowed here."
    ),
}


def source_refs_for(element: catalog.Element) -> list[str]:
    return element.refs or [element.code]


def scenario_for(element: catalog.Element, task_type: str, decision: str) -> str:
    templates = PASS_SCENARIOS if decision == "pass" else NMI_SCENARIOS
    return (
        templates[task_type].format(element=f"{element.code} {element.name}")
        + f" Source anchors for review: {', '.join(source_refs_for(element))}."
    )


def build_item(element: catalog.Element, tier: str, task_type: str, index: int, decision: str) -> dict:
    short_decision = "nmi" if decision == "needs_more_info" else decision
    item_id = f"v2-text-{short_decision}-{task_type.lower()}-{tier.lower()}-{element.code.lower()}-{index:03d}"
    risk = "low" if decision == "pass" else ("high" if task_type == "HAZ" else "medium")
    findings = PASS_FINDINGS[task_type] if decision == "pass" else NMI_FINDINGS[task_type]
    actions = PASS_ACTIONS.get(task_type, [["document"], ["release"]]) if decision == "pass" else [["request"], ["verify"], ["document"]]
    return {
        "id": item_id,
        "title": f"{tier} {element.code} {'Compliant' if decision == 'pass' else 'Insufficient evidence'} {catalog.TASK_TYPE_NAMES[task_type]}",
        "tier": tier,
        "discipline": element.discipline,
        "discipline_code": element.discipline_code,
        "subcategory": element.subcategory,
        "element_code": element.code,
        "element": f"{element.code} {element.name}",
        "task_type": task_type,
        "task_type_name": catalog.TASK_TYPE_NAMES[task_type],
        "s1_state": catalog.S1_BY_TASK_TYPE[task_type],
        "s2_expected": [],
        "s3_percent": 90 if decision == "pass" else 50,
        "modality": "text",
        "media": [],
        "risk": risk,
        "decision": decision,
        "scenario": scenario_for(element, task_type, decision),
        "prompt": "Evaluate the described field condition and return the appropriate decision with supporting observations.",
        "required_findings": findings,
        "required_actions": actions,
        "forbidden": [["stop", "work"], ["rework"], ["reject"]] if decision == "pass" else [["guess"], ["accept", "as", "is"]],
        "source_refs": source_refs_for(element),
        "source_file": element.source_file,
        "generation": "synthetic-text-rebalance-v2",
        "findings_mode": "all",
    }


def main() -> None:
    elements = catalog.parse_elements()
    combos: dict[str, list[tuple[catalog.Element, str]]] = {task_type: [] for task_type in TARGETS_BY_TASK_TYPE}
    for element in elements:
        for task_type in element.task_fit:
            if task_type not in combos:
                continue
            for tier in element.tiers:
                combos[task_type].append((element, tier))

    items: list[dict] = []
    for task_type, target in TARGETS_BY_TASK_TYPE.items():
        task_combos = sorted(combos[task_type], key=lambda pair: (pair[1], pair[0].discipline_code, pair[0].code))
        if not task_combos:
            raise RuntimeError(f"No source combinations for {task_type}")
        for index in range(target):
            element, tier = task_combos[index % len(task_combos)]
            decision = "needs_more_info" if index % 4 == 3 else "pass"
            items.append(build_item(element, tier, task_type, index, decision))

    OUT.write_text(json.dumps(items, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {len(items)} text rebalance items to {OUT}")


if __name__ == "__main__":
    main()
