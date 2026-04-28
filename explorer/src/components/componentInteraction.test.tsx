import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { act, cleanup, fireEvent, render } from '@testing-library/react';
import { JSDOM } from 'jsdom';
import PerspectiveSwitcher from './command-bar/PerspectiveSwitcher';
import SearchCombobox from './command-bar/SearchCombobox';
import SceneMenu from './command-bar/SceneMenu';
import FiltersPanel from './explorer-rail/FiltersPanel';
import LayoutMenu from './graph/LayoutMenu';
import { DEFAULT_GRAPH_LAYOUT_SPREAD, MAX_GRAPH_LAYOUT_SPREAD, MIN_GRAPH_LAYOUT_SPREAD } from './graph/layoutSpread';
import { getGraphLayoutLabel } from './graph/layoutOptions';
import QueryTemplatesSection from './query-panel/QueryTemplatesSection';
import StoredQueriesSection from './query-panel/StoredQueriesSection';
import NodeInspector from './inspector/NodeInspector';
import BackbonePreviewPanel from './explorer-rail/BackbonePreviewPanel';
import { useSceneStore } from '../stores/useSceneStore';
import type {
  BackboneEvidencePreview,
  BackbonePlacementQaPreview,
  BackboneSummary,
  BackboneTaxonomyPreview,
} from '../types';

let dom: JSDOM;

beforeEach(() => {
  dom = new JSDOM('<!doctype html><html><body></body></html>');
  globalThis.window = dom.window as typeof globalThis.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.navigator = dom.window.navigator as Navigator;
});

afterEach(() => {
  cleanup();
});

function sampleBackboneSummary(): BackboneSummary {
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

function sampleBackboneTaxonomyPreview(): BackboneTaxonomyPreview {
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
      { category: 'applicability', count: 4, predicates: ['constrains', 'governs'] },
    ],
    predicates: [
      {
        predicate: 'broader_than',
        category: 'hierarchy',
        direction: 'parent_to_child',
        domainClasses: ['BackboneNode'],
        rangeClasses: ['BackboneNode'],
        allowedStrengthClasses: ['explicit'],
        evidenceRequiredFields: ['source_id'],
        owner: 'Philip Lewis',
      },
    ],
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
        maxDepth: 3,
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
      { sourceRightsClass: 'metadata_crosswalk', count: 16 },
    ],
    clearanceStates: [
      { clearanceState: 'planning_reference_only', count: 10 },
      { clearanceState: 'metadata_crosswalk_planned', count: 15 },
    ],
    sourceFamilies: [
      {
        sourceId: 'SRC-ISO-12006-2',
        sourceFamily: 'ISO 12006-2',
        publisherAuthority: 'ISO',
        sourceRightsClass: 'reference_only',
        clearanceState: 'planning_reference_only',
        declaredUseBoundary: 'no standards text, table, figure, or clause ingest',
        currentnessCheckDate: '2026-04-25',
        stewardOwner: 'Philip Lewis',
        updateCadence: 'before source admission',
      },
    ],
    artifactPaths: sampleBackboneSummary().artifactPaths,
  };
}

