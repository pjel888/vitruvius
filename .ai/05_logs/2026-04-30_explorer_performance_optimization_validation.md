# Explorer Performance Optimization Validation — 2026-04-30

## Scope
Dedicated Explorer performance phase for the Vitruvius architecture / AEC / LEA-ALE knowledge graph. The implementation preserved the current React/Vite/Tailwind/Zustand/React Query/vis-network Explorer UX and optimized the graph data/query/render pipeline underneath it.

## UX preservation checklist
Validated as preserved by code inspection and regression tests:
- Routes, Explorer layout, graph canvas, toolbar, rail, search workflow, preview panel, node selection, graph reset/clear behavior, source-clearance display, learner-facing filtering, Tailwind styling, and vis-network visual language remain in place.
- `VisNetworkHost` still owns the current vis-network renderer and interaction contract.
- Selected-node/neighbor emphasis remains direct visible-edge neighborhood only; the optimization narrows candidate edges through an index before applying the existing visible-edge checks.
- No renderer migration, UI rewrite, or visual redesign was performed.

## Baseline metrics
Measured with the in-process Hono API and Explorer helper benchmark script at `2026-04-30T10:19:28.177Z`.

| Metric | Baseline |
| --- | ---: |
| Graph nodes | 9,880 |
| Graph edges | 13,285 |
| Explorer graph response | 9,032,825 bytes / 8.61 MiB |
| Fetch graph | 126.66 ms |
| Parse graph response | 17.22 ms |
| First shell import | 63.48 ms |
| First searchable/interactive graph proxy | 143.89 ms |
| Search p50/p95 | 14.98 / 28.43 ms |
| Alias p50/p95 | 15.46 / 19.10 ms |
| Selection neighborhood p50/p95 | 0.29 / 0.33 ms |
| Highlight reason p50/p95 | 1.08 / 2.08 ms |
| One-hop expansion p50/p95 | 0.82 / 3.83 ms |
| Two-hop expansion p50/p95 | 1.10 / 6.07 ms |
| Path query p50/p95 | 2.77 / 4.30 ms |
| Preview node detail p50/p95 | 24.43 / 27.23 ms |
| Heap delta after graph load | 43.07 MiB |

## After metrics
Measured after the API compact render profile, lazy/indexed API graph operations, Explorer graph-engine index/worker client, CommandBar graph-engine search, and VisNetworkHost adjacency-candidate optimization.

| Metric | After |
| --- | ---: |
| Graph nodes | 9,880 |
| Graph edges | 13,285 |
| Explorer render response | 4,953,883 bytes / 4.72 MiB |
| Fetch graph | 82.91 ms |
| Parse graph response | 10.63 ms |
| First shell import | 51.79 ms |
| First searchable/interactive graph proxy | 93.54 ms |
| Search p50/p95 | 0.14 / 6.72 ms |
| Alias p50/p95 | 0.12 / 6.84 ms |
| Selection neighborhood p50/p95 | 0.25 / 0.34 ms |
| Highlight reason p50/p95 | 1.01 / 2.18 ms |
| One-hop expansion p50/p95 | 0.14 / 1.73 ms |
| Two-hop expansion p50/p95 | 0.17 / 0.61 ms |
| Path query p50/p95 | 0.41 / 2.02 ms |
| Preview node detail p50/p95 | 0.11 / 0.21 ms |
| Heap delta in one-off script | 56.19 MiB |

The source shadow/staging graph artifact files were not changed; the learner-facing Explorer render payload is smaller because the AEC render endpoint omits metadata not needed by the initial graph renderer.

