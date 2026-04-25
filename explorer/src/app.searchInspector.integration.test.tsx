import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { act, cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import React from 'react';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { useSceneStore } from './stores/useSceneStore';

let dom: JSDOM;
let backboneFetchCount = 0;
let backboneTaxonomyFetchCount = 0;

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
      canonicalTaxonomyTreeAvailable: false,
      backboneNodesAvailable: false,
      previewCompleteness: 'registry_metadata_only',
      limitation: 'Registry metadata only.',
    },
    predicateCategories: [
      { category: 'hierarchy', count: 2, predicates: ['broader_than', 'narrower_than'] },
    ],
    predicates: [],
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
  useSceneStore.setState({
    perspectiveId: 'default',
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
    { id: 'default', name: 'All Knowledge', description: 'Everything', nodeCount: 88 },
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
  getNodesForPerspective: async () => ({
    nodes: [{ id: 'taxonomy-fire-life-safety', label: 'Fire Life Safety', displayLabel: 'Fire Life Safety', type: 'taxonomy' }],
    edges: [],
  }),
  getTaxonomy: async () => ([]),
  getNode: async () => ({
    node: { id: 'taxonomy-fire-life-safety', label: 'Fire Life Safety', displayLabel: 'Fire Life Safety', type: 'taxonomy' },
    taxonomyPath: [],
    incoming: [],
    outgoing: [],
    evidence: [],
  }),
  getEdgeDetail: async () => { throw new Error('not used'); },
  tracePath: async () => ({ paths: [] }),
  runCypherQuery: async () => ({ nodes: [], edges: [], recordCount: 0, rows: [] }),
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
      expect(view.getByRole('button', { name: /All Knowledge/i })).toBeTruthy();
    });

    fireEvent.click(view.getByRole('button', { name: /All Knowledge/i }));
    fireEvent.click(await view.findByRole('menuitemradio', { name: /Concepts Only/i }));

    await waitFor(() => {
      expect(useSceneStore.getState().perspectiveId).toBe('concepts');
      expect(view.getByRole('button', { name: /Concepts Only/i })).toBeTruthy();
      expect(view.getByTestId('location-probe').textContent).toContain('perspective=concepts');
    });
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
    expect(useSceneStore.getState().perspectiveId).toBe('default');

    fireEvent.click(view.getByLabelText('Toggle AEC-MEPFS Backbone preview'));

    await waitFor(() => {
      expect(view.getByLabelText('AEC-MEPFS Backbone preview')).toBeTruthy();
      expect(view.getByText('Run: TEST_RUN')).toBeTruthy();
    });

    expect(backboneFetchCount).toBe(1);
    expect(backboneTaxonomyFetchCount).toBe(0);

    fireEvent.click(view.getByLabelText('Load taxonomy readiness details'));

    await waitFor(() => {
      expect(view.getByText('Canonical tree: not admitted yet')).toBeTruthy();
      expect(view.getByText('hierarchy')).toBeTruthy();
    });

    expect(backboneTaxonomyFetchCount).toBe(1);

    fireEvent.click(view.getByLabelText('Refresh backbone preview'));

    await waitFor(() => {
      expect(view.getByText('Not loaded')).toBeTruthy();
      expect(view.queryByText('Canonical tree: not admitted yet')).toBeNull();
    });

    expect(backboneFetchCount).toBe(2);
    expect(backboneTaxonomyFetchCount).toBe(1);
    expect(useSceneStore.getState().perspectiveId).toBe('default');
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
