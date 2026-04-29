# Targeted Taxonomy Semantic Enrichment Packet

Status: VALIDATED  
Date: 2026-04-29  
Run id: 20260429T065436Z  
Authority: project-owner directive to improve knowledge-graph content materially and use Kimi instead of Codex Spark for enrichment research/synthesis.

## Purpose

Strengthen the AEC-MEPFS backbone with source-backed standards-family nodes, real discipline-topic nodes, aliases, provenance fields, and semantic relationships after broad L4 scaffold cleanup.

## Allowed scope

- Add metadata-only standards-family and guidance-family taxonomy nodes.
- Add real, useful AEC-MEPFS L4 discipline topics under existing parents.
- Add aliases/acronyms and concise descriptions.
- Add governed relationships using existing predicates.
- Add source-rights registry rows with explicit no-ingest boundaries.
- Add deterministic generator and regression tests.
- Regenerate shadow staging and consumer reports.
- Update file-backed API tests for changed counts and semantic edge types.

## Blocked scope

- No protected content ingestion.
- No standard text, table, figure, diagram, or clause storage.
- No Neo4j writes, graph reset, reload, rebuild, or production promotion.
- No broad live-runtime authorization.
- No placeholder/demo/mock graph content.
- No Codex Spark use for enrichment research or taxonomy synthesis.

## Implementation checklist

- [x] Inspect current backbone fixture, schema constraints, prior shadow staging, source registry, and validation scripts.
- [x] Use Kimi for advisory taxonomy/source-family synthesis.
- [x] Add deterministic enrichment script: `scripts/vitruvius/kg/targeted_taxonomy_semantic_enrichment.py`.
- [x] Add 141 real BackboneNode records and 415 governed relationships.
- [x] Add 12 metadata-only source-rights registry rows.
- [x] Add regression tests for idempotency, schema safety, relationship counts, and source-rights no-ingest boundaries.
- [x] Regenerate shadow staging artifacts for `20260429T065436Z`.
- [x] Update API expectations for latest file-backed graph counts and semantic edges.
- [x] Run focused Python and API verification.

## Plan critique

- **Rejected adding a new edge vocabulary first.** Existing predicates already supported the intended semantics, and new predicates would widen schema risk.
- **Rejected ingesting or summarizing protected standards text.** The source-rights registry has no clearance for that; metadata-only source-family references are sufficient for this slice.
- **Rejected broad all-domain expansion in one pass.** The graph already had breadth; the highest immediate value was targeted standards-family connectivity and domain-specific semantic edges.
- **Rejected global provider rewiring.** A task-specific Kimi enrichment route in `opencode.json` avoids breaking unrelated workflows while satisfying the active enrichment requirement.

## Deliverables

- Fixture update: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- Enrichment script: `scripts/vitruvius/kg/targeted_taxonomy_semantic_enrichment.py`
- Source-rights registry update: `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- Test coverage: `scripts/tests/test_kg_targeted_taxonomy_semantic_enrichment.py`, updated backbone/broad/API tests
- Taxonomy report: `006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260429T065436Z/targeted-semantic-enrichment-report.json`
- Shadow artifacts: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T065436Z/`

## Rollback

Revert this commit. The change is file-backed data, tests, docs, reports, and shadow artifacts only; no live graph or production runtime mutation is performed.
