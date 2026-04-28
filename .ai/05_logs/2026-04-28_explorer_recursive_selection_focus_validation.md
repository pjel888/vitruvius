# Explorer Recursive Selection Focus Validation — 2026-04-28

## Summary

Selected-node focus now highlights the full selected taxonomy subtree instead of only the selected node plus first-hop children. When a taxonomy/domain/topic is selected, Explorer keeps labels and full-opacity styling for recursive descendants reached through taxonomy hierarchy edges, including grandchildren and deeper nodes. Non-selected nodes are dimmed more strongly so the selected branch is visually clearer.

## Scope

- Branch: `main`
- Start commit: `083a698f`
- End commit: commit containing this validation slice
- Classification: Explorer-only UI/UX selection-emphasis fix

## Files changed

- `explorer/src/components/graph/graphVisualEmphasis.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T141058Z/explorer-recursive-selection-focus-report.json`
- `.ai/05_logs/2026-04-28_explorer_recursive_selection_focus_validation.md`

## Implementation

- Changed selected-neighborhood construction from one-hop-only to recursive taxonomy subtree traversal.
- Traversal follows `HAS_CHILD` edges forward and `BELONGS_TO` / `PART_OF` edges in reverse.
- Direct connected nodes remain included so non-tree selections still retain useful local context.
- Edge emphasis now applies when both edge endpoints are inside the selected focus set.
- Reduced inactive selected-focus opacity from `0.5` to `0.24` for stronger contrast.

## Verification commands

| Command | Result |
| --- | --- |
| `bun test src/components/graph/VisNetworkHost.test.ts` | PASS — 27 pass, 0 fail, 74 expect calls |
| `bun test` | PASS — 74 pass, 0 fail, 330 expect calls |
| `bun run lint` | PASS |
| `bun run build` | PASS — Vite build succeeded; existing vis-network chunk-size warning remains |
| `git diff --check` | PASS |
| `curl -I --max-time 5 http://127.0.0.1:5174/explore` | PASS — HTTP/1.1 200 OK |

## Evidence artifact

- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T141058Z/explorer-recursive-selection-focus-report.json`

## Safety invariants

- Explorer-only change.
- No API route changes.
- No `/v2/resolve*` changes.
- No Neo4j changes.
- No KG rebuild/reload/reset changes.
- No taxonomy fixture changes.
- No protected content ingest or exposure changes.
- No resolver runtime changes.

## Residual risks

- The focus set intentionally includes direct non-tree neighbors in addition to recursive taxonomy descendants, preserving current behavior for concept/rule selections while expanding taxonomy selections.
- Build still reports the pre-existing large `vis-network` chunk warning.
