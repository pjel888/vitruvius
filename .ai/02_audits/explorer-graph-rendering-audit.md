# Explorer Graph Rendering — Comprehensive Audit

**Date**: 2026-04-19
**Auditor**: Kimi Code CLI
**Scope**: `explorer/src/` entire React application
**Status**: Graph non-functional — blank canvas

---

## 1. FILE INVENTORY

```
explorer/src/
├── main.tsx                    # React entry point (6 lines, no StrictMode, no ErrorBoundary)
├── App.tsx                     # Router + ExploreView (132 lines)
├── index.css                   # Tailwind v4 theme + CSS variables
├── types/index.ts              # TypeScript interfaces (102 lines)
├── api/graphApi.ts             # API client (70 lines)
├── stores/useSceneStore.ts     # Zustand store (106 lines)
├── components/
│   ├── HomeScreen.tsx          # Landing page (133 lines)
│   ├── CommandBar.tsx          # Search + perspective switcher (162 lines)
│   ├── ExplorerRail.tsx        # Taxonomy tree + filters (205 lines)
│   ├── InspectorRail.tsx       # Node/edge detail panel (270 lines)
│   ├── BottomDrawer.tsx        # Source document viewer (50 lines)
│   ├── GraphScene.tsx          # Graph container + controls (213 lines)
│   └── graph/
│       ├── SigmaHost.tsx       # Sigma.js renderer (467 lines) ← BROKEN
│       └── Minimap.tsx         # Placeholder minimap (37 lines)
```

**Total**: ~1,800 lines of React/TypeScript.

---

## 2. DEPENDENCY ANALYSIS

### Graph Stack
| Package | Version | Purpose | Risk |
|---------|---------|---------|------|
| `sigma` | ^3.0.2 | WebGL graph renderer | HIGH — beta API, WebGL fragility |
| `@react-sigma/core` | ^5.0.6 | React wrapper for Sigma | HIGH — lifecycle mismatch with React 19 |
| `@react-sigma/layout-forceatlas2` | ^5.0.6 | FA2 layout for Sigma | UNUSED — we switched to raw `graphology-layout-forceatlas2` |
| `graphology` | ^0.26.0 | Graph data structure | LOW — stable |
| `graphology-layout` | ^0.6.1 | Circular/random layouts | LOW — stable |
| `graphology-layout-forceatlas2` | ^0.10.1 | FA2 layout algorithm | LOW — stable |

### React Stack
| Package | Version | Risk |
|---------|---------|------|
| `react` | ^19.2.4 | HIGH — concurrent features can double-run effects |
| `react-dom` | ^19.2.4 | HIGH — same |
| `react-router-dom` | ^7.14.1 | LOW — stable |
| `@tanstack/react-query` | ^5.99.1 | LOW — stable, but UNUSED in current code |
| `zustand` | ^5.0.12 | LOW — stable |

**Key Finding**: `react-query` is in dependencies but never used. GraphScene uses raw `fetch` + `useEffect` polling.

---

## 3. ARCHITECTURE ANALYSIS

### Data Flow

```
Neo4j → API (Hono) → graphApi.ts (fetch)
                              ↓
                    App.tsx useEffect (loads perspective)
                              ↓
                    useSceneStore (setGraphData)
                              ↓
                    GraphScene useEffect (polls for controller)
                              ↓
                    SigmaHost controller.loadPerspective()
                              ↓
                    Graphology Graph + Sigma.js WebGL
```

**Problems with this flow**:
1. **Double data storage**: Nodes/edges stored in Zustand AND in Graphology graph. Source of truth is split.
2. **Polling anti-pattern**: GraphScene polls with `setTimeout` every 100ms for up to 5 seconds waiting for SigmaHost to initialize. This is a race condition.
3. **No loading state coordination**: App.tsx sets `loading=true`, loads data, sets `loading=false`. GraphScene separately polls and calls `loadPerspective`. The loading spinner disappears before the graph is ready.

### Component Coupling

