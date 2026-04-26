# AEC-MEPFS Backbone Plan Packet

## Purpose

This folder contains the planning packet for the proposed AEC-MEPFS Backbone
knowledge graph architecture shift.

`AEC-MEPFS` names the broader AEC scope while keeping mechanical, electrical,
plumbing, fire protection, and sanitary systems explicit as first-class domains.

The direction captured here is planning-only: build an authored,
standards-aligned AEC-MEPFS Backbone graph first, then classify documents, rules,
chunks, and evidence onto that backbone.

## Files

| File | Role |
|---|---|
| `2026-04-25_aec_mepfs_backbone_knowledge_graph_research.md` | Standards and repo-context research |
| `2026-04-25_aec_mepfs_research_integration_addendum.md` | Integration of the AECMEPFS++ research reports into readiness gates |
| `2026-04-25_aec_mepfs_backbone_architecture_audit.md` | Current-state audit and blast-radius assessment |
| `2026-04-25_aec_mepfs_backbone_readiness_plan.md` | Go/no-go readiness gates before implementation |
| `2026-04-25_aec_mepfs_backbone_architecture_overhaul_plan.md` | Proposed architecture overhaul plan |
| `2026-04-25_aec_mepfs_backbone_cleanup_and_blast_radius_plan.md` | Cleanup, database migration, and blast-radius plan |
| `2026-04-25_aec_mepfs_backbone_plan_validation.md` | Planning-artifact validation note |
| `standards-legal-source-pack.md` | Source families, rights classes, and official-source verification controls |
| `master-taxonomy-l1-l2-decision-record.md` | First-slice L1/L2 taxonomy decision and canonical rules |
| `governance-editorial-control-pack.md` | Stewardship, review, change-control, AI-use, and release controls |
| `vitruvian-context-resolver-pack.md` | Deterministic resolver contract and no-LLM hot-path rules |
| `taxonomy-authoring-migration-qa-pack.md` | Authoring, staging, review queues, confidence policy, and golden dataset design |
| `philippines-overlay-pilot-pack.md` | Philippines jurisdiction overlay pilot and source/fallback rules |
| `relationship-predicate-registry-draft.md` | Readiness-stage predicate vocabulary and vague-edge rejection gate |
| `readiness-artifact-history-and-blast-radius-audit.md` | Historical KG failure evidence and blast-radius implications for the readiness packet |
| `code-intelligence-impact-map.md` | Fresh GitNexus CLI impact map and HIGH/CRITICAL risk evidence |
| `sel-mcp-precheck.md` | Tool-availability, MCP transport, and CLI parity precheck |
| `shadow-graph-database-safety-protocol.md` | Shadow graph topology, backup/restore prerequisites, and destructive-operation block |
| `api-explorer-parity-contract.md` | V1 preservation, `/v2` shadow route, and Explorer parity contract |
| `verification-and-benchmark-contract.md` | Later verification commands, thresholds, and output report requirements |
| `readiness-spec-acceptance-record.md` | Promotion record for accepted readiness-control specs and remaining implementation blockers |
| `first-bounded-implementation-packet.md` | Separate non-executed packet for the first safe code slice |
| `second-bounded-readiness-implementation-packet.md` | Implemented fixture-level readiness validator extension for S2 |
| `third-bounded-readiness-implementation-packet.md` | Implemented S3 readiness-gate validator extension for registry locations, parity, rollback, benchmark, and runtime-blocking gates |
| `fourth-bounded-readiness-implementation-packet.md` | Implemented S4 report-producing API/Explorer parity runner |
| `fifth-bounded-readiness-implementation-packet.md` | Implemented S5 rollback preflight reporter |
| `sixth-bounded-readiness-implementation-packet.md` | Implemented S6 registry/source-admission candidate preparation |
| `seventh-bounded-readiness-implementation-packet.md` | Implemented S7 source-currentness, admission, rollback, and runtime-root readiness evidence |
| `eighth-readiness-runtime-priming-packet.md` | Implemented S8 human-inbox, currentness-resolution, and isolated rollback-proof priming |
| `source-currentness-evidence-pack.md` | Official URL/currentness evidence and manual-review exceptions for S6 source rows |
| `legal-and-steward-admission-record.md` | Human/steward/legal decision ledger; prepared but not signed |
| `canonical-source-admission-packet.md` | Canonical source admission packet with zero sources admitted |
| `neo4j-rollback-rehearsal-evidence.md` | Stopped/isolated dump/load proof requirements and safe rehearsal disposition |
| `runtime-root-implementation-packet.md` | Separate packet for HIGH/CRITICAL KG runtime roots |
| `registry-candidates/` | Candidate predicate, source-rights, and source-admission review artifacts; not runtime registries |
| `readiness-closure-scorecard.md` | Current go/no-go scorecard after S1/S2/S3/S4/S5/S6/S7/S8 |
| `first-shadow-only-implementation-packet.md` | Implemented first additive shadow-only implementation packet |
| `second-shadow-readonly-consumer-reporting-packet.md` | Implemented bounded read-only consumer/reporting packet over the shadow staging artifact |
| `shadow-v2-api-read-route-planning-packet.md` | First route now implemented by a separate packet; remaining `/v2` routes stay planned |
| `third-shadow-v2-backbone-route-implementation-packet.md` | Implemented first additive `GET /v2/backbone` shadow read route |
| `fourth-shadow-explorer-preview-implementation-packet.md` | Implemented non-default Explorer preview for the shadow summary route |
| `fifth-shadow-taxonomy-preview-implementation-packet.md` | Implemented bounded `GET /v2/backbone/taxonomy` registry-readiness preview |
| `sixth-shadow-backbone-node-fixture-implementation-packet.md` | Implemented first admitted `BackboneNode` L1/L2 fixture, strict validator checks, shadow staging support, and opt-in preview exposure |
| `seventh-shadow-graph-parity-implementation-packet.md` | Implemented first sibling shadow graph artifact, consumer parity checks, `/v2/backbone/taxonomy` graph preview, and opt-in Explorer graph counts |
| `eighth-shadow-parity-runner-hardening-implementation-packet.md` | Implemented parity-runner hardening so the shadow graph, `/v2/backbone`, `/v2/backbone/taxonomy`, and opt-in Explorer preview are mandatory parity evidence |
| `ninth-shadow-placement-qa-implementation-packet.md` | Implemented file-backed placement/authoring QA report over the S2 readiness fixture |
| `tenth-shadow-placement-qa-v2-route-implementation-packet.md` | Implemented additive `GET /v2/backbone/placement-qa` summary route and parity case |
| `eleventh-shadow-placement-qa-explorer-preview-implementation-packet.md` | Implemented opt-in Explorer placement QA preview rendering and parity isolation case |
| `twelfth-shadow-explorer-test-hygiene-packet.md` | Removed parity-relevant React `act(...)` warnings from Explorer component tests |
| `thirteenth-shadow-report-reader-hardening-packet.md` | Hardened the file-backed shadow report reader for invalid JSON diagnostics, malformed graph-path rejection, and atomic writes |
| `fourteenth-shadow-node-preview-route-implementation-packet.md` | Implemented additive `GET /v2/backbone/node/:id` node preview route over the file-backed shadow graph |
| `fifteenth-shadow-search-preview-route-implementation-packet.md` | Implemented additive `GET /v2/search` search preview route over staged BackboneNode labels, path codes, and aliases |
| `sixteenth-shadow-source-preview-route-implementation-packet.md` | Implemented additive `GET /v2/sources/:source_id` source metadata preview route over the staged source-rights registry |
| `seventeenth-shadow-resolver-qa-implementation-packet.md` | Implemented file-backed resolver golden-case QA report over the S2 readiness fixture |
| `eighteenth-shadow-api-report-manifest-hardening-packet.md` | Hardened existing API shadow report/artifact readers with filename fencing and deterministic invalid-JSON diagnostics |
| `nineteenth-shadow-boundary-audit-implementation-packet.md` | Implemented consolidated file-backed safety-boundary audit over current shadow evidence |
| `twentieth-shadow-benchmark-implementation-packet.md` | Implemented file-backed benchmark runner over existing shadow evidence with explicit runtime-threshold non-evaluation |
| `twenty-first-shadow-api-route-inventory-hardening-packet.md` | Implemented shared static API route inventory for shadow resolver/boundary/benchmark route checks |
| `twenty-second-shadow-evidence-manifest-packet.md` | Implemented consolidated hash-backed shadow evidence manifest across the current report packet |
| `twenty-third-shadow-evidence-preview-route-packet.md` | Implemented additive `GET /v2/backbone/evidence` compact preview route over the consolidated shadow evidence manifest |
| `twenty-fourth-shadow-evidence-hash-consistency-packet.md` | Hardened the consolidated shadow evidence manifest so route inventory, boundary audit, and benchmark reports must match the current API hash |
| `twenty-fifth-shadow-evidence-explorer-preview-packet.md` | Implemented explicit-action Explorer evidence summary preview over the existing sanitized `/v2/backbone/evidence` route |
| `twenty-sixth-shadow-contract-reconciliation-packet.md` | Reconciled API/Explorer parity and read-route contract docs with the implemented shadow preview surface |
| `twenty-seventh-shadow-evidence-repo-state-hardening-packet.md` | Hardened shadow evidence repo-state reporting so source dirtiness and generated-evidence dirtiness are distinct |
| `twenty-eighth-shadow-evidence-refresh-packet.md` | Regenerated the route inventory, boundary audit, benchmark, and evidence manifest from the hardened clean source tree |
| `twenty-ninth-shadow-repo-state-helper-packet.md` | Extracted shared repo-state freshness helper for route inventory, boundary audit, benchmark, and evidence manifest reports |
| `thirtieth-shadow-evidence-refresh-packet.md` | Regenerated route inventory, boundary audit, benchmark, and evidence manifest after the shared repo-state helper extraction |
| `thirty-first-shadow-parity-fixture-hardening-packet.md` | Required invalid `/v2/search` parity coverage and regenerated the file-backed parity report |
| `thirty-second-shadow-evidence-refresh-packet.md` | Regenerated downstream evidence after parity fixture hardening using the new parity report |
| `thirty-third-shadow-resolver-qa-expansion-packet.md` | Expanded file-backed resolver QA checks for query context, source evidence traceability, and rationale semantics |
| `thirty-fourth-shadow-evidence-refresh-packet.md` | Regenerated downstream evidence after resolver QA expansion using the new resolver QA report |
| `first-slice-backbone-model-spec.md` | Accepted shadow-only model spec for admitted BackboneNode fields and parent/path invariants |