## Validation commands
- `bun test api/explorerPerformance.test.ts explorer/src/graph-engine/graphIndex.test.ts explorer/src/api/graphApi.test.ts` — PASS, 9 tests / 71 assertions.
- `cd explorer && bun test` — PASS, 91 tests / 423 assertions.
- `cd explorer && bun run build` — PASS. Existing Vite warning remains for the large vis-network chunk.
- `cd explorer && bun run lint` — PASS.
- `cd api && bun test` — PASS, 111 tests / 1107 assertions.
- `python -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_lea_ale_resolver_deepening.py -q` — PASS, 75 passed.
- `git diff --check` — PASS.
- JSON validation — not applicable for task-scoped changes; no JSON files were modified by this Explorer performance work.

## Source-rights and learner-facing cleanliness scans
In-process render-profile scan result:
- Nodes: 9,880; edges: 13,285.
- Bad learner-facing label phrases: 0 hits for local raw-source filename metadata, raw-source filename metadata, metadata-only source-family reference, protected payload, reviewer candidate, unknown/private, and planning_reference_only.
- Raw PDF learner-facing labels: 0.
- Source/provenance-like default nodes: 0.
- Tropical Architecture resolves to clean concept node `VTN-DOM-0002711` / `Tropical Architecture And Climate Response`.

## Safety scans
Task diff safety scans found no Neo4j writes, no KG rebuild/reload/reset operation, no destructive graph operation, and no protected source ingestion path introduced. False-positive text matches were limited to documentation terms, existing imports/tests, and non-destructive preload/cache methods.

## Browser/manual smoke
The in-app browser/Playwright/Puppeteer tooling was unavailable in this environment. Closest available smoke:
- Updated API on `PORT=3001` responded to `/health` with 200.
- Updated API served `/perspective/aec-mepfs/nodes?profile=render` with 4,953,883 bytes and expected node/edge counts.
- Updated API search for `Tropical Architecture` returned clean concept result with no bad label.
- Vite dev server served `/explore` with 200 HTML.

Pan/zoom smoothness was not visually verified; this remains a follow-up limitation.

## Kimi final audit
Kimi CLI final evidence audit completed with verdict: PASS. Kimi noted remaining risks: browser visual regression unverified beyond HTTP smoke, Rust deferred, payload budget may need larger-graph monitoring, and no dedicated memory-pressure test was cited.

## GitNexus/index status
`npx gitnexus status` showed the Vitruvius index up to date before edits. Required impact checks were run for modified API/Explorer hot-path symbols. `gitnexus_detect_changes --scope all` reported CRITICAL because the repository already contains broad unrelated dirty work outside this task; task-scoped tests and safety scans passed.

## Remaining limitations
- Workerized query path exists with same-thread fallback; future work should move more parse/index construction cost into a worker-only lifecycle or compact transferable bundle.
- No actual browser screenshot/FPS/pan-zoom trace was available.
- Rust was not implemented because optimized TypeScript/API timings met the requested targets; recommended future insertion point is a build-time compact bundle generator or WASM worker kernel if new measurements justify the complexity.


## Follow-up continuation validation - worker-first graph engine lifecycle

User requested implementation of remaining limitations / next follow-up. The task-scoped follow-up addressed the highest-value safe limitation without changing UX: the graph-engine client now prefers the Web Worker index path and does not eagerly build a full fallback index on the React/main thread when worker loading succeeds. The fallback index is still built lazily when the worker is unavailable or fails, preserving reliability.

### Follow-up implementation
- `explorer/src/graph-engine/graphEngineClient.ts`
  - Added `workerReady`, `fallbackSource`, diagnostics, and test reset helpers.
  - `loadGraphEngine` now posts the full graph to the worker first and only builds the fallback index if the worker path fails.
  - Query helpers use the worker while ready and lazily fall back to the same TypeScript index implementation on worker failure.
- `explorer/src/graph-engine/graphEngineClient.test.ts`
  - Proves successful worker load leaves `fallbackIndexReady: false` while search is served through the worker.
  - Proves unavailable worker builds the same fallback index lazily and preserves search behavior.
- `api/explorerPerformance.test.ts`
  - Added serialized memory-pressure budgets for the render profile: total payload under 5.5 MB, average node under 400 bytes, average edge under 170 bytes, and heavy metadata fields absent.

