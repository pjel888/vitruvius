import { forwardRef, useImperativeHandle, useRef, useEffect } from 'react';
import { Network, DataSet } from 'vis-network/standalone';
import type { GraphNode, GraphEdge } from '../../types';

export interface GraphController {
  loadPerspective: (nodes: GraphNode[], edges: GraphEdge[]) => void;
  selectNode: (id: string | null) => void;
  fitView: () => void;
  zoomIn: () => void;
  zoomOut: () => void;
  setLayout: (type: 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time') => void;
  setFilters: (nodeTypes: Set<string>, edgeTypes: Set<string>) => void;
  setColorScheme: (scheme: string) => void;
  setSizeBy: (metric: 'uniform' | 'confidence' | 'degree') => void;
}

const COLOR_SCHEMES: Record<string, Record<string, string>> = {
  default: {
    taxonomy: '#60a5fa', topic: '#818cf8', subtopic: '#c084fc', concept: '#a78bfa',
    rule: '#f87171', definition: '#34d399', procedure: '#fbbf24', exception: '#f472b6',
  },
  pastel: {
    taxonomy: '#93c5fd', topic: '#a5b4fc', subtopic: '#d8b4fe', concept: '#c4b5fd',
    rule: '#fca5a5', definition: '#6ee7b7', procedure: '#fcd34d', exception: '#f9a8d4',
  },
  vibrant: {
    taxonomy: '#3b82f6', topic: '#6366f1', subtopic: '#a855f7', concept: '#8b5cf6',
    rule: '#ef4444', definition: '#10b981', procedure: '#f59e0b', exception: '#ec4899',
  },
  monochrome: {
    taxonomy: '#e2e8f0', topic: '#cbd5e1', subtopic: '#94a3b8', concept: '#64748b',
    rule: '#475569', definition: '#334155', procedure: '#1e293b', exception: '#0f172a',
  },
};

function getNodeColor(schemeName: string, nodeType: string) {
  const scheme = COLOR_SCHEMES[schemeName] || COLOR_SCHEMES.default;
  return scheme[nodeType] || '#a78bfa';
}

const VisNetworkHost = forwardRef<GraphController>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const nodesRef = useRef<DataSet<any> | null>(null);
  const edgesRef = useRef<DataSet<any> | null>(null);
  const rawNodesRef = useRef<GraphNode[]>([]);
  const rawEdgesRef = useRef<GraphEdge[]>([]);
  const scaleRef = useRef(1);
  const colorSchemeRef = useRef('default');
  const sizeByRef = useRef<'uniform' | 'confidence' | 'degree'>('uniform');
  const degreeMapRef = useRef<Map<string, number>>(new Map());
  const hoveredNodeRef = useRef<string | null>(null);

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
        border: '#ffffff',
        highlight: { background: color, border: '#ffffff' },
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
      // Reset all to normal
      const updates = rawNodesRef.current.map(n => ({
        id: n.id,
        color: {
          background: getNodeColor(colorSchemeRef.current, n.type),
          border: '#ffffff',
          highlight: { background: getNodeColor(colorSchemeRef.current, n.type), border: '#ffffff' },
        },
      }));
      nodesRef.current.update(updates);
      return;
    }
    const connected = new Set(net.getConnectedNodes(hovered) as string[]);
    connected.add(hovered);
    const updates = rawNodesRef.current.map(n => {
      const isActive = connected.has(n.id);
      const baseColor = getNodeColor(colorSchemeRef.current, n.type);
      return {
        id: n.id,
        color: {
          background: isActive ? baseColor : '#334155',
          border: isActive ? '#ffffff' : '#475569',
          highlight: { background: baseColor, border: '#ffffff' },
        },
      };
    });
    nodesRef.current.update(updates);
  }

  useImperativeHandle(ref, () => ({
    loadPerspective(nodes, edges) {
      if (!containerRef.current) return;

      // Deduplicate
      const nodeMap = new Map<string, GraphNode>();
      nodes.forEach(n => { if (!nodeMap.has(n.id)) nodeMap.set(n.id, n); });
      const uniqueNodes = Array.from(nodeMap.values());
      rawNodesRef.current = uniqueNodes;

      const edgeMap = new Map<string, GraphEdge>();
      edges.forEach(e => {
        const key = e.id || `${e.source}-${e.type}-${e.target}`;
        if (!edgeMap.has(key)) edgeMap.set(key, e);
      });
      const uniqueEdges = Array.from(edgeMap.values());
      rawEdgesRef.current = uniqueEdges;

      // Compute degrees
      const degMap = new Map<string, number>();
      uniqueNodes.forEach(n => degMap.set(n.id, 0));
      uniqueEdges.forEach(e => {
        degMap.set(e.source, (degMap.get(e.source) ?? 0) + 1);
        degMap.set(e.target, (degMap.get(e.target) ?? 0) + 1);
      });
      degreeMapRef.current = degMap;

      const visNodes = uniqueNodes.map(buildVisNode);
      const visEdges = uniqueEdges.map((e, i) => ({
        id: `edge-${i}`,
        from: e.source,
        to: e.target,
        label: e.type,
        arrows: 'to',
        color: { color: '#94a3b8', opacity: 0.6 },
        font: { color: '#7a7f8a', size: 10 },
      }));

      if (networkRef.current && nodesRef.current && edgesRef.current) {
        nodesRef.current.clear();
        nodesRef.current.add(visNodes);
        edgesRef.current.clear();
        edgesRef.current.add(visEdges);
      } else {
        nodesRef.current = new DataSet(visNodes);
        edgesRef.current = new DataSet(visEdges as any);

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
        });

        networkRef.current.on('hoverNode', (params: any) => {
          hoveredNodeRef.current = params.node;
          applyHover();
        });

        networkRef.current.on('blurNode', () => {
          hoveredNodeRef.current = null;
          applyHover();
        });
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
      networkRef.current?.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
    },

    zoomIn() {
      if (!networkRef.current) return;
      scaleRef.current *= 1.5;
      networkRef.current.moveTo({ scale: scaleRef.current, animation: { duration: 200, easingFunction: 'easeInOutQuad' } });
    },

    zoomOut() {
      if (!networkRef.current) return;
      scaleRef.current /= 1.5;
      networkRef.current.moveTo({ scale: scaleRef.current, animation: { duration: 200, easingFunction: 'easeInOutQuad' } });
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
      if (!nodesRef.current || !edgesRef.current) return;

      // Save current positions before clearing
      const positions = new Map<string, { x?: number; y?: number }>();
      nodesRef.current.forEach((n: any) => {
        positions.set(n.id, { x: n.x, y: n.y });
      });

      // Rebuild visible nodes with preserved positions
      const visibleNodes = rawNodesRef.current
        .filter(n => nodeTypes.has(n.type))
        .map(n => {
          const pos = positions.get(n.id);
          return { ...buildVisNode(n), x: pos?.x, y: pos?.y };
        });

      // Rebuild visible edges
      const visibleNodeIds = new Set(visibleNodes.map((n: any) => n.id));
      const visibleEdges = rawEdgesRef.current
        .filter(e => edgeTypes.has(e.type) && visibleNodeIds.has(e.source) && visibleNodeIds.has(e.target))
        .map((e, i) => ({
          id: `edge-${i}`,
          from: e.source,
          to: e.target,
          label: e.type,
          arrows: 'to',
          color: { color: '#94a3b8', opacity: 0.6 },
          font: { color: '#7a7f8a', size: 10 },
        }));

      nodesRef.current.clear();
      nodesRef.current.add(visibleNodes);
      edgesRef.current.clear();
      edgesRef.current.add(visibleEdges);
    },

    setColorScheme(scheme) {
      colorSchemeRef.current = scheme;
      if (!nodesRef.current) return;
      const updates = rawNodesRef.current.map(n => {
        const color = getNodeColor(scheme, n.type);
        return {
          id: n.id,
          color: {
            background: color,
            border: '#ffffff',
            highlight: { background: color, border: '#ffffff' },
          },
        };
      });
      nodesRef.current.update(updates);
    },

    setSizeBy(metric) {
      sizeByRef.current = metric;
      if (!nodesRef.current) return;
      const updates = rawNodesRef.current.map(n => {
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
  }));

  useEffect(() => {
    return () => {
      networkRef.current?.destroy();
      networkRef.current = null;
      nodesRef.current = null;
      edgesRef.current = null;
    };
  }, []);

  return <div ref={containerRef} style={{ position: 'absolute', inset: 0 }} />;
});

VisNetworkHost.displayName = 'VisNetworkHost';
export default VisNetworkHost;
