# 2026-04-29 Architecture Interconnectivity Enrichment Validation

## Summary
- Baseline: 9502 nodes, 11617 relationships, 95 source-rights rows, 52 resolver cases.
- Output: 9729 nodes, 12376 relationships, 100 source-rights rows, 72 resolver cases.
- Added: 227 nodes, 759 governed relationships, 5 metadata-only source-rights rows, 20 architecture interconnectivity resolver cases.
- Material nodes added or improved: 114.
- Person nodes added or improved: 64.
- Pritzker laureate nodes added or improved: 33.
- Engineer / architect-engineer nodes added or improved: 25.
- Work/project nodes added or improved: 44.
- Person-work-material paths added or improved: 45 conservative lower-bound paths.
- Material-property/method/assembly relationships added or improved: 126.
- LEA/ALE cross-subject relationships added or improved: 46.

## Node label cleanup and UI highlight investigation
- Bad-label patterns checked: `Local raw-source filename metadata`, `raw-source filename metadata`, `metadata-only source-family reference`, `metadata-only source`, `source-family reference`, `protected payload`, `reviewer candidate`, `unknown/private`, `local file`, `registry row`, `planning_reference_only`.
- Affected learner-facing labels found in current graph: 0.
- Nodes renamed in this phase: 0; previous cleanup already moved raw/local source-reference labels out of learner-facing concepts.
- Nodes hidden/reclassified in this phase: 0; source/provenance records remain preserved in source-rights/provenance rows.
- Source/provenance records preserved: 100 source-rights rows total.
- Generator/source-of-truth fixed in this phase: `scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py`; broad auto-population guard updated in `scripts/vitruvius/kg/broad_taxonomy_semantic_enrichment.py` so curated interconnectivity material nodes are not generic-filled by the older broad taxonomy pass.
- `Local raw-source filename metadata for TOA tropical architecture PDF` in learner-facing graph output: absent.
- Tropical Architecture representation remains the clean concept path `ARC.TAC` / Tropical Architecture And Climate Response, with source metadata kept outside learner-facing labels.
- Parent-click highlight root cause from prior verified cleanup: UI-side selected-neighborhood emphasis was too broad/stale; current tests verify direct selected neighborhoods and dimming behavior. No fake relationships were added to mask UI behavior.
- UI verification: `cd explorer && bun test src/components/graph/VisNetworkHost.test.ts src/utils/labels.test.ts` passed 37 tests.

## Graph Integrity Checks
```json
{
  "records": 9729,
  "relationships": 12376,
  "duplicate_ids": 0,
  "duplicate_path_codes": 0,
  "missing_edge_endpoints": 0,
  "missing_parent_paths": 0,
  "bad_learner_labels": 0,
  "generated_direct_person_to_material_edges": 0
}
```

## Validation Commands And Results
- `python3 -m py_compile scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py scripts/vitruvius/kg/broad_taxonomy_semantic_enrichment.py` — passed.
- `PYTHONPATH=scripts python3 scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py --write --report 006_System-Manifests/aec-mepfs-backbone/architecture-interconnectivity/20260429T153000Z/architecture-interconnectivity-report.json` — passed.
- `PYTHONPATH=scripts pytest scripts/tests/test_kg_architecture_interconnectivity_enrichment.py -q` — 6 passed.
- `PYTHONPATH=scripts pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_lea_ale_resolver_deepening.py scripts/tests/test_kg_architecture_interconnectivity_enrichment.py -q` — 59 passed.
- `PYTHONPATH=scripts pytest scripts/tests/test_kg_backbone_resolver_qa.py -q` — 22 passed.
- `PYTHONPATH=scripts pytest scripts/tests/test_kg_broad_taxonomy_semantic_enrichment.py scripts/tests/test_kg_architecture_interconnectivity_enrichment.py -q` — 8 passed.
- `PYTHONPATH=scripts pytest scripts/tests/test_kg*.py -q` — 588 passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --run-id 20260429T153500Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` — passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260429T153500Z` — passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --run-id 20260429T154000Z` — 72/72 resolver cases passed.
- `cd api && bun test v2Resolver.test.ts v2Backbone.test.ts` — 84 passed.
- `cd explorer && bun test src/components/graph/VisNetworkHost.test.ts src/utils/labels.test.ts` — 37 passed.
- JSON validation for modified JSON fixtures, source-rights registry, enrichment report, shadow reports, and resolver QA report — passed.
- Safety/routing scan — KG enrichment route in `opencode.json` remains Kimi-only (`moonshot/kimi-k2.6`); no active Codex Spark KG enrichment routing found.
- `git diff --check` — passed.
- Kimi final read-only audit (`.omx/logs/architecture-interconnectivity-kimi-final-audit.txt`) — approved.
- `omx team status architecture-interconnectivity` — no team state found after shutdown.
- `omx cancel && omx status` — ralph, ultrawork, skill-active, and team inactive/cancelled after verified completion.

## Safety Confirmation
- Protected source payloads ingested: no.
- Reviewer text, exam questions, answer keys, protected tables, clauses, figures, diagrams ingested: no.
- Neo4j/live graph promotion: no.
- KG rebuild/reload/reset: no.
- Destructive graph operation: no.
- Codex Spark used for enrichment: no.
- Kimi used for advisory and final audit: yes, through `kimi-for-coding/k2p6` after the configured Moonshot Kimi credential path returned an API-key error.
