# Explorer Full-Graph Rendering Optimization Validation

Date: 2026-04-30
Commit base: `608def8a`

## Summary
This phase rejected bounded visible-subgraph rendering as default Explorer behavior and optimized the current full-graph `vis-network` path instead. The default renderer dataset remains the full learner-facing render profile: 9,880 nodes and 13,285 edges.

## Changes validated
- Added full-graph render metrics (`window.__vitruviusGraphRenderMetrics`).
- Added stable full-graph render signature and full-graph contract helper.
- Skipped duplicate same-graph `DataSet` replacement.
- Used cached deterministic full-graph startup layout for large default Network Layout (`forceatlas2`) in the original 2026-04-30 optimization; corrected on 2026-05-01 so default Network Layout again uses centered physics startup.
- Disabled initial physics/stabilization only for explicit Precomputed Layout after the 2026-05-01 correction.
- Preserved settled layout cache writes when physics stabilization occurs.
- Suppressed no-op initial controller updates for unchanged layout, spread, labels, color, size, motion, and clear-path state.
- Added API and Explorer tests proving full learner-facing graph counts and source/provenance exclusions.

## Full-graph browser evidence
Baseline from `/tmp/fullgraph-baseline.json`:
- Nodes rendered by default: 9,880
- Edges rendered by default: 13,285
- Layout source: centered seed
- Physics enabled: true
- Network created: 544.70 ms
- Duplicate same-graph update: 562.00 ms, full replacement
- Long tasks: 8; total 3,609 ms; max 1,780 ms
- JS heap after smoke: ~266.8 MB

After from `/tmp/fullgraph-after-script.json`:
- Nodes rendered by default: 9,880
- Edges rendered by default: 13,285
- Layout source: full-graph precomputed startup (superseded on 2026-05-01; default Network Layout restored to centered physics seed)
- Layout cache hit: true
- Physics enabled: false for static startup (superseded for default Network Layout on 2026-05-01)
- Network created: 541.00 ms
- Duplicate same-graph update: 33.00 ms, full replacement skipped
- Stabilization: skipped by design for cached static full-graph startup
- Long tasks: 18; total 3,111 ms; max 1,657 ms
- JS heap after smoke: ~140.1 MB

## UX preservation
The current Explorer interface is preserved: same route, rails, command bar, toolbar, canvas, minimap, inspector/preview behavior, node/edge styles, search workflow, selection/highlight behavior, and `vis-network` renderer. 2026-05-01 correction: the default visible Network Layout startup uses the compact centered physics seed again; deterministic cached positions are only for the explicit Precomputed Layout option.

## Safety confirmations
- Default Explorer render path is not a bounded subgraph.
- Ordinary learner-facing nodes are not hidden by degree, search state, selected parent, viewport, cluster, or neighborhood cap.
- Internal/provenance/source-rights-only records remain excluded from learner-facing render profile.
- Bad learner-facing label checks remained covered by existing API regression tests and targeted scans.
- No protected source payload ingestion was performed.
- No Neo4j/live graph promotion was performed.
- No KG rebuild/reload/reset was performed.
- No destructive graph operation was performed.
- Kimi advisory audit: PASS, with no blockers.
- Codex Spark was not used; an earlier `omx explore` fallback used `gpt-5.5` after Spark quota failed.

## Validation commands
Final full-suite validation is recorded in the assistant final response for this phase.

## 2026-05-01 Network Layout correction
User review found the default Network Layout looked like the saved backbone/precomputed map rather than the expected bounded physics layout. The 2026-05-01 follow-up restored default `forceatlas2` startup to `centered-physics-seed` with physics enabled, kept the full graph rendered by default, and retained deterministic precomputed positions only for explicit Precomputed Layout.
