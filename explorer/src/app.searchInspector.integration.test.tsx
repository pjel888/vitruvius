import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { act, cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import React from 'react';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { useSceneStore } from './stores/useSceneStore';

let dom: JSDOM;
let backboneFetchCount = 0;
let backboneTaxonomyFetchCount = 0;
let backbonePlacementQaFetchCount = 0;
let backboneEvidenceFetchCount = 0;
let perspectiveFetches: string[] = [];

function sampleBackboneSummary() {
  return {
    schemaVersion: 'aec-bb-shadow-v2-backbone-summary/v1',
    source: 'file-backed-shadow-staging-consumer-report',
    status: 'shadow_ready',
    reportOk: true,
    runId: 'TEST_RUN',
    counts: {
      predicateRegistry: 12,
      sourceRightsRegistry: 29,
      backboneNodes: 2,
    },
    boundaries: {
      shadowOnly: true,
      fileBackedOnly: true,
      liveNeo4jWrites: false,
      graphRebuild: false,
      featureFlagCutover: false,
      apiExplorerCutover: false,
      canonicalContentAdmission: false,
      protectedContentIngest: false,
      liveMutationBoundariesClear: true,
      safeForReadOnlyConsumer: true,
    },
    noIngestBoundaryCoverage: {
      sourcesTotal: 29,
      explicitNoIngestSourceCount: 29,
      missingExplicitBlockCount: 0,
      contentIngestSourceCount: 0,
    },
    artifactPaths: {
      artifact: 'shadow-backbone-staging.json',
      shadowGraph: 'shadow-backbone-graph.json',
      producerReport: 'shadow-staging-report.json',
      consumerReport: 'shadow-staging-consumer-report.json',
    },
  };
}

function sampleBackboneTaxonomyPreview() {
  return {
    schemaVersion: 'aec-bb-shadow-v2-backbone-taxonomy-preview/v1',
    source: 'file-backed-shadow-staging-artifact',
    status: 'shadow_ready',
    reportOk: true,
    runId: 'TEST_RUN',
    counts: sampleBackboneSummary().counts,
    boundaries: sampleBackboneSummary().boundaries,
    noIngestBoundaryCoverage: sampleBackboneSummary().noIngestBoundaryCoverage,
    readiness: {
      registryMetadataAvailable: true,
      canonicalTaxonomyTreeAvailable: true,
      backboneNodesAvailable: true,
      shadowGraphAvailable: true,
      previewCompleteness: 'registry_metadata_admitted_nodes_and_shadow_graph',
      limitation: 'Shadow graph rows are preview-only.',
    },
    predicateCategories: [
      { category: 'hierarchy', count: 2, predicates: ['broader_than', 'narrower_than'] },
    ],
    predicates: [],
    backboneNodes: [
      {
        id: 'VTN-DOM-0000001',
        canonicalId: 'VTN-DOM-0000001',
        label: 'Architecture',
        prefLabel: 'Architecture',
        pathCode: 'ARC',
        level: 1,
        parentPathCode: '',
        reviewStatus: 'steward_admitted',
        steward: 'Philip Lewis',
        releaseVersion: '0.1.0',
      },
      {
        id: 'VTN-DOM-0000002',
        canonicalId: 'VTN-DOM-0000002',
        label: 'Spatial Planning',
        prefLabel: 'Spatial Planning',
        pathCode: 'ARC.SPC',
        level: 2,
        parentPathCode: 'ARC',
        reviewStatus: 'steward_admitted',
        steward: 'Philip Lewis',
        releaseVersion: '0.1.0',
      },
    ],
    shadowGraph: {
      available: true,
      counts: {
        nodes: 2,
        edges: 1,
        roots: 1,
        maxDepth: 4,
      },
      nodes: [
        {
          id: 'VTN-DOM-0000001',
          label: 'Architecture',
          pathCode: 'ARC',
          level: 1,
          parentPathCode: '',
        },
        {
          id: 'VTN-DOM-0000002',
          label: 'Spatial Planning',
          pathCode: 'ARC.SPC',
          level: 2,
          parentPathCode: 'ARC',
        },
      ],
      edges: [
        {
          id: 'VTN-DOM-0000001--broader_than--VTN-DOM-0000002',
          fromId: 'VTN-DOM-0000001',
          toId: 'VTN-DOM-0000002',
          predicate: 'broader_than',
          fromPathCode: 'ARC',
          toPathCode: 'ARC.SPC',
        },
      ],
    },
    sourceRightsClasses: [
      { sourceRightsClass: 'reference_only', count: 13 },
    ],
    clearanceStates: [
      { clearanceState: 'planning_reference_only', count: 10 },
    ],
    sourceFamilies: [],
    artifactPaths: sampleBackboneSummary().artifactPaths,
  };
}

function sampleBackbonePlacementQaPreview() {
  return {
    schemaVersion: 'aec-bb-shadow-v2-backbone-placement-qa-preview/v1',
    source: 'file-backed-placement-qa-report',
    status: 'shadow_ready',
    reportOk: true,
    runId: 'TEST_QA_RUN',
    fixturePath: 'scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s2.json',
    reportPath: '006_System-Manifests/aec-mepfs-backbone/placement-qa/TEST_QA_RUN/placement-qa-report.json',
    summary: {
      casesTotal: 3,
      casesPassed: 3,
      casesFailed: 0,
      autoAcceptCases: 1,
      proposalLevelCounts: {
        L1: 1,
        L2: 1,
        L3: 1,
      },
      reviewQueueCounts: {
        human_steward_review: 2,
        ld8_auto_accept: 1,
      },
    },
    requiredCoverage: {
      l1_l2_human_review: true,
      l3_l4_ld8_auto_accept: true,
      legacy_label_alias: true,
    },
    contractValidation: {
      ok: true,
      warnings: [],
    },
    boundaries: {
      shadowOnly: true,
      fileBackedOnly: true,
      liveNeo4jWrites: false,
      kgRebuild: false,
      featureFlagCutover: false,
      explorerDefaultAdoption: false,
      protectedContentIngest: false,
      canonicalContentAdmission: false,
      liveMutationBoundariesClear: true,
    },
    warnings: ['placement QA remains preview-only'],
  };
}

function sampleBackboneEvidencePreview() {
  return {
    schemaVersion: 'aec-bb-shadow-v2-backbone-evidence-preview/v1',
    source: 'file-backed-shadow-evidence-manifest',
    status: 'shadow_ready',
    reportOk: true,
    runId: 'TEST_EVIDENCE_RUN',
    summary: {
      artifactCount: 9,
      shadowGraphCounts: {
        nodes: 4605,
        edges: 4581,
        roots: 24,
        maxDepth: 4,
      },
      boundaryChecksPassed: 10,
      boundaryChecksTotal: 10,
      benchmarkOperationsPassed: 5,
      benchmarkOperationsTotal: 5,
      routeCount: 24,
      previewRoutesPresent: 7,
      previewRoutesRequired: 7,
      inputHashCount: 10,
      resolverRoutePolicy: 'guarded_default_off',
      benchmarkRuntimeThresholdDisposition: 'not_evaluated_shadow_file_backed_only',
    },
    safetyInvariants: {
      allArtifactsOk: true,
      benchmarkShadowFileBackedOnly: true,
      boundaryAuditSafetyGreen: true,
      noRuntimePromotion: true,
      resolverRoutesAbsentOrDefaultOff: true,
      routeInventoryPreviewRoutesComplete: true,
      runtimeThresholdsNotEvaluated: true,
      allInvariantsClear: true,
    },
    evidenceFiles: [
      {
        label: 'producer_report',
        path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-report.json',
        schemaVersion: 'aec-bb-shadow-staging-report/v1',
        ok: true,
      },
      {
        label: 'route_inventory_report',
        path: '006_System-Manifests/aec-mepfs-backbone/api-route-inventory/TEST_RUN/api-route-inventory-report.json',
        schemaVersion: 'aec-bb-api-route-inventory-report/v1',
        ok: true,
      },
    ],
    repoState: {
      gitHeadCommit: 'abc123',
      workingTreeDirtyAtGeneration: true,
      freshnessAvailable: true,
      sourceWorkingTreeDirtyAtGeneration: false,
      generatedEvidenceDirtyAtGeneration: true,
      sourceDirtyPathCount: 0,
      generatedEvidenceDirtyPathCount: 2,
    },
    reportPath: '006_System-Manifests/aec-mepfs-backbone/evidence-manifest/TEST_EVIDENCE_RUN/shadow-evidence-manifest-report.json',
  };
}

beforeEach(() => {
  dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'http://localhost:5173/explore' });
  globalThis.window = dom.window as typeof globalThis.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.navigator = dom.window.navigator as Navigator;
  globalThis.localStorage = dom.window.localStorage;
  backboneFetchCount = 0;
  backboneTaxonomyFetchCount = 0;
  backbonePlacementQaFetchCount = 0;
  backboneEvidenceFetchCount = 0;
  perspectiveFetches = [];
  useSceneStore.setState({
    perspectiveId: 'aec-mepfs',
    activeSceneId: null,
    activeSceneName: null,
    selectedNodeId: null,
    selectedEdgeId: null,
    pinnedNodeIds: [],
    nodes: [],
    edges: [],
    preloadedPerspectiveId: null,
    explorerOpen: true,
    inspectorOpen: false,
    bottomOpen: false,
    bottomContent: null,
    searchQuery: '',
    contextMenuNodeId: null,
    contextMenuPos: null,
    pathSourceId: null,
    pathTargetId: null,
    highlightedPath: null,
    focusSubgraphNodeId: null,
    focusedNodeId: null,
    camera: { x: 0, y: 0, ratio: 1 },
    loading: false,
    loadError: null,
    hiddenNodeIds: [],
    expandedNodeIds: [],
    visibleNodeTypes: new Set(['taxonomy', 'topic', 'subtopic', 'concept', 'rule', 'definition', 'procedure', 'exception', 'evidence_span']),
    visibleEdgeTypes: new Set(['HAS_CHILD', 'BELONGS_TO', 'RELATED_TO', 'DEPENDS_ON', 'DEFINED_BY', 'REQUIRES', 'SUPPORTED_BY']),
    layout: 'forceatlas2',
    colorScheme: 'default',
    sizeBy: 'uniform',
    pendingSelectedNodeId: null,
  });
});

