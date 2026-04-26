# Fifteenth Shadow Slice: Search Preview Route

**Date:** 2026-04-26
**Status:** implemented

## Scope

Add the next additive `/v2` read route for the AEC-MEPFS shadow backbone:

- `GET /v2/search`

The route is file-backed, shadow-only, and read-only. It searches staged
BackboneNode labels, preferred labels, path codes, and authored aliases from the
admitted L1/L2 fixture. It does not query Neo4j or expose protected source
payloads.

## Changes

- Added `SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION`.
- Added `buildShadowBackboneSearchPreview(...)`.
- Added `GET /v2/search`.
- Added deterministic search ranking and bounded result limiting.
- Added route tests for:
  - alias lookup,
  - deterministic limiting,
  - empty-query client errors,
  - source-payload sanitization,
  - missing shadow graph artifact fail-closed behavior,
  - runtime-boundary fail-closed behavior.
- Updated parity case `API-PARITY-002` from a contract-only placeholder to the
  route-backed `GET /v2/search` test and added `API-PARITY-002A` for the
  empty-query fail-closed path.
- Regenerated parity evidence at
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/api-explorer-parity-report.json`.

## Safety Boundary

This slice does not:

- write Neo4j
- rebuild KG
- ingest protected content
- cut over feature flags
- adopt the Backbone as Explorer default graph
- promote shadow artifacts to primary runtime

The route requires the sibling shadow graph artifact before returning results so
that search remains tied to the validated file-backed graph preview state.

## Blast Radius

Touched runtime code is limited to `api/index.ts` and focused API tests. No
Explorer runtime file is changed, so the current Explorer graph, selected
perspective, and opt-in preview behavior remain unchanged.

GitNexus impact on `buildShadowBackboneTaxonomyPreview` returned LOW impact
with 3 impacted nodes. The new search helper reuses that existing validation
path and adds only route-local result shaping.

## Verification

Primary validation is recorded in:

`/.ai/05_logs/2026-04-26_aec_bb_shadow_search_preview_route_validation.md`

Fresh parity evidence is recorded in:

`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T043021Z/api-explorer-parity-report.json`