```
App.tsx
  └─ ExploreView
       ├─ CommandBar          ← reads/writes store
       ├─ ExplorerRail        ← reads/writes store
       ├─ GraphScene          ← reads store, calls controllerRef
       │    └─ SigmaHost      ← imperative API via ref
       │         └─ Minimap   ← reads controllerRef (placeholder)
       └─ InspectorRail       ← reads store, fetches API
```

**Coupling issues**:
- `GraphScene` ↔ `SigmaHost`: Tight coupling via `useRef<GraphController>`. React docs discourage imperative APIs.
- `ExplorerRail` ↔ `SigmaHost`: Filter state flows: ExplorerRail → store → GraphScene useEffect → controller.setFilters → Sigma reducer. 4 hops.
- `Minimap` → `SigmaHost`: Receives controller ref but doesn't actually use it (draws placeholder text).

---

## 4. SIGMAHOST.tsx — DETAILED FAULT ANALYSIS

### Line 152-456: Single `useEffect` with 304 lines of logic

**Critical**: All Sigma initialization, event handlers, controller creation, drag logic, and reducers live in ONE effect with `[]` deps. This means:
- The effect runs once on mount.
- All closures capture initial state.
- Refs are used to work around closure staleness, creating a fragile "ref hell".

### Drag Implementation (Lines 177-219)

```typescript
const onMouseDown = (e: MouseEvent) => {
  // ... finds nearest node ...
  e.preventDefault();
  e.stopPropagation();  // ← BREAKS SIGMA'S EVENT HANDLING
};
```

**Fault**: `stopPropagation()` on mousedown prevents Sigma's internal event system from receiving the event. Sigma may fail to initialize its interaction state, causing:
- Click detection to break
- Pan/zoom to fail
- The entire renderer to enter an undefined state

**Fault**: `onMouseDown` is attached to the container DIV, not the canvas. Sigma attaches its own listeners to the canvas. The container listener fires first, calls `stopPropagation()`, and Sigma never sees the event.

### Reducers (Lines 120-149)

```typescript
function buildReducers(graph: Graph) {
  return {
    nodeReducer: (node: string, data: any) => {
      const hovered = hoveredNodeRef.current;
      // ...
    },
    edgeReducer: (edge: string, data: any) => {
      const hovered = hoveredNodeRef.current;
      // ...
    },
  };
}
```

**Fault**: Reducers are created once during initialization and registered via `sigma.setSetting()`. Sigma v3 may not support dynamic reducer replacement. If it does, the reducer closures capture `hoveredNodeRef` which is a mutable ref — but Sigma may cache the reducer function and not re-evaluate it on refresh.

**Fault**: Returning `{ ...data, hidden: true }` from a reducer sets the `hidden` property on the rendered data. If Sigma caches this, the node/edge may stay hidden even when the reducer later returns `data` without `hidden`.

### Attribute Name Collisions (Previously Fixed, Still Risky)

Sigma v3 reserves these node attributes:
- `type` → selects WebGL node program (CRASH if unknown value)
- `hidden` → hides node
- `zIndex` → render order
- `highlighted` → selection highlight

We renamed `type` → `nodeType` and `type` → `edgeType`, but this is a manual convention with no enforcement. Future developers (or future Sigma versions) could reintroduce collisions.

### Layout Algorithms (Lines 304-367)

```typescript
} else if (type === 'forceatlas2') {
  try {
    forceAtlas2.assign(g, { iterations: 300, settings: { gravity: 0.05, scalingRatio: 10 } });
  } catch (e) {
    console.error('ForceAtlas2 failed:', e);
  }
}
```

**Fault**: `forceAtlas2.assign()` is synchronous and blocking. For 200+ nodes with 300 iterations, this could take 50-200ms, blocking the main thread. No web worker, no async yield.

**Fault**: Layout runs inside the same tick as `loadPerspective`, which runs inside a `setTimeout` poll loop. The browser may paint a partially-layouted graph or freeze.

---

## 5. THE WORKING LEGACY HTML

