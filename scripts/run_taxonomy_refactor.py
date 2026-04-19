#!/usr/bin/env python3
"""
Taxonomy Refactor — assign taxonomy paths to all canonical concepts,
create topic/subtopic scaffolding, and rewire the graph spine.

Run from repo root:
    python scripts/run_taxonomy_refactor.py
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(".").resolve()
CANONICAL = REPO_ROOT / "003_Canonical-Knowledge-Layer" / "shared"
TAXONOMY_DIR = CANONICAL / "taxonomy"
TOPIC_DIR = CANONICAL / "topics"
SUBTOPIC_DIR = CANONICAL / "subtopics"

# ---------------------------------------------------------------------------
# Taxonomy classification map: concept_id -> [taxonomy, topic, subtopic?]
# ---------------------------------------------------------------------------
CLASSIFICATION: dict[str, list[str]] = {
    # ===== Building Code (PD-1096 core) =====
    "concept-building-permit": ["taxonomy-building-code", "topic-administrative", "subtopic-permits"],
    "concept-certificate-of-occupancy": ["taxonomy-building-code", "topic-administrative", "subtopic-permits"],
    "concept-temporary-special-permit": ["taxonomy-building-code", "topic-administrative", "subtopic-permits"],
    "concept-occupancy-classification": ["taxonomy-building-code", "topic-occupancy", "subtopic-classification"],
    "concept-occupancy-load": ["taxonomy-building-code", "topic-occupancy", "subtopic-loading"],
    "concept-mixed-occupancy": ["taxonomy-building-code", "topic-occupancy", "subtopic-classification"],
    "concept-occupancy-separation": ["taxonomy-building-code", "topic-occupancy", "subtopic-separation"],
    "concept-building-height": ["taxonomy-building-code", "topic-building-envelope", "subtopic-dimensions"],
    "concept-floor-area": ["taxonomy-building-code", "topic-building-envelope", "subtopic-dimensions"],
    "concept-floor-area-ratio": ["taxonomy-building-code", "topic-building-envelope", "subtopic-dimensions"],
    "concept-lot-occupancy": ["taxonomy-building-code", "topic-building-envelope", "subtopic-dimensions"],
    "concept-setbacks": ["taxonomy-building-code", "topic-building-envelope", "subtopic-dimensions"],
    "concept-yards": ["taxonomy-building-code", "topic-building-envelope", "subtopic-dimensions"],
    "concept-open-courts": ["taxonomy-building-code", "topic-building-envelope", "subtopic-openings"],
    "concept-projections-over-public-ways": ["taxonomy-building-code", "topic-building-envelope", "subtopic-openings"],
    "concept-means-of-egress": ["taxonomy-building-code", "topic-circulation", "subtopic-egress"],
    "concept-exit-width": ["taxonomy-building-code", "topic-circulation", "subtopic-egress"],
    "concept-doors-and-exits": ["taxonomy-building-code", "topic-circulation", "subtopic-egress"],
    "concept-stairs": ["taxonomy-building-code", "topic-circulation", "subtopic-egress"],
    "concept-parking-and-loading-spaces": ["taxonomy-building-code", "topic-circulation", "subtopic-parking"],
    "concept-light-and-ventilation": ["taxonomy-building-code", "topic-environmental-systems", "subtopic-natural-systems"],

    # ===== Fire and Life Safety (RA-9514 + PD-1096 overlap) =====
    "concept-fire-resistive-construction": ["taxonomy-fire-and-life-safety", "topic-fire-protection", "subtopic-construction"],

    # ===== Accessibility (BP-344) =====
    "concept-accessible-ramps": ["taxonomy-accessibility", "topic-barrier-free-design", "subtopic-routes"],

    # ===== Structural =====
    "concept-reinforced-concrete-detailing": ["taxonomy-structural", "topic-concrete", "subtopic-detailing"],

    # ===== MEP =====
    "concept-minimum-energy-performance": ["taxonomy-mep", "topic-energy", "subtopic-performance"],
    "concept-energy-audit": ["taxonomy-mep", "topic-energy", "subtopic-compliance"],
    "concept-building-utilities": ["taxonomy-mep", "topic-utilities", "subtopic-general"],

    # ===== Site Planning / Environmental =====
    "concept-comprehensive-land-use-plan": ["taxonomy-site-planning", "topic-land-use", "subtopic-planning"],
    "concept-zoning-ordinance": ["taxonomy-site-planning", "topic-land-use", "subtopic-regulation"],
    "concept-central-business-district": ["taxonomy-site-planning", "topic-land-use", "subtopic-zones"],
    "concept-heritage-zone": ["taxonomy-site-planning", "topic-land-use", "subtopic-zones"],
    "concept-human-settlements": ["taxonomy-site-planning", "topic-land-use", "subtopic-planning"],
    "concept-urban-development-planning": ["taxonomy-site-planning", "topic-land-use", "subtopic-planning"],
    "concept-project-area": ["taxonomy-site-planning", "topic-land-use", "subtopic-zones"],
    "concept-water-right": ["taxonomy-site-planning", "topic-water-resources", "subtopic-rights"],
    "concept-water-permit": ["taxonomy-site-planning", "topic-water-resources", "subtopic-permits"],
    "concept-discharge-permit": ["taxonomy-site-planning", "topic-water-resources", "subtopic-permits"],
    "concept-water-quality-management-area": ["taxonomy-site-planning", "topic-water-resources", "subtopic-quality"],
    "concept-groundwater-drilling": ["taxonomy-site-planning", "topic-water-resources", "subtopic-extraction"],
    "concept-waste-disposal": ["taxonomy-site-planning", "topic-environmental", "subtopic-waste"],
    "concept-hazardous-wastes": ["taxonomy-site-planning", "topic-environmental", "subtopic-waste"],
    "concept-wastewater-charge-system": ["taxonomy-site-planning", "topic-water-resources", "subtopic-economics"],

    # ===== Architecture Theory & History =====
    "concept-modernism": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "concept-bauhaus-influence": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "concept-bauhaus-philosophy": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "concept-international-style": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "concept-functionalism": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "concept-less-is-more": ["taxonomy-architecture", "topic-history", "subtopic-modern-movement"],
    "concept-organic-architecture": ["taxonomy-architecture", "topic-history", "subtopic-regionalism"],
    "concept-adaptive-reuse": ["taxonomy-architecture", "topic-history", "subtopic-preservation"],
    "concept-architectural-history": ["taxonomy-architecture", "topic-history", "subtopic-general"],
    "concept-built-heritage": ["taxonomy-architecture", "topic-history", "subtopic-preservation"],
    "concept-architectural-theory": ["taxonomy-architecture", "topic-theory", "subtopic-general"],
    "concept-architectural-interiors": ["taxonomy-architecture", "topic-theory", "subtopic-interiors"],

    # ===== Procedures / Construction Administration =====
    "concept-competitive-bidding": ["taxonomy-procedures", "topic-construction-administration", "subtopic-procurement"],
    "concept-bids-and-awards-committee": ["taxonomy-procedures", "topic-construction-administration", "subtopic-procurement"],
    "concept-approved-budget-for-the-contract": ["taxonomy-procedures", "topic-construction-administration", "subtopic-cost-control"],
    "concept-general-conditions-of-contract": ["taxonomy-procedures", "topic-construction-administration", "subtopic-contracts"],
    "concept-construction-estimating": ["taxonomy-procedures", "topic-construction-administration", "subtopic-cost-control"],
    "concept-simplified-construction-estimate": ["taxonomy-procedures", "topic-construction-administration", "subtopic-cost-control"],
    "concept-area-method": ["taxonomy-procedures", "topic-construction-administration", "subtopic-cost-control"],
    "concept-unit-price-method": ["taxonomy-procedures", "topic-construction-administration", "subtopic-cost-control"],
    "concept-volume-method": ["taxonomy-procedures", "topic-construction-administration", "subtopic-cost-control"],
    "concept-cross-sectional-analysis": ["taxonomy-procedures", "topic-construction-administration", "subtopic-analysis"],
    "concept-continuity-of-instruction": ["taxonomy-procedures", "topic-construction-administration", "subtopic-contracts"],
    "concept-prior-consultations": ["taxonomy-procedures", "topic-construction-administration", "subtopic-contracts"],

    # ===== Professional Practice =====
    "concept-architectural-firm-registration": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-registration"],
    "concept-code-of-ethics": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-ethics"],
    "concept-illegal-practice-of-architecture": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-enforcement"],
    "concept-standards-of-professional-practice": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-standards"],
    "concept-arbitration": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-dispute-resolution"],
    "concept-mediation": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-dispute-resolution"],
    "concept-mediator": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-dispute-resolution"],
    "concept-master-plumber": ["taxonomy-compliance-checks", "topic-professional-practice", "subtopic-registration"],

    # ===== Health / Safety / Social =====
    "concept-school-safety": ["taxonomy-fire-and-life-safety", "topic-life-safety", "subtopic-educational"],
    "concept-health-facility-zoning": ["taxonomy-site-planning", "topic-land-use", "subtopic-health"],
    "concept-local-health-authority": ["taxonomy-compliance-checks", "topic-governance", "subtopic-health"],
    "concept-local-shelter-plan": ["taxonomy-fire-and-life-safety", "topic-life-safety", "subtopic-emergency"],
    "concept-patient-movement": ["taxonomy-compliance-checks", "topic-healthcare", "subtopic-operations"],
    "concept-food-establishment": ["taxonomy-compliance-checks", "topic-healthcare", "subtopic-sanitation"],
    "concept-designated-establishment": ["taxonomy-compliance-checks", "topic-healthcare", "subtopic-sanitation"],
    "concept-disaster-risk-reduction": ["taxonomy-fire-and-life-safety", "topic-life-safety", "subtopic-emergency"],
    "concept-balanced-housing-development": ["taxonomy-site-planning", "topic-housing", "subtopic-policy"],
    "concept-socialized-housing-projects": ["taxonomy-site-planning", "topic-housing", "subtopic-programs"],

    # ===== Miscellaneous / General =====
    "concept-common-areas": ["taxonomy-building-code", "topic-occupancy", "subtopic-shared-spaces"],
    "concept-local-autonomy": ["taxonomy-compliance-checks", "topic-governance", "subtopic-local"],
    "concept-chemical-substance": ["taxonomy-site-planning", "topic-environmental", "subtopic-chemicals"],
    "concept-chemical-mixture": ["taxonomy-site-planning", "topic-environmental", "subtopic-chemicals"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter. Return (frontmatter_dict, body)."""
    m = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}, text
    return fm, text[m.end():]


