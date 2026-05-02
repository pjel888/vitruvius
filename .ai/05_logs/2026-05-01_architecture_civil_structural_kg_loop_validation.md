# Architecture Civil Structural KG Loop Validation

Date: 2026-05-01

## Validation commands
- `python -m pytest scripts/tests/test_kg_architecture_civil_structural_enrichment.py scripts/tests/test_kg_domain_cluster_enrichment.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_shadow_staging.py -q` -> 88 passed.
- `(cd api && bun test v2Backbone.test.ts)` -> 73 passed.
- `(cd api && bun test v2Resolver.test.ts)` -> 15 passed.
- `python -m vitruvius.kg.backbone_graph_quality --run-id 20260501T054000Z_ACS_GRAPH_QUALITY_FINAL --introduced-generation-method steward_governed_architecture_civil_structural_interrelationships_from_source_family_research --source-rights-registry .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` -> ok true, 0 errors.
- `python -m vitruvius.kg.architecture_civil_structural_quality --run-id 20260501T054000Z_ACS_QUALITY_FINAL` -> ok true, quality score 100/100.
- `python -m vitruvius.kg.backbone_resolver_qa --run-id 20260501T054000Z_ACS_RESOLVER_QA` -> 132/132 cases passed.
- `python -m vitruvius.kg.backbone_shadow_staging --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json --run-id 20260501T054000Z` -> ok true.
- `python -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260501T054000Z` -> ok true.

## Result
The ACS quality gates are satisfied for the implemented file-backed loop. Historical duplicate labels remain as a warning and future gap, not a critical failure of this ACS pass.

## Post-change code intelligence
- `bash ./scripts/refresh_code_intelligence.sh` -> exit 0. GitNexus already up to date; ChunkHound completed; code-review-graph full build completed. Warnings/errors recorded from tool output: multiple YAML files could not be parsed because `tree-sitter-yaml` is missing; code-review-graph embedding batches emitted `_Task` object has no attribute `elapsed`, but the build still completed and returned exit 0.
- `npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` -> exit 0, low risk, 11 tracked files / 31 symbols, 0 affected processes; warnings included Git line-ending notices and two file-symbol prepare timeouts.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo .` -> exit 0, 19 changed files, risk score 0.00, no affected flows/test gaps.
- Initial `chunkhound search ... --limit 20` failed because this installed ChunkHound command does not accept `--limit`; rerun without `--limit` succeeded and found ACS enrichment symbols and `transfers_gravity_load_to` relationships.
