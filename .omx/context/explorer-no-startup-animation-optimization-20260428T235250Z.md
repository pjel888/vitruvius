# Explorer No-Startup-Animation Optimization Context

## Task statement
Implement the most effective, efficient, and optimized way for the large AEC-MEPFS Explorer graph to appear in its final layout without visible startup animation from the center.

## Desired outcome
- Large graph loads without visible node fly-out/startup settling.
- Physics should be paused or hidden during initial stabilization/precomputation.
- Preserve existing controls, spread behavior, child council layout, filters, minimap, selection opacity, and current AEC-MEPFS default graph behavior.
- Add regression tests and evidence.

## Known facts/evidence
- AEC-MEPFS graph now has 4605 nodes / 4581 edges.
- Existing Explorer tests include large graph guardrails and network layout position tests in `explorer/src/components/graph/VisNetworkHost.test.ts`.
- Prior user complaints centered on nodes disappearing, minimap updates, cramped layouts, startup animation, subtree highlighting, dimming, and edge styling.

## Constraints
- No API behavior change unless required for Explorer tests.
- No Neo4j/KG/protected-source behavior.
- Prefer small, reversible frontend changes.
- Verify with focused Explorer tests and build/lint if needed.

## Unknowns/open questions
- Current exact vis-network startup options and stabilization event handling.
- Whether existing tests already expose seed position helpers or physics settings.
- Whether a deterministic pre-layout exists and can be reused without visual hidden stabilization.

## Likely codebase touchpoints
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `explorer/src/styles.css` or component CSS if adding a loading/reveal overlay.
- `explorer/src/store/sceneStore.ts` only if a persisted/cached layout option exists or is needed.