## Current Status

Status: first additive shadow-only implementation completed; second bounded
read-only consumer/reporting slice implemented and validated; first additive
`GET /v2/backbone` shadow read route implemented and validated; non-default
Explorer preview implemented; bounded `GET /v2/backbone/taxonomy`
registry-readiness preview implemented and validated; first admitted
`BackboneNode` L1/L2 fixture staged and exposed in the same opt-in preview; the
first sibling shadow graph/parity artifact is staged and exposed as preview-only
metadata. The eighth shadow slice hardens the API/Explorer parity runner so the
existing shadow graph artifact, compact `/v2/backbone` summary route, bounded
`/v2/backbone/taxonomy` graph preview route, and opt-in Explorer preview
isolation are required parity cases.

The ninth shadow slice adds a file-backed placement/authoring QA runner at
`scripts/vitruvius/kg/backbone_placement_qa.py`. It produces
`006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`
with 3/3 pilot QA cases passing across LD-8 auto-accept, L1/L2 human-review,
and legacy-label alias coverage. It does not call the runtime `PlacementEngine`
or expose a runtime/Explorer consumer.

The tenth shadow slice adds `GET /v2/backbone/placement-qa` as a compact
read-only summary over that placement QA report. The parity runner now requires
21 cases, including `shadow_backbone_placement_qa_preview`, with fresh passing
report
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T024015Z/api-explorer-parity-report.json`.
The route does not expose per-case payloads or change Explorer defaults.

The eleventh shadow slice adds an opt-in Explorer placement QA subsection inside
the existing AEC-MEPFS preview. It fetches `/v2/backbone/placement-qa` only
after the user explicitly loads the placement QA summary, resets that detail
state on summary refresh, and does not replace graph state, selected
perspective, nodes, or edges. The parity runner now requires 22 cases,
including `shadow_placement_qa_preview_opt_in_isolation`, with fresh passing
report
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T031555Z/api-explorer-parity-report.json`.

