"""Stream L.4 — concept mapper tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.spatial.concept_mapper import (
    MappingResult,
    load_known_concepts,
    resolve_mapping,
)
from vitruvius.spatial.walker import SpatialCandidate


def _make_candidate(concept_id: str) -> SpatialCandidate:
    return SpatialCandidate(
        spatial_context_id="spatial-test-01",
        instance_id="instance-a-01",
        canonical_concept_id=concept_id,
        bounding_box_min=None,
        bounding_box_max=None,
        source_file="a.json",
    )


def _write_concept(dir_path: Path, slug: str, concept_id: str) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / f"{slug}.md").write_text(
        f"---\nid: {concept_id}\npage_type: concept\n"
        f"canonical_status: enriched\n"
        f"last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n\n# {slug}\n",
        encoding="utf-8",
    )


def test_resolve_mapping_direct_match() -> None:
    candidate = _make_candidate("concept-means-of-egress")
    known = frozenset({"concept-means-of-egress", "concept-doors-and-exits"})
    result = resolve_mapping(candidate, known_concepts=known)
    assert isinstance(result, MappingResult)
    assert result.is_known_concept is True
    assert result.resolution_method == "direct"
    assert result.canonical_concept_id == "concept-means-of-egress"
    assert result.instance_id == "instance-a-01"


def test_resolve_mapping_unknown_concept() -> None:
    candidate = _make_candidate("concept-nonexistent")
    known = frozenset({"concept-means-of-egress"})
    result = resolve_mapping(candidate, known_concepts=known)
    assert result.is_known_concept is False
    assert result.resolution_method == "unknown"


def test_resolve_mapping_empty_known_concepts() -> None:
    candidate = _make_candidate("concept-anything")
    result = resolve_mapping(candidate, known_concepts=frozenset())
    assert result.is_known_concept is False
    assert result.resolution_method == "unknown"


def test_load_known_concepts_from_tmp_dir(tmp_path: Path) -> None:
    _write_concept(tmp_path, "means-of-egress", "concept-means-of-egress")
    _write_concept(tmp_path, "doors-and-exits", "concept-doors-and-exits")
    known = load_known_concepts(tmp_path)
    assert isinstance(known, frozenset)
    assert "concept-means-of-egress" in known
    assert "concept-doors-and-exits" in known
    assert len(known) == 2


def test_load_known_concepts_missing_dir(tmp_path: Path) -> None:
    missing = tmp_path / "nonexistent"
    known = load_known_concepts(missing)
    assert known == frozenset()


def test_load_known_concepts_skips_files_without_frontmatter(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "no-frontmatter.md").write_text("# just a heading\n", encoding="utf-8")
    _write_concept(tmp_path, "real-concept", "concept-real")
    known = load_known_concepts(tmp_path)
    assert known == frozenset({"concept-real"})


def test_mapping_result_is_frozen() -> None:
    candidate = _make_candidate("concept-x")
    result = resolve_mapping(candidate, known_concepts=frozenset({"concept-x"}))
    with pytest.raises(Exception):
        result.resolution_method = "other"  # type: ignore[misc]


def test_load_known_concepts_case_sensitive(tmp_path: Path) -> None:
    _write_concept(tmp_path, "mixed", "concept-Mixed-Case")
    known = load_known_concepts(tmp_path)
    candidate = _make_candidate("concept-mixed-case")
    result = resolve_mapping(candidate, known_concepts=known)
    assert result.is_known_concept is False


def test_load_known_concepts_handles_bad_yaml(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "broken.md").write_text(
        "---\nid: [unclosed list\n---\n",
        encoding="utf-8",
    )
    _write_concept(tmp_path, "good", "concept-good")
    known = load_known_concepts(tmp_path)
    assert "concept-good" in known
