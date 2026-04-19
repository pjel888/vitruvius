# Explorer Graph Rendering — Implementation Plan

**Status**: Awaiting user approval
**Scope**: Fix the graph renderer. Preserve all UI (CommandBar, ExplorerRail, InspectorRail, BottomDrawer).
**Constraint**: One change at a time. Verify in browser after each step.

---

## DECISION: Switch to vis-network

After auditing both the broken Sigma.js integration and the working legacy HTML, the decision is to **replace Sigma.js with vis-network**.

**Rationale**:
- The legacy HTML uses vis-network and works perfectly.
- vis-network is Canvas-based (no WebGL shader crashes).
- vis-network has built-in dragging, physics, hover, zoom, pan.
- Our graph size (205 nodes) is well within vis-network's comfortable range.
- The React integration is simpler: mount vis-network in a `useEffect`, update via `DataSet`.
- Eliminates the entire class of Sigma.js attribute collision bugs.

**Trade-off**: Slightly lower performance for 1000+ nodes. Not relevant for our use case.

---

## PHASE 1: STRIP & VERIFY (30 min)

### Step 1.1: Remove Sigma packages, add vis-network

```bash
cd explorer
bun remove sigma @react-sigma/core @react-sigma/layout-forceatlas2 graphology-layout-forceatlas2
bun add vis-network react-vis-network-graph
# Keep: graphology, graphology-layout (may use for layout calculations)
```

**Verification**: `package.json` should list `vis-network` and `react-vis-network-graph`.

### Step 1.2: Create minimal VisNetworkHost component

Create `explorer/src/components/graph/VisNetworkHost.tsx`:

```typescript
import { forwardRef, useImperativeHandle, useRef, useEffect } from 'react';
import { Network, DataSet } from 'vis-network/standalone';
import type { GraphNode, GraphEdge } from '../../types';

export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  selectNode: (id: string | null) => void;
  fitView: () => void;
}

const NODE_COLORS: Record<string, string> = {
  taxonomy: '#60a5fa',
  topic: '#818cf8',
  subtopic: '#c084fc',
  concept: '#a78bfa',
  rule: '#f87171',
  definition: '#34d399',
  procedure: '#fbbf24',
  exception: '#f472b6',
};

const VisNetworkHost = forwardRef<GraphController>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);

  useImperativeHandle(ref, () => ({
    loadPerspective(nodes, edges) {
      if (!containerRef.current) return;

      const visNodes = new DataSet(
        nodes.map((n, i) => ({
          id: n.id,
          label: n.label,
          color: NODE_COLORS[n.type] || '#a78bfa',
          size: n.radius ?? 8,
          group: n.type,
          title: `${n.type}: ${n.label}`,
        }))
      );

      const visEdges = new DataSet(
        edges.map((e) => ({
          from: e.source,
          to: e.target,
          label: e.type,
          arrows: 'to',
          color: { color: '#94a3b8', opacity: 0.6 },
        }))
      );

      if (networkRef.current) {
        networkRef.current.setData({ nodes: visNodes, edges: visEdges });
      } else {
        networkRef.current = new Network(
          containerRef.current,
          { nodes: visNodes, edges: visEdges },
          {
            nodes: {
              shape: 'dot',
              font: { size: 12, color: '#e2e8f0' },
              borderWidth: 2,
            },
            edges: {
              width: 1,
              smooth: { type: 'continuous' },
            },
            physics: {
              forceAtlas2Based: {
                gravitationalConstant: -50,
                centralGravity: 0.01,
                springLength: 100,
                springConstant: 0.08,
              },
              solver: 'forceAtlas2Based',
              stabilization: { iterations: 150 },
            },
            interaction: {
              hover: true,
              tooltipDelay: 200,
            },
          }
        );
      }
    },
    selectNode(id) {
      if (id && networkRef.current) {
        networkRef.current.selectNodes([id]);
      } else if (networkRef.current) {
        networkRef.current.unselectAll();
      }
    },
    fitView() {
      networkRef.current?.fit({ animation: true });
    },
  }));

  useEffect(() => {
    return () => {
      networkRef.current?.destroy();
      networkRef.current = null;
    };
  }, []);

  return <div ref={containerRef} style={{ position: 'absolute', inset: 0 }} />;
});

VisNetworkHost.displayName = 'VisNetworkHost';
export default VisNetworkHost;
```

