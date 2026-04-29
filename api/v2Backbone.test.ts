import { afterEach, describe, expect, test } from 'bun:test';
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import api, {
  AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID,
  AEC_MEPFS_EXPLORER_GRAPH_SCHEMA_VERSION,
  SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION,
  SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION,
  buildAecMepfsEdgeDetail,
  buildAecMepfsExplorerGraph,
  buildAecMepfsNodeDetail,
  buildShadowBackboneEvidencePreview,
  buildShadowBackboneNodePreview,
  buildShadowBackbonePlacementQaPreview,
  buildShadowBackboneSearchPreview,
  buildShadowBackboneSourcePreview,
  buildShadowBackboneSummary,
  buildShadowBackboneTaxonomyPreview,
  resolveShadowBackboneArtifactPath,
  resolveShadowBackboneEvidenceManifestPath,
  resolveShadowBackboneGraphPath,
  resolveShadowBackbonePlacementQaReportPath,
  resolveShadowBackboneReportPath,
} from './index';

const ORIGINAL_REPORT_PATH = process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
const ORIGINAL_PLACEMENT_QA_REPORT_PATH = process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH;
const ORIGINAL_EVIDENCE_MANIFEST_PATH = process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH;
const PARITY_CASES_PATH = resolve(
  import.meta.dir,
  '..',
  'scripts',
  'tests',
  'fixtures',
  'aec_mepfs_backbone',
  'api-explorer-parity-cases.json'
);
const TEST_SHADOW_STAGING_DIR = resolve(
  import.meta.dir,
  '..',
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'shadow-staging',
  'API_TEST_INVALID'
);
const TEST_PLACEMENT_QA_DIR = resolve(
  import.meta.dir,
  '..',
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'placement-qa',
  'API_TEST_INVALID'
);
const TEST_EVIDENCE_MANIFEST_DIR = resolve(
  import.meta.dir,
  '..',
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'evidence-manifest',
  'API_TEST_INVALID'
);
const TEST_EVIDENCE_MANIFEST_OLDER_DIR = resolve(
  import.meta.dir,
  '..',
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'evidence-manifest',
  '00000000T000000Z'
);
const TEST_EVIDENCE_MANIFEST_INCOMPLETE_LATEST_DIR = resolve(
  import.meta.dir,
  '..',
  '006_System-Manifests',
  'aec-mepfs-backbone',
  'evidence-manifest',
  '99999999T999999Z'
);

afterEach(() => {
  if (ORIGINAL_REPORT_PATH === undefined) {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
  } else {
    process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH = ORIGINAL_REPORT_PATH;
  }
  if (ORIGINAL_PLACEMENT_QA_REPORT_PATH === undefined) {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH;
  } else {
    process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH = ORIGINAL_PLACEMENT_QA_REPORT_PATH;
  }
  if (ORIGINAL_EVIDENCE_MANIFEST_PATH === undefined) {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH;
  } else {
    process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH = ORIGINAL_EVIDENCE_MANIFEST_PATH;
  }
  rmSync(TEST_SHADOW_STAGING_DIR, { recursive: true, force: true });
  rmSync(TEST_PLACEMENT_QA_DIR, { recursive: true, force: true });
  rmSync(TEST_EVIDENCE_MANIFEST_DIR, { recursive: true, force: true });
  rmSync(TEST_EVIDENCE_MANIFEST_OLDER_DIR, { recursive: true, force: true });
  rmSync(TEST_EVIDENCE_MANIFEST_INCOMPLETE_LATEST_DIR, { recursive: true, force: true });
});

function validConsumerReport(includeBackboneNodes = false) {
  const counts: Record<string, number> = {
    predicate_registry: 12,
    source_rights_registry: 29,
  };
  if (includeBackboneNodes) counts.backbone_nodes = 2;

  return {
    schema_version: 'aec-bb-shadow-staging-consumer-report/v1',
    ok: true,
    run_id: 'TEST_RUN',
    artifact_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-backbone-staging.json',
    shadow_graph_path: includeBackboneNodes
      ? '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-backbone-graph.json'
      : null,
    producer_report_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-report.json',
    report_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-consumer-report.json',
    counts,
    ...(includeBackboneNodes
      ? {
          shadow_graph_counts: {
            nodes: 2,
            edges: 1,
            roots: 1,
            max_depth: 2,
          },
        }
      : {}),
    boundaries: {
      shadow_only: true,
      file_backed_only: true,
      live_neo4j_writes: false,
      graph_rebuild: false,
      feature_flag_cutover: false,
      api_explorer_cutover: false,
      canonical_content_admission: false,
      protected_content_ingest: false,
    },
    boundary_coverage: {
      safe_for_read_only_consumer: true,
    },
    no_ingest_boundary_coverage: {
      sources_total: 29,
      explicit_no_ingest_source_count: 29,
      missing_explicit_block_count: 0,
      missing_explicit_block_source_ids: [],
      content_ingest_source_count: 0,
      content_ingest_source_ids: [],
    },
  };
}

