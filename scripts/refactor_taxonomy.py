#!/usr/bin/env python3
"""
Taxonomy refactor script.

Aligns Vitruvius taxonomy with ISO 12006-2, OmniClass, UniClass, and MasterFormat.
"""

import glob
import os
import shutil
import yaml
from collections import defaultdict

BASE = "003_Canonical-Knowledge-Layer/shared"
TAXONOMY_DIR = f"{BASE}/taxonomy"
TOPICS_DIR = f"{BASE}/topics"
SUBTOPICS_DIR = f"{BASE}/subtopics"
CONCEPTS_DIR = f"{BASE}/concepts"


def load_frontmatter(path: str) -> tuple[dict, str]:
    with open(path) as f:
        content = f.read()
    if "---" not in content:
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        fm = {}
    return fm, content


def save_frontmatter(path: str, fm: dict, body: str):
    fm_str = yaml.dump(fm, default_flow_style=False, sort_keys=False, allow_unicode=True)
    text = f"---\n{fm_str}---\n{body.lstrip()}"
    with open(path, "w") as f:
        f.write(text)


def update_frontmatter_field(path: str, field: str, value):
    fm, content = load_frontmatter(path)
    old_value = fm.get(field)
    if old_value == value:
        return False
    fm[field] = value
    parts = content.split("---", 2)
    body = parts[2] if len(parts) >= 3 else content
    save_frontmatter(path, fm, body)
    return True


# ============================================================================
# NEW TAXONOMY DEFINITION
# ============================================================================

