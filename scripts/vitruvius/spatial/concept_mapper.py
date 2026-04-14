"""Stream L.4 — map spatial candidates to canonical concepts.

The mapper only verifies that a candidate's canonical_concept_id exists
in the canonical layer's concept set. Fallback resolution (alias lookup,
fuzzy match) is deferred — an unknown concept ID returns a MappingResult
with is_known_concept=False and resolution_method='unknown'. The caller
can then decide whether to escalate, skip, or flag the instance.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .walker import SpatialCandidate


@dataclass(frozen=True)
class MappingResult:
    instance_id: str
    canonical_concept_id: str
    is_known_concept: bool
    resolution_method: str


def load_known_concepts(concepts_dir: Path) -> frozenset[str]:
    if not concepts_dir.exists() or not concepts_dir.is_dir():
        return frozenset()
    known: set[str] = set()
    for path in sorted(concepts_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[3:end].strip()) or {}
        except yaml.YAMLError:
            continue
        cid = fm.get("id") if isinstance(fm, dict) else None
        if isinstance(cid, str) and cid.startswith("concept-"):
            known.add(cid)
    return frozenset(known)


def resolve_mapping(
    candidate: SpatialCandidate,
    *,
    known_concepts: frozenset[str],
) -> MappingResult:
    concept_id = candidate.canonical_concept_id
    if concept_id in known_concepts:
        return MappingResult(
            instance_id=candidate.instance_id,
            canonical_concept_id=concept_id,
            is_known_concept=True,
            resolution_method="direct",
        )
    return MappingResult(
        instance_id=candidate.instance_id,
        canonical_concept_id=concept_id,
        is_known_concept=False,
        resolution_method="unknown",
    )
