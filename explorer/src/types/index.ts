export interface GraphNode {
  id: string;
  label: string;
  type: string;
  kind?: string;
  summary?: string;
  slug?: string;
  status?: string;
  confidence?: number;
  aliases?: string[];
  taxonomy_path?: string[];
  createdAt?: string;
  updatedAt?: string;
  radius?: number;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  reasoning?: string;
  confidence?: number;
  assertionId?: string;
}

export interface TaxonomyNode {
  id: string;
  label: string;
  kind: 'taxonomy' | 'topic' | 'subtopic';
  conceptCount: number;
  children: TaxonomyNode[];
}

export interface EvidenceSpan {
  id: string;
  quote: string;
  normalized_text?: string;
  deep_link?: string;
  document_id?: string;
  document_title?: string;
  confidence?: number;
}

export interface NodeDetail {
  node: GraphNode;
  taxonomyPath: TaxonomyNode[];
  incoming: RelationDetail[];
  outgoing: RelationDetail[];
  evidence: EvidenceSpan[];
}

export interface RelationDetail {
  relType: string;
  other: GraphNode;
  reasoning?: string;
  confidence?: number;
  assertionId?: string;
}

export interface EdgeDetail {
  edge: GraphEdge;
  source: GraphNode;
  target: GraphNode;
  evidence: EvidenceSpan[];
}

export interface SearchResult {
  kind: 'node' | 'taxonomy' | 'action';
  id: string;
  label: string;
  type?: string;
  matchType: string;
  matchedField: string;
}

export interface Perspective {
  id: string;
  name: string;
  description: string;
  nodeTypes: string[];
  edgeTypes: string[];
}

export interface SceneState {
  id: string;
  name: string;
  perspectiveId: string;
  camera: { x: number; y: number; ratio: number };
  selectedNodeIds: string[];
  selectedEdgeIds: string[];
  pinnedNodeIds: string[];
  filters: {
    nodeTypes: string[];
    edgeTypes: string[];
    minConfidence: number;
    maxConfidence: number;
    searchQuery: string;
  };
  expandedNodeIds: string[];
  hiddenNodeIds: string[];
}
