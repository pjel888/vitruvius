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
    "steward_governed_real_architecture_semantic_enrichment_from_public_"
    "licensure_curriculum_accreditation_and_professional_topic_structures"
)
SCOPE_NOTE = (
    "Architecture semantic enrichment synthesized from public licensure, curriculum, "
    "accreditation, professional-practice, and local filename topic signals; labels and "
    "metadata only, no protected source payloads."
)
STOPWORDS = {"and", "of", "the", "for", "to", "in", "with", "a", "an"}

# Exact high-value topic sets for areas where the user specifically called out
# history/theory, licensure, laws, rules, and real architectural knowledge.
SPECIAL_L4_TOPICS: dict[str, list[str]] = {
    "ARC.WAC.PAO": [
        "Paleolithic Shelter Forms",
        "Neolithic Settlement Patterns",
        "Megalithic Monument Types",
        "Early River Valley Urbanism",
        "Vernacular Material Adaptation",
        "Ritual Landscape Alignment",
    ],
    "ARC.WAC.CIT": [
        "Egyptian Monumental Axis",
        "Greek Orders And Proportion",
        "Roman Concrete Vaulting",
        "Persian Palace Complexes",
        "Mesoamerican Ceremonial Precincts",
        "Classical Civic Space Types",
    ],
    "ARC.WAC.MSW": [
        "Early Christian Basilica Planning",
        "Byzantine Dome Systems",
        "Islamic Courtyard And Iwan Traditions",
        "Romanesque Massing And Pilgrimage Routes",
        "Gothic Rib Vault And Flying Buttress Systems",
        "Medieval Urban Fabric",
    ],
    "ARC.WAC.MCT": [
        "Renaissance Humanist Proportion",
        "Baroque Spatial Drama",
        "Neoclassical Civic Order",
        "Industrial Iron And Glass Architecture",
        "Modernist Functionalism",
        "Postmodern And Contemporary Pluralism",
        "High Tech And Parametric Lineages",
    ],
    "ARC.HIS.ANC": [
        "Mesopotamian Ziggurat Planning",
        "Egyptian Temple Procession",
        "Greek Temple Orders",
        "Roman Forum And Basilica Types",
        "Classical Proportion Systems",
        "Ancient Infrastructure Urbanism",
    ],
    "ARC.HIS.ASN": [
        "Chinese Timber Bracket Traditions",
        "Japanese Modular Tatami Planning",
        "Indian Temple Mandala Planning",
        "Islamic Geometric Surface Systems",
        "Southeast Asian Stilt House Traditions",
        "Vernacular Climate Adaptation",
    ],
    "ARC.HIS.MOD": [
        "Arts And Crafts Reform",
        "Bauhaus Pedagogy And Modernism",
        "International Style Curtain Wall Logic",
        "Brutalist Material Expression",
        "Critical Regionalism",
        "Deconstructivist Formal Strategies",
        "Contemporary Parametric Design",
    ],
    "ARC.HIS.SEA": [
        "Bahay Kubo Spatial Logic",
        "Bahay Na Bato Hybrid Construction",
        "Spanish Colonial Church Complexes",
        "American Colonial Civic Planning",
        "Postwar Modern Philippine Architecture",
        "Tropical Modernism In Southeast Asia",
    ],
    "ARC.PRC.LEG": [
        "Scope Of Architectural Practice",
        "Architect Of Record Responsibility",
        "Signing And Sealing Authority",
        "Responsible Control And Authorship",
        "Professional Liability And Duty Of Care",
        "Title Protection And Registration",
    ],
    "ARC.PRC.CON": [
        "Owner Architect Agreement Scope",
        "Procurement Method Selection",
        "Bid Evaluation And Award Advice",
        "Consultant Coordination Agreements",
        "Change Order Governance",
        "Payment Certification Controls",
    ],
    "ARC.PRC.ETH": [
        "Conflict Of Interest Disclosure",
        "Public Health Safety Welfare Duty",
        "Client Confidentiality Boundaries",
        "Competence And Continuing Development",
        "Fair Competition And Advertising Ethics",
        "Professional Accountability Records",
    ],
    "ARC.PRC.OFM": [
        "Project Work Plan Setup",
        "Fee Basis And Resource Planning",
        "Risk Register Maintenance",
        "Quality Assurance Reviews",
        "Document Control Workflow",
        "Client Communication Cadence",
    ],
    "ARC.COD.BCA": [
        "Occupancy Classification Review",
        "Construction Type Determination",
        "Allowable Height And Area Check",
        "Fire Separation Distance Coordination",
        "Certificate Of Occupancy Pathway",
        "Inspection And Correction Workflow",
    ],
    "ARC.COD.ZLU": [
        "Permitted Use Verification",
        "Setback And Yard Controls",
        "Floor Area Ratio Controls",
        "Parking And Loading Requirements",
        "Easement And Right Of Way Checks",
        "Variance And Exception Pathways",
    ],
    "ARC.COD.PER": [
        "Permit Drawing Completeness",
        "Code Analysis Sheet",
        "Agency Submission Matrix",
        "Revision Cloud And Response Log",
        "Signed And Sealed Sheet Control",
        "Permit Condition Tracking",
    ],
    "ARC.COD.JUR": [
        "Local Ordinance Overlay Mapping",
        "Heritage District Controls",
        "Environmental Permit Interface",
        "Fire Authority Referral",
        "Accessibility Authority Review",
        "Utility Agency Clearance",
    ],
    "ARC.REG.PHL": [
        "Philippines ALE History Theory Practice Area",
        "Philippines ALE Structures Materials Utilities Area",
        "Philippines ALE Design And Site Planning Area",
        "RA 9266 Practice Scope Metadata",
        "PD 1096 Code Coordination Metadata",
        "BP 344 Accessibility Coordination Metadata",
    ],
    "ARC.REG.HKG": [
        "HKIA Professional Assessment Case Study",
        "Hong Kong Professional Practice Interview",
        "Local Ordinance And Practice Knowledge",
        "Contract Administration Competence",
        "Practical Experience Record",
        "Professional Conduct Review",
    ],
    "ARC.REG.SGP": [
        "Singapore PPE Professional Practice Knowledge",
        "Singapore Practice Course Competency Areas",
        "Building Control Submission Awareness",
        "Contracts And Statutory Duties",
        "Practical Experience Documentation",
        "Professional Conduct And Liability",
    ],
    "ARC.REG.SEA": [
        "ASEAN Mutual Recognition Context",
        "Indonesia Architect Registration Context",
        "Thailand Architect Council Context",
        "Tropical Regional Practice Conditions",
        "Cross Border Practice Constraints",
        "Local Code Adaptation Workflow",
    ],
    "ARC.DTS.CPT": [
        "Vitruvian Firmitas Utilitas Venustas",
        "Classical Orders And Entasis",
        "Renaissance Geometry And Symmetry",
        "Golden Section And Proportion Studies",
        "Beaux Arts Parti And Axis",
        "Typology And Precedent Logic",
    ],
    "ARC.DTS.MDD": [
        "Form Follows Function Doctrine",
        "Plan Libre And Free Facade",
        "Functional Zoning Diagrams",
        "Machine Age Aesthetic",
        "Universal Space And Modular Grid",
        "Modernist Social Housing Ideals",
    ],
    "ARC.DTS.PPT": [
        "Genius Loci And Place Identity",
        "Phenomenology Of Light And Material",
        "Critical Regionalist Mediation",
        "Embodied Spatial Experience",
        "Memory Meaning And Atmosphere",
        "Landscape Urbanism Interface",
    ],
    "ARC.DTS.PST": [
        "Parametric Rule Sets",
        "Systems Feedback Modeling",
        "Agent Based Spatial Simulation",
        "Computational Morphogenesis",
        "Performance Driven Form Finding",
        "Data Informed Design Iteration",
    ],
}

