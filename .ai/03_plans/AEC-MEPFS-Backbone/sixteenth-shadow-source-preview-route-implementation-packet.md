# Sixteenth Shadow Slice: Source Metadata Preview Route

**Date:** 2026-04-26
**Status:** implemented

## Scope

Add a bounded additive `/v2` read route for AEC-MEPFS shadow source metadata:

- `GET /v2/sources/:source_id`

The route must stay file-backed, shadow-only, and read-only. It resolves a
source-rights registry row from the staged Backbone artifact and returns only
sanitized source metadata needed for preview/parity. It must not expose
standards text, protected source payloads, official URLs, blocking notes, or
intended-use governance prose.

## Planned Changes

- Added a source-preview schema constant.
- Added `buildShadowBackboneSourcePreview(...)`.
- Added `GET /v2/sources/:source_id`.
- Added route tests for:
  - successful source lookup,
  - source not found,
  - malformed escaped source ids,
  - blank decoded source ids,
  - source-payload sanitization,
  - runtime-boundary fail-closed behavior.
- Updated parity case `API-PARITY-011` from a placeholder Explorer coverage case
  to a route-backed source metadata preview case.
- Added parity case `API-PARITY-011A` for invalid blank decoded source IDs.
- Regenerated API/Explorer parity evidence at
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T052238Z/api-explorer-parity-report.json`.

## Safety Boundary

This slice must not:

- write Neo4j
- rebuild KG
- ingest protected content
- cut over feature flags
- adopt the Backbone as Explorer default graph
- promote shadow artifacts to primary runtime

The implementation must reuse the existing shadow staging consumer report and
artifact validation path so source metadata is only exposed when the file-backed
shadow artifact passes the same safety gates as the taxonomy/search previews.

## Verification Plan

- GitNexus status and impact review before editing.
- Focused API route tests.
- API typecheck.
- Focused Python backbone tests if parity fixture/report changes.
- Full API tests.
- API/Explorer parity runner with a fresh run id.
- Explorer tests/lint/build when parity or preview-surface contracts could
  affect consumers.
- Gemini/Kimi advisory review if local access is available.
- Native architect review before commit.

Primary validation is recorded in:

`/.ai/05_logs/2026-04-26_aec_bb_shadow_source_preview_route_validation.md`
