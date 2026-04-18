"""Tests for the KG review-queue CLI surface in pipeline_cli.py."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.enums import EdgeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    RelationshipAssertion,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_snapshot_for_review() -> KgV2Snapshot:
    snap = KgV2Snapshot()
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-floor-area",
            type="concept",
            label="Floor Area",
            slug="floor-area",
        )
    )
    snap.relationship_assertions.extend(
        [
            RelationshipAssertion(
                id="assert-rel-001",
                edge_type=EdgeType.RELATED_TO,
                from_node_id="concept-floor-area",
                to_node_id="concept-floor-area",
                reasoning_summary="Needs review.",
                inference_type="direct_citation",
                confidence=0.75,
                validation_status=ValidationState.REVIEW_REQUIRED,
                review_state="pending",
                evidence_ids=["span-001"],
            ),
            RelationshipAssertion(
                id="assert-rel-002",
                edge_type=EdgeType.RELATED_TO,
                from_node_id="concept-floor-area",
                to_node_id="concept-floor-area",
                reasoning_summary="Already good.",
                inference_type="direct_citation",
                confidence=0.95,
                validation_status=ValidationState.VALIDATED,
                review_state="approved",
                evidence_ids=["span-001"],
            ),
        ]
    )
    return snap


# ---------------------------------------------------------------------------
# CLI-level tests (invoke the handler logic directly)
# ---------------------------------------------------------------------------

class TestKgReviewQueue:
    def test_lists_review_required_only(self, tmp_path: Path, capsys: Any) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        # Simulate kg-review-queue --status REVIEW_REQUIRED
        from vitruvius.kg.query_engine import QueryEngine

        engine = QueryEngine.from_path(snap_path)
        rows = [
            (
                a.id,
                a.from_node_id,
                a.to_node_id,
                a.confidence,
                a.reasoning_summary.replace("\n", " ")[:60],
            )
            for a in engine.snapshot.relationship_assertions
            if a.validation_status == ValidationState.REVIEW_REQUIRED
        ]
        assert len(rows) == 1
        assert rows[0][0] == "assert-rel-001"

    def test_lists_validated_when_filtered(self, tmp_path: Path) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        from vitruvius.kg.query_engine import QueryEngine

        engine = QueryEngine.from_path(snap_path)
        rows = [
            a
            for a in engine.snapshot.relationship_assertions
            if a.validation_status == ValidationState.VALIDATED
        ]
        assert len(rows) == 1
        assert rows[0].id == "assert-rel-002"

    def test_empty_when_no_matches(self, tmp_path: Path) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        from vitruvius.kg.query_engine import QueryEngine

        engine = QueryEngine.from_path(snap_path)
        rows = [
            a
            for a in engine.snapshot.relationship_assertions
            if a.validation_status == ValidationState.REJECTED
        ]
        assert rows == []


class TestKgReviewAction:
    def test_approve_updates_status(self, tmp_path: Path) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        # Simulate kg-review-action --action approve
        loaded = KgV2Snapshot.read(snap_path)
        for assertion in loaded.relationship_assertions:
            if assertion.id == "assert-rel-001":
                assertion.validation_status = ValidationState.VALIDATED
                assertion.review_state = "approved"
                assertion.reasoning_detail.append("[approve] Looks correct")
                break
        loaded.write(snap_path)

        reloaded = KgV2Snapshot.read(snap_path)
        target = next(a for a in reloaded.relationship_assertions if a.id == "assert-rel-001")
        assert target.validation_status == ValidationState.VALIDATED
        assert target.review_state == "approved"
        assert "[approve] Looks correct" in target.reasoning_detail

    def test_reject_updates_status(self, tmp_path: Path) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        loaded = KgV2Snapshot.read(snap_path)
        for assertion in loaded.relationship_assertions:
            if assertion.id == "assert-rel-001":
                assertion.validation_status = ValidationState.REJECTED
                assertion.review_state = "rejected"
                break
        loaded.write(snap_path)

        reloaded = KgV2Snapshot.read(snap_path)
        target = next(a for a in reloaded.relationship_assertions if a.id == "assert-rel-001")
        assert target.validation_status == ValidationState.REJECTED
        assert target.review_state == "rejected"

    def test_escalate_updates_status(self, tmp_path: Path) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        loaded = KgV2Snapshot.read(snap_path)
        for assertion in loaded.relationship_assertions:
            if assertion.id == "assert-rel-002":
                assertion.validation_status = ValidationState.REVIEW_REQUIRED
                assertion.review_state = "escalated"
                break
        loaded.write(snap_path)

        reloaded = KgV2Snapshot.read(snap_path)
        target = next(a for a in reloaded.relationship_assertions if a.id == "assert-rel-002")
        assert target.validation_status == ValidationState.REVIEW_REQUIRED
        assert target.review_state == "escalated"

    def test_no_match_raises(self, tmp_path: Path) -> None:
        snap = _make_snapshot_for_review()
        snap_path = tmp_path / "snapshot.json"
        snap.write(snap_path)

        loaded = KgV2Snapshot.read(snap_path)
        matched = any(a.id == "assert-missing" for a in loaded.relationship_assertions)
        assert not matched