# Concept file basename (without .md) -> new taxonomy_path list
CONCEPT_MAPPING = {
    # taxonomy-accessibility (1)
    "accessible-ramps": ["taxonomy-accessibility", "topic-barrier-free-design", "subtopic-routes"],

    # taxonomy-architecture (12)
    "adaptive-reuse": ["taxonomy-architecture", "topic-history", "subtopic-preservation"],
    "architectural-history": ["taxonomy-architecture", "topic-history", "subtopic-general"],
    "architectural-interiors": ["taxonomy-architecture", "topic-theory", "subtopic-interiors"],
    "architectural-theory": ["taxonomy-architecture", "topic-theory", "subtopic-general"],
    "bauhaus-influence": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "bauhaus-philosophy": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "built-heritage": ["taxonomy-architecture", "topic-history", "subtopic-preservation"],
    "functionalism": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "international-style": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "less-is-more": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "modernism": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "organic-architecture": ["taxonomy-architecture", "topic-history", "subtopic-regionalism"],

    # taxonomy-building-systems (2)
    "building-utilities": ["taxonomy-building-systems", "topic-utilities", "subtopic-general"],
    "reinforced-concrete-detailing": ["taxonomy-building-systems", "topic-concrete", "subtopic-detailing"],

    # taxonomy-fire-life-safety (8)
    "disaster-risk-reduction": ["taxonomy-fire-life-safety", "topic-life-safety", "subtopic-emergency"],
    "fire-resistive-construction": ["taxonomy-fire-life-safety", "topic-fire-protection", "subtopic-construction"],
    "local-shelter-plan": ["taxonomy-fire-life-safety", "topic-life-safety", "subtopic-emergency"],
    "school-safety": ["taxonomy-fire-life-safety", "topic-life-safety", "subtopic-educational"],
    "doors-and-exits": ["taxonomy-fire-life-safety", "topic-egress", "subtopic-egress-systems"],
    "exit-width": ["taxonomy-fire-life-safety", "topic-egress", "subtopic-egress-systems"],
    "means-of-egress": ["taxonomy-fire-life-safety", "topic-egress", "subtopic-egress-systems"],
    "stairs": ["taxonomy-fire-life-safety", "topic-egress", "subtopic-egress-systems"],

    # taxonomy-spaces-occupancy (14)
    "building-height": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-dimensions"],
    "common-areas": ["taxonomy-spaces-occupancy", "topic-shared-spaces", "subtopic-shared-spaces"],
    "floor-area": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-dimensions"],
    "floor-area-ratio": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-dimensions"],
    "light-and-ventilation": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-natural-systems"],
    "lot-occupancy": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-dimensions"],
    "mixed-occupancy": ["taxonomy-spaces-occupancy", "topic-occupancy", "subtopic-classification"],
    "occupancy-classification": ["taxonomy-spaces-occupancy", "topic-occupancy", "subtopic-classification"],
    "occupancy-load": ["taxonomy-spaces-occupancy", "topic-occupancy", "subtopic-loading"],
    "occupancy-separation": ["taxonomy-spaces-occupancy", "topic-occupancy", "subtopic-separation"],
    "open-courts": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-openings"],
    "parking-and-loading-spaces": ["taxonomy-spaces-occupancy", "topic-circulation", "subtopic-parking"],
    "projections-over-public-ways": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-openings"],
    "setbacks": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-site-requirements"],
    "yards": ["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-site-requirements"],

    # taxonomy-site-infrastructure (16)
    "balanced-housing-development": ["taxonomy-site-infrastructure", "topic-housing", "subtopic-policy"],
    "central-business-district": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-zones"],
    "chemical-mixture": ["taxonomy-site-infrastructure", "topic-environmental", "subtopic-chemicals"],
    "chemical-substance": ["taxonomy-site-infrastructure", "topic-environmental", "subtopic-chemicals"],
    "comprehensive-land-use-plan": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-planning"],
    "groundwater-drilling": ["taxonomy-site-infrastructure", "topic-water-resources", "subtopic-extraction"],
    "hazardous-wastes": ["taxonomy-site-infrastructure", "topic-environmental", "subtopic-waste"],
    "health-facility-zoning": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-health"],
    "heritage-zone": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-zones"],
    "human-settlements": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-planning"],
    "project-area": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-zones"],
    "socialized-housing-projects": ["taxonomy-site-infrastructure", "topic-housing", "subtopic-programs"],
    "urban-development-planning": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-planning"],
    "wastewater-charge-system": ["taxonomy-site-infrastructure", "topic-water-resources", "subtopic-economics"],
    "waste-disposal": ["taxonomy-site-infrastructure", "topic-environmental", "subtopic-waste"],
    "water-quality-management-area": ["taxonomy-site-infrastructure", "topic-water-resources", "subtopic-quality"],
    "water-right": ["taxonomy-site-infrastructure", "topic-water-resources", "subtopic-rights"],
    "zoning-ordinance": ["taxonomy-site-infrastructure", "topic-land-use", "subtopic-regulation"],

    # taxonomy-energy-sustainability (2)
    "energy-audit": ["taxonomy-energy-sustainability", "topic-energy", "subtopic-compliance"],
    "minimum-energy-performance": ["taxonomy-energy-sustainability", "topic-energy", "subtopic-performance"],

    # taxonomy-construction-execution (12)
    "approved-budget-for-the-contract": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-cost-control"],
    "area-method": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-cost-control"],
    "bids-and-awards-committee": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-procurement"],
    "competitive-bidding": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-procurement"],
    "construction-estimating": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-cost-control"],
    "continuity-of-instruction": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-contracts"],
    "cross-sectional-analysis": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-analysis"],
    "general-conditions-of-contract": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-contracts"],
    "prior-consultations": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-contracts"],
    "simplified-construction-estimate": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-cost-control"],
    "unit-price-method": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-cost-control"],
    "volume-method": ["taxonomy-construction-execution", "topic-construction-administration", "subtopic-cost-control"],

    # taxonomy-project-practice (13)
    "arbitration": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-dispute-resolution"],
    "architectural-firm-registration": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-registration"],
    "code-of-ethics": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-ethics"],
    "designated-establishment": ["taxonomy-project-practice", "topic-healthcare", "subtopic-sanitation"],
    "food-establishment": ["taxonomy-project-practice", "topic-healthcare", "subtopic-sanitation"],
    "illegal-practice-of-architecture": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-enforcement"],
    "local-autonomy": ["taxonomy-project-practice", "topic-governance", "subtopic-local"],
    "local-health-authority": ["taxonomy-project-practice", "topic-governance", "subtopic-health"],
    "master-plumber": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-registration"],
    "mediation": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-dispute-resolution"],
    "mediator": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-dispute-resolution"],
    "patient-movement": ["taxonomy-project-practice", "topic-healthcare", "subtopic-operations"],
    "standards-of-professional-practice": ["taxonomy-project-practice", "topic-professional-practice", "subtopic-standards"],

    # taxonomy-regulatory-permits (5)
    "building-permit": ["taxonomy-regulatory-permits", "topic-permits", "subtopic-building"],
    "certificate-of-occupancy": ["taxonomy-regulatory-permits", "topic-certificates", "subtopic-occupancy"],
    "discharge-permit": ["taxonomy-regulatory-permits", "topic-permits", "subtopic-environmental"],
    "temporary-special-permit": ["taxonomy-regulatory-permits", "topic-permits", "subtopic-special"],
    "water-permit": ["taxonomy-regulatory-permits", "topic-permits", "subtopic-environmental"],
}

