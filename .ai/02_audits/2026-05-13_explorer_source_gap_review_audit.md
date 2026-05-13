# Audit: Explorer Source Gap Review Surface

## Current State
- Source-gap artifacts are generated but not directly inspectable from the selected-node Explorer panel.
- Explorer already has source context UI, but it shows graph paths/resources rather than the workqueue of missing evidence/source links.
- The existing API has helpers for safe run-id validation, JSONL tolerant reading, latest-run selection, and read-only overlay projection.

## Blast Radius
- API read path: add one file-backed preview route and helper functions in `api/index.ts`.
- Explorer client: add one fetch helper and types.
- Explorer UI: add one compact panel inside the existing Context tab.
- Tests: API route behavior and NodeInspector rendering.

## Risks
- Artifact files can be absent, partial, or from older schema versions. The route must return an empty unavailable-safe payload rather than crash.
- Large workqueues could be expensive to render. The route should cap returned rows.
- Workqueue data is proposal-only. UI must keep no-admission language visible.

## Safety Audit
- No active graph fixture writes are needed.
- No Resource Layer registry writes are needed.
- No Neo4j/Postgres write calls are needed.
- No protected payload/source text is included; only generated labels, ids, metadata matches, and resource titles are displayed.

## Recommendation
Implement selected-node source-gap preview first. Defer approval/admission workflows until a separate source-link steward packet exists.
