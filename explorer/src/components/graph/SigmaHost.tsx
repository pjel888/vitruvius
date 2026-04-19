import { forwardRef, useImperativeHandle, useRef, useEffect } from 'react';
import Sigma from 'sigma';
import Graph from 'graphology';
import { circular } from 'graphology-layout';
import forceAtlas2 from 'graphology-layout-forceatlas2';
import type { GraphNode, GraphEdge } from '../../types';

export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  selectNode: (id: string | null) => void;
  expandNode: (id: string, neighbors: { nodes: GraphNode[]; edges: GraphEdge[] }) => void;
  setLayout: (type: 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time') => void;
  zoomIn: () => void;
  zoomOut: () => void;
  fitView: () => void;
  setFilters: (nodeTypes: Set<string>, edgeTypes: Set<string>) => void;
  setColorScheme: (scheme: string) => void;
  setSizeBy: (metric: 'uniform' | 'confidence' | 'degree') => void;
  getDebugInfo: () => Record<string, any>;
}

const COLOR_SCHEMES: Record<string, Record<string, string>> = {
  default: {
    taxonomy: '#60a5fa',
    topic: '#818cf8',
    subtopic: '#c084fc',
    concept: '#a78bfa',
    rule: '#f87171',
    definition: '#34d399',
    procedure: '#fbbf24',
    exception: '#f472b6',
  },
  pastel: {
    taxonomy: '#93c5fd',
    topic: '#a5b4fc',
    subtopic: '#d8b4fe',
    concept: '#c4b5fd',
    rule: '#fca5a5',
    definition: '#6ee7b7',
    procedure: '#fcd34d',
    exception: '#f9a8d4',
  },
  vibrant: {
    taxonomy: '#3b82f6',
    topic: '#6366f1',
    subtopic: '#a855f7',
    concept: '#8b5cf6',
    rule: '#ef4444',
    definition: '#10b981',
    procedure: '#f59e0b',
    exception: '#ec4899',
  },
  monochrome: {
    taxonomy: '#e2e8f0',
    topic: '#cbd5e1',
    subtopic: '#94a3b8',
    concept: '#64748b',
    rule: '#475569',
    definition: '#334155',
    procedure: '#1e293b',
    exception: '#0f172a',
  },
};

const EDGE_COLORS: Record<string, string> = {
  HAS_CHILD: '#94a3b8',
  BELONGS_TO: '#94a3b8',
  RELATED_TO: '#94a3b8',
  DEPENDS_ON: '#fbbf24',
  DEFINED_BY: '#34d399',
  REQUIRES: '#a78bfa',
  SUPPORTED_BY: '#94a3b8',
};

