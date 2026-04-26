# Strategic Next Move

## Single Best Next Move

**Choose the next shadow slice from fresh evidence, with priority on remaining route-backed `/v2` parity surfaces or manifest/report hardening before any runtime cutover.**

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
- The node preview route `GET /v2/backbone/node/:id` is now implemented as a
  file-backed shadow-only surface over the sibling shadow graph. It resolves by
  VTN ID, canonical ID, or path code, exposes immediate relationships with
  file-backed provenance, returns 400 for malformed escaped IDs, and fails
  closed if the shadow graph artifact is unavailable. Fresh parity evidence is
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json`
  with 22/22 cases passing.
- The search preview route `GET /v2/search` is now implemented as a file-backed
  shadow-only surface over staged BackboneNode labels, preferred labels, path
  codes, and authored aliases. It requires the shadow graph artifact, does not
  query Neo4j, and keeps Explorer default adoption unchanged. Fresh parity
  evidence is
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/api-explorer-parity-report.json`
  with 23/23 cases passing.
- The source metadata preview route `GET /v2/sources/:source_id` is now
  implemented as a file-backed shadow-only surface over the staged
  source-rights registry. It returns copyable source labels and governance
  status while omitting official URLs, blocking notes, intended-use prose, and
  protected source content. Fresh parity evidence is
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T052238Z/api-explorer-parity-report.json`
  with 24/24 cases passing.
- The resolver QA runner is now implemented as a file-backed shadow-only report
  over the S2 resolver golden cases. It validates 4/4 pilot cases across
  `single_value`, `composed`, `conflict`, and `none`, confirms `/v2/resolve`
  routes remain unmounted, and writes
  `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/resolver-qa-report.json`.
- API-side shadow report/manifest hardening is now implemented. The existing
  `/v2` preview readers require expected shadow filenames, fail closed with
  deterministic invalid-JSON diagnostics, and the fresh parity report
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T062032Z/api-explorer-parity-report.json`
  passes 6/6 commands and 24/24 cases.
- The file-backed boundary audit runner is now implemented. It consolidates the
  latest shadow consumer report, sibling graph artifact, placement QA report,
  resolver QA report, parity report, feature-flag state, and API route surface
  into
  `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T075100Z/shadow-boundary-audit-report.json`.
  The report passed 10/10 checks and confirms no Neo4j writes, no KG rebuild, no
  protected content ingest, no feature-flag cutover, no Explorer default
  adoption, no resolver route mounting, preview/read-only/shadow-only behavior,
  and auditable file-backed artifacts.
- The file-backed benchmark runner is now implemented. It measures five
  local-only shadow evidence operations across contract validation, JSON reads,
  graph-shape scan, API route static scan, and input-hash scan, then writes
  `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T080510Z/benchmark-report.json`.
  The report keeps runtime thresholds explicitly unevaluated and makes no
  resolver/API/Explorer/Neo4j latency claim.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, feature flags, graph rebuilds, or primary Explorer adoption.
- The highest-leverage move is therefore to inspect remaining file-backed
  evidence, report, and preview-readiness gaps before adding any new runtime
  surface, still without protected content ingest, Neo4j writes, graph rebuilds,
  or default Explorer adoption.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond file-backed shadow staging, read-only reporting, the first compact `/v2` summary route, and the opt-in Explorer preview
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Keep the shadow BackboneNode, sibling shadow graph, placement QA, resolver QA, API reader hardening, boundary audit, benchmark, and parity validation evidence current.
2. Write a separate packet for the next file-backed evidence hardening task or another read-only `/v2` preview surface before implementation.
3. Run fresh GitNexus impact/status on the exact files before touching them.
4. Keep protected content ingest, live graph reset/rebuild, primary-label promotion, v1 behavior changes, Explorer default adoption, and default-on feature flags blocked.
