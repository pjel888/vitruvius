"""Stream L.8 — backward-compat regression for 3D spatial upgrade.

Locks the non-breaking guarantee. With every 3D feature flag OFF, the
Phase 8 graph builder must produce a snapshot byte-identical to the
checked-in fixture. Also verifies that the contract additions do not
affect existing validate_node/validate_edge behaviour.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.graph.builder import build_snapshot
from vitruvius.graph.contract import (
    ALLOWED_EDGE_STATUSES,
    ALLOWED_ID_PREFIXES,
    ALLOWED_NODE_TYPES,
    ContractViolation,
    GraphEdge,
    GraphNode,
    validate_edge,
    validate_node,
)
from vitruvius.graph.snapshot import _snapshot_to_dict


FIX = Path(__file__).resolve().parent / "fixtures" / "spatial"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_minimal_canonical_tree(root: Path) -> None:
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    _write(
        shared / "sources" / "pd-1096.md",
        "---\nid: law-pd-1096\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
    )
    _write(
        shared / "concepts" / "building-permit.md",
        "---\nid: concept-building-permit\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
    )
    _write(
        shared / "relationships" / "pd-1096-governs-building-permit.md",
        "---\nid: rel-pd-1096-governs-building-permit\n"
        "page_type: relationship\nrelationship_type: governs\n"
        "from_entity: law-pd-1096\nto_entity: concept-building-permit\n"
        "canonical_status: promoted\n---\n",
    )


def test_flag_off_snapshot_matches_frozen_expectation(tmp_path: Path) -> None:
    _seed_minimal_canonical_tree(tmp_path)
    snapshot = build_snapshot(
        tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
        now="2026-04-15T00:00:00Z",
    )
    actual = _snapshot_to_dict(snapshot)
    expected = json.loads((FIX / "expected_frozen_snapshot.json").read_text())
    assert actual == expected, (
        "Phase 8 graph drifted. Check Stream L contract extensions are "
        "truly additive and 3D flags default OFF."
    )


def test_flag_off_snapshot_is_deterministic_across_runs(tmp_path: Path) -> None:
    _seed_minimal_canonical_tree(tmp_path)
    s1 = _snapshot_to_dict(
        build_snapshot(
            tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
            now="2026-04-15T00:00:00Z",
        )
    )
    s2 = _snapshot_to_dict(
        build_snapshot(
            tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
            now="2026-04-15T00:00:00Z",
        )
    )
    assert s1 == s2


def test_contract_additions_do_not_break_existing_nodes() -> None:
    node = GraphNode(
        id="law-pd-1096",
        type="source",
        slug="pd-1096",
        trust_level="primary",
        last_updated_utc="2026-04-01T00:00:00Z",
    )
    validate_node(node)

    concept = GraphNode(
        id="concept-building-permit",
        type="concept",
        slug="building-permit",
        trust_level="derived",
        last_updated_utc="2026-04-01T00:00:00Z",
    )
    validate_node(concept)

    edge = GraphEdge(
        from_id="law-pd-1096",
        to_id="concept-building-permit",
        type="governs",
        evidence_id="rel-pd-1096-governs-building-permit",
        status="verified",
    )
    validate_edge(edge)

    bad = GraphNode(
        id="not-a-prefix",
        type="source",
        slug="x",
        trust_level="primary",
        last_updated_utc="2026-04-01T00:00:00Z",
    )
    with pytest.raises(ContractViolation):
        validate_node(bad)


def test_contract_sets_are_strictly_additive() -> None:
    legacy_node_types = {"source", "concept", "attribute"}
    legacy_edge_statuses = {"verified", "unverified"}
    legacy_prefixes = {
        "law-",
        "irr-",
        "concept-",
        "rel-",
        "source-",
        "handout-",
        "reviewer-",
        "law-section-",
    }
    assert legacy_node_types.issubset(ALLOWED_NODE_TYPES)
    assert legacy_edge_statuses.issubset(ALLOWED_EDGE_STATUSES)
    assert legacy_prefixes.issubset(ALLOWED_ID_PREFIXES)
    assert "spatial_instance" in ALLOWED_NODE_TYPES
    assert "spatially_verified" in ALLOWED_EDGE_STATUSES
    assert "instance-" in ALLOWED_ID_PREFIXES
    assert "spatial-" in ALLOWED_ID_PREFIXES
