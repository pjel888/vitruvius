# AEC Bounded Resolver Contract Static Verification Context

- Task statement: implement the bounded resolver-runtime contract/static-verification slice authorized by `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_bounded_resolver_runtime_contract_packet.md`.
- Desired outcome: static/no-op contract definitions, golden fixtures, tests, generated evidence, validation log, commit and push.
- Known facts/evidence: governance commit `690738c5` is pushed; runtime-governance packet is BOUNDARY_APPROVED but not LIVE_RUNTIME_AUTHORIZED.
- Constraints: do not mount `/v2/resolve*`; do not call hot resolver from API; do not mutate Neo4j; do not rebuild/reload KG; do not ingest protected content; do not change Explorer default behavior; do not add default-on flags; do not claim runtime thresholds; do not edit CanonicalNode/TaxonomyLoader/Neo4jLoader.
- Likely codebase touchpoints: `scripts/vitruvius/kg/backbone_resolver_qa.py`, `scripts/vitruvius/kg/backbone_api_route_inventory.py`, `scripts/tests/fixtures/aec_mepfs_backbone`, `scripts/tests/test_kg_backbone_resolver_qa.py`, `scripts/tests/test_kg_backbone_api_route_inventory.py`, `api/v2Backbone.test.ts`, `.ai/05_logs`.