const SigmaHost = forwardRef<GraphController>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const graphRef = useRef<Graph | null>(null);
  const controllerRef = useRef<GraphController | null>(null);
  const selectedNodeRef = useRef<string | null>(null);
  const hoveredNodeRef = useRef<string | null>(null);
  const layoutTypeRef = useRef<'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time'>('forceatlas2');
  const visibleNodeTypesRef = useRef<Set<string>>(new Set());
  const visibleEdgeTypesRef = useRef<Set<string>>(new Set());
  const colorSchemeRef = useRef<string>('default');
  const sizeByRef = useRef<'uniform' | 'confidence' | 'degree'>('uniform');
  const rawNodesRef = useRef<GraphNode[]>([]);

  // Drag state
  const dragNodeRef = useRef<string | null>(null);
  const isDraggingRef = useRef(false);

  useImperativeHandle(ref, () => controllerRef.current!);

  function getNodeColor(nodeType: string) {
    const scheme = COLOR_SCHEMES[colorSchemeRef.current] || COLOR_SCHEMES.default;
    return scheme[nodeType] || '#a78bfa';
  }

  function getNodeSize(node: GraphNode, graph: Graph) {
    const base = (node.radius ?? 8) * 0.6;
    if (sizeByRef.current === 'confidence' && node.confidence != null) {
      return Math.max(3, Math.min(16, node.confidence * 12));
    }
    if (sizeByRef.current === 'degree') {
      return Math.max(3, Math.min(16, base + (graph.degree(node.id) ?? 0) * 0.8));
    }
    return base;
  }

  function applyNodeVisuals(graph: Graph) {
    graph.forEachNode((nodeId) => {
      const attrs = graph.getNodeAttributes(nodeId);
      const node = rawNodesRef.current.find(n => n.id === nodeId);
      graph.setNodeAttribute(nodeId, 'color', getNodeColor(attrs.nodeType as string));
      graph.setNodeAttribute(nodeId, 'size', getNodeSize(node as GraphNode, graph));
    });
  }

  function buildReducers(graph: Graph) {
    return {
      nodeReducer: (node: string, data: any) => {
        const hovered = hoveredNodeRef.current;
        const nodeType = data.nodeType as string;
        const hidden = !visibleNodeTypesRef.current.has(nodeType);

        if (hidden) return { ...data, hidden: true };
        if (!hovered) return data;
        if (node === hovered) return { ...data, zIndex: 1 };
        const isNeighbor = graph.hasEdge(hovered, node) || graph.hasEdge(node, hovered);
        if (isNeighbor) return data;
        return { ...data, color: '#334155', zIndex: 0 };
      },
      edgeReducer: (edge: string, data: any) => {
        const hovered = hoveredNodeRef.current;
        const edgeType = data.edgeType as string;
        const hidden = !visibleEdgeTypesRef.current.has(edgeType);
        if (hidden) return { ...data, hidden: true };

        if (!hovered) return data;
        const ext = graph.extremities(edge);
        const connected = ext[0] === hovered || ext[1] === hovered;
        if (connected) {
          return { ...data, color: '#e2e8f0', size: 4, zIndex: 1 };
        }
        // Dim unconnected edges instead of hiding them
        return { ...data, color: '#1e293b60', size: 0.5, zIndex: 0 };
      },
    };
  }

  useEffect(() => {
    if (!containerRef.current) {
      console.error('[SigmaHost] Container ref is null');
      return;
    }

    const graph = new Graph({ multi: true });
    graphRef.current = graph;

    const sigma = new Sigma(graph, containerRef.current, {
      defaultEdgeType: 'arrow',
      labelDensity: 1,
      labelGridCellSize: 40,
      labelRenderedSizeThreshold: 1,
      labelFont: 'system-ui, sans-serif',
      labelColor: { color: '#e2e8f0' },
      zIndex: true,
      enableEdgeEvents: true,
      allowInvalidContainer: true,
      // Make edges more visible by default
      defaultEdgeColor: '#94a3b8',
      minEdgeThickness: 1.5,
    });
    sigmaRef.current = sigma;

    // Drag implementation
    const container = containerRef.current;

    const onMouseDown = (e: MouseEvent) => {
      const mouseGraphCoords = sigma.viewportToGraph({ x: e.offsetX, y: e.offsetY });
      // Find nearest node within grab radius
      let nearest: string | null = null;
      let nearestDist = Infinity;
      graph.forEachNode((node, attrs) => {
        const dx = (attrs.x as number) - mouseGraphCoords.x;
        const dy = (attrs.y as number) - mouseGraphCoords.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const grabRadius = (attrs.size as number || 8) + 4;
        if (dist < grabRadius && dist < nearestDist) {
          nearest = node;
          nearestDist = dist;
        }
      });
      if (nearest) {
        dragNodeRef.current = nearest;
        isDraggingRef.current = true;
        e.preventDefault();
        e.stopPropagation();
      }
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDraggingRef.current || !dragNodeRef.current) return;
      const coords = sigma.viewportToGraph({ x: e.offsetX, y: e.offsetY });
      graph.setNodeAttribute(dragNodeRef.current, 'x', coords.x);
      graph.setNodeAttribute(dragNodeRef.current, 'y', coords.y);
      sigma.refresh({ skipIndexation: true });
    };

    const onMouseUp = () => {
      dragNodeRef.current = null;
      isDraggingRef.current = false;
    };

    container.addEventListener('mousedown', onMouseDown);
    container.addEventListener('mousemove', onMouseMove);
    container.addEventListener('mouseup', onMouseUp);
    container.addEventListener('mouseleave', onMouseUp);

    // Expose controller API
    const controller: GraphController = {
      loadPerspective(nodes, edges) {
        if (!graphRef.current) return;
        const g = graphRef.current;
        rawNodesRef.current = nodes;

        console.log('[SigmaHost] loadPerspective called with', nodes.length, 'nodes,', edges.length, 'edges');

        g.clear();

        nodes.forEach((n, i) => {
          if (g.hasNode(n.id)) return;
          g.addNode(n.id, {
            label: n.label,
            size: getNodeSize(n, g),
            color: getNodeColor(n.type),
            nodeType: n.type,
            taxonomyPath: n.taxonomy_path || [],
            createdAt: n.createdAt,
            x: Math.cos((i / Math.max(nodes.length, 1)) * Math.PI * 2) * 200,
            y: Math.sin((i / Math.max(nodes.length, 1)) * Math.PI * 2) * 200,
          });
        });

        edges.forEach((e) => {
          if (!g.hasNode(e.source) || !g.hasNode(e.target)) return;
          const edgeId = e.id || `${e.source}-${e.type}-${e.target}`;
          if (g.hasEdge(edgeId)) return;
          g.addDirectedEdgeWithKey(edgeId, e.source, e.target, {
            size: 2.5,
            color: EDGE_COLORS[e.type] || '#94a3b8',
            edgeType: e.type,
          });
        });

        console.log('[SigmaHost] Graph now has', g.nodes().length, 'nodes,', g.edges().length, 'edges');

        controller.setLayout(layoutTypeRef.current);
        sigmaRef.current?.refresh();
        setTimeout(() => controller.fitView(), 100);
      },

      selectNode(id) {
        selectedNodeRef.current = id;
        if (!graphRef.current || !sigmaRef.current) return;
        graphRef.current.forEachNode((nodeId) => {
          graphRef.current!.setNodeAttribute(nodeId, 'highlighted', nodeId === id);
        });
        sigmaRef.current.refresh();
      },

      expandNode(_id, { nodes: newNodes, edges: newEdges }) {
        if (!graphRef.current) return;
        const g = graphRef.current;
        rawNodesRef.current = [...rawNodesRef.current, ...newNodes];
        newNodes.forEach((n) => {
          if (!g.hasNode(n.id)) {
            g.addNode(n.id, {
              label: n.label,
              size: getNodeSize(n, g),
              color: getNodeColor(n.type),
              nodeType: n.type,
              taxonomyPath: n.taxonomy_path || [],
              createdAt: n.createdAt,
            });
          }
        });
        newEdges.forEach((e) => {
          if (!g.hasNode(e.source) || !g.hasNode(e.target)) return;
          const edgeId = e.id || `${e.source}-${e.type}-${e.target}`;
          if (g.hasEdge(edgeId)) return;
          g.addDirectedEdgeWithKey(edgeId, e.source, e.target, {
            size: 2.5,
            color: EDGE_COLORS[e.type] || '#94a3b8',
            edgeType: e.type,
          });
        });
        applyNodeVisuals(g);
        controller.setLayout(layoutTypeRef.current);
        sigmaRef.current?.refresh();
      },

      setLayout(type) {
        layoutTypeRef.current = type;
        if (!graphRef.current) return;
        const g = graphRef.current;
        if (type === 'circular') {
          circular.assign(g, { scale: 200 });
        } else if (type === 'random') {
          g.forEachNode((node) => {
            g.setNodeAttribute(node, 'x', (Math.random() - 0.5) * 600);
            g.setNodeAttribute(node, 'y', (Math.random() - 0.5) * 600);
          });
        } else if (type === 'forceatlas2') {
          try {
            forceAtlas2.assign(g, { iterations: 300, settings: { gravity: 0.05, scalingRatio: 10 } });
          } catch (e) {
            console.error('ForceAtlas2 failed:', e);
          }
        } else if (type === 'clustered') {
          const groups = new Map<string, string[]>();
          g.forEachNode((nodeId) => {
            const attrs = g.getNodeAttributes(nodeId);
            const path = (attrs.taxonomyPath as string[]) || [];
            const root = path[0] || 'uncategorized';
            if (!groups.has(root)) groups.set(root, []);
            groups.get(root)!.push(nodeId);
          });
          const groupKeys = [...groups.keys()];
          const groupRadius = 350;
          groupKeys.forEach((groupKey, gi) => {
            const members = groups.get(groupKey)!;
            const cx = Math.cos((gi / Math.max(groupKeys.length, 1)) * Math.PI * 2) * groupRadius;
            const cy = Math.sin((gi / Math.max(groupKeys.length, 1)) * Math.PI * 2) * groupRadius;
            members.forEach((nodeId, mi) => {
              const angle = (mi / Math.max(members.length, 1)) * Math.PI * 2;
              g.setNodeAttribute(nodeId, 'x', cx + Math.cos(angle) * 120);
              g.setNodeAttribute(nodeId, 'y', cy + Math.sin(angle) * 120);
            });
          });
        } else if (type === 'time') {
          const nodesWithDate: { id: string; date: number }[] = [];
          g.forEachNode((nodeId) => {
            const attrs = g.getNodeAttributes(nodeId);
            const dateStr = attrs.createdAt as string | undefined;
            if (dateStr) {
              nodesWithDate.push({ id: nodeId, date: new Date(dateStr).getTime() });
            }
          });
          if (nodesWithDate.length > 1) {
            nodesWithDate.sort((a, b) => a.date - b.date);
            const min = nodesWithDate[0].date;
            const max = nodesWithDate[nodesWithDate.length - 1].date;
            const range = Math.max(max - min, 1);
            const groupMap = new Map<number, number>();
            nodesWithDate.forEach(({ id, date }) => {
              const x = ((date - min) / range) * 1200 - 600;
              const day = Math.floor(date / 86400000);
              const yOffset = (groupMap.get(day) || 0) * 35;
              groupMap.set(day, (groupMap.get(day) || 0) + 1);
              g.setNodeAttribute(id, 'x', x);
              g.setNodeAttribute(id, 'y', yOffset - 150);
            });
          }
        }
        sigmaRef.current?.refresh();
      },

      zoomIn() {
        const cam = sigmaRef.current?.getCamera();
        if (cam) cam.animate({ ratio: cam.ratio / 1.5 }, { duration: 200 });
      },

      zoomOut() {
        const cam = sigmaRef.current?.getCamera();
        if (cam) cam.animate({ ratio: cam.ratio * 1.5 }, { duration: 200 });
      },

      fitView() {
        sigmaRef.current?.getCamera().animatedReset({ duration: 600 });
      },

      setFilters(nodeTypes, edgeTypes) {
        visibleNodeTypesRef.current = nodeTypes;
        visibleEdgeTypesRef.current = edgeTypes;
        sigmaRef.current?.refresh({ skipIndexation: true });
      },

      setColorScheme(scheme) {
        colorSchemeRef.current = scheme;
        if (!graphRef.current) return;
        applyNodeVisuals(graphRef.current);
        sigmaRef.current?.refresh();
      },

      setSizeBy(metric) {
        sizeByRef.current = metric;
        if (!graphRef.current) return;
        applyNodeVisuals(graphRef.current);
        sigmaRef.current?.refresh();
      },

      getDebugInfo() {
        const canvas = containerRef.current?.querySelector('canvas');
        return {
          graphNodes: graphRef.current?.nodes().length ?? 0,
          graphEdges: graphRef.current?.edges().length ?? 0,
          sigmaExists: !!sigmaRef.current,
          containerExists: !!containerRef.current,
          canvasExists: !!canvas,
          canvasWidth: canvas?.width ?? 0,
          canvasHeight: canvas?.height ?? 0,
          containerWidth: containerRef.current?.clientWidth ?? 0,
          containerHeight: containerRef.current?.clientHeight ?? 0,
        };
      },
    };

    controllerRef.current = controller;

    // Hover events
    sigma.on('enterNode', (e) => {
      hoveredNodeRef.current = e.node;
      sigma.refresh({ skipIndexation: true });
    });
    sigma.on('leaveNode', () => {
      hoveredNodeRef.current = null;
      sigma.refresh({ skipIndexation: true });
    });

    // Click events
    sigma.on('clickNode', (e) => {
      if (e.node) controller.selectNode(e.node);
    });
    sigma.on('clickStage', () => {
      controller.selectNode(null);
    });

    // Reducers for filtering + hover
    const reducers = buildReducers(graph);
    sigma.setSetting('nodeReducer', reducers.nodeReducer);
    sigma.setSetting('edgeReducer', reducers.edgeReducer);

    console.log('[SigmaHost] Raw Sigma initialized with drag + reducers');

    return () => {
      container.removeEventListener('mousedown', onMouseDown);
      container.removeEventListener('mousemove', onMouseMove);
      container.removeEventListener('mouseup', onMouseUp);
      container.removeEventListener('mouseleave', onMouseUp);
      sigma.kill();
      sigmaRef.current = null;
      controllerRef.current = null;
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', cursor: 'grab' }}
    />
  );
});

SigmaHost.displayName = 'SigmaHost';
export default SigmaHost;