function validStagingArtifact(includeBackboneNodes = false) {
  const boundaries = {
    shadow_only: true,
    file_backed_only: true,
    live_neo4j_writes: false,
    graph_rebuild: false,
    feature_flag_cutover: false,
    api_explorer_cutover: false,
    canonical_content_admission: false,
    protected_content_ingest: false,
  };
  const predicateRows = Array.from({ length: 12 }, (_, index) => ({
    allowed_strength_classes: ['explicit', 'steward-curated'],
    category: index % 2 === 0 ? 'hierarchy' : 'applicability',
    direction: index % 2 === 0 ? 'parent_to_child' : 'rule_to_context',
    domain_classes: ['BackboneNode'],
    evidence_required_fields: ['source_id', 'review_status'],
    examples: ['not exposed by API'],
    migration_behavior: 'shadow review',
    non_examples: ['not exposed by API'],
    owner: 'Philip Lewis',
    predicate: index === 0 ? 'broader_than' : `test_predicate_${index}`,
    range_classes: ['BackboneNode'],
    validation_rule: 'must be steward-reviewed',
  }));
  const sourceRows = Array.from({ length: 29 }, (_, index) => ({
    blocking_notes: 'not exposed by API',
    clearance_state: index % 2 === 0 ? 'planning_reference_only' : 'metadata_crosswalk_planned',
    currentness_check_date: '2026-04-25',
    declared_use_boundary: 'no standards text, table, figure, or clause ingest',
    edition_version_effective_date: 'admission-time verification required',
    intended_vitruvius_use: 'classification framework citation only',
    official_url: 'https://example.invalid/not-exposed',
    publisher_authority: 'Test Authority',
    source_family: index === 0 ? 'ISO 12006-2' : `Source Family ${index}`,
    source_id: index === 0 ? 'SRC-ISO-12006-2' : `SRC-TEST-${index}`,
    source_rights_class: index % 2 === 0 ? 'reference_only' : 'metadata_crosswalk',
    steward_owner: 'Philip Lewis',
    update_cadence: 'before source admission',
  }));
  const backboneRows = [
    {
      id: 'VTN-DOM-0000001',
      canonical_id: 'VTN-DOM-0000001',
      label: 'Architecture',
      pref_label: 'Architecture',
      path_code: 'ARC',
      level: 1,
      parent_path_code: null,
      record_type: 'BackboneNode',
      review_status: 'steward_admitted',
      steward: 'Philip Lewis',
      release_version: '0.1.0',
      aliases: ['Architectural domain'],
      definition: 'not exposed by API',
    },
    {
      id: 'VTN-DOM-0000002',
      canonical_id: 'VTN-DOM-0000002',
      label: 'Spatial Planning',
      pref_label: 'Spatial Planning',
      path_code: 'ARC.SPC',
      level: 2,
      parent_path_code: 'ARC',
      record_type: 'BackboneNode',
      review_status: 'steward_admitted',
      steward: 'Philip Lewis',
      release_version: '0.1.0',
      aliases: ['Space planning'],
      definition: 'not exposed by API',
    },
  ];
  const counts: Record<string, number> = {
    predicate_registry: predicateRows.length,
    source_rights_registry: sourceRows.length,
  };
  if (includeBackboneNodes) counts.backbone_nodes = backboneRows.length;

  return {
    schema_version: 'aec-bb-shadow-staging/v1',
    run_id: 'TEST_RUN',
    status: 'shadow_staged',
    created_at_utc: '2026-04-25T15:58:59Z',
    counts,
    boundaries,
    source_paths: {
      predicate_registry: '.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json',
      source_rights_registry: '.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json',
      ...(includeBackboneNodes
        ? { backbone_nodes: 'scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json' }
        : {}),
    },
    predicate_registry: predicateRows,
    source_rights_registry: sourceRows,
    ...(includeBackboneNodes ? { backbone_nodes: backboneRows } : {}),
  };
}

function validShadowGraphArtifact() {
  return {
    schema_version: 'aec-bb-shadow-graph/v1',
    run_id: 'TEST_RUN',
    status: 'shadow_graph_staged',
    created_at_utc: '2026-04-25T15:58:59Z',
    source_artifact_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-backbone-staging.json',
    counts: {
      nodes: 2,
      edges: 1,
      roots: 1,
      max_depth: 2,
    },
    nodes: [
      {
        id: 'VTN-DOM-0000001',
        label: 'Architecture',
        path_code: 'ARC',
        level: 1,
        parent_path_code: null,
      },
      {
        id: 'VTN-DOM-0000002',
        label: 'Spatial Planning',
        path_code: 'ARC.SPC',
        level: 2,
        parent_path_code: 'ARC',
      },
    ],
    edges: [
      {
        id: 'VTN-DOM-0000001--broader_than--VTN-DOM-0000002',
        from_id: 'VTN-DOM-0000001',
        to_id: 'VTN-DOM-0000002',
        predicate: 'broader_than',
        from_path_code: 'ARC',
        to_path_code: 'ARC.SPC',
      },
    ],
  };
}

function validPlacementQaReport() {
  return {
    schema_version: 'aec-bb-placement-qa-report/v1',
    ok: true,
    run_id: 'TEST_QA_RUN',
    fixture_path: 'scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json',
    report_path: '006_System-Manifests/aec-mepfs-backbone/placement-qa/TEST_QA_RUN/placement-qa-report.json',
    contract_validation: {
      ok: true,
      errors: [],
      warnings: ['shadow_rollback_plan: rollback proof is planned, not executed'],
    },
    summary: {
      cases_total: 3,
      cases_passed: 3,
      cases_failed: 0,
      auto_accept_cases: 1,
      proposal_level_counts: {
        L1: 1,
        L3: 1,
        L4: 1,
      },
      required_coverage: {
        l1_l2_human_review: true,
        l3_l4_ld8_auto_accept: true,
        legacy_label_alias: true,
      },
      review_queue_counts: {
        auto_accept_sampling_audit: 1,
        two_human_review: 1,
      },
    },
    safety_boundaries: {
      shadow_only: true,
      file_backed_only: true,
      live_neo4j_writes: false,
      kg_rebuild: false,
      feature_flag_cutover: false,
      explorer_default_adoption: false,
      protected_content_ingest: false,
      canonical_content_admission: false,
    },
    warnings: ['shadow_rollback_plan: rollback proof is planned, not executed'],
  };
}

function validEvidenceManifestReport() {
  const artifactResults = [
    ['producer_report', 'aec-bb-shadow-staging-report/v1'],
    ['consumer_report', 'aec-bb-shadow-staging-consumer-report/v1'],
    ['shadow_graph', 'aec-bb-shadow-graph/v1'],
    ['parity_report', 'aec-bb-parity-report/v1'],
    ['placement_qa_report', 'aec-bb-placement-qa-report/v1'],
    ['resolver_qa_report', 'aec-bb-resolver-qa-report/v1'],
    ['boundary_audit_report', 'aec-bb-shadow-boundary-audit-report/v1'],
    ['benchmark_report', 'aec-bb-shadow-benchmark-report/v1'],
    ['route_inventory_report', 'aec-bb-api-route-inventory-report/v1'],
  ].map(([label, schemaVersion]) => ({
    errors: [],
    label,
    ok: true,
    path: `006_System-Manifests/aec-mepfs-backbone/test/${label}.json`,
    schema_version: schemaVersion,
    warnings: [],
  }));
  return {
    schema_version: 'aec-bb-shadow-evidence-manifest-report/v1',
    ok: true,
    run_id: 'TEST_EVIDENCE_RUN',
    report_path: '006_System-Manifests/aec-mepfs-backbone/evidence-manifest/TEST_EVIDENCE_RUN/shadow-evidence-manifest-report.json',
    input_file_hashes_sha256: Object.fromEntries(
      [
        ...artifactResults.map((entry: any, index) => [entry.label, String(index).repeat(64).slice(0, 64)]),
        ['api_index', 'a'.repeat(64)],
      ]
    ),
    repo_state: {
      git_head_commit: 'abc123',
      working_tree_dirty: false,
      source_working_tree_dirty: false,
      generated_evidence_dirty: true,
      source_dirty_path_count: 0,
      generated_evidence_dirty_path_count: 3,
    },
    summary: {
      artifact_count: artifactResults.length,
      shadow_graph_counts: {
        nodes: 9403,
        edges: 10979,
        roots: 24,
        max_depth: 4,
      },
      boundary_checks_passed: 10,
      boundary_checks_total: 10,
      benchmark_operations_passed: 5,
      benchmark_operations_total: 5,
      route_count: 24,
      preview_routes_present: 7,
      preview_routes_required: 7,
      resolver_route_policy: 'guarded_default_off',
      benchmark_runtime_threshold_disposition: 'not_evaluated_shadow_file_backed_only',
    },
    safety_invariants: {
      all_artifacts_ok: true,
      benchmark_shadow_file_backed_only: true,
      boundary_audit_safety_green: true,
      no_runtime_promotion: true,
      resolver_routes_absent_or_default_off: true,
      route_inventory_preview_routes_complete: true,
      runtime_thresholds_not_evaluated: true,
    },
    artifact_results: artifactResults,
    errors: [],
    warnings: [],
  };
}

