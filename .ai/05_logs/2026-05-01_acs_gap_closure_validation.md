# ACS Gap Closure Validation Log

Date: 2026-05-01

## Scope
Closed remaining safe Architecture-Civil-Structural graph gaps and deferred metadata/hygiene items without crossing production/live graph, KG rebuild/reset, or protected source admission boundaries.

## Implemented
- Added 2 ACS Backbone nodes: `CIV.MIS.UCC.SUC` Subsurface Utility Conflict Review and `CIV.HDI.FCI.DFE` Design Flood Elevation Interface.
- Added 11 typed ACS relationships covering utility conflict review, flood-elevation coordination, and slope-stability connections.
- Added resolver cases `RES-ACS-009`, `RES-ACS-010`, and `RES-ACS-011`.
- Removed 11 historical self-loop relationships.
- Added graph-quality diagnostics and tests for self-loops, duplicate samples, same-parent duplicate labels, generic `predicate`/`edge_type`, and introduced non-hierarchy orphan nodes.
- Added allowlisted API/explorer edge metadata exposure while keeping compact render metadata bounded and source-payload safe.

## Evidence artifacts
- Enrichment before self-loop cleanup: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T062000Z_ACS_GAP_CLOSURE/architecture-civil-structural-enrichment-report.json`
- Post-cleanup idempotence report: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T064500Z_ACS_GAP_CLOSURE_POST_CLEANUP/architecture-civil-structural-enrichment-report.json`
- Graph quality: `006_System-Manifests/aec-mepfs-backbone/graph-quality/20260501T062500Z_ACS_GAP_CLOSURE_GRAPH_QUALITY/graph-quality-report.json`
- Shadow staging: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T062700Z/shadow-staging-consumer-report.json`
- ACS quality: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality/20260501T062900Z_ACS_GAP_CLOSURE_QUALITY_FINAL/architecture-civil-structural-quality-report.json`
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T063000Z_ACS_GAP_CLOSURE_RESOLVER_QA/resolver-qa-report.json`

## Validation commands
- `bun test api` -> 117 passed.
- `$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_backbone_graph_quality.py scripts/tests/test_kg_architecture_civil_structural_enrichment.py scripts/tests/test_kg_domain_cluster_enrichment.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_shadow_staging.py -q` -> 98 passed.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.backbone_graph_quality --run-id 20260501T062500Z_ACS_GAP_CLOSURE_GRAPH_QUALITY --repo-root . --introduced-generation-method steward_governed_architecture_civil_structural_interrelationships_from_source_family_research --source-rights-registry .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` -> ok true, errors empty.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.architecture_civil_structural_quality --repo-root . --run-id 20260501T062900Z_ACS_GAP_CLOSURE_QUALITY_FINAL` -> score 100/100.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.backbone_resolver_qa --repo-root . --run-id 20260501T063000Z_ACS_GAP_CLOSURE_RESOLVER_QA` -> 135/135 cases passed.

## Metrics
- Nodes: 10,004 before gap closure -> 10,006 after.
- Relationships: 13,610 before gap closure -> 13,610 after; 11 added and 11 self-loops removed.
- Resolver cases: 132 -> 135.
- ACS introduced nodes: 65 -> 67.
- ACS typed non-hierarchy relationships: 86 -> 95.
- ACS hierarchy relationships: 65 -> 67.
- Global self-loop relationships: 11 -> 0.
- Generic relationships: 0 -> 0.
- Quality score: 100/100.

## Tooling notes
- Pre-change GitNexus impact for `buildShadowBackboneTaxonomyPreview` returned HIGH risk, so the API metadata implementation stayed allowlisted and tests were updated across dependent surfaces.
- Kimi CLI was attempted for critique but did not return a usable final response before its step limit; subagent peer review was used instead.

## Post-change code-intelligence checks
- `bash ./scripts/refresh_code_intelligence.sh` -> exit 0. GitNexus already up to date; ChunkHound processed 19 changed files with 0 errors; code-review-graph full build completed. Warnings recorded: many YAML files still report missing `tree-sitter-yaml`; embedding batches still emit `[EmbSvc-AsyncBatch] '_Task' object has no attribute 'elapsed'` while the wrapper exits 0.
- `cmd /c npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` -> exit 0, 15 files / 77 symbols, 8 affected processes, high risk. This high risk is expected because the API edge-metadata change touches `buildShadowBackboneTaxonomyPreview`, `buildShadowBackboneNodePreview`, and `buildAecMepfsNodeDetail`; pre-change impact was measured and the dependent API suite now passes.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo .` -> exit 0, 23 changed files, risk score 0.00, 0 affected flows, 0 test gaps.
- `chunkhound search --regex "RAW_SOURCE_ROOT|immutable raw source custody layer|Subsurface Utility Conflict Review|shadowBackboneEdgeMetadataFromPreview"` -> exit 0, 49 matches, confirming indexed coverage for path guards, ACS gap nodes, and API sanitizer.

## Path guard review fixes
- Added output-path confinement for ACS enrichment, ACS quality, and graph-quality reports so generated reports must stay under their expected `006_System-Manifests/aec-mepfs-backbone/.../<run_id>/<expected-report-name>.json` roots.
- Added raw-source custody write guards for ACS enrichment write targets so `001_Raw-Source-Layer` cannot be used as a rewritten Backbone/source/readiness target.
- Added tests for raw-source output rejection, unexpected report filename rejection, and raw-source enrichment write-target rejection.
- Removed stray control characters from changed `.ai` text artifacts and fixed `git diff --check` whitespace.

## Final review status
- Read-only subagent review initially requested changes for path guards, Kimi provenance drift, enrichment-report final-state clarity, and whitespace/control-character hygiene.
- Implemented path confinement and raw-source write-target guards, reconciled Kimi provenance wording, added a post-cleanup idempotence report, removed control characters from changed `.ai` text files, and confirmed `git diff --check` has no whitespace errors beyond line-ending warnings.
- Final validation after review fixes: `bun test api` -> 117 passed; targeted pytest suite -> 98 passed; `git diff --check` -> exit 0 with line-ending warnings only; post-change code-intelligence wrapper and detect-change checks completed as recorded above.
