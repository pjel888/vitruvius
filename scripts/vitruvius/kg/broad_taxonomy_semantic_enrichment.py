from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PLACEHOLDER_SUFFIXES = (
    " Concepts",
    " Concept Anchor",
    " Rule Context",
    " Topics",
)
GENERATION_METHOD = (
    "steward_governed_real_broad_taxonomy_semantic_enrichment_from_public_"
    "engineering_code_curriculum_practice_and_operations_topic_structures"
)
SCOPE_NOTE = (
    "Broad AEC-MEPFS semantic enrichment synthesized from public accreditation, "
    "engineering handbook topic structures, code-family headings, professional practice, "
    "operations, and local filename signals; labels and metadata only, no protected source payloads."
)
STOPWORDS = {"and", "of", "the", "for", "to", "in", "with", "a", "an", "or"}
TARGET_CHILDREN_PER_NON_ARCH_PARENT = 5
BROAD_POPULATION_EXCLUDED_NODE_KINDS = {
    "commissioning_overlay",
    "semantic_overlay",
    "semantic_overlay_parent",
    "standard_family",
    "standard_reference",
}
BROAD_POPULATION_EXCLUDED_GENERATION_METHODS = {
    # Project-evidence bridge nodes are intentionally sparse anchors for
    # person/work/material reasoning.  Broad fallback population would add
    # generic compliance children under them and dilute the source-backed
    # evidence paths they were created to preserve.
    "steward_governed_architecture_interconnectivity_from_kimi_guided_materials_people_works_and_source_safe_public_references",
}

