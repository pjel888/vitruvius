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

    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": utc_now_stamp(),
        "source": relative_markdown_path,
        "total_sections": len(sections),
        "total_relationships": len(aggregated),
        "relationships": aggregated,
    }

    json_path = runs_dir / "latest_relationship_extraction_sections.json"
    txt_path = runs_dir / "latest_relationship_extraction_sections.txt"

    write_json(json_path, report)

    lines = []
    lines.append("Section-Aware Relationship Extraction\n")
    lines.append(f"Sections: {len(sections)}")
    lines.append(f"Unique relationships: {len(aggregated)}\n")

    for rel in aggregated:
        lines.append(
            f"{rel['from']} -> {rel['type']} -> {rel['to']} "
            f"(x{rel['occurrences']}) sections={rel['sections']}"
        )

    write_text(txt_path, "\n".join(lines))

    print("extract-relationships-sections-one complete.")
    print(f"Sections processed: {len(sections)}")
    print(f"Unique relationships: {len(aggregated)}")
    print(f"JSON: {json_path}")
    print(f"TXT: {txt_path}")

    return 0