DOMAIN_L4_TOPICS: dict[str, list[str]] = {
    "BTY": ["Program Mix", "Public Private Gradient", "Service Access", "Security Screening", "Back Of House Flow", "Adaptability Strategy"],
    "COO": ["Discipline Interface Matrix", "Model Clash Issue Log", "Penetration And Opening Coordination", "Equipment Clearance Zone", "Coordination Meeting Action Register", "Design Responsibility Boundary"],
    "DOC": ["Sheet Index Governance", "Annotation And Keynote System", "Detail Reference Logic", "Specification Section Mapping", "Revision And Issuance Control", "Drawing Coordination Checklist"],
    "ENV": ["Rainscreen Drainage Plane", "Thermal Control Layer", "Air Barrier Continuity", "Solar Shading Geometry", "Opening Performance Criteria", "Facade Maintenance Access"],
    "HER": ["Statement Of Significance", "Fabric Condition Survey", "Minimum Intervention Strategy", "Reversible Intervention Detail", "Adaptive Reuse Compatibility", "Conservation Maintenance Plan"],
    "HUM": ["Anthropometric Clearance", "Reach Range And Controls", "Sightline Comfort", "Glare Management", "Behavioral Wayfinding Cue", "Occupant Density Pattern"],
    "INT": ["Furniture Equipment Layout", "Finish Schedule Logic", "Acoustic Interior Surface", "Ceiling Service Coordination", "Casework And Millwork Detail", "Interior Life Safety Coordination"],
    "SPC": ["Adjacency Matrix", "Bubble Diagram Translation", "Primary Circulation Spine", "Threshold And Transition Space", "Space Syntax Cue", "Functional Zoning Strategy"],
    "TEC": ["Movement Joint Placement", "Sealant And Flashing Continuity", "Tolerance Stack Up", "Thermal Break Detail", "Moisture Path Interruption", "Constructability Sequence"],
    "WAY": ["Decision Point Hierarchy", "Room Identification Logic", "Accessible Tactile Cue", "Signage Mounting Zone", "Multilingual Symbol System", "Emergency Egress Signage"],
    "THE": ["Parti Diagram", "Axis Hierarchy", "Rhythm And Proportion", "Figure Ground Reading", "Phenomenological Atmosphere", "Critical Interpretation Framework"],
    "BLD": ["Structural Grid Coordination", "Vertical Shaft Planning", "MEP Equipment Zone", "Envelope System Interface", "Construction Sequence Awareness", "Performance Trade Off Review"],
    "MAT": ["Embodied Carbon Profile", "Moisture Durability Risk", "Fire Rating Compatibility", "Tactile And Visual Finish Quality", "Maintenance And Replacement Cycle", "Local Availability Constraint"],
    "SIT": ["Topographic Section Reading", "Stormwater Flow Path", "Solar And Wind Exposure", "Arrival And Drop Off Sequence", "Landscape Buffer Strategy", "Site Constraint Overlay"],
    "ECD": ["Daylight Factor Strategy", "Cross Ventilation Path", "Thermal Mass Placement", "Acoustic Separation Strategy", "Solar Heat Gain Control", "Occupant Comfort Metric"],
    "SUS": ["Passive Cooling Strategy", "Water Conservation Strategy", "Material Reuse Strategy", "Operational Energy Reduction", "Climate Resilience Measure", "Lifecycle Carbon Review"],
    "URB": ["Street Wall Continuity", "Active Frontage Strategy", "Transit Access Node", "Block Permeability", "Public Realm Edge", "Neighborhood Amenity Network"],
    "ACC": ["Accessible Route Continuity", "Door Hardware Usability", "Toilet Room Clearance", "Tactile Warning Surface", "Wayfinding For Low Vision", "Inclusive Seating Distribution"],
    "FIR": ["Travel Distance Calculation", "Exit Capacity Coordination", "Smoke Compartment Strategy", "Fire Rated Assembly Continuity", "Emergency Vehicle Access", "Life Safety Systems Interface"],
    "DIG": ["Model Level Of Information", "Shared Coordinate Setup", "Clash Detection Workflow", "Parametric Family Governance", "IFC Export Check", "Issue Tracking Integration"],
    "DES": ["Problem Framing", "Concept Massing Option", "Design Critique Response", "Spatial Scenario Testing", "Precedent Translation", "Design Intent Narrative"],
    "PLN": ["Stakeholder Requirement Capture", "Room Data Sheet", "Area Program Reconciliation", "Occupancy Scenario", "Functional Performance Criteria", "Post Occupancy Lesson Loop"],
    "TYP": ["Patient Or User Flow", "Assembly Crowd Movement", "Education Learning Cluster", "Hospitality Arrival Sequence", "Industrial Process Adjacency", "Research Laboratory Flexibility"],
    "HOU": ["Unit Mix Strategy", "Privacy Gradient", "Shared Amenity Planning", "Incremental Growth Pattern", "Affordability Constraint", "Residential Natural Ventilation"],
    "DET": ["Envelope Corner Detail", "Waterproofing Termination", "Material Transition Joint", "Interior Trim Interface", "Buildability Mockup", "Maintenance Access Detail"],
    "CHC": ["Heritage Value Mapping", "Conservation Management Policy", "Compatible New Use", "Cultural Landscape Buffer", "Impact Mitigation Measure", "Archival Documentation Protocol"],
    "PRE": ["Analytical Diagram", "Sectional Perspective", "Physical Study Model", "Rendered View Narrative", "Jury Board Sequencing", "Portfolio Curation"],
    "TAC": ["Deep Overhang Strategy", "Ventilated Roof Cavity", "Courtyard Stack Ventilation", "Rain Screened Veranda", "Humidity Resistant Material", "Monsoon Drainage Detail"],
    "ARC": ["Gesture Drawing", "Plan Section Elevation Set", "Exploded Axonometric", "Concept Diagram Series", "Scale Model Craft", "Critique Presentation Narrative"],
    "COA": ["Submittal Review Log", "Request For Information Response", "Site Observation Report", "Change Directive Evaluation", "Punch List Verification", "Closeout Document Review"],
    "HPR": ["Tenure And Affordability Model", "Community Facility Integration", "Subdivision Control Interface", "Incremental Housing Support", "Residential Safety Upgrade", "Housing Policy Compliance"],
    "ABT": ["Specialized User Journey", "Operational Support Zone", "High Occupancy Flow", "Service Core Strategy", "Security And Screening Layer", "Future Adaptability Provision"],
    "ARM": ["Research Question Framing", "Case Study Selection", "Interview Protocol", "Observation And Mapping Method", "Performance Evidence Metric", "Design Research Synthesis"],
    "HIS": ["Cultural Context Driver", "Construction Technique Lineage", "Spatial Type Evolution", "Ornament And Symbol System", "Urban Pattern Influence", "Climate Adapted Precedent"],
    "REG": ["Licensure Competency Domain", "Professional Experience Evidence", "Local Statutory Knowledge", "Professional Conduct Standard", "Submission And Documentation Rule", "Regional Practice Adaptation"],
    "WAC": ["Chronological Period Marker", "Regional Center Of Development", "Structural System Innovation", "Sacred Or Civic Typology", "Material Culture Cue", "Urban Settlement Pattern"],
    "DTS": ["Theoretical Premise", "Spatial Ordering Rule", "Formal Language Device", "Design Pedagogy Reference", "Critique Vocabulary", "Contemporary Application"],
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


def _topics_for(parent: dict[str, Any]) -> list[str]:
    code = parent["path_code"]
    if code in SPECIAL_L4_TOPICS:
        return SPECIAL_L4_TOPICS[code]
    l2 = code.split(".")[1]
    topics = DOMAIN_L4_TOPICS.get(l2) or DOMAIN_L4_TOPICS.get(parent["parent_path_code"].split(".")[1], [])
    if not topics:
        topics = [
            "Definition And Scope Boundary",
            "Performance Criteria",
            "Documentation Requirement",
            "Coordination Interface",
            "Risk And Compliance Check",
            "Design Decision Rule",
        ]
    # Keep depth consistent and substantial without overwhelming Explorer: six concrete children per L3.
    return topics[:6]


def _make_record(parent: dict[str, Any], suffix: str, label: str, next_id: int) -> dict[str, Any]:
    node_id = f"VTN-DOM-{next_id:07d}"
    parent_label = parent["label"]
    grandparent = parent.get("parent_path_code", "ARC")
    return {
        "id": node_id,
        "canonical_id": node_id,
        "record_type": "BackboneNode",
        "review_status": "steward_admitted",
        "label": label,
        "pref_label": label,
        "definition": (
            f"Rights-safe architecture taxonomy node for {label} under {parent_label}; "
            "records a real professional, historical, design, technical, or regulatory topic "
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
            grandparent.lower(),
            "architecture semantic taxonomy",
        ],
        "generation_method": GENERATION_METHOD,
    }


def enrich(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records = payload["records"]
    relationships = payload["relationships"]
    arc_l4 = [
        r for r in records
        if r.get("path_code", "").startswith("ARC.") and r.get("level") == 4
    ]
    placeholder_l4 = [r for r in arc_l4 if str(r.get("label", "")).endswith(PLACEHOLDER_SUFFIXES)]
    removed_ids = {r["id"] for r in placeholder_l4}
    parent_by_code = {r["path_code"]: r for r in records}
    arc_l3 = sorted(
        [r for r in records if r.get("path_code", "").startswith("ARC.") and r.get("level") == 3],
        key=lambda r: r["path_code"],
    )
    filtered_records = [r for r in records if r["id"] not in removed_ids]
    filtered_relationships = [
        rel for rel in relationships
        if rel.get("from_id") not in removed_ids and rel.get("to_id") not in removed_ids
    ]
    next_id = max(int(r["id"].split("-")[-1]) for r in records if r["id"].startswith("VTN-DOM-")) + 1
    new_records: list[dict[str, Any]] = []
    new_relationships: list[dict[str, Any]] = []
    skipped_parent_count = 0
    for parent in arc_l3:
        existing_children = [
            r for r in filtered_records
            if r.get("parent_path_code") == parent["path_code"] and r.get("level") == 4
        ]
        existing_real_labels = {r["label"] for r in existing_children if not str(r.get("label", "")).endswith(PLACEHOLDER_SUFFIXES)}
        if len(existing_real_labels) >= 6:
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
    new_payload = {**payload, "records": filtered_records + new_records, "relationships": filtered_relationships + new_relationships}
    arch_l4_after = [r for r in new_payload["records"] if r.get("path_code", "").startswith("ARC.") and r.get("level") == 4]
    placeholder_after = [r for r in arch_l4_after if str(r.get("label", "")).endswith(PLACEHOLDER_SUFFIXES)]
    parent_counts = Counter(r["parent_path_code"] for r in arch_l4_after)
    report = {
        "ok": not placeholder_after and len(parent_counts) == len(arc_l3) and min(parent_counts.values() or [0]) >= 6,
        "generation_method": GENERATION_METHOD,
        "input_record_count": len(records),
        "output_record_count": len(new_payload["records"]),
        "input_relationship_count": len(relationships),
        "output_relationship_count": len(new_payload["relationships"]),
        "architecture_l3_count": len(arc_l3),
        "removed_architecture_placeholder_l4_count": len(placeholder_l4),
        "added_architecture_real_l4_count": len(new_records),
        "already_enriched_architecture_l3_parent_count": skipped_parent_count,
        "architecture_l4_after_count": len(arch_l4_after),
        "remaining_architecture_placeholder_l4_count": len(placeholder_after),
        "min_l4_per_architecture_l3": min(parent_counts.values() or [0]),
        "max_l4_per_architecture_l3": max(parent_counts.values() or [0]),
        "records_by_level": Counter(str(r.get("level")) for r in new_payload["records"]),
        "architecture_records_by_level": Counter(str(r.get("level")) for r in new_payload["records"] if r.get("path_code", "").startswith("ARC")),
        "sample_added_path_codes": [r["path_code"] for r in new_records[:24]],
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
    parser = argparse.ArgumentParser(description="Replace generic Architecture L4 scaffold nodes with real semantic taxonomy nodes.")
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
