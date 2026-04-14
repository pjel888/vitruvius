from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Tuple

from .paths import get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


# --------------------------------------------------
# LOAD CONCEPTS
# --------------------------------------------------

def load_concepts() -> Dict[str, str]:
    repo_root = get_repo_root()
    concepts_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"

    concept_map = {}

    for file in concepts_dir.glob("*.md"):
        slug = file.stem
        phrase = slug.replace("-", " ")
        concept_map[phrase] = f"concept-{slug}"

    return concept_map


# --------------------------------------------------
# SECTION SEGMENTATION
# --------------------------------------------------

SECTION_PATTERN = re.compile(r"(SECTION|SEC\.)\s+(\d+)[\.\-]?\s*(.*)", re.IGNORECASE)


def split_sections(text: str) -> List[Dict]:
    lines = text.splitlines()
    sections = []

    current = None

    for line in lines:
        match = SECTION_PATTERN.match(line.strip())

        if match:
            if current:
                sections.append(current)

            sec_num = match.group(2)
            title = match.group(3).strip()

            current = {
                "section_id": f"section-{sec_num}",
                "title": title if title else f"Section {sec_num}",
                "lines": []
            }
        elif current:
            current["lines"].append(line)

    if current:
        sections.append(current)

    return sections


# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------

def normalize_text(lines: List[str]) -> str:
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# --------------------------------------------------
# PATTERNS
# --------------------------------------------------

PATTERNS = [
    (r"shall comply with", "requires"),
    (r"as defined in", "defines"),
    (r"subject to", "depends_on"),
    (r"shall not exceed", "limits"),
    (r"used for determining", "affects"),
    (r"determine[s]?", "affects"),
    (r"shall be", "defines"),
    (r"required to", "requires"),
]


# --------------------------------------------------
# CONCEPT MATCHING
# --------------------------------------------------

def find_concepts(text: str, concept_map: Dict[str, str]) -> List[str]:
    text_lower = text.lower()
    matches = []

    for phrase, cid in concept_map.items():
        if phrase in text_lower:
            matches.append(cid)

    return list(set(matches))


# --------------------------------------------------
# SOURCE ID
# --------------------------------------------------