The twelfth shadow slice is a test-hygiene cleanup for the Explorer component
test path used by the parity runner. It wraps asynchronous copy-button clicks in
`act(...)`, changes no runtime behavior, and regenerates clean parity evidence
at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T032507Z/api-explorer-parity-report.json`.

The thirteenth shadow slice hardens the file-backed shadow report reader. It
adds deterministic invalid-JSON diagnostics, rejects malformed non-string
`producer_report.shadow_graph_path` values, writes consumer reports through a
same-directory temporary file followed by replace, and adds focused regression
tests for the happy and failure paths. It changes no API, Explorer, Neo4j, KG
loader, feature-flag, or source-ingest behavior. Fresh parity evidence is at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T034724Z/api-explorer-parity-report.json`.

The fourteenth shadow slice adds `GET /v2/backbone/node/:id` as an additive
file-backed node preview route. It resolves staged BackboneNode records by VTN
ID, canonical ID, or path code, returns sanitized node fields plus immediate
relationships from `shadow-backbone-graph.json`, and fails closed if the graph
artifact is unavailable. Fresh parity evidence is at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json`.

The fifteenth shadow slice adds `GET /v2/search` as an additive file-backed
search preview route over staged BackboneNode labels, preferred labels, path
codes, and authored aliases. It does not query Neo4j, does not expose protected
source payloads, and requires the sibling shadow graph artifact before returning
results. Fresh parity evidence is at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/api-explorer-parity-report.json`.

