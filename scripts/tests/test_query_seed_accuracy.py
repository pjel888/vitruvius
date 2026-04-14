"""Phase 9 Task 7 — seed-question accuracy suite."""

from __future__ import annotations

from pathlib import Path

import yaml

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.query.engine import (
    edges_between,
    neighbors_query,
    supersession_chain,
    what_affects,
    what_defines,
    what_depends_on,
    what_governs,
    what_limits,
    what_requires,
)
from vitruvius.query.nl_translator import translate_question


_FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "seed_questions.yaml"


_ENGINE = {
    "what_governs": what_governs,
    "what_requires": what_requires,
    "what_limits": what_limits,
    "what_defines": what_defines,
    "what_depends_on": what_depends_on,
    "what_affects": what_affects,
    "supersession_chain": supersession_chain,
    "neighbors": neighbors_query,
    "edges_between": edges_between,
}


def _n(id_: str, *, type_: str = "concept", trust: str = "derived") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
        slug=id_.split("-", 1)[-1] or "x",
        trust_level=trust,
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(
    from_id: str,
    to_id: str,
    *,
    type_: str,
    evidence: str,
    status: str = "verified",
) -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
        evidence_id=evidence,
        status=status,
    )


def _seed_snapshot() -> GraphSnapshot:
    nodes = [
        _n("law-pd-1096", type_="source", trust="primary"),
        _n("law-ra-9514", type_="source", trust="primary"),
        _n("concept-building-permit"),
        _n("concept-occupancy-classification"),
        _n("concept-fire-resistive-construction"),
        _n("concept-lot-occupancy"),
    ]
    edges = [
        _e("law-pd-1096", "concept-building-permit", type_="governs",
           evidence="rel-1"),
        _e("law-pd-1096", "concept-occupancy-classification", type_="governs",
           evidence="rel-2"),
        _e("law-pd-1096", "concept-fire-resistive-construction", type_="governs",
           evidence="rel-3"),
        _e("concept-building-permit", "concept-occupancy-classification",
           type_="requires", evidence="rel-4"),
        _e("law-pd-1096", "concept-lot-occupancy", type_="limits",
           evidence="rel-5"),
        _e("law-ra-9514", "concept-fire-resistive-construction",
           type_="defines", evidence="rel-6"),
        _e("concept-occupancy-classification", "concept-building-permit",
           type_="depends_on", evidence="rel-7"),
        _e("concept-building-permit", "concept-occupancy-classification",
           type_="affects", evidence="rel-8"),
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def _load_fixture() -> list[dict]:
    data = yaml.safe_load(_FIXTURE_PATH.read_text(encoding="utf-8"))
    return data["questions"]


def test_fixture_loads_10_questions() -> None:
    questions = _load_fixture()
    assert len(questions) == 10
    for entry in questions:
        assert "q" in entry and isinstance(entry["q"], str)
        assert entry["expected_function"] in _ENGINE


def test_individual_seed_question_happy_path() -> None:
    snap = _seed_snapshot()
    known = tuple(n.id for n in snap.nodes)
    translation = translate_question(
        "What governs building permits?",
        known_entities=known,
    )
    assert translation.function == "what_governs"
    assert translation.arguments["subject"] == "concept-building-permit"
    result = what_governs(translation.arguments["subject"], snap)
    assert result.has_evidence is True
    assert "law-pd-1096" in result.answer_entities


def test_seed_suite_accuracy_meets_threshold() -> None:
    snap = _seed_snapshot()
    known = tuple(n.id for n in snap.nodes)
    questions = _load_fixture()
    correct_function = 0
    correct_citations = 0
    total = len(questions)

    for entry in questions:
        translation = translate_question(entry["q"], known_entities=known)
        if translation.function == entry["expected_function"]:
            correct_function += 1
        # Execute the query regardless of translator accuracy so we can
        # measure the structured API's citation-return rate independently.
        expected_func = _ENGINE[entry["expected_function"]]
        subject = entry["expected_subject"]
        result = expected_func(subject, snap)
        min_cites = entry.get("expected_citation_count_min", 0)
        if len(result.citations) >= min_cites:
            correct_citations += 1

    function_accuracy = correct_function / total
    citation_accuracy = correct_citations / total
    assert function_accuracy >= 0.7, (
        f"NL translator function accuracy {function_accuracy:.0%} < 70%"
    )
    assert citation_accuracy == 1.0, (
        f"Engine citation contract failure: {citation_accuracy:.0%}"
    )
