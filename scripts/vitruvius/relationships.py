from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Tuple

from .concept_matching import find_concepts_in_text, load_concept_term_map
from .paths import get_repo_root
from .reports import write_json, write_text
from .source_identity import canonical_source_id_for_relative_path
from .utils import utc_now_stamp


# --------------------------------------------------
# LOAD CONCEPTS
# --------------------------------------------------

def load_concepts() -> Dict[str, str]:
    repo_root = get_repo_root()
    concepts_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    return load_concept_term_map(concepts_dir)


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
# TEXT WINDOWS
# --------------------------------------------------

def build_windows(lines: List[str], size: int = 3) -> List[str]:
    windows = []

    for i in range(len(lines)):
        chunk = " ".join(lines[i:i+size]).strip()

        if len(chunk) > 40:
            windows.append(chunk)

    return windows


# --------------------------------------------------
# CONCEPT MATCHING (IMPROVED)
# --------------------------------------------------

def find_concepts(text: str, concept_map: Dict[str, str]) -> List[str]:
    return find_concepts_in_text(text, concept_map)


# --------------------------------------------------
# SOURCE ID
# --------------------------------------------------

def build_source_id(relative_path: str) -> str:
    return canonical_source_id_for_relative_path(relative_path)


# --------------------------------------------------
# EXTRACTION (WITH AGGREGATION)
# --------------------------------------------------

def extract_relationships(
    text: str,
    concept_map: Dict[str, str],
    source_id: str
) -> Dict[Tuple[str, str, str], Dict]:

    relationships = {}

    lines = text.splitlines()
    windows = build_windows(lines, size=3)

    for window in windows:
        window_lower = window.lower()

        found = find_concepts(window, concept_map)

        if not found:
            continue

        for pattern, rel_type in PATTERNS:
            if not re.search(pattern, window_lower):
                continue

            # ----------------------------------
            # CASE 1: CONCEPT → CONCEPT
            # ----------------------------------
            if len(found) >= 2:
                key = (found[0], rel_type, found[1])

                if key not in relationships:
                    relationships[key] = {
                        "from": found[0],
                        "type": rel_type,
                        "to": found[1],
                        "occurrences": 0,
                        "examples": []
                    }

                relationships[key]["occurrences"] += 1

                if len(relationships[key]["examples"]) < 3:
                    relationships[key]["examples"].append(window.strip())

            # ----------------------------------
            # CASE 2: LAW → CONCEPT
            # ----------------------------------
            elif len(found) == 1:
                key = (source_id, "governs", found[0])

                if key not in relationships:
                    relationships[key] = {
                        "from": source_id,
                        "type": "governs",
                        "to": found[0],
                        "occurrences": 0,
                        "examples": []
                    }

                relationships[key]["occurrences"] += 1

                if len(relationships[key]["examples"]) < 3:
                    relationships[key]["examples"].append(window.strip())

    return relationships


# --------------------------------------------------
# COMMAND
# --------------------------------------------------

def run_extract_relationships_one(*, relative_markdown_path: str) -> int:
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

    concept_map = load_concepts()
    source_id = build_source_id(relative_markdown_path)

    rel_map = extract_relationships(text, concept_map, source_id)

    relationships = list(rel_map.values())

    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": utc_now_stamp(),
        "source": relative_markdown_path,
        "source_id": source_id,
        "total_relationships": len(relationships),
        "relationships": relationships,
    }

    json_path = runs_dir / "latest_relationship_extraction.json"
    txt_path = runs_dir / "latest_relationship_extraction.txt"

    write_json(json_path, report)

    lines = []
    lines.append("Relationship Extraction Report\n")
    lines.append(f"Source: {relative_markdown_path}")
    lines.append(f"Unique relationships: {len(relationships)}\n")

    for rel in relationships:
        lines.append(
            f"{rel['from']} -> {rel['type']} -> {rel['to']} "
            f"(x{rel['occurrences']})"
        )

    write_text(txt_path, "\n".join(lines))

    print("extract-relationships-one complete.")
    print(f"Unique relationships: {len(relationships)}")
    print(f"JSON: {json_path}")
    print(f"TXT: {txt_path}")

    return 0