# Root-specific phrase templates. The parent L3 label is deliberately embedded in
# every label so each generated node is a concrete semantic child of its parent,
# not a generic detached placeholder like "Concepts" or "Rule Context".
ROOT_TEMPLATES: dict[str, list[str]] = {
    "ACC": [
        "{base} User Need Assessment",
        "{base} Dimensional Clearance Criteria",
        "{base} Assistive Interface Coordination",
        "{base} Inspection And Acceptance Checks",
        "{base} Inclusive Wayfinding Detail",
    ],
    "CIV": [
        "{base} Design Criteria",
        "{base} Construction Tolerance Controls",
        "{base} Drainage And Service Interface",
        "{base} Inspection And Testing Points",
        "{base} Maintenance Access Requirements",
    ],
    "COM": [
        "{base} Applicability Determination",
        "{base} Submission Evidence Package",
        "{base} Authority Review Workflow",
        "{base} Inspection Trigger Points",
        "{base} Variance Or Alternative Compliance Path",
    ],
    "CON": [
        "{base} Method Statement Requirements",
        "{base} Sequencing And Access Controls",
        "{base} Quality Hold Points",
        "{base} Temporary Works Interface",
        "{base} Handover Acceptance Evidence",
    ],
    "DIG": [
        "{base} Information Requirement Definition",
        "{base} Common Data Environment Workflow",
        "{base} Model Exchange Validation",
        "{base} Metadata And Classification Rules",
        "{base} Asset Information Handover",
    ],
    "ELE": [
        "{base} Load And Demand Basis",
        "{base} Circuiting And Protection Coordination",
        "{base} Equipment Schedule Requirements",
        "{base} Testing And Commissioning Procedure",
        "{base} Maintenance Isolation Strategy",
    ],
    "FIG": [
        "{base} Biographical Context",
        "{base} Major Work Attribution",
        "{base} Influence Network Mapping",
        "{base} Practice Or Institution Role",
        "{base} Citation And Source Trace",
    ],
    "FLS": [
        "{base} Hazard Scenario Basis",
        "{base} Detection And Notification Interface",
        "{base} Suppression Or Control Strategy",
        "{base} Egress And Tenability Coordination",
        "{base} Inspection Testing Maintenance Record",
    ],
    "GEO": [
        "{base} Site Investigation Parameters",
        "{base} Design Assumption Controls",
        "{base} Instrumentation And Monitoring Points",
        "{base} Construction Risk Mitigation",
        "{base} Long Term Performance Review",
    ],
    "HIS": [
        "{base} Chronology And Periodization",
        "{base} Regional Transmission Path",
        "{base} Typology And Precedent Examples",
        "{base} Material Culture And Craft Evidence",
        "{base} Interpretation And Historiography",
    ],
    "HRC": [
        "{base} Significance Assessment",
        "{base} Fabric Condition Mapping",
        "{base} Intervention Compatibility Review",
        "{base} Documentation And Archival Record",
        "{base} Maintenance And Monitoring Plan",
    ],
    "LAW": [
        "{base} Jurisdiction And Applicability",
        "{base} Permit Or Approval Trigger",
        "{base} Responsible Party Obligation",
        "{base} Compliance Evidence Record",
        "{base} Enforcement And Remedy Path",
    ],
    "MAT": [
        "{base} Material Properties And Limits",
        "{base} Substrate Compatibility",
        "{base} Installation And Curing Conditions",
        "{base} Fire Moisture And Durability Checks",
        "{base} Maintenance And Replacement Cycle",
    ],
    "MEC": [
        "{base} Load Calculation Basis",
        "{base} Equipment Selection Criteria",
        "{base} Distribution And Zoning Strategy",
        "{base} Controls And Sensor Interface",
        "{base} Commissioning And Balancing Procedure",
    ],
    "OPS": [
        "{base} Asset Register Fields",
        "{base} Preventive Maintenance Schedule",
        "{base} Work Order Response Workflow",
        "{base} Condition Assessment Metrics",
        "{base} Lifecycle Renewal Trigger",
    ],
    "PER": [
        "{base} Performance Target Definition",
        "{base} Simulation Or Calculation Method",
        "{base} Field Measurement Protocol",
        "{base} Comfort Safety Or Resilience Threshold",
        "{base} Post Occupancy Feedback Loop",
    ],
    "PLS": [
        "{base} Fixture Or Demand Unit Basis",
        "{base} Pipe Sizing And Routing Criteria",
        "{base} Backflow Venting Or Trap Protection",
        "{base} Testing Flushing And Disinfection Procedure",
        "{base} Maintenance Access And Isolation",
    ],
    "SAN": [
        "{base} Public Health Risk Pathway",
        "{base} Collection And Conveyance Criteria",
        "{base} Treatment Process Interface",
        "{base} Monitoring And Sampling Protocol",
        "{base} Residuals Or Waste Handling Plan",
    ],
    "SEC": [
        "{base} Threat And Vulnerability Basis",
        "{base} Device Placement Criteria",
        "{base} Power Network And Data Interface",
        "{base} Monitoring Response Workflow",
        "{base} Privacy Retention And Audit Control",
    ],
    "SMS": [
        "{base} Device Identity And Provisioning",
        "{base} Sensor Actuator Data Model",
        "{base} Automation Logic And Overrides",
        "{base} Cybersecurity And Access Control",
        "{base} Lifecycle Firmware And Support Plan",
    ],
    "STR": [
        "{base} Load Path Behavior",
        "{base} Member Sizing Criteria",
        "{base} Connection And Detailing Requirements",
        "{base} Serviceability And Deflection Checks",
        "{base} Inspection And Retrofit Considerations",
    ],
    "SUS": [
        "{base} Baseline And Boundary Definition",
        "{base} Reduction Strategy",
        "{base} Measurement And Verification Method",
        "{base} Co Benefit And Trade Off Review",
        "{base} Reporting And Certification Evidence",
    ],
    "URB": [
        "{base} Spatial Policy Objective",
        "{base} Network And Access Pattern",
        "{base} Public Realm Performance Criteria",
        "{base} Development Control Parameter",
        "{base} Implementation And Phasing Tool",
    ],
}


