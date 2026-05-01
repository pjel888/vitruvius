# AEC-MEPFS-first Explorer cutover context

## Task statement
Project owner authorized moving forward from the old Explorer default graph into an AEC-MEPFS-first taxonomy/backbone experience. Implement the next practical cutover path.

## Desired outcome
Explorer should default to an AEC-MEPFS graph surface rather than legacy default graph, with safe fallback/rollback and tests/evidence. No production Neo4j mutation or protected content ingest unless separately required and safe.

## Known facts/evidence
- Prior four-lane closure is at commit 96455a3e.
- AEC-MEPFS backbone evidence is file-backed under 006_System-Manifests/aec-mepfs-backbone/.
- Existing Explorer defaults to perspective `default` / All Knowledge.
- Prior Explorer default-adoption prep intentionally kept adoption disabled.
- User says pre-launch means no need to preserve legacy default behavior as product default.

## Constraints
- Do not ingest protected content.
- Do not destructively mutate Neo4j or rebuild KG as part of this first Explorer cutover unless explicitly packeted and verified.
- Keep rollback possible through a non-default legacy route/perspective or env/setting if practical.
- Update docs/evidence and run relevant tests.

## Unknowns/open questions
- Exact shape needed to adapt AEC backbone graph into Explorer GraphNode/GraphEdge.
- Whether API can expose AEC backbone as a perspective-like graph without Neo4j.
- Which tests need updating from legacy-default assumptions.

## Likely codebase touchpoints
- api/index.ts
- explorer/src/App.tsx
- explorer/src/stores/useSceneStore.ts
- explorer/src/api/graphApi.ts
- explorer/src/components/HomeScreen.tsx
- explorer/src/app.searchInspector.integration.test.tsx
- explorer/src/api/graphApi.test.ts
- .ai/03_plans/AEC-MEPFS-Backbone/
- .ai/05_logs/
