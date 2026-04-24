# Post Laws KG Rebuild Relationship Graph Validation - 2026-04-24

## Result

PASS. The current KG snapshot and Neo4j graph are rebuilt from `001-Laws` only and the Explorer-facing rule-title quality gate is clean.

## Build Evidence

- Reset/rebuild report: `006_System-Manifests/runs/kg_pipeline_report_20260424T154833Z.json`
- Rebuilt snapshot after post-audit fixes: `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`
- Snapshot counts: 181 document versions, 313 canonical nodes, 432 relationship assertions, 734 fast edges.
- Neo4j reload: cleared from 2429 nodes to 0, loaded 5911/5911 statements, 0 errors, ended at 2429 nodes.

## Quality Evidence

- Source frontmatter: 181 source pages, 0 non-`001-Laws` paths, 0 invalid/generic titles.
- Conversion layer: 753 files, all under `002_Raw-Conversion-Layer/001-Laws/`.
- Rule title quality: 214 rules, 0 duplicate display labels, 0 generic display labels, 0 display-title truncation markers.
- KG quality report warnings: none.
- Relationship endpoint quality: 0 missing endpoints; 214/214 `SUPPORTED_BY` assertions target evidence/document endpoints.

## Verification Commands

- `PYTHONPATH=scripts pytest -q scripts/tests/test_canonicalize_body.py scripts/tests/test_kg_rule_extractor.py scripts/tests/test_kg_quality_report.py` -> 48 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_source_identity.py scripts/tests/test_kg_pipeline_force_path.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonicalize_integration.py scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_concept_enrichment.py` -> 174 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg_schemas.py scripts/tests/test_kg_unified_snapshot_builder.py scripts/tests/test_evidence_materializer.py scripts/tests/test_edge_materializer.py scripts/tests/test_kg_architectural_invariants.py` -> 86 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg*.py` -> 294 passed.
- `bun test api/perspectiveContracts.test.ts api/sceneStore.test.ts` -> 13 passed.
- `bun test explorer/src/components/graph/VisNetworkHost.test.ts explorer/src/utils/labels.test.ts explorer/src/components/componentInteraction.test.tsx` -> 16 passed.
- `cd explorer && bun run build` -> passed; Vite still reports the existing `vis-network` chunk-size warning.

## Caveats

- The graph includes 2 sources under `001-Laws/refined_markdown/test/...` because that folder is part of the selected subject tree.
- The relationship distribution is still shallow: `DEFINED_BY=214`, `SUPPORTED_BY=214`, `REQUIRES=3`, `RELATED_TO=1`.
- Cross-subject relationship discovery remains deferred until a later aggregate/cross-subject enrichment run.
