"""Tests for QuizGenerator."""

from __future__ import annotations

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.quiz_generator import QuizGenerator
from vitruvius.kg.query_engine import QueryEngine
from vitruvius.kg.schemas import CanonicalNode, EvidenceSpan, RelationshipAssertion, TextRangeSelector


def _make_snapshot() -> KgV2Snapshot:
    snap = KgV2Snapshot()
    snap.canonical_nodes.extend([
        CanonicalNode(id="concept-a", type=NodeType.CONCEPT, label="Concept A", slug="a", summary="Summary of A"),
        CanonicalNode(id="concept-b", type=NodeType.CONCEPT, label="Concept B", slug="b", summary="Summary of B"),
        CanonicalNode(id="concept-c", type=NodeType.CONCEPT, label="Concept C", slug="c", summary="Summary of C"),
    ])
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-001",
            document_id="doc-x",
            document_version_id="docv-x-v1",
            selector=TextRangeSelector(kind="text_range", char_start=0, char_end=5),
            quote="quote",
            normalized_text="quote",
            parser="test",
            checksum="a" * 64,
        )
    )
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-001",
            edge_type=EdgeType.RELATED_TO,
            from_node_id="concept-a",
            to_node_id="concept-b",
            reasoning_summary="A relates to B",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.9,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )
    return snap


class TestGenerateFromNode:
    def test_generates_definition_question(self) -> None:
        snap = _make_snapshot()
        engine = QueryEngine(snap)
        generator = QuizGenerator(engine)
        quiz = generator.generate_from_node("concept-a", num_questions=3)
        assert quiz.title == "Quiz: Concept A"
        assert len(quiz.questions) >= 1
        assert quiz.questions[0].question_type == "definition"
        assert quiz.questions[0].correct_answer == "Summary of A"

    def test_generates_relationship_question(self) -> None:
        snap = _make_snapshot()
        engine = QueryEngine(snap)
        generator = QuizGenerator(engine)
        quiz = generator.generate_from_node("concept-a", num_questions=3)
        rel_questions = [q for q in quiz.questions if q.question_type == "relationship"]
        assert len(rel_questions) >= 1
        assert "Concept B" in rel_questions[0].prompt

    def test_unknown_node_returns_empty(self) -> None:
        snap = _make_snapshot()
        engine = QueryEngine(snap)
        generator = QuizGenerator(engine)
        quiz = generator.generate_from_node("concept-unknown")
        assert quiz.title == "Unknown node"
        assert quiz.questions == []


class TestGenerateRandomQuiz:
    def test_generates_from_multiple_nodes(self) -> None:
        snap = _make_snapshot()
        engine = QueryEngine(snap)
        generator = QuizGenerator(engine)
        quiz = generator.generate_random_quiz(num_questions=2)
        assert len(quiz.questions) == 2
        assert quiz.title == "General Knowledge Quiz"

    def test_empty_snapshot_returns_empty(self) -> None:
        snap = KgV2Snapshot()
        engine = QueryEngine(snap)
        generator = QuizGenerator(engine)
        quiz = generator.generate_random_quiz()
        assert quiz.questions == []
