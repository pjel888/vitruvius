import { forwardRef, useImperativeHandle, useRef, useEffect, useState } from 'react';
import { useSceneStore } from '../../stores/useSceneStore';
import type { GraphNode, GraphEdge } from '../../types';

// ---------------------------------------------------------------------------
// Dynamic vis-network import — code-splits the ~900 KB library into its own
// chunk so the main bundle stays lean.
// ---------------------------------------------------------------------------
let visModule: typeof import('vis-network/standalone') | null = null;
let visPromise: Promise<typeof import('vis-network/standalone')> | null = null;

function loadVisNetwork() {
  if (visModule) return Promise.resolve(visModule);
  if (visPromise) return visPromise;
  visPromise = import('vis-network/standalone').then((mod) => {
    visModule = mod;
    return mod;
  });
  return visPromise;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  applySceneView: (state: { camera: { x: number; y: number; ratio: number }; hiddenNodeIds: string[] }) => void;
  getSceneView: () => { camera: { x: number; y: number; ratio: number }; hiddenNodeIds: string[] };
  selectNode: (id: string | null) => void;
  focusNode: (id: string) => void;
  fitView: () => void;
  zoomIn: () => void;
  zoomOut: () => void;
  setLayout: (type: 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time') => void;
  setFilters: (nodeTypes: Set<string>, edgeTypes: Set<string>) => void;
  setColorScheme: (scheme: string) => void;
  setSizeBy: (metric: 'uniform' | 'confidence' | 'degree') => void;
  hideNode: (id: string) => void;
  showAll: () => void;
  focusSubgraph: (centerId: string) => void;
  mergeNodesEdges: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  highlightPath: (nodeIds: string[], edgeIds: string[]) => void;
  clearPathHighlight: () => void;
}

const COLOR_SCHEMES: Record<string, Record<string, string>> = {
  default: {
    taxonomy: '#60a5fa', topic: '#818cf8', subtopic: '#c084fc', concept: '#a78bfa',
    rule: '#f87171', definition: '#34d399', procedure: '#fbbf24', exception: '#f472b6', evidence_span: '#38bdf8',
  },
  pastel: {
    taxonomy: '#93c5fd', topic: '#a5b4fc', subtopic: '#d8b4fe', concept: '#c4b5fd',
    rule: '#fca5a5', definition: '#6ee7b7', procedure: '#fcd34d', exception: '#f9a8d4', evidence_span: '#7dd3fc',
  },
  vibrant: {
    taxonomy: '#3b82f6', topic: '#6366f1', subtopic: '#a855f7', concept: '#8b5cf6',
    rule: '#ef4444', definition: '#10b981', procedure: '#f59e0b', exception: '#ec4899', evidence_span: '#0ea5e9',
  },
  monochrome: {
    taxonomy: '#e2e8f0', topic: '#cbd5e1', subtopic: '#94a3b8', concept: '#64748b',
    rule: '#475569', definition: '#334155', procedure: '#1e293b', exception: '#0f172a', evidence_span: '#38bdf8',
  },
};

function getNodeColor(schemeName: string, nodeType: string) {
  const scheme = COLOR_SCHEMES[schemeName] || COLOR_SCHEMES.default;
  return scheme[nodeType] || '#a78bfa';
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
const VisNetworkHost = forwardRef<GraphController>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  const setCamera = useSceneStore((s) => s.setCamera);
  const setHiddenNodeIds = useSceneStore((s) => s.setHiddenNodeIds);

  // vis-network instances (typed loosely because the module is loaded dynamically)
  const networkRef = useRef<any>(null);
  const nodesRef = useRef<any>(null);
  const edgesRef = useRef<any>(null);

  const rawNodesRef = useRef<GraphNode[]>([]);
  const rawEdgesRef = useRef<GraphEdge[]>([]);
  const scaleRef = useRef(1);
  const colorSchemeRef = useRef('default');
  const sizeByRef = useRef<'uniform' | 'confidence' | 'degree'>('uniform');
  const degreeMapRef = useRef<Map<string, number>>(new Map());
  const hoveredNodeRef = useRef<string | null>(null);
  const lastNodeTypesRef = useRef<Set<string>>(new Set());
  const lastEdgeTypesRef = useRef<Set<string>>(new Set());
  const hiddenNodeIdsRef = useRef<Set<string>>(new Set());

  // Load vis-network on mount
  useEffect(() => {
    let cancelled = false;
    loadVisNetwork().then(() => {
      if (!cancelled) setReady(true);
    });
    return () => {
      cancelled = true;
      networkRef.current?.destroy();
      networkRef.current = null;
      nodesRef.current = null;
      edgesRef.current = null;
    };
  }, []);

  function buildVisNode(n: GraphNode) {
    const color = getNodeColor(colorSchemeRef.current, n.type);
    const baseSize = n.radius ?? 8;
    let size = baseSize;
    if (sizeByRef.current === 'confidence' && n.confidence != null) {
      size = Math.max(4, Math.min(18, n.confidence * 14));
    } else if (sizeByRef.current === 'degree') {
      size = Math.max(4, Math.min(18, baseSize + (degreeMapRef.current.get(n.id) ?? 0) * 0.8));
    }
    return {
      id: n.id,
      label: n.label,
      color: {
        background: color,
        border: color,
        highlight: { background: color, border: '#e2e8f0' },
      },
      size,
      group: n.type,
      title: `<b>${n.label}</b><br/>${n.type}`,
    };
  }

  function applyHover() {
    if (!nodesRef.current) return;
    const hovered = hoveredNodeRef.current;
    const net = networkRef.current;
    if (!hovered || !net) {
      const updates = rawNodesRef.current.map((n) => {
        const c = getNodeColor(colorSchemeRef.current, n.type);
        return {
          id: n.id,
          color: {
            background: c,
            border: c,
            highlight: { background: c, border: '#e2e8f0' },
          },
        };
      });
      nodesRef.current.update(updates);
      return;
    }
    const connected = new Set(net.getConnectedNodes(hovered) as string[]);
    connected.add(hovered);
    const updates = rawNodesRef.current.map((n) => {
      const isActive = connected.has(n.id);
      const baseColor = getNodeColor(colorSchemeRef.current, n.type);
      return {
        id: n.id,
        color: {
          background: isActive ? baseColor : '#334155',
          border: isActive ? baseColor : '#475569',
          highlight: { background: baseColor, border: '#e2e8f0' },
        },
      };
    });
    nodesRef.current.update(updates);
  }

  function applyNodeColors() {
    if (!nodesRef.current) return;
    const updates = rawNodesRef.current.map((n) => {
      const color = getNodeColor(colorSchemeRef.current, n.type);
      return {
        id: n.id,
        color: {
          background: color,
          border: color,
          highlight: { background: color, border: '#e2e8f0' },
        },
      };
    });
    nodesRef.current.update(updates);
  }

  function applyEdgeColors() {
    if (!edgesRef.current) return;
    const updates = rawEdgesRef.current.map((e) => ({
      id: e.id,
      color: { color: '#94a3b8', opacity: 0.6 },
    }));
    edgesRef.current.update(updates);
  }

  function applyFilters(nodeTypes: Set<string>, edgeTypes: Set<string>) {
    if (!nodesRef.current || !edgesRef.current || !networkRef.current) return;

    const visibleNodeIds = new Set(
      rawNodesRef.current.filter((n) => nodeTypes.has(n.type)).map((n) => n.id)
    );

    const nodeUpdates = rawNodesRef.current.map((n) => ({
      id: n.id,
      hidden: !visibleNodeIds.has(n.id) || hiddenNodeIdsRef.current.has(n.id),
    }));
    nodesRef.current.update(nodeUpdates);

    const edgeUpdates = rawEdgesRef.current.map((e) => ({
      id: e.id,
      hidden: !(edgeTypes.has(e.type) && visibleNodeIds.has(e.source) && visibleNodeIds.has(e.target))
        || hiddenNodeIdsRef.current.has(e.source)
        || hiddenNodeIdsRef.current.has(e.target),
    }));
    edgesRef.current.update(edgeUpdates);

    applyHover();
  }

  function syncCameraFromNetwork() {
    if (!networkRef.current) return;
    const position = networkRef.current.getViewPosition();
    setCamera({ x: position.x, y: position.y, ratio: scaleRef.current });
  }

  function loadGraph(nodes: GraphNode[], edges: GraphEdge[]) {
    const nodeMap = new Map<string, GraphNode>();
    nodes.forEach((n) => {
      if (!nodeMap.has(n.id)) nodeMap.set(n.id, n);
    });
    const uniqueNodes = Array.from(nodeMap.values());
    rawNodesRef.current = uniqueNodes;

    const edgeMap = new Map<string, GraphEdge>();
    edges.forEach((e) => {
      const key = e.id || `${e.source}-${e.type}-${e.target}`;
      if (!edgeMap.has(key)) edgeMap.set(key, e);
    });
    const uniqueEdges = Array.from(edgeMap.values());
    rawEdgesRef.current = uniqueEdges;

    if (!ready || !containerRef.current || !visModule) {
      return;
    }

    const { Network, DataSet } = visModule;

    hiddenNodeIdsRef.current.clear();

    const degMap = new Map<string, number>();
    uniqueNodes.forEach((n) => degMap.set(n.id, 0));
    uniqueEdges.forEach((e) => {
      degMap.set(e.source, (degMap.get(e.source) ?? 0) + 1);
      degMap.set(e.target, (degMap.get(e.target) ?? 0) + 1);
    });
    degreeMapRef.current = degMap;

    const visNodes = uniqueNodes.map(buildVisNode);
    const visEdges = uniqueEdges.map((e) => ({
      id: e.id,
      from: e.source,
      to: e.target,
      label: e.type,
      color: { color: '#94a3b8', opacity: 0.6 },
    }));

    if (networkRef.current && nodesRef.current && edgesRef.current) {
      nodesRef.current.clear();
      nodesRef.current.add(visNodes);
      edgesRef.current.clear();
      edgesRef.current.add(visEdges);
      return;
    }

    nodesRef.current = new DataSet(visNodes);
    edgesRef.current = new DataSet(visEdges);

    networkRef.current = new Network(
      containerRef.current,
      { nodes: nodesRef.current, edges: edgesRef.current },
      {
        nodes: {
          shape: 'dot',
          font: { size: 12, color: '#e2e8f0', face: 'system-ui, sans-serif' },
          borderWidth: 2,
          borderWidthSelected: 3,
          shadow: { enabled: true, color: 'rgba(0,0,0,0.3)', size: 8 },
        },
        edges: {
          width: 1,
          smooth: { enabled: true, type: 'continuous', roundness: 0.5 },
          font: { size: 8, color: '#7a7f8a', strokeWidth: 0, face: 'system-ui, sans-serif' },
          arrows: { to: { enabled: true, scaleFactor: 0.4 } },
        },
        physics: {
          forceAtlas2Based: {
            gravitationalConstant: -50,
            centralGravity: 0.01,
            springLength: 100,
            springConstant: 0.08,
          },
          maxVelocity: 50,
          solver: 'forceAtlas2Based',
          timestep: 0.35,
          stabilization: { iterations: 150 },
        },
        interaction: {
          hover: true,
          tooltipDelay: 200,
          hideEdgesOnDrag: false,
        },
      }
    );

    networkRef.current.on('zoom', (params: any) => {
      if (params.scale) scaleRef.current = params.scale;
      syncCameraFromNetwork();
    });

    networkRef.current.on('dragEnd', () => {
      syncCameraFromNetwork();
    });

    networkRef.current.on('stabilized', () => {
      syncCameraFromNetwork();
    });

    networkRef.current.on('hoverNode', (params: any) => {
      hoveredNodeRef.current = params.node;
      applyHover();
    });

    networkRef.current.on('blurNode', () => {
      hoveredNodeRef.current = null;
      applyHover();
    });

    networkRef.current.on('click', (params: any) => {
      const store = useSceneStore.getState();
      store.closeContextMenu();
      if (params.nodes && params.nodes.length > 0) {
        store.setSelectedNode(params.nodes[0]);
        store.openInspector();
      } else if (params.edges && params.edges.length > 0) {
        store.setSelectedNode(null);
        store.setSelectedEdge(params.edges[0]);
        store.openInspector();
      } else {
        store.setSelectedNode(null);
        store.setSelectedEdge(null);
      }
    });

    networkRef.current.on('oncontext', (params: any) => {
      params.event.preventDefault();
      const canvasPos = networkRef.current!.DOMtoCanvas(params.pointer.DOM);
      const nodeId = networkRef.current!.getNodeAt(canvasPos);
      const store = useSceneStore.getState();
      if (nodeId) {
        store.openContextMenu(String(nodeId), {
          x: params.pointer.DOM.x + (containerRef.current?.getBoundingClientRect().left ?? 0),
          y: params.pointer.DOM.y + (containerRef.current?.getBoundingClientRect().top ?? 0),
        });
      } else {
        store.closeContextMenu();
      }
    });

    syncCameraFromNetwork();
  }

  useEffect(() => {
    if (!ready || networkRef.current || rawNodesRef.current.length === 0) return;
    loadGraph(rawNodesRef.current, rawEdgesRef.current);
  }, [ready]);

  useImperativeHandle(
    ref,
    () => ({
      loadPerspective(nodes, edges) {
        loadGraph(nodes, edges);
      },

      applySceneView(state) {
        hiddenNodeIdsRef.current = new Set(state.hiddenNodeIds);
        setHiddenNodeIds(state.hiddenNodeIds);
        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);
        if (networkRef.current) {
          scaleRef.current = state.camera.ratio;
          networkRef.current.moveTo({
            position: { x: state.camera.x, y: state.camera.y },
            scale: state.camera.ratio,
            animation: false,
          });
          syncCameraFromNetwork();
        }
      },

      getSceneView() {
        syncCameraFromNetwork();
        const position = networkRef.current?.getViewPosition?.() ?? { x: 0, y: 0 };
        return {
          camera: { x: position.x, y: position.y, ratio: scaleRef.current },
          hiddenNodeIds: Array.from(hiddenNodeIdsRef.current),
        };
      },

      selectNode(id) {
        if (id && networkRef.current) {
          networkRef.current.selectNodes([id]);
        } else if (networkRef.current) {
          networkRef.current.unselectAll();
        }
      },

      focusNode(id) {
        if (!networkRef.current) return;
        networkRef.current.selectNodes([id]);
        networkRef.current.focus(id, {
          scale: 1.2,
          animation: { duration: 500, easingFunction: 'easeInOutQuad' },
        });
      },

      fitView() {
        networkRef.current?.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
        syncCameraFromNetwork();
      },

      zoomIn() {
        if (!networkRef.current) return;
        scaleRef.current *= 1.5;
        networkRef.current.moveTo({ scale: scaleRef.current, animation: { duration: 200, easingFunction: 'easeInOutQuad' } });
        syncCameraFromNetwork();
      },

      zoomOut() {
        if (!networkRef.current) return;
        scaleRef.current /= 1.5;
        networkRef.current.moveTo({ scale: scaleRef.current, animation: { duration: 200, easingFunction: 'easeInOutQuad' } });
        syncCameraFromNetwork();
      },

      setLayout(type) {
        if (!networkRef.current || !nodesRef.current) return;
        const net = networkRef.current;
        const ds = nodesRef.current;
        const nodes = rawNodesRef.current;

        if (type === 'forceatlas2') {
          net.setOptions({ physics: { enabled: true } });
          return;
        }

        net.setOptions({ physics: { enabled: false } });
        const updates: any[] = [];

        if (type === 'circular') {
          nodes.forEach((n, i) => {
            const angle = (i / Math.max(nodes.length, 1)) * Math.PI * 2;
            updates.push({ id: n.id, x: Math.cos(angle) * 300, y: Math.sin(angle) * 300 });
          });
        } else if (type === 'random') {
          nodes.forEach((n) => {
            updates.push({ id: n.id, x: (Math.random() - 0.5) * 800, y: (Math.random() - 0.5) * 800 });
          });
        } else if (type === 'clustered') {
          const groups = new Map<string, GraphNode[]>();
          nodes.forEach((n) => {
            const root = n.taxonomy_path?.[0] || 'uncategorized';
            if (!groups.has(root)) groups.set(root, []);
            groups.get(root)!.push(n);
          });
          const groupKeys = [...groups.keys()];
          const groupRadius = 400;
          groupKeys.forEach((groupKey, gi) => {
            const members = groups.get(groupKey)!;
            const cx = Math.cos((gi / Math.max(groupKeys.length, 1)) * Math.PI * 2) * groupRadius;
            const cy = Math.sin((gi / Math.max(groupKeys.length, 1)) * Math.PI * 2) * groupRadius;
            members.forEach((n, mi) => {
              const angle = (mi / Math.max(members.length, 1)) * Math.PI * 2;
              updates.push({ id: n.id, x: cx + Math.cos(angle) * 140, y: cy + Math.sin(angle) * 140 });
            });
          });
        } else if (type === 'time') {
          const nodesWithDate: { id: string; date: number }[] = [];
          nodes.forEach((n) => {
            if (n.createdAt) nodesWithDate.push({ id: n.id, date: new Date(n.createdAt).getTime() });
          });
          if (nodesWithDate.length > 1) {
            nodesWithDate.sort((a, b) => a.date - b.date);
            const min = nodesWithDate[0].date;
            const max = nodesWithDate[nodesWithDate.length - 1].date;
            const range = Math.max(max - min, 1);
            const dayMap = new Map<number, number>();
            nodesWithDate.forEach(({ id, date }) => {
              const x = ((date - min) / range) * 1400 - 700;
              const day = Math.floor(date / 86400000);
              const yOffset = (dayMap.get(day) || 0) * 40;
              dayMap.set(day, (dayMap.get(day) || 0) + 1);
              updates.push({ id, x, y: yOffset - 200 });
            });
          }
          let noDateY = 0;
          nodes.forEach((n) => {
            if (!n.createdAt) {
              updates.push({ id: n.id, x: 0, y: noDateY });
              noDateY += 40;
            }
          });
        }

        if (updates.length > 0) {
          ds.update(updates);
          net.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
        }
      },

      setFilters(nodeTypes, edgeTypes) {
        lastNodeTypesRef.current = nodeTypes;
        lastEdgeTypesRef.current = edgeTypes;
        applyFilters(nodeTypes, edgeTypes);
      },

      setColorScheme(scheme) {
        colorSchemeRef.current = scheme;
        applyNodeColors();
      },

      setSizeBy(metric) {
        sizeByRef.current = metric;
        if (!nodesRef.current) return;
        const updates = rawNodesRef.current.map((n) => {
          const baseSize = n.radius ?? 8;
          let size = baseSize;
          if (metric === 'confidence' && n.confidence != null) {
            size = Math.max(4, Math.min(18, n.confidence * 14));
          } else if (metric === 'degree') {
            size = Math.max(4, Math.min(18, baseSize + (degreeMapRef.current.get(n.id) ?? 0) * 0.8));
          }
          return { id: n.id, size };
        });
        nodesRef.current.update(updates);
      },

      hideNode(id) {
        hiddenNodeIdsRef.current.add(id);
        setHiddenNodeIds(Array.from(hiddenNodeIdsRef.current));
        if (!nodesRef.current || !edgesRef.current) return;
        nodesRef.current.update({ id, hidden: true });
        const edgeUpdates = rawEdgesRef.current
          .filter((e) => e.source === id || e.target === id)
          .map((e) => ({ id: e.id, hidden: true }));
        if (edgeUpdates.length) edgesRef.current.update(edgeUpdates);
      },

      showAll() {
        hiddenNodeIdsRef.current.clear();
        setHiddenNodeIds([]);
        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);
      },

      focusSubgraph(centerId) {
        if (!networkRef.current || !nodesRef.current || !edgesRef.current) return;
        const connected = new Set(networkRef.current.getConnectedNodes(centerId) as string[]);
        connected.add(centerId);
        const nodeUpdates = rawNodesRef.current.map((n) => ({
          id: n.id,
          hidden: !connected.has(n.id),
        }));
        hiddenNodeIdsRef.current = new Set(rawNodesRef.current.filter((n) => !connected.has(n.id)).map((n) => n.id));
        setHiddenNodeIds(Array.from(hiddenNodeIdsRef.current));
        nodesRef.current.update(nodeUpdates);
        const edgeUpdates = rawEdgesRef.current.map((e) => ({
          id: e.id,
          hidden: !(connected.has(e.source) && connected.has(e.target)),
        }));
        edgesRef.current.update(edgeUpdates);
      },

      mergeNodesEdges(newNodes, newEdges) {
        if (!nodesRef.current || !edgesRef.current || !networkRef.current) return;

        const existingNodeIds = new Set(rawNodesRef.current.map((n) => n.id));
        const existingEdgeIds = new Set(rawEdgesRef.current.map((e) => e.id));
        const nodesToAdd = newNodes.filter((n) => !existingNodeIds.has(n.id));
        const edgesToAdd = newEdges.filter((e) => !existingEdgeIds.has(e.id));

        if (!nodesToAdd.length && !edgesToAdd.length) return;

        rawNodesRef.current = [...rawNodesRef.current, ...nodesToAdd];
        rawEdgesRef.current = [...rawEdgesRef.current, ...edgesToAdd];

        edgesToAdd.forEach((e) => {
          degreeMapRef.current.set(e.source, (degreeMapRef.current.get(e.source) ?? 0) + 1);
          degreeMapRef.current.set(e.target, (degreeMapRef.current.get(e.target) ?? 0) + 1);
        });

        const visNodes = nodesToAdd.map(buildVisNode);
        const visEdges = edgesToAdd.map((e) => ({
          id: e.id,
          from: e.source,
          to: e.target,
          label: e.type,
          color: { color: '#94a3b8', opacity: 0.6 },
        }));

        nodesRef.current.update(visNodes);
        edgesRef.current.update(visEdges);

        applyFilters(lastNodeTypesRef.current, lastEdgeTypesRef.current);

        const colorUpdates = nodesToAdd.map((n) => {
          const color = getNodeColor(colorSchemeRef.current, n.type);
          return {
            id: n.id,
            color: {
              background: color,
              border: color,
              highlight: { background: color, border: '#e2e8f0' },
            },
          };
        });
        nodesRef.current.update(colorUpdates);

        const sizeUpdates = nodesToAdd.map((n) => {
          const baseSize = n.radius ?? 8;
          let size = baseSize;
          if (sizeByRef.current === 'confidence' && n.confidence != null) {
            size = Math.max(4, Math.min(18, n.confidence * 14));
          } else if (sizeByRef.current === 'degree') {
            size = Math.max(4, Math.min(18, baseSize + (degreeMapRef.current.get(n.id) ?? 0) * 0.8));
          }
          return { id: n.id, size };
        });
        nodesRef.current.update(sizeUpdates);
        applyHover();
      },

      highlightPath(nodeIds, edgeIds) {
        if (!nodesRef.current || !edgesRef.current) return;
        const pathNodeSet = new Set(nodeIds);
        const pathEdgeSet = new Set(edgeIds);

        const nodeUpdates = rawNodesRef.current.map((n) => {
          const isPath = pathNodeSet.has(n.id);
          return {
            id: n.id,
            color: {
              background: isPath ? '#fbbf24' : getNodeColor(colorSchemeRef.current, n.type),
              border: isPath ? '#f59e0b' : getNodeColor(colorSchemeRef.current, n.type),
              highlight: { background: '#fbbf24', border: '#e2e8f0' },
            },
          };
        });
        nodesRef.current.update(nodeUpdates);

        const edgeUpdates = rawEdgesRef.current.map((e) => ({
          id: e.id,
          color: { color: pathEdgeSet.has(e.id) ? '#fbbf24' : '#334155', opacity: pathEdgeSet.has(e.id) ? 1 : 0.2 },
        }));
        edgesRef.current.update(edgeUpdates);
      },

      clearPathHighlight() {
        applyNodeColors();
        applyEdgeColors();
        applyHover();
      },
    }),
    [ready]
  );

  // While vis-network is loading, show a subtle loading indicator
  if (!ready) {
    return (
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-border border-t-accent rounded-full animate-spin" />
          <span className="text-sm text-text-dim">Loading graph engine...</span>
        </div>
      </div>
    );
  }

  return <div ref={containerRef} style={{ position: 'absolute', inset: 0 }} />;
});

VisNetworkHost.displayName = 'VisNetworkHost';
export default VisNetworkHost;