The sixteenth shadow slice adds `GET /v2/sources/:source_id` as an additive
file-backed source metadata preview route over the staged source-rights
registry. It returns copyable source labels and governance status fields while
omitting official URLs, blocking notes, intended-use prose, and protected source
content. Fresh parity evidence is at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T052238Z/api-explorer-parity-report.json`.

The seventeenth shadow slice adds a file-backed resolver QA runner at
`scripts/vitruvius/kg/backbone_resolver_qa.py`. It validates the four S2
resolver golden-case result types and confidence classes, writes
`006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/resolver-qa-report.json`,
and fails if `/v2/resolve` routes are mounted. It does not call the runtime
resolver, expose an API route, alter Explorer, write Neo4j, rebuild the KG, or
ingest protected content.

The eighteenth shadow slice hardens the existing API shadow report and artifact
readers. `api/index.ts` now fences expected shadow filenames and emits
deterministic invalid-JSON diagnostics for consumer, staging, graph, and
placement QA report reads. Fresh parity evidence is at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T062032Z/api-explorer-parity-report.json`.

The nineteenth shadow slice adds a file-backed boundary audit runner at
`scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`. It reads the latest
shadow consumer report, sibling shadow graph, placement QA report, resolver QA
report, parity report, feature flags, and API route surface, then writes
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T075100Z/shadow-boundary-audit-report.json`.
The report passes 10/10 checks and confirms the current shadow lane has no Neo4j
writes, KG rebuild, protected content ingest, feature-flag cutover, Explorer
default adoption, or `/v2/resolve` route mounting.

The twentieth shadow slice adds a file-backed benchmark runner at
`scripts/vitruvius/kg/backbone_shadow_benchmark.py`. It measures five local
shadow evidence operations over the S3 fixture and current evidence files, then
writes
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T080510Z/benchmark-report.json`.
The report includes p50/p95 timings, input hashes, repo-state metadata, and an
explicit `runtime_thresholds_evaluated: false` disposition. It does not run
runtime resolver paths, call API/Explorer servers, query Neo4j, rebuild the KG,
ingest protected content, alter feature flags, or adopt the Explorer default
graph.