# topic_id -> (new_root_id, title)
TOPIC_MOVES = {
    "topic-administrative": ("taxonomy-regulatory-permits", "Administrative"),
    "topic-barrier-free-design": ("taxonomy-accessibility", "Barrier Free Design"),
    "topic-building-envelope": ("taxonomy-spaces-occupancy", "Building Envelope"),  # will be deleted
    "topic-circulation": ("taxonomy-spaces-occupancy", "Circulation"),
    "topic-concrete": ("taxonomy-building-systems", "Concrete"),
    "topic-construction-administration": ("taxonomy-construction-execution", "Construction Administration"),
    "topic-energy": ("taxonomy-energy-sustainability", "Energy"),
    "topic-environmental-systems": ("taxonomy-spaces-occupancy", "Environmental Systems"),  # will be deleted
    "topic-environmental": ("taxonomy-site-infrastructure", "Environmental"),
    "topic-fire-protection": ("taxonomy-fire-life-safety", "Fire Protection"),
    "topic-governance": ("taxonomy-project-practice", "Governance"),
    "topic-healthcare": ("taxonomy-project-practice", "Healthcare"),
    "topic-history": ("taxonomy-architecture", "History"),
    "topic-housing": ("taxonomy-site-infrastructure", "Housing"),
    "topic-land-use": ("taxonomy-site-infrastructure", "Land Use"),
    "topic-life-safety": ("taxonomy-fire-life-safety", "Life Safety"),
    "topic-occupancy": ("taxonomy-spaces-occupancy", "Occupancy"),
    "topic-professional-practice": ("taxonomy-project-practice", "Professional Practice"),
    "topic-theory": ("taxonomy-architecture", "Theory"),
    "topic-utilities": ("taxonomy-building-systems", "Utilities"),
    "topic-water-resources": ("taxonomy-site-infrastructure", "Water Resources"),
}

