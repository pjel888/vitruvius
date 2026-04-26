# Strategic Next Move

## Single Best Next Move

**Choose the next shadow slice from fresh evidence, with priority on file-backed report-reader hardening or UI test-hygiene cleanup before any runtime cutover.**

## Why This Is Right Now

- The control-surface cleanup is complete enough that the next major decision can be made from a truthful live planning layer.
- The AEC-MEPFS Backbone packet reframes the work correctly: author the standards-aligned backbone first, then classify documents and evidence into it.
- The first additive shadow-only implementation slice is implemented as a file-backed staging artifact, while primary runtime cutover remains blocked.
- The second bounded read-only consumer/reporting slice is implemented and validates the existing staging artifact without touching Neo4j, Explorer, feature flags, graph rebuilds, or protected source content.
- The first additive `/v2` shadow read route, `GET /v2/backbone`, is implemented as a compact file-backed summary route and does not change v1 behavior or Explorer defaults.
- The non-default Explorer preview is implemented as an opt-in rail panel that reads `/v2/backbone` without replacing the graph, changing perspectives, mutating Neo4j, or enabling runtime cutover.
- The bounded `GET /v2/backbone/taxonomy` detail route is implemented as a sanitized registry-readiness preview over the shadow staging artifact.
- The first admitted `BackboneNode` L1/L2 fixture/model slice is implemented and staged, and the latest generated run `20260426T003710Z` includes a sibling shadow graph artifact with 7 nodes, 4 governed hierarchy edges, 3 roots, and max depth 2.
- The opt-in Explorer preview can show those file-backed shadow nodes and shadow graph counts/edges without routing them into Neo4j or the default graph.
- The API/Explorer parity runner is now hardened after the shadow graph slice:
  it requires 20 parity cases and 6 allowlisted commands, with fresh passing
  report `006_System-Manifests/aec-mepfs-backbone/parity/20260426T014754Z/api-explorer-parity-report.json`.
- The file-backed placement/authoring QA runner is implemented and generated
  `006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`
  with 3/3 pilot cases passing for LD-8 auto-accept, L1/L2 human review, and
  legacy-label alias handling.
- The placement QA report now has an additive read-only
  `GET /v2/backbone/placement-qa` summary route. The parity runner requires
  this route through `shadow_backbone_placement_qa_preview`, with fresh passing
  report
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T024015Z/api-explorer-parity-report.json`
  covering 21/21 cases.
- Explorer now renders placement QA inside the existing non-default AEC-MEPFS
  preview only after the explicit `Load placement QA summary` action. The
  parity runner now requires `shadow_placement_qa_preview_opt_in_isolation`,
  with fresh passing report
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T031555Z/api-explorer-parity-report.json`
  covering 22/22 cases.
- The parity-relevant Explorer component test now wraps asynchronous
  copy-button clicks with `act(...)`, and the clean regenerated parity report is
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T032507Z/api-explorer-parity-report.json`
  with 22/22 cases passing.
- The shadow report reader now fails closed on malformed graph-path metadata,
  reports invalid JSON with deterministic path/line/column context, and writes
  consumer reports atomically. Fresh parity evidence is
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T034724Z/api-explorer-parity-report.json`
  with 22/22 cases passing.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, feature flags, graph rebuilds, or primary Explorer adoption.
- The highest-leverage move is therefore to keep advancing file-backed semantics around the admitted fixture and cleaning evidence/test quality, still without protected content ingest, Neo4j writes, graph rebuilds, or default Explorer adoption.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond file-backed shadow staging, read-only reporting, the first compact `/v2` summary route, and the opt-in Explorer preview
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Keep the shadow BackboneNode and sibling shadow graph validation evidence current.
2. Write a separate packet for the next file-backed QA/evidence hardening task or another read-only `/v2` preview surface before implementation.
3. Run fresh GitNexus impact/status on the exact files before touching them.
4. Keep protected content ingest, live graph reset/rebuild, primary-label promotion, v1 behavior changes, Explorer default adoption, and default-on feature flags blocked.
