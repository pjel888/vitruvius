from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .contract import GraphEdge, GraphNode, GraphSnapshot


IntegritySeverity = Literal["warning", "error"]


@dataclass(frozen=True)
class IntegrityFinding:
    code: str
    severity: IntegritySeverity
    node_id: str | None
    edge_from: str | None
    edge_to: str | None
    message: str


@dataclass(frozen=True)
class IntegrityReport:
    findings: tuple[IntegrityFinding, ...]
    warning_count: int
    error_count: int
    passed: bool


def _edge_key(edge: GraphEdge) -> tuple[str, str, str, str]:
    return (edge.from_id, edge.type, edge.to_id, edge.evidence_id)


def _duplicate_node_findings(snapshot: GraphSnapshot) -> list[IntegrityFinding]:
    seen: dict[str, int] = {}
    findings: list[IntegrityFinding] = []
    for node in snapshot.nodes:
        seen[node.id] = seen.get(node.id, 0) + 1
        if seen[node.id] != 2:
            continue
        findings.append(
            IntegrityFinding(
                code="duplicate_node_id",
                severity="error",
                node_id=node.id,
                edge_from=None,
                edge_to=None,
                message=f"duplicate node id detected: {node.id!r}",
            )
        )
    return findings


def _orphan_findings(snapshot: GraphSnapshot) -> list[IntegrityFinding]:
    incident: set[str] = set()
    for edge in snapshot.edges:
        incident.add(edge.from_id)
        incident.add(edge.to_id)
    findings: list[IntegrityFinding] = []
    for node in snapshot.nodes:
        if node.id in incident:
            continue
        findings.append(
            IntegrityFinding(
                code="orphan_node",
                severity="warning",
                node_id=node.id,
                edge_from=None,
                edge_to=None,
                message=f"node {node.id!r} has zero incident edges",
            )
        )
    return findings


def _dangling_findings(snapshot: GraphSnapshot) -> list[IntegrityFinding]:
    node_ids = {n.id for n in snapshot.nodes}
    findings: list[IntegrityFinding] = []
    for edge in snapshot.edges:
        missing: list[str] = []
        if edge.from_id not in node_ids:
            missing.append("from_id")
        if edge.to_id not in node_ids:
            missing.append("to_id")
        if not missing:
            continue
        findings.append(
            IntegrityFinding(
                code="dangling_edge",
                severity="error",
                node_id=None,
                edge_from=edge.from_id,
                edge_to=edge.to_id,
                message=(
                    f"edge {edge.evidence_id!r} references missing "
                    f"{', '.join(missing)}"
                ),
            )
        )
    return findings


def _unknown_predicate_findings(
    snapshot: GraphSnapshot,
    known_predicates: frozenset[str] | None,
) -> list[IntegrityFinding]:
    if known_predicates is None:
        return []
    findings: list[IntegrityFinding] = []
    for edge in snapshot.edges:
        if edge.type in known_predicates:
            continue
        findings.append(
            IntegrityFinding(
                code="unknown_predicate",
                severity="error",
                node_id=None,
                edge_from=edge.from_id,
                edge_to=edge.to_id,
                message=f"predicate {edge.type!r} not in the known vocabulary",
            )
        )
    return findings


def _duplicate_findings(snapshot: GraphSnapshot) -> list[IntegrityFinding]:
    seen: dict[tuple[str, str, str, str], int] = {}
    duplicates: list[GraphEdge] = []
    for edge in snapshot.edges:
        key = _edge_key(edge)
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 2:
            duplicates.append(edge)
    findings: list[IntegrityFinding] = []
    for edge in duplicates:
        findings.append(
            IntegrityFinding(
                code="duplicate_edge",
                severity="warning",
                node_id=None,
                edge_from=edge.from_id,
                edge_to=edge.to_id,
                message=(
                    f"duplicate edge: {edge.from_id} -[{edge.type}]-> {edge.to_id} "
                    f"(evidence {edge.evidence_id})"
                ),
            )
        )
    return findings


def _stale_evidence_findings(
    snapshot: GraphSnapshot,
    known_evidence_ids: frozenset[str] | None,
) -> list[IntegrityFinding]:
    if known_evidence_ids is None:
        return []
    findings: list[IntegrityFinding] = []
    for edge in snapshot.edges:
        if edge.evidence_id in known_evidence_ids:
            continue
        findings.append(
            IntegrityFinding(
                code="stale_evidence",
                severity="error",
                node_id=None,
                edge_from=edge.from_id,
                edge_to=edge.to_id,
                message=f"evidence_id {edge.evidence_id!r} not found in the known set",
            )
        )
    return findings


def check_integrity(
    snapshot: GraphSnapshot,
    *,
    known_predicates: frozenset[str] | None = None,
    known_evidence_ids: frozenset[str] | None = None,
) -> IntegrityReport:
    findings: list[IntegrityFinding] = []
    findings.extend(_duplicate_node_findings(snapshot))
    findings.extend(_orphan_findings(snapshot))
    findings.extend(_dangling_findings(snapshot))
    findings.extend(_unknown_predicate_findings(snapshot, known_predicates))
    findings.extend(_duplicate_findings(snapshot))
    findings.extend(_stale_evidence_findings(snapshot, known_evidence_ids))

    warning_count = sum(1 for f in findings if f.severity == "warning")
    error_count = sum(1 for f in findings if f.severity == "error")
    return IntegrityReport(
        findings=tuple(findings),
        warning_count=warning_count,
        error_count=error_count,
        passed=error_count == 0,
    )