def build_source_id(relative_path: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", Path(relative_path).stem.lower()).strip("-")

    if "irr" in slug:
        return "irr-implementing-rules-and-regulations-of-the-national-building-code"

    return "law-national-building-code-of-the-philippines"


# --------------------------------------------------
# EXTRACTION PER SECTION
# --------------------------------------------------

def extract_section_relationships(
    section: Dict,
    concept_map: Dict[str, str],
    source_id: str
) -> List[Dict]:

    relationships = []

    text = normalize_text(section["lines"])

    found = find_concepts(text, concept_map)

    if not found:
        return relationships

    for pattern, rel_type in PATTERNS:
        if not re.search(pattern, text.lower()):
            continue

        if len(found) >= 2:
            relationships.append({
                "from": found[0],
                "type": rel_type,
                "to": found[1],
                "section": section["section_id"],
                "section_title": section["title"],
                "source_text": text[:300]
            })

        elif len(found) == 1:
            relationships.append({
                "from": source_id,
                "type": "governs",
                "to": found[0],
                "section": section["section_id"],
                "section_title": section["title"],
                "source_text": text[:300]
            })

    return relationships


# --------------------------------------------------
# AGGREGATION
# --------------------------------------------------

# --------------------------------------------------
# ENDPOINT-PAIR DEDUPLICATION
# --------------------------------------------------

PREDICATE_PRIORITY = [
    "governs",
    "defines",
    "requires",
    "depends_on",
    "limits",
    "affects",
    "supersedes",
]


def _priority_rank(predicate: str) -> int:
    try:
        return PREDICATE_PRIORITY.index(predicate)
    except ValueError:
        return len(PREDICATE_PRIORITY)


def _infer_entity_type(entity_id: str) -> str:
    """Infer a canonical entity type from its ID prefix.

    Used by dedupe_by_endpoints to check registry compatibility without
    requiring a full canonical-index load. Prefixes that map to `source`:
    law-, irr-, source-, handout-, reviewer-, law-section-. `concept-`
    maps to concept. `attribute-` maps to attribute. Anything else falls
    back to the raw first segment (useful for debugging).
    """
    if not isinstance(entity_id, str):
        return "unknown"
    source_prefixes = ("law-", "irr-", "source-", "handout-", "reviewer-", "law-section-")
    if any(entity_id.startswith(p) for p in source_prefixes):
        return "source"
    if entity_id.startswith("concept-"):
        return "concept"
    if entity_id.startswith("attribute-"):
        return "attribute"
    if entity_id.startswith("section-"):
        return "section"
    return "unknown"


def _load_registry_compat_table() -> dict[str, set[tuple[str, str]]]:
    """Load the relationship registry and flatten it into a compatibility
    lookup table: predicate -> set of (subject_type, object_type) pairs.

    Returns an empty table if the registry file is missing or unparseable —
    in that case dedupe_by_endpoints degrades to priority-only behavior.
    """
    import yaml

    path = get_repo_root() / "scripts" / "vitruvius" / "rules" / "relationship_registry.yaml"
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return {}

    table: dict[str, set[tuple[str, str]]] = {}
    for predicate, spec in (data.get("predicates") or {}).items():
        pairs: set[tuple[str, str]] = set()
        for pair in spec.get("allowed_pairs", []) or []:
            s = pair.get("subject_type")
            o = pair.get("object_type")
            if s and o:
                pairs.add((s, o))
        table[predicate] = pairs
    return table


def dedupe_by_endpoints(candidates: List[Dict]) -> List[Dict]:
    """Collapse multiple (from, X, to) candidates into one per (from, to).

    The regex extractor produces up to 5 candidates for the same endpoint pair
    because 5 predicate patterns can each match the same section text. Given
    the review layer rejects most of them as false positives, we dedup before
    review.

    Selection order:
      1. Partition candidates by (from, to).
      2. For each pair, infer the (from_type, to_type) from ID prefixes.
      3. Prefer candidates whose predicate is REGISTRY-COMPATIBLE with that
         type pair. If any compatible candidates exist, pick only from them.
      4. Within the preferred subset, pick highest `occurrences`, tie-broken
         by PREDICATE_PRIORITY (lower rank wins).
      5. If NO predicate is registry-compatible, fall back to the full group
         with priority-only selection. The resulting candidate will likely be
         rejected at Rule 7 downstream but we don't silently discard it.

    This is the fix for the 2026-04-14 post-dedup experiment finding: the
    priority-only picker chose `defines` for concept->concept edges, losing
    three promotions that would have been valid under `requires` / `affects`
    / `depends_on`.

    Sections and examples from all dropped siblings are merged into the
    survivor. Dropped predicates are recorded in `alternate_predicates` so
    Phase 6B can revisit them.
    """
    from collections import defaultdict

    compat = _load_registry_compat_table()

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for cand in candidates:
        groups[(cand["from"], cand["to"])].append(cand)

    result: list[dict] = []
    for (from_id, to_id), group in groups.items():
        from_type = _infer_entity_type(from_id)
        to_type = _infer_entity_type(to_id)
        type_pair = (from_type, to_type)

        # Filter to candidates whose predicate is registry-compatible for
        # this endpoint type pair. Empty compat table (no registry) or no
        # matches -> fall back to the full group.
        if compat:
            compatible = [
                c for c in group
                if type_pair in compat.get(c["type"], set())
            ]
        else:
            compatible = []
        selection_pool = compatible if compatible else group

        group_sorted = sorted(
            selection_pool,
            key=lambda c: (-int(c.get("occurrences", 0)), _priority_rank(c["type"])),
        )
        winner = dict(group_sorted[0])

        alternates: list[str] = []
        merged_sections: list = list(winner.get("sections", []))
        merged_examples: list = list(winner.get("examples", []))
        for other in group_sorted[1:]:
            if other["type"] != winner["type"]:
                alternates.append(other["type"])
            for s in other.get("sections", []):
                if s not in merged_sections:
                    merged_sections.append(s)
            for ex in other.get("examples", []):
                if ex not in merged_examples and len(merged_examples) < 5:
                    merged_examples.append(ex)

        winner["sections"] = merged_sections
        winner["examples"] = merged_examples
        winner["alternate_predicates"] = alternates
        result.append(winner)

    return result


def aggregate_relationships(rel_list: List[Dict]) -> List[Dict]:
    agg: Dict[Tuple[str, str, str], Dict] = {}

    for rel in rel_list:
        key = (rel["from"], rel["type"], rel["to"])

        if key not in agg:
            agg[key] = {
                "from": rel["from"],
                "type": rel["type"],
                "to": rel["to"],
                "occurrences": 0,
                "sections": [],
                "examples": []
            }

        agg[key]["occurrences"] += 1

        if rel["section"] not in agg[key]["sections"]:
            agg[key]["sections"].append(rel["section"])

        if len(agg[key]["examples"]) < 3:
            agg[key]["examples"].append(rel["source_text"])

    return list(agg.values())


# --------------------------------------------------
# COMMAND
# --------------------------------------------------

def run_extract_relationships_sections_one(*, relative_markdown_path: str) -> int:
    repo_root = get_repo_root()

    source_path = (
        repo_root
        / "002_Raw-Conversion-Layer"
        / relative_markdown_path
    )

    if not source_path.exists():
        print(f"ERROR: Source not found: {source_path}")
        return 1

    text = source_path.read_text(encoding="utf-8", errors="ignore")

    sections = split_sections(text)
    concept_map = load_concepts()
    source_id = build_source_id(relative_markdown_path)

    all_relationships = []

    for section in sections:
        rels = extract_section_relationships(section, concept_map, source_id)
        all_relationships.extend(rels)

    aggregated = aggregate_relationships(all_relationships)
    deduped = dedupe_by_endpoints(aggregated)

    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": utc_now_stamp(),
        "source": relative_markdown_path,
        "total_sections": len(sections),
        "total_relationships": len(deduped),
        "relationships": deduped,
    }

    json_path = runs_dir / "latest_relationship_extraction_sections.json"
    txt_path = runs_dir / "latest_relationship_extraction_sections.txt"

    write_json(json_path, report)

    lines = []
    lines.append("Section-Aware Relationship Extraction\n")
    lines.append(f"Sections: {len(sections)}")
    lines.append(f"Unique relationships: {len(deduped)}\n")

    for rel in deduped:
        alt_str = f" alt={rel.get('alternate_predicates')}" if rel.get('alternate_predicates') else ""
        lines.append(
            f"{rel['from']} -> {rel['type']} -> {rel['to']} "
            f"(x{rel['occurrences']}) sections={rel['sections']}{alt_str}"
        )

    write_text(txt_path, "\n".join(lines))

    print("extract-relationships-sections-one complete.")
    print(f"Sections processed: {len(sections)}")
    print(f"Unique relationships: {len(deduped)}")
    print(f"JSON: {json_path}")
    print(f"TXT: {txt_path}")

    return 0