import type {
  SceneState,
  SceneSummary,
  SceneUpdateInput,
  QueryResultRow,
  GraphNode,
  GraphEdge,
  TaxonomyNode,
  NodeDetail,
  EdgeDetail,
  SearchResult,
  Perspective,
  ApiHealth,
  BackboneEvidencePreview,
  BackbonePlacementQaPreview,
  BackboneSummary,
  BackboneTaxonomyPreview,
} from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';
export const BACKBONE_EVIDENCE_PREVIEW_PATH = '/v2/backbone/evidence';
export const BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-evidence-preview/v1';
export const BACKBONE_PLACEMENT_QA_PREVIEW_PATH = '/v2/backbone/placement-qa';
export const BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION = 'aec-bb-shadow-v2-backbone-placement-qa-preview/v1';

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error?.message || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function searchNodes(q: string, perspectiveId?: string, limit = 20): Promise<SearchResult[]> {
  const data = await api<{ results: SearchResult[] }>(
    `/search?q=${encodeURIComponent(q)}&perspective=${encodeURIComponent(perspectiveId || '')}&limit=${limit}`
  );
  return data.results;
}

export async function getNode(id: string): Promise<NodeDetail> {
  return api<NodeDetail>(`/node/${encodeURIComponent(id)}`);
}

export async function getEdgeDetail(edgeId: string): Promise<EdgeDetail> {
  return api<EdgeDetail>(`/edge/${encodeURIComponent(edgeId)}`);
}

export async function getTaxonomy(): Promise<TaxonomyNode[]> {
  const data = await api<{ roots: TaxonomyNode[] }>('/taxonomy');
  return data.roots;
}

export async function getPerspectives(): Promise<Perspective[]> {
  const data = await api<{ perspectives: Perspective[] }>('/perspectives');
  return data.perspectives;
}

export async function getHealth(): Promise<ApiHealth> {
  return api<ApiHealth>('/health');
}

export async function getBackboneSummary(): Promise<BackboneSummary> {
  return api<BackboneSummary>('/v2/backbone');
}

export async function getBackboneTaxonomyPreview(): Promise<BackboneTaxonomyPreview> {
  return api<BackboneTaxonomyPreview>('/v2/backbone/taxonomy');
}

export async function getBackbonePlacementQaPreview(): Promise<BackbonePlacementQaPreview> {
  return api<BackbonePlacementQaPreview>(BACKBONE_PLACEMENT_QA_PREVIEW_PATH);
}

export async function getBackboneEvidencePreview(): Promise<BackboneEvidencePreview> {
  return api<BackboneEvidencePreview>(BACKBONE_EVIDENCE_PREVIEW_PATH);
}

export async function listScenes(): Promise<SceneSummary[]> {
  const data = await api<{ scenes: SceneSummary[] }>('/scenes');
  return data.scenes;
}

export async function getScene(id: string): Promise<SceneState> {
  return api<SceneState>(`/scene/${encodeURIComponent(id)}`);
}

export async function saveScene(scene: SceneUpdateInput): Promise<{ sceneId: string; url: string; scene: SceneState }> {
  return api('/scene/save', {
    method: 'POST',
    body: JSON.stringify(scene),
  });
}

export async function updateScene(id: string, scene: SceneUpdateInput): Promise<{ scene: SceneState }> {
  return api(`/scene/${encodeURIComponent(id)}`, {
    method: 'PUT',
    body: JSON.stringify(scene),
  });
}

export async function deleteScene(id: string): Promise<{ ok: true; id: string }> {
  return api(`/scene/${encodeURIComponent(id)}`, {
    method: 'DELETE',
  });
}

export async function getNodesForPerspective(perspectiveId: string): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] }> {
  return api(`/perspective/${encodeURIComponent(perspectiveId)}/nodes`);
}

export async function expandNode(nodeId: string, relTypes?: string[]): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] }> {
  const params = new URLSearchParams({ nodeId });
  if (relTypes) params.set('relTypes', relTypes.join(','));
  return api(`/expand?${params.toString()}`);
}

export async function tracePath(from: string, to: string): Promise<{ paths: { length: number; nodes: GraphNode[]; edges: GraphEdge[] }[] }> {
  return api(`/path?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`);
}

export async function runCypherQuery(cypher: string): Promise<{ nodes: GraphNode[]; edges: GraphEdge[]; recordCount: number; rows: QueryResultRow[] }> {
  return api('/query', {
    method: 'POST',
    body: JSON.stringify({ cypher }),
  });
}