function parityCase(caseId: string) {
  const payload = JSON.parse(readFileSync(PARITY_CASES_PATH, 'utf-8'));
  const found = payload.api_explorer_parity_cases.find((entry: any) => entry.case_id === caseId);
  if (!found) throw new Error(`Missing parity case ${caseId}`);
  return found;
}

function expectResponseShape(value: any, shape: Record<string, any>) {
  for (const [key, expected] of Object.entries(shape)) {
    if (expected === 'array') {
      expect(Array.isArray(value?.[key])).toBe(true);
    } else if (expected === 'object') {
      expect(value?.[key] !== null && typeof value?.[key] === 'object' && !Array.isArray(value?.[key])).toBe(true);
    } else if (expected === 'string') {
      expect(typeof value?.[key]).toBe('string');
    } else if (expected !== null && typeof expected === 'object' && !Array.isArray(expected)) {
      expect(value?.[key] !== null && typeof value?.[key] === 'object' && !Array.isArray(value?.[key])).toBe(true);
      expectResponseShape(value[key], expected);
    } else {
      expect(value?.[key]).toBe(expected);
    }
  }
}

describe('GET /v2/backbone', () => {
  test('returns compact read-only backbone summary from the shadow consumer report', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone'));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION);
    expect(body.runId).toBe('20260429T092800Z');
    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 79,
      backboneNodes: 9403,
    });
    expect(body.boundaries.shadowOnly).toBe(true);
    expect(body.boundaries.fileBackedOnly).toBe(true);
    expect(body.boundaries.liveMutationBoundariesClear).toBe(true);
    expect(body.noIngestBoundaryCoverage.contentIngestSourceCount).toBe(0);
    expect(body.artifactPaths.consumerReport).toContain('shadow-staging-consumer-report.json');
    expect(body).not.toHaveProperty('predicate_registry');
    expect(body).not.toHaveProperty('source_rights_registry');
  });

  test('fails closed when the configured shadow report is missing', async () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH =
      '006_System-Manifests/aec-mepfs-backbone/shadow-staging/MISSING_RUN/shadow-staging-consumer-report.json';

    const response = await api.fetch(new Request('http://localhost/v2/backbone'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_REPORT_UNAVAILABLE');
  });

  test('fails closed with deterministic diagnostics for invalid consumer report JSON', async () => {
    mkdirSync(TEST_SHADOW_STAGING_DIR, { recursive: true });
    const reportPath = resolve(TEST_SHADOW_STAGING_DIR, 'shadow-staging-consumer-report.json');
    writeFileSync(reportPath, '{', 'utf-8');
    process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH = reportPath;

    const response = await api.fetch(new Request('http://localhost/v2/backbone'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_REPORT_UNAVAILABLE');
    expect(body.error.message).toContain('Invalid JSON in shadow backbone consumer report');
    expect(body.error.message).toContain('shadow-staging-consumer-report.json');
  });

  test('consumer report path resolver rejects wrong filenames inside the report root', () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH =
      '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-backbone-staging.json';

    expect(() => resolveShadowBackboneReportPath()).toThrow(/filename must be shadow-staging-consumer-report\.json/);
  });

  test('summary builder fails closed when the consumer report is not passing', () => {
    const report = validConsumerReport();
    report.ok = false;

    expect(() => buildShadowBackboneSummary(report)).toThrow(/not passing/);
  });

  test('summary builder fails closed when runtime cutover boundaries are enabled', () => {
    const report = validConsumerReport();
    report.boundaries.api_explorer_cutover = true;

    expect(() => buildShadowBackboneSummary(report)).toThrow(/api_explorer_cutover/);
  });
});

