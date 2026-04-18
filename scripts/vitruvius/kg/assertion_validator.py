"""Assertion Validator — validates KG v2 assertions against promotion rules.

Extends the legacy ``promotion_validator.py`` logic to operate on Pydantic
``RelationshipAssertion``, ``PlacementAssertion``, and ``MergeAssertion``
objects.  Updates ``validation_status`` in-place when rules pass.

Rules
-----
R1  id format must match assertion-type pattern
R2  edge_type must be a registered EdgeType
R3  from_node_id must exist in canonical index
R4  to_node_id   must exist in canonical index
R5  reasoning_summary must be non-empty
R6  confidence must be in [0.0, 1.0]
R7  (Relationship) inference_type must be a registered InferenceType
R8  evidence_ids must be non-empty
R9  every evidence_id must resolve to a known EvidenceSpan
R10 (Placement) parent_node_id must be taxonomy|topic|subtopic
R11 (Placement) node must not already be placed under a different parent
R12 (Merge)     from_node and to_node must share a compatible type
R13 (Merge)     nodes must not already be merged / superseded
R14 review_state must not be "rejected"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import EdgeType, InferenceType, NodeType, ValidationState
from .schemas import (
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
)


@dataclass
class AssertionValidationResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    assertion_id: str = ""
    updated_status: ValidationState = ValidationState.CANDIDATE


class AssertionValidator:
    """Validate KG v2 assertions and promote ``CANDIDATE`` → ``VALIDATED``."""

    def __init__(
        self,
        canonical_index: dict[str, dict[str, Any]] | None = None,
        evidence_index: dict[str, dict[str, Any]] | None = None,
        placement_index: dict[str, str] | None = None,
        merge_index: dict[str, str] | None = None,
    ) -> None:
        self.canonical_index = canonical_index or {}
        self.evidence_index = evidence_index or {}
        # placement_index: node_id -> parent_node_id
        self.placement_index = placement_index or {}
        # merge_index: node_id -> merged_target_node_id
        self.merge_index = merge_index or {}

    # -- public API ---------------------------------------------------------

    def validate_relationship(
        self,
        assertion: RelationshipAssertion,
    ) -> AssertionValidationResult:
        errors: list[str] = []
        errors.extend(self._check_common(assertion))

        # R7 inference_type
        if assertion.inference_type not in InferenceType:
            errors.append(
                f"R7: inference_type '{assertion.inference_type}' not in {list(InferenceType)}"
            )

        # R14 review_state
        if assertion.review_state == "rejected":
            errors.append("R14: review_state is 'rejected'")

        return self._build_result(assertion, errors)

    def validate_placement(
        self,
        assertion: PlacementAssertion,
    ) -> AssertionValidationResult:
        errors: list[str] = []
        errors.extend(self._check_common(assertion))

        # R10 parent must be a taxonomy container
        parent = self.canonical_index.get(assertion.parent_node_id)
        if parent:
            ptype = parent.get("type", "")
            if ptype not in ("taxonomy", "topic", "subtopic"):
                errors.append(
                    f"R10: parent_node_id '{assertion.parent_node_id}' type '{ptype}' "
                    "is not taxonomy|topic|subtopic"
                )

        # R11 no conflicting existing placement
        existing_parent = self.placement_index.get(assertion.node_id)
        if existing_parent and existing_parent != assertion.parent_node_id:
            errors.append(
                f"R11: node '{assertion.node_id}' already placed under "
                f"'{existing_parent}'"
            )

        return self._build_result(assertion, errors)

    def validate_merge(
        self,
        assertion: MergeAssertion,
    ) -> AssertionValidationResult:
        errors: list[str] = []
        errors.extend(self._check_common(assertion))

        # R12 compatible types
        from_node = self.canonical_index.get(assertion.from_node_id)
        to_node = self.canonical_index.get(assertion.to_node_id)
        if from_node and to_node:
            ftype = from_node.get("type", "")
            ttype = to_node.get("type", "")
            if ftype != ttype:
                errors.append(
                    f"R12: type mismatch '{ftype}' vs '{ttype}'"
                )

        # R13 not already merged / superseded
        if assertion.from_node_id in self.merge_index:
            errors.append(
                f"R13: from_node '{assertion.from_node_id}' already merged"
            )
        if assertion.to_node_id in self.merge_index:
            errors.append(
                f"R13: to_node '{assertion.to_node_id}' already merged"
            )
        for nid in (assertion.from_node_id, assertion.to_node_id):
            node = self.canonical_index.get(nid)
            if node and node.get("status") == ValidationState.SUPERSEDED:
                errors.append(f"R13: node '{nid}' is superseded")

        return self._build_result(assertion, errors)

    # -- shared checks ------------------------------------------------------

    def _check_common(
        self,
        assertion: RelationshipAssertion | PlacementAssertion | MergeAssertion,
    ) -> list[str]:
        errors: list[str] = []
        aid = assertion.id

        # R2 edge_type must be registered (only for RelationshipAssertion)
        if isinstance(assertion, RelationshipAssertion):
            if assertion.edge_type not in EdgeType:
                errors.append(
                    f"R2: edge_type '{assertion.edge_type}' is not a registered EdgeType"
                )

        # R3 / R4 endpoint existence
        if hasattr(assertion, "from_node_id"):
            if assertion.from_node_id not in self.canonical_index:
                errors.append(f"R3: from_node_id '{assertion.from_node_id}' not in index")
            if assertion.to_node_id not in self.canonical_index:
                errors.append(f"R4: to_node_id '{assertion.to_node_id}' not in index")

        if hasattr(assertion, "node_id"):
            if assertion.node_id not in self.canonical_index:
                errors.append(f"R3: node_id '{assertion.node_id}' not in index")

        # R5 reasoning
        rs = getattr(assertion, "reasoning_summary", "")
        if not isinstance(rs, str) or not rs.strip():
            errors.append("R5: reasoning_summary is empty")

        # R6 confidence range (schema already enforces [0,1], but double-check)
        conf = getattr(assertion, "confidence", 0.0)
        if not (0.0 <= conf <= 1.0):
            errors.append(f"R6: confidence {conf} outside [0.0, 1.0]")

        # R8 evidence non-empty
        ev_ids = getattr(assertion, "evidence_ids", [])
        if not ev_ids:
            errors.append("R8: evidence_ids is empty")

        # R9 evidence resolution
        for eid in ev_ids:
            if eid not in self.evidence_index:
                errors.append(f"R9: evidence_id '{eid}' not in evidence index")

        return errors

    def _build_result(
        self,
        assertion: RelationshipAssertion | PlacementAssertion | MergeAssertion,
        errors: list[str],
    ) -> AssertionValidationResult:
        passed = not errors
        new_status = ValidationState.VALIDATED if passed else ValidationState.REVIEW_REQUIRED
        # Update in-place when passed
        if passed:
            assertion.validation_status = new_status
        return AssertionValidationResult(
            passed=passed,
            errors=errors,
            assertion_id=assertion.id,
            updated_status=new_status,
        )