# subtopic_id -> (new_root_id, new_topic_id, title)
SUBTOPIC_MOVES = {
    "subtopic-analysis": ("taxonomy-construction-execution", "topic-construction-administration", "Analysis"),
    "subtopic-building": ("taxonomy-regulatory-permits", "topic-permits", "Building"),
    "subtopic-chemicals": ("taxonomy-site-infrastructure", "topic-environmental", "Chemicals"),
    "subtopic-classification": ("taxonomy-spaces-occupancy", "topic-occupancy", "Classification"),
    "subtopic-compliance": ("taxonomy-energy-sustainability", "topic-energy", "Compliance"),
    "subtopic-construction": ("taxonomy-fire-life-safety", "topic-fire-protection", "Construction"),
    "subtopic-contracts": ("taxonomy-construction-execution", "topic-construction-administration", "Contracts"),
    "subtopic-cost-control": ("taxonomy-construction-execution", "topic-construction-administration", "Cost Control"),
    "subtopic-detailing": ("taxonomy-building-systems", "topic-concrete", "Detailing"),
    "subtopic-dimensions": ("taxonomy-spaces-occupancy", "topic-building-planning", "Dimensions"),
    "subtopic-dispute-resolution": ("taxonomy-project-practice", "topic-professional-practice", "Dispute Resolution"),
    "subtopic-economics": ("taxonomy-site-infrastructure", "topic-water-resources", "Economics"),
    "subtopic-educational": ("taxonomy-fire-life-safety", "topic-life-safety", "Educational"),
    "subtopic-egress": ("taxonomy-fire-life-safety", "topic-egress", "Egress"),
    "subtopic-emergency": ("taxonomy-fire-life-safety", "topic-life-safety", "Emergency"),
    "subtopic-enforcement": ("taxonomy-project-practice", "topic-professional-practice", "Enforcement"),
    "subtopic-environmental": ("taxonomy-regulatory-permits", "topic-permits", "Environmental"),
    "subtopic-ethics": ("taxonomy-project-practice", "topic-professional-practice", "Ethics"),
    "subtopic-extraction": ("taxonomy-site-infrastructure", "topic-water-resources", "Extraction"),
    "subtopic-general": ("taxonomy-architecture", "topic-history", "General"),
    "subtopic-health": ("taxonomy-project-practice", "topic-governance", "Health"),
    "subtopic-interiors": ("taxonomy-architecture", "topic-theory", "Interiors"),
    "subtopic-loading": ("taxonomy-spaces-occupancy", "topic-occupancy", "Loading"),
    "subtopic-local": ("taxonomy-project-practice", "topic-governance", "Local"),
    "subtopic-modern-movement": ("taxonomy-architecture", "topic-history", "Modern Movement"),
    "subtopic-natural-systems": ("taxonomy-spaces-occupancy", "topic-building-planning", "Natural Systems"),
    "subtopic-occupancy": ("taxonomy-regulatory-permits", "topic-certificates", "Occupancy"),
    "subtopic-openings": ("taxonomy-spaces-occupancy", "topic-building-planning", "Openings"),
    "subtopic-operations": ("taxonomy-project-practice", "topic-healthcare", "Operations"),
    "subtopic-parking": ("taxonomy-spaces-occupancy", "topic-circulation", "Parking"),
    "subtopic-performance": ("taxonomy-energy-sustainability", "topic-energy", "Performance"),
    "subtopic-permits": ("taxonomy-regulatory-permits", "topic-permits", "Permits"),
    "subtopic-planning": ("taxonomy-site-infrastructure", "topic-land-use", "Planning"),
    "subtopic-policy": ("taxonomy-site-infrastructure", "topic-housing", "Policy"),
    "subtopic-preservation": ("taxonomy-architecture", "topic-history", "Preservation"),
    "subtopic-procurement": ("taxonomy-construction-execution", "topic-construction-administration", "Procurement"),
    "subtopic-programs": ("taxonomy-site-infrastructure", "topic-housing", "Programs"),
    "subtopic-quality": ("taxonomy-site-infrastructure", "topic-water-resources", "Quality"),
    "subtopic-regionalism": ("taxonomy-architecture", "topic-history", "Regionalism"),
    "subtopic-registration": ("taxonomy-project-practice", "topic-professional-practice", "Registration"),
    "subtopic-regulation": ("taxonomy-site-infrastructure", "topic-land-use", "Regulation"),
    "subtopic-rights": ("taxonomy-site-infrastructure", "topic-water-resources", "Rights"),
    "subtopic-routes": ("taxonomy-accessibility", "topic-barrier-free-design", "Routes"),
    "subtopic-sanitation": ("taxonomy-project-practice", "topic-healthcare", "Sanitation"),
    "subtopic-separation": ("taxonomy-spaces-occupancy", "topic-occupancy", "Separation"),
    "subtopic-shared-spaces": ("taxonomy-spaces-occupancy", "topic-shared-spaces", "Shared Spaces"),
    "subtopic-site-requirements": ("taxonomy-spaces-occupancy", "topic-building-planning", "Site Requirements"),
    "subtopic-special": ("taxonomy-regulatory-permits", "topic-permits", "Special"),
    "subtopic-standards": ("taxonomy-project-practice", "topic-professional-practice", "Standards"),
    "subtopic-waste": ("taxonomy-site-infrastructure", "topic-environmental", "Waste"),
    "subtopic-zones": ("taxonomy-site-infrastructure", "topic-land-use", "Zones"),
    "subtopic-egress-systems": ("taxonomy-fire-life-safety", "topic-egress", "Egress Systems"),
}

NEW_TAXONOMY_ROOTS = {
    "taxonomy-building-systems": "Building Systems",
    "taxonomy-fire-life-safety": "Fire & Life Safety",
    "taxonomy-spaces-occupancy": "Spaces & Occupancy",
    "taxonomy-energy-sustainability": "Energy & Sustainability",
    "taxonomy-construction-execution": "Construction & Execution",
    "taxonomy-project-practice": "Project & Practice Management",
    "taxonomy-regulatory-permits": "Regulatory & Permits",
}