The twenty-first shadow slice adds a shared static API route inventory runner at
`scripts/vitruvius/kg/backbone_api_route_inventory.py`. It inventories direct
Hono `app.<method>(...)` declarations in `api/index.ts`, ignores route-like
strings/comments, and writes
`006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T082614Z/api-route-inventory-report.json`.
Resolver QA, boundary audit, and benchmark checks now consume the same
route-status helpers. Fresh route-inventory-backed boundary and benchmark
evidence is staged at
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T082628Z/shadow-boundary-audit-report.json`
and
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T082629Z/benchmark-report.json`.
This remains static file-backed evidence only and adds no route or runtime
consumer.

The twenty-second shadow slice adds a consolidated evidence manifest runner at
`scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`. It verifies the
producer, consumer, graph, parity, placement QA, resolver QA, boundary audit,
benchmark, and API route-inventory reports; records SHA-256 input hashes; and
writes
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T084131Z/shadow-evidence-manifest-report.json`.
The benchmark default now points at the route-inventory-backed boundary audit,
with refreshed benchmark evidence at
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T084118Z/benchmark-report.json`.
This remains file-backed manifest evidence only and adds no API route, runtime
consumer, graph promotion, or Explorer default adoption.

The twenty-third shadow slice adds `GET /v2/backbone/evidence` as an additive
read-only preview route over the consolidated evidence manifest. It returns only
sanitized manifest metadata and file labels/paths, fails closed on stale or
unsafe evidence, and does not expose full report payloads or input hashes. The
fresh evidence packet is:
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T090300Z/api-explorer-parity-report.json`,
`006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T090320Z/api-route-inventory-report.json`,
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T090340Z/shadow-boundary-audit-report.json`,
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T090400Z/benchmark-report.json`,
and
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T090420Z/shadow-evidence-manifest-report.json`.
This remains API preview evidence only and adds no Explorer default adoption,
runtime resolver mounting, Neo4j write/query path, KG rebuild, protected content
ingest, feature flag cutover, or graph promotion.

The twenty-fourth shadow slice hardens the evidence packet against stale API
inputs. The evidence manifest now records `api/index.ts` as an input and fails
closed unless the route-inventory, boundary-audit, and benchmark reports all
record the current API SHA-256 hash. The refreshed packet is:
`006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T093920Z/api-route-inventory-report.json`,
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T093921Z/api-explorer-parity-report.json`,
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T093922Z/shadow-boundary-audit-report.json`,
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T093923Z/benchmark-report.json`,
and
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T093924Z/shadow-evidence-manifest-report.json`.
The API evidence route resolves the latest fenced evidence-manifest report by
default instead of carrying a stale hardcoded run id. This remains file-backed
preview evidence only and adds no Explorer default adoption, Neo4j query/write
path, KG rebuild, protected content ingest, feature flag cutover, runtime
resolver mounting, or graph promotion.

