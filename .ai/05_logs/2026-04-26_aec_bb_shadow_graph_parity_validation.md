# AEC-BB Shadow Graph Parity Validation

**Date:** 2026-04-26
**Scope:** seventh AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added a sibling file-backed `shadow-backbone-graph.json` artifact for admitted
  `BackboneNode` rows and governed fixture relationships.
- Kept the graph shadow-only, file-backed, and disconnected from Neo4j,
  operational KG loading, feature flags, protected source ingest, and Explorer
  default graph state.
- Extended the shadow consumer report with `shadow_graph_path` and
  `shadow_graph_counts`.
- Tightened consumer behavior so only the graph path explicitly referenced by
  the producer report is read; stray sibling graph files are ignored.
- Extended `/v2/backbone/taxonomy` with sanitized shadow graph preview data and
  fail-closed validation for graph schema, run id, source artifact, counts, and
  edge endpoints.
- Extended the opt-in Explorer preview to display shadow graph counts and
  sample hierarchy edges without mutating graph state.

## Generated Evidence

Latest generated run:

`006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/`

Artifacts:

- `shadow-backbone-staging.json`
- `shadow-backbone-graph.json`
- `shadow-staging-report.json`
- `shadow-staging-consumer-report.json`

Graph counts:

- Nodes: 7
- Edges: 4
- Roots: 3
- Max depth: 2

Runtime boundaries remained false for live Neo4j writes, graph rebuild,
feature-flag cutover, API/Explorer cutover, canonical content admission, and
protected content ingest.

## Verification

- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`
  - Result: 70 passed.
- `cd api && bun test`
  - Result: 30 passed.
- `cd explorer && bun test`
  - Result: 39 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed.
  - Note: Vite emitted the existing chunk-size warning for the large
    `vis-network` chunk.

Architect verification:

- Result: APPROVED.
- Finding: no blocking issues; implementation remains file-backed,
  shadow-only, fail-closed, sanitized, and disconnected from Explorer default
  graph adoption.

Deslop cleanup:

- Scope: changed files only.
- Simplification: removed permissive fallback discovery of unreported sibling
  graph files in the consumer report reader.
- Regression: added a test that a stray graph file is ignored unless the
  producer report references it.

## Remaining Runtime Blocks

- No protected content ingest is authorized.
- No Neo4j write, reset, dump/load, or graph rebuild is authorized.
- No v1 API behavior or Explorer default graph behavior is changed.
- Runtime registry admission, source classification, and primary graph
  promotion still require separate packets and fresh impact review.
