---
task: concept-centric-relationship-enrichment
date: 2026-04-25
status: validated
---

# Concept-Centric Relationship Enrichment Validation

## Scope

MVP relationship-quality improvement over the existing
`001-Laws` KG snapshot only. No raw conversion, canonicalization, relationship
review, promotion, or `run-kg-pipeline` rebuild was run.

Input snapshot:

- `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`

Output snapshot:

- `005_Operational-Intelligence-Layer/graph/kg-v2/20260425T003423Z_kg_v2_unified_enriched.json`

## Implementation Evidence

- Added `scripts/vitruvius/kg/relationship_enricher.py`.
- Added `kg-enrich-relationships` CLI command.
- Added semantic edge vocabulary: `CONSTRAINS`, `AFFECTS`, `INFLUENCES`,
  `USED_IN`, `EXECUTED_IN`, `REGULATED_BY`.
- Updated Neo4j fast-edge loading so concept-to-DocumentVersion support
  assertions materialize instead of being skipped.
- Updated API perspectives:
  - `concepts`: concept-only nodes and semantic concept-to-concept edges
  - `evidence`: concept support edges to EvidenceSpan and DocumentVersion nodes
- Updated Explorer filters/colors for the new semantic edge types.

## Enrichment Result

CLI:

```bash
source /Users/philiplewis/vitruvius/.venv/bin/activate
PYTHONPATH=scripts python3 scripts/pipeline_cli.py kg-enrich-relationships \
  --snapshot 005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json \
  --max-new-assertions 220 \
  --load-neo4j \
  --clear-neo4j \
  --ensure-neo4j
```

Result:

- rule-evidence candidate pairs: 28
- source-reference candidate pairs: 270
- added assertions: 1701
- added source support assertions: 1481
- semantic assertions after enrichment: 224
- added by type:
  - `AFFECTS`: 60
  - `CONSTRAINS`: 66
  - `INFLUENCES`: 3
  - `REGULATED_BY`: 45
  - `RELATED_TO`: 31
  - `SUPPORTED_BY`: 1481
  - `USED_IN`: 15

## Quality Report

`build_kg_quality_report` on the enriched snapshot:

- document_versions: 181
- canonical_nodes: 313
- relationship_assertions: 2133
- fast_edges: 2435
- semantic_relationship_quality:
  - semantic_assertion_count: 224
  - semantic_edge_type_diversity: 7
- relationship_endpoint_quality:
  - missing_endpoint_count: 0
  - supported_by_total: 1695
  - supported_by_to_evidence: 1695
- rule_title_quality:
  - duplicate_display_labels: []
  - generic_display_labels: []
  - truncated_rule_label_ids: []
- warnings: []

## Neo4j Evidence

Neo4j was cleared and reloaded from the enriched snapshot only.

- nodes: 2429
- loader statements: 7665
- loader errors: 0
- concept-to-concept semantic relationship counts:
  - `CONSTRAINS`: 66
  - `AFFECTS`: 60
  - `REGULATED_BY`: 45
  - `RELATED_TO`: 32
  - `USED_IN`: 15
  - `INFLUENCES`: 3
  - `REQUIRES`: 3

SPP 205 check:

- `concept-standards-of-professional-practice`
  `SUPPORTED_BY` `docv-spp-205-v1`
- Document title: `SPP DOC. 205`
- assertion id:
  `assert-mvp-concept-standards-of-professional-practice-supported-by-docv-spp-205-v1`

## Tests

- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg_relationship_enricher.py scripts/tests/test_kg_quality_report.py scripts/tests/test_kg_neo4j_loader.py`
  - 34 passed
- `bun test api/perspectiveContracts.test.ts`
  - 15 passed
- `bun test explorer/src/components/componentInteraction.test.tsx explorer/src/components/graph/VisNetworkHost.test.ts explorer/src/app.searchInspector.integration.test.tsx`
  - 20 passed
- `cd explorer && bun run build`
  - passed

## Remaining Risk

This is an MVP overlay. The added deterministic assertions are
`review_required` / `pending`, not admitted canonical truth. The governed
taxonomy/backbone remains the proper long-term relationship substrate.
