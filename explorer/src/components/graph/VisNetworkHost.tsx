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
  const nodesRef = useRef<DataSet<any> | null>(null);
  const edgesRef = useRef<DataSet<any> | null>(null);
  const rawNodesRef = useRef<GraphNode[]>([]);
  const scaleRef = useRef(1);

  useImperativeHandle(ref, () => ({
    loadPerspective(nodes, edges) {
      if (!containerRef.current) return;

      // Deduplicate nodes by id
      const nodeMap = new Map<string, GraphNode>();
      nodes.forEach(n => { if (!nodeMap.has(n.id)) nodeMap.set(n.id, n); });
      const uniqueNodes = Array.from(nodeMap.values());
      rawNodesRef.current = uniqueNodes;

      const visNodes = uniqueNodes.map((n) => ({
        id: n.id,
        label: n.label,
        color: {
          background: NODE_COLORS[n.type] || '#a78bfa',
          border: '#ffffff',
          highlight: { background: NODE_COLORS[n.type] || '#a78bfa', border: '#ffffff' },
        },
        size: n.radius ?? 8,
        group: n.type,
        title: `<b>${n.label}</b><br/>${n.type}`,
      }));

      // Deduplicate edges by id
      const edgeMap = new Map<string, GraphEdge>();
      edges.forEach(e => {
        const key = e.id || `${e.source}-${e.type}-${e.target}`;
        if (!edgeMap.has(key)) edgeMap.set(key, e);
      });
      const uniqueEdges = Array.from(edgeMap.values());

      const visEdges = uniqueEdges.map((e) => ({
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

        // Track scale for zoom buttons
        networkRef.current.on('zoom', (params: any) => {
          if (params.scale) scaleRef.current = params.scale;
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

      // For non-physics layouts, disable physics first
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
        // Nodes without dates: place them below
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