describe('GET /v2/backbone/taxonomy', () => {
  test('returns sanitized registry metadata from the shadow staging artifact', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/taxonomy'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION);
    expect(body.runId).toBe('20260429T092800Z');
    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 79,
      backboneNodes: 9403,
    });
    expect(body.readiness.registryMetadataAvailable).toBe(true);
    expect(body.readiness.canonicalTaxonomyTreeAvailable).toBe(true);
    expect(body.readiness.backboneNodesAvailable).toBe(true);
    expect(body.readiness.shadowGraphAvailable).toBe(true);
    expect(body.shadowGraph.counts).toEqual({
      nodes: 9403,
      edges: 10979,
      roots: 24,
      maxDepth: 4,
    });
    expect(body.shadowGraph.edges.some((row: any) => row.fromPathCode === 'ARC' && row.toPathCode === 'ARC.SPC')).toBe(true);
    expect(body.predicateCategories.length).toBeGreaterThan(0);
    expect(body.backboneNodes.some((row: any) => row.pathCode === 'ARC.SPC')).toBe(true);
    expect(body.predicates.some((row: any) => row.predicate === 'broader_than')).toBe(true);
    expect(body.sourceFamilies.some((row: any) => row.sourceId === 'SRC-ISO-12006-2')).toBe(true);
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('examples');
    expect(serialized).not.toContain('non_examples');
  });

  test('taxonomy preview builder exposes admitted BackboneNode metadata when staged', () => {
    const body = buildShadowBackboneTaxonomyPreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      validShadowGraphArtifact()
    );
    const serialized = JSON.stringify(body);

    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 29,
      backboneNodes: 2,
    });
    expect(body.readiness.canonicalTaxonomyTreeAvailable).toBe(true);
    expect(body.readiness.backboneNodesAvailable).toBe(true);
    expect(body.readiness.shadowGraphAvailable).toBe(true);
    expect(body.readiness.previewCompleteness).toBe(
      'registry_metadata_admitted_nodes_and_shadow_graph'
    );
    expect(body.backboneNodes[1]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000002',
      label: 'Spatial Planning',
      pathCode: 'ARC.SPC',
      level: 2,
      parentPathCode: 'ARC',
    }));
    expect(body.shadowGraph.counts).toEqual({
      nodes: 2,
      edges: 1,
      roots: 1,
      maxDepth: 2,
    });
    expect(body.shadowGraph.edges[0]).toEqual(expect.objectContaining({
      fromPathCode: 'ARC',
      toPathCode: 'ARC.SPC',
      predicate: 'broader_than',
    }));
    expect(serialized).not.toContain('not exposed by API');
  });

  test('taxonomy preview builder fails closed when shadow graph counts drift', () => {
    const graph = validShadowGraphArtifact();
    graph.counts.edges = 99;

    expect(() => buildShadowBackboneTaxonomyPreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      graph
    )).toThrow(/shadow_graph.counts.edges/);
  });

  test('taxonomy preview builder fails closed when consumer graph counts drift', () => {
    const report = validConsumerReport(true);
    report.shadow_graph_counts!.edges = 99;

    expect(() => buildShadowBackboneTaxonomyPreview(
      report,
      validStagingArtifact(true),
      validShadowGraphArtifact()
    )).toThrow(/shadow_graph_counts\.edges/);
  });

  test('taxonomy preview builder fails closed when graph source artifact drifts', () => {
    const graph = validShadowGraphArtifact();
    graph.source_artifact_path =
      '006_System-Manifests/aec-mepfs-backbone/shadow-staging/OTHER/shadow-backbone-staging.json';

    expect(() => buildShadowBackboneTaxonomyPreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      graph
    )).toThrow(/shadow_graph\.source_artifact_path/);
  });

  test('taxonomy preview builder fails closed when shadow graph edge endpoints drift', () => {
    const graph = validShadowGraphArtifact();
    graph.edges[0]!.to_id = 'VTN-DOM-9999999';

    expect(() => buildShadowBackboneTaxonomyPreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      graph
    )).toThrow(/shadow_graph\.edges\[0\]\.to_id/);
  });

  test('taxonomy preview builder fails closed when artifact runtime boundaries are enabled', () => {
    const artifact = validStagingArtifact();
    artifact.boundaries.live_neo4j_writes = true;

    expect(() => buildShadowBackboneTaxonomyPreview(validConsumerReport(), artifact)).toThrow(/live_neo4j_writes/);
  });

  test('artifact path resolver rejects paths outside shadow staging', () => {
    const report = validConsumerReport();
    report.artifact_path = '/tmp/shadow-backbone-staging.json';

    expect(() => resolveShadowBackboneArtifactPath(report)).toThrow(/inside the shadow staging report directory/);
  });

  test('artifact path resolver rejects wrong filenames inside shadow staging', () => {
    const report = validConsumerReport();
    report.artifact_path =
      '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-consumer-report.json';

    expect(() => resolveShadowBackboneArtifactPath(report)).toThrow(/filename must be shadow-backbone-staging\.json/);
  });

  test('shadow graph path resolver rejects wrong filenames inside shadow staging', () => {
    const report = validConsumerReport(true);
    report.shadow_graph_path =
      '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-backbone-staging.json';

    expect(() => resolveShadowBackboneGraphPath(report)).toThrow(/filename must be shadow-backbone-graph\.json/);
  });
});

describe('GET /v2/backbone/node/:id', () => {
  test('returns sanitized read-only node preview from the file-backed shadow graph', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/node/VTN-DOM-0000002'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION);
    expect(body.source).toBe('file-backed-shadow-backbone-node-preview');
    expect(body.runId).toBe('20260429T092800Z');
    expect(body.node).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000002',
      canonicalId: 'VTN-DOM-0000002',
      label: 'Spatial Planning',
      displayLabel: 'Spatial Planning',
      pathCode: 'ARC.SPC',
      level: 2,
      parentPathCode: 'ARC',
    }));
    expect(body.relationshipCounts).toEqual({
      incoming: 1,
      outgoing: 3,
      total: 4,
    });
    expect(body.relationships[0]).toEqual(expect.objectContaining({
      predicate: 'broader_than',
      direction: 'incoming',
      from: expect.objectContaining({
        id: 'VTN-DOM-0000001',
        label: 'Architecture',
        pathCode: 'ARC',
      }),
      to: expect.objectContaining({
        id: 'VTN-DOM-0000002',
        label: 'Spatial Planning',
        pathCode: 'ARC.SPC',
      }),
      provenance: expect.objectContaining({
        source: 'file-backed-shadow-backbone-graph',
      }),
    }));
    expect(body.boundaries.liveMutationBoundariesClear).toBe(true);
    expect(body.noIngestBoundaryCoverage.contentIngestSourceCount).toBe(0);
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('not exposed by API');
  });

  test('node preview builder resolves by path code without exposing source payloads', () => {
    const body = buildShadowBackboneNodePreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      validShadowGraphArtifact(),
      'ARC.SPC'
    );
    const serialized = JSON.stringify(body);

    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION);
    expect(body.node.id).toBe('VTN-DOM-0000002');
    expect(body.relationshipCounts.incoming).toBe(1);
    expect(body.relationships[0]!.provenance).toEqual(expect.objectContaining({
      artifactPath: expect.stringContaining('shadow-backbone-graph.json'),
      consumerReportPath: expect.stringContaining('shadow-staging-consumer-report.json'),
    }));
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('not exposed by API');
  });

  test('returns not found for unknown shadow node ids', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/node/VTN-DOM-9999999'));
    const body = await response.json() as any;

    expect(response.status).toBe(404);
    expect(body.error.code).toBe('SHADOW_BACKBONE_NODE_NOT_FOUND');
  });

  test('returns a client error for malformed escaped node ids', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/node/%E0%A4%A'));
    const body = await response.json() as any;

    expect(response.status).toBe(400);
    expect(body.error.code).toBe('SHADOW_BACKBONE_NODE_ID_INVALID');
  });

  test('node preview builder fails closed when the shadow graph artifact is unavailable', () => {
    expect(() => buildShadowBackboneNodePreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      null,
      'VTN-DOM-0000002'
    )).toThrow(/requires a shadow graph artifact/);
  });

  test('node preview builder fails closed when runtime boundaries are enabled', () => {
    const artifact = validStagingArtifact(true);
    artifact.boundaries.live_neo4j_writes = true;

    expect(() => buildShadowBackboneNodePreview(
      validConsumerReport(true),
      artifact,
      validShadowGraphArtifact(),
      'VTN-DOM-0000002'
    )).toThrow(/live_neo4j_writes/);
  });
});

