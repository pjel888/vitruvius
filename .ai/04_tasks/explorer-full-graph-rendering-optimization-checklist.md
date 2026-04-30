# Explorer Full-Graph Rendering Optimization Checklist

Date: 2026-04-30

- [x] Confirm prior bounded visible-subgraph recommendation is not acceptable as default behavior.
- [x] Audit default render path for full graph vs subgraph behavior.
- [x] Add full-graph render instrumentation.
- [x] Measure pre-optimization full-graph browser baseline.
- [x] Implement stable graph signature and duplicate dataset replacement skip.
- [x] Implement cached deterministic full-graph startup layout for default large Network Layout.
- [x] Reduce redundant initial full-node/full-edge style updates.
- [x] Add full-graph render contract tests.
- [x] Run full validation suite.
- [x] Run Kimi final audit.
- [x] Commit task-scoped changes with Lore commit message.
