# Explorer Network Layout Physics Restoration Context

Date: 2026-05-01

## Task statement
User observed that Explorer Network Layout now looks like the saved/precomputed backbone map and asked to restore the physics-based Network Layout bounded by the invisible force/circle feel.

## Desired outcome
Default Network Layout (`forceatlas2`) should use the physics-driven centered seed again. The deterministic precomputed/cached backbone-style layout should remain in the explicit Precomputed Layout path only. Preserve full learner-facing graph rendering and the non-visual performance wins from the prior phase.

## Known facts/evidence
- Prior full-graph optimization commit: `26b3bb16`.
- That commit made large `forceatlas2` startup use `full-graph-precomputed-startup` and disabled physics, which changed visible layout semantics.
- User says Network Layout should be the physics layout, not the saved backbone map.
- Full graph must remain default: no subgraph slicing/caps/show-more.

## Constraints
- Preserve current Explorer UX/UI except restoring expected Network Layout semantics.
- Do not hide ordinary learner-facing nodes.
- No Neo4j/live promotion, KG rebuild/reload/reset, destructive graph operations, or protected source ingestion.
- `$team` tmux runtime is unavailable in Codex App (`TMUX` unset); keep team terminal/cancelled and execute through Ralph/Ultrawork locally.

## Unknowns/open questions
- Exact visual FPS should be checked with available headless/DOM metrics; human headful manual FPS may remain not-tested unless browser automation is available.

## Likely code touchpoints
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/precomputedNetworkLayout.ts`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- Explorer performance docs/validation logs
