---
task: graph-api-explorer-hardening
phase: meta
created: 2026-04-22
author: Hephaestus
status: COMPLETE
---

# Graph API / Explorer Hardening Validation — 2026-04-22

## Scope

Validate the bounded Graph API / explorer hardening slices that:
1. hardened scene CRUD and stale-scene recovery,
2. completed the evidence perspective contract and edge-evidence path,
3. tightened query/search behavior and interaction stubs,
4. reduced avoidable API query fanout in taxonomy and taxonomy-path hydration.

## Files validated

- `api/index.ts`
- `api/sceneStore.ts`
- `api/sceneStore.test.ts`
- `api/perspectiveContracts.test.ts`
- `api/README.md`
- `explorer/src/App.tsx`
- `explorer/src/api/graphApi.ts`
- `explorer/src/components/CommandBar.tsx`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/GraphScene.tsx`
- `explorer/src/components/HomeScreen.tsx`
- `explorer/src/components/InspectorRail.tsx`
- `explorer/src/components/graph/NodeSearch.tsx`
- `explorer/src/components/graph/QueryPanel.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/stores/useSceneStore.ts`
- `explorer/src/types/index.ts`
- `explorer/README.md`

## Validation checks

### 1. API unit tests

```bash
cd api && bun test
```

Result:
- `7 pass`
- `0 fail`

### 2. Explorer production build

```bash
cd explorer && bun run build
```

Result:
- build completed successfully
- output emitted under `explorer/dist/`

### 3. Endpoint checks

```bash
curl -s http://localhost:3000/health
curl -s http://localhost:3000/perspectives
curl -s http://localhost:3000/scenes
curl -s "http://localhost:3000/search?q=concept&perspective=default&limit=20"
curl -s http://localhost:3000/taxonomy
```

Result:
- `/health` returned connected Neo4j status
- `/perspectives` returned the Evidence Map entry
- `/scenes` returned stable scene list payloads
- `/search` returned successful concept results instead of 500
- `/taxonomy` returned the hierarchy successfully after bulk-query refactor
- taxonomy search now includes concepts, matching the documented taxonomy perspective contract
- evidence search and evidence perspective now constrain canonical nodes to `concept` plus `evidence_span`, matching the documented Evidence Map contract
- evidence search now returns `evidence_span` as the type for evidence nodes instead of collapsing them to `unknown`
- taxonomy and evidence **edge** queries are now constrained to the documented perspective node families instead of returning broader relationship sets
- perspective contract coverage now imports and verifies the live API query-builder functions rather than duplicating standalone query strings

### 4. Browser QA

Validated in the running explorer:
- fresh `/explore` load renders a canvas immediately
- `Save Scene` creates a durable `?scene=` URL
- reloading a saved scene URL restores the graph
- renaming and deleting a scene update the UI and recover cleanly
- stale/deleted `?scene=` URLs fall back to `/explore`
- query panel shows saved and recent query groups
- query assets expose delete controls
- pinning a node surfaces it in the rail
- focus 1-hop no longer behaves as a no-op
- home screen exposes the Evidence Map entry point

## Interpretation

- The Graph API / explorer lane now has durable scene storage, working scene lifecycle controls, and a bounded evidence-first path.
- The previous query/search failure mode and stale-scene failure mode were removed.
- Perspective contracts between the explorer docs and the API filters/queries are now aligned for taxonomy and evidence.
- A focused API regression test now guards the taxonomy/evidence perspective contracts.
- The validation evidence now includes the latest perspective contract regression coverage rather than only the scene-store unit tests.
- The highest-leverage performance cleanup in this lane was API-side query fanout reduction, not a Rust migration.

## Deferred follow-on

- Minimap remains intentionally deferred as a separate lane.
- API security posture for arbitrary Cypher and permissive local CORS should be treated as a separate hardening decision if this surface moves beyond trusted local use.
