"""Stream W3.3 — resolve_stringency is called during promotion conflict."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.promotion import _maybe_resolve_stringency_conflict
from vitruvius.promotion.stringency_resolver import CandidateEdge, StringencyVerdict


def _edge(edge_id: str, value: float | None) -> CandidateEdge:
    return CandidateEdge(
        edge_id=edge_id,
        from_entity="concept-zone-r2",
        predicate="requires",
        to_entity="concept-setbacks",
        numeric_value=value,
        jurisdiction="national" if edge_id == "rel-a" else "lgu-quezon-city",
    )


def test_winner_is_tagged_governing_when_flag_on(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_promotion_stringency_gate": True},
    )
    # Stub concept lookup to return a maximize-vector concept
    import vitruvius.promotion as prom
    monkeypatch.setattr(
        prom, "_concept_stringency_vector",
        lambda cid: "maximize",
    )

    edge_a = _edge("rel-a", 2.0)  # national
    edge_b = _edge("rel-b", 3.0)  # LGU (stricter)

    result = _maybe_resolve_stringency_conflict(edge_a, edge_b)
    assert result is not None
    assert result["winner_edge_id"] == "rel-b"
    assert result["loser_edge_id"] == "rel-a"
    assert result["is_governing_standard"] is True


def test_resolver_is_noop_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_promotion_stringency_gate": False},
    )
    edge_a = _edge("rel-a", 2.0)
    edge_b = _edge("rel-b", 3.0)
    assert _maybe_resolve_stringency_conflict(edge_a, edge_b) is None


def test_unresolved_qualitative_returns_none(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_promotion_stringency_gate": True},
    )
    import vitruvius.promotion as prom
    monkeypatch.setattr(
        prom, "_concept_stringency_vector",
        lambda cid: "qualitative",
    )
    edge_a = _edge("rel-a", None)
    edge_b = _edge("rel-b", None)
    result = _maybe_resolve_stringency_conflict(edge_a, edge_b)
    # Qualitative + both None → unresolved; the wire returns None so the
    # promotion path keeps both without a governing tag.
    assert result is None