`vitruvius-graph.html` uses **vis-network** (not Sigma.js):

```html
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
```

**Why vis-network works**:
- Canvas-based (not WebGL) — no shader programs, no attribute collisions
- Built-in physics engine with `forceAtlas2Based` solver
- Built-in dragging, hover, tooltips, zoom, pan
- No React integration needed — plain JS imperative API
- Mature, stable, well-documented

**Why we chose Sigma.js**:
- Better performance for >1000 nodes (WebGL)
- More customizable rendering
- Modern TypeScript support

**Reality check**: We have 205 nodes. vis-network handles 205 nodes effortlessly. WebGL is overkill.

---

## 6. BLAST RADIUS ANALYSIS

### If we rewrite SigmaHost.tsx

| Affected File | Impact | Action Needed |
|---------------|--------|---------------|
| `SigmaHost.tsx` | TOTAL REWRITE | Replace entire file |
| `GraphScene.tsx` | MODERATE | Remove polling, simplify controller sync |
| `ExplorerRail.tsx` | LOW | Filter state already in store, may need wiring adjustment |
| `Minimap.tsx` | LOW | Currently placeholder, needs actual implementation |
| `api/index.ts` | NONE | No changes |
| `types/index.ts` | NONE | No changes |
| `useSceneStore.ts` | LOW | May need to add `graphReady` state |

### If we switch to vis-network

| Affected File | Impact | Action Needed |
|---------------|--------|---------------|
| `package.json` | ADD/DEP | Add `vis-network` or `vis-network-react`, remove Sigma packages |
| `SigmaHost.tsx` | TOTAL REWRITE | New component wrapping vis-network |
| `GraphScene.tsx` | MODERATE | vis-network has built-in zoom/pan controls — may remove some overlay buttons |
| `ExplorerRail.tsx` | LOW | Filter logic stays the same |
| `Minimap.tsx` | LOW | vis-network has built-in minimap? No, but easier to implement |

### If we switch to D3-force + SVG

| Affected File | Impact | Action Needed |
|---------------|--------|---------------|
| `package.json` | ADD/DEP | Add `d3-force`, `d3-zoom`, `d3-selection`; remove Sigma |
| `SigmaHost.tsx` | TOTAL REWRITE | New SVG-based renderer |
| `GraphScene.tsx` | MODERATE | Simplify overlays |
| All CSS | LOW | May need z-index adjustments for SVG vs HTML overlays |

---

## 7. ROOT CAUSE OF CURRENT BLANK PAGE

**Hypothesis 1 (Most Likely)**: The drag `stopPropagation()` on mousedown breaks Sigma's event system. Sigma enters an invalid internal state and fails to render.

**Hypothesis 2**: The `cursor: grab` CSS on the container may interfere with Sigma's canvas styling.

**Hypothesis 3**: React 19's concurrent rendering causes the `useEffect` to run, partially initialize, then be interrupted. The cleanup function kills Sigma, but the re-run doesn't reinitialize properly because `[]` deps prevent re-run.

**Hypothesis 4**: A TypeScript error or runtime exception in the bundled code (not caught by `tsc`) crashes the app. Vite's production build may tree-shake or transform differently than dev.

**Recommended diagnostic**: Run in dev mode (`bun run dev`) with browser DevTools open. Check console for uncaught exceptions. Check Elements tab for canvas presence. Check React DevTools for component tree.

---

## 8. NON-GRAPH ISSUES FOUND

1. **Unused dependency**: `@tanstack/react-query` is installed but never used.
2. **Unused import**: `GraphEdge` imported in `GraphScene.tsx` but never used.
3. **Missing ErrorBoundary**: No error boundary around SigmaHost. One graph crash kills entire app.
4. **Missing StrictMode**: Removed to fix Sigma double-mount, but this hides real React issues.
5. **Minimap is placeholder**: Always draws "Minimap" text, never actual graph overview.
6. **Context menu never opens**: No right-click handler registered on Sigma canvas.
