from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Dict, Tuple

from .concept_matching import find_concepts_in_text, load_concept_term_map
from .paths import get_repo_root
from .reports import write_json, write_text
from .source_identity import canonical_source_id_for_relative_path
from .utils import utc_now_stamp


# --------------------------------------------------
# LOAD CONCEPTS
# --------------------------------------------------

def load_concepts(*, allowed_paths: Iterable[Path] | None = None) -> Dict[str, str]:
    repo_root = get_repo_root()
    concepts_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    resolved_paths: list[Path] | None = None
    if allowed_paths is not None:
        resolved_paths = []
        for path in allowed_paths:
            candidate = path if path.is_absolute() else repo_root / path
            if candidate.exists() and candidate.is_file():
                resolved_paths.append(candidate)
    return load_concept_term_map(concepts_dir, allowed_paths=resolved_paths)


# --------------------------------------------------
# SECTION SEGMENTATION
# --------------------------------------------------

SECTION_PATTERN = re.compile(
    r"^(?:SECTION|SEC\.)\s+(\d+(?:\.\d+)*)[\.\-:]?\s*(.*)$",
    re.IGNORECASE,
)
NUMBERED_HEADING_PATTERN = re.compile(
    r"^(\d+)\.\s+([A-Z][A-Z0-9 ,/&()\-]+)$"
)


def _normalize_heading_candidate(line: str) -> str:
    stripped = line.strip()
    stripped = re.sub(r"^#+\s*", "", stripped)
    stripped = re.sub(r"^[-*]\s*", "", stripped)
    stripped = re.sub(r"\s+", " ", stripped)
    return stripped.strip()


def _looks_like_toc_entry(candidate: str) -> bool:
    return "...." in candidate or bool(re.search(r"\s+\d+$", candidate))


