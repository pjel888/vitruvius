# Fourteenth Shadow Slice: Node Preview Route

**Date:** 2026-04-26
**Status:** implemented

## Scope

Add the next additive `/v2` read route for the AEC-MEPFS shadow backbone:

- `GET /v2/backbone/node/:id`

The route is file-backed, shadow-only, and read-only. It resolves the staged
BackboneNode fixture by VTN ID, canonical ID, or path code and returns a compact
node-detail preview with immediate file-backed relationship provenance.

## Changes

- Added `SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION`.
- Added `buildShadowBackboneNodePreview(...)`.
- Added `GET /v2/backbone/node/:id`.
- Expanded route tests for:
  - sanitized success payloads,
  - path-code lookup,
  - unknown IDs,
  - malformed escaped IDs,
  - missing shadow graph artifact fail-closed behavior,
  - runtime-boundary fail-closed behavior.
- Updated the parity fixture so direct VTN lookup and edge provenance display
  are now covered by the real node preview route.
- Regenerated parity evidence at
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json`.

## Safety Boundary

This slice does not:

- write Neo4j
- rebuild KG
- ingest protected content
- cut over feature flags
- adopt the Backbone as Explorer default graph
- promote shadow artifacts to primary runtime

The route fails closed if the shadow graph artifact is unavailable, because a
node-detail preview without graph provenance would misrepresent missing graph
state as an isolated node.

## Blast Radius

Touched runtime code is limited to `api/index.ts` and focused API tests. No
Explorer runtime file is changed, so the current Explorer graph, selected
perspective, and opt-in preview behavior remain unchanged.

GitNexus direct symbol impact for the new helper could not resolve before the
index refresh because the helper was newly introduced. The safer route was to
keep the change additive, run the full affected API and Explorer suites, rerun
the parity runner, and refresh GitNexus after commit.

## Verification

Primary validation is recorded in:

`/.ai/05_logs/2026-04-26_aec_bb_shadow_node_preview_route_validation.md`

Fresh parity evidence is recorded in:

`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json`
