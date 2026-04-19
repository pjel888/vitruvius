"""Contradiction detector for the Knowledge Graph assertion layer.

Performs deterministic sweeps over ``RelationshipAssertion`` records to
find logically incompatible pairs.  This is an offline / batch tool, not
run on the request path.

Detected contradiction patterns
-------------------------------
- **Override conflict:** A ``OVERRIDES`` assertion and an ``APPLIES_TO``
  assertion between the same two nodes (same direction).
- **Requirement conflict:** A ``REQUIRES`` assertion and an ``EXCLUDES``
  assertion between the same two nodes (same direction).
- **Inference credibility:** A ``SEMANTIC_SIMILARITY`` assertion that
  claims the same relationship as a ``DIRECT_CITATION`` but with lower
  confidence (flagged for review, not a hard contradiction).
- **Bidirectional inversion:** A ``DEPENDS_ON`` from A→B and a
  ``DEPENDS_ON`` from B→A with conflicting reasoning summaries.

Usage::

    from vitruvius.kg.contradiction_detector import ContradictionDetector
    detector = ContradictionDetector()
    issues = detector.detect(snapshot.relationship_assertions)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import EdgeType, InferenceType
from .schemas import RelationshipAssertion


@dataclass
class ContradictionIssue:
    """A single detected contradiction or conflict."""

    severity: str  # "critical", "warning", "info"
    pattern: str  # machine-readable pattern name
    description: str
    assertion_ids: list[str] = field(default_factory=list)
    suggested_action: str = "review"


class ContradictionDetector:
    """Offline contradiction sweep over relationship assertions."""

    def __init__(self, min_confidence_delta: float = 0.15) -> None:
        self.min_confidence_delta = min_confidence_delta

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect(
        self,
        assertions: list[RelationshipAssertion],
    ) -> list[ContradictionIssue]:
        """Return all contradiction issues found in *assertions*."""
        issues: list[ContradictionIssue] = []

        # Index for fast lookup
        by_pair: dict[tuple[str, str, str], list[RelationshipAssertion]] = {}
        for assertion in assertions:
            key = (assertion.from_node_id, assertion.to_node_id, assertion.edge_type.value)
            by_pair.setdefault(key, []).append(assertion)

        # 1. Override vs Applies-To conflict
        issues.extend(self._detect_override_conflict(assertions, by_pair))

        # 2. Requires vs Excludes conflict
        issues.extend(self._detect_requirement_conflict(assertions, by_pair))

        # 3. Semantic similarity undermining direct citation
        issues.extend(self._detect_inference_credibility(assertions, by_pair))

        # 4. Bidirectional DEPENDS_ON with weak confidence
        issues.extend(self._detect_bidirectional_dependency(assertions))

        return issues

    # ------------------------------------------------------------------
    # Pattern detectors
    # ------------------------------------------------------------------

    def _detect_override_conflict(
        self,
        _assertions: list[RelationshipAssertion],
        by_pair: dict[tuple[str, str, str], list[RelationshipAssertion]],
    ) -> list[ContradictionIssue]:
        """Find OVERRIDES + APPLIES_TO on the same directed pair."""
        issues: list[ContradictionIssue] = []
        seen: set[tuple[str, str]] = set()

        for assertion in _assertions:
            if assertion.edge_type != EdgeType.OVERRIDES:
                continue
            pair = (assertion.from_node_id, assertion.to_node_id)
            if pair in seen:
                continue
            seen.add(pair)

            # Look for APPLIES_TO on same pair
            applies_key = (pair[0], pair[1], EdgeType.APPLIES_TO.value)
            if applies_key in by_pair:
                ids = [assertion.id] + [a.id for a in by_pair[applies_key]]
                issues.append(
                    ContradictionIssue(
                        severity="critical",
                        pattern="override_vs_applies_to",
                        description=(
                            f"Node {pair[0]} both OVERRIDES and APPLIES_TO "
                            f"node {pair[1]}"
                        ),
                        assertion_ids=ids,
                        suggested_action="demote one assertion to rejected",
                    )
                )

        return issues

    def _detect_requirement_conflict(
        self,
        _assertions: list[RelationshipAssertion],
        by_pair: dict[tuple[str, str, str], list[RelationshipAssertion]],
    ) -> list[ContradictionIssue]:
        """Find REQUIRES + EXCLUDES on the same directed pair."""
        issues: list[ContradictionIssue] = []
        seen: set[tuple[str, str]] = set()

        for assertion in _assertions:
            if assertion.edge_type != EdgeType.REQUIRES:
                continue
            pair = (assertion.from_node_id, assertion.to_node_id)
            if pair in seen:
                continue
            seen.add(pair)

            excludes_key = (pair[0], pair[1], EdgeType.EXCLUDES.value)
            if excludes_key in by_pair:
                ids = [assertion.id] + [a.id for a in by_pair[excludes_key]]
                issues.append(
                    ContradictionIssue(
                        severity="critical",
                        pattern="requires_vs_excludes",
                        description=(
                            f"Node {pair[0]} both REQUIRES and EXCLUDES "
                            f"node {pair[1]}"
                        ),
                        assertion_ids=ids,
                        suggested_action="demote one assertion to rejected",
                    )
                )

        return issues

    def _detect_inference_credibility(
        self,
        _assertions: list[RelationshipAssertion],
        by_pair: dict[tuple[str, str, str], list[RelationshipAssertion]],
    ) -> list[ContradictionIssue]:
        """Flag SEMANTIC_SIMILARITY assertions that shadow DIRECT_CITATION."""
        issues: list[ContradictionIssue] = []

        for assertion in _assertions:
            if assertion.inference_type != InferenceType.SEMANTIC_SIMILARITY:
                continue
            key = (assertion.from_node_id, assertion.to_node_id, assertion.edge_type.value)
            for other in by_pair.get(key, []):
                if other.inference_type == InferenceType.DIRECT_CITATION:
                    delta = other.confidence - assertion.confidence
                    if delta >= self.min_confidence_delta:
                        issues.append(
                            ContradictionIssue(
                                severity="warning",
                                pattern="semantic_shadows_direct_citation",
                                description=(
                                    f"Semantic assertion {assertion.id} "
                                    f"shadows direct citation {other.id} "
                                    f"(confidence delta {delta:.2f})"
                                ),
                                assertion_ids=[assertion.id, other.id],
                                suggested_action="review semantic assertion",
                            )
                        )

        return issues

    def _detect_bidirectional_dependency(
        self,
        assertions: list[RelationshipAssertion],
    ) -> list[ContradictionIssue]:
        """Flag bidirectional DEPENDS_ON with both directions below 0.8."""
        issues: list[ContradictionIssue] = []
        depends: dict[tuple[str, str], RelationshipAssertion] = {}

        for assertion in assertions:
            if assertion.edge_type == EdgeType.DEPENDS_ON:
                pair = (assertion.from_node_id, assertion.to_node_id)
                depends[pair] = assertion

        seen_pairs: set[frozenset[str]] = set()
        for (a, b), assert_ab in depends.items():
            pair = frozenset({a, b})
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            if (b, a) in depends:
                assert_ba = depends[(b, a)]
                if assert_ab.confidence < 0.8 and assert_ba.confidence < 0.8:
                    issues.append(
                        ContradictionIssue(
                            severity="warning",
                            pattern="weak_bidirectional_dependency",
                            description=(
                                f"Weak bidirectional DEPENDS_ON between "
                                f"{a} and {b} (confidences {assert_ab.confidence:.2f}, "
                                f"{assert_ba.confidence:.2f})"
                            ),
                            assertion_ids=[assert_ab.id, assert_ba.id],
                            suggested_action="review or merge into mutual requirement",
                        )
                    )

        return issues