describe('GET /v2/search', () => {
  test('returns sanitized read-only search results from staged BackboneNode aliases', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/search?q=Space%20planning'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION);
    expect(body.source).toBe('file-backed-shadow-backbone-search-preview');
    expect(body.runId).toBe('20260429T092800Z');
    expect(body.total).toBe(3);
    expect(body.results[0]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000002',
      label: 'Spatial Planning',
      displayLabel: 'Spatial Planning',
      pathCode: 'ARC.SPC',
      matchedField: 'alias',
      matchedText: 'space planning',
      detailRoute: '/v2/backbone/node/VTN-DOM-0000002',
    }));
    expect(body.boundaries.liveMutationBoundariesClear).toBe(true);
    expect(body.noIngestBoundaryCoverage.contentIngestSourceCount).toBe(0);
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('not exposed by API');
  });

  test('search preview respects deterministic result limiting', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/search?q=systems&limit=1'));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.total).toBe(338);
    expect(body.returned).toBe(1);
    expect(body.results).toHaveLength(1);
    expect(body.results[0].pathCode).toBe('OPS.COM');
  });

  test('returns a client error for empty search queries', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/search?q='));
    const body = await response.json() as any;

    expect(response.status).toBe(400);
    expect(body.error.code).toBe('SHADOW_BACKBONE_SEARCH_QUERY_INVALID');
  });

  test('search preview builder resolves aliases without exposing source payloads', () => {
    const body = buildShadowBackboneSearchPreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      validShadowGraphArtifact(),
      'Space planning'
    );
    const serialized = JSON.stringify(body);

    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION);
    expect(body.results[0]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000002',
      matchedField: 'alias',
      matchedText: 'Space planning',
    }));
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('not exposed by API');
  });

  test('search preview builder fails closed when the shadow graph artifact is unavailable', () => {
    expect(() => buildShadowBackboneSearchPreview(
      validConsumerReport(true),
      validStagingArtifact(true),
      null,
      'Architecture'
    )).toThrow(/requires a shadow graph artifact/);
  });

  test('search preview builder fails closed when runtime boundaries are enabled', () => {
    const artifact = validStagingArtifact(true);
    artifact.boundaries.protected_content_ingest = true;

    expect(() => buildShadowBackboneSearchPreview(
      validConsumerReport(true),
      artifact,
      validShadowGraphArtifact(),
      'Architecture'
    )).toThrow(/protected_content_ingest/);
  });
});


describe('GET /health', () => {
  test('reports API ok when the file-backed AEC-MEPFS Explorer graph is ready', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/health'));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.status).toBe('ok');
    expect(body.aecMepfs).toBe('ready');
    expect(typeof body.neo4j).toBe('string');
  });
});

