# Vitruvius Knowledge Graph Explorer

An interactive, browser-based explorer for the Vitruvius knowledge graph. It is built with React 19, TypeScript, Tailwind CSS, Vite, Bun, and vis-network.

Explorer is a presentation and investigation layer. Canonical identity, source evidence, relationship semantics, and graph materialization remain owned by the upstream pipeline and Graph API.

## Stack

| Layer | Technology |
| --- | --- |
| Runtime | Bun 1.3+ |
| Bundler | Vite 8 |
| Framework | React 19 |
| Language | TypeScript 6 |
| Styling | Tailwind CSS 4 |
| Graph renderer | vis-network 10, lazy-loaded |
| Server state | TanStack React Query |
| Local state | Zustand |
| Router | React Router 7 |
| Icons | Lucide React |

## Prerequisites

- Bun 1.3+.
- The Vitruvius Graph API available at `http://localhost:3000`, unless `VITE_API_BASE_URL` points elsewhere.
- Neo4j Community 5.26+ with the Vitruvius graph populated.
- Neo4j HTTP reachable at `http://localhost:7474` when using the full `bun run dev` wrapper.

## Quick Start

From the repository root:

```bash
cd explorer
bun install
bun run dev
```

Open the Vite URL printed by the dev server, usually `http://localhost:5173`.

`bun run dev` checks that Neo4j is reachable, starts the Graph API from the repo `api/` directory on `http://localhost:3000`, waits for `/health`, and then starts Vite.

If the API is already running separately:

```bash
cd explorer
VITE_API_BASE_URL=http://localhost:3000 bun run dev:vite
```

## Production Build

```bash
bun run build
```

Output goes to `dist/`. The API serves this folder statically at `/*` when running in production.

## Useful Commands

```bash
bun test
bun run build
bun run lint
bun run preview
```

Command expectations:

- `bun test` runs the Explorer unit and integration tests.
- `bun run build` runs TypeScript project checks and the Vite production build.
- `bun run lint` is the strictest static check and should be clean before treating lint as a release gate.
- `bun run preview` serves the production build locally after `bun run build`.

## Runtime Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `http://localhost:3000` | Browser-side base URL for Explorer API requests. |
| `NEO4J_PASS` | `password` in `scripts/dev.ts` | Password passed to the local API process by the full dev wrapper. |

Use explicit environment values for local databases that do not match the defaults.

## Architecture

```text
+-------------------------------------------------------------+
| CommandBar      search, perspective switch, actions          |
+----------+------------------------------+-------------------+
|          |                              |                   |
| Explorer |        Graph Scene           | Inspector         |
| Rail     |   vis-network canvas         | Rail              |
|          |                              |                   |
+----------+------------------------------+-------------------+
| Bottom Drawer    evidence preview and query details          |
+-------------------------------------------------------------+
```

## Project Layout

| Path | Purpose |
| --- | --- |
| `src/App.tsx` | Top-level route, perspective, and layout orchestration. |
| `src/api/graphApi.ts` | Browser client for Explorer API endpoints. |
| `src/components/CommandBar.tsx` | Perspective switcher, search, scene actions, and API status. |
| `src/components/ExplorerRail.tsx` | Taxonomy tree, type filters, and saved scenes. |
| `src/components/explorer-rail/BackbonePreviewPanel.tsx` | Opt-in AEC-MEPFS Backbone shadow summary preview. |
| `src/components/GraphScene.tsx` | Graph data loading, controller sync, and graph overlays. |
| `src/components/InspectorRail.tsx` | Node inspector, edge inspector, and path tracer. |
| `src/components/graph/VisNetworkHost.tsx` | Imperative vis-network wrapper for physics, layouts, filters, hover, and path highlighting. |
| `src/components/graph/QueryPanel.tsx` | Cypher query runner with templates and result rendering. |
| `src/stores/useSceneStore.ts` | Zustand store for selection, filters, camera, context menu, and path tracing. |
| `src/types/index.ts` | Shared Explorer API and UI types. |
| `src/utils/` | Runtime helpers and label formatting utilities. |
| `scripts/dev.ts` | Full-stack local dev launcher for API plus Vite. |

## Features

### Node Search

- Search across node labels, aliases, slugs, and IDs.
- Keyboard navigation with arrow keys, Enter, and Escape.
- 20-result cap in the command bar.
- Camera auto-focuses on the selected node.
- Search result display uses readable labels while preserving canonical node identity.

### AEC-MEPFS Shadow Preview

- The Explorer rail includes an opt-in AEC-MEPFS Backbone preview.
- The preview reads `GET /v2/backbone` and renders the compact shadow summary.
- The detail control reads `GET /v2/backbone/taxonomy` and renders sanitized
  registry-readiness metadata, staged admitted `BackboneNode` rows, and
  sanitized shadow graph counts/hierarchy edges when present.
- Separate explicit controls read `GET /v2/backbone/placement-qa` and
  `GET /v2/backbone/evidence` for compact placement-QA and evidence-manifest
  summaries.
- It does not change the active graph perspective, graph data, Neo4j state, or Explorer default view.

### Context Menu and Neighbor Expansion