def _slug_suffix(label: str, used: set[str]) -> str:
    tokens = [re.sub(r"[^A-Za-z0-9]", "", t).upper() for t in label.split()]
    tokens = [t for t in tokens if t and t.lower() not in STOPWORDS and t[0].isalpha()]
    base = "".join(t[0] for t in tokens[:3])
    if len(base) < 3:
        base = re.sub(r"[^A-Z]", "", (base + "".join(tokens)))[:3]
    base = (base + "XXX")[:3]
    suffix = base
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = 0
    while suffix in used:
        suffix = (base[:2] + alphabet[i % 26])[:3]
        i += 1
        if i > 26:
            suffix = f"{base[0]}{i:02d}"[-3:]
    used.add(suffix)
    return suffix


def _is_broad_population_parent(record: dict[str, Any]) -> bool:
    path_code = record.get("path_code", "")
    if record.get("level") != 3:
        return False
    if record.get("interconnectivity_category") == "materials_taxonomy":
        return False
    if not isinstance(path_code, str) or path_code.startswith("ARC."):
        return False
    if path_code.split(".")[0] not in ROOT_TEMPLATES:
        return False
    if record.get("semantic_node_kind") in BROAD_POPULATION_EXCLUDED_NODE_KINDS:
        return False
    return record.get("generation_method") not in BROAD_POPULATION_EXCLUDED_GENERATION_METHODS


def _topics_for(parent: dict[str, Any]) -> list[str]:
    root = parent["path_code"].split(".")[0]
    templates = ROOT_TEMPLATES[root]
    base = parent["label"]
    return [template.format(base=base) for template in templates[:TARGET_CHILDREN_PER_NON_ARCH_PARENT]]


def _make_record(parent: dict[str, Any], suffix: str, label: str, next_id: int) -> dict[str, Any]:
    node_id = f"VTN-DOM-{next_id:07d}"
    parent_label = parent["label"]
    root = parent["path_code"].split(".")[0]
    return {
        "id": node_id,
        "canonical_id": node_id,
        "record_type": "BackboneNode",
        "review_status": "steward_admitted",
        "label": label,
        "pref_label": label,
        "definition": (
            f"Rights-safe {root} taxonomy node for {label} under {parent_label}; "
            "records a concrete discipline, compliance, performance, operations, or delivery topic "
            "for Explorer navigation and resolver grounding without storing protected source payloads."
        ),
        "path_code": f"{parent['path_code']}.{suffix}",
        "level": 4,
        "parent_path_code": parent["path_code"],
        "owner": parent.get("owner") or "Philip Lewis",
        "steward": parent.get("steward") or parent.get("owner") or "Philip Lewis",
        "release_version": parent.get("release_version", "0.4.0"),
        "aliases": [
            f"{parent['path_code']}.{suffix}",
            label.lower(),
            f"{parent_label.lower()} {label.lower()}",
        ],
        "scope_note": SCOPE_NOTE,
        "example_concepts": [
            label.lower(),
            parent_label.lower(),
            root.lower(),
            "broad aec mepfs semantic taxonomy",
        ],
        "generation_method": GENERATION_METHOD,
    }


