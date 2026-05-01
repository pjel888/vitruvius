# Ralph Context Snapshot: Explorer UI/UX Optimization Plan

Task statement: Create a comprehensive Explorer UI/UX improvement audit, readiness assessment, and implementation plan for a now-large AEC-MEPFS graph. Requested focus includes zoom slider, more expansive spread, pausing physics when spread changes, more spacing between nodes, and readiness for future document interrelationships.

Desired outcome:
- Repo-backed audit of current Explorer implementation.
- Online best-practice research synthesis.
- Readiness and implementation plan with concrete phased steps, acceptance criteria, tests, risks, and measurement.
- Kimi/Moonshot advisory review attempted where available.
- No broad implementation unless plan requires tiny evidence-only changes; primary deliverable is planning artifacts.

Known facts/evidence:
- Current AEC-MEPFS graph after latest expansion: 2424 nodes, 2400 edges, max depth 4.
- Explorer uses vis-network and already has physics/performance guardrails, layout spread controls, minimap, label visibility filters, resizable panels, and taxonomy tree controls.
- Recent UI work: panel resizing, label filters, bigger taxonomy, physics/drag fixes, minimap update fixes.

Constraints:
- Do not use Gemini.
- Do not print secrets/env values.
- Plan only unless clear low-risk docs/evidence updates.
- Preserve no protected content ingest / no Neo4j mutation / no KG rebuild safety boundaries.

Likely codebase touchpoints:
- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/components/graph/layoutSpread.ts`
- `explorer/src/components/graph/largeGraphPerformance.ts`
- `explorer/src/components/graph/GraphMinimap.tsx`
- `explorer/src/components/CommandBar.tsx`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/stores/useSceneStore.ts`
- Explorer tests under `explorer/src/`
