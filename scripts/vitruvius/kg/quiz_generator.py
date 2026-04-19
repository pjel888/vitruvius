"""Quiz / drill generator using canonical knowledge graph nodes.

Produces question sets from validated ``concept``, ``rule``, and
``definition`` nodes.  This is a scaffold implementation; future work
may add LLM-based question synthesis and distractor generation.

Usage::

    from vitruvius.kg.quiz_generator import QuizGenerator
    from vitruvius.kg.query_engine import QueryEngine
    generator = QuizGenerator(QueryEngine(snapshot))
    quiz = generator.generate_from_node("concept-means-of-egress", num_questions=3)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .enums import NodeType
from .query_engine import QueryEngine
from .schemas import CanonicalNode


@dataclass
class QuizQuestion:
    """A single quiz question."""

    question_type: str  # "definition", "rule", "concept"
    prompt: str
    correct_answer: str
    distractors: list[str] = field(default_factory=list)
    source_node_id: str = ""
    evidence_span_ids: list[str] = field(default_factory=list)


@dataclass
class QuizSet:
    """A generated quiz."""

    title: str
    questions: list[QuizQuestion] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class QuizGenerator:
    """Generate quizzes from validated canonical nodes."""

    def __init__(self, query_engine: QueryEngine) -> None:
        self.query = query_engine

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_from_node(
        self,
        node_id: str,
        num_questions: int = 3,
    ) -> QuizSet:
        """Generate a quiz focused on *node_id* and its neighborhood."""
        node = self.query.get_node_by_id(node_id)
        if node is None:
            return QuizSet(title="Unknown node", questions=[])

        questions: list[QuizQuestion] = []
        neighbors = self.query.get_node_neighborhood(node_id)

        # Question 1: definition of the node itself
        if node.summary:
            questions.append(
                QuizQuestion(
                    question_type="definition",
                    prompt=f"What is '{node.label}'?",
                    correct_answer=node.summary[:200],
                    source_node_id=node.id,
                    evidence_span_ids=[e.id for e in self.query.get_evidence_for_node(node.id)],
                )
            )

        # Questions 2+: relationships
        for neighbor_node, assertion in neighbors[: num_questions - 1]:
            if assertion.reasoning_summary:
                questions.append(
                    QuizQuestion(
                        question_type="relationship",
                        prompt=(
                            f"How does '{node.label}' relate to "
                            f"'{neighbor_node.label}'?"
                        ),
                        correct_answer=assertion.reasoning_summary[:200],
                        source_node_id=node.id,
                        evidence_span_ids=[e.id for e in self.query.get_evidence_for_assertion(assertion.id)],
                    )
                )

        # Distractors: random other node labels
        all_nodes = list(self.query.snapshot.canonical_nodes)
        for q in questions:
            if len(all_nodes) > 3:
                others = [n for n in all_nodes if n.id != q.source_node_id]
                q.distractors = [n.label for n in random.sample(others, min(3, len(others)))]

        return QuizSet(
            title=f"Quiz: {node.label}",
            questions=questions,
            metadata={"source_node_id": node_id, "node_type": node.type.value},
        )

    def generate_random_quiz(
        self,
        node_types: list[NodeType] | None = None,
        num_questions: int = 5,
    ) -> QuizSet:
        """Generate a random quiz from validated nodes of given types."""
        if node_types is None:
            node_types = [NodeType.CONCEPT, NodeType.RULE, NodeType.DEFINITION]

        candidates = [
            n for n in self.query.snapshot.canonical_nodes
            if n.type in node_types and n.summary
        ]
        if not candidates:
            return QuizSet(title="Empty quiz", questions=[])

        selected = random.sample(candidates, min(num_questions, len(candidates)))
        questions: list[QuizQuestion] = []
        for node in selected:
            questions.append(
                QuizQuestion(
                    question_type=node.type.value,
                    prompt=f"What is '{node.label}'?",
                    correct_answer=node.summary[:200],
                    source_node_id=node.id,
                )
            )

        return QuizSet(
            title="General Knowledge Quiz",
            questions=questions,
            metadata={"node_types": [t.value for t in node_types]},
        )
