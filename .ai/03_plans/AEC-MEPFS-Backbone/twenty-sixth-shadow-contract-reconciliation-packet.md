---
task: aec-mepfs-shadow-contract-reconciliation
phase: 05
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Twenty-Sixth Shadow Slice: Contract Reconciliation

## Scope

Reconcile the AEC-MEPFS API/Explorer contract docs with the implemented
shadow-only `/v2` preview surface after the evidence Explorer preview.

This is documentation and state reconciliation only. It does not change API or
Explorer runtime code, add a route, mount `/v2/resolve`, write Neo4j, rebuild
the KG, ingest protected content, cut over feature flags, or make Explorer
adopt the shadow graph by default.

## Audit Findings

- `api-explorer-parity-contract.md` still described the implemented route set
  without `GET /v2/backbone/placement-qa` and
  `GET /v2/backbone/evidence` in the introductory contract text.
- `shadow-v2-api-read-route-planning-packet.md` still framed some read-route
  candidates as future even though the summary, taxonomy, node, search, source,
  placement-QA, and evidence routes are now implemented by separate packets.
- `api/README.md` and `explorer/README.md` did not fully describe the current
  placement-QA and evidence preview consumers.

## Implementation Plan

1. Update the API/Explorer parity contract to list all current implemented
   `/v2` preview routes and keep only resolver routes as blocked.
2. Update the shadow route planning packet to mark read previews implemented
   and resolver routes blocked.
3. Update API and Explorer READMEs for current placement-QA/evidence preview
   behavior.
4. Update AEC-MEPFS plan index/status docs and write validation evidence.

## Plan Critique

- [C001] Do not imply runtime readiness.
- [C002] Do not imply `/v2/resolve` is safe to mount.
- [C003] Keep no-ingest/no-Neo4j/no-default-Explorer boundaries explicit.
- [C004] Do not change runtime code for a documentation reconciliation slice.

## Execution Checklist

- [x] Inspect current contracts and implemented route/Explorer surfaces.
- [x] Update contract/readme/status documents.
- [x] Verify docs references and working tree scope.
- [x] Prepare commit-ready evidence; refresh GitNexus and inspect the next safe
  slice after commit/push.

## Explicit Non-Goals

- No API route changes.
- No Explorer runtime changes.
- No Neo4j write or query.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No `/v2/resolve` route mounting.
