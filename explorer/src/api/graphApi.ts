import type {
  SceneState,
  SceneSummary,
  SceneUpdateInput,
  GraphNode,
  GraphEdge,
  TaxonomyNode,
  NodeDetail,
  EdgeDetail,
  SearchResult,
  Perspective,
} from '../types';

const API_BASE = 'http://localhost:3000';

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

export async function getNode(id: string): Promise<NodeDetail | null> {
  try {
    return await api<NodeDetail>(`/node/${encodeURIComponent(id)}`);
  } catch {
    return null;
  }
}

export async function getEdgeDetail(edgeId: string): Promise<EdgeDetail | null> {
  try {
    return await api<EdgeDetail>(`/edge/${encodeURIComponent(edgeId)}`);
  } catch {
    return null;
  }
}

export async function getTaxonomy(): Promise<TaxonomyNode[]> {
  const data = await api<{ roots: TaxonomyNode[] }>('/taxonomy');
  return data.roots;
}

export async function getPerspectives(): Promise<Perspective[]> {
  const data = await api<{ perspectives: Perspective[] }>('/perspectives');
  return data.perspectives;
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

export async function runCypherQuery(cypher: string): Promise<{ nodes: GraphNode[]; edges: GraphEdge[]; recordCount: number }> {
  return api('/query', {
    method: 'POST',
    body: JSON.stringify({ cypher }),
  });
}