describe('AEC-MEPFS Explorer default perspective', () => {
  test('Explorer graph builder maps shadow graph rows into main graph nodes and edges', () => {
    const body = buildAecMepfsExplorerGraph(
      validConsumerReport(true),
      validStagingArtifact(true),
      validShadowGraphArtifact()
    );
    const serialized = JSON.stringify(body);

    expect(body.schemaVersion).toBe(AEC_MEPFS_EXPLORER_GRAPH_SCHEMA_VERSION);
    expect(body.source).toBe('file-backed-aec-mepfs-backbone-graph');
    expect(body.boundaries).toEqual(expect.objectContaining({
      fileBackedOnly: true,
      liveNeo4jWrites: false,
      kgRebuild: false,
      protectedContentIngest: false,
      explorerDefaultAdoption: true,
      broadLiveRuntimeAuthorization: false,
    }));
    expect(body.nodes[0]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000001',
      label: 'Architecture',
      type: 'taxonomy',
      kind: 'backbone',
      aliases: expect.arrayContaining(['ARC', 'Architectural domain']),
      taxonomy_path: ['ARC'],
    }));
    expect(body.nodes[1]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000002',
      type: 'topic',
      aliases: expect.arrayContaining(['ARC.SPC', 'Space planning']),
      taxonomy_path: ['ARC', 'ARC.SPC'],
    }));
    expect(body.edges[0]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000001--broader_than--VTN-DOM-0000002',
      source: 'VTN-DOM-0000001',
      target: 'VTN-DOM-0000002',
      type: 'HAS_CHILD',
      assertionId: 'VTN-DOM-0000001--broader_than--VTN-DOM-0000002',
    }));
    expect(serialized).not.toContain('not exposed by API');
    expect(serialized).not.toContain('official_url');
  });

  test('Explorer node and edge details use the file-backed AEC graph without evidence payloads', () => {
    const report = validConsumerReport(true);
    const artifact = validStagingArtifact(true);
    const graph = validShadowGraphArtifact();
    const nodeDetail = buildAecMepfsNodeDetail(report, artifact, graph, 'VTN-DOM-0000002');
    const edgeDetail = buildAecMepfsEdgeDetail(report, artifact, graph, 'VTN-DOM-0000001--broader_than--VTN-DOM-0000002');

    expect(nodeDetail.node.id).toBe('VTN-DOM-0000002');
    expect(nodeDetail.incoming[0]).toEqual(expect.objectContaining({
      relType: 'HAS_CHILD',
      assertionId: 'VTN-DOM-0000001--broader_than--VTN-DOM-0000002',
    }));
    expect(nodeDetail.outgoing).toEqual([]);
    expect(nodeDetail.evidence).toEqual([]);
    expect(edgeDetail.edge.type).toBe('HAS_CHILD');
    expect(edgeDetail.source.id).toBe('VTN-DOM-0000001');
    expect(edgeDetail.target.id).toBe('VTN-DOM-0000002');
    expect(edgeDetail.evidence).toEqual([]);
  });

  test('GET /perspectives lists AEC-MEPFS first with file-backed node count and legacy as secondary', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/perspectives'));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.perspectives[0]).toEqual(expect.objectContaining({
      id: AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID,
      name: 'AEC-MEPFS Backbone',
      nodeCount: 9403,
    }));
    expect(body.perspectives.some((perspective: any) => (
      perspective.id === 'default'
      && perspective.name === 'Legacy All Knowledge'
    ))).toBe(true);
  });

  test('GET /perspective/aec-mepfs/nodes serves the default graph from file-backed AEC artifacts', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request(`http://localhost/perspective/${AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID}/nodes`));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.nodes).toHaveLength(9403);
    expect(body.edges).toHaveLength(10979);
    expect(body.nodes.some((node: any) => node.id === 'VTN-DOM-0000002' && node.type === 'topic')).toBe(true);
    expect(body.edges.some((edge: any) => edge.type === 'HAS_CHILD')).toBe(true);
    expect(body.edges.some((edge: any) => edge.type === 'MAPS_TO_EXTERNAL_STANDARD')).toBe(true);
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('protected content');
  });

  test('GET /search routes AEC-MEPFS perspective searches through sanitized shadow search', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request(`http://localhost/search?perspective=${AEC_MEPFS_EXPLORER_DEFAULT_PERSPECTIVE_ID}&q=Space%20planning`));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.results[0]).toEqual(expect.objectContaining({
      kind: 'node',
      id: 'VTN-DOM-0000002',
      label: 'Spatial Planning',
      displayLabel: 'Spatial Planning',
      type: 'topic',
      matchType: 'alias',
      matchedField: 'alias',
    }));
  });

  test('GET /node, /edge, /expand, /path use file-backed AEC detail surfaces for backbone ids', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const nodeResponse = await api.fetch(new Request('http://localhost/node/VTN-DOM-0000002'));
    const edgeResponse = await api.fetch(new Request('http://localhost/edge/VTN-DOM-0000001--broader_than--VTN-DOM-0000002'));
    const expandResponse = await api.fetch(new Request('http://localhost/expand?nodeId=VTN-DOM-0000001'));
    const pathResponse = await api.fetch(new Request('http://localhost/path?from=VTN-DOM-0000001&to=VTN-DOM-0000002'));

    expect(nodeResponse.status).toBe(200);
    expect((await nodeResponse.json() as any).node.id).toBe('VTN-DOM-0000002');
    expect(edgeResponse.status).toBe(200);
    expect((await edgeResponse.json() as any).edge.type).toBe('HAS_CHILD');
    expect(expandResponse.status).toBe(200);
    expect((await expandResponse.json() as any).neighbors.length).toBeGreaterThan(0);
    expect(pathResponse.status).toBe(200);
    expect((await pathResponse.json() as any).paths[0].length).toBe(1);
  });

  test('GET /taxonomy serves an AEC-MEPFS tree for the Explorer rail', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/taxonomy'));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.roots.some((root: any) => root.id === 'VTN-DOM-0000001')).toBe(true);
    expect(JSON.stringify(body)).toContain('Spatial Planning');
  });
});

describe('GET /v2/sources/:source_id', () => {
  test('returns sanitized read-only source metadata from the staged source-rights registry', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/sources/SRC-ISO-12006-2'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION);
    expect(body.source).toBe('file-backed-shadow-source-preview');
    expect(body.runId).toBe('20260429T092800Z');
    expect(body.sourceRecord).toEqual(expect.objectContaining({
      sourceId: 'SRC-ISO-12006-2',
      sourceFamily: 'ISO 12006-2',
      evidenceTitle: 'ISO 12006-2',
      publisherAuthority: 'ISO',
      sourceRightsClass: 'reference_only',
      clearanceState: 'planning_reference_only',
    }));
    expect(body.sourceRecord.sourceLabels).toEqual(['ISO 12006-2', 'ISO']);
    expect(body.boundaries.liveMutationBoundariesClear).toBe(true);
    expect(body.noIngestBoundaryCoverage.contentIngestSourceCount).toBe(0);
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('intended_vitruvius_use');
    expect(serialized).not.toContain('https://');
  });

  test('source parity fixture status and expected shape match the route response', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const parity = parityCase('API-PARITY-011');
    const response = await api.fetch(new Request(
      `http://localhost/v2/sources/${encodeURIComponent(parity.request.source_id)}`
    ));
    const body = await response.json() as any;

    expect(response.status).toBe(parity.expected_status);
    expectResponseShape(body, parity.expected_shape);
  });

  test('source preview builder resolves source family labels without exposing hidden governance payloads', () => {
    const body = buildShadowBackboneSourcePreview(
      validConsumerReport(),
      validStagingArtifact(),
      'ISO 12006-2'
    );
    const serialized = JSON.stringify(body);

    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION);
    expect(body.sourceRecord).toEqual(expect.objectContaining({
      sourceId: 'SRC-ISO-12006-2',
      sourceFamily: 'ISO 12006-2',
      sourceLabels: ['ISO 12006-2', 'Test Authority'],
      evidenceTitle: 'ISO 12006-2',
    }));
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('not exposed by API');
    expect(serialized).not.toContain('https://example.invalid');
  });

  test('returns not found for unknown shadow source ids', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/sources/SRC-NOT-FOUND'));
    const body = await response.json() as any;

    expect(response.status).toBe(404);
    expect(body.error.code).toBe('SHADOW_BACKBONE_SOURCE_NOT_FOUND');
  });

  test('returns a client error for malformed escaped source ids', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/sources/%E0%A4%A'));
    const body = await response.json() as any;

    expect(response.status).toBe(400);
    expect(body.error.code).toBe('SHADOW_BACKBONE_SOURCE_ID_INVALID');
  });

  test('returns a client error for blank shadow source ids after decoding', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const parity = parityCase('API-PARITY-011A');
    const response = await api.fetch(new Request(
      `http://localhost/v2/sources/${encodeURIComponent(parity.request.source_id)}`
    ));
    const body = await response.json() as any;

    expect(response.status).toBe(parity.expected_status);
    expectResponseShape(body, parity.expected_shape);
  });

  test('fails closed when the configured shadow report is missing', async () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH =
      '006_System-Manifests/aec-mepfs-backbone/shadow-staging/MISSING_RUN/shadow-staging-consumer-report.json';

    const response = await api.fetch(new Request('http://localhost/v2/sources/SRC-ISO-12006-2'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_SOURCE_UNAVAILABLE');
  });

  test('source preview builder fails closed when runtime boundaries are enabled', () => {
    const artifact = validStagingArtifact();
    artifact.boundaries.canonical_content_admission = true;

    expect(() => buildShadowBackboneSourcePreview(
      validConsumerReport(),
      artifact,
      'SRC-ISO-12006-2'
    )).toThrow(/canonical_content_admission/);
  });
});

