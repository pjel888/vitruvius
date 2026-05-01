# Explorer Network Layout Physics Restoration Validation

Date: 2026-05-01
Base: follow-up to commit `26b3bb16`

## Purpose
Restore default Explorer Network Layout (`forceatlas2`) semantics after user review showed the default layout looked like the saved/precomputed backbone map rather than the expected bounded physics layout.

## Corrected behavior
- Default Explorer still renders the full learner-facing graph by default.
- Default Network Layout uses compact centered startup positions and `vis-network` physics.
- Deterministic precomputed backbone-style positions are restricted to explicit Precomputed Layout.
- Duplicate full `DataSet` replacement skipping and full-graph render contract guardrails remain intact.
- No bounded subgraph, graph slicing, degree cap, or show-more default was introduced.

## Browser/headless evidence
Source files: `/tmp/network-layout-physics-after.json`, `/tmp/explorer-interaction-smoke.json`.

- Full graph nodes passed to the renderer: 9,880
- Full graph edges passed to the renderer: 13,285
- Default layout type: `forceatlas2`
- Default layout source: `centered-physics-seed`
- Layout cache hit for default Network Layout: `false`
- Physics enabled at `loadGraph:visData`: `true`
- Physics enabled at `loadGraph:networkCreated`: `true`
- First `loadGraph:networkCreated`: 673.5 ms in local Vite/headless smoke
- Duplicate same-graph update remained optimized: 33.0-34.6 ms with `skippedFullDatasetReplacement: true`
- Canvas count: 2
- Headless smoke confirmed the Explorer route, rail/search UI, and full graph metrics loaded without replacing the default graph with a subgraph.

## Data/source-rights safety evidence
- Render profile counts: 9,880 nodes, 13,285 edges.
- Bad learner-facing label hits: 0.
- Raw PDF filename label hits: 0.
- Source/provenance/evidence/document-version render-node leaks: 0.
- `Tropical Architecture` search resolves by alias to `VTN-DOM-0002711`.

## Validation commands
- `cd explorer && bun test ./src/components/graph/VisNetworkHost.test.ts` — 40 pass, 0 fail.
- `cd explorer && bun test` — 100 pass, 0 fail.
- `cd explorer && bun run build` — passed.
- `cd explorer && bun run lint` — passed.
- `cd api && bun test ./explorerPerformance.test.ts ./v2Backbone.test.ts ./v2Resolver.test.ts` — 93 pass, 0 fail.
- `cd api && bun test` — 113 pass, 0 fail.
- `cd explorer && bun run measure:full-graph http://127.0.0.1:9224 http://127.0.0.1:5176/explore 90000` — passed and recorded the metrics above.
- API render-profile safety scan — passed with counts and zero leak/bad-label hits above.
- `git diff --check` on task-scoped files — passed.
- Safety diff scans for Neo4j writes, KG rebuild/reload/reset, and Codex Spark routing — no hits in task-scoped diff.
- `npx gitnexus detect-changes --repo vitruvius --scope staged` — 8 files, 6 symbols, high process risk due `GraphScene` flows; accepted with targeted/full Explorer and API validation above.
- Kimi final read-only staged-diff audit — PASS.

## Safety confirmations
No protected source payloads were ingested. No Neo4j/live graph promotion was performed. No KG rebuild/reload/reset was performed. No destructive graph operation was performed. Codex Spark was not used.
