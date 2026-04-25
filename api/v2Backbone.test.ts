import { afterEach, describe, expect, test } from 'bun:test';
import api, {
  SHADOW_BACKBONE_SUMMARY_SCHEMA_VERSION,
  buildShadowBackboneSummary,
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
