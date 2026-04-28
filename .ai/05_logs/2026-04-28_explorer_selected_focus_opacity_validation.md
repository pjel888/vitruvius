# Explorer Selected Focus Occlusion Validation — 2026-04-28

## Summary

Unselected nodes are now visually reduced during selected-node focus. The inactive focus opacity changed from `0.24` to `0.08`, unrelated focus edges changed to `0.06`, and inactive node bodies shrink to `42%` of their normal size with a `2.5px` minimum. This makes the selected node and recursive selected subtree stand out more clearly in dense AEC-MEPFS graphs and reduces visual occlusion from unrelated overlapping nodes.

## Scope

- Branch: `main`
- Start commit: `e48d3832`
- End commit: commit containing this validation slice
- Classification: Explorer-only visual emphasis / occlusion tuning

## Files changed

- `explorer/src/components/graph/graphVisualEmphasis.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T141556Z/explorer-selected-focus-opacity-report.json`
- `.ai/05_logs/2026-04-28_explorer_selected_focus_opacity_validation.md`

## Browser Use status

The requested Browser Use path was attempted according to the installed skill. Browser Use requires a Node REPL `js` execution tool for the in-app browser runtime; tool discovery did not expose that execution tool in this session. Local Vite smoke testing is used as the available fallback.

## Verification commands

| Command | Result |
| --- | --- |
| `bun test src/components/graph/VisNetworkHost.test.ts` | PASS — 27 pass, 0 fail, 77 expect calls |
| `bun test` | PASS — 74 pass, 0 fail, 333 expect calls |
| `bun run lint` | PASS |
| `bun run build` | PASS — Vite build succeeded; existing vis-network chunk-size warning remains |
| `git diff --check` | PASS |
| `curl -I --max-time 5 http://127.0.0.1:5174/explore` | PASS — HTTP/1.1 200 OK |

## Safety invariants

- Explorer-only change.
- No API route changes.
- No `/v2/resolve*` changes.
- No Neo4j changes.
- No KG rebuild/reload/reset changes.
- No taxonomy fixture changes.
- No protected content ingest or exposure changes.
- No resolver runtime changes.
