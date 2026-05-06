import { afterEach, beforeEach, describe, expect, mock, test } from "bun:test";
import { act, cleanup, fireEvent, render } from "@testing-library/react";
import { JSDOM } from "jsdom";
import PerspectiveSwitcher from "./command-bar/PerspectiveSwitcher";
import SearchCombobox from "./command-bar/SearchCombobox";
import SceneMenu from "./command-bar/SceneMenu";
import { buildScopedEdgeTypes } from "./ExplorerRail";
import FiltersPanel from "./explorer-rail/FiltersPanel";
import LayoutMenu from "./graph/LayoutMenu";
import {
  DEFAULT_GRAPH_LAYOUT_SPREAD,
  MAX_GRAPH_LAYOUT_SPREAD,
  MIN_GRAPH_LAYOUT_SPREAD,
} from "./graph/layoutSpread";
import {
  DEFAULT_EXPLORER_PANEL_WIDTH,
  DEFAULT_INSPECTOR_PANEL_WIDTH,
  MAX_SIDE_PANEL_WIDTH,
  MIN_SIDE_PANEL_WIDTH,
} from "../utils/resizablePanels";
import { getGraphLayoutLabel } from "./graph/layoutOptions";
import QueryTemplatesSection from "./query-panel/QueryTemplatesSection";
import StoredQueriesSection from "./query-panel/StoredQueriesSection";
import NodeInspector from "./inspector/NodeInspector";
import BackbonePreviewPanel from "./explorer-rail/BackbonePreviewPanel";
import { collectExpandableTreeIds } from "./explorer-rail/treeExpansion";
import { useSceneStore } from "../stores/useSceneStore";
import type {
  BackboneEvidencePreview,
  BackbonePlacementQaPreview,
  BackboneSummary,
  BackboneTaxonomyPreview,
  TaxonomyNode,
} from "../types";

let dom: JSDOM;

beforeEach(() => {
  dom = new JSDOM("<!doctype html><html><body></body></html>");
  globalThis.window = dom.window as typeof globalThis.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.navigator = dom.window.navigator as Navigator;
  globalThis.HTMLCanvasElement = dom.window.HTMLCanvasElement;
  dom.window.HTMLCanvasElement.prototype.getContext = () => ({
    clearRect: () => {},
    createLinearGradient: () => ({ addColorStop: () => {} }),
    fillRect: () => {},
    fillText: () => {},
    beginPath: () => {},
    arc: () => {},
    fill: () => {},
    strokeRect: () => {},
  }) as unknown as CanvasRenderingContext2D;
});

afterEach(() => {
  cleanup();
});

function sampleBackboneSummary(): BackboneSummary {
  return {
    schemaVersion: "aec-bb-shadow-v2-backbone-summary/v1",
    source: "file-backed-shadow-staging-consumer-report",
    status: "shadow_ready",
    reportOk: true,
    runId: "TEST_RUN",
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
      artifact: "shadow-backbone-staging.json",
      shadowGraph: "shadow-backbone-graph.json",
      producerReport: "shadow-staging-report.json",
      consumerReport: "shadow-staging-consumer-report.json",
    },
  };
}

