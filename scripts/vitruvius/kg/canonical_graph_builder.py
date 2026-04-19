"""CanonicalGraphBuilder — unify taxonomy, canonical nodes, and assertions.

Combines output from:
- TaxonomyLoader (existing taxonomy roots and concepts from disk)
- Canonicalizer (new nodes from extracted candidates)
- PlacementEngine (taxonomy placement assertions)
- MergeAdjudicator (merge proposals)

Produces a unified ``KgV2Snapshot`` that is the source of truth for the
canonical graph layer.

Usage::

    from vitruvius.kg.canonical_graph_builder import CanonicalGraphBuilder
    builder = CanonicalGraphBuilder()
    builder.load_taxonomy_snapshot(path)
    builder.load_canonical_jsonl(path)
    builder.build()
    builder.write_snapshot(out_path)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .assertion_validator import AssertionValidator
from .canonical_store import CanonicalStore
from .canonicalizer import Canonicalizer
from .edge_materializer import EdgeMaterializer
from .json_evidence_store import KgV2Snapshot
from .merge_adjudicator import MergeAdjudicator
from .placement_engine import PlacementEngine
from .schemas import CanonicalNode, PlacementAssertion, TaxonomyNode


class CanonicalGraphBuilder:
    """Build a unified canonical graph snapshot from multiple sources."""

    def __init__(self) -> None:
        self.snapshot = KgV2Snapshot()
        self._taxonomy_nodes: list[TaxonomyNode] = []
        self._canonical_nodes: list[CanonicalNode] = []
        self._placements: list[PlacementAssertion] = []
        self._merges: list[Any] = []
        self._warnings: list[str] = []

    # -- load sources --------------------------------------------------------

    def load_taxonomy_snapshot(self, path: Path) -> None:
        """Load an existing taxonomy snapshot (from TaxonomyLoader)."""
        snap = KgV2Snapshot.read(path)
        for node in snap.canonical_nodes:
            if node.type.value == "taxonomy":
                self._taxonomy_nodes.append(
                    TaxonomyNode(
                        id=node.id,
                        path=node.taxonomy_path or [node.slug],
                        label=node.label,
                        embedding=None,
                    )
                )
                self._canonical_nodes.append(node)
            else:
                self._canonical_nodes.append(node)
        self.snapshot.document_versions.extend(snap.document_versions)
        self.snapshot.sections.extend(snap.sections)
        self.snapshot.chunks.extend(snap.chunks)
        self.snapshot.evidence_spans.extend(snap.evidence_spans)
        self.snapshot.relationship_assertions.extend(snap.relationship_assertions)

    def load_canonical_jsonl(self, path: Path) -> None:
        """Load Phase 3 canonicalization output (from CanonicalStore)."""
        store = CanonicalStore()
        nodes, placements, merges = store.load(path)
        self._canonical_nodes.extend(nodes)
        self._placements.extend(placements)
        self._merges.extend(merges)

    def add_candidates(self, candidates: list[Any]) -> None:
        """Run canonicalizer on raw candidates and add the resulting nodes."""
        canonicalizer = Canonicalizer()
        nodes = canonicalizer.canonicalize(candidates)
        self._canonical_nodes.extend(nodes)

    # -- build ---------------------------------------------------------------

    def build(
        self,
        *,
        run_placement: bool = True,
        run_merge_adjudication: bool = True,
        materialize_edges: bool = True,
    ) -> KgV2Snapshot:
        """Assemble the unified snapshot.

        Deduplicates canonical nodes by ID, runs placement and merge
        adjudication if requested, and optionally materializes fast edges.
        """
        # Deduplicate canonical nodes by ID (last one wins)
        seen_ids: dict[str, CanonicalNode] = {}
        for node in self._canonical_nodes:
            if node.id in seen_ids:
                self._warnings.append(f"Duplicate canonical node ID: {node.id}")
            seen_ids[node.id] = node
        self.snapshot.canonical_nodes = list(seen_ids.values())

        # Run placement if no placements were loaded
        if run_placement and not self._placements:
            placement_engine = PlacementEngine(self._taxonomy_nodes)
            from datetime import datetime, timezone
            from .enums import ValidationState

            for node in self.snapshot.canonical_nodes:
                # Skip taxonomy roots themselves
                if node.type.value == "taxonomy":
                    continue
                paths = placement_engine.place(node)
                for path in paths:
                    parent_id = self._resolve_parent_id(path)
                    if parent_id is None:
                        self._warnings.append(
                            f"Could not resolve taxonomy parent for node {node.id} path '{path}'"
                        )
                        continue
                    safe_parent = parent_id.replace("/", "-")
                    # Propagate node's evidence into the placement assertion
                    node_evidence = [
                        eid for eid in (node.primary_assertion_id,)
                        if eid
                    ] or []
                    self._placements.append(
                        PlacementAssertion(
                            id=f"assert-placement-{node.id}-to-{safe_parent}",
                            node_id=node.id,
                            parent_node_id=parent_id,
                            reasoning_summary=f"Placed under '{path}'",
                            confidence=node.confidence,
                            validation_status=ValidationState.CANDIDATE,
                            evidence_ids=node_evidence,
                            created_at=datetime.now(timezone.utc).isoformat(),
                            version=1,
                        )
                    )

        self.snapshot.placement_assertions = self._placements

        # Run merge adjudication if no merges were loaded
        if run_merge_adjudication and not self._merges:
            merge_adjudicator = MergeAdjudicator()
            self._merges = merge_adjudicator.propose(self.snapshot.canonical_nodes)

        self.snapshot.merge_assertions = self._merges

        # Validate assertions before materialization — filter out invalid ones
        self._validate_assertions()

        # Materialize fast edges
        if materialize_edges:
            materializer = EdgeMaterializer(snapshot=self.snapshot)
            materializer.materialize(
                self.snapshot.relationship_assertions, skip_unvalidated=False
            )
            materializer.materialize_placements(
                self.snapshot.placement_assertions, skip_unvalidated=False
            )
            self.snapshot.fast_edges = materializer.write_snapshot(out_path=None)["edges"]

        self.snapshot.metadata = {
            "generator": "canonical_graph_builder",
            "version": "2.1.0",
            "warnings": self._warnings,
            "entity_counts": self.snapshot.entity_counts(),
        }
        return self.snapshot

    # -- write ---------------------------------------------------------------

    def write_snapshot(self, out_path: Path | None = None) -> Path:
        """Write the snapshot to disk and return the path."""
        if out_path is None:
            from datetime import datetime, timezone

            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            out_path = (
                Path("005_Operational-Intelligence-Layer")
                / "graph"
                / "kg-v2"
                / f"{ts}_kg_v2_canonical.json"
            )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        self.snapshot.write(out_path)
        return out_path

    # -- internal ------------------------------------------------------------

    def _validate_assertions(self) -> None:
        """Run AssertionValidator over all assertions and filter out invalid ones."""
        canonical_index = {
            n.id: {"type": n.type.value, "status": n.status}
            for n in self.snapshot.canonical_nodes
        }
        evidence_index = {e.id: e for e in self.snapshot.evidence_spans}
        all_placement_index = {
            p.node_id: p.parent_node_id for p in self.snapshot.placement_assertions
        }
        all_merge_index = {
            m.from_node_id: m.to_node_id for m in self.snapshot.merge_assertions
        }

        valid_placements: list[PlacementAssertion] = []
        for p in self.snapshot.placement_assertions:
            # Exclude current placement from conflict index
            placement_index = dict(all_placement_index)
            placement_index.pop(p.node_id, None)
            validator = AssertionValidator(
                canonical_index=canonical_index,
                evidence_index=evidence_index,
                placement_index=placement_index,
                merge_index=all_merge_index,
            )
            result = validator.validate_placement(p)
            if result.passed:
                valid_placements.append(p)
            else:
                self._warnings.append(
                    f"Placement {p.id} rejected: {'; '.join(result.errors)}"
                )
        self.snapshot.placement_assertions = valid_placements

        valid_merges = []
        for m in self.snapshot.merge_assertions:
            # Exclude current merge from duplicate index
            merge_index = dict(all_merge_index)
            merge_index.pop(m.from_node_id, None)
            merge_index.pop(m.to_node_id, None)
            validator = AssertionValidator(
                canonical_index=canonical_index,
                evidence_index=evidence_index,
                placement_index=all_placement_index,
                merge_index=merge_index,
            )
            result = validator.validate_merge(m)
            if result.passed:
                valid_merges.append(m)
            else:
                self._warnings.append(
                    f"Merge {m.id} rejected: {'; '.join(result.errors)}"
                )
        self.snapshot.merge_assertions = valid_merges

        valid_relationships = []
        for r in self.snapshot.relationship_assertions:
            validator = AssertionValidator(
                canonical_index=canonical_index,
                evidence_index=evidence_index,
                placement_index=all_placement_index,
                merge_index=all_merge_index,
            )
            result = validator.validate_relationship(r)
            if result.passed:
                valid_relationships.append(r)
            else:
                self._warnings.append(
                    f"Relationship {r.id} rejected: {'; '.join(result.errors)}"
                )
        self.snapshot.relationship_assertions = valid_relationships

    def _resolve_parent_id(self, path: str) -> str | None:
        """Resolve a taxonomy path string to a parent node ID."""
        for tn in self._taxonomy_nodes:
            if "/".join(tn.path) == path:
                return tn.id
        return None
