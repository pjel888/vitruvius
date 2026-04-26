---
task: aec-mepfs-shadow-graph-parity
phase: 05
created: 2026-04-26
author: CODEX
status: VALIDATED
supersedes: null
---

# Seventh Shadow Slice: BackboneNode Shadow Graph Parity

## Scope

Implement a file-backed shadow graph/parity layer over the already admitted
`BackboneNode` L1/L2 fixture.

This slice turns the staged BackboneNode rows and governed fixture
relationships into a deterministic sibling artifact,
`shadow-backbone-graph.json`, referenced by the existing shadow staging report
and consumer report. The graph is for read-only parity and preview only. It is
not a Neo4j graph, not the operational KG, and not the Explorer default graph.

## Research Baseline

- `current-phase.md` and `milestone-tracker.md` identify shadow graph
  construction/parity as the next bounded shadow slice.
- The prior sixth slice generated run `20260426T000726Z` with 7 admitted
  BackboneNodes and no live-write boundaries.
- Existing staging/report/API/Explorer preview functions are additive and have
  LOW GitNexus impact:
  `stage_shadow_backbone`, `build_shadow_staging_consumer_report`,
  `buildShadowBackboneTaxonomyPreview`, and `BackbonePreviewPanel`.
- `docs/shared/agent-tiers.md` requested by the Ralph skill is absent; AGENTS
  role catalog and native specialist tiers are used instead.

## Audit Findings

- The current staging artifact exposes BackboneNode rows but not a graph
  adjacency contract.
- Runtime graph roots remain too risky for this slice; no `CanonicalNode`,
  `TaxonomyLoader`, `Neo4jLoader`, or operational KG loader should be touched.
- Shadow graph parity must validate that all staged graph edges resolve inside
  the admitted node set, that the graph points back to the exact staging
  artifact, and that producer/consumer graph counts do not drift.
- The API/Explorer preview may show sanitized graph counts and adjacency, but
  must not inject the shadow graph into the Explorer's operational graph store.

## Implementation Plan

1. Extend shadow staging to write a sibling `shadow-backbone-graph.json`
   artifact only when a BackboneNode contract file is supplied.
2. Include sanitized graph nodes and edges:
   - nodes: `id`, `label`, `path_code`, `level`, `parent_path_code`
   - edges: deterministic id, `from_id`, `to_id`, `predicate`
3. Validate graph parity:
   - all edge endpoints resolve to admitted staged nodes
   - duplicate edge ids are rejected
   - every L2-L4 node has a `broader_than` edge from its declared parent node
4. Extend the read-only consumer report with `shadow_graph_path` and
   `shadow_graph_counts`, and fail closed on source-artifact, count, and edge
   endpoint mismatches.
5. Extend `/v2/backbone/taxonomy` to expose sanitized `shadowGraph` metadata
   when present.
6. Extend the opt-in Explorer preview to display graph counts and sample
   hierarchy edges without mutating graph state.
7. Add focused Python/API/Explorer tests, generate a new shadow run, update
   validation/state docs, then run full affected QA.

## Plan Critique

- [C001] A shadow graph can be mistaken for production graph admission. Docs,
  API readiness strings, and Explorer labels must keep saying shadow/preview.
- [C002] Relationship edges must come from fixture relationships and admitted
  parent paths, not from source-derived rules or protected content.
- [C003] The preview must not replace the existing graph store, perspective
  routing, or Neo4j-backed graph APIs.
- [C004] Do not build a generic graph engine. Keep this to the first admitted
  fixture and deterministic hierarchy parity.
- [C005] Do not embed the graph inside row staging data. A sibling derived
  graph artifact keeps row admission and adjacency projection separate.

## Execution Checklist

- [x] Create Ralph context snapshot.
- [x] Clear incompatible workflow state and activate Ralph.
- [x] Read current phase, milestone, prior packet, and validation evidence.
- [x] Run GitNexus status/query/impact evidence.
- [x] Implement shadow graph staging/report support.
- [x] Implement API/Explorer preview support.
- [x] Add focused tests.
- [x] Generate a new shadow run via command.
- [x] Run initial UltraQA verification.
- [x] Run architect verification.
- [x] Run changed-file deslop pass and re-verify.
- [x] Update validation/state docs.
- [ ] Commit, refresh GitNexus, push, and clear workflow state.

## Explicit Non-Goals

- No Neo4j write, read-load, dump/load, reset, or cleanup.
- No KG rebuild.
- No production registry admission.
- No protected content ingest.
- No Explorer default graph replacement.
- No runtime feature flag promotion.
