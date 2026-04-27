---
task: aec-mepfs-backbone
phase: default-off-resolver-runtime
created: 2026-04-27
author: CODEX
status: PASS
classification: YELLOW-1,YELLOW-2,YELLOW-3
---

# Default-Off Resolver Runtime Packet

## Purpose

Authorize the first narrow runtime resolver surface for AEC-MEPFS Backbone under
the project-owner standing directive. This packet advances beyond static/no-op
contract verification by allowing a guarded, default-off, file-backed
`/v2/resolve*` route family that is deterministic over non-protected fixture
metadata only.

This is a scoped runtime boundary. It is not global `LIVE_RUNTIME_AUTHORIZED`
for the AEC-MEPFS project.

## Authority

- Standing project-owner directive for autonomous AEC-MEPFS completion.
- `runtime-governance-admission-packet.md`, with row-level decisions preserved.
- Completed predecessor: `2026-04-27_bounded_resolver_runtime_contract_packet.md`
  and commit `618a659b`.

## Allowed Scope

This packet permits only:

1. A default-off runtime guard for resolver routes.
2. `POST /v2/resolve` and `GET /v2/resolve/trace/:trace_id` declarations only
   when wrapped by the default-off runtime guard.
3. File-backed deterministic response builders over the existing non-protected
   S2 resolver fixture.
4. Deterministic trace-safe responses that expose canonical IDs, source IDs,
   fallback reasons, and safe rationale only.
5. Static route inventory evolution so guarded default-off declarations are
   represented honestly instead of hidden as absence.
6. Resolver QA, route-inventory, boundary-audit, benchmark, evidence-manifest,
   API, and Explorer tests needed to prove the route is default-off and safe.
7. Documentation/state reconciliation for the completed static slice and this
   default-off runtime slice.

## Explicitly Blocked Scope

This packet does not authorize:

- global `LIVE_RUNTIME_AUTHORIZED` status
- default-on feature flags or hidden cutover
- Neo4j writes, reset, reload, backup, restore, cleanup, namespace promotion, or
  primary graph replacement
- KG rebuild, reload, reset, or primary graph replacement
- protected source text, table, figure, dataset, clause, or local protected-cache
  ingest
- Explorer default graph adoption or default perspective changes
- automatic Explorer preview fetches
- runtime threshold pass/fail claims
- edits to `CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`
- LLM calls on the resolver hot path

## Exact Runtime Surface

| Surface | Status | Guard | Default |
|---|---|---|---|
| `POST /v2/resolve` | allowed only under this packet | `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME` | off |
| `GET /v2/resolve/trace/:trace_id` | allowed only under this packet | `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME` | off |

The default exported API must keep `/v2/resolve*` absent when the guard is not
set to an explicit true value (`1`, `true`, `yes`, or `on`).

## Request Contract

Accepted request shape:

- `query.text` (required)
- `query.concept_id` / `query.conceptId` (optional)
- `query.asset_context` / `query.assetContext` (optional)
- `query.context_ids` / `query.contextIds` (optional string array)
- `query.jurisdiction_filters` / `query.jurisdictionFilters` (optional string array)
- `query.discipline_filters` / `query.disciplineFilters` (optional string array)
- `query.trace_requested` / `query.traceRequested` / `include_trace` (optional boolean)
- `jurisdiction` (optional)
- `effective_date` / `effectiveDate` (optional)

Invalid JSON, empty `query.text`, and malformed array fields fail
deterministically with 400-class errors.

## Response Contract

Responses are deterministic and file-backed:

- `schemaVersion: aec-mepfs-resolver-response/v1`
- `runtimeMode: default_off_file_backed_fixture`
- `resultType: single_value | composed | conflict | none`
- `confidence: deterministic | review_required | insufficient`
- `canonicalNodeRefs[]`
- `sourceEvidenceRefs[]`
- `fallbackReason`
- `traceId`
- `traceSafeRationale`
- optional `trace` when requested
- optional `conflictSet` for `conflict`
- `boundaries` proving no Neo4j, KG rebuild, protected ingest, LLM hot path,
  Explorer default adoption, or threshold claim

## Golden Fixtures

Authorized fixture source:

```text
scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json
```

Required cases:

- `single_value`
- `composed`
- `conflict`
- `none`
- invalid input
- malformed request
- missing fixture artifact
- deterministic no-result
- guarded/default-off route inventory
- unguarded route rejection

## Route Inventory Policy

The route inventory must no longer conflate default-off declarations with unsafe
mounting. It must report:

- `resolverRoutePolicy: absent | guarded_default_off | unsafe_mounted`
- `resolveRouteDeclared`
- `traceRouteDeclared`
- `defaultOffResolveRouteDeclared`
- `defaultOffTraceRouteDeclared`
- `guardedResolveRoutes`
- `forbiddenResolveRoutes` for unauthorized/unguarded routes only

Existing shadow evidence must shift from the stale phrase “resolver routes
unmounted” to “resolver routes absent or default-off guarded.”

## Fallback Semantics

- Missing exact fixture case returns `none`, not generated content.
- Equal-force incompatible fixture case returns `conflict` with human-review
  disposition.
- Missing fixture artifact fails closed with 503.
- Trace lookup is deterministic from fixture case IDs; no runtime trace state is
  persisted.
- No protected source payload is exposed.

## Verification Commands

Minimum verification for this packet:

```bash
git diff --check
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_resolver_qa.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py -q
(cd api && bun test v2Resolver.test.ts)
(cd api && bun test v2Backbone.test.ts)
(cd explorer && bun test)
```

Run broader lint/build if Explorer or API contracts are touched beyond test
fixtures.

## Evidence Artifacts

After source/docs are committed so source-tree dirtiness is false, regenerate:

- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/<RUN_ID>/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/resolver-qa/<RUN_ID>/resolver-qa-report.json`
- `006_System-Manifests/aec-mepfs-backbone/boundary-audit/<RUN_ID>/shadow-boundary-audit-report.json`
- `006_System-Manifests/aec-mepfs-backbone/benchmarks/<RUN_ID>/benchmark-report.json`
- `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/<RUN_ID>/shadow-evidence-manifest-report.json`
- `.ai/05_logs/2026-04-27_aec_mepfs_default_off_resolver_runtime_validation.md`

## Rollback Proof

Rollback is git-revert only. No database, graph, Explorer default, feature flag,
or protected-source cleanup is required because the slice is code/file-backed
and default-off.

## Safety Invariants

- Resolver routes are absent by default or explicitly default-off guarded.
- No Neo4j write/mutation path is introduced.
- No KG rebuild/reload/reset path is introduced.
- No protected content ingest or exposure is introduced.
- No Explorer default adoption is introduced.
- No default-on flag is introduced.
- No runtime threshold claim is made.
- Existing `/v2/backbone*`, `/v2/search`, and source/evidence preview routes
  remain stable.

## Completion Criteria

This packet is complete when:

- guarded default-off resolver routes exist and are absent by default
- enabled route behavior is covered by API tests
- route inventory distinguishes guarded/default-off from unsafe mounting
- downstream evidence uses “absent or default-off” semantics
- focused Python/API/Explorer tests pass
- evidence artifacts are regenerated from a clean source tree
- validation log records impact, tests, advisory review, and safety invariants
- commits are pushed to `origin/main`

## Next Boundary

The next packet may add broader resolver fixtures, parity cases, or benchmark
harness work. Neo4j/live graph promotion, protected source ingestion, Explorer
default adoption, default-on flags, and runtime threshold claims remain separate
YELLOW/RED gates.
