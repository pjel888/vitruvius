# Explorer Performance Next-Agent Handoff Plan

Created: 2026-05-01 Asia/Manila
Scope: Vitruvius Explorer performance optimization follow-up
Status: Ready for next codebase AI takeover

## Current verified state

The latest Explorer performance phase completed with the current UX preserved.

Known verified baseline:

- Learner-facing graph: 9,880 nodes / 13,285 relationships.
- Active UI/API graph source: file-backed shadow staging run `20260430T094129Z`.
- Active resolver source: `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`.
- Graph artifact size: 5,367,411 bytes.
- Learner-facing bad-label hits: 0.
- `SRC-RAW-*` learner-facing graph nodes: 0.
- Kimi final read-only audit: approved, no blockers.
- Codex Spark was not used.
- No protected source payloads were ingested.
- No Neo4j/live graph promotion, KG rebuild/reload/reset, or destructive graph operation was performed.

## Work completed in the latest phase

Main performance changes:

- Added exact-search index and token/inverted search index in `explorer/src/graph-engine/graphIndex.ts`.
- Added bounded caches for search, neighborhood expansion, and visible-subgraph generation.
- Optimized rooted visible-subgraph generation to avoid full-edge scans when adjacency is enough.
- Added worker timing diagnostics in `explorer/src/graph-engine/graphEngineClient.ts`.
- Added `buildGraphEngineVisibleSubgraph()` through the existing worker/fallback graph-engine contract.
- Added performance regression coverage against the current shadow graph artifact.
- Preserved current vis-network renderer and UI/UX.

Primary files touched by the Explorer performance phase:

- `explorer/src/graph-engine/graphIndex.ts`
- `explorer/src/graph-engine/graphEngineClient.ts`
- `explorer/src/graph-engine/graphIndex.test.ts`
- `explorer/src/graph-engine/graphEngineClient.test.ts`
- `explorer/src/graph-engine/graphPerformanceBench.test.ts`
- `.ai/03_plans/explorer-performance-ux-preservation-checklist.md`
- `.ai/05_logs/2026-04-30_explorer_performance_optimization_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260430T180217Z/explorer-performance-report.json`

Performance evidence from the latest benchmark report:

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

## Validation already run

Latest relevant validation evidence:

- `bun test explorer/src/graph-engine/graphIndex.test.ts explorer/src/graph-engine/graphPerformanceBench.test.ts explorer/src/graph-engine/graphEngineClient.test.ts` — 10 pass / 0 fail.
- `cd explorer && bunx tsc -p tsconfig.app.json --noEmit` — pass.
- `bun test api explorer` — 213 pass / 0 fail.
- `cd explorer && bun run lint` — pass.
- `cd explorer && bun run build` — pass; existing chunk-size warning remains for the vis-network chunk.
- `python -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py -q` — 70 passed.
- JSON validation for `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260430T180217Z/explorer-performance-report.json` — pass.
- `git diff --check` — pass.
- Learner-facing bad-label scan — 0 hits.
- Current graph artifact `SRC-RAW-*` node scan — 0 hits.
- GitNexus status — up to date at commit `26b3bb1` when checked.

## Current worktree warning

The repository has a broad dirty worktree from multiple recent phases. A future agent must inspect before staging/committing.

Do not assume all dirty files belong to the Explorer performance phase.

Known groups of dirty/untracked files include:

1. Explorer performance phase files listed above.
2. Prior Philippine architecture / UI evidence path graph work.
3. Prior KG fixture/script/test updates.
4. Shadow staging and resolver QA output folders.

Before committing, run:

```bash
git status --short
git diff --stat
git diff --name-only
```

If committing only Explorer performance work, stage selectively.

## UX preservation contract for future work

Future performance work must preserve:

- Current routes and Explorer layout.
- Top command/search flow.
- Explorer rail and taxonomy navigation.
- Graph canvas look and visual language.
- Camera toolbar, Select/Pan behavior, and keyboard shortcuts.
- Zoom and spread controls.
- Node selection and preview/inspector workflow.
- Direct visible-edge selected-neighborhood highlighting.
- Source-clearance display.
- Default learner-facing filtering.
- Current vis-network renderer unless replacement is benchmark-proven and adapter-gated.

Reference checklist:

- `.ai/03_plans/explorer-performance-ux-preservation-checklist.md`

## Next highest-value optimization plan

### 1. Run true interactive browser performance profiling

Goal: determine whether remaining perceived slowness is vis-network drawing, DataSet update churn, layout/physics, React re-rendering, or network/worker duplication.

Suggested steps:

1. Start API and Explorer dev server.
2. Open `/explore` in real Chrome.
3. Record Chrome DevTools Performance trace for:
   - initial graph load,
   - pan for 5 seconds,
   - zoom in/out repeatedly,
   - select high-degree parent node,
   - search `Tropical Architecture`,
   - switch Select/Pan modes.
4. Capture:
   - long tasks over 50 ms,
   - canvas paint/redraw time,
   - `DataSet.update()` cost,
   - vis-network stabilization time,
   - React commit/render hotspots,
   - memory after graph load and after repeated selection.
5. Save trace summary under:
   - `.ai/02_audits/explorer-browser-performance-profile-audit.md`
   - `006_System-Manifests/aec-mepfs-backbone/explorer-performance/<run-id>/browser-profile-summary.json`

Do not claim manual/browser profiling unless actually performed.

### 2. Optimize vis-network DataSet churn if profiling confirms it

Likely candidates:

