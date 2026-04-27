# Strategic Next Move

> **2026-04-27 superseding update:** the default-off resolver route slice is complete through `6e91b96a`, and resolver fixture expansion is complete through `e90710ac`. The best next move is `2026-04-27_default_off_resolver_parity_packet.md`, a parity-governance update for exact default-off resolver routes, not broad `LIVE_RUNTIME_AUTHORIZED`.


## Single Best Next Move

**Hold the runtime boundary. The runtime-governance packet is boundary-approved only for the first bounded resolver-runtime contract/static-verification packet; live runtime remains blocked.**

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
- The shared static API route inventory runner is now implemented. It writes
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T082614Z/api-route-inventory-report.json`
  with 21 direct Hono routes inventoried, all six required `/v2` preview routes
  present, and `/v2/resolve` plus `/v2/resolve/trace` unmounted. Resolver QA,
  boundary audit, and benchmark checks now share that route-status parser.
- The consolidated shadow evidence manifest runner is now implemented. It
  writes
  `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T084131Z/shadow-evidence-manifest-report.json`
  over nine current shadow reports, records SHA-256 input hashes, checks
  producer/consumer/graph/benchmark path relationships, and keeps all safety
  invariants file-backed and read-only. The refreshed benchmark report
  `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T084118Z/benchmark-report.json`
  now points at the route-inventory-backed boundary audit.
- The compact evidence preview route `GET /v2/backbone/evidence` is now
  implemented as an API-only file-backed surface over the consolidated evidence
  manifest. Fresh evidence is staged at
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T090300Z/api-explorer-parity-report.json`,
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T090320Z/api-route-inventory-report.json`,
  `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T090340Z/shadow-boundary-audit-report.json`,
  `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T090400Z/benchmark-report.json`,
  and
  `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T090420Z/shadow-evidence-manifest-report.json`.
  It exposes only sanitized manifest metadata and does not change Explorer
  defaults, mount `/v2/resolve`, query/write Neo4j, rebuild KG artifacts, ingest
  protected content, or cut over feature flags.
- The consolidated evidence packet is now hardened against stale API inputs.
  The refreshed route inventory, boundary audit, benchmark, and evidence
  manifest under `20260426T093920Z` through `20260426T093924Z` record the
  current `api/index.ts` SHA-256 hash, and the manifest rejects route inventory,
  boundary audit, or benchmark reports whose recorded API hash drifts from the
  current API file.
- The Explorer now has an explicit-action evidence summary preview inside the
  existing non-default AEC-MEPFS panel. It fetches `/v2/backbone/evidence` only
  after `Load evidence summary`, keeps graph nodes/edges and selected
  perspective unchanged, and does not render raw evidence input hashes or
  protected source payloads. Fresh evidence is staged under `20260426T095439Z`
  through `20260426T100633Z`, with 26/26 parity cases, 10/10 boundary checks,
  5/5 benchmark operations, and 9/9 manifest artifacts ok.
- The API/Explorer parity and read-route contract docs now reflect the current
  implemented preview surface, including placement-QA and evidence routes plus
  explicit-action Explorer consumers. Resolver routes remain the only planned
  `/v2` routes and are still blocked.
- The evidence repo-state hardening slice is implemented. Route inventory,
  boundary audit, benchmark, and evidence manifest reports now split source
  dirtiness from generated-evidence dirtiness; `/v2/backbone/evidence` and the
  Explorer evidence preview render that distinction, render legacy freshness as
  `unknown`, and fail closed on refreshed source-dirty evidence.
- The refreshed clean-source evidence packet is staged under
  `20260426T105359Z` through `20260426T105418Z`. The final manifest passes with
  9/9 artifacts ok, 10/10 boundary checks, 5/5 benchmark operations, 7/7
  preview routes present, all safety invariants true, and source dirtiness false
  across the refreshed reports.
- The shared repo-state helper extraction is implemented. Route inventory,
  boundary audit, benchmark, and evidence manifest now consume
  `scripts/vitruvius/kg/backbone_repo_state.py` for identical source/generated
  dirtiness classification, with 163 focused backbone tests passing and no API,
  Explorer, Neo4j, KG rebuild, protected-ingest, or feature-flag behavior
  changed.
- The post-helper evidence refresh is staged under `20260426T112300Z` through
  `20260426T112330Z`. The final manifest passes with 9/9 artifacts ok, 10/10
  boundary checks, 5/5 benchmark operations, 7/7 preview routes present, all
  safety invariants true, and source dirtiness false across the refreshed
  reports.
- The parity fixture coverage gate is hardened. `search_invalid_query` is now
  required by `backbone_parity_runner.py`, and the fresh parity report at
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T113000Z/api-explorer-parity-report.json`
  passes 6/6 commands and 26/26 cases with that category recorded in
  `required_case_categories`.
- The post-parity evidence refresh is staged under `20260426T113810Z` through
  `20260426T113840Z`. The final manifest references the hardened parity report,
  passes with 9/9 artifacts ok, 10/10 boundary checks, 5/5 benchmark operations,
  7/7 preview routes present, all safety invariants true, and source dirtiness
  false across the refreshed reports.