The twenty-fifth shadow slice adds an explicit-action Explorer evidence summary
inside the existing non-default AEC-MEPFS Backbone preview. The Explorer now
fetches `/v2/backbone/evidence` only when the user selects
`Load evidence summary`; the preview resets on summary refresh, renders compact
manifest health and safety fields, and does not expose raw input hashes or
source report payloads. Fresh evidence is:
`006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T095439Z/api-route-inventory-report.json`,
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T095440Z/api-explorer-parity-report.json`,
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T100631Z/shadow-boundary-audit-report.json`,
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T100632Z/benchmark-report.json`,
and
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T100633Z/shadow-evidence-manifest-report.json`.
The parity report now passes 26/26 cases and includes
`shadow_evidence_preview_opt_in_isolation`. This remains preview-only and adds
no Explorer default adoption, Neo4j query/write path, KG rebuild, protected
content ingest, feature-flag cutover, runtime resolver mounting, or graph
promotion.

The twenty-sixth shadow slice reconciles contract documentation after the
Explorer evidence preview. `api-explorer-parity-contract.md`,
`shadow-v2-api-read-route-planning-packet.md`, `api/README.md`, and
`explorer/README.md` now describe the current summary, taxonomy, node, search,
source, placement-QA, evidence, and Explorer preview surfaces as implemented
shadow-only/read-only previews, with only resolver routes remaining blocked.
This changes no runtime code and authorizes no Explorer default adoption,
Neo4j query/write path, KG rebuild, protected content ingest, feature-flag
cutover, runtime resolver mounting, or graph promotion.

The twenty-seventh shadow slice hardens repository-state freshness reporting
for the file-backed evidence packet. Route inventory, boundary audit, benchmark,
and evidence manifest reports now split aggregate `working_tree_dirty` into
source-tree dirtiness and generated-evidence dirtiness with path counts. The
sanitized `/v2/backbone/evidence` preview and explicit-action Explorer evidence
summary expose that distinction, render legacy manifests as `unknown` instead
of clean, and fail closed when a refreshed manifest explicitly reports source
tree dirtiness. The next safe slice is to regenerate the evidence packet after
this source hardening is committed and clean.

The twenty-eighth shadow slice regenerates the evidence packet from clean
source commit `1ad1332c`. Fresh evidence is:
`006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T105359Z/api-route-inventory-report.json`,
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T105405Z/shadow-boundary-audit-report.json`,
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T105410Z/benchmark-report.json`,
and
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T105418Z/shadow-evidence-manifest-report.json`.
The final manifest passes with 9/9 artifacts ok, 10/10 boundary checks, 5/5
benchmark operations, 7/7 preview routes present, and source dirtiness false in
every refreshed report. Later generated-evidence dirty counts are expected
because the reports are generated sequentially into the tracked evidence
directory.

Current implementation status: the first file-backed shadow staging slice is
implemented by `scripts/vitruvius/kg/backbone_shadow_staging.py`; broad runtime
architecture work remains blocked.

The second bounded slice adds a file-backed report reader at
`scripts/vitruvius/kg/backbone_shadow_report_reader.py`. It reads the existing
shadow staging artifact and producer report, validates read-only/no-ingest
boundaries, and writes
`006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-staging-consumer-report.json`.
It does not route API or Explorer consumers to Backbone data.

The third bounded slice adds `GET /v2/backbone` in `api/index.ts`. It reads only
the shadow consumer report and returns a compact summary. Explorer adoption,
remaining `/v2` routes, Neo4j writes, graph rebuild/reset, feature flags, and
protected source ingest remain blocked.

The fifth bounded slice adds `GET /v2/backbone/taxonomy` as a sanitized
registry-readiness detail route over the shadow staging artifact. The sixth
shadow slice extends that route with the first staged admitted `BackboneNode`
L1/L2 fixture when the artifact contains it. It does not expose standards text,
source examples, official URLs, or blocking notes. The Explorer consumes it only
after the user opens the existing AEC-MEPFS preview and then explicitly loads
readiness details.

The sixth shadow slice adds strict admitted `BackboneNode` validation and the
generated shadow run
`006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T000726Z/`.
The fixture has 7 authored L1/L2 `BackboneNode` records and remains
file-backed, shadow-only, and disconnected from Neo4j/runtime graph loading.

The seventh shadow slice adds a sibling `shadow-backbone-graph.json` artifact
for the same admitted fixture shape. The latest generated run is
`006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/`,
with 7 graph nodes, 4 governed hierarchy edges, 3 roots, and max depth 2. The
consumer report and `/v2/backbone/taxonomy` route fail closed if graph schema,
run id, source artifact, counts, or edge endpoints drift. The Explorer still
uses the graph only inside the opt-in AEC-MEPFS preview and does not mutate the
active graph state.

The eighth shadow slice updates the S4 parity runner from 14 to 20 required
parity cases and from 3 to 6 allowlisted commands. The fresh report at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T014754Z/api-explorer-parity-report.json`
passes 6/6 commands and 20/20 cases. This remains evidence-only; it does not
add routes, change Explorer defaults, write Neo4j, rebuild the KG, or ingest
protected content.