### Fresh follow-up verification evidence
- `bun test api/explorerPerformance.test.ts explorer/src/graph-engine/graphEngineClient.test.ts explorer/src/graph-engine/graphIndex.test.ts explorer/src/api/graphApi.test.ts` - PASS, 12 tests / 89 assertions.
- `cd explorer && bun test` - PASS after fixing test isolation, 93 tests / 435 assertions.
- `cd explorer && bun run lint && bun run build` - PASS. Existing Vite chunk warning remains for `vis-network` size.
- `cd api && bun test` - PASS, 112 tests / 1113 assertions.
- `python -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_lea_ale_resolver_deepening.py -q` - PASS, 75 passed.
- `git diff --check` - PASS.
- Source-rights scan - PASS: 9,880 nodes, 13,285 edges, 4,953,883 bytes, 0 bad learner-facing label hits, 0 raw PDF labels, 0 source/provenance-like default nodes, clean Tropical Architecture concept result.
- Task diff safety scan - no destructive graph operation found; the only matches were false-positive `reset`/preload helper text.
- Kimi follow-up audit - PASS with risks: browser visual still unavailable; worker still uses structured clone, so a future transferable compact bundle may help.

### Follow-up limitations remaining
- Actual browser visual/FPS/pan-zoom verification remains unavailable in this environment.
- Worker load still transfers the graph via structured clone. A compact transferable typed-array/binary bundle remains the next high-value engine optimization if browser traces show structured clone cost or memory pressure.
- The tmux team runtime was not launched because this native Codex session is outside tmux.


### Final follow-up evidence refresh
- Added stale worker fingerprint guards and expected-fingerprint query checks so out-of-order worker load responses cannot mark an old graph as ready.
- `bun test explorer/src/graph-engine/graphEngineClient.test.ts explorer/src/graph-engine/graphIndex.test.ts api/explorerPerformance.test.ts` - PASS, 11 tests / 90 assertions.
- `cd explorer && bun test` - PASS, 95 tests / 445 assertions.
- `cd explorer && bun run lint && bun run build` - PASS.
- `cd api && bun test` - PASS, 112 tests / 1113 assertions.
- `git diff --check` and source-rights scan - PASS: 9,880 nodes, 13,285 edges, 4,953,883 bytes, 0 bad-label hits, 0 raw PDF labels, 0 source/provenance-like default nodes.
- Kimi latest follow-up audit - PASS; remaining risks are browser visual availability and structured-clone transfer cost.


### Ralph stop-hook fresh verification refresh
- `bun test explorer/src/graph-engine/graphEngineClient.test.ts explorer/src/graph-engine/graphIndex.test.ts api/explorerPerformance.test.ts` - PASS, 11 tests / 90 assertions.
- `cd explorer && bun test src/graph-engine/graphEngineClient.test.ts src/graph-engine/graphIndex.test.ts src/api/graphApi.test.ts && bun run lint` - PASS, 10 tests / 49 assertions plus lint.
- `git diff --check` - PASS.
- Source-rights scan - PASS: 9,880 nodes, 13,285 edges, 4,953,883 bytes, 0 bad-label hits, 0 raw PDF labels, 0 source/provenance-like default nodes, Tropical Architecture resolves to `VTN-DOM-0002711`.


### Team stop-hook terminal reconciliation
- Root team state was stale: `active: true`, `current_phase: starting`, but this native Codex session is outside tmux (`TMUX` unset), so no tmux coordinated runtime/workers were launched for the Explorer performance phase.
- Reconciled `.omx/state/team-state.json` to terminal `current_phase: cancelled` with lifecycle outcome `unavailable_without_attached_tmux`.
- Reconciled session `skill-active-state.json` so `ultrawork` and `ralph` are complete and `team` is cancelled/unavailable.
- Checked recent current-branch history for current-phase system worker checkpoint commits; none were introduced by this Explorer performance phase, so no Lore rewrite was applicable. Older historical checkpoint commits exist outside this phase and were not rewritten because history rewrite would be destructive.
- Fresh verification for the Explorer performance implementation remained green immediately before reconciliation.