function sampleBackbonePlacementQaPreview(): BackbonePlacementQaPreview {
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
      warnings: ['fixture uses shadow-only placement cases'],
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

function sampleBackboneEvidencePreview(): BackboneEvidencePreview {
  return {
    schemaVersion: 'aec-bb-shadow-v2-backbone-evidence-preview/v1',
    source: 'file-backed-shadow-evidence-manifest',
    status: 'shadow_ready',
    reportOk: true,
    runId: 'TEST_EVIDENCE_RUN',
    summary: {
      artifactCount: 9,
      shadowGraphCounts: {
        nodes: 984,
        edges: 960,
        roots: 24,
        maxDepth: 3,
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

describe('explorer component interactions', () => {
  test('BackbonePreviewPanel renders the shadow summary and runtime boundaries', () => {
    const view = render(
      <BackbonePreviewPanel
        summary={sampleBackboneSummary()}
        loading={false}
        error={null}
        onRefresh={() => {}}
        taxonomyPreview={null}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={() => {}}
        placementQaPreview={null}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={() => {}}
        evidencePreview={null}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={() => {}}
      />,
    );

    expect(view.getByText('AEC-MEPFS')).toBeTruthy();
    expect(view.getByText('Predicates')).toBeTruthy();
    expect(view.getByText('12')).toBeTruthy();
    expect(view.getByText('Sources')).toBeTruthy();
    expect(view.getByText('29')).toBeTruthy();
    expect(view.getByText('Nodes')).toBeTruthy();
    expect(view.getByText('No live graph writes')).toBeTruthy();
    expect(view.getByText('No live Explorer mutation')).toBeTruthy();
    expect(view.getByText('Content ingest: 0')).toBeTruthy();
    expect(view.getByText('Run: TEST_RUN')).toBeTruthy();
    expect(view.getByText('Readiness details')).toBeTruthy();
    expect(view.getAllByText('Not loaded')).toHaveLength(3);
    expect(view.getByText('Placement QA')).toBeTruthy();
    expect(view.getByText('Evidence summary')).toBeTruthy();
    expect(view.queryByText('QA run: TEST_QA_RUN')).toBeNull();
    expect(view.queryByText('Evidence run: TEST_EVIDENCE_RUN')).toBeNull();
  });

  test('BackbonePreviewPanel renders taxonomy readiness details only when supplied', () => {
    const onLoadTaxonomyPreview = mock(() => {});
    const view = render(
      <BackbonePreviewPanel
        summary={sampleBackboneSummary()}
        loading={false}
        error={null}
        onRefresh={() => {}}
        taxonomyPreview={sampleBackboneTaxonomyPreview()}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={onLoadTaxonomyPreview}
        placementQaPreview={null}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={() => {}}
        evidencePreview={null}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={() => {}}
      />,
    );

    expect(view.getByText('Loaded')).toBeTruthy();
    expect(view.getByText('Canonical tree: available')).toBeTruthy();
    expect(view.getByText('Backbone nodes')).toBeTruthy();
    expect(view.getByText('Admitted preview')).toBeTruthy();
    expect(view.getByText('ARC.SPC - Spatial Planning')).toBeTruthy();
    expect(view.getByText('Shadow graph')).toBeTruthy();
    expect(view.getByText('ARC -> ARC.SPC')).toBeTruthy();
    expect(view.getByText('Predicate categories')).toBeTruthy();
    expect(view.getByText('hierarchy')).toBeTruthy();
    expect(view.getByText('Source clearance')).toBeTruthy();
    expect(view.getByText('planning_reference_only')).toBeTruthy();
    fireEvent.click(view.getByLabelText('Load taxonomy readiness details'));
    expect(onLoadTaxonomyPreview).toHaveBeenCalledTimes(1);
  });

  test('BackbonePreviewPanel loads placement QA only through the explicit control', () => {
    const onLoadPlacementQaPreview = mock(() => {});
    const view = render(
      <BackbonePreviewPanel
        summary={sampleBackboneSummary()}
        loading={false}
        error={null}
        onRefresh={() => {}}
        taxonomyPreview={null}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={() => {}}
        placementQaPreview={null}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={onLoadPlacementQaPreview}
        evidencePreview={null}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={() => {}}
      />,
    );

    expect(view.getByText('Placement QA')).toBeTruthy();
    expect(view.queryByText('QA run: TEST_QA_RUN')).toBeNull();
    fireEvent.click(view.getByLabelText('Load placement QA summary'));
    expect(onLoadPlacementQaPreview).toHaveBeenCalledTimes(1);
  });

  test('BackbonePreviewPanel renders placement QA summary and safety boundaries', () => {
    const view = render(
      <BackbonePreviewPanel
        summary={sampleBackboneSummary()}
        loading={false}
        error={null}
        onRefresh={() => {}}
        taxonomyPreview={null}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={() => {}}
        placementQaPreview={sampleBackbonePlacementQaPreview()}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={() => {}}
        evidencePreview={null}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={() => {}}
      />,
    );

    expect(view.getByText('Placement QA')).toBeTruthy();
    expect(view.getByText('3/3')).toBeTruthy();
    expect(view.getByText('Auto')).toBeTruthy();
    expect(view.getByText('Failed')).toBeTruthy();
    expect(view.getByText('LD-8 auto-accept')).toBeTruthy();
    expect(view.getByText('Legacy labels as aliases')).toBeTruthy();
    expect(view.getByText('No live graph adoption')).toBeTruthy();
    expect(view.getByText('Human Steward Review')).toBeTruthy();
    expect(view.getByText('placement QA remains preview-only')).toBeTruthy();
    expect(view.getByText('QA run: TEST_QA_RUN')).toBeTruthy();
  });

  test('BackbonePreviewPanel loads evidence only through the explicit control', () => {
    const onLoadEvidencePreview = mock(() => {});
    const view = render(
      <BackbonePreviewPanel
        summary={sampleBackboneSummary()}
        loading={false}
        error={null}
        onRefresh={() => {}}
        taxonomyPreview={null}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={() => {}}
        placementQaPreview={null}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={() => {}}
        evidencePreview={null}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={onLoadEvidencePreview}
      />,
    );

    expect(view.getByText('Evidence summary')).toBeTruthy();
    expect(view.queryByText('Evidence run: TEST_EVIDENCE_RUN')).toBeNull();
    fireEvent.click(view.getByLabelText('Load evidence summary'));
    expect(onLoadEvidencePreview).toHaveBeenCalledTimes(1);
  });

  test('BackbonePreviewPanel renders evidence manifest health without input hashes', () => {
    const view = render(
      <BackbonePreviewPanel
        summary={sampleBackboneSummary()}
        loading={false}
        error={null}
        onRefresh={() => {}}
        taxonomyPreview={null}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={() => {}}
        placementQaPreview={null}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={() => {}}
        evidencePreview={sampleBackboneEvidencePreview()}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={() => {}}
      />,
    );

    expect(view.getByText('Evidence summary')).toBeTruthy();
    expect(view.getByText('Files')).toBeTruthy();
    expect(view.getByText('Routes')).toBeTruthy();
    expect(view.getByText('Checks')).toBeTruthy();
    expect(view.getByText('7/7')).toBeTruthy();
    expect(view.getByText('10/10')).toBeTruthy();
    expect(view.getByText('No runtime promotion')).toBeTruthy();
    expect(view.getByText('Resolver routes absent or default-off')).toBeTruthy();
    expect(view.getByText('Runtime thresholds not evaluated')).toBeTruthy();
    expect(view.getByText('Route policy: Guarded Default Off')).toBeTruthy();
    expect(view.getByText('Threshold disposition: Not Evaluated Shadow File Backed Only')).toBeTruthy();
    expect(view.getByText('Producer Report')).toBeTruthy();
    expect(view.getByText('Route Inventory Report')).toBeTruthy();
    expect(view.getByText('Input hashes: 10')).toBeTruthy();
    expect(view.getByText('Freshness fields: available')).toBeTruthy();
    expect(view.getByText('Source dirty: no')).toBeTruthy();
    expect(view.getByText('Source dirty paths: 0')).toBeTruthy();
    expect(view.getByText('Evidence dirty: yes')).toBeTruthy();
    expect(view.getByText('Evidence dirty paths: 2')).toBeTruthy();
    expect(view.getByText('Evidence run: TEST_EVIDENCE_RUN')).toBeTruthy();
    expect(view.queryByText('input_file_hashes_sha256')).toBeNull();
  });

  test('BackbonePreviewPanel renders an error state and refresh action', () => {
    const onRefresh = mock(() => {});
    const view = render(
      <BackbonePreviewPanel
        summary={null}
        loading={false}
        error="Shadow backbone report unavailable"
        onRefresh={onRefresh}
        taxonomyPreview={null}
        taxonomyLoading={false}
        taxonomyError={null}
        onLoadTaxonomyPreview={() => {}}
        placementQaPreview={null}
        placementQaLoading={false}
        placementQaError={null}
        onLoadPlacementQaPreview={() => {}}
        evidencePreview={null}
        evidenceLoading={false}
        evidenceError={null}
        onLoadEvidencePreview={() => {}}
      />,
    );

    expect(view.getByText('Preview unavailable')).toBeTruthy();
    expect(view.getByText('Shadow backbone report unavailable')).toBeTruthy();
    fireEvent.click(view.getByLabelText('Refresh backbone preview'));
    expect(onRefresh).toHaveBeenCalledTimes(1);
  });

  test('PerspectiveSwitcher calls onSelect for the chosen perspective', () => {
    const onSelect = mock(() => {});
    const view = render(
      <PerspectiveSwitcher
        activePerspectiveName="All Knowledge"
        perspectiveId="default"
        perspectives={[
          { id: 'default', name: 'All Knowledge', description: 'Everything' },
          { id: 'concepts', name: 'Concepts Only', description: 'Concept graph' },
        ]}
        showPerspectives
        onToggle={() => {}}
        onClose={() => {}}
        onSelect={onSelect}
      />,
    );

    fireEvent.click(view.getByText('Concepts Only'));
    expect(onSelect).toHaveBeenCalledWith('concepts');
  });

  test('SearchCombobox calls onSelect when a result is clicked', () => {
    const onSelect = mock(() => {});
    const view = render(
      <SearchCombobox
        query="fire"
        results={[
          { id: 'taxonomy-fire-life-safety', kind: 'node', label: 'Fire Life Safety', type: 'taxonomy', matchType: 'slug', matchedField: 'slug' },
        ]}
        searching={false}
        showSuggestions
        highlighted={0}
        inputRef={{ current: null }}
        onQueryChange={() => {}}
        onKeyDown={() => {}}
        onFocus={() => {}}
        onClear={() => {}}
        onClose={() => {}}
        onHighlight={() => {}}
        onSelect={onSelect}
        getResultDotClass={() => 'bg-node-taxonomy'}
      />,
    );

    fireEvent.click(view.getByText('Fire Life Safety'));
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'taxonomy-fire-life-safety' }));
  });

  test('SearchCombobox renders compact display labels while preserving selected result identity', () => {
    const onSelect = mock(() => {});
    const longLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    const view = render(
      <SearchCombobox
        query="permit"
        results={[
          {
            id: 'rule-long-1',
            kind: 'node',
            label: longLabel,
            displayLabel: 'Rule · Building permit documentation…',
            type: 'rule',
            matchType: 'label',
            matchedField: 'label',
          },
        ]}
        searching={false}
        showSuggestions
        highlighted={0}
        inputRef={{ current: null }}
        onQueryChange={() => {}}
        onKeyDown={() => {}}
        onFocus={() => {}}
        onClear={() => {}}
        onClose={() => {}}
        onHighlight={() => {}}
        onSelect={onSelect}
        getResultDotClass={() => 'bg-node-rule'}
      />,
    );

    expect(view.getByText('Rule · Building permit documentation…')).toBeTruthy();
    expect(view.queryByText(longLabel)).toBeNull();
    fireEvent.click(view.getByText('Rule · Building permit documentation…'));
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'rule-long-1', label: longLabel }));
  });

  test('NodeInspector opens on overview and shows compact title, full label, canonical ID, sources, relationships, and metadata tabs', () => {
    const longLabel = 'Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.';
    useSceneStore.setState({ pinnedNodeIds: [], pathSourceId: null, pathTargetId: null, highlightedPath: null });

    const view = render(
      <NodeInspector
        detail={{
          node: {
            id: 'rule-long-1',
            label: longLabel,
            displayLabel: 'Rule · Building permit documentation…',
            type: 'rule',
            confidence: 0.91,
            status: 'accepted',
          },
          taxonomyPath: [],
          incoming: [],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    expect(view.getByText('Rule · Building permit documentation…')).toBeTruthy();
    expect(view.getByText(longLabel)).toBeTruthy();
    expect(view.getByText('rule-long-1')).toBeTruthy();
    expect(view.getByText('Overview')).toBeTruthy();
    expect(view.getByText('Relationships')).toBeTruthy();
    expect(view.getByText('Sources')).toBeTruthy();
    expect(view.getByText('Metadata')).toBeTruthy();

    fireEvent.click(view.getByText('Relationships'));
    expect(view.getByText('No relationships are available for this node.')).toBeTruthy();
    expect(view.getByText('No incoming relationships.')).toBeTruthy();
    expect(view.getByText('No outgoing relationships.')).toBeTruthy();

    fireEvent.click(view.getByText('Sources'));
    expect(view.getByText('No source materials are linked to this node.')).toBeTruthy();

    fireEvent.click(view.getByText('Metadata'));
    expect(view.getByText('Canonical ID')).toBeTruthy();
    expect(view.getByText('Type')).toBeTruthy();
    expect(view.getByText('Status')).toBeTruthy();
  });

  test('NodeInspector exposes unpin and clear-isolation actions', async () => {
    const writeText = mock(() => Promise.resolve());
    Object.defineProperty(globalThis.navigator, 'clipboard', {
      value: { writeText },
      configurable: true,
    });

    useSceneStore.setState({
      pinnedNodeIds: ['rule-long-1'],
      hiddenNodeIds: ['other-node'],
      showAllRequestId: 0,
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: {
            id: 'rule-long-1',
            label: 'Every building permit applicant must submit complete documentation.',
            displayLabel: 'Building Permit Rule',
            type: 'rule',
          },
          taxonomyPath: [],
          incoming: [{ relType: 'DEFINED_BY', other: { id: 'concept-building-permit', label: 'Building Permit', type: 'concept' } }],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    fireEvent.click(view.getByLabelText('Unpin node'));
    expect(useSceneStore.getState().pinnedNodeIds).toEqual([]);

    fireEvent.click(view.getByLabelText('Clear node isolation'));
    expect(useSceneStore.getState().showAllRequestId).toBe(1);

    await act(async () => {
      fireEvent.click(view.getByLabelText('Copy node name'));
    });
    expect(writeText).toHaveBeenCalledWith('Building Permit Rule');

    fireEvent.click(view.getByText('Relationships'));
    await act(async () => {
      fireEvent.click(view.getByLabelText('Copy incoming node name'));
    });
    expect(writeText).toHaveBeenCalledWith('Building Permit');
  });

  test('SceneMenu calls scene actions', () => {
    const onOpenScene = mock(() => {});
    const onRenameScene = mock(() => {});
    const onDeleteScene = mock(() => {});
    const view = render(
      <SceneMenu
        activeSceneId={null}
        activeSceneName={null}
        sceneFilter=""
        showScenes
        filteredScenes={[{ id: 'scene-1', name: 'My Scene', perspectiveId: 'default', savedAt: '2026-04-23T00:00:00Z' }]}
        deletingSceneId={null}
        onToggle={() => {}}
        onClose={() => {}}
        onSceneFilterChange={() => {}}
        onOpenScene={onOpenScene}
        onRenameScene={onRenameScene}
        onDeleteScene={onDeleteScene}
      />,
    );

    fireEvent.click(view.getByText('My Scene'));
    fireEvent.click(view.getByText('Rename'));
    fireEvent.click(view.getByText('Delete'));
    expect(onOpenScene).toHaveBeenCalledWith('scene-1');
    expect(onRenameScene).toHaveBeenCalledTimes(1);
    expect(onDeleteScene).toHaveBeenCalledTimes(1);
  });

  test('FiltersPanel dispatches toggle and selection callbacks', () => {
    const onSelectColorScheme = mock(() => {});
    const onSelectSizeBy = mock(() => {});
    const onToggleNodeType = mock(() => {});
    const onToggleEdgeType = mock(() => {});
    const view = render(
      <FiltersPanel
        colorScheme="default"
        sizeBy="uniform"
        visibleNodeTypes={new Set(['concept'])}
        visibleEdgeTypes={new Set(['RELATED_TO'])}
        colorSchemes={[{ key: 'default', label: 'Default' }, { key: 'pastel', label: 'Pastel' }]}
        sizeOptions={[{ key: 'uniform', label: 'Uniform' }, { key: 'degree', label: 'By Connectivity' }]}
        nodeTypes={[{ key: 'concept', label: 'Concept', color: 'bg-node-concept' }]}
        edgeTypes={[{ key: 'RELATED_TO', label: 'RELATED_TO' }]}
        onSelectColorScheme={onSelectColorScheme}
        onSelectSizeBy={onSelectSizeBy}
        onToggleNodeType={onToggleNodeType}
        onToggleEdgeType={onToggleEdgeType}
      />,
    );

    fireEvent.click(view.getByText('Pastel'));
    fireEvent.click(view.getByText('By Connectivity'));
    fireEvent.click(view.getByLabelText('Concept'));
    fireEvent.click(view.getByLabelText('RELATED_TO'));
    expect(onSelectColorScheme).toHaveBeenCalledWith('pastel');
    expect(onSelectSizeBy).toHaveBeenCalledWith('degree');
    expect(onToggleNodeType).toHaveBeenCalledWith('concept');
    expect(onToggleEdgeType).toHaveBeenCalledWith('RELATED_TO');
  });

  test('LayoutMenu exposes readable graph layout choices', () => {
    const onSelect = mock(() => {});
    const view = render(
      <LayoutMenu
        layout="forceatlas2"
        open
        onToggle={() => {}}
        onClose={() => {}}
        onSelect={onSelect}
      />,
    );

    expect(getGraphLayoutLabel('forceatlas2')).toBe('Network Layout');
    expect(view.getAllByText('Network Layout').length).toBe(2);
    expect(view.getByText('Taxonomy Clusters')).toBeTruthy();
    fireEvent.click(view.getByText('Taxonomy Clusters'));
    expect(onSelect).toHaveBeenCalledWith('clustered');
  });

  test('scene store keeps an interactive graph spread control value with documented reset bounds', () => {
    useSceneStore.setState({ layoutSpread: DEFAULT_GRAPH_LAYOUT_SPREAD });

    act(() => {
      useSceneStore.getState().setLayoutSpread(2.1);
    });

    expect(useSceneStore.getState().layoutSpread).toBe(2.1);
    expect(MIN_GRAPH_LAYOUT_SPREAD).toBe(0.75);
    expect(MAX_GRAPH_LAYOUT_SPREAD).toBe(2.5);

    act(() => {
      useSceneStore.getState().setLayoutSpread(DEFAULT_GRAPH_LAYOUT_SPREAD);
    });

    expect(useSceneStore.getState().layoutSpread).toBe(DEFAULT_GRAPH_LAYOUT_SPREAD);
  });

  test('QueryTemplatesSection dispatches select and run callbacks', () => {
    const onSelectTemplate = mock(() => {});
    const onRunTemplate = mock(() => {});
    const view = render(
      <QueryTemplatesSection
        templates={[{ label: 'All rules', query: 'MATCH (n) RETURN n' }]}
        onSelectTemplate={onSelectTemplate}
        onRunTemplate={onRunTemplate}
      />,
    );

    fireEvent.click(view.getByText('All rules'));
    fireEvent.click(view.getByText('Run'));
    expect(onSelectTemplate).toHaveBeenCalledWith('MATCH (n) RETURN n');
    expect(onRunTemplate).toHaveBeenCalledWith('MATCH (n) RETURN n');
  });

  test('StoredQueriesSection dispatches select and delete callbacks', () => {
    const onSelect = mock(() => {});
    const onDelete = mock(() => {});
    const view = render(
      <StoredQueriesSection
        title="Saved Queries"
        icon={<span>icon</span>}
        queries={['MATCH (n) RETURN n LIMIT 10']}
        onSelect={onSelect}
        onDelete={onDelete}
      />,
    );

    fireEvent.click(view.getByText('MATCH (n) RETURN n LIMIT 10'));
    fireEvent.click(view.getByTitle('Delete saved querie'));
    expect(onSelect).toHaveBeenCalledWith('MATCH (n) RETURN n LIMIT 10');
    expect(onDelete).toHaveBeenCalledWith('MATCH (n) RETURN n LIMIT 10');
  });
});
