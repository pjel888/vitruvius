# Vitruvius Knowledge Graph Explorer

An interactive, browser-based explorer for the Vitruvius knowledge graph. Built with React 19, TypeScript, Tailwind CSS, and vis-network.

## Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Bun 1.3+ |
| Bundler | Vite 8 |
| Framework | React 19 |
| Language | TypeScript 6 |
| Styling | Tailwind CSS 4 |
| Graph Renderer | vis-network 10 (code-split, lazy-loaded) |
| State | Zustand |
| Router | React Router 6 |
| Icons | Lucide React |

## Prerequisites

- [Bun](https://bun.sh) 1.3+
- The [Vitruvius Graph API](../api/) running on `http://localhost:3000`
- Neo4j Community 5.26+ with the Vitruvius graph populated

## Quick Start

```bash
# 1. Install dependencies
bun install

# 2. Start the dev stack
bun run dev

# 3. Open http://localhost:5173
```

`bun run dev` now checks that Neo4j is reachable, starts the Graph API on `http://localhost:3000`, waits for `/health`, and then starts Vite on `http://localhost:5173`. If your API runs on a different port, update `VITE_API_BASE_URL` in `.env` or the hardcoded default in `src/api/graphApi.ts`.

## Production Build

```bash
bun run build
```

Output goes to `dist/`. The API serves this folder statically at `/*` when running in production.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CommandBar      (search, perspective switch, actions)      │
├──────────┬──────────────────────────────┬───────────────────┤
│          │                              │                   │
│ Explorer │      Graph Scene             │   Inspector       │
│  Rail    │   (vis-network canvas)       │    Rail           │
│  320px   │                              │   400px           │
│          │                              │                   │
├──────────┴──────────────────────────────┴───────────────────┤
│  Bottom Drawer  (evidence preview, query details)           │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | File | Role |
|-----------|------|------|
| `VisNetworkHost` | `src/components/graph/VisNetworkHost.tsx` | Imperative vis-network wrapper. Physics, layouts, filters, hover, path highlighting. |
| `GraphScene` | `src/components/GraphScene.tsx` | Orchestrates data loading, controller sync, and UI overlays (search, zoom, layout switcher). |
| `InspectorRail` | `src/components/InspectorRail.tsx` | Node inspector, edge inspector, path tracer. |
| `ExplorerRail` | `src/components/ExplorerRail.tsx` | Taxonomy tree, type filters, saved scenes. |
| `CommandBar` | `src/components/CommandBar.tsx` | Perspective switcher, search, status. |
| `NodeSearch` | `src/components/graph/NodeSearch.tsx` | Fuzzy node search with keyboard navigation. |
| `NodeContextMenu` | `src/components/graph/NodeContextMenu.tsx` | Right-click menu: expand neighbors, focus, hide. |
| `QueryPanel` | `src/components/graph/QueryPanel.tsx` | Cypher query runner with examples and results. |
| `useSceneStore` | `src/stores/useSceneStore.ts` | Zustand store for selection, filters, camera, context menu, path tracing. |

## Features

### Node Search (Phase 5)
- Fuzzy search across node labels, aliases, slugs, and IDs
- Keyboard navigation: ↑↓ to navigate, ↵ to select, Esc to close
- 10-result cap, grouped by match quality
- Camera auto-focuses on selected node

### Context Menu & Neighbor Expansion (Phase 6)
- Right-click any node → expand 1-hop neighbors, focus subgraph, hide node, show all
- Hidden nodes compose with type filters
- New nodes/edges merge into the existing scene via `mergeNodesEdges()`

### Edge Inspector (Phase 7)
- Click any edge to open the edge inspector
- Two-tier API lookup: `assertion_id` first, then `source|type|target` fallback
- Shows relationship type, confidence, reasoning summary, source/target nodes

### Cypher Query Panel (Phase 8)
- Run custom Cypher queries against the graph API
- Read-only session enforcement on the backend
- Recursive extraction of nodes, paths, and arrays from query results
- Examples: neighborhood, paths, taxonomy, evidence

### Path Tracer (Phase 9)
- Set source and target nodes from the node inspector
- Find shortest path via `shortestPath()` Neo4j query
- Path highlights in gold; non-path nodes/edges dim
- Click any hop in the result list to focus that node

### Code Splitting (Phase 10)
- vis-network is dynamically imported on first mount
- Main bundle: ~294 KB (was ~939 KB)
- vis-network chunk: ~650 KB, lazy-loaded

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `/` or `Ctrl+K` | Focus search |
| `Esc` | Clear selection |
| `Ctrl+B` | Toggle explorer rail |
| `Ctrl+I` | Toggle inspector rail |
| `Ctrl+Enter` | Run Cypher query (when panel open) |
| `+` / `-` | Zoom in / out |
| `0` | Fit to view |

## API Endpoints Consumed

The explorer talks to the Graph API BFF (not directly to Neo4j):

| Endpoint | Used By |
|----------|---------|
| `GET /perspective/:id/nodes` | Initial graph load |
| `GET /search?q=...` | Node search |
| `GET /node/:id` | Node inspector |
| `GET /edge/:id` | Edge inspector |
| `GET /expand?nodeId=...` | Neighbor expansion |
| `GET /path?from=...&to=...` | Path tracer |
| `GET /taxonomy` | Taxonomy tree |
| `POST /query` | Cypher query panel |
| `GET /health` | Status indicator |

## Perspectives

| ID | Name | Visible Nodes | Visible Edges |
|----|------|---------------|---------------|
| `default` | All Knowledge | All canonical + taxonomy | All graph edges |
| `concepts` | Concepts Only | concept, rule, definition, procedure, exception | RELATED_TO, DEPENDS_ON, DEFINED_BY, REQUIRES |
| `taxonomy` | Taxonomy Browser | taxonomy, topic, subtopic, concept | HAS_CHILD, BELONGS_TO |
| `regulatory` | Regulatory Rules | rule, concept | REQUIRES, DEPENDS_ON, DEFINED_BY |
| `evidence` | Evidence Map | concept, evidence_span | SUPPORTED_BY |

## State Model

Scene state is URL-synced (`?perspective=concepts&node=concept-floor-area`) and includes:
- Camera position and zoom
- Selected node/edge
- Active filters (node types, edge types)
- Expanded/hidden node sets
- Layout engine

Saved scenes are now shareable through `?scene=<id>` URLs and persisted through the Graph API. Query assets still persist locally in the browser.