### Proceed follow-up: structured-clone measurement, worker self-fetch, browser smoke, and layout-cache insertion point
- Measured real Chrome headless browser smoke against local API `http://localhost:3100` and Vite Explorer `http://127.0.0.1:5176/explore`.
- UX smoke PASS: Explorer shell opened, current rail/search/canvas/inspector text remained recognizable, `Tropical Architecture` search returned `VTN-DOM-0002711`, Enter selected the node and updated `/explore?node=VTN-DOM-0002711`, inspector text mentioned Tropical Architecture, and canvas pan/zoom input was accepted.
- Browser resource timing showed the render graph endpoint requested as `http://localhost:3100/perspective/aec-mepfs/nodes?profile=render`; the worker self-fetch path creates a second same render-profile request instead of transferring the full graph object from React to the worker.
- Structured-clone transfer measurement on the 4.72 MiB render payload: main-thread `structuredClone(graph)` p50 ~14.8-15.3 ms; object worker postMessage roundtrip p50 ~279-299 ms with cold p95/first roundtrip ~1.21-1.25 s. This confirmed graph-object structured clone is material enough to avoid in the app load path.
- Implemented worker `loadFromUrl`: `loadGraphEngine(nodes, edges, { sourceUrl })` sends only URL + expected fingerprint to the worker; the worker fetches the graph, builds the index, and rejects mismatched fingerprints. Unit test proves no `nodes`/`edges` are posted in the URL load message.
- Added settled vis-network layout-position cache keys by graph signature, layout mode, and spread. The current UX and default Network Layout remain unchanged; this is an invisible warm-load insertion point for persisted positions after stabilization.
- Post-change browser smoke remained PASS. Dev/headless readiness to full `9,880 nodes` text was still slow (~59-61 s) and long-task observer still showed vis-network/main-thread rendering work; this is now the primary remaining bottleneck, not API/search/index latency.

### Fresh proceed validation evidence
- `bun test explorer/src/components/graph/VisNetworkHost.test.ts explorer/src/graph-engine/graphEngineClient.test.ts explorer/src/api/graphApi.test.ts` - PASS, 47 tests / 174 assertions.
- `cd explorer && bun test` - PASS, 97 tests / 457 assertions.
- `cd explorer && bun run lint` - PASS.
- `cd explorer && bun run build` - PASS. Existing Vite chunk warning remains for `vis-network-Pd1GV7-0.js` at ~650 KiB.
- `cd api && bun test` - PASS, 112 tests / 1113 assertions.
- `bun test api/explorerPerformance.test.ts explorer/src/graph-engine/graphIndex.test.ts explorer/src/graph-engine/graphEngineClient.test.ts explorer/src/api/graphApi.test.ts explorer/src/components/graph/VisNetworkHost.test.ts` - PASS, 54 tests / 242 assertions.
- `git diff --check` - PASS.
- Source-rights safety scan - PASS: 9,880 nodes, 13,285 edges, 0 bad learner-facing label hits, 0 raw PDF labels, Tropical Architecture resolves first to `VTN-DOM-0002711`.
- Focused task-diff safety grep - PASS: no Neo4j live write/promotion, no KG rebuild/reload/reset, no protected source ingest, no destructive delete/mutation command, and no active Codex Spark routing found.

