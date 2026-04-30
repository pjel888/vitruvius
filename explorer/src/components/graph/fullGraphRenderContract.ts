import type { GraphEdge, GraphNode } from '../../types';

function stableHashParts(parts: Iterable<string>) {
  let hash = 2166136261;
  for (const part of parts) {
    for (let index = 0; index < part.length; index += 1) {
      hash ^= part.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    hash ^= 31;
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0).toString(36);
}

export function buildFullGraphRenderSignature(nodes: GraphNode[], edges: GraphEdge[]) {
  const nodeHash = stableHashParts(
    nodes
      .map((node) => `${node.id}:${node.type}:${node.taxonomy_path?.join('/') ?? ''}`)
      .sort(),
  );
  const edgeHash = stableHashParts(
    edges
      .map((edge) => `${edge.id}:${edge.source}>${edge.type}>${edge.target}`)
      .sort(),
  );
  return `${nodes.length}:${edges.length}:${nodeHash}:${edgeHash}`;
}

export function assertFullGraphRenderContract(inputNodeCount: number, inputEdgeCount: number, renderNodeCount: number, renderEdgeCount: number) {
  return inputNodeCount === renderNodeCount && inputEdgeCount === renderEdgeCount;
}
