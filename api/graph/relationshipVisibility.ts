export type GraphNodeLike = {
  id: string;
  label?: string;
  displayLabel?: string;
  type?: string;
  aliases?: string[];
  taxonomy_path?: string[];
};

export type GraphEdgeLike = {
  id: string;
  source: string;
  target: string;
  type: string;
  relationType?: string;
  relationCategory?: string;
  relationNature?: string[];
  direction?: string;
  edgeDirection?: string;
  semanticOverlayCategory?: string;
  reviewStatus?: string;
  rationale?: string;
  provenanceNote?: string;
  sourceFamilyIds?: string[];
};

export type RelationshipCategory = 'hierarchy' | 'semantic';

export type NormalizedGraphRelationship = {
  id: string;
  sourceNodeId: string;
  targetNodeId: string;
  relationType: string;
  direction: 'incoming' | 'outgoing' | 'self' | 'undirected';
  label: string;
  category: RelationshipCategory;
  isHierarchyEdge: boolean;
  isSemanticEdge: boolean;
  sourceNode?: GraphNodeLike;
  targetNode?: GraphNodeLike;
  original: GraphEdgeLike;
};

export type NeighborhoodOptions = {
  depth?: number;
  limit?: number;
  direction?: 'in' | 'out' | 'both';
  relTypes?: string[];
  includeHierarchyEdges?: boolean;
  includeSemanticEdges?: boolean;
};

export type NeighborhoodIndex = {
  nodeById: Map<string, GraphNodeLike>;
  edgeById: Map<string, GraphEdgeLike>;
  incomingByNodeId: Map<string, GraphEdgeLike[]>;
  outgoingByNodeId: Map<string, GraphEdgeLike[]>;
  undirectedByNodeId: Map<string, GraphEdgeLike[]>;
};

export type RelationshipValidationIssue = {
  code: string;
  message: string;
  edgeId?: string;
  nodeId?: string;
};

export type DuplicateCanonicalCandidate = {
  normalizedLabel: string;
  nodeIds: string[];
  labels: string[];
  taxonomyPaths: string[][];
  types: string[];
  safeToAutoMerge: boolean;
  reason: string;
};

const HIERARCHY_EDGE_TYPES = new Set(['HAS_CHILD', 'BELONGS_TO']);
const CONTEXTUAL_HIERARCHY_TYPES = new Set(['PART_OF']);