- The resolver QA expansion is implemented. The fresh resolver QA report at
  `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T115200Z/resolver-qa-report.json`
  passes 4/4 cases with 12/12 required coverage keys true, including query
  asset context, jurisdiction/effective-date presence, source evidence
  traceability, composed compatibility rationale, conflict incompatibility
  rationale, and none/absence rationale. `/v2/resolve` and
  `/v2/resolve/trace` remain unmounted.
- The post-resolver QA evidence refresh is staged under `20260426T120320Z`
  through `20260426T120350Z`. The final manifest references the expanded
  resolver QA report and the hardened parity report, passes with 9/9 artifacts
  ok, 10/10 boundary checks, 5/5 benchmark operations, 7/7 preview routes
  present, all safety invariants true, and source dirtiness false across the
  refreshed reports.
- The placement QA expansion is implemented. The fresh placement QA report at
  `006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T122042Z/placement-qa-report.json`
  passes 3/3 cases with 11/11 required coverage keys true, including case ID,
  input context, owner/review status, proposal level, non-empty
  source-evidence IDs, LD-8 auto-accept rationale, and legacy alias rationale.
- The post-placement QA evidence refresh is staged under `20260426T122729Z`
  through `20260426T122733Z`. The final manifest references the expanded
  placement QA report, expanded resolver QA report, and hardened parity report,
  passes with 9/9 artifacts ok, 10/10 boundary checks, 5/5 benchmark operations,
  7/7 preview routes present, all safety invariants true, and source dirtiness
  false across the refreshed reports.
- Resolver-route parity hygiene is implemented. The contract now rejects v2
  parity cases using `/v2/resolve` or `/v2/resolve/trace*`, the S2 fixture uses
  implemented `/v2/backbone/evidence` coverage instead of a planned resolver
  route, and the fresh parity report at
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T124014Z/api-explorer-parity-report.json`
  passes 6/6 commands and 26/26 cases.
- The post-resolver-route parity evidence refresh is staged under
  `20260426T124656Z` through `20260426T124700Z`. The final manifest references
  the resolver-route-hardened parity report, expanded placement QA report, and
  expanded resolver QA report, passes with 9/9 artifacts ok, 10/10 boundary
  checks, 5/5 benchmark operations, 7/7 preview routes present, all safety
  invariants true, and source dirtiness false across the refreshed reports.
- Benchmark evidence hardening is implemented. The benchmark report now records
  required file-backed operation coverage and explicit runtime-threshold
  non-evaluation evidence, while the evidence manifest fails closed if required
  operations drift, operation pass counts disagree, blocked runtime scope is
  omitted, or runtime thresholds appear evaluated.
- The post-benchmark-hardening evidence refresh is staged under
  `20260426T132000Z` through `20260426T132003Z`. The final manifest references
  the hardened benchmark report, passes with 9/9 artifacts ok, 10/10 boundary
  checks, 5/5 benchmark operations, 7/7 preview routes present, benchmark
  required-operation coverage present, 4 declared thresholds recorded, all
  safety invariants true, and source dirtiness false across the refreshed
  reports.
- The post-`c442d047` remaining-work scan found no repo-backed concrete
  candidate slice inside the current safe shadow-only/read-only scope. The
  remaining known work is blocked runtime/governance work, not another safe
  preview/report slice.
- `AEC-BB-S1` through `AEC-BB-S8` are the safe foothold: file-backed validators, fixtures, parity reports, rollback metadata, Neo4j admin preflight, live read-only graph smoke, registry/source-admission candidate rows, source-currentness evidence, admission decision records, runtime-root impact evidence, human inbox packet, manual currentness resolution, and isolated rollback proof now check readiness without touching KG schemas, Neo4j write paths, feature flags, graph rebuilds, or primary Explorer adoption.
- The highest-leverage move is therefore to preserve the runtime boundary and
  complete `2026-04-27_default_off_resolver_parity_packet.md` only for
  default-off resolver route parity coverage. Unguarded/default-on `/v2/resolve*`
  behavior, Neo4j, KG rebuild, protected ingest, benchmark-threshold claims,
  default-on flags, and Explorer-default surfaces remain blocked.

## What Should Be Deferred

- Broad new feature expansion
- Generic dataset expansion beyond the bounded laws-wave maintenance state
- Large archive migrations that could break references before the active surface is fully stable
- AEC runtime cutover beyond file-backed shadow staging, read-only reporting, the first compact `/v2` summary route, and the opt-in Explorer preview
- Neo4j cleanup/reset, feature-flag cutover, graph rebuild, or backup/restore test runs under the readiness plan

## Concrete Tasks

1. Use `AEC-MEPFS-Backbone/2026-04-27_default_off_resolver_parity_packet.md` as the next bounded implementation authority for default-off resolver route parity coverage only.
2. Keep protected content ingest, live graph reset/rebuild, KG rebuild/reload, primary-label promotion, v1 behavior changes, Explorer default adoption, unguarded/default-on `/v2/resolve*` behavior, runtime threshold adoption, and default-on feature flags blocked.
3. Treat `/.ai/09_archive/research/chatgpt-conversations/` as the transcript archive and keep `/.ai/chatGPT-Conversations/README.md` as a forwarding pointer only.
4. Keep `/.ai/skills/gitnexus/` canonical; duplicate `.ai/11_skills` skill docs are archived, while imported skill/agent packs remain optional reference/adoption cleanup.
