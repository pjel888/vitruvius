# Explorer Full-Graph Rendering Baseline and After Metrics

Date: 2026-04-30
Environment: local API on `localhost:3100`, Vite dev server on `127.0.0.1:5176`, Chrome headless via CDP on `127.0.0.1:9224`.

## Instrumented pre-optimization baseline
Source file: `/tmp/fullgraph-baseline.json`

- Default renderer node count: 9,880
- Default renderer edge count: 13,285
- Default layout source: centered seed
- Physics enabled: true
- First `loadGraph:networkCreated`: 544.70 ms
- Duplicate same-graph `loadGraph:updatedExisting`: 562.00 ms and replaced the full dataset
- Stabilization: no `stabilized` event observed within smoke window; physics remained enabled during startup
- Long tasks: 8; total 3,609 ms; max 1,780 ms
- Memory after smoke: ~266.8 MB used JS heap
- Render-profile resource durations observed: 202.7 ms and 1,490.1 ms (API fetch plus worker self-fetch)

## Post-optimization headless measurement
Source file: `/tmp/fullgraph-after-script.json`

- Default renderer node count: 9,880
- Default renderer edge count: 13,285
- Default layout source: full-graph precomputed startup layout (superseded by 2026-05-01 correction)
- Layout cache hit: true
- Physics enabled on startup: false (superseded for default Network Layout by 2026-05-01 correction)
- First `loadGraph:networkCreated`: 541.00 ms
- Duplicate same-graph `loadGraph:updatedExisting`: 33.00 ms and skipped full dataset replacement
- Stabilization: explicitly skipped for the cached static full-graph startup layout
- Long tasks: 18; total 3,111 ms; max 1,657 ms
- Memory after smoke: ~140.1 MB used JS heap
- Render-profile resource durations observed by the repo `measure:full-graph` script; values vary under the local dev server because the API fetch and worker self-fetch overlap with Vite/dev tooling.

## Interpretation
The highest-confidence measured improvement is not hiding graph nodes; it is eliminating repeated full `DataSet` replacement and redundant initial controller updates while keeping the full graph in `vis-network`. The 2026-04-30 startup-stabilization shortcut was superseded on 2026-05-01 because it made default Network Layout look like the saved backbone map. The corrected interpretation keeps duplicate full `DataSet` replacement elimination, but restores default full-graph physics startup and scopes deterministic cached positions to explicit Precomputed Layout only.

The remaining bottleneck is still `vis-network` full graph creation and initial canvas work, which remains on the main thread. Future work should evaluate a full-graph WebGL renderer adapter only if vis-network remains insufficient after production-browser profiling.

## 2026-05-01 corrected after-state
Default Network Layout should be read as: full graph rendered, compact centered seed, physics enabled, and no deterministic precomputed backbone-style startup. Explicit Precomputed Layout remains available for static cached positions.