afterEach(() => {
  cleanup();
});

mock.module('./api/graphApi', () => ({
  searchNodes: async () => ([
    {
      id: 'taxonomy-fire-life-safety',
      kind: 'node',
      label: 'Fire Life Safety',
      displayLabel: 'Fire Life Safety',
      type: 'taxonomy',
      matchType: 'slug',
      matchedField: 'slug',
    },
  ]),
  getPerspectives: async () => ([
    { id: 'aec-mepfs', name: 'AEC-MEPFS Backbone', description: 'Default taxonomy-first backbone', nodeCount: 4605 },
    { id: 'default', name: 'Legacy Knowledge Snapshot', description: 'Pre-cutover graph snapshot', nodeCount: 88 },
    { id: 'concepts', name: 'Concepts Only', description: 'Concept semantic network', nodeCount: 22 },
  ]),
  listScenes: async () => ([]),
  saveScene: async () => { throw new Error('not used'); },
  updateScene: async () => { throw new Error('not used'); },
  deleteScene: async () => { throw new Error('not used'); },
  getScene: async () => { throw new Error('not used'); },
  getHealth: async () => ({ status: 'ok', neo4j: 'connected' }),
  getBackboneSummary: async () => {
    backboneFetchCount += 1;
    return sampleBackboneSummary();
  },
  getBackboneTaxonomyPreview: async () => {
    backboneTaxonomyFetchCount += 1;
    return sampleBackboneTaxonomyPreview();
  },
  getBackbonePlacementQaPreview: async () => {
    backbonePlacementQaFetchCount += 1;
    return sampleBackbonePlacementQaPreview();
  },
  getBackboneEvidencePreview: async () => {
    backboneEvidenceFetchCount += 1;
    return sampleBackboneEvidencePreview();
  },
  getNodesForPerspective: async (perspectiveId: string) => {
    perspectiveFetches.push(perspectiveId);
    return {
      nodes: [{ id: 'taxonomy-fire-life-safety', label: 'Fire Life Safety', displayLabel: 'Fire Life Safety', type: 'taxonomy' }],
      edges: [],
    };
  },
  getNodesForPerspectiveUrl: (perspectiveId: string) => `http://test.local/perspective/${perspectiveId}/nodes`,
  getTaxonomy: async () => ([]),
  getNode: async () => ({
    node: { id: 'taxonomy-fire-life-safety', label: 'Fire Life Safety', displayLabel: 'Fire Life Safety', type: 'taxonomy' },
    taxonomyPath: [],
    incoming: [],
    outgoing: [],
    evidence: [],
  }),
  getNodeNeighborhood: async (id: string) => ({
    schemaVersion: 'aec-mepfs-graph-neighborhood/v1',
    source: 'test',
    nodeId: id,
    depth: 1,
    limit: 1000,
    nodes: [],
    edges: [],
    relationships: [],
    relationshipCounts: {
      totalDirect: 0,
      visibleDirect: 0,
      hiddenDirect: 0,
      incoming: 0,
      outgoing: 0,
      hierarchy: 0,
      semantic: 0,
    },
    hiddenRelationships: [],
    filters: {
      direction: 'both',
      includeHierarchyEdges: true,
      includeSemanticEdges: true,
    },
    truncated: false,
  }),
  getEdgeDetail: async () => { throw new Error('not used'); },
  tracePath: async () => ({ paths: [] }),
  runCypherQuery: async () => ({ nodes: [], edges: [], recordCount: 0, rows: [] }),
  getResourceReviewQueue: async () => {
    const response = await fetch('http://localhost:3000/resources/review/queue');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'review queue unavailable');
    return response.json();
  },
  getResourceReviewCandidates: async () => {
    const response = await fetch('http://localhost:3000/resources/review/candidates');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'review candidates unavailable');
    return response.json();
  },
  getResourceReviewLocalFiles: async () => {
    const response = await fetch('http://localhost:3000/resources/review/local-files');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'review local files unavailable');
    return response.json();
  },
  getResourceReviewStandards: async () => {
    const response = await fetch('http://localhost:3000/resources/review/standards');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'review standards unavailable');
    return response.json();
  },
  getResourceReviewReport: async () => {
    const response = await fetch('http://localhost:3000/resources/review/report');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'review report unavailable');
    return response.json();
  },
  submitLinkReviewDecision: async (linkId: string, body: Record<string, unknown>) => fetch(
    `http://localhost:3000/resources/review/link/${encodeURIComponent(linkId)}/decision`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) },
  ),
  submitCandidateReviewDecision: async (candidateId: string, body: Record<string, unknown>) => fetch(
    `http://localhost:3000/resources/review/candidate/${encodeURIComponent(candidateId)}/decision`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) },
  ),
  submitLocalFileReviewDecision: async (fileId: string, body: Record<string, unknown>) => fetch(
    `http://localhost:3000/resources/review/local-file/${encodeURIComponent(fileId)}/decision`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) },
  ),
  getCanonicalDuplicateGroups: async (params?: Record<string, string | number | boolean | undefined>) => {
    const query = new URLSearchParams();
    Object.entries(params || {}).forEach(([key, value]) => {
      if (value !== undefined && value !== '') query.set(key, String(value));
    });
    const response = await fetch(`http://localhost:3000/graph/canonical/duplicates${query.toString() ? `?${query.toString()}` : ''}`);
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical duplicates unavailable');
    return response.json();
  },
  getCanonicalDuplicateGroup: async (groupId: string) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/duplicates/${encodeURIComponent(groupId)}`);
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical duplicate unavailable');
    return response.json();
  },
  previewCanonicalDecision: async (groupId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/duplicates/${encodeURIComponent(groupId)}/preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical preview unavailable');
    return response.json();
  },
  submitCanonicalDecision: async (groupId: string, body: Record<string, unknown>) => fetch(
    `http://localhost:3000/graph/canonical/duplicates/${encodeURIComponent(groupId)}/decision`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) },
  ),
  getCanonicalDecisions: async () => {
    const response = await fetch('http://localhost:3000/graph/canonical/decisions');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical decisions unavailable');
    return response.json();
  },
  getCanonicalApprovals: async () => {
    const response = await fetch('http://localhost:3000/graph/canonical/approvals');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical approvals unavailable');
    return response.json();
  },
  getCanonicalApproval: async (approvalId: string) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/approvals/${encodeURIComponent(approvalId)}`);
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical approval unavailable');
    return response.json();
  },
  previewCanonicalApproval: async (decisionId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/decisions/${encodeURIComponent(decisionId)}/approval-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical approval preview unavailable');
    return response.json();
  },
  submitCanonicalApproval: async (decisionId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/decisions/${encodeURIComponent(decisionId)}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical approval unavailable');
    return response.json();
  },
  rejectCanonicalApproval: async (decisionId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/decisions/${encodeURIComponent(decisionId)}/reject-approval`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical approval rejection unavailable');
    return response.json();
  },
  getCanonicalSearch: async (q: string) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/search?q=${encodeURIComponent(q)}`);
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical search unavailable');
    return response.json();
  },
  getCanonicalValidation: async () => {
    const response = await fetch('http://localhost:3000/graph/canonical/validation');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical validation unavailable');
    return response.json();
  },
  getCanonicalBatches: async () => {
    const response = await fetch('http://localhost:3000/graph/canonical/batches');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical batches unavailable');
    return response.json();
  },
  createCanonicalBatch: async (body: Record<string, unknown>) => {
    const response = await fetch('http://localhost:3000/graph/canonical/batches', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical batch creation unavailable');
    return response.json();
  },
  previewCanonicalBatchDecision: async (batchId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/batches/${encodeURIComponent(batchId)}/preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical batch preview unavailable');
    return response.json();
  },
  submitCanonicalBatchDecision: async (batchId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/batches/${encodeURIComponent(batchId)}/decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical batch decision unavailable');
    return response.json();
  },
  getCanonicalP1DecisionPackets: async () => {
    const response = await fetch('http://localhost:3000/graph/canonical/p1-decision-packets');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical P1 packets unavailable');
    return response.json();
  },
  generateCanonicalP1DecisionPackets: async (body: Record<string, unknown>) => {
    const response = await fetch('http://localhost:3000/graph/canonical/p1-decision-packets/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical P1 packet generation unavailable');
    return response.json();
  },
  getCanonicalRollbackPreview: async (decisionId: string) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/decisions/${encodeURIComponent(decisionId)}/rollback-preview`);
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical rollback preview unavailable');
    return response.json();
  },
  submitCanonicalRollback: async (decisionId: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/decisions/${encodeURIComponent(decisionId)}/rollback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical rollback unavailable');
    return response.json();
  },
  getCanonicalRemediation: async () => {
    const response = await fetch('http://localhost:3000/graph/canonical/remediation');
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical remediation unavailable');
    return response.json();
  },
  getCanonicalRemediationManifest: async (id: string) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/remediation/${encodeURIComponent(id)}`);
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical remediation manifest unavailable');
    return response.json();
  },
  submitCanonicalRemediationStatus: async (id: string, body: Record<string, unknown>) => {
    const response = await fetch(`http://localhost:3000/graph/canonical/remediation/${encodeURIComponent(id)}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error((await response.json()).error?.message || 'canonical remediation status unavailable');
    return response.json();
  },
}));