describe('GET /v2/backbone/placement-qa', () => {
  test('returns compact read-only placement QA summary from the file-backed report', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/placement-qa'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION);
    expect(body.runId).toBe('20260426T015915Z');
    expect(body.source).toBe('file-backed-placement-qa-report');
    expect(body.status).toBe('shadow_ready');
    expect(body.summary).toEqual({
      casesTotal: 3,
      casesPassed: 3,
      casesFailed: 0,
      autoAcceptCases: 1,
      proposalLevelCounts: {
        L1: 1,
        L3: 1,
        L4: 1,
      },
      reviewQueueCounts: {
        auto_accept_sampling_audit: 1,
        two_human_review: 1,
      },
    });
    expect(body.requiredCoverage).toEqual({
      l1_l2_human_review: true,
      l3_l4_ld8_auto_accept: true,
      legacy_label_alias: true,
    });
    expect(body.boundaries.shadowOnly).toBe(true);
    expect(body.boundaries.fileBackedOnly).toBe(true);
    expect(body.boundaries.liveNeo4jWrites).toBe(false);
    expect(body.boundaries.kgRebuild).toBe(false);
    expect(body.boundaries.featureFlagCutover).toBe(false);
    expect(body.boundaries.explorerDefaultAdoption).toBe(false);
    expect(body.boundaries.protectedContentIngest).toBe(false);
    expect(body.boundaries.canonicalContentAdmission).toBe(false);
    expect(body.boundaries.liveMutationBoundariesClear).toBe(true);
    expect(body.warnings).toContain('shadow_rollback_plan: rollback proof is planned, not executed');
    expect(serialized).not.toContain('case_results');
    expect(serialized).not.toContain('AUTH-CASE-');
    expect(serialized).not.toContain('expected_output');
  });

  test('fails closed when the configured placement QA report is missing', async () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH =
      '006_System-Manifests/aec-mepfs-backbone/placement-qa/MISSING_RUN/placement-qa-report.json';

    const response = await api.fetch(new Request('http://localhost/v2/backbone/placement-qa'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_PLACEMENT_QA_UNAVAILABLE');
  });

  test('fails closed with deterministic diagnostics for invalid placement QA JSON', async () => {
    mkdirSync(TEST_PLACEMENT_QA_DIR, { recursive: true });
    const reportPath = resolve(TEST_PLACEMENT_QA_DIR, 'placement-qa-report.json');
    writeFileSync(reportPath, '[', 'utf-8');
    process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH = reportPath;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/placement-qa'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_PLACEMENT_QA_UNAVAILABLE');
    expect(body.error.message).toContain('Invalid JSON in shadow backbone placement QA report');
    expect(body.error.message).toContain('placement-qa-report.json');
  });

  test('placement QA preview builder fails closed when the report is not passing', () => {
    const report = validPlacementQaReport();
    report.ok = false;

    expect(() => buildShadowBackbonePlacementQaPreview(report)).toThrow(/not passing/);
  });

  test('placement QA preview builder fails closed when runtime boundaries are enabled', () => {
    const report = validPlacementQaReport();
    report.safety_boundaries.explorer_default_adoption = true;

    expect(() => buildShadowBackbonePlacementQaPreview(report)).toThrow(/explorer_default_adoption/);
  });

  test('placement QA preview builder fails closed when required coverage drifts', () => {
    const report = validPlacementQaReport();
    report.summary.required_coverage.legacy_label_alias = false;

    expect(() => buildShadowBackbonePlacementQaPreview(report)).toThrow(/legacy_label_alias/);
  });

  test('placement QA report path resolver rejects paths outside placement QA reports', () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH = '/tmp/placement-qa-report.json';

    expect(() => resolveShadowBackbonePlacementQaReportPath()).toThrow(
      /inside the placement QA report directory/
    );
  });

  test('placement QA report path resolver rejects wrong filenames inside the report root', () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH =
      '006_System-Manifests/aec-mepfs-backbone/placement-qa/TEST_RUN/shadow-staging-consumer-report.json';

    expect(() => resolveShadowBackbonePlacementQaReportPath()).toThrow(
      /filename must be placement-qa-report\.json/
    );
  });
});

