# Vitruvius Explorer Remediation Plan

**Status:** Critical — React app crashes repeatedly in development due to fundamental architecture mismatches between React lifecycle and Sigma.js imperative API.

**Date:** 2026-04-19

---

## 1. Root Cause Analysis

The current `GraphScene.tsx` violates a core React-Sigma integration rule: **Sigma.js is an imperative, stateful canvas library; React is a declarative, functional UI framework.** The current code tries to mix them without a proper isolation layer.

### 1.1 Specific Failure Modes

| Symptom | Root Cause | Why It Happens |
|---------|-----------|----------------|
| `Container has no height` | Sigma measures DOM before flex layout completes | React renders SigmaContainer before parent flex dimensions are computed |
| `Node already exists in graph` | StrictMode double-mount + `loadGraph` persisting across unmount | React mounts → unmounts → remounts; Sigma graph object survives unmount via closure/ref |
| `Edge already exists` | Same as above + non-multi graph | Graphology `addDirectedEdgeWithKey` throws if ANY edge exists between same node pair |
| `Sigma: <ForwardRef> error` | Exception during Sigma constructor leaves component in broken state | One of the above errors cascades into an unrecoverable React error boundary |

### 1.2 Architectural Flaws

1. **StrictMode incompatibility:** `main.tsx` wraps `<App />` in `<StrictMode>`. StrictMode intentionally double-invokes effects in development. Sigma.js is not designed for this — it initializes WebGL contexts, creates graphology instances, and registers event listeners that are not idempotent.

2. **Graph lifecycle inside useEffect:** The graph is created, populated, and loaded inside a `useEffect` that depends on `perspectiveId`. When the effect re-runs (perspective change OR StrictMode remount), the code tries to add nodes/edges to a graph that may already exist in Sigma's internal state.

3. **`useLoadGraph` misuse:** The `@react-sigma/core` `useLoadGraph` hook is designed to be called ONCE per Sigma instance. Calling it multiple times (on remount) causes undefined behavior.

4. **Layout hook lifecycle:** `useLayoutForceAtlas2` starts a physics simulation. On unmount, the simulation continues running in the background. On remount, a new simulation starts, creating duplicate force calculations.

5. **Monolithic component:** `GraphScene.tsx` (~450 lines) mixes data loading, graph construction, layout management, event registration, zoom controls, minimap, context menu, and multi-select state. Any change to one concern risks breaking all others.

---

## 2. Remediation Strategy

### Principle: Isolate Sigma from React lifecycle

Sigma.js must live in a **stable, long-lived component that never unmounts** during normal use. React state changes (perspective, selection, filters) should be communicated to Sigma via an **imperative API** (refs, not props/effects).

### 2.1 Phase A — Stabilize the Shell (Immediate)

**Goal:** Stop the crash loop. Get a working graph on screen.

1. **Remove StrictMode**
   - File: `explorer/src/main.tsx`
   - Action: Remove `<StrictMode>` wrapper entirely.
   - Rationale: StrictMode is valuable for detecting side-effect bugs, but Sigma.js + graphology + WebGL are fundamentally incompatible with double-mount semantics. Re-enable only after the architecture is proven stable.

2. **Create a stable Sigma mount point**
   - File: `explorer/src/components/graph/SigmaHost.tsx`
   - Pattern: A component that mounts ONCE and never unmounts. It owns the Sigma instance, the graphology graph, and the layout engine for its entire lifetime.
   - Cleanup: On actual unmount (page close/navigation away), properly kill the simulation and dispose the WebGL context.

3. **Move perspective changes OUT of useEffect**
   - Instead of destroying and recreating the graph on perspective change, **update the existing graph** by:
     - Dropping nodes/edges that are no longer in the perspective
     - Adding new nodes/edges that entered the perspective
     - Preserving positions of nodes that stayed
   - This is incremental, not destructive.

4. **Create a graph controller ref**
   - File: `explorer/src/components/graph/useGraphController.ts`
   - Exposes an imperative API:
     ```typescript
     interface GraphController {
       loadPerspective(nodes: GraphNode[], edges: GraphEdge[]): void;
       selectNode(id: string | null): void;
       expandNode(id: string): Promise<void>;
       setLayout(type: LayoutType): void;
       zoomIn(): void;
       zoomOut(): void;
       fitView(): void;
       // ... etc
     }
     ```
   - React components call these methods via `useRef`. No state changes inside Sigma's render cycle.