mock.module('./components/GraphScene', () => ({
  default: function MockGraphScene() {
    return <div>Graph Scene</div>;
  },
}));

mock.module('./components/BottomDrawer', () => ({
  default: function MockBottomDrawer() {
    return null;
  },
}));

function LocationProbe() {
  const location = useLocation();
  return <div data-testid="location-probe">{location.pathname}{location.search}</div>;
}

describe('ExploreView search-to-inspector integration', () => {


  test('default explore route loads AEC-MEPFS perspective without AEC preview panel fetches', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(useSceneStore.getState().nodes.some((node) => node.id === 'taxonomy-fire-life-safety')).toBe(true);
    });

    expect(useSceneStore.getState().perspectiveId).toBe('aec-mepfs');
    expect(perspectiveFetches[0]).toBe('aec-mepfs');
    expect(view.getByTestId('location-probe').textContent).toBe('/explore');
    expect(backboneFetchCount).toBe(0);
    expect(backboneTaxonomyFetchCount).toBe(0);
    expect(backbonePlacementQaFetchCount).toBe(0);
    expect(backboneEvidenceFetchCount).toBe(0);
  });

  test('HomeScreen default entry points preload the AEC-MEPFS graph', async () => {
    const { default: HomeScreen } = await import('./components/HomeScreen');

    const view = render(
      <MemoryRouter>
        <HomeScreen />
      </MemoryRouter>,
    );

    const primaryAecButtons = await view.findAllByRole('button', { name: /Open AEC-MEPFS Backbone/i });
    const primaryAecButton = primaryAecButtons.find((button) =>
      button.textContent?.includes('Browse the taxonomy-first AEC / MEPFS graph')
    );
    expect(primaryAecButton).toBeTruthy();
    fireEvent.click(primaryAecButton!);

    await waitFor(() => {
      expect(perspectiveFetches).toContain('aec-mepfs');
      expect(useSceneStore.getState().perspectiveId).toBe('aec-mepfs');
      expect(useSceneStore.getState().preloadedPerspectiveId).toBe('aec-mepfs');
    });

    cleanup();
    perspectiveFetches = [];
    useSceneStore.setState({
      perspectiveId: 'concepts',
      nodes: [],
      edges: [],
      preloadedPerspectiveId: null,
    });

    const secondView = render(
      <MemoryRouter>
        <HomeScreen />
      </MemoryRouter>,
    );

    const aecButtons = await secondView.findAllByRole('button', { name: /AEC-MEPFS Backbone/i });
    const aecPerspective = aecButtons.find((button) =>
      button.textContent?.includes('Default taxonomy-first backbone')
    );
    expect(aecPerspective).toBeTruthy();
    fireEvent.click(aecPerspective!);

    await waitFor(() => {
      expect(perspectiveFetches).toContain('aec-mepfs');
      expect(useSceneStore.getState().perspectiveId).toBe('aec-mepfs');
      expect(useSceneStore.getState().preloadedPerspectiveId).toBe('aec-mepfs');
    });
  });
  test('node query parameter populates the inspector content', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore?node=taxonomy-fire-life-safety']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(view.getByTestId('location-probe').textContent).toContain('node=taxonomy-fire-life-safety');
      expect(view.getByText('Path Tracing')).toBeTruthy();
      expect(view.getByText('Path Tracing')).toBeTruthy();
    });
  });

  test('direct graph-style selection without node query parameter stays selected and populates inspector', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(useSceneStore.getState().nodes.some((node) => node.id === 'taxonomy-fire-life-safety')).toBe(true);
    });

    act(() => {
      const store = useSceneStore.getState();
      store.setSelectedNode('taxonomy-fire-life-safety');
      store.openInspector();
    });

    await waitFor(() => {
      expect(useSceneStore.getState().selectedNodeId).toBe('taxonomy-fire-life-safety');
      expect(view.getByText('Path Tracing')).toBeTruthy();
      expect(view.getByTestId('location-probe').textContent).toContain('node=taxonomy-fire-life-safety');
    });
  });

  test('perspective menu selection persists and syncs to the URL', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(view.getAllByRole('button', { name: /AEC-MEPFS Backbone/i }).length).toBeGreaterThan(0);
    });

    const perspectiveButtons = view.getAllByRole('button', { name: /AEC-MEPFS Backbone/i });
    const perspectiveSwitcher = perspectiveButtons.find((button) => button.getAttribute('aria-haspopup') === 'menu');
    expect(perspectiveSwitcher).toBeTruthy();
    fireEvent.click(perspectiveSwitcher!);
    fireEvent.click(await view.findByRole('menuitemradio', { name: /Concepts Only/i }));

    await waitFor(() => {
      expect(useSceneStore.getState().perspectiveId).toBe('concepts');
      expect(view.getByRole('button', { name: /Concepts Only/i })).toBeTruthy();
      expect(view.getByTestId('location-probe').textContent).toContain('perspective=concepts');
    });
  });

  test('legacy graph remains reachable from the AEC-MEPFS default perspective menu', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(useSceneStore.getState().perspectiveId).toBe('aec-mepfs');
      expect(perspectiveFetches).toContain('aec-mepfs');
    });

    const perspectiveSwitcher = view
      .getAllByRole('button', { name: /AEC-MEPFS Backbone/i })
      .find((button) => button.getAttribute('aria-haspopup') === 'menu');
    expect(perspectiveSwitcher).toBeTruthy();
    fireEvent.click(perspectiveSwitcher!);
    fireEvent.click(await view.findByRole('menuitemradio', { name: /Legacy Knowledge Snapshot/i }));

    await waitFor(() => {
      expect(useSceneStore.getState().perspectiveId).toBe('default');
      expect(perspectiveFetches).toContain('default');
      expect(view.getByRole('button', { name: /Legacy Knowledge Snapshot/i })).toBeTruthy();
      expect(view.getByTestId('location-probe').textContent).toContain('perspective=default');
    });

    expect(backboneFetchCount).toBe(0);
    expect(backboneTaxonomyFetchCount).toBe(0);
  });

  test('inspector header column owns the sidebar summary and toggle', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    const maximizeButton = await view.findByLabelText('Maximize inspector');
    fireEvent.click(maximizeButton);

    await waitFor(() => {
      expect(useSceneStore.getState().inspectorOpen).toBe(true);
      expect(view.getByText('Inspector')).toBeTruthy();
      expect(view.getByText('1 nodes · 0 edges')).toBeTruthy();
      expect(view.getByText('Network Layout · 1 filters')).toBeTruthy();
      expect(view.getByLabelText('Minimize inspector')).toBeTruthy();
    });

    fireEvent.click(view.getByLabelText('Minimize inspector'));
    expect(useSceneStore.getState().inspectorOpen).toBe(false);
  });

  test('AEC-MEPFS preview is opt-in and does not replace the graph state', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(useSceneStore.getState().nodes.some((node) => node.id === 'taxonomy-fire-life-safety')).toBe(true);
      expect(view.queryByLabelText('AEC-MEPFS Backbone preview')).toBeNull();
    });

    expect(backboneFetchCount).toBe(0);
    expect(backboneTaxonomyFetchCount).toBe(0);
    expect(backbonePlacementQaFetchCount).toBe(0);
    expect(backboneEvidenceFetchCount).toBe(0);
    expect(useSceneStore.getState().perspectiveId).toBe('aec-mepfs');

    fireEvent.click(view.getByLabelText('Toggle AEC-MEPFS Backbone preview'));

    await waitFor(() => {
      expect(view.getByLabelText('AEC-MEPFS Backbone preview')).toBeTruthy();
      expect(view.getByText('Run: TEST_RUN')).toBeTruthy();
    });

    expect(backboneFetchCount).toBe(1);
    expect(backboneTaxonomyFetchCount).toBe(0);
    expect(backbonePlacementQaFetchCount).toBe(0);
    expect(backboneEvidenceFetchCount).toBe(0);

    fireEvent.click(view.getByLabelText('Load taxonomy readiness details'));

    await waitFor(() => {
      expect(view.getByText('Canonical tree: available')).toBeTruthy();
      expect(view.getByText('ARC.SPC - Spatial Planning')).toBeTruthy();
      expect(view.getByText('ARC -> ARC.SPC')).toBeTruthy();
      expect(view.getByText('hierarchy')).toBeTruthy();
    });

    expect(backboneTaxonomyFetchCount).toBe(1);
    expect(backbonePlacementQaFetchCount).toBe(0);
    expect(backboneEvidenceFetchCount).toBe(0);

    fireEvent.click(view.getByLabelText('Load placement QA summary'));

    await waitFor(() => {
      expect(view.getByText('QA run: TEST_QA_RUN')).toBeTruthy();
      expect(view.getByText('3/3')).toBeTruthy();
      expect(view.getByText('No live graph adoption')).toBeTruthy();
    });

    expect(backbonePlacementQaFetchCount).toBe(1);

    fireEvent.click(view.getByLabelText('Load evidence summary'));

    await waitFor(() => {
      expect(view.getByText('Evidence run: TEST_EVIDENCE_RUN')).toBeTruthy();
      expect(view.getByText('Producer Report')).toBeTruthy();
      expect(view.getByText('No runtime promotion')).toBeTruthy();
      expect(view.getByText('Route policy: Guarded Default Off')).toBeTruthy();
      expect(view.getByText('Threshold disposition: Not Evaluated Shadow File Backed Only')).toBeTruthy();
      expect(view.getByText('Freshness fields: available')).toBeTruthy();
      expect(view.getByText('Source dirty: no')).toBeTruthy();
      expect(view.getByText('Evidence dirty: yes')).toBeTruthy();
    });

    expect(backboneEvidenceFetchCount).toBe(1);

    fireEvent.click(view.getByLabelText('Refresh backbone preview'));

    await waitFor(() => {
      expect(view.getAllByText('Not loaded')).toHaveLength(3);
      expect(view.queryByText('Canonical tree: available')).toBeNull();
      expect(view.queryByText('QA run: TEST_QA_RUN')).toBeNull();
      expect(view.queryByText('Evidence run: TEST_EVIDENCE_RUN')).toBeNull();
    });

    expect(backboneFetchCount).toBe(2);
    expect(backboneTaxonomyFetchCount).toBe(1);
    expect(backbonePlacementQaFetchCount).toBe(1);
    expect(backboneEvidenceFetchCount).toBe(1);
    expect(useSceneStore.getState().perspectiveId).toBe('aec-mepfs');
    expect(useSceneStore.getState().nodes).toEqual([
      { id: 'taxonomy-fire-life-safety', label: 'Fire Life Safety', displayLabel: 'Fire Life Safety', type: 'taxonomy' },
    ]);
    expect(useSceneStore.getState().edges).toEqual([]);
  });

  test('inspector minimize persists for the same selection and reopens for a new selection', async () => {
    const { ExploreView } = await import('./App');

    const view = render(
      <MemoryRouter initialEntries={['/explore']}>
        <Routes>
          <Route
            path="/explore"
            element={
              <>
                <ExploreView />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(useSceneStore.getState().nodes.some((node) => node.id === 'taxonomy-fire-life-safety')).toBe(true);
    });

    act(() => {
      useSceneStore.getState().setSelectedNode('taxonomy-fire-life-safety');
    });

    await waitFor(() => {
      expect(useSceneStore.getState().inspectorOpen).toBe(true);
      expect(view.getByLabelText('Minimize inspector')).toBeTruthy();
    });

    fireEvent.click(view.getByLabelText('Minimize inspector'));

    await waitFor(() => {
      expect(useSceneStore.getState().inspectorOpen).toBe(false);
      expect(view.getByLabelText('Maximize inspector')).toBeTruthy();
    });

    act(() => {
      useSceneStore.getState().setSelectedNode('concept-building-permit');
    });

    await waitFor(() => {
      expect(useSceneStore.getState().selectedNodeId).toBe('concept-building-permit');
      expect(useSceneStore.getState().inspectorOpen).toBe(true);
    });
  });
});