function sampleBackboneTaxonomyPreview(): BackboneTaxonomyPreview {
  return {
    schemaVersion: "aec-bb-shadow-v2-backbone-taxonomy-preview/v1",
    source: "file-backed-shadow-staging-artifact",
    status: "shadow_ready",
    reportOk: true,
    runId: "TEST_RUN",
    counts: sampleBackboneSummary().counts,
    boundaries: sampleBackboneSummary().boundaries,
    noIngestBoundaryCoverage: sampleBackboneSummary().noIngestBoundaryCoverage,
    readiness: {
      registryMetadataAvailable: true,
      canonicalTaxonomyTreeAvailable: true,
      backboneNodesAvailable: true,
      shadowGraphAvailable: true,
      previewCompleteness: "registry_metadata_admitted_nodes_and_shadow_graph",
      limitation: "Shadow graph rows are preview-only.",
    },
    predicateCategories: [
      {
        category: "hierarchy",
        count: 2,
        predicates: ["broader_than", "narrower_than"],
      },
      {
        category: "applicability",
        count: 4,
        predicates: ["constrains", "governs"],
      },
    ],
    predicates: [
      {
        predicate: "broader_than",
        category: "hierarchy",
        direction: "parent_to_child",
        domainClasses: ["BackboneNode"],
        rangeClasses: ["BackboneNode"],
        allowedStrengthClasses: ["explicit"],
        evidenceRequiredFields: ["source_id"],
        owner: "Philip Lewis",
      },
    ],
    backboneNodes: [
      {
        id: "VTN-DOM-0000001",
        canonicalId: "VTN-DOM-0000001",
        label: "Architecture",
        prefLabel: "Architecture",
        pathCode: "ARC",
        level: 1,
        parentPathCode: "",
        reviewStatus: "steward_admitted",
        steward: "Philip Lewis",
        releaseVersion: "0.1.0",
      },
      {
        id: "VTN-DOM-0000002",
        canonicalId: "VTN-DOM-0000002",
        label: "Spatial Planning",
        prefLabel: "Spatial Planning",
        pathCode: "ARC.SPC",
        level: 2,
        parentPathCode: "ARC",
        reviewStatus: "steward_admitted",
        steward: "Philip Lewis",
        releaseVersion: "0.1.0",
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
          id: "VTN-DOM-0000001",
          label: "Architecture",
          pathCode: "ARC",
          level: 1,
          parentPathCode: "",
        },
        {
          id: "VTN-DOM-0000002",
          label: "Spatial Planning",
          pathCode: "ARC.SPC",
          level: 2,
          parentPathCode: "ARC",
        },
      ],
      edges: [
        {
          id: "VTN-DOM-0000001--broader_than--VTN-DOM-0000002",
          fromId: "VTN-DOM-0000001",
          toId: "VTN-DOM-0000002",
          predicate: "broader_than",
          fromPathCode: "ARC",
          toPathCode: "ARC.SPC",
        },
      ],
    },
    sourceRightsClasses: [
      { sourceRightsClass: "reference_only", count: 13 },
      { sourceRightsClass: "metadata_crosswalk", count: 16 },
    ],
    clearanceStates: [
      { clearanceState: "planning_reference_only", count: 10 },
      { clearanceState: "metadata_crosswalk_planned", count: 15 },
    ],
    sourceFamilies: [
      {
        sourceId: "SRC-ISO-12006-2",
        sourceFamily: "ISO 12006-2",
        publisherAuthority: "ISO",
        sourceRightsClass: "reference_only",
        clearanceState: "planning_reference_only",
        declaredUseBoundary:
          "no standards text, table, figure, or clause ingest",
        currentnessCheckDate: "2026-04-25",
        stewardOwner: "Philip Lewis",
        updateCadence: "before source admission",
      },
    ],
    artifactPaths: sampleBackboneSummary().artifactPaths,
  };
}

function sampleBackbonePlacementQaPreview(): BackbonePlacementQaPreview {
  return {
    schemaVersion: "aec-bb-shadow-v2-backbone-placement-qa-preview/v1",
    source: "file-backed-placement-qa-report",
    status: "shadow_ready",
    reportOk: true,
    runId: "TEST_QA_RUN",
    fixturePath:
      "scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s2.json",
    reportPath:
      "006_System-Manifests/aec-mepfs-backbone/placement-qa/TEST_QA_RUN/placement-qa-report.json",
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
      warnings: ["fixture uses shadow-only placement cases"],
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
    warnings: ["placement QA remains preview-only"],
  };
}

function sampleBackboneEvidencePreview(): BackboneEvidencePreview {
  return {
    schemaVersion: "aec-bb-shadow-v2-backbone-evidence-preview/v1",
    source: "file-backed-shadow-evidence-manifest",
    status: "shadow_ready",
    reportOk: true,
    runId: "TEST_EVIDENCE_RUN",
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
      resolverRoutePolicy: "guarded_default_off",
      benchmarkRuntimeThresholdDisposition:
        "not_evaluated_shadow_file_backed_only",
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
        label: "producer_report",
        path: "006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-report.json",
        schemaVersion: "aec-bb-shadow-staging-report/v1",
        ok: true,
      },
      {
        label: "route_inventory_report",
        path: "006_System-Manifests/aec-mepfs-backbone/api-route-inventory/TEST_RUN/api-route-inventory-report.json",
        schemaVersion: "aec-bb-api-route-inventory-report/v1",
        ok: true,
      },
    ],
    repoState: {
      gitHeadCommit: "abc123",
      workingTreeDirtyAtGeneration: true,
      freshnessAvailable: true,
      sourceWorkingTreeDirtyAtGeneration: false,
      generatedEvidenceDirtyAtGeneration: true,
      sourceDirtyPathCount: 0,
      generatedEvidenceDirtyPathCount: 2,
    },
    reportPath:
      "006_System-Manifests/aec-mepfs-backbone/evidence-manifest/TEST_EVIDENCE_RUN/shadow-evidence-manifest-report.json",
  };
}