export function normalizeCanonicalLabel(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[’']/g, '')
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function singularizeSimple(value: string) {
  return value
    .split(' ')
    .map((part) => {
      if (part.length <= 3) return part;
      if (part.endsWith('ies')) return `${part.slice(0, -3)}y`;
      if (part.endsWith('s') && !part.endsWith('ss')) return part.slice(0, -1);
      return part;
    })
    .join(' ');
}

export function normalizeCanonicalLabelLoose(value: string) {
  return singularizeSimple(normalizeCanonicalLabel(value));
}

export function classifyGraphEdge(edge: Pick<GraphEdgeLike, 'type' | 'relationCategory' | 'semanticOverlayCategory'>): RelationshipCategory {
  const relationCategory = String(edge.relationCategory || '').toLowerCase();
  const overlayCategory = String(edge.semanticOverlayCategory || '').toLowerCase();
  if (
    HIERARCHY_EDGE_TYPES.has(edge.type)
    || relationCategory.includes('hierarchy')
    || overlayCategory === 'hierarchy'
  ) {
    return 'hierarchy';
  }
  if (CONTEXTUAL_HIERARCHY_TYPES.has(edge.type) && overlayCategory === 'hierarchy') {
    return 'hierarchy';
  }
  return 'semantic';
}

export function normalizeGraphRelationship(
  edge: GraphEdgeLike,
  nodeById: Map<string, GraphNodeLike>,
  focusNodeId?: string,
): NormalizedGraphRelationship {
  const category = classifyGraphEdge(edge);
  let direction: NormalizedGraphRelationship['direction'] = 'undirected';
  if (focusNodeId) {
    if (edge.source === focusNodeId && edge.target === focusNodeId) direction = 'self';
    else if (edge.source === focusNodeId) direction = 'outgoing';
    else if (edge.target === focusNodeId) direction = 'incoming';
  }
  return {
    id: edge.id,
    sourceNodeId: edge.source,
    targetNodeId: edge.target,
    relationType: edge.type,
    direction,
    label: edge.relationType || edge.type,
    category,
    isHierarchyEdge: category === 'hierarchy',
    isSemanticEdge: category === 'semantic',
    sourceNode: nodeById.get(edge.source),
    targetNode: nodeById.get(edge.target),
    original: edge,
  };
}

function edgeMatchesDirection(edge: GraphEdgeLike, nodeId: string, direction: NeighborhoodOptions['direction']) {
  if (direction === 'out') return edge.source === nodeId;
  if (direction === 'in') return edge.target === nodeId;
  return edge.source === nodeId || edge.target === nodeId;
}

function otherNodeId(edge: GraphEdgeLike, currentNodeId: string) {
  return edge.source === currentNodeId ? edge.target : edge.source;
}

function edgeHiddenReasons(edge: GraphEdgeLike, nodeId: string, options: Required<Pick<NeighborhoodOptions, 'direction' | 'includeHierarchyEdges' | 'includeSemanticEdges'>> & Pick<NeighborhoodOptions, 'relTypes'>) {
  const reasons: string[] = [];
  if (!edgeMatchesDirection(edge, nodeId, options.direction)) reasons.push(`direction:${options.direction}`);
  if (options.relTypes?.length && !options.relTypes.includes(edge.type)) reasons.push('relation_type_filter');
  const category = classifyGraphEdge(edge);
  if (category === 'hierarchy' && !options.includeHierarchyEdges) reasons.push('hierarchy_edges_disabled');
  if (category === 'semantic' && !options.includeSemanticEdges) reasons.push('semantic_edges_disabled');
  return reasons;
}

export function buildGraphNeighborhood(index: NeighborhoodIndex, nodeId: string, options: NeighborhoodOptions = {}) {
  if (!index.nodeById.has(nodeId)) {
    throw new Error(`Graph node not found: ${nodeId}`);
  }

  const depth = Math.min(Math.max(Math.floor(options.depth ?? 1) || 1, 1), 3);
  const limit = Math.min(Math.max(Math.floor(options.limit ?? 500) || 1, 1), 1000);
  const normalizedOptions = {
    direction: options.direction ?? 'both',
    includeHierarchyEdges: options.includeHierarchyEdges ?? true,
    includeSemanticEdges: options.includeSemanticEdges ?? true,
    relTypes: options.relTypes,
  };

  const selectedEdges: GraphEdgeLike[] = [];
  const hiddenDirectRelationships: Array<{ edge: GraphEdgeLike; hiddenReasons: string[] }> = [];
  const seenEdgeIds = new Set<string>();
  const visitedNodeIds = new Set<string>([nodeId]);
  let frontier = [nodeId];
  let truncated = false;

  for (let currentDepth = 0; currentDepth < depth && frontier.length > 0; currentDepth += 1) {
    const nextFrontier: string[] = [];
    for (const currentNodeId of frontier) {
      const incident = (normalizedOptions.direction === 'out'
        ? index.outgoingByNodeId.get(currentNodeId)
        : normalizedOptions.direction === 'in'
          ? index.incomingByNodeId.get(currentNodeId)
          : index.undirectedByNodeId.get(currentNodeId)) || [];
      for (const edge of incident) {
        const hiddenReasons = edgeHiddenReasons(edge, currentNodeId, normalizedOptions);
        const isDirectFocusEdge = edge.source === nodeId || edge.target === nodeId;
        if (hiddenReasons.length > 0) {
          if (isDirectFocusEdge) hiddenDirectRelationships.push({ edge, hiddenReasons });
          continue;
        }
        if (seenEdgeIds.has(edge.id)) continue;
        if (selectedEdges.length >= limit) {
          truncated = true;
          continue;
        }
        seenEdgeIds.add(edge.id);
        selectedEdges.push(edge);
        const nextNodeId = otherNodeId(edge, currentNodeId);
        if (!visitedNodeIds.has(nextNodeId)) {
          visitedNodeIds.add(nextNodeId);
          nextFrontier.push(nextNodeId);
        }
      }
    }
    frontier = nextFrontier;
  }

  const nodeIds = new Set<string>([nodeId]);
  for (const edge of selectedEdges) {
    nodeIds.add(edge.source);
    nodeIds.add(edge.target);
  }

  const relationships = selectedEdges
    .filter((edge) => edge.source === nodeId || edge.target === nodeId)
    .map((edge) => normalizeGraphRelationship(edge, index.nodeById, nodeId))
    .sort((left, right) => (
      `${left.direction}:${left.relationType}:${left.sourceNodeId}:${left.targetNodeId}`
        .localeCompare(`${right.direction}:${right.relationType}:${right.sourceNodeId}:${right.targetNodeId}`)
    ));

  return {
    nodeId,
    depth,
    limit,
    nodes: Array.from(nodeIds).map((id) => index.nodeById.get(id)).filter(Boolean),
    edges: selectedEdges,
    relationships,
    relationshipCounts: {
      totalDirect: (index.undirectedByNodeId.get(nodeId) || []).length,
      visibleDirect: relationships.length,
      hiddenDirect: hiddenDirectRelationships.length + (truncated ? 1 : 0),
      incoming: relationships.filter((relationship) => relationship.direction === 'incoming').length,
      outgoing: relationships.filter((relationship) => relationship.direction === 'outgoing').length,
      hierarchy: relationships.filter((relationship) => relationship.isHierarchyEdge).length,
      semantic: relationships.filter((relationship) => relationship.isSemanticEdge).length,
    },
    hiddenRelationships: hiddenDirectRelationships.map(({ edge, hiddenReasons }) => ({
      id: edge.id,
      sourceNodeId: edge.source,
      targetNodeId: edge.target,
      relationType: edge.type,
      hiddenReasons,
    })),
    filters: normalizedOptions,
    truncated,
  };
}

export function validateGraphRelationshipData(nodes: GraphNodeLike[], edges: GraphEdgeLike[]) {
  const issues: RelationshipValidationIssue[] = [];
  const nodeIds = new Set<string>();
  const edgeIds = new Set<string>();
  for (const node of nodes) {
    if (!node.id) {
      issues.push({ code: 'node_missing_id', message: 'Graph node is missing id' });
      continue;
    }
    if (nodeIds.has(node.id)) {
      issues.push({ code: 'duplicate_node_id', message: `Duplicate node id: ${node.id}`, nodeId: node.id });
    }
    nodeIds.add(node.id);
  }
  for (const edge of edges) {
    if (!edge.id) {
      issues.push({ code: 'edge_missing_id', message: 'Graph edge is missing id' });
      continue;
    }
    if (edgeIds.has(edge.id)) {
      issues.push({ code: 'duplicate_edge_id', message: `Duplicate edge id: ${edge.id}`, edgeId: edge.id });
    }
    edgeIds.add(edge.id);
    if (!nodeIds.has(edge.source)) {
      issues.push({ code: 'missing_edge_source', message: `Edge source node does not exist: ${edge.source}`, edgeId: edge.id, nodeId: edge.source });
    }
    if (!nodeIds.has(edge.target)) {
      issues.push({ code: 'missing_edge_target', message: `Edge target node does not exist: ${edge.target}`, edgeId: edge.id, nodeId: edge.target });
    }
    if (!edge.type) {
      issues.push({ code: 'edge_missing_type', message: `Edge is missing type: ${edge.id}`, edgeId: edge.id });
    }
  }
  return issues;
}

export function detectCanonicalDuplicateCandidates(nodes: GraphNodeLike[]) {
  const byLabel = new Map<string, GraphNodeLike[]>();
  for (const node of nodes) {
    const normalized = normalizeCanonicalLabelLoose(node.displayLabel || node.label || '');
    if (!normalized) continue;
    const existing = byLabel.get(normalized);
    if (existing) existing.push(node);
    else byLabel.set(normalized, [node]);
  }

  return Array.from(byLabel.entries())
    .filter(([, candidates]) => candidates.length > 1)
    .map(([normalizedLabel, candidates]): DuplicateCanonicalCandidate => {
      const taxonomyPaths = candidates.map((node) => Array.isArray(node.taxonomy_path) ? node.taxonomy_path : []);
      const types = Array.from(new Set(candidates.map((node) => node.type || 'unknown'))).sort();
      const pathRoots = Array.from(new Set(taxonomyPaths.map((path) => path[0] || ''))).sort();
      const safeToAutoMerge = types.length === 1
        && pathRoots.length === 1
        && candidates.every((node) => (node.aliases || []).length > 0)
        && candidates.length === 2;
      return {
        normalizedLabel,
        nodeIds: candidates.map((node) => node.id).sort(),
        labels: Array.from(new Set(candidates.map((node) => node.displayLabel || node.label || '').filter(Boolean))).sort(),
        taxonomyPaths,
        types,
        safeToAutoMerge,
        reason: safeToAutoMerge
          ? 'case/plural/spacing duplicate candidate under the same taxonomy root; still requires reviewer confirmation before merge'
          : 'same normalized label spans multiple nodes, taxonomy paths, or concept contexts; queue for duplicate review rather than auto-merge',
      };
    })
    .sort((left, right) => left.normalizedLabel.localeCompare(right.normalizedLabel));
}