The twenty-ninth shadow slice extracts shared repo-state freshness logic into
`scripts/vitruvius/kg/backbone_repo_state.py` and updates route inventory,
boundary audit, benchmark, and evidence manifest reports to consume it. This
removes duplicated source/generated dirtiness parsing without changing API
routes, Explorer, Neo4j, KG rebuild behavior, feature flags, or evidence
schemas.

The thirtieth shadow slice regenerates the route inventory, boundary audit,
benchmark, and evidence manifest after the shared helper extraction. The final
manifest at
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T112330Z/shadow-evidence-manifest-report.json`
passes 9/9 artifacts, 10/10 boundary checks, 5/5 benchmark operations, and 7/7
preview routes with source dirtiness false throughout the refreshed packet.

The thirty-first shadow slice hardens the parity runner so the existing
`search_invalid_query` case is a required coverage category. The fresh parity
report at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T113000Z/api-explorer-parity-report.json`
passes 6/6 commands and 26/26 cases and records `search_invalid_query` in
`required_case_categories`.

The thirty-second shadow slice regenerates downstream route inventory, boundary
audit, benchmark, and evidence manifest reports after parity hardening. The
final manifest at
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T113840Z/shadow-evidence-manifest-report.json`
references the hardened parity report and passes 9/9 artifacts, 10/10 boundary
checks, 5/5 benchmark operations, and 7/7 preview routes with source dirtiness
false throughout the refreshed packet.

The thirty-third shadow slice expands the file-backed resolver QA runner. It
requires query asset context, jurisdiction, effective date, traceable source
evidence IDs, and rationale-specific coverage for composed, conflict, and none
outcomes. The fresh resolver QA report at
`006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T115200Z/resolver-qa-report.json`
passes 4/4 cases with 12/12 required coverage keys true and confirms
`/v2/resolve` plus `/v2/resolve/trace` remain unmounted. Downstream boundary,
benchmark, and manifest reports should be refreshed from a clean source commit
before treating this resolver report as the current consolidated evidence input.

The thirty-fourth shadow slice regenerates downstream route inventory, boundary
audit, benchmark, and evidence manifest reports after the resolver QA expansion.
The final manifest at
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T120350Z/shadow-evidence-manifest-report.json`
references the expanded resolver QA report and the hardened parity report, then
passes 9/9 artifacts, 10/10 boundary checks, 5/5 benchmark operations, and 7/7
preview routes with source dirtiness false throughout the refreshed packet.

No primary runtime integration or Explorer adoption has started from this
packet. It authorizes no Neo4j cleanup/reset, feature-flag changes, graph
rebuilds, backup test runs, or derived-artifact cleanup.

Readiness-control artifacts for source rights, L1/L2, governance, resolver,
shadow graph safety, API/Explorer parity, predicate registry, and verification
are now accepted as readiness controls. Taxonomy authoring/migration QA and the
Philippines overlay pilot remain draft controls. These artifacts improve
readiness evidence but do not by themselves authorize implementation.

The current scorecard remains conservative because the packet still lacks
independent second review, legal/licensing clearance, rollback proof, executable
benchmark fixtures, accepted runtime registries, and canonical source admission.
Fresh GitNexus evidence also shows HIGH/CRITICAL KG impact roots that must be
avoided or separately planned.

