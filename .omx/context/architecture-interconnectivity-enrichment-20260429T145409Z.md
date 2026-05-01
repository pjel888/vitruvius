# Architecture Interconnectivity Enrichment Context Snapshot

## Task statement
Increase semantic interconnectedness across the architecture/AEC/LEA-ALE file-backed knowledge graph with dedicated materials taxonomy improvements, notable architects, Pritzker laureates, engineers/architect-engineers, project/work anchors, resolver/API golden cases, relationship quality controls, and continued learner-facing label/highlight correctness.

## Desired outcome
Graph content and resolver behavior materially improve for multi-hop architectural reasoning: people -> roles -> works -> materials/systems/movements and LEA/ALE study paths.

## Known facts/evidence
- Prior cleanup commit: 76d83ef2 Keep learner graph concepts clean and canvas controls explicit.
- Current admitted learner graph after cleanup is expected around 9,502 nodes / 11,617 relationships in current shadow artifacts.
- Raw/local source-reference rows must remain in source-rights/provenance only, not learner-facing concept nodes.
- Explorer direct visible-neighborhood highlighting is already fixed and tested, but must remain protected.

## Constraints
- Use Kimi for model-assisted research/synthesis/final audit; do not use Codex Spark for enrichment.
- No protected source payload ingest; no exam questions/reviewer text/answer keys/tables/clauses/figures/diagrams.
- No Neo4j/live promotion, KG rebuild/reload/reset, or destructive graph ops.
- Preserve deterministic IDs, schema conventions, source-rights boundaries, and Windows-safe generated file names.

## Unknowns/open questions
- Exact current schema/valid predicate set for person/work/material relationships.
- Whether existing material/person/work nodes exist and should be improved rather than duplicated.
- Existing resolver golden case format for adding interconnectivity queries.
- Available Kimi invocation surface in repo/opencode.

## Likely codebase touchpoints
- scripts/vitruvius/kg/*enrichment*.py
- scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
- scripts/tests/test_kg_*
- api/v2Backbone.test.ts and resolver fixtures/tests
- .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json
- 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T101500Z
- opencode.json
