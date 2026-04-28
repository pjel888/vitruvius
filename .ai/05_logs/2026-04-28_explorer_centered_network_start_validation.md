# Explorer Centered Network Start Validation — 2026-04-28

## Summary

Network Layout previously allowed vis-network to choose initial node positions, which made the dense AEC-MEPFS graph appear to start near the outskirts before slowly settling into the middle. This slice seeds Network Layout nodes into a compact centered golden-angle disk before physics starts, so the first loaded frame begins near the center while preserving normal physics settling.

## Scope

- Branch: `main`
- Start commit: `169d9c88`
- End commit: commit containing this validation slice
- Classification: Explorer-only UI/UX performance/initial-layout fix

## Files changed

- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T135838Z/explorer-centered-network-start-report.json`
- `.ai/05_logs/2026-04-28_explorer_centered_network_start_validation.md`

## Implementation

- Added `buildCenteredNetworkLayoutPositions(...)` to compute compact centered first-frame coordinates.
- Applied those positions only when the active layout is `forceatlas2` / Network Layout.
- Left circular, clustered, random, and timeline layout placement unchanged.
- Added a regression test proving Network Layout seeding stays within a compact centered disk before physics settles.

## Verification commands

| Command | Result |
| --- | --- |
| `bun test src/components/graph/VisNetworkHost.test.ts` | PASS — 26 pass, 0 fail, 72 expect calls |
| `bun test` | PASS — 73 pass, 0 fail, 328 expect calls |
| `bun run lint` | PASS |
| `bun run build` | PASS — Vite build succeeded; existing vis-network chunk-size warning remains |
| `git diff --check` | PASS |
| `curl -I --max-time 5 http://127.0.0.1:5174/explore` | PASS — HTTP/1.1 200 OK |

## Evidence artifact

- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T135838Z/explorer-centered-network-start-report.json`

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

- The graph still uses physics, so nodes can continue to settle after first paint; the intended fix is that the initial positions start centered instead of far outside the view.
- Build still reports the pre-existing large `vis-network` chunk warning.
- In-app Browser Use screenshot automation was not available in this execution pass; local Vite HTTP smoke verified `/explore` availability.