NEW_TOPICS = {
    "topic-egress": ("taxonomy-fire-life-safety", "Egress"),
    "topic-shared-spaces": ("taxonomy-spaces-occupancy", "Shared Spaces"),
    "topic-building-planning": ("taxonomy-spaces-occupancy", "Building Planning"),
    "topic-certificates": ("taxonomy-regulatory-permits", "Certificates"),
}

NEW_SUBTOPICS = {
    "subtopic-egress-systems": ("taxonomy-fire-life-safety", "topic-egress", "Egress Systems"),
    "subtopic-building": ("taxonomy-regulatory-permits", "topic-permits", "Building"),
    "subtopic-special": ("taxonomy-regulatory-permits", "topic-permits", "Special"),
    "subtopic-environmental": ("taxonomy-regulatory-permits", "topic-permits", "Environmental"),
    "subtopic-occupancy": ("taxonomy-regulatory-permits", "topic-certificates", "Occupancy"),
    "subtopic-site-requirements": ("taxonomy-spaces-occupancy", "topic-building-planning", "Site Requirements"),
}

# Files to delete (old taxonomy roots that are fully replaced)
DELETE_TAXONOMY_ROOTS = [
    "taxonomy-compliance-checks.md",
    "taxonomy-definitions.md",
    "taxonomy-fire-and-life-safety.md",
    "taxonomy-mep.md",
    "taxonomy-procedures.md",
    "taxonomy-structural.md",
]

# Old topic files to delete (fully replaced by new topics)
DELETE_TOPICS = [
    "topic-building-envelope.md",
    "topic-environmental-systems.md",
]


def make_taxonomy_root_file(root_id: str, title: str):
    path = f"{TAXONOMY_DIR}/{root_id}.md"
    body = f"# {title}\n\nTop-level taxonomy node for {title.lower()}.\n"
    fm = {
        "id": root_id,
        "title": title,
        "page_type": "taxonomy",
        "canonical_status": "validated",
        "trust_level": "primary",
    }
    save_frontmatter(path, fm, body)


def make_topic_file(topic_id: str, root_id: str, title: str):
    path = f"{TOPICS_DIR}/{topic_id}.md"
    body = f"# {title}\n\nTopic node in the Vitruvius canonical knowledge graph.\n"
    fm = {
        "id": topic_id,
        "title": title,
        "page_type": "topic",
        "canonical_status": "validated",
        "trust_level": "primary",
        "taxonomy_path": [root_id],
    }
    save_frontmatter(path, fm, body)


def make_subtopic_file(subtopic_id: str, root_id: str, topic_id: str, title: str):
    path = f"{SUBTOPICS_DIR}/{subtopic_id}.md"
    body = f"# {title}\n\nSubtopic node in the Vitruvius canonical knowledge graph.\n"
    fm = {
        "id": subtopic_id,
        "title": title,
        "page_type": "subtopic",
        "canonical_status": "validated",
        "trust_level": "primary",
        "taxonomy_path": [root_id, topic_id],
    }
    save_frontmatter(path, fm, body)


