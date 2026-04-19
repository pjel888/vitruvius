"""End-to-end test for the KG transition pipeline.

Exercises: extraction → canonicalization → placement → merge → materialization → query
"""

from __future__ import annotations

from pathlib import Path

from vitruvius.kg.canonical_graph_builder import CanonicalGraphBuilder
from vitruvius.kg.canonical_store import CanonicalStore
from vitruvius.kg.canonicalizer import Canonicalizer
from vitruvius.kg.enums import NodeType, ValidationState
from vitruvius.kg.merge_adjudicator import MergeAdjudicator
from vitruvius.kg.placement_engine import PlacementEngine
from vitruvius.kg.query_engine import QueryEngine
from vitruvius.kg.schemas import (
    CanonicalNode,
    EvidenceSpan,
    KnowledgeUnitCandidate,
    TaxonomyNode,
    TextRangeSelector,
)


def _make_candidate(label: str, text: str, unit_type: str = "concept") -> KnowledgeUnitCandidate:
    return KnowledgeUnitCandidate(
        id=f"cand-test-{label.lower().replace(' ', '-')}",
        unit_type=unit_type,
        label=label,
        text=text,
        span_ids=["span-001"],
        chunk_id="chk-001",
        confidence=0.9,
    )


def test_full_pipeline(tmp_path: Path) -> None:
    """Extract candidates → canonicalize → place → merge → materialize → query."""

    # 1. Simulate extraction output
    candidates = [
        _make_candidate("Building Permit", "A permit is required."),
        _make_candidate("Building Permit", "A permit is required."),  # duplicate
        _make_candidate("Zoning Variance", "A variance allows exceptions."),
    ]

    # 2. Canonicalize
    canonicalizer = Canonicalizer()
    nodes = canonicalizer.canonicalize(candidates)
    assert len(nodes) == 2  # deduped

    # 3. Placement
    tax_nodes = [
        TaxonomyNode(id="taxonomy-building-code", path=["building-code"], label="Building Code"),
    ]
    placement_engine = PlacementEngine(tax_nodes)
    placements = []
    for node in nodes:
        paths = placement_engine.place(node)
        for path in paths:
            placements.append(
                {
                    "node_id": node.id,
                    "parent_node_id": path,
                    "confidence": node.confidence,
                }
            )

    # 4. Merge adjudication
    merge_adjudicator = MergeAdjudicator()
    merges = merge_adjudicator.propose(nodes)
    assert len(merges) == 0  # different labels

    # 5. Save to canonical store
    store = CanonicalStore(base_dir=tmp_path)
    jsonl_path = store.save(nodes, [], [], run_id="e2e-test")

    # 6. Build canonical graph snapshot
    builder = CanonicalGraphBuilder()
    builder.load_canonical_jsonl(jsonl_path)
    snapshot = builder.build(run_placement=False, run_merge_adjudication=False)

    # 7. Query
    engine = QueryEngine(snapshot)
    permit_node = engine.get_node_by_id("concept-building-permit")
    assert permit_node is not None
    assert permit_node.type == NodeType.CONCEPT

    variance_node = engine.get_node_by_id("concept-zoning-variance")
    assert variance_node is not None

    # Search
    results = engine.search_nodes_by_label("permit")
    assert len(results) == 1

    # Evidence
    assert engine.get_evidence_for_node("concept-building-permit") == []

    # Taxonomy
    assert engine.get_taxonomy_tree() == []


def test_pipeline_with_evidence(tmp_path: Path) -> None:
    """Pipeline with evidence spans linked to assertions."""
    from vitruvius.kg.json_evidence_store import KgV2Snapshot
    from vitruvius.kg.schemas import RelationshipAssertion
    from vitruvius.kg.enums import EdgeType, InferenceType

    snap = KgV2Snapshot()
    snap.canonical_nodes.extend([
        CanonicalNode(id="concept-a", type=NodeType.CONCEPT, label="A", slug="a"),
        CanonicalNode(id="concept-b", type=NodeType.CONCEPT, label="B", slug="b"),
    ])
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-001",
            document_id="doc-x",
            document_version_id="docv-x-v1",
            selector=TextRangeSelector(kind="text_range", char_start=0, char_end=5),
            quote="Quote text",
            normalized_text="quote text",
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
            reasoning_summary="Reason",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.9,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )

    engine = QueryEngine(snap)
    evidence = engine.get_evidence_for_node("concept-a")
    assert len(evidence) == 1
    assert evidence[0].id == "span-001"

    neighbors = engine.get_node_neighborhood("concept-a")
    assert len(neighbors) == 1
    assert neighbors[0][0].id == "concept-b"
    assert neighbors[0][1].id == "assert-rel-001"
