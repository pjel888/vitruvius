# AEC-MEPFS Domain Cluster Interrelationships Validation

Date: 2026-05-01

## Scope

Validated the rights-safe, file-backed domain-cluster enrichment of the AEC-MEPFS Backbone. No protected source payloads, live Neo4j writes, graph rebuild/reload/reset, feature flag cutover, or destructive graph operations were performed.

## Changed artifacts

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `scripts/vitruvius/kg/domain_cluster_enrichment.py`
- `scripts/vitruvius/kg/backbone_graph_quality.py`
- `scripts/vitruvius/kg/backbone_shadow_staging.py`
- Targeted Python/API tests and documentation files listed in git diff.

## Metrics

- Nodes: 9,880 -> 9,939 (+59)
- Relationships: 13,285 -> 13,459 (+174)
- Source-rights rows: 106 -> 114 (+8)
- Resolver golden cases: 117 -> 124 (+7)
- Introduced domain interrelationships: 115
- Introduced hierarchy relationships: 59
- Generic governed relationships: 0
- Orphan nodes: 0

## Validation commands

```powershell
$env:PYTHONPATH='scripts'
python -m vitruvius.kg.backbone_graph_quality --run-id 20260501T040000Z_GRAPH_QUALITY --introduced-generation-method steward_governed_aec_mepfs_domain_cluster_interrelationships_from_source_family_research
python -m vitruvius.kg.backbone_shadow_staging --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json --run-id 20260501T040000Z_DOMAIN_CLUSTER_SHADOW
python -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260501T040000Z_DOMAIN_CLUSTER_SHADOW --artifact 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T040000Z_DOMAIN_CLUSTER_SHADOW/shadow-backbone-staging.json --producer-report 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T040000Z_DOMAIN_CLUSTER_SHADOW/shadow-staging-report.json
python -m vitruvius.kg.backbone_resolver_qa --fixture scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json --run-id 20260501T040000Z_DOMAIN_CLUSTER_RESOLVER_QA
python -m pytest scripts/tests/test_kg_domain_cluster_enrichment.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py -q
cd api; bun test v2Backbone.test.ts; bun test v2Resolver.test.ts
```

## Results

- Graph quality: passed. Report: `006_System-Manifests/aec-mepfs-backbone/graph-quality/20260501T040000Z_GRAPH_QUALITY/graph-quality-report.json`.
- Shadow staging: passed. Report: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T040000Z_DOMAIN_CLUSTER_SHADOW/shadow-staging-report.json`.
- Shadow consumer: passed. Report: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T040000Z_DOMAIN_CLUSTER_SHADOW/shadow-staging-consumer-report.json`.
- Resolver QA: passed, 124/124 cases. Report: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T040000Z_DOMAIN_CLUSTER_RESOLVER_QA/resolver-qa-report.json`.
- Python tests: 83 passed.
- API backbone tests: 73 passed.
- API resolver tests: 15 passed.

## Notes

- The graph quality validator reports 514 duplicate normalized labels as a pre-existing broad-taxonomy warning class, not a blocker for this enrichment. Introduced nodes and relationships pass the stricter checks.
- `chunkhound research` remained unavailable because no LLM provider is configured; regex/index refresh paths still ran via the project wrapper.
- One failed shadow consumer run with mismatched run id was discarded and rerun with matching producer/artifact run id.