def split_sections(text: str) -> List[Dict]:
    lines = text.splitlines()
    sections = []

    current = None

    for line in lines:
        candidate = _normalize_heading_candidate(line)
        if not candidate or _looks_like_toc_entry(candidate):
            if current:
                current["lines"].append(line)
            continue

        match = SECTION_PATTERN.match(candidate)
        numbered_match = NUMBERED_HEADING_PATTERN.match(candidate)

        if match:
            if current:
                sections.append(current)

            sec_num = match.group(1)
            title = match.group(2).strip()

            current = {
                "section_id": f"section-{sec_num.lower()}",
                "title": title if title else f"Section {sec_num}",
                "lines": []
            }
        elif numbered_match:
            if current:
                sections.append(current)
            sec_num = numbered_match.group(1)
            title = numbered_match.group(2).strip()
            current = {
                "section_id": f"section-{sec_num.lower()}",
                "title": title,
                "lines": [],
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


def _is_window_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("!["):
        return False
    if stripped.startswith("|") and stripped.endswith("|"):
        return False
    return True


def build_text_windows(lines: List[str], *, min_chars: int = 40) -> List[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if not _is_window_line(line):
            if current:
                paragraphs.append(normalize_text(current))
                current = []
            continue
        current.append(line.strip())
    if current:
        paragraphs.append(normalize_text(current))

    windows: list[str] = []
    for paragraph in paragraphs:
        sentences = re.split(r"(?<=[.!?;:])\s+", paragraph)
        for sentence in sentences:
            cleaned = sentence.strip()
            if len(cleaned) >= min_chars:
                windows.append(cleaned)
        if len(paragraph) >= min_chars:
            windows.append(paragraph)

    deduped: list[str] = []
    seen: set[str] = set()
    for window in windows:
        if window not in seen:
            seen.add(window)
            deduped.append(window)
    return deduped


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
    return find_concepts_in_text(text, concept_map)


# --------------------------------------------------
# SOURCE ID
# --------------------------------------------------

def build_source_id(relative_path: str) -> str:
    return canonical_source_id_for_relative_path(relative_path)


# --------------------------------------------------
# EXTRACTION PER SECTION
# --------------------------------------------------

def extract_section_relationships(
    section: Dict,
    concept_map: Dict[str, str],
    source_id: str
) -> List[Dict]:

    relationships = []

    windows = build_text_windows(section["lines"])
    if not windows:
        text = normalize_text(section["lines"])
        if text:
            windows = [text]

    for text in windows:
        found = find_concepts(text, concept_map)
        if not found:
            continue

        for pattern, rel_type in PATTERNS:
            if not re.search(pattern, text.lower()):
                continue

            if len(found) >= 2:
                if rel_type == "defines":
                    # `defines` is only registry-compatible for source->concept
                    # style edges. Emitting concept->concept `defines` from a
                    # noisy shared window creates obvious false positives such
                    # as "stairs defines ramps". Keep the safer law->concept
                    # path for define-like language and let richer relation
                    # types come from more explicit patterns.
                    continue
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

def run_extract_relationships_sections_one(
    *,
    relative_markdown_path: str,
    json_output_path: Path | None = None,
    txt_output_path: Path | None = None,
    source_id_override: str | None = None,
    concept_paths: Iterable[Path] | None = None,
) -> int:
    return run_extract_relationships_sections_one_inner(
        repo_root=get_repo_root(),
        relative_markdown_path=relative_markdown_path,
        json_output_path=json_output_path,
        txt_output_path=txt_output_path,
        source_id_override=source_id_override,
        concept_paths=concept_paths,
    )


def run_extract_relationships_sections_one_inner(
    *,
    repo_root: Path,
    relative_markdown_path: str,
    json_output_path: Path | None = None,
    txt_output_path: Path | None = None,
    source_id_override: str | None = None,
    concept_paths: Iterable[Path] | None = None,
    source_path: Path | None = None,
) -> int:
    if source_path is None:
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
    concept_map = load_concepts(allowed_paths=concept_paths)
    source_id = source_id_override or build_source_id(relative_markdown_path)

    all_relationships = []

    for section in sections:
        rels = extract_section_relationships(section, concept_map, source_id)
        all_relationships.extend(rels)

    aggregated = aggregate_relationships(all_relationships)

    # Sprint CLEANUP-1 C4.3 — optional Phase 5E LLM-assisted extraction.
    # Flag-gated behind `p5e_llm_extraction`. Flag-off is byte-identical —
    # aggregated flows unchanged to dedupe. Flag-on runs the LLM proposer
    # for each section, then merges the LLM candidates with `aggregated`
    # (regex wins on overlap). Any exception falls back to regex-only.
    try:
        from vitruvius.spatial._feature_gate import _load_features_cached
        _features = _load_features_cached()
    except Exception:
        _features = None

    if _features is not None and _features.is_enabled("p5e_llm_extraction"):
        try:
            from vitruvius.relationships.llm_proposer import propose_relationships_llm
            from vitruvius.relationships.phase_5e_merger import merge_regex_and_llm

            llm_candidates = []
            for section in sections:
                sec_id = section.get("section_id", "section-unknown")
                sec_text = normalize_text(section.get("lines", []))
                if not sec_text:
                    continue
                llm_candidates.extend(
                    propose_relationships_llm(
                        section_text=sec_text,
                        section_id=sec_id,
                        source_id=source_id,
                    )
                )
            aggregated = merge_regex_and_llm(aggregated, llm_candidates)
        except Exception:
            # Graceful degrade: fall through with regex-only candidates
            pass

    # Sprint LSH-1 — optional fuzzy near-duplicate layer per AD-037.
    # Off by default (plan §1.3 non-breaking contract). On a
    # byte-identical run the flag-off path must produce exactly the
    # same deduped list as the pre-LSH-1 baseline.
    try:
        from vitruvius.config import _features_block
        use_lsh = bool(_features_block().get("w_lsh_dedup", False))
    except Exception:
        use_lsh = False

    if use_lsh:
        from vitruvius.relationships.lsh_dedup import dedupe_by_endpoints_lsh
        deduped = dedupe_by_endpoints_lsh(aggregated)
    else:
        deduped = dedupe_by_endpoints(aggregated)

    report = {
        "generated_at": utc_now_stamp(),
        "source": relative_markdown_path,
        "source_id": source_id,
        "total_sections": len(sections),
        "total_relationships": len(deduped),
        "relationships": deduped,
    }

    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_output_path or runs_dir / "latest_relationship_extraction_sections.json"
    txt_path = txt_output_path or runs_dir / "latest_relationship_extraction_sections.txt"

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
