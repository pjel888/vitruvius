"""Parity checker — verify legacy snapshot vs v2 canonical graph equivalence.

Compares the legacy v1 JSON snapshot (document-primary) against the new
v2 canonical graph to measure coverage and identify gaps before Phase 6
legacy deprecation.

Usage::

    from vitruvius.kg.parity_checker import ParityChecker
    from vitruvius.graph.snapshot import read_snapshot as read_v1
    from vitruvius.kg.json_evidence_store import KgV2Snapshot
    checker = ParityChecker()
    report = checker.check(
        v1_snapshot=read_v1(v1_path),
        v2_snapshot=KgV2Snapshot.read(v2_path),
    )
    print(report.coverage_pct)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from vitruvius.graph.contract import GraphSnapshot as V1Snapshot

from .json_evidence_store import KgV2Snapshot
from .schemas import CanonicalNode


@dataclass
class ParityReport:
    """Result of a legacy → v2 parity check."""

    v1_node_count: int = 0
    v2_node_count: int = 0
    matched_node_ids: list[str] = field(default_factory=list)
    missing_in_v2: list[str] = field(default_factory=list)
    new_in_v2: list[str] = field(default_factory=list)
    v1_edge_count: int = 0
    v2_edge_count: int = 0
    matched_edges: list[tuple[str, str, str]] = field(default_factory=list)
    missing_edges_in_v2: list[tuple[str, str, str]] = field(default_factory=list)
    coverage_pct: float = 0.0
    warnings: list[str] = field(default_factory=list)


class ParityChecker:
    """Compare legacy v1 snapshot with v2 canonical snapshot."""

    def __init__(self, coverage_threshold: float = 0.95) -> None:
        self.coverage_threshold = coverage_threshold

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check(
        self,
        v1_snapshot: V1Snapshot,
        v2_snapshot: KgV2Snapshot,
    ) -> ParityReport:
        """Run parity comparison and return report."""
        report = ParityReport()
        report.v1_node_count = len(v1_snapshot.nodes)
        report.v2_node_count = len(v2_snapshot.canonical_nodes)

        # Node parity
        v1_ids = {n.id for n in v1_snapshot.nodes}
        v2_ids = {n.id for n in v2_snapshot.canonical_nodes}
        report.matched_node_ids = sorted(v1_ids & v2_ids)
        report.missing_in_v2 = sorted(v1_ids - v2_ids)
        report.new_in_v2 = sorted(v2_ids - v1_ids)

        # Edge parity (v1 edges are simple; v2 fast_edges are dicts)
        report.v1_edge_count = len(v1_snapshot.edges)
        report.v2_edge_count = len(v2_snapshot.fast_edges)

        v1_edge_keys: set[tuple[str, str, str]] = set()
        for e in v1_snapshot.edges:
            v1_edge_keys.add((e.from_id, e.to_id, e.type))

        v2_edge_keys: set[tuple[str, str, str]] = set()
        for e in v2_snapshot.fast_edges:
            v2_edge_keys.add((
                e.get("from_node_id", ""),
                e.get("to_node_id", ""),
                e.get("edge_type", ""),
            ))

        report.matched_edges = sorted(v1_edge_keys & v2_edge_keys)
        report.missing_edges_in_v2 = sorted(v1_edge_keys - v2_edge_keys)

        # Coverage calculation
        if report.v1_node_count > 0:
            node_coverage = len(report.matched_node_ids) / report.v1_node_count
        else:
            node_coverage = 1.0

        if report.v1_edge_count > 0:
            edge_coverage = len(report.matched_edges) / report.v1_edge_count
        else:
            edge_coverage = 1.0

        report.coverage_pct = round((node_coverage + edge_coverage) / 2, 4)

        if report.coverage_pct < self.coverage_threshold:
            report.warnings.append(
                f"Coverage {report.coverage_pct:.2%} is below threshold "
                f"{self.coverage_threshold:.2%}"
            )

        return report

    def is_ready_for_deprecation(self, report: ParityReport) -> bool:
        """Return True if v2 coverage is sufficient to deprecate v1."""
        return report.coverage_pct >= self.coverage_threshold
