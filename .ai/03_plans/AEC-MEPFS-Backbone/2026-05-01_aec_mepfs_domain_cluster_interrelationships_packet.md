---
task: aec-mepfs-domain-cluster-interrelationships
phase: 05-07
created: 2026-05-01
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Plan — AEC-MEPFS Domain Cluster Interrelationships

## Decision
Implement a rights-safe file-backed enrichment pass that adds 5-8 deeply interconnected AEC-MEPFS clusters, enriches edges with mechanism metadata while preserving existing governed predicates, adds source-rights rows, adds graph-quality validation, stages a new shadow graph run, and records before/after metrics.

## Drivers
- Preserve the current governed predicate registry and source-rights boundaries.
- Improve reasoning utility through cross-domain directional edges, not filler nodes.
- Avoid API route-shape edits due HIGH GitNexus impact.
- Keep changes deterministic, idempotent, and testable.

## Alternatives considered
1. Add dozens of new predicates such as supplies_air_to and monitored_by: rejected because Vitruvius P10 requires schema/AD work for predicate expansion and current predicate registry is intentionally constrained.
2. Add hundreds of topical nodes: rejected because user explicitly asked for deep clusters over shallow breadth.
3. Only write documentation: rejected because the repo supports safe file-backed graph/data/test changes.

## Implementation plan
1. Add scripts/vitruvius/kg/domain_cluster_enrichment.py with deterministic node/edge/source definitions and idempotent enrichment functions. [G001-G008]
2. Add scripts/vitruvius/kg/backbone_graph_quality.py to compute inventory and enforce placeholder/provenance/rationale/orphan/duplicate/metadata/relationship checks. [G004-G008]
3. Add optional relationship metadata preservation in _build_shadow_graph without changing existing edge shape when metadata is absent. [G006]
4. Run the enrichment against the admitted fixture, resolver fixture, and source-rights registry. [G001-G003,G007]
5. Generate reports under 06_System-Manifests/aec-mepfs-backbone/domain-cluster-enrichment/<RUN_ID>/ and quality reports under 06_System-Manifests/aec-mepfs-backbone/graph-quality/<RUN_ID>/. [G008]
6. Stage a new shadow graph run and resolver QA run. [G001]
7. Add focused tests for idempotency, cluster traversal, source-rights metadata-only rows, quality validation, and shadow edge metadata preservation. [G006-G008]
8. Update docs/state and validation logs. [G008]

## Plan critique
- [C001] Relationship metadata is useful only if consumers can eventually expose it; this pass preserves it in generated shadow graph artifacts but intentionally avoids API preview route edits because impact is HIGH.
- [C002] Some relationships are source-family grounded rather than clause-level grounded; rationale text must say when a relation is professional synthesis and must not imply universal jurisdictional governance.
- [C003] Existing predicates remain broad, so tests must verify 
elation_type rather than only predicate counts.
- [C004] Adding source rows must not imply content-ingest clearance.

## Execution checklist
- [ ] Create enrichment and quality modules. [G001-G008]
- [ ] Apply enrichment to fixture/source-rights/resolver fixtures. [G001-G007]
- [ ] Generate before/after and graph-quality reports. [G004-G008]
- [ ] Stage shadow graph and resolver QA artifacts. [G001]
- [ ] Add tests for graph reasoning queries. [C001-C004]
- [ ] Run contract, enrichment, quality, shadow, resolver, API, and Explorer focused tests. [G005-G008]
- [ ] Refresh code intelligence and run change-impact checks. [G006]
- [ ] Update validation log, roadmap/state surfaces, and final report. [G008]

## Completion Update - 2026-05-01

Status: implemented and validated.

Evidence:
- Domain-cluster enrichment report: `006_System-Manifests/aec-mepfs-backbone/domain-cluster-enrichment/20260501T040000Z_DOMAIN_CLUSTER_ENRICHMENT/domain-cluster-enrichment-report.json`
- Patch enrichment report: `006_System-Manifests/aec-mepfs-backbone/domain-cluster-enrichment/20260501T040000Z_DOMAIN_CLUSTER_ENRICHMENT_PATCH_01/domain-cluster-enrichment-report.json`
- Graph quality report: `006_System-Manifests/aec-mepfs-backbone/graph-quality/20260501T040000Z_GRAPH_QUALITY/graph-quality-report.json`
- Shadow staging report: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T040000Z_DOMAIN_CLUSTER_SHADOW/shadow-staging-report.json`
- Resolver QA report: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T040000Z_DOMAIN_CLUSTER_RESOLVER_QA/resolver-qa-report.json`
- Validation log: `.ai/05_logs/2026-05-01_aec_mepfs_domain_cluster_interrelationships_validation.md`

Implemented totals: 59 admitted nodes, 174 governed relationships, 8 source-rights rows, 7 resolver cases, 115 typed domain interrelationships, and 59 hierarchy edges.