def _dump_frontmatter(fm: dict, body: str) -> str:
    """Dump frontmatter + body using proper YAML serialization."""
    dumped = yaml.safe_dump(
        fm,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=120,
    )
    return f"---\n{dumped}---\n{body}"


def _make_page(id_: str, title: str, page_type: str, taxonomy_path: list[str]) -> str:
    ts = datetime.now(timezone.utc).isoformat()
    fm = {
        "id": id_,
        "title": title,
        "page_type": page_type,
        "canonical_status": "validated",
        "trust_level": "primary",
        "taxonomy_path": taxonomy_path,
        "last_canonicalized_utc": ts,
    }
    body = f"# {title}\n\n{page_type.capitalize()} node in the Vitruvius canonical knowledge graph.\n"
    return _dump_frontmatter(fm, body)


def _title_from_id(id_: str) -> str:
    # e.g. "topic-administrative" -> "Administrative"
    parts = id_.split("-")
    return " ".join(p.capitalize() for p in parts[1:])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 60)
    print("TAXONOMY REFACTOR")
    print("=" * 60)

    # Ensure directories exist
    TOPIC_DIR.mkdir(parents=True, exist_ok=True)
    SUBTOPIC_DIR.mkdir(parents=True, exist_ok=True)

    concepts_dir = CANONICAL / "concepts"
    concept_files = sorted(concepts_dir.glob("*.md"))
    print(f"\nFound {len(concept_files)} concept files")

    # ------------------------------------------------------------------
    # 1. Identify all taxonomy / topic / subtopic nodes needed
    # ------------------------------------------------------------------
    taxonomies_needed: set[str] = set()
    topics_needed: set[tuple[str, str]] = set()
    subtopics_needed: set[tuple[str, str, str]] = set()
    unclassified: list[str] = []

    for p in concept_files:
        text = p.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)
        cid = fm.get("id", "")
        if cid in CLASSIFICATION:
            path = CLASSIFICATION[cid]
            taxonomies_needed.add(path[0])
            if len(path) >= 2:
                topics_needed.add((path[0], path[1]))
            if len(path) >= 3:
                subtopics_needed.add((path[0], path[1], path[2]))
        else:
            unclassified.append(f"{cid} ({p.name})")

    print(f"\nTaxonomies referenced: {len(taxonomies_needed)}")
    print(f"Topics to create: {len(topics_needed)}")
    print(f"Subtopics to create: {len(subtopics_needed)}")
    if unclassified:
        print(f"\n⚠️  UNCLASSIFIED ({len(unclassified)}):")
        for u in unclassified:
            print(f"  - {u}")

    # ------------------------------------------------------------------
    # 2. Create topic files
    # ------------------------------------------------------------------
    created_topics = 0
    for tax, topic in sorted(topics_needed):
        path = TOPIC_DIR / f"{topic}.md"
        if not path.exists():
            path.write_text(
                _make_page(
                    id_=topic,
                    title=_title_from_id(topic),
                    page_type="topic",
                    taxonomy_path=[tax],
                ),
                encoding="utf-8",
            )
            created_topics += 1
    print(f"\nCreated {created_topics} topic files")

    # ------------------------------------------------------------------
    # 3. Create subtopic files
    # ------------------------------------------------------------------
    created_subtopics = 0
    for tax, topic, subtopic in sorted(subtopics_needed):
        path = SUBTOPIC_DIR / f"{subtopic}.md"
        if not path.exists():
            path.write_text(
                _make_page(
                    id_=subtopic,
                    title=_title_from_id(subtopic),
                    page_type="subtopic",
                    taxonomy_path=[tax, topic],
                ),
                encoding="utf-8",
            )
            created_subtopics += 1
    print(f"Created {created_subtopics} subtopic files")

    # ------------------------------------------------------------------
    # 4. Update concept frontmatter with taxonomy_path
    # ------------------------------------------------------------------
    updated_concepts = 0
    skipped_concepts = 0
    for p in concept_files:
        text = p.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)
        cid = fm.get("id", "")
        if cid in CLASSIFICATION:
            fm["taxonomy_path"] = list(CLASSIFICATION[cid])
            p.write_text(_dump_frontmatter(fm, body), encoding="utf-8")
            updated_concepts += 1
        else:
            skipped_concepts += 1

    print(f"\nUpdated {updated_concepts} concept files with taxonomy_path")
    print(f"Skipped {skipped_concepts} unclassified concept files")

    # ------------------------------------------------------------------
    # 5. Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("REFACTOR COMPLETE")
    print("=" * 60)
    print(f"""
New structure:
  {len(taxonomies_needed)} taxonomies (existing)
  {len(topics_needed)} topics ({created_topics} newly created)
  {len(subtopics_needed)} subtopics ({created_subtopics} newly created)
  {updated_concepts} concepts with taxonomy_path

Next steps:
  1. Inspect a concept: head 003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md
  2. Build unified snapshot: python scripts/pipeline_cli.py kg-build-unified
  3. Query the graph: python scripts/pipeline_cli.py kg-query-nodes "building permit"
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
