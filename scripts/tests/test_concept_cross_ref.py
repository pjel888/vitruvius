"""Sprint CLEANUP-1 Stream C2.2 — bidirectional concept cross-ref linker tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.concept_cross_ref import (
    build_concept_cross_ref_map,
)


def _write_relationship(relationships_dir: Path, filename: str, yaml_body: str) -> None:
    (relationships_dir / filename).write_text(yaml_body, encoding="utf-8")


def test_empty_relationships_dir_returns_empty_map(tmp_path: Path) -> None:
    relationships_dir = tmp_path / "relationships"
    relationships_dir.mkdir()
    result = build_concept_cross_ref_map(relationships_dir)
    assert result == {}


def test_single_edge_populates_both_sides(tmp_path: Path) -> None:
    relationships_dir = tmp_path / "relationships"
    relationships_dir.mkdir()
    _write_relationship(
        relationships_dir,
        "rel-concept-setbacks-depends-on-concept-yards.md",
        """---
id: rel-concept-setbacks-depends-on-concept-yards
relationship_type: depends_on
from_entity: concept-setbacks
to_entity: concept-yards
canonical_status: promoted
---

# concept-setbacks depends_on concept-yards
""",
    )
    result = build_concept_cross_ref_map(relationships_dir)
    assert result["concept-setbacks"] == ["concept-yards"]
    assert result["concept-yards"] == ["concept-setbacks"]


def test_multiple_edges_bidirectional_and_deduped(tmp_path: Path) -> None:
    relationships_dir = tmp_path / "relationships"
    relationships_dir.mkdir()
    _write_relationship(
        relationships_dir,
        "rel-concept-yards-depends-on-concept-setbacks.md",
        """---
id: rel-concept-yards-depends-on-concept-setbacks
relationship_type: depends_on
from_entity: concept-yards
to_entity: concept-setbacks
---
""",
    )
    _write_relationship(
        relationships_dir,
        "rel-concept-yards-affects-concept-setbacks.md",
        """---
id: rel-concept-yards-affects-concept-setbacks
relationship_type: affects
from_entity: concept-yards
to_entity: concept-setbacks
---
""",
    )
    result = build_concept_cross_ref_map(relationships_dir)
    # Bidirectional, each appears once per list (deduped)
    assert result["concept-yards"] == ["concept-setbacks"]
    assert result["concept-setbacks"] == ["concept-yards"]