**Verification**: `bun run build` passes.

### Step 1.3: Wire VisNetworkHost into GraphScene

Replace `SigmaHost` import with `VisNetworkHost` in `GraphScene.tsx`.

Update `GraphController` interface references.

Remove all Sigma-specific overlays (zoom buttons, layout switcher, debug overlay) temporarily.

Keep only: `<VisNetworkHost ref={controllerRef} />` + loading overlay.

**Verification**: Refresh browser. Graph should render with nodes and edges. Physics should run automatically. Dragging should work. Zoom/pan should work.

**STOP HERE IF BROKEN. Do not proceed.**

---

## PHASE 2: RESTORE UI OVERLAYS (20 min)

### Step 2.1: Add zoom controls back

vis-network has `network.moveTo()` and `network.fit()` methods.

Add zoom in/out buttons that call:
- `network.moveTo({ scale: currentScale * 1.5 })`
- `network.moveTo({ scale: currentScale / 1.5 })`

### Step 2.2: Add layout switcher back

vis-network physics can be toggled:
- **ForceAtlas2**: `network.setOptions({ physics: { enabled: true } })`
- **Circular**: Disable physics, manually position nodes in a circle using `network.moveNode()`
- **Random**: Disable physics, random positions
- **Clustered**: Disable physics, group by taxonomy path
- **Time**: Disable physics, x-axis by createdAt

**Verification**: Each layout button works. Nodes reposition.

### Step 2.3: Remove debug overlay

Once graph is stable, delete the debug overlay div from GraphScene.

---

## PHASE 3: RESTORE ADVANCED FEATURES (30 min)

### Step 3.1: Node/edge filters

vis-network `DataSet` supports filtering:

```typescript
const allNodes = new DataSet([...]);
const allEdges = new DataSet([...]);

function applyFilters(visibleNodeTypes, visibleEdgeTypes) {
  const filteredNodes = allNodes.get({ filter: n => visibleNodeTypes.has(n.group) });
  const nodeIds = new Set(filteredNodes.map(n => n.id));
  const filteredEdges = allEdges.get({ filter: e => 
    visibleEdgeTypes.has(e.label) && nodeIds.has(e.from) && nodeIds.has(e.to)
  });
  network.setData({ nodes: filteredNodes, edges: filteredEdges });
}
```

**Verification**: Toggle filters in ExplorerRail. Graph updates instantly.

### Step 3.2: Color schemes

Update `NODE_COLORS` map, call `network.setOptions({ nodes: { color: {...} } })` or update each node in DataSet.

**Verification**: Switch color schemes. Nodes change color.

### Step 3.3: Size scaling

Update node `size` attribute in DataSet based on confidence or degree.

**Verification**: Switch size metrics. Nodes resize.

### Step 3.4: Hover interactions

vis-network has built-in hover (`interaction: { hover: true }`).

For custom hover (dim non-connected nodes), use `network.on('hoverNode', ...)`:

```typescript
network.on('hoverNode', (params) => {
  const connected = network.getConnectedNodes(params.node);
  const allNodes = nodesDataSet.get();
  const updates = allNodes.map(n => ({
    id: n.id,
    color: n.id === params.node || connected.includes(n.id)
      ? NODE_COLORS[n.group]
      : '#334155',
  }));
  nodesDataSet.update(updates);
});

network.on('blurNode', () => {
  // Reset all colors
});
```

**Verification**: Hover over node. Connected nodes stay bright, others dim.

---

## PHASE 4: POLISH (20 min)

### Step 4.1: Fix minimap

vis-network doesn't have a built-in minimap. Options:
- Remove minimap toggle button (simplest)
- Implement custom minimap by drawing node positions on a small canvas

