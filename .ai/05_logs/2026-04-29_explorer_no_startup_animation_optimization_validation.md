# Explorer No-Startup-Animation Optimization Validation

## Scope

Optimize the Explorer large-graph startup experience so the AEC-MEPFS graph does
not visibly begin as a compact center mass and animate outward on entry.

## Repo state

- Branch: `main`
- Starting commit: `16c04dfc`
- Ending commit: recorded in final response after commit
- Working tree before implementation: clean

## Files inspected

- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/package.json`
- `.ai/13_research/2026-04-28_explorer_ui_ux_large_graph_optimization_research.md`
- `.ai/02_audits/2026-04-28_explorer_ui_ux_performance_audit.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_ui_ux_optimization_readiness_and_implementation_plan.md`

## Files changed

- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_no_startup_animation_optimization_packet.md`
- `.ai/05_logs/2026-04-29_explorer_no_startup_animation_optimization_validation.md`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T000000Z/no-startup-animation-report.json`

## Team findings reconciled

OMX team `read-only-explorer-large-graph` completed read-only research. Findings:

- Worker 1 identified visible constructor-time physics/stabilization as the
  startup animation source and recommended a large-graph-only startup guardrail.
- Worker 2 confirmed relevant Explorer test anchors and verification commands;
  after dependency install, focused tests, full Explorer tests, lint, and build
  passed in the worker workspace.
- Team was shut down cleanly after both tasks completed.

## Implementation summary

- Added `shouldHideInitialGraphStabilization` to classify only large,
  unpaused Network Layout startup as requiring hidden stabilization.
- `VisNetworkHost` now hides the vis-network canvas synchronously before large-graph stabilization on first mount and reused graph loads, then reveals only after `stabilizationIterationsDone` or `stabilized`, with no timeout-based early reveal.
- Existing bounded physics, spread controls, auto-freeze, small-graph behavior,
  label/edge styling, minimap/filter behavior, and selected-neighborhood logic
  remain unchanged.

## Commands run

```bash
git status --short --branch
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts
bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx
cd explorer && bun test
cd explorer && bun run lint
cd explorer && bun run build
curl -I http://127.0.0.1:5174/explore
git diff --check
```

## Results

- `bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts`: 29 pass / 0 fail.
- `bun --cwd explorer test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx`: 50 pass / 0 fail.
- `cd explorer && bun test`: 76 pass / 0 fail / 350 expects.
- `cd explorer && bun run lint`: pass.
- `cd explorer && bun run build`: pass; existing vis-network chunk-size warning remains.
- `git diff --check`: pass.
- Vite smoke: `curl -I http://127.0.0.1:5174/explore` returned HTTP 200 from a local dev server.
- GitNexus CLI evidence: attempted `npx gitnexus detect-changes`; the npm exec probe hung without output and was killed. OMX code-intel transport was also unavailable earlier, so final impact evidence is diff/test/build/verifier based.
- Verifier first pass returned PARTIAL because a timeout reveal could expose an unfinished large graph and reused graph loads skipped hidden stabilization; both issues were fixed and verification rerun.

## Safety invariants

- API routes changed: no.
- Taxonomy or protected content changed: no.
- Neo4j/KG mutation changed: no.
- Explorer default graph cutover changed: no.
- Runtime threshold claims changed: no.

## Evidence artifacts

- Packet: `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_explorer_no_startup_animation_optimization_packet.md`
- Report: `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260429T000000Z/no-startup-animation-report.json`
- Team shutdown report: `.omx/reports/team-commit-hygiene/read-only-explorer-large-graph.md`

## Residual risks

- Browser-perceived startup depends on vis-network delivering `stabilizationIterationsDone` or `stabilized`; both events now reveal the canvas only after the stabilization cycle reports completion.
- Build still emits the pre-existing large dynamic `vis-network` chunk warning.

## Final status

Implementation is verified. Architect/verifier second pass approved after the timeout reveal and reused-load gaps were fixed. Final commit, push, and post-commit git status are recorded in the final response.
