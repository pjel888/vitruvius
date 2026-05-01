---
task: aec-mepfs-explorer-preview
created: 2026-04-25T22:38:01Z
status: active
---

# AEC-MEPFS Explorer Preview Context Snapshot

## Task Statement

Implement the recommended non-default Explorer preview that reads the existing `GET /v2/backbone` shadow summary without changing the current Explorer graph default.

## Desired Outcome

Users can intentionally open an AEC-MEPFS Backbone preview in Explorer and see the compact shadow-readiness summary that is already exposed by `/v2/backbone`.

## Known Facts / Evidence

- The current Git baseline is `1b630ddc Expose the shadow backbone through a gated v2 read route`.
- Working tree was clean at intake.
- `.ai/01_roadmap/current-phase.md` says the first additive `/v2` shadow read route is implemented but not live-runtime-authorized for primary graph cutover or Explorer adoption.
- `.ai/STRATEGIC_NEXT_MOVE.md` names the next bounded choice as another `/v2` route or a non-default Explorer preview.
- The chosen path is the non-default Explorer preview.

## Constraints

- Do not rebuild, reset, or reload any KG or Neo4j graph.
- Do not change the Explorer default graph, default perspective, or graph loading path.
- Do not promote AEC-MEPFS shadow data into the current KG.
- Do not expose protected source content, registry rows, or staging internals beyond the compact route summary.
- Preserve current v1 API and Explorer graph behavior.
- Keep the preview additive, explicit, and reversible.

## Unknowns / Open Questions

- Exact Explorer component placement must be determined from the current UI structure.
- Existing test utilities and mocking style must be inspected before choosing the test shape.

## Likely Codebase Touchpoints

- `explorer/src/api/graphApi.ts`
- `explorer/src/App.tsx`
- Existing Explorer component tests under `explorer/src/**`
- `api/index.ts` only if the route shape needs a frontend-safe header or CORS adjustment; default expectation is no API runtime change.