**Decision**: Remove minimap for now. Add back later if requested.

### Step 4.2: Context menu

vis-network supports right-click via `network.on('oncontext', ...)`.

Restore context menu with "Select node", "Expand neighbors", "Fit to view".

### Step 4.3: Node selection → InspectorRail

vis-network `click` event: `network.on('click', (params) => { ... })`.

Call `setSelectedNode(params.nodes[0])` to populate InspectorRail.

**Verification**: Click node → InspectorRail shows details.

### Step 4.4: Keyboard shortcuts

Update keyboard shortcuts in App.tsx to call vis-network methods:
- `/` or `Ctrl+K`: Focus search (already works)
- `Escape`: Clear selection + `network.unselectAll()`
- `Ctrl+B`: Toggle explorer (already works)
- `Ctrl+I`: Toggle inspector (already works)

---

## PHASE 5: CLEANUP (10 min)

### Step 5.1: Remove unused code

- Delete `SigmaHost.tsx` and `Minimap.tsx`
- Remove unused imports from `GraphScene.tsx`
- Remove `@react-sigma/*` and `sigma` from `package.json` if not already done

### Step 5.2: Add ErrorBoundary

Create `explorer/src/components/ErrorBoundary.tsx`:

```typescript
import { Component, type ReactNode } from 'react';

export class GraphErrorBoundary extends Component<
  { children: ReactNode; fallback?: ReactNode },
  { hasError: boolean }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  render() {
    if (this.state.hasError) {
      return this.props.fallback || <div className="p-4 text-red-400">Graph failed to render.</div>;
    }
    return this.props.children;
  }
}
```

Wrap `<GraphScene />` in App.tsx:

```tsx
<GraphErrorBoundary>
  <GraphScene />
</GraphErrorBoundary>
```

### Step 5.3: Re-enable StrictMode

In `main.tsx`:

```tsx
import { StrictMode } from 'react';

<StrictMode>
  <App />
</StrictMode>
```

vis-network is imperatively mounted and unmounted in `useEffect`, so StrictMode double-mount should work correctly (mount → unmount cleanup → remount).

---

## TESTING CHECKLIST

After EACH phase:
- [ ] `bun run build` passes with zero errors
- [ ] `bun run dev` starts without errors
- [ ] Browser console shows no uncaught exceptions
- [ ] Graph renders with visible nodes and edges
- [ ] Nodes can be dragged
- [ ] Canvas can be panned and zoomed
- [ ] Hover shows tooltip
- [ ] Click selects node and opens InspectorRail
- [ ] Filter toggles hide/show nodes and edges
- [ ] Layout switcher reposition nodes
- [ ] Color scheme changes node colors
- [ ] Size metric changes node sizes

---

## ESTIMATED TIMELINE

| Phase | Estimated Time | Cumulative |
|-------|---------------|------------|
| Phase 1: Strip & Verify | 30 min | 30 min |
| Phase 2: Restore UI Overlays | 20 min | 50 min |
| Phase 3: Restore Advanced Features | 30 min | 1h 20m |
| Phase 4: Polish | 20 min | 1h 40m |
| Phase 5: Cleanup | 10 min | 1h 50m |

**Total**: ~2 hours of focused, sequential work.

---

## RISK MITIGATION

| Risk | Mitigation |
|------|-----------|
| vis-network also has issues | Phase 1 is minimal — if it fails, we can revert to Sigma in <5 min |
| React 19 compatibility | vis-network has no React dependency; our wrapper is thin |
| Performance with 500+ nodes | vis-network handles 500 nodes fine; if we hit limits, we can optimize later |
| Missing Sigma-specific features | None of our features require WebGL; vis-network has equivalents |

---

## APPROVAL REQUIRED

Before proceeding, confirm:

1. **Switch to vis-network** (instead of fixing Sigma.js)?
2. **Remove minimap** for now (can add back later)?
3. **Preserve all existing UI** (CommandBar, ExplorerRail, InspectorRail, BottomDrawer)?
