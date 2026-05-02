# ACS Remaining-Gaps Follow-Up Validation

Date: 2026-05-01

## Scope

Validated the second Architecture-Civil-Structural remaining-gap follow-up pass. The pass is file-backed and metadata-only. It does not mutate production Neo4j, rebuild/reset the KG, ingest protected source payloads, or admit numerical/jurisdiction-specific design criteria.

## Implemented

- Added 8 ACS nodes and 35 governed relationships net since the prior gap closure.
- Added resolver cases `RES-ACS-012` through `RES-ACS-015`.
- Added duplicate normalized-label context index generation.
- Added AHJ/project-basis metadata fields for enriched ACS relationships.
- Preserved the new metadata through shadow staging, API preview serialization, `GraphEdge`, `RelationDetail`, and `BackboneShadowGraphPreview` TypeScript contracts.
- Added a shadow-staging predicate-registry cross-check so governed relationship predicates used by the staged backbone must be present in the staged predicate registry, not only in the static contract vocabulary.

## Key metrics

- Backbone nodes: 10,014.
- Governed relationships: 13,645.
- Source-rights rows: 123.
- Resolver golden cases: 139.
- ACS introduced nodes: 75.
- ACS typed non-hierarchy relationships: 122.
- ACS hierarchy relationships: 75.
- Duplicate normalized labels: 514 groups, 1,377 nodes, all contextual; same-parent duplicates: 0.
- Graph-quality errors: 0.
- ACS quality score: 100/100.

## Validation commands

- `python -m vitruvius.kg.backbone_graph_quality --repo-root . --run-id 20260501T072300Z_ACS_REMAINING_GAPS_GRAPH_QUALITY --introduced-generation-method steward_governed_architecture_civil_structural_interrelationships_from_source_family_research --source-rights-registry .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` - passed.
- `python -m vitruvius.kg.architecture_civil_structural_quality --repo-root . --run-id 20260501T072400Z_ACS_REMAINING_GAPS_QUALITY` - passed, 100/100.
- `python -m vitruvius.kg.backbone_shadow_staging --repo-root . --run-id 20260501T071900Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` - passed.
- `python -m vitruvius.kg.backbone_shadow_report_reader --repo-root . --run-id 20260501T071900Z` - passed.
- `python -m vitruvius.kg.backbone_resolver_qa --repo-root . --run-id 20260501T072100Z_ACS_REMAINING_GAPS_RESOLVER_QA` - passed, 139/139 resolver cases.
- `python -m pytest scripts/tests/test_kg_backbone_graph_quality.py scripts/tests/test_kg_architecture_civil_structural_enrichment.py scripts/tests/test_kg_domain_cluster_enrichment.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_shadow_staging.py -q` - 100 passed.
- `bun test api` - 118 passed.
- `bun test explorer` - 106 passed.

## Notes

- `docs/shared/agent-tiers.md` is missing, so Ralph/Ultrawork agent tier selection used local STANDARD/THOROUGH judgment and recorded the missing file as a tooling limitation.
- Initial shadow staging caught unsupported governed predicates (`depends_on`, `supports`). The final implementation retained mechanism-specific `relation_type` values but changed governed predicates to the registered vocabulary.
- Kimi review completed on the follow-up pass and recommended duplicate-context reporting plus explicit source-family/adopted-basis metadata; both were implemented without blindly following numerical or jurisdiction-specific suggestions.
- Architect review flagged the missing `BackboneShadowGraphPreview` metadata fields and lack of staged predicate-registry compatibility guard. Both blockers were fixed and covered by targeted tests before final validation.

## Post-change intelligence refresh

- `bash ./scripts/refresh_code_intelligence.sh` - exited 0 after changes. GitNexus was already up to date; ChunkHound reindexed successfully. code-review-graph rebuilt but retained known environment warnings: missing `tree-sitter-yaml` for YAML parsing and `[EmbSvc-AsyncBatch] '_Task' object has no attribute 'elapsed'` embedding-service batch errors. These warnings were recorded; Python/API/Explorer validations passed independently.

## Post-change impact checks

- `npx.cmd --yes gitnexus@1.6.4-rc.32 impact stage_shadow_backbone --repo vitruvius --direction upstream --include-tests` - LOW risk; direct caller `main` plus module file.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 impact BackboneShadowGraphPreview --repo vitruvius --direction upstream --include-tests` - CRITICAL import-surface risk because `explorer/src/types/index.ts` is widely imported. The change was additive optional fields only and was mitigated with `bun test explorer` and API tests.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope all` - HIGH risk, 16 tracked files and 8 affected execution flows; output included two `Prepare timed out after 30000ms` warnings. Mitigation: targeted Python KG tests, API tests, Explorer tests, shadow staging, graph quality, ACS quality, and resolver QA all passed.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo . --brief` - analyzed 24 changed files, 0 changed functions/classes, 0 affected flows, 0 test gaps, overall risk score 0.00.
- `chunkhound search --regex "duplicate_label_context|applicability_basis|design_basis_status|CIV\\.PAV\\.SBG|RES-ACS-015|BackboneShadowGraphPreview"` - succeeded and found expected docs/artifact/type coverage.
- `git diff --check` - exited 0 with line-ending normalization warnings only.
