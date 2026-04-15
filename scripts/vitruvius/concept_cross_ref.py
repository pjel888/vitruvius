"""Sprint CLEANUP-1 Stream C2.2 — bidirectional concept cross-reference linker.

Walks the promoted relationship files under
003_Canonical-Knowledge-Layer/shared/relationships/, extracts every
directed edge (from_entity, predicate, to_entity), and returns a map
from concept-id -> sorted list of related concept-ids (both directions,
deduped).

Used by concept_enrichment.py::_render_enriched when
`p3_bidirectional_refs` is on to inject `related_concepts: [...]` into
enriched concept frontmatter.

Perf call: pure YAML parse + dict ops, above the Rust Line (AD-036).
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import yaml

_CONCEPT_PREFIX = "concept-"


def _parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def build_concept_cross_ref_map(
    relationships_dir: Path,
) -> Dict[str, List[str]]:
    """Return concept-id -> sorted list of related concept-ids, both directions."""
    pairs: Dict[str, set] = defaultdict(set)

    for rel_file in sorted(relationships_dir.glob("rel-concept-*.md")):
        fm = _parse_frontmatter(rel_file.read_text(encoding="utf-8"))
        from_id = fm.get("from_entity")
        to_id = fm.get("to_entity")
        if not isinstance(from_id, str) or not isinstance(to_id, str):
            continue
        if not from_id.startswith(_CONCEPT_PREFIX) or not to_id.startswith(_CONCEPT_PREFIX):
            continue
        pairs[from_id].add(to_id)
        pairs[to_id].add(from_id)

    return {concept: sorted(related) for concept, related in pairs.items()}
