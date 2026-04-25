import { afterEach, describe, expect, test } from 'bun:test';
import api, {
  SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION,
  SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION,
  buildShadowBackboneSummary,
  buildShadowBackboneTaxonomyPreview,
  resolveShadowBackboneArtifactPath,
} from './index';

const ORIGINAL_REPORT_PATH = process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

afterEach(() => {
  if (ORIGINAL_REPORT_PATH === undefined) {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;
  } else {
    process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH = ORIGINAL_REPORT_PATH;
  }
});

function validConsumerReport() {
  return {
    schema_version: 'aec-bb-shadow-staging-consumer-report/v1',
    ok: true,
    run_id: 'TEST_RUN',
    artifact_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-backbone-staging.json',
    producer_report_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-report.json',
    report_path: '006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN/shadow-staging-consumer-report.json',
    counts: {
      predicate_registry: 12,
      source_rights_registry: 29,
    },
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

function validStagingArtifact() {
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

  return {
    schema_version: 'aec-bb-shadow-staging/v1',
    run_id: 'TEST_RUN',
    status: 'shadow_staged',
    created_at_utc: '2026-04-25T15:58:59Z',
    counts: {
      predicate_registry: predicateRows.length,
      source_rights_registry: sourceRows.length,
    },
    boundaries,
    source_paths: {
      predicate_registry: '.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json',
      source_rights_registry: '.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json',
    },
    predicate_registry: predicateRows,
    source_rights_registry: sourceRows,
  };
}

describe('GET /v2/backbone', () => {
  test('returns compact read-only backbone summary from the shadow consumer report', async () => {
    delete process.env.VITRUVIUS_SHADOW_BACKBONE_REPORT_PATH;

    const response = await api.fetch(new Request('http://localhost/v2/backbone'));
    const body = await response.json() as any;

    expect(response.status).toBe(200);
    expect(body.schemaVersion).toBe(SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION);
    expect(body.runId).toBe('20260425T154000Z');
    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 29,
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
    expect(body.runId).toBe('20260425T154000Z');
    expect(body.counts).toEqual({
      predicateRegistry: 12,
      sourceRightsRegistry: 29,
    });
    expect(body.readiness.registryMetadataAvailable).toBe(true);
    expect(body.readiness.canonicalTaxonomyTreeAvailable).toBe(false);
    expect(body.readiness.backboneNodesAvailable).toBe(false);
    expect(body.predicateCategories.length).toBeGreaterThan(0);
    expect(body.predicates.some((row: any) => row.predicate === 'broader_than')).toBe(true);
    expect(body.sourceFamilies.some((row: any) => row.sourceId === 'SRC-ISO-12006-2')).toBe(true);
    expect(serialized).not.toContain('official_url');
    expect(serialized).not.toContain('blocking_notes');
    expect(serialized).not.toContain('examples');
    expect(serialized).not.toContain('non_examples');
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
});