- Right-click a node to expand one-hop neighbors, focus a subgraph, hide the node, or restore hidden nodes.
- Hidden nodes compose with type filters.
- New nodes and edges merge into the existing scene.

### Node and Edge Inspector

- Click a node to inspect overview, relationships, sources, and metadata.
- Click an edge to inspect relationship type, confidence, reasoning summary, and endpoint nodes.
- Edge lookup supports assertion identity and source/type/target fallback behavior exposed by the API.
- Inspector copy should keep both readable labels and canonical IDs visible.

### Cypher Query Panel

- Run custom Cypher queries against the Graph API.
- Uses backend read-only query enforcement.
- Renders tabular rows and extracts renderable graph results.
- Includes built-in examples for neighborhoods, paths, taxonomy, and evidence.

### Path Tracer

- Set source and target nodes from the node inspector.
- Find shortest paths via the Graph API.
- Highlight path nodes and edges while dimming unrelated graph elements.
- Click any hop in the result list to focus that node.

### Code Splitting

- vis-network is dynamically imported on first mount.
- The production build keeps the main bundle separate from the large vis-network chunk.

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `/` or `Ctrl+K` | Focus search. |
| `Esc` | Clear selection. |
| `Ctrl+B` | Toggle explorer rail. |
| `Ctrl+I` | Toggle inspector rail. |
| `Ctrl+Enter` | Run Cypher query when the query panel is open. |
| `+` / `-` | Zoom in or out. |
| `0` | Fit graph to view. |

## API Endpoints Consumed

Explorer talks to the Graph API BFF, not directly to Neo4j.

| Endpoint | Used by |
| --- | --- |
| `GET /health` | API and Neo4j connection indicator. |
| `GET /v2/backbone` | Opt-in AEC-MEPFS Backbone shadow preview. |
| `GET /v2/backbone/taxonomy` | Explicit registry, admitted BackboneNode, and shadow graph parity detail inside the opt-in AEC-MEPFS preview. |
| `GET /perspectives` | Perspective inventory and live counts. |
| `GET /perspective/:id/nodes` | Initial graph load. |
| `GET /search?q=...` | Node search. |
| `GET /node/:id` | Node inspector. |
| `GET /edge/:id` | Edge inspector. |
| `GET /expand?nodeId=...` | Neighbor expansion. |
| `GET /path?from=...&to=...` | Path tracer. |
| `GET /taxonomy` | Taxonomy tree. |
| `GET /scenes` | Saved scene inventory. |
| `GET /scene/:id` | Saved scene load. |
| `POST /scene/save` | Saved scene creation. |
| `PUT /scene/:id` | Saved scene update. |
| `DELETE /scene/:id` | Saved scene deletion. |
| `POST /query` | Cypher query panel. |

## API Contract Notes

Explorer expects canonical graph IDs to remain stable and uses display labels only for presentation.

- Preserve canonical `id` values for lookup, URLs, scene state, and debugging.
- Use `displayLabel` when present for readable node and edge presentation.
- Keep inspector panels capable of showing both readable labels and canonical IDs.
- Do not infer new relationship truth in the UI. Semantic enrichment belongs in the pipeline and graph materialization layer.
- Keep AEC-MEPFS Backbone preview data read-only and shadow-scoped until a separate runtime cutover plan is accepted.

## Perspectives

| ID | Name | Visible nodes | Visible edges |
| --- | --- | --- | --- |
| `default` | All Knowledge | All canonical and taxonomy nodes | All graph edges |
| `concepts` | Concepts Only | `concept`, `rule`, `definition`, `procedure`, `exception` | `RELATED_TO`, `DEPENDS_ON`, `DEFINED_BY`, `REQUIRES` |
| `taxonomy` | Taxonomy Browser | `taxonomy`, `topic`, `subtopic`, `concept` | `HAS_CHILD`, `BELONGS_TO` |
| `regulatory` | Regulatory Rules | `rule`, `concept` | `REQUIRES`, `DEPENDS_ON`, `DEFINED_BY` |
| `evidence` | Evidence Map | `concept`, `evidence_span` | `SUPPORTED_BY` |

## State Model

Scene state is URL-synced and includes:

- Camera position and zoom.
- Selected node or edge.
- Active node and edge filters.
- Expanded and hidden node sets.
- Layout engine.

Saved scenes are shareable through `?scene=<id>` URLs and persisted through the Graph API. Query assets still persist locally in the browser.

## Manual Smoke Check

After starting the app:

1. Open the Explorer home screen and verify perspectives load.
2. Select a perspective and confirm graph nodes and edges render.
3. Search for a node, select it, and inspect relationships, sources, and metadata.
4. Expand a node from the graph or inspector and verify new neighbors merge into the scene.
5. Open the query panel, run a known-safe template, and confirm rows plus graph results render.
6. Save or load a scene and confirm the URL state remains consistent.

## Known Issues

- `bun run lint` currently reports existing React hook and TypeScript lint violations in the Explorer source tree.
- `bun run build` currently passes but emits the existing Vite chunk-size warning for `vis-network`.
- `bun run dev` requires local Neo4j. Use `bun run dev:vite` when pointing the UI at an already running API.
