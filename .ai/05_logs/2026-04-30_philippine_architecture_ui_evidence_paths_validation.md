# Philippine Architecture UI Evidence Paths Validation — 2026-04-30

## Scope
Focused follow-up for learner-facing Explorer graph cleanliness, current-data-source confidence, Filipino/Philippine architecture evidence paths, resolver/API behavior, and source-rights safety.

## Output state
- Backbone fixture: 9,880 nodes and 13,285 relationships.
- Source-rights registry: 106 rows.
- Resolver fixture: 117 total cases, including 65 architecture interconnectivity cases.
- Current shadow staging run: `20260430T094129Z`.
- Resolver QA rerun: `20260430T094129Z_RESOLVER_QA_RERUN` with 117/117 cases passed.

## Browser/UI verification status
Actual in-app browser tooling was not available from this CLI session. The closest equivalent was completed through Explorer component/integration tests, API graph-source tests, production build, and selector-level highlight assertions.

## Validation commands and results
- `PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py` — passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg_broad_taxonomy_semantic_enrichment.py scripts/tests/test_kg_architecture_interconnectivity_enrichment.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_lea_ale_resolver_deepening.py` — 84 passed.
- `bun test api/v2Backbone.test.ts api/v2Resolver.test.ts explorer/src/components/graph/VisNetworkHost.test.ts` — 126 passed.
- `bun test api explorer` — 195 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests --ignore=scripts/tests/test_mahalanobis_parity.py --ignore=scripts/tests/test_proximity_jump_weight_parity.py --ignore=scripts/tests/test_spatial_edge_builder_parity.py` — 2,466 passed, 21 skipped, 7 warnings.
- Full `PYTHONPATH=scripts pytest -q scripts/tests` was also attempted and hit known unrelated Rust parity wiring failures in `test_mahalanobis_parity.py`, `test_proximity_jump_weight_parity.py`, and `test_spatial_edge_builder_parity.py`; this phase did not touch Rust.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --run-id 20260430T094129Z_RESOLVER_QA_RERUN` — 117/117 resolver cases passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --run-id 20260430T094129Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` — passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260430T094129Z` — passed.
- `python3 -m json.tool` on modified JSON fixtures, source-rights registry, and shadow consumer report — passed.
- Duplicate ID/path, missing edge endpoint, missing parent path, SRC-RAW learner node, and bad learner label checks — all zero.
- `git diff --check` — passed.
- `bun run lint` in `explorer/` — passed.
- `bun run build` in `explorer/` — passed with the existing Vite chunk-size warning only.
- Kimi final read-only audit saved at `.omx/logs/philippine-architecture-ui-evidence-kimi-final-audit.txt` — approved with no blockers.

## Safety confirmation
No protected source payloads, reviewer text, exam questions, answer keys, protected tables, clauses, figures, diagrams, Neo4j/live graph promotion, KG rebuild/reload/reset, or destructive graph operations were introduced.