- Avoid full `nodesRef.current.update(rawNodesRef.current.map(...))` on every selection where possible.
- Track previous selected-neighborhood set and update only node/edge deltas.
- Use partial update payloads containing only changed fields.
- Batch/coalesce selection/label/color updates within one animation frame.
- Preserve current visual semantics: selected node + direct visible-edge neighbors only.

High-risk file:

- `explorer/src/components/graph/VisNetworkHost.tsx`

Required before editing:

```bash
npx -p gitnexus@1.6.2-rc.10 gitnexus impact VisNetworkHost -r vitruvius -d upstream --include-tests || true
npx -p gitnexus@1.6.2-rc.10 gitnexus impact applySelectedNeighborhoodEmphasis -r vitruvius -d upstream --include-tests || true
```

Add tests before/with edits:

- Selection still highlights only selected node plus direct visible-edge neighbors.
- Provenance/internal/source edges do not create learner-facing highlight.
- Node labels remain visible for selected-neighborhood nodes and hidden for dimmed non-neighbors.
- No stale emphasis remains after clear selection.

### 3. Evaluate render payload preparation

If traces show object hydration or vis-network item creation is expensive:

- Consider moving render item preparation into a worker.
- Keep vis-network itself on main thread.
- Transfer only compact node/edge render arrays or deltas.
- Preserve current UI and graph semantics.

Do not implement a binary bundle until browser profiling proves JSON parse/object hydration is a real bottleneck.

### 4. Keep Rust deferred unless compute-bound evidence appears

Rust/WASM is not currently justified for Explorer graph queries.

Defer Rust unless new measurements show one of these is slow after TypeScript worker/index optimizations:

- worker search p95 > 30 ms,
- alias p95 > 15 ms,
- one-hop expansion p95 > 30 ms,
- two-hop expansion p95 > 75 ms,
- path queries become compute-bound on much larger graphs,
- deterministic spatial indexing for viewport culling becomes necessary.

Best future Rust insertion point:

- `explorer/src/graph-engine/graphWorker.ts`
- `explorer/src/graph-engine/graphIndex.ts`

Do not rewrite the Explorer UI in Rust.

### 5. Renderer migration remains deferred

Do not replace vis-network by default.

Only revisit renderer migration if profiling proves vis-network remains the dominant bottleneck after:

- delta-based DataSet updates,
- batched selection updates,
- layout/physics tuning,
- label level-of-detail experiments,
- viewport/subgraph or hidden-node strategies that preserve UX.

If migration becomes necessary, use an adapter contract and keep old renderer until parity is proven.

## Suggested validation commands for the next phase

Run at minimum:

```bash
bun test explorer/src/graph-engine/graphIndex.test.ts explorer/src/graph-engine/graphPerformanceBench.test.ts explorer/src/graph-engine/graphEngineClient.test.ts
bun test explorer/src/components/graph/VisNetworkHost.test.ts explorer/src/app.searchInspector.integration.test.tsx explorer/src/components/componentInteraction.test.tsx explorer/src/api/graphApi.test.ts
bun test api/explorerPerformance.test.ts api/v2Backbone.test.ts api/v2Resolver.test.ts
cd explorer && bunx tsc -p tsconfig.app.json --noEmit
cd explorer && bun run lint
cd explorer && bun run build
python -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py -q
git diff --check
npx -p gitnexus@1.6.2-rc.10 gitnexus status
```

If graph fixtures/artifacts are touched, also run the broader KG validation suite and resolver QA.

## Safety checks for next phase

Always verify:

- No learner-facing label contains `Local raw-source filename metadata`.
- No learner-facing label contains `raw-source filename metadata`.
- No learner-facing label contains `metadata-only source-family reference`.
- No learner-facing label contains `protected payload`.
- No learner-facing label contains `reviewer candidate`.
- No learner-facing label contains `unknown/private`.
- No learner-facing label contains `planning_reference_only`.
- No learner-facing node is a raw PDF filename.
- `Tropical Architecture` resolves to the clean concept node.
- No source/provenance/internal-only records appear as ordinary concept nodes.
- No provenance/internal edge creates learner-facing selected-neighborhood highlight.
- No protected source payloads, reviewer text, exam questions, answer keys, protected tables, clauses, figures, or diagrams are ingested.
- No Neo4j/live graph promotion, KG rebuild/reload/reset, or destructive graph operation is performed.
- Codex Spark is not used for KG enrichment/research.

## Kimi usage guidance

Use Kimi for:

- performance strategy review,
- browser-profile interpretation,
- Rust/WASM feasibility review,
- final read-only audit.

Example:

```bash
opencode run --model kimi-for-coding/k2p6 "Read-only audit of Explorer performance follow-up. Review changed files, benchmark evidence, UX preservation, source-rights safety, and validation. Do not edit files. Return blockers or approval."
```

## Do-not-do list

- Do not redesign the Explorer.
- Do not replace vis-network without benchmark evidence and adapter parity.
- Do not add graph content as part of performance work.
- Do not promote to Neo4j or mutate a live graph.
- Do not run KG rebuild/reload/reset for this UI performance task.
- Do not ingest protected source payloads.
- Do not fake browser/manual results.
- Do not fake benchmarks.
- Do not stage all dirty files blindly.

## Immediate next action for takeover agent

1. Read this file.
2. Read `.ai/05_logs/2026-04-30_explorer_performance_optimization_validation.md`.
3. Inspect `git status --short` and separate Explorer performance changes from prior KG changes.
4. Run the focused graph-engine tests once to establish local continuity.
5. Start real Chrome/Playwright profiling of `/explore` and save the browser profile summary.
6. If profiling confirms selection/DataSet churn, implement delta-based selected-neighborhood updates in `VisNetworkHost.tsx` with tests.
