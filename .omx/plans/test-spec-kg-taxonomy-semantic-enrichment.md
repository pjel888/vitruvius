# Test Spec - KG Taxonomy Semantic Enrichment

## Required checks
1. Contract validation for admitted backbone fixture.
2. New deterministic enrichment idempotency and content-count tests.
3. Broad taxonomy enrichment idempotency after targeted additions.
4. Shadow staging generation with new run ID.
5. Safety grep for blocked runtime/protected/Neo4j operations in new script/tests/artifacts.
6. Git diff/path review to confirm source-of-truth graph content changed and no raw-source/API/Explorer runtime files changed.

## Commands
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_targeted_taxonomy_semantic_enrichment.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_broad_taxonomy_semantic_enrichment.py scripts/tests/test_kg_backbone_shadow_staging.py -q`
- `python3 scripts/vitruvius/kg/backbone_shadow_staging.py --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json --run-id 20260429T065436Z`
- Safety grep over changed enrichment source, tests, reports, and staging artifacts.