describe("explorer component interactions", () => {
  test("BackbonePreviewPanel renders the shadow summary and runtime boundaries", () => {
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

    expect(view.getByText("AEC-MEPFS")).toBeTruthy();
    expect(view.getByText("Predicates")).toBeTruthy();
    expect(view.getByText("12")).toBeTruthy();
    expect(view.getByText("Sources")).toBeTruthy();
    expect(view.getByText("29")).toBeTruthy();
    expect(view.getByText("Nodes")).toBeTruthy();
    expect(view.getByText("No live graph writes")).toBeTruthy();
    expect(view.getByText("No live Explorer mutation")).toBeTruthy();
    expect(view.getByText("Content ingest: 0")).toBeTruthy();
    expect(view.getByText("Run: TEST_RUN")).toBeTruthy();
    expect(view.getByText("Readiness details")).toBeTruthy();
    expect(view.getAllByText("Not loaded")).toHaveLength(3);
    expect(view.getByText("Placement QA")).toBeTruthy();
    expect(view.getByText("Evidence summary")).toBeTruthy();
    expect(view.queryByText("QA run: TEST_QA_RUN")).toBeNull();
    expect(view.queryByText("Evidence run: TEST_EVIDENCE_RUN")).toBeNull();
  });

  test("BackbonePreviewPanel renders taxonomy readiness details only when supplied", () => {
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

    expect(view.getByText("Loaded")).toBeTruthy();
    expect(view.getByText("Canonical tree: available")).toBeTruthy();
    expect(view.getByText("Backbone nodes")).toBeTruthy();
    expect(view.getByText("Admitted preview")).toBeTruthy();
    expect(view.getByText("ARC.SPC - Spatial Planning")).toBeTruthy();
    expect(view.getByText("Shadow graph")).toBeTruthy();
    expect(view.getByText("ARC -> ARC.SPC")).toBeTruthy();
    expect(view.getByText("Predicate categories")).toBeTruthy();
    expect(view.getByText("hierarchy")).toBeTruthy();
    expect(view.getByText("Source clearance")).toBeTruthy();
    expect(view.getByText("Planning Reference Only")).toBeTruthy();
    expect(view.queryByText("planning_reference_only")).toBeNull();
    fireEvent.click(view.getByLabelText("Load taxonomy readiness details"));
    expect(onLoadTaxonomyPreview).toHaveBeenCalledTimes(1);
  });

  test("BackbonePreviewPanel loads placement QA only through the explicit control", () => {
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

    expect(view.getByText("Placement QA")).toBeTruthy();
    expect(view.queryByText("QA run: TEST_QA_RUN")).toBeNull();
    fireEvent.click(view.getByLabelText("Load placement QA summary"));
    expect(onLoadPlacementQaPreview).toHaveBeenCalledTimes(1);
  });

  test("BackbonePreviewPanel renders placement QA summary and safety boundaries", () => {
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

    expect(view.getByText("Placement QA")).toBeTruthy();
    expect(view.getByText("3/3")).toBeTruthy();
    expect(view.getByText("Auto")).toBeTruthy();
    expect(view.getByText("Failed")).toBeTruthy();
    expect(view.getByText("LD-8 auto-accept")).toBeTruthy();
    expect(view.getByText("Legacy labels as aliases")).toBeTruthy();
    expect(view.getByText("No live graph adoption")).toBeTruthy();
    expect(view.getByText("Human Steward Review")).toBeTruthy();
    expect(view.getByText("placement QA remains preview-only")).toBeTruthy();
    expect(view.getByText("QA run: TEST_QA_RUN")).toBeTruthy();
  });

  test("BackbonePreviewPanel loads evidence only through the explicit control", () => {
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

    expect(view.getByText("Evidence summary")).toBeTruthy();
    expect(view.queryByText("Evidence run: TEST_EVIDENCE_RUN")).toBeNull();
    fireEvent.click(view.getByLabelText("Load evidence summary"));
    expect(onLoadEvidencePreview).toHaveBeenCalledTimes(1);
  });

  test("BackbonePreviewPanel renders evidence manifest health without input hashes", () => {
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

    expect(view.getByText("Evidence summary")).toBeTruthy();
    expect(view.getByText("Files")).toBeTruthy();
    expect(view.getByText("Routes")).toBeTruthy();
    expect(view.getByText("Checks")).toBeTruthy();
    expect(view.getByText("7/7")).toBeTruthy();
    expect(view.getByText("10/10")).toBeTruthy();
    expect(view.getByText("No runtime promotion")).toBeTruthy();
    expect(
      view.getByText("Resolver routes absent or default-off"),
    ).toBeTruthy();
    expect(view.getByText("Runtime thresholds not evaluated")).toBeTruthy();
    expect(view.getByText("Route policy: Guarded Default Off")).toBeTruthy();
    expect(
      view.getByText(
        "Threshold disposition: Not Evaluated Shadow File Backed Only",
      ),
    ).toBeTruthy();
    expect(view.getByText("Producer Report")).toBeTruthy();
    expect(view.getByText("Route Inventory Report")).toBeTruthy();
    expect(view.getByText("Input hashes: 10")).toBeTruthy();
    expect(view.getByText("Freshness fields: available")).toBeTruthy();
    expect(view.getByText("Source dirty: no")).toBeTruthy();
    expect(view.getByText("Source dirty paths: 0")).toBeTruthy();
    expect(view.getByText("Evidence dirty: yes")).toBeTruthy();
    expect(view.getByText("Evidence dirty paths: 2")).toBeTruthy();
    expect(view.getByText("Evidence run: TEST_EVIDENCE_RUN")).toBeTruthy();
    expect(view.queryByText("input_file_hashes_sha256")).toBeNull();
  });

  test("BackbonePreviewPanel renders an error state and refresh action", () => {
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

    expect(view.getByText("Preview unavailable")).toBeTruthy();
    expect(view.getByText("Shadow backbone report unavailable")).toBeTruthy();
    fireEvent.click(view.getByLabelText("Refresh backbone preview"));
    expect(onRefresh).toHaveBeenCalledTimes(1);
  });

  test("PerspectiveSwitcher calls onSelect for the chosen perspective", () => {
    const onSelect = mock(() => {});
    const view = render(
      <PerspectiveSwitcher
        activePerspectiveName="All Knowledge"
        perspectiveId="default"
        perspectives={[
          { id: "default", name: "All Knowledge", description: "Everything" },
          {
            id: "concepts",
            name: "Concepts Only",
            description: "Concept graph",
          },
        ]}
        showPerspectives
        onToggle={() => {}}
        onClose={() => {}}
        onSelect={onSelect}
      />,
    );

    fireEvent.click(view.getByText("Concepts Only"));
    expect(onSelect).toHaveBeenCalledWith("concepts");
  });

  test("SearchCombobox calls onSelect when a result is clicked", () => {
    const onSelect = mock(() => {});
    const view = render(
      <SearchCombobox
        query="fire"
        results={[
          {
            id: "taxonomy-fire-life-safety",
            kind: "node",
            label: "Fire Life Safety",
            type: "taxonomy",
            matchType: "slug",
            matchedField: "slug",
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
        getResultDotClass={() => "bg-node-taxonomy"}
      />,
    );

    fireEvent.click(view.getByText("Fire Life Safety"));
    expect(onSelect).toHaveBeenCalledWith(
      expect.objectContaining({ id: "taxonomy-fire-life-safety" }),
    );
  });

  test("SearchCombobox renders compact display labels while preserving selected result identity", () => {
    const onSelect = mock(() => {});
    const longLabel =
      "Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.";
    const view = render(
      <SearchCombobox
        query="permit"
        results={[
          {
            id: "rule-long-1",
            kind: "node",
            label: longLabel,
            displayLabel: "Rule · Building permit documentation…",
            type: "rule",
            matchType: "label",
            matchedField: "label",
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
        getResultDotClass={() => "bg-node-rule"}
      />,
    );

    expect(
      view.getByText("Rule · Building permit documentation…"),
    ).toBeTruthy();
    expect(view.queryByText(longLabel)).toBeNull();
    fireEvent.click(view.getByText("Rule · Building permit documentation…"));
    expect(onSelect).toHaveBeenCalledWith(
      expect.objectContaining({ id: "rule-long-1", label: longLabel }),
    );
  });

  test("NodeInspector opens on overview and shows compact title, full label, canonical ID, sources, relationships, and metadata tabs", () => {
    const longLabel =
      "Every building permit applicant must submit complete fire safety, structural, zoning, and occupancy documentation before approval can proceed.";
    useSceneStore.setState({
      pinnedNodeIds: [],
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: {
            id: "rule-long-1",
            label: longLabel,
            displayLabel: "Rule · Building permit documentation…",
            type: "rule",
            confidence: 0.91,
            status: "accepted",
          },
          taxonomyPath: [],
          incoming: [],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    expect(
      view.getByText("Rule · Building permit documentation…"),
    ).toBeTruthy();
    expect(view.getByText(longLabel)).toBeTruthy();
    expect(view.getByText("rule-long-1")).toBeTruthy();
    expect(view.getByText("Overview")).toBeTruthy();
    expect(view.getByText("Relationships")).toBeTruthy();
    expect(view.getByText("Sources")).toBeTruthy();
    expect(view.getByText("Metadata")).toBeTruthy();

    fireEvent.click(view.getByText("Relationships"));
    expect(
      view.getByText("No relationships are available for this node."),
    ).toBeTruthy();
    expect(view.getByText("No incoming relationships.")).toBeTruthy();
    expect(view.getByText("No outgoing relationships.")).toBeTruthy();

    fireEvent.click(view.getByText("Sources"));
    expect(
      view.getByText("No source materials are linked to this node."),
    ).toBeTruthy();

    fireEvent.click(view.getByText("Metadata"));
    expect(view.getByText("Canonical ID")).toBeTruthy();
    expect(view.getByText("Type")).toBeTruthy();
    expect(view.getByText("Status")).toBeTruthy();
  });

  test("NodeInspector renders verified resource reference cards in the Sources tab", () => {
    const view = render(
      <NodeInspector
        detail={{
          node: { id: "VTN-DOM-0012777", label: "Structural Wind Load", type: "concept" },
          taxonomyPath: [],
          incoming: [],
          outgoing: [],
          evidence: [],
          resources: [
            {
              linkId: "nrl-wind-load-wbdg-wind",
              resourceId: "res-wbdg-wind-safety-building-envelope",
              nodeId: "VTN-DOM-0012777",
              title: "Wind Safety of the Building Envelope",
              organization: "Whole Building Design Guide",
              publisher: "National Institute of Building Sciences",
              resourceType: "professional_guidance",
              sourceAuthority: "government",
              accessType: "public_web",
              verificationStatus: "link_verified",
              reviewStatus: "accepted",
              relationship: "provides_design_guidance",
              relevanceScore: 0.86,
              authorityScore: 0.9,
              confidenceScore: 0.82,
              displayScore: 0.84,
              rationale:
                "The resource is specifically about wind safety of the building envelope and is relevant contextual guidance for wind load concepts.",
              jurisdiction:
                "United States federal/public design guidance context; not a project-specific wind design criterion.",
              url: "https://www.wbdg.org/resources/wind-safety-building-envelope",
              lastCheckedAt: "2026-05-01T00:00:00.000Z",
            },
            {
              linkId: "nrl-hidden-reviewer-only-candidate",
              resourceId: "res-reviewer-only-asce-candidate",
              nodeId: "VTN-DOM-0012777",
              title: "Reviewer-only ASCE Candidate",
              organization: "ASCE",
              resourceType: "standard_candidate",
              sourceAuthority: "professional_body",
              accessType: "public_web",
              verificationStatus: "unverified",
              reviewStatus: "candidate",
              relationship: "is_supplementary_reference_for",
              relevanceScore: 0.5,
              authorityScore: 0.5,
              confidenceScore: 0.5,
              displayScore: 0.5,
              rationale: "Reviewer-only candidate should not be learner-visible.",
              warning: "Standard context incomplete; reviewer-only candidate.",
            },
          ],
        }}
      />,
    );

    fireEvent.click(view.getByText("Sources"));
    expect(view.getByText("Resources / References")).toBeTruthy();
    expect(view.getByText("Wind Safety of the Building Envelope")).toBeTruthy();
    expect(view.getByText("Professional Guidance")).toBeTruthy();
    expect(view.getByText("Link Verified")).toBeTruthy();
    expect(view.getByText(/relevant contextual guidance/)).toBeTruthy();
    expect(view.getByText("Open online")).toBeTruthy();
    expect(view.queryByText("Reviewer-only ASCE Candidate")).toBeNull();
    expect(view.queryByText("Standard Candidate")).toBeNull();
    expect(view.queryByText("Unverified")).toBeNull();
    expect(view.queryByText("Candidate")).toBeNull();
  });

  test("NodeInspector discloses hidden semantic relationships and can reveal their filters", () => {
    useSceneStore.setState({
      selectedNodeId: "VTN-DOM-0012495",
      visibleNodeTypes: new Set(["work"]),
      visibleEdgeTypes: new Set(["HAS_CHILD"]),
      hiddenNodeIds: [],
      showAllRequestId: 0,
      focusRequest: null,
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: { id: "VTN-DOM-0012495", label: "Sendai Mediatheque", type: "work" },
          taxonomyPath: [],
          incoming: [
            {
              relType: "HAS_FACET",
              other: { id: "VTN-DOM-0012436", label: "Toyo Ito", type: "person" },
              category: "semantic",
              isSemanticEdge: true,
              isHierarchyEdge: false,
              reviewStatus: "admitted",
              sourceFamilyIds: ["source-family-sendai"],
              provenanceNote:
                "Admitted overlay relationship metadata; review evidence indicator only, not source truth.",
            },
          ],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    fireEvent.click(view.getByText("Relationships"));

    expect(view.getByText(/1 hidden by current filters\/isolation/)).toBeTruthy();
    expect(view.getByText("semantic")).toBeTruthy();
    expect(view.getByText("review Admitted")).toBeTruthy();
    expect(view.getByText("source refs 1")).toBeTruthy();
    expect(view.getByText("provenance note")).toBeTruthy();
    expect(view.getByText(/review evidence indicator only, not source truth/)).toBeTruthy();
    expect(view.getByText(/hidden: edge type HAS_FACET, node type person/)).toBeTruthy();

    fireEvent.click(view.getByText("Show all direct relationships"));
    expect(useSceneStore.getState().visibleEdgeTypes.has("HAS_FACET")).toBe(true);
    expect(useSceneStore.getState().visibleNodeTypes.has("person")).toBe(true);
    expect(useSceneStore.getState().showAllRequestId).toBe(1);

    fireEvent.click(view.getByText("Toyo Ito"));
    expect(useSceneStore.getState().selectedNodeId).toBe("VTN-DOM-0012436");
  });

  test("NodeInspector requests a child council orbit from the right panel slider", () => {
    useSceneStore.setState({
      childOrbitRequest: null,
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: { id: "taxonomy-architecture", label: "Architecture", type: "taxonomy" },
          taxonomyPath: [],
          incoming: [],
          outgoing: [
            {
              relType: "HAS_CHILD",
              other: { id: "topic-history", label: "History", type: "topic" },
            },
          ],
          evidence: [],
        }}
      />,
    );

    act(() => {
      fireEvent.input(view.getByLabelText("Child council orbit strength"), { target: { value: "0.75" } });
    });

    expect(useSceneStore.getState().childOrbitRequest).toEqual({
      nodeId: "taxonomy-architecture",
      strength: 0.75,
      requestId: 1,
    });
  });

  test("NodeInspector renders clickable taxonomy breadcrumbs", () => {
    useSceneStore.setState({
      selectedNodeId: null,
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: { id: "concept-daylighting", label: "Daylighting", type: "concept" },
          taxonomyPath: [
            {
              id: "taxonomy-architecture",
              label: "Architecture",
              kind: "taxonomy",
              conceptCount: 0,
              children: [],
            },
            {
              id: "topic-tropical",
              label: "Tropical Architecture",
              kind: "topic",
              conceptCount: 0,
              children: [],
            },
          ],
          incoming: [],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    expect(view.getByText("Breadcrumbs")).toBeTruthy();
    fireEvent.click(view.getByTitle("Select Architecture"));
    expect(useSceneStore.getState().selectedNodeId).toBe("taxonomy-architecture");
  });


  test("NodeInspector exposes unpin and clear-isolation actions", async () => {
    const writeText = mock(() => Promise.resolve());
    Object.defineProperty(globalThis.navigator, "clipboard", {
      value: { writeText },
      configurable: true,
    });

    useSceneStore.setState({
      pinnedNodeIds: ["rule-long-1"],
      hiddenNodeIds: ["other-node"],
      showAllRequestId: 0,
      pathSourceId: null,
      pathTargetId: null,
      highlightedPath: null,
    });

    const view = render(
      <NodeInspector
        detail={{
          node: {
            id: "rule-long-1",
            label:
              "Every building permit applicant must submit complete documentation.",
            displayLabel: "Building Permit Rule",
            type: "rule",
          },
          taxonomyPath: [],
          incoming: [
            {
              relType: "DEFINED_BY",
              other: {
                id: "concept-building-permit",
                label: "Building Permit",
                type: "concept",
              },
            },
          ],
          outgoing: [],
          evidence: [],
        }}
      />,
    );

    fireEvent.click(view.getByLabelText("Unpin node"));
    expect(useSceneStore.getState().pinnedNodeIds).toEqual([]);

    fireEvent.click(view.getByLabelText("Clear node isolation"));
    expect(useSceneStore.getState().showAllRequestId).toBe(1);

    await act(async () => {
      fireEvent.click(view.getByLabelText("Copy node name"));
    });
    expect(writeText).toHaveBeenCalledWith("Building Permit Rule");

    fireEvent.click(view.getByText("Relationships"));
    await act(async () => {
      fireEvent.click(view.getByLabelText("Copy incoming node name"));
    });
    expect(writeText).toHaveBeenCalledWith("Building Permit");
  });

  test("SceneMenu calls scene actions", () => {
    const onOpenScene = mock(() => {});
    const onRenameScene = mock(() => {});
    const onDeleteScene = mock(() => {});
    const view = render(
      <SceneMenu
        activeSceneId={null}
        activeSceneName={null}
        sceneFilter=""
        showScenes
        filteredScenes={[
          {
            id: "scene-1",
            name: "My Scene",
            perspectiveId: "default",
            savedAt: "2026-04-23T00:00:00Z",
          },
        ]}
        deletingSceneId={null}
        onToggle={() => {}}
        onClose={() => {}}
        onSceneFilterChange={() => {}}
        onOpenScene={onOpenScene}
        onRenameScene={onRenameScene}
        onDeleteScene={onDeleteScene}
      />,
    );

    fireEvent.click(view.getByText("My Scene"));
    fireEvent.click(view.getByText("Rename"));
    fireEvent.click(view.getByText("Delete"));
    expect(onOpenScene).toHaveBeenCalledWith("scene-1");
    expect(onRenameScene).toHaveBeenCalledTimes(1);
    expect(onDeleteScene).toHaveBeenCalledTimes(1);
  });

  test("FiltersPanel dispatches toggle and selection callbacks", () => {
    const onSelectColorScheme = mock(() => {});
    const onSelectSizeBy = mock(() => {});
    const onToggleNodeType = mock(() => {});
    const onToggleEdgeType = mock(() => {});
    const onToggleNodeLabelType = mock(() => {});
    const onToggleScaffoldAnchors = mock(() => {});
    const onShowAllNodeLabels = mock(() => {});
    const onHideAllNodeLabels = mock(() => {});
    const view = render(
      <FiltersPanel
        colorScheme="default"
        sizeBy="uniform"
        visibleNodeTypes={new Set(["concept"])}
        visibleEdgeTypes={new Set(["RELATED_TO"])}
        visibleNodeLabelTypes={new Set(["concept"])}
        showScaffoldAnchors={false}
        colorSchemes={[
          { key: "default", label: "Default" },
          { key: "pastel", label: "Pastel" },
        ]}
        sizeOptions={[
          { key: "uniform", label: "Uniform" },
          { key: "degree", label: "By Connectivity" },
        ]}
        nodeTypes={[
          { key: "concept", label: "Concept", color: "bg-node-concept" },
        ]}
        edgeTypes={[{ key: "RELATED_TO", label: "RELATED_TO" }]}
        onSelectColorScheme={onSelectColorScheme}
        onSelectSizeBy={onSelectSizeBy}
        onToggleNodeType={onToggleNodeType}
        onToggleEdgeType={onToggleEdgeType}
        onToggleNodeLabelType={onToggleNodeLabelType}
        onToggleScaffoldAnchors={onToggleScaffoldAnchors}
        onShowAllNodeLabels={onShowAllNodeLabels}
        onHideAllNodeLabels={onHideAllNodeLabels}
      />,
    );

    fireEvent.click(view.getByText("Pastel"));
    fireEvent.click(view.getByText("By Connectivity"));
    fireEvent.click(view.getByLabelText("Concept"));
    fireEvent.click(view.getByLabelText("RELATED_TO"));
    fireEvent.click(view.getByLabelText("Concept label"));
    fireEvent.click(view.getByLabelText("Show scaffold anchors"));
    fireEvent.click(view.getByText("All"));
    fireEvent.click(view.getByText("None"));
    expect(onSelectColorScheme).toHaveBeenCalledWith("pastel");
    expect(onSelectSizeBy).toHaveBeenCalledWith("degree");
    expect(onToggleNodeType).toHaveBeenCalledWith("concept");
    expect(onToggleEdgeType).toHaveBeenCalledWith("RELATED_TO");
    expect(onToggleNodeLabelType).toHaveBeenCalledWith("concept");
    expect(onToggleScaffoldAnchors).toHaveBeenCalledTimes(1);
    expect(onShowAllNodeLabels).toHaveBeenCalledTimes(1);
    expect(onHideAllNodeLabels).toHaveBeenCalledTimes(1);
  });

  test("Explorer rail edge filters include graph-derived relationship types", () => {
    const onToggleEdgeType = mock(() => {});
    const scopedEdgeTypes = buildScopedEdgeTypes(
      new Map([
        ["HAS_CHILD", 2],
        ["HAS_FACET", 1],
      ]),
    );
    const dynamicEdge = scopedEdgeTypes.find((edgeType) => edgeType.key === "HAS_FACET");

    expect(dynamicEdge).toEqual({
      key: "HAS_FACET",
      label: "HAS FACET",
      count: 1,
      available: true,
    });

    const view = render(
      <FiltersPanel
        colorScheme="default"
        sizeBy="uniform"
        visibleNodeTypes={new Set(["concept"])}
        visibleEdgeTypes={new Set(["HAS_CHILD"])}
        visibleNodeLabelTypes={new Set(["concept"])}
        showScaffoldAnchors={false}
        colorSchemes={[{ key: "default", label: "Default" }]}
        sizeOptions={[{ key: "uniform", label: "Uniform" }]}
        nodeTypes={[
          { key: "concept", label: "Concept", color: "bg-node-concept" },
        ]}
        edgeTypes={scopedEdgeTypes}
        onSelectColorScheme={() => {}}
        onSelectSizeBy={() => {}}
        onToggleNodeType={() => {}}
        onToggleEdgeType={onToggleEdgeType}
        onToggleNodeLabelType={() => {}}
        onToggleScaffoldAnchors={() => {}}
        onShowAllNodeLabels={() => {}}
        onHideAllNodeLabels={() => {}}
      />,
    );

    fireEvent.click(view.getByLabelText("HAS FACET"));
    expect(onToggleEdgeType).toHaveBeenCalledWith("HAS_FACET");
  });

  test("taxonomy tree bulk expansion collects only expandable nodes", () => {
    const roots: TaxonomyNode[] = [
      {
        id: "architecture",
        label: "Architecture",
        kind: "taxonomy",
        conceptCount: 0,
        children: [
          {
            id: "architecture-theory",
            label: "History and Theory",
            kind: "topic",
            conceptCount: 0,
            children: [
              {
                id: "architecture-theory-heritage",
                label: "Heritage Conservation",
                kind: "subtopic",
                conceptCount: 4,
                children: [],
              },
            ],
          },
        ],
      },
      {
        id: "laws",
        label: "Laws",
        kind: "taxonomy",
        conceptCount: 3,
        children: [],
      },
    ];

    expect(collectExpandableTreeIds(roots)).toEqual([
      "architecture",
      "architecture-theory",
    ]);
  });

  test("LayoutMenu exposes readable graph layout choices", () => {
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

    expect(getGraphLayoutLabel("precomputed")).toBe("Saved Backbone Map");
    expect(getGraphLayoutLabel("forceatlas2")).toBe("Network Layout");
    expect(view.getAllByText("Network Layout").length).toBe(2);
    expect(view.getByText("Saved Backbone Map")).toBeTruthy();
    expect(view.getByText("Taxonomy Clusters")).toBeTruthy();
    fireEvent.click(view.getByText("Taxonomy Clusters"));
    expect(onSelect).toHaveBeenCalledWith("clustered");
  });

  test("scene store clamps resizable side panel widths and tracks node label visibility", () => {
    useSceneStore.setState({
      explorerPanelWidth: DEFAULT_EXPLORER_PANEL_WIDTH,
      inspectorPanelWidth: DEFAULT_INSPECTOR_PANEL_WIDTH,
      visibleNodeLabelTypes: new Set(["taxonomy", "topic", "subtopic"]),
      showScaffoldAnchors: false,
    });

    act(() => {
      useSceneStore.getState().setExplorerPanelWidth(100);
      useSceneStore.getState().setInspectorPanelWidth(999);
      useSceneStore.getState().setVisibleNodeLabelTypes(new Set(["subtopic"]));
      useSceneStore.getState().setShowScaffoldAnchors(true);
    });

    expect(useSceneStore.getState().explorerPanelWidth).toBe(
      MIN_SIDE_PANEL_WIDTH,
    );
    expect(useSceneStore.getState().inspectorPanelWidth).toBe(
      MAX_SIDE_PANEL_WIDTH,
    );
    expect(useSceneStore.getState().visibleNodeLabelTypes).toEqual(
      new Set(["subtopic"]),
    );
    expect(useSceneStore.getState().showScaffoldAnchors).toBe(true);
  });

  test("scene store keeps an interactive graph spread control value with documented reset bounds", () => {
    useSceneStore.setState({ layoutSpread: DEFAULT_GRAPH_LAYOUT_SPREAD });

    act(() => {
      useSceneStore.getState().setLayoutSpread(2.1);
    });

    expect(useSceneStore.getState().layoutSpread).toBe(2.1);
    expect(MIN_GRAPH_LAYOUT_SPREAD).toBe(0.75);
    expect(MAX_GRAPH_LAYOUT_SPREAD).toBe(6);

    act(() => {
      useSceneStore.getState().setLayoutSpread(99);
    });

    expect(useSceneStore.getState().layoutSpread).toBe(MAX_GRAPH_LAYOUT_SPREAD);

    act(() => {
      useSceneStore.getState().setLayoutSpread(DEFAULT_GRAPH_LAYOUT_SPREAD);
    });

    expect(useSceneStore.getState().layoutSpread).toBe(
      DEFAULT_GRAPH_LAYOUT_SPREAD,
    );
  });

  test("scene store tracks graph camera interaction mode for select and pan controls", () => {
    useSceneStore.setState({
      graphInteractionMode: "select",
      selectedNodeId: "node-1",
      selectedEdgeId: null,
      contextMenuNodeId: "node-1",
      contextMenuPos: { x: 12, y: 24 },
    });

    act(() => {
      useSceneStore.getState().setGraphInteractionMode("pan");
    });

    expect(useSceneStore.getState().graphInteractionMode).toBe("pan");
    expect(useSceneStore.getState().selectedNodeId).toBe("node-1");
    expect(useSceneStore.getState().selectedEdgeId).toBeNull();
    expect(useSceneStore.getState().contextMenuNodeId).toBeNull();
    expect(useSceneStore.getState().contextMenuPos).toBeNull();

    act(() => {
      useSceneStore.getState().setGraphInteractionMode("select");
    });

    expect(useSceneStore.getState().graphInteractionMode).toBe("select");
  });

  test("QueryTemplatesSection dispatches select and run callbacks", () => {
    const onSelectTemplate = mock(() => {});
    const onRunTemplate = mock(() => {});
    const view = render(
      <QueryTemplatesSection
        templates={[{ label: "All rules", query: "MATCH (n) RETURN n" }]}
        onSelectTemplate={onSelectTemplate}
        onRunTemplate={onRunTemplate}
      />,
    );

    fireEvent.click(view.getByText("All rules"));
    fireEvent.click(view.getByText("Run"));
    expect(onSelectTemplate).toHaveBeenCalledWith("MATCH (n) RETURN n");
    expect(onRunTemplate).toHaveBeenCalledWith("MATCH (n) RETURN n");
  });

  test("StoredQueriesSection dispatches select and delete callbacks", () => {
    const onSelect = mock(() => {});
    const onDelete = mock(() => {});
    const view = render(
      <StoredQueriesSection
        title="Saved Queries"
        icon={<span>icon</span>}
        queries={["MATCH (n) RETURN n LIMIT 10"]}
        onSelect={onSelect}
        onDelete={onDelete}
      />,
    );

    fireEvent.click(view.getByText("MATCH (n) RETURN n LIMIT 10"));
    fireEvent.click(view.getByTitle("Delete saved querie"));
    expect(onSelect).toHaveBeenCalledWith("MATCH (n) RETURN n LIMIT 10");
    expect(onDelete).toHaveBeenCalledWith("MATCH (n) RETURN n LIMIT 10");
  });
});