### Current limitations after proceed follow-up
- Browser smoke was real Chrome headless, not human manual review; no claim is made about subjective FPS beyond accepted pan/zoom input and preserved visible workflow text.
- The app now avoids graph-object structured clone for worker load, but it still fetches/parses JSON in both main UI and worker. A compact transferable/binary bundle remains the next evidence-backed optimization if production traces show duplicate parse/fetch or vis-network payload creation dominates.
- The largest remaining measured browser issue is vis-network/main-thread full-graph rendering/stabilization. Renderer migration remains deferred; bounded visible-subgraph rendering is rejected for the default Explorer behavior. The next no-redesign optimization path is full-graph render/stabilization optimization through stable vis-network datasets, layout caching, physics control, and possible full-graph WebGL renderer evaluation.
- Rust/WASM remains deferred because the newest bottleneck is browser renderer/main-thread workload, not TypeScript graph-query/index latency.

### Kimi proceed follow-up audit
Kimi CLI read-only audit completed with verdict PASS. Kimi found no serious blockers, judged UX preservation supportable because vis-network/current layout mode remain in use, judged worker self-fetch justified by the structured-clone evidence and unit assertions, and identified the next risk as remaining vis-network full-graph main-thread layout/render cost.

---

# Follow-up Explorer Performance Optimization Validation — 2026-04-30 UTC

## Scope

Dedicated Explorer performance optimization phase for the AEC-MEPFS / LEA-ALE learner-facing graph.

## Baseline graph

- Current UI/API graph source: file-backed shadow staging run `20260430T094129Z`.
- Current resolver source: `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`.
- Current measured learner-facing graph: 9,880 nodes / 13,285 relationships.
- Current artifact size: 5,367,411 bytes.
- Current source-rights rows from previous verified baseline: 106.
- Current resolver cases from previous verified baseline: 117.
- Bad-label hits in learner-facing graph artifact: 0.
- `SRC-RAW-*` learner-facing graph nodes: 0.

## Changes made in this phase

- Preserved current Explorer UX/UI and active vis-network renderer.
- Added UX preservation checklist: `.ai/03_plans/explorer-performance-ux-preservation-checklist.md`.
- Added exact-search and token-search indexes to `explorer/src/graph-engine/graphIndex.ts`.
- Cached visible-subgraph generation by graph fingerprint/options and avoided rooted full-edge scans where adjacency is sufficient. Search, neighborhood, and visible-subgraph caches are capped to prevent unbounded growth.
- Exposed graph-engine worker timing diagnostics through `getGraphEngineDiagnostics()`.
- Added `buildGraphEngineVisibleSubgraph()` so visible-subgraph generation can be requested through the existing worker/fallback graph-engine contract.
- Added current-shadow-artifact performance regression coverage in `explorer/src/graph-engine/graphPerformanceBench.test.ts`.
- Wrote benchmark report: `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260430T180217Z/explorer-performance-report.json`.

## Performance measurements

Measured via Bun against the current clean shadow graph artifact.

- Fetch/read: 0.871 ms.
- JSON parse: 6.2898 ms.
- Index build: 151.4063 ms.
- Optimized cold search p95: 0.1914 ms.
- Legacy full-scan search p95 emulation: 2.9373 ms.
- Optimized exact search p95: 0.0005 ms.
- Legacy exact full-scan search p95 emulation: 2.7432 ms.
- Alias lookup p95: 0.0009 ms.
- Selected direct-neighborhood p95: 0.0077 ms.
- One-hop expansion p95: 0.0011 ms.
- Two-hop expansion p95: 0.0005 ms.
- Path query p95: 1.0602 ms.
- Optimized visible-subgraph p95: 0.0015 ms.
- Legacy rooted full-edge-scan visible-subgraph p95 emulation: 0.2775 ms.

## Browser / visual smoke

- Actual Chromium screenshot smoke was run through `bunx playwright screenshot` against `http://127.0.0.1:5173/explore` with live API health available on port 3000.
- Screenshot evidence:
  - `/tmp/vitruvius-explorer-smoke.png` captured initial load state.
  - `/tmp/vitruvius-explorer-smoke-loaded.png` captured the loaded graph, toolbar, camera controls, zoom/spread controls, navigator, legend, minimap, and current visual language.
