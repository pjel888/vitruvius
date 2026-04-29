---
status: IMPLEMENTED_VERIFIED
scope: explorer-large-graph-startup-optimization
authority: project-owner-directed-ui-optimization
baseline_commit: 16c04dfc
runtime_surface: Explorer AEC-MEPFS file-backed graph UI
---

# Explorer No-Startup-Animation Optimization Packet

## Purpose

The AEC-MEPFS Explorer graph now contains thousands of nodes. The previous
Network Layout behavior allowed vis-network physics/stabilization to be visible
at startup, so the user could see nodes begin in a compact center and animate
outward into the large knowledge graph. This packet implements the smallest safe
UI optimization that makes the graph appear only after large-graph stabilization
has produced its settled form.

## Existing authority and sources

This implementation follows the existing Explorer UI/UX optimization artifacts:

- `.ai/13_research/2026-04-28_explorer_ui_ux_large_graph_optimization_research.md`
- `.ai/02_audits/2026-04-28_explorer_ui_ux_performance_audit.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_ui_ux_optimization_readiness_and_implementation_plan.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_explorer_ui_ux_optimization_implementation_packet.md`

Read-only OMX team findings confirmed the startup risk is constructor-time
physics/stabilization running visibly for expanded graphs while large-graph
physics is otherwise already bounded and auto-frozen.

## Allowed scope

- Explorer frontend-only rendering optimization.
- Add a guardrail helper for large initial Network Layout stabilization.
- Hide the graph canvas only while initial large-graph stabilization is running.
- Reveal the graph only after vis-network reports `stabilizationIterationsDone` or
  `stabilized`, so large-graph startup physics is not shown.
- Preserve current Network Layout physics, spread controls, minimap snapshots,
  labels, filters, selected-neighborhood emphasis, and motion controls.
- Add regression tests for the startup guardrail decision.

## Blocked scope

- No taxonomy data changes.
- No API route changes.
- No resolver/runtime threshold changes.
- No Neo4j/KG rebuild/reload/reset.
- No protected content ingest or exposure.
- No feature-flag/default-adoption changes beyond the already implemented
  Explorer AEC-MEPFS-first behavior.

## Implementation summary

- `largeGraphPerformance.ts` now exposes
  `shouldHideInitialGraphStabilization(...)`.
- `VisNetworkHost.tsx` hides only large `forceatlas2` startup stabilization,
  invokes bounded stabilization on first mount and reused large graph loads, and
  reveals only on `stabilizationIterationsDone` or `stabilized`.
- `VisNetworkHost.test.ts` covers large/small, paused/unpaused, and non-Network
  layout cases.

## Verification plan

- `git diff --check`
- `bun test src/components/graph/VisNetworkHost.test.ts`
- `bun test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx`
- `bun test`
- `bun run lint`
- `bun run build`
- diff-only safety grep for prohibited runtime/Neo4j/KG/protected-source terms

## Rollback

Git revert of the implementation commit restores prior visible startup
stabilization. No database, graph artifact, API, or protected-source state is
mutated by this packet.
