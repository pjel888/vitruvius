from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


ALLOWED_NODE_TYPES = frozenset({"source", "concept", "attribute", "spatial_instance"})

ALLOWED_TRUST_LEVELS = frozenset({
    "primary", "secondary", "tertiary", "unverified", "derived",
})

ALLOWED_EDGE_STATUSES = frozenset({"verified", "unverified", "spatially_verified"})

ALLOWED_ID_PREFIXES = frozenset({
    "law-",
    "irr-",
    "concept-",
    "rel-",
    "source-",
    "handout-",
    "reviewer-",
    "law-section-",
    "instance-",
    "spatial-",
})


_ISO_DATE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?)?$"
)


@dataclass(frozen=True)
class GraphNode:
    id: str
    type: str
    slug: str
    trust_level: str
    last_updated_utc: str
    title: str | None = None


@dataclass(frozen=True)
class GraphEdge:
    from_id: str
    to_id: str
    type: str
    evidence_id: str
    status: str
    evidence_source_id: str | None = None
    evidence_source_section_id: str | None = None
    evidence_snippet: str | None = None
    reviewer_confidence: float | None = None
    # Stream W3.4 — None means "unset / legacy edge"; True means this edge
    # won a stringency resolver contest; False means it lost and another
    # edge for the same (predicate, from, to) triplet is authoritative.
    is_governing_standard: bool | None = None


@dataclass
class GraphSnapshot:
    schema_version: str
    generated_at_utc: str
    node_count: int
    edge_count: int
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    metadata: dict[str, Any] | None = None


class ContractViolation(ValueError):
    pass


def _has_allowed_prefix(value: str) -> bool:
    return any(value.startswith(prefix) for prefix in ALLOWED_ID_PREFIXES)


def validate_node(node: GraphNode) -> None:
    if not isinstance(node.id, str) or not _has_allowed_prefix(node.id):
        raise ContractViolation(
            f"node id {node.id!r} must start with one of {sorted(ALLOWED_ID_PREFIXES)}"
        )
    if node.type not in ALLOWED_NODE_TYPES:
        raise ContractViolation(
            f"node type {node.type!r} not in {sorted(ALLOWED_NODE_TYPES)}"
        )
    if node.trust_level not in ALLOWED_TRUST_LEVELS:
        raise ContractViolation(
            f"node trust_level {node.trust_level!r} not in {sorted(ALLOWED_TRUST_LEVELS)}"
        )
    if not isinstance(node.slug, str) or not node.slug.strip():
        raise ContractViolation(f"node slug must be a non-empty string (got {node.slug!r})")
    if not isinstance(node.last_updated_utc, str) or not _ISO_DATE_RE.match(node.last_updated_utc):
        raise ContractViolation(
            f"node last_updated_utc {node.last_updated_utc!r} is not a valid ISO-8601 date"
        )
    if node.title is not None and (not isinstance(node.title, str) or not node.title.strip()):
        raise ContractViolation(f"node title must be null or a non-empty string (got {node.title!r})")


def validate_edge(edge: GraphEdge) -> None:
    if not isinstance(edge.from_id, str) or not _has_allowed_prefix(edge.from_id):
        raise ContractViolation(
            f"edge from_id {edge.from_id!r} must start with one of {sorted(ALLOWED_ID_PREFIXES)}"
        )
    if not isinstance(edge.to_id, str) or not _has_allowed_prefix(edge.to_id):
        raise ContractViolation(
            f"edge to_id {edge.to_id!r} must start with one of {sorted(ALLOWED_ID_PREFIXES)}"
        )
    if not isinstance(edge.type, str) or not edge.type.strip():
        raise ContractViolation(f"edge type must be a non-empty string (got {edge.type!r})")
    if not isinstance(edge.evidence_id, str) or not edge.evidence_id.startswith("rel-"):
        raise ContractViolation(
            f"edge evidence_id {edge.evidence_id!r} must start with 'rel-'"
        )
    if edge.status not in ALLOWED_EDGE_STATUSES:
        raise ContractViolation(
            f"edge status {edge.status!r} not in {sorted(ALLOWED_EDGE_STATUSES)}"
        )


@dataclass(frozen=True)
class TemporalEdge:
    """Stream GT.3.1 — a time-bound edge: (s, p, o, [valid_from, valid_until)).

    ``valid_until`` is ``None`` for open intervals (edge is still valid).
    Timestamps MUST be ISO-8601 UTC strings to match the rest of the
    graph contract.
    """
    from_id: str
    to_id: str
    type: str
    evidence_id: str
    status: str
    valid_from: str
    valid_until: str | None = None


def validate_temporal_edge(edge: TemporalEdge) -> None:
    """Validate a TemporalEdge. Delegates the s/p/o checks to the
    regular ``validate_edge`` helper by projecting onto a GraphEdge,
    then layers on the valid_from/valid_until checks on top."""
    projection = GraphEdge(
        from_id=edge.from_id,
        to_id=edge.to_id,
        type=edge.type,
        evidence_id=edge.evidence_id,
        status=edge.status,
    )
    validate_edge(projection)

    if not isinstance(edge.valid_from, str) or not _ISO_DATE_RE.match(edge.valid_from):
        raise ContractViolation(
            f"temporal edge valid_from {edge.valid_from!r} is not a valid ISO-8601 date"
        )
    if edge.valid_until is not None:
        if not isinstance(edge.valid_until, str) or not _ISO_DATE_RE.match(edge.valid_until):
            raise ContractViolation(
                f"temporal edge valid_until {edge.valid_until!r} is not a valid ISO-8601 date"
            )
        if edge.valid_until <= edge.valid_from:
            raise ContractViolation(
                f"temporal edge valid_until {edge.valid_until!r} must be strictly after "
                f"valid_from {edge.valid_from!r}"
            )
