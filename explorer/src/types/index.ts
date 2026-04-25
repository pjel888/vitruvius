export interface GraphNode {
  id: string;
  label: string;
  displayLabel?: string;
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
  displayLabel?: string;
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
  displayLabel?: string;
  type?: string;
  matchType: string;
  matchedField: string;
}

export interface Perspective {
  id: string;
  name: string;
  description: string;
  nodeCount?: number;
}

export interface ApiHealth {
  status: 'ok' | 'error';
  neo4j: string;
}

export interface BackboneSummary {
  schemaVersion: string;
  source: string;
  status: string;
  reportOk: boolean;
  runId: string;
  counts: {
    predicateRegistry: number;
    sourceRightsRegistry: number;
  };
  boundaries: {
    shadowOnly: boolean;
    fileBackedOnly: boolean;
    liveNeo4jWrites: boolean;
    graphRebuild: boolean;
    featureFlagCutover: boolean;
    apiExplorerCutover: boolean;
    canonicalContentAdmission: boolean;
    protectedContentIngest: boolean;
    liveMutationBoundariesClear: boolean;
    safeForReadOnlyConsumer: boolean;
  };
  noIngestBoundaryCoverage: {
    sourcesTotal: number;
    explicitNoIngestSourceCount: number;
    missingExplicitBlockCount: number;
    contentIngestSourceCount: number;
  };
  artifactPaths: {
    artifact: string;
    producerReport: string;
    consumerReport: string;
  };
}

export interface QueryResultRow {
  id: string;
  values: Record<string, string>;
}

export interface CameraState {
  x: number;
  y: number;
  ratio: number;
}

export interface SceneGraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface SceneState {
  id: string;
  name: string;
  savedAt?: string;
  perspectiveId: string;
  camera: CameraState;
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
  layout: 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time';
  colorScheme: string;
  sizeBy: 'uniform' | 'confidence' | 'degree';
  graph: SceneGraphData;
}

export interface SceneSummary {
  id: string;
  name: string;
  savedAt?: string;
  perspectiveId: string;
}

export type SceneUpdateInput = Omit<SceneState, 'id' | 'savedAt'>;
