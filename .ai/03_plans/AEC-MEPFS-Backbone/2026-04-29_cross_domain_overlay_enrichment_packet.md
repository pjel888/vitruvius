# Cross-Domain Overlay Enrichment Packet

Status: VALIDATED  
Date: 2026-04-29  
Run id: 20260429T075023Z  
Authority: project-owner directive to continue AEC-MEPFS KG enrichment with Kimi-only model-assisted research and no live/protected graph operations.

## Purpose

Improve semantic connectedness and practical AEC-MEPFS usefulness by adding governed, source-backed cross-domain relationships and applicability overlays for anchorage/support coordination, commissioning/handover workflows, operational resilience/continuity, and jurisdiction/code applicability.

## Allowed scope

- Add real overlay/reference nodes only where endpoints are missing.
- Improve existing nodes with aliases, source-family IDs, provenance, and semantic node-kind metadata.
- Add governed relationships using only registry-valid predicates.
- Add metadata-only source-rights rows with explicit no-ingest boundaries.
- Regenerate file-backed shadow staging artifacts.
- Update tests and state docs to reflect the new file-backed graph.

## Blocked scope

- No Neo4j/live graph mutation or promotion.
- No KG rebuild/reload/reset/destructive graph operation.
- No protected content ingestion.
- No standard clauses, tables, figures, diagrams, or copied payloads.
- No Codex Spark enrichment provider usage.
- No placeholder/demo/TODO graph nodes.

## Implementation checklist

- [x] Inspect current graph fixture, source-rights registry, prior reports, predicate constraints, and API/backbone tests.
- [x] Verify Kimi-only enrichment routing remains active and Codex Spark is not active for enrichment.
- [x] Add deterministic enrichment script: `scripts/vitruvius/kg/cross_domain_overlay_enrichment.py`.
- [x] Add 91 real BackboneNode records and 460 governed relationships.
- [x] Improve 27 existing nodes with aliases/source-family metadata.
- [x] Add 10 metadata-only source-rights registry references.
- [x] Regenerate shadow staging and consumer reports for `20260429T075023Z`.
- [x] Add regression tests for idempotency, semantic counts, aliases, source-rights boundaries, and contract expectations.
- [x] Complete full validation matrix and Kimi final review.

## Plan critique

- **Rejected new predicate invention.** Existing governed predicates are enough, and new vocabulary would raise schema/test risk.
- **Rejected bulk node addition as the main value.** The requested phase is relationship/applicability quality, so the graph adds only necessary overlay/source nodes and focuses on semantic links.
- **Rejected protected-source ingestion.** All source usage is metadata-only with explicit registry boundaries.
- **Rejected live promotion.** This remains a file-backed/staging workflow until external production authority exists.

## Deliverables

- Fixture update: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- Enrichment script: `scripts/vitruvius/kg/cross_domain_overlay_enrichment.py`
- Source-rights registry update: `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- Test coverage: `scripts/tests/test_kg_cross_domain_overlay_enrichment.py`, updated backbone/API tests
- Enrichment report: `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/20260429T075023Z/cross-domain-overlay-enrichment-report.json`
- Shadow artifacts: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T075023Z/`

## Rollback

Revert the files from this slice. No live graph, Neo4j, protected-content, API route logic, or production runtime state is mutated.
