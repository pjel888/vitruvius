import type {
  SceneState,
  SceneSummary,
  SceneUpdateInput,
  QueryResultRow,
  GraphNode,
  GraphEdge,
  GraphNeighborhoodResponse,
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
  ResourceReviewCandidatesResponse,
  ResourceReviewLocalFilesResponse,
  ResourceReviewMetrics,
  ResourceReviewQueue,
  ResourceReviewStandardsResponse,
  StandardsContextDecisionBody,
  StandardsContextPreviewResponse,
  CanonicalDuplicateGroup,
  CanonicalDuplicateQueue,
  CanonicalDecisionPreview,
  CanonicalBatchRecord,
  CanonicalStewardshipDecision,
  CanonicalStewardshipApproval,
  CanonicalAdmittedRelationship,
  CanonicalP1DecisionPacket,
  CanonicalValidationResult,
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

export async function getNodeNeighborhood(
  id: string,
  options?: {
    depth?: number;
    limit?: number;
    direction?: 'in' | 'out' | 'both';
    includeHierarchyEdges?: boolean;
    includeSemanticEdges?: boolean;
    relTypes?: string[];
  },
): Promise<GraphNeighborhoodResponse> {
  const params = new URLSearchParams();
  if (options?.depth != null) params.set('depth', String(options.depth));
  if (options?.limit != null) params.set('limit', String(options.limit));
  if (options?.direction) params.set('direction', options.direction);
  if (options?.includeHierarchyEdges === false) params.set('includeHierarchyEdges', 'false');
  if (options?.includeSemanticEdges === false) params.set('includeSemanticEdges', 'false');
  if (options?.relTypes?.length) params.set('relTypes', options.relTypes.join(','));
  const query = params.toString();
  return api<GraphNeighborhoodResponse>(`/node/${encodeURIComponent(id)}/neighborhood${query ? `?${query}` : ''}`);
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

export async function getResourceReviewQueue(params?: Record<string, string | number | undefined>): Promise<ResourceReviewQueue> {
  const query = new URLSearchParams();
  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return api<ResourceReviewQueue>(`/resources/review/queue${query.toString() ? `?${query.toString()}` : ''}`);
}

export async function getResourceReviewCandidates(): Promise<ResourceReviewCandidatesResponse> {
  return api<ResourceReviewCandidatesResponse>('/resources/review/candidates');
}

export async function getResourceReviewLocalFiles(): Promise<ResourceReviewLocalFilesResponse> {
  return api<ResourceReviewLocalFilesResponse>('/resources/review/local-files');
}

export async function getResourceReviewStandards(): Promise<ResourceReviewStandardsResponse> {
  return api<ResourceReviewStandardsResponse>('/resources/review/standards');
}

export async function getResourceReviewStandardDetail(id: string): Promise<StandardsContextPreviewResponse> {
  return api<StandardsContextPreviewResponse>(`/resources/review/standards/${encodeURIComponent(id)}`);
}

export async function getResourceReviewReport(): Promise<ResourceReviewMetrics> {
  return api<ResourceReviewMetrics>('/resources/review/report');
}

export async function submitLinkReviewDecision(linkId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/resources/review/link/${encodeURIComponent(linkId)}/decision`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function submitCandidateReviewDecision(candidateId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/resources/review/candidate/${encodeURIComponent(candidateId)}/decision`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function submitLocalFileReviewDecision(fileId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/resources/review/local-file/${encodeURIComponent(fileId)}/decision`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function previewStandardsContextDecision(id: string, body: StandardsContextDecisionBody): Promise<StandardsContextPreviewResponse> {
  return api<StandardsContextPreviewResponse>(`/resources/review/standards/${encodeURIComponent(id)}/context-preview`, {
    method: 'POST',
    body: JSON.stringify({ ...body, dryRun: true }),
  });
}

export async function submitStandardsContextDecision(id: string, body: StandardsContextDecisionBody): Promise<StandardsContextPreviewResponse> {
  return api<StandardsContextPreviewResponse>(`/resources/review/standards/${encodeURIComponent(id)}/context-decision`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function getCanonicalDuplicateGroups(params?: Record<string, string | number | boolean | undefined>): Promise<CanonicalDuplicateQueue> {
  const query = new URLSearchParams();
  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return api<CanonicalDuplicateQueue>(`/graph/canonical/duplicates${query.toString() ? `?${query.toString()}` : ''}`);
}

export async function getCanonicalDuplicateGroup(groupId: string): Promise<{ group: CanonicalDuplicateGroup }> {
  return api<{ group: CanonicalDuplicateGroup }>(`/graph/canonical/duplicates/${encodeURIComponent(groupId)}`);
}

export async function previewCanonicalDecision(groupId: string, body: Record<string, unknown>): Promise<{ preview?: CanonicalDecisionPreview; decision?: CanonicalStewardshipDecision; blockers?: string[] }> {
  return api(`/graph/canonical/duplicates/${encodeURIComponent(groupId)}/preview`, {
    method: 'POST',
    body: JSON.stringify({ ...body, dryRun: true, apply: false }),
  });
}

export async function submitCanonicalDecision(groupId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/duplicates/${encodeURIComponent(groupId)}/decision`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function getCanonicalDecisions(): Promise<{ decisions: CanonicalStewardshipDecision[] }> {
  return api('/graph/canonical/decisions');
}

export async function getCanonicalApprovals(): Promise<{ approvals: CanonicalStewardshipApproval[]; admittedRelationships: CanonicalAdmittedRelationship[] }> {
  return api('/graph/canonical/approvals');
}

export async function getCanonicalApproval(approvalId: string): Promise<{ approval: CanonicalStewardshipApproval; admittedRelationships: CanonicalAdmittedRelationship[] }> {
  return api(`/graph/canonical/approvals/${encodeURIComponent(approvalId)}`);
}

export async function previewCanonicalApproval(decisionId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/decisions/${encodeURIComponent(decisionId)}/approval-preview`, {
    method: 'POST',
    body: JSON.stringify({ ...body, dryRun: true, apply: false }),
  });
}

export async function submitCanonicalApproval(decisionId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/decisions/${encodeURIComponent(decisionId)}/approve`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function rejectCanonicalApproval(decisionId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/decisions/${encodeURIComponent(decisionId)}/reject-approval`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function getCanonicalSearch(q: string, limit = 20): Promise<{ results: SearchResult[] }> {
  return api(`/graph/canonical/search?q=${encodeURIComponent(q)}&limit=${limit}`);
}

export async function getCanonicalValidation(): Promise<CanonicalValidationResult> {
  return api<CanonicalValidationResult>('/graph/canonical/validation');
}

export async function getCanonicalBatches(): Promise<{ batches: CanonicalBatchRecord[]; total: number }> {
  return api('/graph/canonical/batches');
}

export async function createCanonicalBatch(body: Record<string, unknown>): Promise<{ batch: CanonicalBatchRecord }> {
  return api('/graph/canonical/batches', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function previewCanonicalBatchDecision(batchId: string, body: Record<string, unknown>): Promise<{ preview: unknown; blockers?: string[] }> {
  return api(`/graph/canonical/batches/${encodeURIComponent(batchId)}/preview`, {
    method: 'POST',
    body: JSON.stringify({ ...body, dryRun: true, apply: false }),
  });
}

export async function submitCanonicalBatchDecision(batchId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/batches/${encodeURIComponent(batchId)}/decision`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function getCanonicalP1DecisionPackets(): Promise<{ packets: CanonicalP1DecisionPacket[]; total: number }> {
  return api('/graph/canonical/p1-decision-packets');
}

export async function generateCanonicalP1DecisionPackets(body: Record<string, unknown>): Promise<{ packets: CanonicalP1DecisionPacket[]; blockers?: string[] }> {
  return api('/graph/canonical/p1-decision-packets/generate', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function getCanonicalRollbackPreview(decisionId: string): Promise<unknown> {
  return api(`/graph/canonical/decisions/${encodeURIComponent(decisionId)}/rollback-preview`);
}

export async function submitCanonicalRollback(decisionId: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/decisions/${encodeURIComponent(decisionId)}/rollback`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function getCanonicalRemediation(): Promise<{ remediationManifests: Array<Record<string, unknown>> }> {
  return api('/graph/canonical/remediation');
}

export async function getCanonicalRemediationManifest(id: string): Promise<{ remediation: Record<string, unknown> }> {
  return api(`/graph/canonical/remediation/${encodeURIComponent(id)}`);
}

export async function submitCanonicalRemediationStatus(id: string, body: Record<string, unknown>): Promise<unknown> {
  return api(`/graph/canonical/remediation/${encodeURIComponent(id)}/status`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
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

export function getNodesForPerspectivePath(perspectiveId: string) {
  const params = new URLSearchParams();
  if (perspectiveId === 'aec-mepfs') params.set('profile', 'render');
  const query = params.toString();
  return `/perspective/${encodeURIComponent(perspectiveId)}/nodes${query ? `?${query}` : ''}`;
}

export function getNodesForPerspectiveUrl(perspectiveId: string) {
  return `${API_BASE}${getNodesForPerspectivePath(perspectiveId)}`;
}

export async function getNodesForPerspective(perspectiveId: string): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] }> {
  return api(getNodesForPerspectivePath(perspectiveId));
}

export async function expandNode(
  nodeId: string,
  relTypes?: string[],
  options?: { direction?: 'in' | 'out' | 'both'; depth?: number },
): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] }> {
  const params = new URLSearchParams({ nodeId });
  if (relTypes) params.set('relTypes', relTypes.join(','));
  if (options?.direction) params.set('direction', options.direction);
  if (options?.depth != null) params.set('depth', String(options.depth));
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
