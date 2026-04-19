"""Serialization contract tests — ensure snapshot payloads are downstream-safe.

Downstream consumers (Neo4j loader, UI serializers, third-party tools) depend on
``KgV2Snapshot.to_dict()`` producing JSON-compatible structures with stable keys.
"""

from __future__ import annotations

import json

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    Chunk,
    DocumentVersion,
    EvidenceSpan,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
    Section,
    TextRangeSelector,
)


def _make_populated_snapshot() -> KgV2Snapshot:
    snap = KgV2Snapshot()
    snap.document_versions.append(
        DocumentVersion(
            id="docv-test-v1",
            document_id="doc-test",
            title="Test Doc",
            source_uri="test.md",
            sha256="a" * 64,
            created_at="2026-01-01T00:00:00Z",
        )
    )
    snap.sections.append(
        Section(
            id="sec-test",
            document_version_id="docv-test-v1",
            title="Section",
        )
    )
    snap.chunks.append(
        Chunk(
            id="chk-test",
            section_id="sec-test",
            document_version_id="docv-test-v1",
            text="Text",
            char_start=0,
            char_end=4,
        )
    )
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-test",
            document_id="doc-test",
            document_version_id="docv-test-v1",
            selector=TextRangeSelector(kind="text_range", char_start=0, char_end=4),
            quote="Text",
            normalized_text="text",
            parser="test",
            checksum="b" * 64,
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-test",
            type=NodeType.CONCEPT,
            label="Test",
            slug="test",
        )
    )
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-test",
            edge_type=EdgeType.RELATED_TO,
            from_node_id="concept-test",
            to_node_id="concept-test",
            reasoning_summary="Reason",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.9,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-test"],
        )
    )
    snap.placement_assertions.append(
        PlacementAssertion(
            id="assert-placement-test",
            node_id="concept-test",
            parent_node_id="taxonomy-root",
            reasoning_summary="Placed",
            confidence=0.9,
            validation_status=ValidationState.CANDIDATE,
        )
    )
    snap.merge_assertions.append(
        MergeAssertion(
            id="assert-merge-test",
            from_node_id="concept-test",
            to_node_id="concept-test",
            reasoning_summary="Merge",
            confidence=1.0,
            validation_status=ValidationState.REVIEW_REQUIRED,
        )
    )
    snap.fast_edges = [
        {
            "id": "edge-test",
            "edge_type": "RELATED_TO",
            "from_node_id": "concept-test",
            "to_node_id": "concept-test",
            "assertion_id": "assert-rel-test",
            "confidence": 0.9,
            "validation_status": "validated",
            "evidence_span_count": 1,
            "document_version_count": 0,
        }
    ]
    return snap


class TestToDict:
    def test_produces_json_serializable_dict(self) -> None:
        snap = _make_populated_snapshot()
        payload = snap.to_dict()
        # Should not raise
        json_str = json.dumps(payload, ensure_ascii=False)
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_roundtrip_through_json(self) -> None:
        snap = _make_populated_snapshot()
        payload = snap.to_dict()
        json_str = json.dumps(payload, ensure_ascii=False)
        restored = json.loads(json_str)
        assert restored["schema_version"] == snap.schema_version
        assert len(restored["canonical_nodes"]) == 1
        assert restored["canonical_nodes"][0]["id"] == "concept-test"

    def test_sorted_keys_for_determinism(self) -> None:
        snap = _make_populated_snapshot()
        payload = snap.to_dict()
        # When serialized to JSON with sort_keys, keys should be sorted
        json_str = json.dumps(payload, sort_keys=True)
        # Parse back and verify top-level order
        restored = json.loads(json_str)
        keys = list(restored.keys())
        assert keys == sorted(keys)

    def test_no_pydantic_models_in_payload(self) -> None:
        """Ensure every value is JSON-native (dict, list, str, int, float, bool, None)."""
        snap = _make_populated_snapshot()
        payload = snap.to_dict()

        def _check(obj: object, path: str) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    _check(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    _check(item, f"{path}[{i}]")
            else:
                assert isinstance(
                    obj, (str, int, float, bool, type(None))
                ), f"Non-JSON value at {path}: {type(obj).__name__} = {obj!r}"

        _check(payload, "payload")

    def test_enum_values_are_strings(self) -> None:
        """Edge types, node types, and validation states must serialize as strings."""
        snap = _make_populated_snapshot()
        payload = snap.to_dict()
        node = payload["canonical_nodes"][0]
        assert node["type"] == "concept"
        assertion = payload["relationship_assertions"][0]
        assert assertion["edge_type"] == "RELATED_TO"
        assert assertion["validation_status"] == "validated"


class TestChecksum:
    def test_checksum_is_stable(self) -> None:
        snap = _make_populated_snapshot()
        cs1 = snap.checksum()
        cs2 = snap.checksum()
        assert cs1 == cs2
        assert len(cs1) == 64

    def test_checksum_changes_when_content_changes(self) -> None:
        snap1 = _make_populated_snapshot()
        snap2 = _make_populated_snapshot()
        snap2.canonical_nodes[0] = snap2.canonical_nodes[0].model_copy(update={"label": "Changed"})
        assert snap1.checksum() != snap2.checksum()
