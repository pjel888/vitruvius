# Source Grounding Gap Workqueue Context

Task statement: implement the next real improvement after the read-only source-grounding inventory and Explorer context pass.

Desired outcome: produce proposal-only, ranked source/resource gap artifacts from the existing AEC backbone, Resource Layer metadata, and optional relationship overlay run. The operator should be able to inspect which high-value nodes and relationships need source/resource support next, without mutating the active graph or Resource Layer.

Known facts/evidence:
- `aec-source-grounding-inventory` exists in `scripts/vitruvius/kg/source_grounding_inventory.py`.
- Latest smoke inventory `SOURCE_GROUNDING_SMOKE` reported 10,018 nodes, 13,670 relationships, 8 source-backed nodes, 4,344 source-backed relationships, 2,757 relationship overlay records, and 1,255 node consolidation overlay records.
- Roadmap state says source/resource gap closure is the next concrete action before answer composition, database projection, or new relationship volume.
- Resource Layer registries are file-backed under `006_System-Manifests/resource-layer/`.

Constraints:
- No active graph mutation.
- No Resource Layer mutation.
- No Neo4j/Postgres writes.
- No protected source text exposure.
- No AI truth admission.
- Proposal artifacts only.

Unknowns/open questions:
- Resource coverage is very sparse at node-link level, so deterministic resource proposals may be broad. The implementation must mark these as candidate review items, not admissions.
- Existing Resource Layer has only a small number of resources, so proposal quality is bounded by available metadata.

Likely codebase touchpoints:
- `scripts/vitruvius/kg/source_grounding_inventory.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_source_grounding_inventory.py`
- `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `docs/knowledge-graph/aec-explorer-overlay-campaigns.md`
