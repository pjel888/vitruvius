---
task: aec-mepfs-explorer-preview
phase: 09
created: 2026-04-26
author: REVIEWER
status: ACCEPTED
---

# AEC-MEPFS Explorer Preview Validation

## Scope Validated

This validation covers the fourth shadow consumer slice: an opt-in Explorer rail preview for `GET /v2/backbone`.

## Implementation Evidence

- `explorer/src/api/graphApi.ts` adds `getBackboneSummary()` for `GET /v2/backbone`.
- `explorer/src/types/index.ts` adds the typed `BackboneSummary` contract consumed by Explorer.
- `explorer/src/components/ExplorerRail.tsx` adds an icon-only AEC-MEPFS preview toggle; the preview is closed by default.
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx` renders compact counts, read-only boundaries, no-ingest posture, error state, loading state, and refresh.
- `explorer/src/components/componentInteraction.test.tsx` covers the panel success and error states.
- `explorer/src/app.searchInspector.integration.test.tsx` covers that the real Explorer rail does not fetch the preview on initial app load, fetches only after the explicit AEC-MEPFS toggle, and leaves graph state/perspective unchanged.
- `explorer/README.md` documents that the preview is shadow-scoped and does not change graph defaults.

## Boundary Evidence

- No KG rebuild was run.
- No Neo4j reset, dump, load, write, or mutation was run.
- No feature flag was added or flipped.
- No current graph perspective or default graph-loading path was changed.
- No protected source content, registry rows, or staging internals are exposed beyond the compact `/v2/backbone` summary.

## Impact Evidence

- GitNexus status before edit: indexed commit `1b630dd`, current commit `1b630dd`, status up to date.
- `ExplorerRail` upstream impact: LOW, 0 impacted symbols/processes/modules.
- Shared `graphApi.ts::api` helper upstream impact: CRITICAL, 31 impacted symbols. The implementation intentionally did not edit this helper; it only added a new exported wrapper that calls it.

## Verification

- `cd explorer && bun test` -> 38 pass, 0 fail.
- `cd explorer && bun run build` -> TypeScript build and Vite production build passed; Vite emitted the existing large-chunk warning for `vis-network`.
- `cd explorer && bun run lint` -> passed.
- `cd api && bun test` -> 22 pass, 0 fail.
- `git diff --check` -> passed.
- Live smoke on non-conflicting ports: `PORT=3001 bun run index.ts` and `VITE_API_BASE_URL=http://localhost:3001 bun run dev:vite --host 127.0.0.1 --port 5174`.
- `curl http://localhost:3001/v2/backbone` returned `schemaVersion: aec-bb-shadow-v2-backbone-summary/v1`, `runId: 20260425T154000Z`, 12 predicates, 29 source-rights rows, and all no-ingest/live-mutation boundaries clear.
- `curl -I http://127.0.0.1:5174/explore` returned HTTP 200.

## Residual Risks

- The preview is summary-only. Any future detail view needs a separate `/v2` route and packet.
- The full Explorer graph remains the 001-Laws MVP graph; AEC-MEPFS Backbone is not a live graph source yet.
- Browser screenshot verification was not run in this validation pass; component tests, production build, and live dev-server smoke covered the UI behavior.

## Architect Verification

- Ralph architect review: APPROVED / CLEAR.
- Architect noted the original gap that no test exercised the real ExplorerRail toggle/fetch path. That gap was closed after review with the new `AEC-MEPFS preview is opt-in and does not replace the graph state` integration test.
