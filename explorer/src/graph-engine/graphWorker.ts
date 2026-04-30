import { buildGraphIndex, buildVisibleSubgraph, expandNeighborhood, resolveAlias, searchGraphIndex, tracePathInIndex } from './graphIndex';
import type { GraphEdge, GraphNode } from '../types';

type WorkerRequest =
  | { id: number; type: 'load'; nodes: GraphNode[]; edges: GraphEdge[] }
  | { id: number; type: 'loadFromUrl'; url: string; expectedFingerprint: string }
  | { id: number; type: 'search'; query: string; limit?: number }
  | { id: number; type: 'alias'; alias: string }
  | { id: number; type: 'expand'; nodeId: string; depth?: number; maxEdges?: number }
  | { id: number; type: 'path'; from: string; to: string; maxHops?: number }
  | { id: number; type: 'visibleSubgraph'; rootNodeId?: string | null; depth?: number; maxNodes?: number; maxEdges?: number };

let index: ReturnType<typeof buildGraphIndex> | null = null;

self.onmessage = (event: MessageEvent<WorkerRequest>) => {
  void handleWorkerRequest(event.data);
};

async function handleWorkerRequest(request: WorkerRequest) {
  const startedAt = performance.now();
  try {
    if (request.type === 'load') {
      index = buildGraphIndex(request.nodes, request.edges);
      postMessage({ id: request.id, ok: true, data: { fingerprint: index.fingerprint }, timingMs: performance.now() - startedAt });
      return;
    }
    if (request.type === 'loadFromUrl') {
      const response = await fetch(request.url);
      if (!response.ok) throw new Error(`Graph worker load failed: HTTP ${response.status}`);
      const graph = await response.json() as { nodes: GraphNode[]; edges: GraphEdge[] };
      index = buildGraphIndex(graph.nodes, graph.edges);
      if (index.fingerprint !== request.expectedFingerprint) {
        throw new Error('Graph worker loaded a mismatched graph fingerprint');
      }
      postMessage({ id: request.id, ok: true, data: { fingerprint: index.fingerprint }, timingMs: performance.now() - startedAt });
      return;
    }
    if (!index) throw new Error('Graph index has not been loaded');
    if (request.type === 'search') {
      postMessage({ id: request.id, ok: true, data: searchGraphIndex(index, request.query, request.limit), timingMs: performance.now() - startedAt });
    } else if (request.type === 'alias') {
      postMessage({ id: request.id, ok: true, data: resolveAlias(index, request.alias), timingMs: performance.now() - startedAt });
    } else if (request.type === 'expand') {
      postMessage({ id: request.id, ok: true, data: expandNeighborhood(index, request.nodeId, request.depth, request.maxEdges), timingMs: performance.now() - startedAt });
    } else if (request.type === 'path') {
      postMessage({ id: request.id, ok: true, data: tracePathInIndex(index, request.from, request.to, request.maxHops), timingMs: performance.now() - startedAt });
    } else if (request.type === 'visibleSubgraph') {
      postMessage({ id: request.id, ok: true, data: buildVisibleSubgraph(index, request), timingMs: performance.now() - startedAt });
    }
  } catch (error) {
    postMessage({ id: request.id, ok: false, error: error instanceof Error ? error.message : String(error), timingMs: performance.now() - startedAt });
  }
}