`AEC-BB-S1` added a file-backed validator only. It does not wire Backbone data
into the KG, Neo4j, API, Explorer, feature flags, or graph rebuilds.

`AEC-BB-S2` extends that same runtime-disconnected validator to executable
readiness fixtures for predicate rows, source-rights rows, authoring/migration
QA cases, resolver golden cases, API/Explorer parity cases, and a planned shadow
rollback protocol. The S2 fixture rows are contract examples only, not admitted
canonical taxonomy/source data.

`AEC-BB-S3` extends the validator again for integration readiness controls:
planned registry locations, API/Explorer parity-runner plan, rollback-proof
plan, benchmark plan, and runtime-blocking gate status. The S3 fixture is still
planning/readiness evidence only. It is not a production registry, not a Neo4j
backup/restore proof, and not runtime API/Explorer parity execution.

The current go/no-go answer is recorded in
`readiness-closure-scorecard.md`: local readiness controls improved, but runtime
integration remains blocked by legal/licensing clearance, executed rollback
proof, steward-admitted registries, canonical source admission, and separate
impact packets for HIGH/CRITICAL KG roots.

`AEC-BB-S4` adds the report-producing parity runner and a passing report at
`006_System-Manifests/aec-mepfs-backbone/parity/20260425T113719Z/api-explorer-parity-report.json`.
It also adds
`scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
with 14 required parity categories. This closes the local runner/case-evidence
gate, but not future `/v2` runtime route parity after shadow routes exist.

`AEC-BB-S5` adds the rollback preflight runner and a read-only report at
`006_System-Manifests/aec-mepfs-backbone/rollback/20260425T130816Z/rollback-preflight-report.json`.
It confirms the local Neo4j admin surface is available and the live graph is
reachable, but also confirms runtime remains blocked because dump/load require a
stopped or isolated database and no online backup subcommand is available.

`AEC-BB-S6` adds candidate registry files under `registry-candidates/` and a
validation report at
`006_System-Manifests/aec-mepfs-backbone/registry-candidates/20260425T133000Z/registry-candidate-validation-report.json`.
It validates 12 governed predicate rows and 29 first-wave source-rights rows,
but does not make those rows steward-admitted or legally cleared.

`AEC-BB-S7` adds the remaining AI-permissible readiness evidence and decision
packets: source currentness evidence, legal/steward admission ledger, canonical
source admission packet, Neo4j rollback rehearsal disposition, and the separate
runtime-root implementation packet. It also adds generated reports at
`006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T140712Z/source-currentness-report.json`
and
`006_System-Manifests/aec-mepfs-backbone/code-impact/20260425T140845Z/runtime-root-impact-report.json`.
S7 prepares implementation review but does not close human/legal approval,
canonical admission, or stopped/isolated rollback proof.

`AEC-BB-S8` adds a single human inbox packet at
`.ai/14_human_inbox/ANSWER_HERE.md`, resolves the five prior source currentness
exception rows for declared reference/metadata use where evidence permits, and
executes an isolated offline Neo4j import/dump/load rehearsal at
`006_System-Manifests/aec-mepfs-backbone/rollback/20260425T144332Z/isolated-dump-load-rehearsal-report.json`.
The S8 inbox was answered by project-owner directive captured on
2026-04-25T15:39:12Z. The first additive shadow-only implementation slice is now
implemented and documented in `first-shadow-only-implementation-packet.md`. This
does not authorize protected content ingest, live graph mutation, primary graph
promotion, or API/Explorer cutover.

Final locked-decision review returned `ITERATE` until L1/L2 home-domain policy,
L3/L4 auto-accept policy, and L1/L2 review thresholds are fully reconciled with
`.ai/03_plans/taxonomy-governance/00_locked_decisions.md`. The seventh shadow
graph slice does not change that runtime-readiness constraint.
