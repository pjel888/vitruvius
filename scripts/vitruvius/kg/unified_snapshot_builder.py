"""UnifiedSnapshotBuilder — combine all graph layers into one snapshot.

Orchestrates:
- TaxonomyLoader (existing concepts + taxonomy roots from disk)
- EvidenceMaterializer (documents, sections, chunks, spans, relationships)
- Placement assertion generation for concepts with taxonomy paths
- Edge materialization from all assertion types

Produces a single ``KgV2Snapshot`` that is the rebuild source of truth.

Usage::

    from vitruvius.kg.unified_snapshot_builder import UnifiedSnapshotBuilder
    builder = UnifiedSnapshotBuilder(repo_root=Path("."))
    snapshot = builder.build()
    builder.write_snapshot()
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .edge_materializer import EdgeMaterializer
from .enums import ValidationState
from .evidence_materializer import EvidenceMaterializer, TaxonomyLoader
from .json_evidence_store import KgV2Snapshot
from .rule_extractor import RuleExtractor
from .schemas import PlacementAssertion


class UnifiedSnapshotBuilder:
    """Build a unified knowledge graph snapshot from all canonical sources."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)
        self._warnings: list[str] = []

    # -- public API ----------------------------------------------------------

    def build(self) -> KgV2Snapshot:
        """Run the full build pipeline and return the unified snapshot."""
        # 1. Load taxonomy and concepts
        taxonomy_loader = TaxonomyLoader(self.repo_root)
        taxonomy_snapshot = taxonomy_loader.load_all()
        self._warnings.extend(taxonomy_loader._warnings)

        # 2. Load evidence graph (documents, relationships, etc.)
        evidence_materializer = EvidenceMaterializer(self.repo_root)
        evidence_snapshot = evidence_materializer.materialize_all()
        self._warnings.extend(evidence_materializer._warnings)

        # 3. Merge into unified snapshot (evidence side first)
        unified = KgV2Snapshot()
        unified.document_versions = evidence_snapshot.document_versions
        unified.sections = evidence_snapshot.sections
        unified.chunks = evidence_snapshot.chunks
        unified.evidence_spans = evidence_snapshot.evidence_spans
        unified.relationship_assertions = evidence_snapshot.relationship_assertions

        # 4. Merge canonical nodes (taxonomy + concepts)
        # Deduplicate by ID; taxonomy loader wins over evidence materializer
        # for canonical nodes since it loads from the canonical layer directly.
        unified.canonical_nodes = list(taxonomy_snapshot.canonical_nodes)

        # 5. Phase 2 — Atomic rule extraction
        # Convert document→concept assertions into rule nodes and rewire edges.
        rule_extractor = RuleExtractor(snapshot=unified)
        rule_extractor.extract_all()
        self._warnings.extend(rule_extractor._warnings)

        # 6. Generate placement assertions for concepts that have taxonomy_path
        placement_assertions = self._generate_placements(unified.canonical_nodes)
        unified.placement_assertions = placement_assertions

        # 7. Materialize fast edges from all assertions
        materializer = EdgeMaterializer(snapshot=unified)
        materializer.materialize(
            unified.relationship_assertions, skip_unvalidated=False
        )
        materializer.materialize_placements(
            unified.placement_assertions, skip_unvalidated=False
        )
        unified.fast_edges = materializer.write_snapshot(out_path=None)["edges"]

        # 8. Metadata
        unified.metadata = {
            "generator": "unified_snapshot_builder",
            "version": "2.1.0",
            "warnings": self._warnings,
            "entity_counts": unified.entity_counts(),
        }
        return unified

    def write_snapshot(self, snapshot: KgV2Snapshot | None = None, out_path: Path | None = None) -> Path:
        """Write the snapshot to disk and return the path."""
        if snapshot is None:
            snapshot = self.build()
        if out_path is None:
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            out_path = (
                self.repo_root
                / "005_Operational-Intelligence-Layer"
                / "graph"
                / "kg-v2"
                / f"{ts}_kg_v2_unified.json"
            )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write(out_path)
        return out_path

    # -- internal ------------------------------------------------------------

    def _generate_placements(
        self, nodes: list[Any]
    ) -> list[PlacementAssertion]:
        """Create PlacementAssertion records for concepts with taxonomy_path."""
        placements: list[PlacementAssertion] = []
        ts = datetime.now(timezone.utc).isoformat()

        # Build taxonomy root index for path → id resolution
        taxonomy_index: dict[str, str] = {}
        for node in nodes:
            if node.type.value == "taxonomy":
                path_key = "/".join(node.taxonomy_path)
                taxonomy_index[path_key] = node.id

        for node in nodes:
            if node.type.value == "taxonomy":
                continue
            if not node.taxonomy_path:
                continue

            # Generate one placement assertion per segment in the taxonomy path
            # The full path is the primary parent
            full_path = "/".join(node.taxonomy_path)
            parent_id = taxonomy_index.get(full_path)
            if parent_id is None:
                # Fallback: try to find a matching taxonomy root
                for tid, tpath in taxonomy_index.items():
                    if tid == full_path or full_path.startswith(tid + "/"):
                        parent_id = tpath
                        break

            if parent_id is None:
                # No matching taxonomy node found — skip placement
                continue

            safe_parent = parent_id.replace("/", "-")
            node_evidence = [
                eid for eid in (node.primary_assertion_id or "").split(",")
                if eid
            ] or []
            placements.append(
                PlacementAssertion(
                    id=f"assert-placement-{node.id}-to-{safe_parent}",
                    node_id=node.id,
                    parent_node_id=parent_id,
                    reasoning_summary=f"Backfilled from taxonomy_path: {full_path}",
                    confidence=node.confidence,
                    validation_status=node.status,
                    evidence_ids=node_evidence,
                    created_at=ts,
                    version=1,
                )
            )

        return placements