- Full scripted interaction smoke using Playwright test runner was attempted but unavailable through the transient `bunx playwright` package because `@playwright/test` was not available in the project dependency tree for temporary tests.
- Closest equivalent interaction coverage remains the Explorer component/integration suite plus the screenshot smoke.

## Rust feasibility

- Existing Rust surfaces were inspected read-only by the Rust feasibility lane.
- Existing crates include `vitruvius_engine_rs_core`, `vitruvius_engine_rs`, `vitruvius_spatial_kernels`, `vitruvius_stats_kernels`, `vitruvius_rust_pdf`, and `vitruvius_datalog_rs`.
- Existing WASM surface: `scripts/vitruvius/engine_rs/core/src/wasm_api.rs`; existing `.wasm` artifact is present.
- Current Explorer bottleneck remains vis-network main-thread rendering/DataSet churn, not graph-query compute.
- Rust/WASM was deferred; best future insertion point is `explorer/src/graph-engine/graphWorker.ts` / `graphIndex.ts` if future benchmarks prove a compute-bound worker bottleneck.

## Validation commands and results

- `bun test explorer/src/graph-engine/graphIndex.test.ts explorer/src/graph-engine/graphPerformanceBench.test.ts explorer/src/graph-engine/graphEngineClient.test.ts` — 10 pass / 0 fail after cache-bound regression coverage.
- `cd explorer && bunx tsc -p tsconfig.app.json --noEmit` — pass.
- Focused Explorer/API tests: 85 pass / 0 fail for targeted Explorer set; 93 pass / 0 fail for targeted API resolver/backbone/performance set.
- `cd explorer && bun run lint` — pass.
- `cd explorer && bun run lint && bun run build` — pass; existing chunk-size warning remains for vis-network chunk.
- `bun test api explorer` — 213 pass / 0 fail.
- `python -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py -q` — 70 passed.
- JSON validation for new performance report — pass.
- `git diff --check` — pass.
- Learner-facing bad-label scan on current graph artifact — 0 hits.
- Current graph artifact `SRC-RAW-*` node scan — 0 hits.
- Diff safety grep for exam/reviewer/code/table/figure/protected payload/Neo4j/destructive operations — 0 hits.
- Active Codex Spark route scan — only existing negative/Kimi-only routing assertions and prior reports; no active Codex Spark enrichment route introduced.
- GitNexus status at start: index up to date at commit `26b3bb1`.
- GitNexus impact for `buildGraphIndex`: CRITICAL blast radius because this is a central graph-engine function; covered by focused and broad Explorer/API validation.

## Source-rights and destructive-operation safety

- No protected source payloads were ingested.
- No reviewer text, exam questions, answer keys, protected tables, clauses, figures, diagrams, or protected PDF payloads were copied.
- No Neo4j/live graph promotion was performed.
- No KG rebuild/reload/reset was performed.
- No destructive graph operation was performed.

## Kimi usage

- Kimi advisory was run through `opencode run --model kimi-for-coding/k2p6` for performance strategy and Rust feasibility.
- Kimi identified vis-network/DataSet churn as the likely dominant remaining bottleneck and recommended TypeScript index/worker optimizations before Rust.
- Codex Spark was not used.

## Remaining limitations

- The browser smoke was screenshot-based rather than a fully scripted Playwright interaction because transient Playwright CLI did not expose `@playwright/test` in the project dependency graph.
- True pan/zoom FPS and main-thread long-task profiling remain the next highest-value manual browser follow-up.
- This phase did not change the renderer or implement Rust because benchmarks do not justify that complexity yet.

## Kimi final read-only audit

- Command: `opencode run --model kimi-for-coding/k2p6 ...`.
- Result: APPROVED — no blockers.
- Kimi audit confirmed UX preservation, benchmark honesty, worker/index correctness, source-rights cleanliness, bad-label regression coverage, no protected ingestion, no Neo4j/live promotion or KG rebuild/reset, Rust deferral rationale, and Codex Spark avoidance.