describe('GET /v2/backbone/evidence', () => {
  test('returns compact read-only evidence summary from the file-backed manifest', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/evidence'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION);
    expect(body.source).toBe('file-backed-shadow-evidence-manifest');
    expect(body.status).toBe('shadow_ready');
    expect(body.summary.artifactCount).toBe(9);
    expect(body.summary.resolverRoutePolicy).toBe('guarded_default_off');
    expect(body.summary.benchmarkRuntimeThresholdDisposition).toBe(
      'not_evaluated_shadow_file_backed_only'
    );
    expect(body.summary.shadowGraphCounts).toEqual({
      nodes: 7,
      edges: 4,
      roots: 3,
      maxDepth: 2,
    });
    expect(body.safetyInvariants.allInvariantsClear).toBe(true);
    expect(body.safetyInvariants.noRuntimePromotion).toBe(true);
    expect(body.evidenceFiles).toHaveLength(9);
    expect(body.evidenceFiles.every((entry: any) => entry.ok === true)).toBe(true);
    expect(body.reportPath).toContain('shadow-evidence-manifest-report.json');
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('case_results');
  });

  test('evidence preview builder returns sanitized manifest metadata', () => {
    const body = buildShadowBackboneEvidencePreview(validEvidenceManifestReport());

    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_EVIDENCE_PREVIEW_SCHEMA_VERSION);
    expect(body.summary).toEqual({
      artifactCount: 9,
      shadowGraphCounts: {
        nodes: 9403,
        edges: 10979,
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
    });
    expect(body.safetyInvariants.allInvariantsClear).toBe(true);
    expect(body.repoState).toEqual({
      gitHeadCommit: 'abc123',
      workingTreeDirtyAtGeneration: false,
      freshnessAvailable: true,
      sourceWorkingTreeDirtyAtGeneration: false,
      generatedEvidenceDirtyAtGeneration: true,
      sourceDirtyPathCount: 0,
      generatedEvidenceDirtyPathCount: 3,
    });
    expect(body.evidenceFiles[0]).toEqual(expect.objectContaining({
      label: 'producer_report',
      schemaVersion: 'aec-bb-shadow-staging-report/v1',
      ok: true,
    }));
    expect(JSON.stringify(body)).not.toContain('input_file_hashes_sha256');
  });

  test('evidence preview builder surfaces legacy repo-state freshness as unknown', () => {
    const report = validEvidenceManifestReport();
    delete report.repo_state.source_working_tree_dirty;
    delete report.repo_state.generated_evidence_dirty;
    delete report.repo_state.source_dirty_path_count;
    delete report.repo_state.generated_evidence_dirty_path_count;

    const body = buildShadowBackboneEvidencePreview(report);

    expect(body.repoState).toEqual({
      gitHeadCommit: 'abc123',
      workingTreeDirtyAtGeneration: false,
      freshnessAvailable: false,
      sourceWorkingTreeDirtyAtGeneration: null,
      generatedEvidenceDirtyAtGeneration: null,
      sourceDirtyPathCount: null,
      generatedEvidenceDirtyPathCount: null,
    });
  });

  test('evidence preview builder fails closed when source-tree freshness is dirty', () => {
    const report = validEvidenceManifestReport();
    report.repo_state.source_working_tree_dirty = true;
    report.repo_state.source_dirty_path_count = 2;

    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(
      /repo_state\.source_working_tree_dirty: expected false/
    );
  });

  test('evidence route fails closed when source-tree freshness is dirty', async () => {
    mkdirSync(TEST_EVIDENCE_MANIFEST_DIR, { recursive: true });
    const reportPath = resolve(TEST_EVIDENCE_MANIFEST_DIR, 'shadow-evidence-manifest-report.json');
    const report = validEvidenceManifestReport();
    report.repo_state.source_working_tree_dirty = true;
    report.repo_state.source_dirty_path_count = 2;
    writeFileSync(reportPath, JSON.stringify(report), 'utf-8');
    process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH = reportPath;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/evidence'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_EVIDENCE_UNAVAILABLE');
    expect(body.error.message).toContain('repo_state.source_working_tree_dirty');
  });

  test('fails closed when the configured evidence manifest is missing', async () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH =
      '006_System-Manifests/aec-mepfs-backbone/evidence-manifest/MISSING_RUN/shadow-evidence-manifest-report.json';

    const response = await api.fetch(new Request('http://localhost/v2/backbone/evidence'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_EVIDENCE_UNAVAILABLE');
  });

  test('fails closed with deterministic diagnostics for invalid evidence manifest JSON', async () => {
    mkdirSync(TEST_EVIDENCE_MANIFEST_DIR, { recursive: true });
    const reportPath = resolve(TEST_EVIDENCE_MANIFEST_DIR, 'shadow-evidence-manifest-report.json');
    writeFileSync(reportPath, '{', 'utf-8');
    process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH = reportPath;

    const response = await api.fetch(new Request('http://localhost/v2/backbone/evidence'));
    const body = await response.json() as any;

    expect(response.status).toBe(503);
    expect(body.error.code).toBe('SHADOW_BACKBONE_EVIDENCE_UNAVAILABLE');
    expect(body.error.message).toContain('Invalid JSON in shadow backbone evidence manifest report');
    expect(body.error.message).toContain('shadow-evidence-manifest-report.json');
  });

  test('evidence preview builder fails closed when a safety invariant drifts', () => {
    const report = validEvidenceManifestReport();
    report.safety_invariants.no_runtime_promotion = false;

    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/no_runtime_promotion/);
  });

  test('evidence preview builder fails closed when artifact counts drift', () => {
    const report = validEvidenceManifestReport();
    report.summary.artifact_count = 99;

    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/artifact_count/);
  });

  test('evidence preview builder fails closed when the manifest is not passing', () => {
    const report = validEvidenceManifestReport();
    report.ok = false;

    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/not passing/);
  });

  test('evidence preview builder fails closed when an artifact is not passing', () => {
    const report = validEvidenceManifestReport();
    report.artifact_results[0].ok = false;

    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/artifact_results\[0\]\.ok/);
  });

  test('evidence preview builder fails closed when input hashes are malformed', () => {
    const report = validEvidenceManifestReport();
    report.input_file_hashes_sha256.producer_report = 'not-a-sha256';

    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/input_file_hashes_sha256/);
  });

	  test('evidence preview builder fails closed when preview route coverage drifts', () => {
	    const report = validEvidenceManifestReport();
	    report.summary.preview_routes_present = 6;

	    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/preview routes/);
	  });

	  test('evidence preview builder fails closed when runtime disposition fields are missing', () => {
	    const report = validEvidenceManifestReport();
	    delete report.summary.resolver_route_policy;
	    delete report.summary.benchmark_runtime_threshold_disposition;

	    expect(() => buildShadowBackboneEvidencePreview(report)).toThrow(/resolver_route_policy/);
	  });

  test('evidence manifest path resolver rejects paths outside evidence reports', () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH =
      '/tmp/shadow-evidence-manifest-report.json';

    expect(() => resolveShadowBackboneEvidenceManifestPath()).toThrow(
      /inside the evidence manifest report directory/
    );
  });

  test('evidence manifest path resolver rejects wrong filenames inside the report root', () => {
    process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH =
      '006_System-Manifests/aec-mepfs-backbone/evidence-manifest/TEST_RUN/benchmark-report.json';

    expect(() => resolveShadowBackboneEvidenceManifestPath()).toThrow(
      /filename must be shadow-evidence-manifest-report\.json/
    );
  });

  test('evidence manifest path resolver fails closed when newest run is incomplete', () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_EVIDENCE_MANIFEST_PATH;
    mkdirSync(TEST_EVIDENCE_MANIFEST_OLDER_DIR, { recursive: true });
    writeFileSync(
      resolve(TEST_EVIDENCE_MANIFEST_OLDER_DIR, 'shadow-evidence-manifest-report.json'),
      JSON.stringify(validEvidenceManifestReport()),
      'utf-8'
    );
    mkdirSync(TEST_EVIDENCE_MANIFEST_INCOMPLETE_LATEST_DIR, { recursive: true });

    expect(() => resolveShadowBackboneEvidenceManifestPath()).toThrow(
      /unavailable for latest run 99999999T999999Z/
    );
  });
});