def main():
    updated = defaultdict(list)
    created = defaultdict(list)
    deleted = defaultdict(list)

    # 1. Update concept taxonomy paths
    for basename, new_path in CONCEPT_MAPPING.items():
        path = f"{CONCEPTS_DIR}/{basename}.md"
        if not os.path.exists(path):
            print(f"MISSING concept: {path}")
            continue
        if update_frontmatter_field(path, "taxonomy_path", new_path):
            updated["concepts"].append(basename)

    # 2. Create new taxonomy roots
    for root_id, title in NEW_TAXONOMY_ROOTS.items():
        path = f"{TAXONOMY_DIR}/{root_id}.md"
        if not os.path.exists(path):
            make_taxonomy_root_file(root_id, title)
            created["taxonomy_roots"].append(root_id)

    # 3. Update existing taxonomy roots
    # taxonomy-accessibility and taxonomy-architecture unchanged
    # taxonomy-building-code gets narrower description update
    bc_path = f"{TAXONOMY_DIR}/taxonomy-building-code.md"
    if os.path.exists(bc_path):
        fm, content = load_frontmatter(bc_path)
        fm["title"] = "Building Code"
        parts = content.split("---", 2)
        save_frontmatter(bc_path, fm, parts[2] if len(parts) >= 3 else content)
        updated["taxonomy_roots"].append("taxonomy-building-code")

    # 4. Update topic files
    for topic_id, (root_id, title) in TOPIC_MOVES.items():
        path = f"{TOPICS_DIR}/{topic_id}.md"
        if not os.path.exists(path):
            continue
        fm, content = load_frontmatter(path)
        changed = False
        if fm.get("taxonomy_path", [None])[0] != root_id:
            fm["taxonomy_path"] = [root_id]
            changed = True
        if fm.get("title") != title:
            fm["title"] = title
            changed = True
        if changed:
            parts = content.split("---", 2)
            save_frontmatter(path, fm, parts[2] if len(parts) >= 3 else content)
            updated["topics"].append(topic_id)

    # 5. Create new topic files
    for topic_id, (root_id, title) in NEW_TOPICS.items():
        path = f"{TOPICS_DIR}/{topic_id}.md"
        if not os.path.exists(path):
            make_topic_file(topic_id, root_id, title)
            created["topics"].append(topic_id)

    # 6. Update subtopic files
    for subtopic_id, (root_id, topic_id, title) in SUBTOPIC_MOVES.items():
        path = f"{SUBTOPICS_DIR}/{subtopic_id}.md"
        if not os.path.exists(path):
            # Some new subtopics defined in NEW_SUBTOPICS will be created below
            continue
        fm, content = load_frontmatter(path)
        changed = False
        expected_path = [root_id, topic_id]
        if fm.get("taxonomy_path") != expected_path:
            fm["taxonomy_path"] = expected_path
            changed = True
        if fm.get("title") != title:
            fm["title"] = title
            changed = True
        if changed:
            parts = content.split("---", 2)
            save_frontmatter(path, fm, parts[2] if len(parts) >= 3 else content)
            updated["subtopics"].append(subtopic_id)

    # 7. Create new subtopic files
    for subtopic_id, (root_id, topic_id, title) in NEW_SUBTOPICS.items():
        path = f"{SUBTOPICS_DIR}/{subtopic_id}.md"
        if not os.path.exists(path):
            make_subtopic_file(subtopic_id, root_id, topic_id, title)
            created["subtopics"].append(subtopic_id)

    # 8. Delete obsolete taxonomy roots
    for fname in DELETE_TAXONOMY_ROOTS:
        path = f"{TAXONOMY_DIR}/{fname}"
        if os.path.exists(path):
            os.remove(path)
            deleted["taxonomy_roots"].append(fname)

    # 9. Delete obsolete topic files
    for fname in DELETE_TOPICS:
        path = f"{TOPICS_DIR}/{fname}"
        if os.path.exists(path):
            os.remove(path)
            deleted["topics"].append(fname)

    # Summary
    print("=== TAXONOMY REFACTOR SUMMARY ===\n")
    print(f"Concepts updated: {len(updated['concepts'])}")
    print(f"Taxonomy roots created: {created['taxonomy_roots']}")
    print(f"Taxonomy roots updated: {updated['taxonomy_roots']}")
    print(f"Taxonomy roots deleted: {deleted['taxonomy_roots']}")
    print(f"Topics created: {created['topics']}")
    print(f"Topics updated: {updated['topics']}")
    print(f"Topics deleted: {deleted['topics']}")
    print(f"Subtopics created: {created['subtopics']}")
    print(f"Subtopics updated: {updated['subtopics']}")

    # Verification
    print("\n=== VERIFICATION ===")
    missing = []
    for basename, expected in CONCEPT_MAPPING.items():
        path = f"{CONCEPTS_DIR}/{basename}.md"
        fm, _ = load_frontmatter(path)
        actual = fm.get("taxonomy_path", [])
        if actual != expected:
            missing.append((basename, expected, actual))
    if missing:
        print(f"MISMATCHES: {len(missing)}")
        for b, e, a in missing:
            print(f"  {b}: expected {e}, got {a}")
    else:
        print("All concept taxonomy paths match.")

    # Count concepts per new root
    root_counts = defaultdict(int)
    for basename in CONCEPT_MAPPING:
        path = f"{CONCEPTS_DIR}/{basename}.md"
        fm, _ = load_frontmatter(path)
        tp = fm.get("taxonomy_path", [])
        if tp:
            root_counts[tp[0]] += 1
    print("\nConcepts per root:")
    for root, count in sorted(root_counts.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}  {root}")


if __name__ == "__main__":
    main()