def enrich(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records = payload["records"]
    relationships = payload["relationships"]
    non_arc_l3 = sorted(
        [r for r in records if _is_broad_population_parent(r)],
        key=lambda r: r["path_code"],
    )
    scoped_parent_paths = {r["path_code"] for r in non_arc_l3}
    l4_records = [r for r in records if r.get("level") == 4]
    placeholder_l4 = [
        r for r in l4_records
        if not r.get("path_code", "").startswith("ARC.")
        and str(r.get("label", "")).endswith(PLACEHOLDER_SUFFIXES)
    ]
    removed_ids = {r["id"] for r in placeholder_l4}
    filtered_records = [r for r in records if r["id"] not in removed_ids]
    filtered_relationships = [
        rel for rel in relationships
        if rel.get("from_id") not in removed_ids and rel.get("to_id") not in removed_ids
    ]
    next_id = max(int(r["id"].split("-")[-1]) for r in records if r["id"].startswith("VTN-DOM-")) + 1
    new_records: list[dict[str, Any]] = []
    new_relationships: list[dict[str, Any]] = []
    skipped_parent_count = 0
    for parent in non_arc_l3:
        existing_children = [
            r for r in filtered_records
            if r.get("parent_path_code") == parent["path_code"] and r.get("level") == 4
        ]
        existing_real_labels = {
            r["label"] for r in existing_children
            if not str(r.get("label", "")).endswith(PLACEHOLDER_SUFFIXES)
        }
        if len(existing_real_labels) >= TARGET_CHILDREN_PER_NON_ARCH_PARENT:
            skipped_parent_count += 1
            continue
        used_suffixes = {r["path_code"].split(".")[-1] for r in existing_children}
        for label in _topics_for(parent):
            if label in existing_real_labels:
                continue
            suffix = _slug_suffix(label, used_suffixes)
            child = _make_record(parent, suffix, label, next_id)
            next_id += 1
            new_records.append(child)
            new_relationships.append({
                "from_id": parent["id"],
                "predicate": "broader_than",
                "to_id": child["id"],
                "governed": True,
            })
    new_payload = {
        **payload,
        "records": filtered_records + new_records,
        "relationships": filtered_relationships + new_relationships,
    }
    l4_after = [r for r in new_payload["records"] if r.get("level") == 4]
    non_arc_l4_after = [r for r in l4_after if not r.get("path_code", "").startswith("ARC.")]
    placeholder_after = [r for r in non_arc_l4_after if str(r.get("label", "")).endswith(PLACEHOLDER_SUFFIXES)]
    parent_counts = Counter(
        r["parent_path_code"]
        for r in non_arc_l4_after
        if r.get("parent_path_code") in scoped_parent_paths
    )
    root_counts = Counter(r["path_code"].split(".")[0] for r in new_records)
    report = {
        "ok": not placeholder_after and len(parent_counts) == len(non_arc_l3) and min(parent_counts.values() or [0]) >= TARGET_CHILDREN_PER_NON_ARCH_PARENT,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(records),
        "output_record_count": len(new_payload["records"]),
        "input_relationship_count": len(relationships),
        "output_relationship_count": len(new_payload["relationships"]),
        "non_architecture_l3_count": len(non_arc_l3),
        "target_children_per_non_architecture_l3": TARGET_CHILDREN_PER_NON_ARCH_PARENT,
        "removed_non_architecture_placeholder_l4_count": len(placeholder_l4),
        "added_non_architecture_real_l4_count": len(new_records),
        "already_enriched_non_architecture_l3_parent_count": skipped_parent_count,
        "non_architecture_l4_after_count": len(non_arc_l4_after),
        "remaining_non_architecture_placeholder_l4_count": len(placeholder_after),
        "min_l4_per_non_architecture_l3": min(parent_counts.values() or [0]),
        "max_l4_per_non_architecture_l3": max(parent_counts.values() or [0]),
        "added_records_by_root": dict(sorted(root_counts.items())),
        "records_by_level": Counter(str(r.get("level")) for r in new_payload["records"]),
        "sample_added_path_codes": [r["path_code"] for r in new_records[:48]],
        "rights_safety": {
            "protected_source_payloads_ingested": False,
            "source_payload_mode": "labels_and_metadata_only",
            "neo4j_mutation": False,
            "kg_rebuild_reload_reset": False,
            "api_or_explorer_runtime_behavior_changed": False,
        },
    }
    return new_payload, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Replace non-Architecture generic L4 scaffold nodes with real semantic taxonomy nodes.")
    parser.add_argument("--fixture", default="scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
    parser.add_argument("--report", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    fixture = Path(args.fixture)
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    enriched, report = enrich(payload)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write:
        fixture.write_text(json.dumps(enriched, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