### 2.2 Phase B — Component Decomposition

**Goal:** Split the monolith into testable, isolated parts.

```
components/graph/
├── SigmaHost.tsx          # Stable mount point, owns Sigma instance
├── GraphController.ts     # Imperative API for graph mutations
├── GraphDataManager.ts    # Fetches from API, diffs against current graph
├── GraphEventBridge.ts    # Registers Sigma events, forwards to React
├── GraphOverlays.tsx      # Zoom controls, layout switcher, minimap toggle
├── Minimap.tsx            # Canvas-based minimap
├── ContextMenu.tsx        # Right-click menu (positioned via portal)
└── useGraphSelection.ts   # Multi-select state logic (React side)
```

**Rules:**
- Only `SigmaHost.tsx` imports from `@react-sigma/core`.
- Only `GraphController.ts` imports from `graphology`.
- All other components communicate via the controller ref.

### 2.3 Phase C — Robust Data Flow

**Goal:** Eliminate the "fetch → build graph → load → layout" crash-prone sequence.

Current broken flow:
```
perspective change
  → useEffect fires
    → fetch nodes/edges
      → create new Graph()
        → graph.addNode() x N  ← CRASH if node exists
          → graph.addEdge() x M  ← CRASH if edge exists
            → loadGraph(graph)
              → assign() layout
```

New robust flow:
```
perspective change
  → React state updates (nodes[], edges[])
    → useEffect fires (stable, once per change)
      → GraphDataManager.diff(currentGraph, newNodes, newEdges)
        → controller.addNodes(added)
        → controller.removeNodes(removed)
        → controller.addEdges(added)
        → controller.removeEdges(removed)
          → sigma.refresh()
            → layout.warmup() on new nodes only
```

**Key:** The graph object is LONG-LIVED. It is created once when SigmaHost mounts. Perspective changes mutate it incrementally.

### 2.4 Phase D — Developer Experience

**Goal:** Make the app debuggable and testable.

1. **Add React Error Boundary**
   - Wrap `<SigmaHost />` in an error boundary that shows a fallback UI instead of a blank screen.
   - Display: "Graph engine error. Refresh to retry."

2. **Add a `/debug` route**
   - Shows raw API responses
   - Shows graph statistics (node count, edge count, simulation status)
   - Allows manual API calls

3. **Unit tests for GraphDataManager**
   - Test diff logic with mock data
   - Test that duplicate nodes/edges are handled gracefully

---

## 3. Implementation Order

### Step 1: Remove StrictMode (5 min)
- Edit `main.tsx`
- Verify app launches without double-mount

### Step 2: Create SigmaHost + GraphController (2 hours)
- New file: `SigmaHost.tsx`
- New file: `GraphController.ts`
- Move all Sigma-related imports here
- Mount graph ONCE, never recreate

### Step 3: Create GraphDataManager with diff logic (1 hour)
- Compare incoming nodes/edges against current graph
- Only add/remove what changed
- Guard against duplicates at the diff level, not at the graphology level

### Step 4: Wire up perspective changes via controller (30 min)
- `ExploreView` fetches data via React Query
- Passes data to controller via ref
- No more `useLoadGraph` in render path

### Step 5: Extract overlays and context menu (30 min)
- Move zoom controls, layout switcher, minimap into `GraphOverlays.tsx`
- Move context menu into `ContextMenu.tsx`

### Step 6: Add error boundary (15 min)
- Wrap SigmaHost

### Step 7: Test all perspectives (30 min)
- Default, Concepts, Taxonomy, Regulatory
- Verify no crashes on switch

### Step 8: Commit and push (10 min)

**Total estimated time:** ~5 hours

---

## 4. Success Criteria

- [ ] App launches at `/explore` without console errors
- [ ] Switching perspectives updates the graph smoothly (no flash, no crash)
- [ ] Clicking nodes selects them and opens the inspector
- [ ] Right-click shows context menu
- [ ] Zoom controls work
- [ ] Layout switcher works
- [ ] Multi-select works
- [ ] Refreshing the page restores the same view (URL state)

---

## 5. Integration with Existing Plan

This remediation replaces **Phase 3 — Graph Scene** in the original Foundation Document. After remediation is complete, we resume with:
- Phase 4 — Trust, collaboration, and polish (evidence surfaces, save/share, etc.)

The Foundation Document's product model, API contract, and UX architecture remain valid. Only the React-Sigma integration implementation needs to be rebuilt.

---

*End of Remediation Plan.*
