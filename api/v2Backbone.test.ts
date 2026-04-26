import { afterEach, describe, expect, test } from 'bun:test';
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import api, {
  SHADOW_BACKBONE_NODE_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_PLACEMENT_QA_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_SEARCH_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION,
  SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION,
  SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION,
  buildShadowBackboneNodePreview,
  buildShadowBackbonePlacementQaPreview,
  buildShadowBackboneSearchPreview,
  buildShadowBackboneSourcePreview,
  buildShadowBackboneSummary,
  buildShadowBackboneTaxonomyPreview,
  resolveShadowBackboneArtifactPath,
  resolveShadowBackboneGraphPath,
  resolveShadowBackbonePlacementQaReportPath,
  resolveShadowBackboneReportPath,
} from './index';

const ORIGINAL_REPORT_PATH = process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
const ORIGINAL_PLACEMENT_QA_REPORT_PATH = process.env.VITRUVIUS_SHADOW_BACKBONE_PLACEMENT_QA_REPORT_PATH;
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
  rmSync(TEST_SHADOW_STAGING_DIR, { recursive: true, force: true });
  rmSync(TEST_PLACEMENT_QA_DIR, { recursive: true, force: true });
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
    expect(body.runId).toBe('20260426T003710Z');
    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 29,
      backboneNodes: 7,
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
    expect(body.runId).toBe('20260426T003710Z');
    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 29,
      backboneNodes: 7,
    });
    expect(body.readiness.registryMetadataAvailable).toBe(true);
    expect(body.readiness.canonicalTaxonomyTreeAvailable).toBe(true);
    expect(body.readiness.backboneNodesAvailable).toBe(true);
    expect(body.readiness.shadowGraphAvailable).toBe(true);
    expect(body.shadowGraph.counts).toEqual({
      nodes: 7,
      edges: 4,
      roots: 3,
      maxDepth: 2,
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
    expect(body.runId).toBe('20260426T003710Z');
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
      outgoing: 0,
      total: 1,
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
    expect(body.runId).toBe('20260426T003710Z');
    expect(body.total).toBe(1);
    expect(body.results[0]).toEqual(expect.objectContaining({
      id: 'VTN-DOM-0000002',
      label: 'Spatial Planning',
      displayLabel: 'Spatial Planning',
      pathCode: 'ARC.SPC',
      matchedField: 'alias',
      matchedText: 'Space planning',
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
    expect(body.total).toBe(3);
    expect(body.returned).toBe(1);
    expect(body.results).toHaveLength(1);
    expect(body.results[0].pathCode).toBe('ELE');
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

describe('GET /v2/sources/:source_id', () => {
  test('returns sanitized read-only source metadata from the staged source-rights registry', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/sources/SRC-ISO-12006-2'));
    const body = await response.json() as any;
    const serialized = JSON.stringify(body);

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SOURCE_PREVIEW_SCHEMA_VERSION);
    expect(body.source).toBe('file-backed-shadow-source-preview');
    expect(body.runId).toBe('20260426T003710Z');
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
