import { afterEach, describe, expect, test } from 'bun:test';
import api, {
  AEC_MEPFS_RESOLVER_RESPONSE_SCHEMA_VERSION,
  AEC_MEPFS_RESOLVER_RUNTIME_FLAG,
  AEC_MEPFS_RESOLVER_TRACE_SCHEMA_VERSION,
  buildAecMepfsResolverRuntimeResponse,
  buildAecMepfsResolverTraceResponse,
  isAecMepfsResolverRuntimeEnabled,
} from './index';

const ORIGINAL_RESOLVER_FLAG = process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG];
const ORIGINAL_FIXTURE_PATH = process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH;

afterEach(() => {
  if (ORIGINAL_RESOLVER_FLAG === undefined) {
    delete process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG];
  } else {
    process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG] = ORIGINAL_RESOLVER_FLAG;
  }
  if (ORIGINAL_FIXTURE_PATH === undefined) {
    delete process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH;
  } else {
    process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH = ORIGINAL_FIXTURE_PATH;
  }
});

function resolverRequest(assetContext = 'public_building', text = 'Resolve accessibility overlay for a public building entrance.') {
  return {
    query: {
      concept_id: 'VTN-CON-0000002',
      asset_context: assetContext,
      text,
      context_ids: ['VTN-DOM-0000001'],
      jurisdiction_filters: ['PH'],
      discipline_filters: ['architecture'],
      trace_requested: true,
    },
    jurisdiction: 'PH',
    effective_date: '2026-04-25',
  };
}

let enabledImportCounter = 0;

async function importResolverEnabledApi() {
  process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG] = 'true';
  const enabledModule = await import(`./index.ts?resolver-runtime-enabled=${Date.now()}-${enabledImportCounter++}`);
  return enabledModule.default;
}

describe('AEC-MEPFS resolver runtime gate', () => {
  test('is default-off unless explicitly enabled', () => {
    expect(isAecMepfsResolverRuntimeEnabled({})).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: 'false' })).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: '0' })).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: 'true' })).toBe(true);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: '1' })).toBe(true);
  });

  test('keeps /v2/resolve absent on the default exported API when flag is off', async () => {
    delete process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG];

    const response = await api.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify(resolverRequest()),
      headers: { 'content-type': 'application/json' },
    }));

    expect(response.status).toBe(404);

    const traceResponse = await api.fetch(new Request('http://localhost/v2/resolve/trace/aec-trace-missing'));
    expect(traceResponse.status).toBe(404);
  });

  test('mounts /v2/resolve and trace only when imported with explicit default-off flag enabled', async () => {
    const enabledApi = await importResolverEnabledApi();

    const response = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify(resolverRequest()),
      headers: { 'content-type': 'application/json' },
    }));
    const payload = await response.json();

    expect(response.status).toBe(200);
    expect(payload.resultType).toBe('single_value');
    expect(payload.boundaries.liveNeo4jWrites).toBe(false);
    expect(payload.boundaries.kgRebuild).toBe(false);
    expect(payload.boundaries.protectedContentIngest).toBe(false);

    const traceResponse = await enabledApi.fetch(
      new Request(`http://localhost/v2/resolve/trace/${encodeURIComponent(payload.traceId)}`)
    );
    const tracePayload = await traceResponse.json();

    expect(traceResponse.status).toBe(200);
    expect(tracePayload.schemaVersion).toBe(AEC_MEPFS_RESOLVER_TRACE_SCHEMA_VERSION);
    expect(tracePayload.traceId).toBe(payload.traceId);
    expect(tracePayload.steps.map((step: any) => step.step)).toEqual([
      'validate_request',
      'read_file_backed_fixture',
      'deterministic_case_match',
      'return_safe_result',
    ]);
  });

  test('enabled default-off routes fail closed for malformed input and missing artifacts', async () => {
    const enabledApi = await importResolverEnabledApi();

    const invalidJson = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: '{',
      headers: { 'content-type': 'application/json' },
    }));
    expect(invalidJson.status).toBe(400);
    expect((await invalidJson.json()).error.code).toBe('AEC_MEPFS_RESOLVER_MALFORMED_REQUEST');

    const emptyQuery = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify({ query: { text: '' } }),
      headers: { 'content-type': 'application/json' },
    }));
    expect(emptyQuery.status).toBe(400);
    expect((await emptyQuery.json()).error.code).toBe('AEC_MEPFS_RESOLVER_INVALID_INPUT');

    const malformedArray = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify({
        query: {
          text: 'Resolve accessible route',
          context_ids: 'VTN-CON-0000002',
        },
      }),
      headers: { 'content-type': 'application/json' },
    }));
    expect(malformedArray.status).toBe(400);
    expect((await malformedArray.json()).error.code).toBe('AEC_MEPFS_RESOLVER_MALFORMED_REQUEST');

    process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH = 'missing-fixture.json';
    const missingFixture = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify(resolverRequest()),
      headers: { 'content-type': 'application/json' },
    }));
    expect(missingFixture.status).toBe(503);
    expect((await missingFixture.json()).error.code).toBe('AEC_MEPFS_RESOLVER_FIXTURE_UNAVAILABLE');

    delete process.env.VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH;
    const missingTrace = await enabledApi.fetch(
      new Request('http://localhost/v2/resolve/trace/aec-trace-missing')
    );
    expect(missingTrace.status).toBe(404);
    expect((await missingTrace.json()).error.code).toBe('AEC_MEPFS_RESOLVER_TRACE_NOT_FOUND');
  });
});

describe('AEC-MEPFS file-backed resolver response builder', () => {
  test('returns deterministic single_value response without protected payloads', async () => {
    const payload = await buildAecMepfsResolverRuntimeResponse(resolverRequest());

    expect(payload.schemaVersion).toBe(AEC_MEPFS_RESOLVER_RESPONSE_SCHEMA_VERSION);
    expect(payload.runtimeMode).toBe('default_off_file_backed_fixture');
    expect(payload.resultType).toBe('single_value');
    expect(payload.confidence).toBe('deterministic');
    expect(payload.canonicalNodeRefs).toEqual([
      { nodeId: 'VTN-CON-0000002', role: 'resolved_concept' },
    ]);
    expect(payload.sourceEvidenceRefs).toEqual(['SRC-PH-DPWH-PD1096']);
    expect(payload.trace?.schemaVersion).toBe(AEC_MEPFS_RESOLVER_TRACE_SCHEMA_VERSION);
    expect(JSON.stringify(payload)).not.toContain('official_url');
    expect(JSON.stringify(payload)).not.toContain('blocking_notes');
    expect(payload.boundaries).toMatchObject({
      defaultOffRuntimeRoute: true,
      fileBackedOnly: true,
      liveNeo4jWrites: false,
      kgRebuild: false,
      protectedContentIngest: false,
      llmHotPath: false,
      explorerDefaultAdoption: false,
      runtimeThresholdClaim: false,
    });
  });

  test('returns composed, conflict, and none fixture semantics deterministically', async () => {
    const composed = await buildAecMepfsResolverRuntimeResponse(resolverRequest(
      'national_and_local_compatible',
      'Resolve compatible national and local accessibility requirements.',
    ));
    const conflict = await buildAecMepfsResolverRuntimeResponse({
      ...resolverRequest(
        'equal_force_incompatible',
        'Resolve equal-force incompatible accessibility requirements.',
      ),
      jurisdiction: 'PH-EXAMPLE-LGU',
    });
    const none = await buildAecMepfsResolverRuntimeResponse({
      ...resolverRequest(
        'no_overlay',
        'Resolve an unmodeled local accessibility overlay.',
      ),
      jurisdiction: 'PH-UNMODELED',
    });

    expect(composed.resultType).toBe('composed');
    expect(composed.canonicalNodeRefs).toHaveLength(2);
    expect(conflict.resultType).toBe('conflict');
    expect(conflict.conflictSet?.resolution).toBe('human_review_required');
    expect(none.resultType).toBe('none');
    expect(none.confidence).toBe('insufficient');
  });

  test('returns expanded non-protected fixture cases deterministically', async () => {
    const domain = await buildAecMepfsResolverRuntimeResponse({
      query: {
        text: 'Resolve the Architecture backbone domain.',
        trace_requested: true,
      },
    });
    const jurisdiction = await buildAecMepfsResolverRuntimeResponse({
      query: {
        concept_id: 'VTN-JUR-0000004',
        asset_context: 'jurisdiction_crosswalk',
        text: 'Resolve the Philippines jurisdiction metadata crosswalk.',
        trace_requested: true,
      },
      jurisdiction: 'PH',
    });
    const overlay = await buildAecMepfsResolverRuntimeResponse({
      query: {
        concept_id: 'VTN-OVR-0000003',
        asset_context: 'overlay_metadata',
        text: 'Resolve the Philippines accessibility overlay metadata.',
        trace_requested: true,
      },
      jurisdiction: 'PH',
    });

    expect(domain.canonicalNodeRefs).toEqual([{ nodeId: 'VTN-DOM-0000001', role: 'resolved_domain' }]);
    expect(domain.sourceEvidenceRefs).toEqual(['SRC-ISO-12006-2']);
    expect(JSON.stringify(domain)).not.toContain('61753');

    expect(jurisdiction.canonicalNodeRefs).toEqual([
      { nodeId: 'VTN-JUR-0000004', role: 'resolved_jurisdiction' },
    ]);
    expect(jurisdiction.sourceEvidenceRefs).toEqual(['SRC-PH-PSA-PSGC']);
    expect(JSON.stringify(jurisdiction)).not.toContain('classifications-api');

    expect(overlay.canonicalNodeRefs).toEqual([{ nodeId: 'VTN-OVR-0000003', role: 'resolved_overlay' }]);
    expect(overlay.sourceEvidenceRefs).toEqual(['SRC-PH-DPWH-PD1096']);
    expect(JSON.stringify(overlay)).not.toContain('laws_codes_orders');
  });

  test('returns deterministic no-result for unmatched requests', async () => {
    const payload = await buildAecMepfsResolverRuntimeResponse({
      query: {
        text: 'Resolve something not admitted into the fixture yet',
        context_ids: [],
        trace_requested: true,
      },
    });

    expect(payload.resultType).toBe('none');
    expect(payload.confidence).toBe('insufficient');
    expect(payload.fallbackReason).toBe('no_static_fixture_case_match');
    expect(payload.canonicalNodeRefs).toEqual([]);
    expect(payload.trace?.steps.at(-1)?.detail).toContain('canonical IDs');
  });

  test('rejects invalid and malformed requests deterministically', async () => {
    await expect(buildAecMepfsResolverRuntimeResponse({
      query: { text: '', context_ids: [] },
    })).rejects.toThrow('query.text');

    await expect(buildAecMepfsResolverRuntimeResponse({
      query: { text: 'Resolve accessible route', context_ids: 'VTN-CON-0000002' },
    })).rejects.toThrow('query.context_ids');
  });

  test('fails closed when fixture artifact is missing', async () => {
    await expect(buildAecMepfsResolverRuntimeResponse(
      resolverRequest(),
      { VITRUVIUS_AEC_MEPFS_RESOLVER_FIXTURE_PATH: 'missing-fixture.json' },
    )).rejects.toThrow('fixture is unavailable');
  });

  test('returns trace by deterministic trace id without storing runtime state', async () => {
    const payload = await buildAecMepfsResolverRuntimeResponse(resolverRequest());
    const trace = await buildAecMepfsResolverTraceResponse(payload.traceId);

    expect(trace.schemaVersion).toBe(AEC_MEPFS_RESOLVER_TRACE_SCHEMA_VERSION);
    expect(trace.traceId).toBe(payload.traceId);
    expect(trace.caseId).toBe('RES-CASE-001');
    expect(trace.steps.map((step: any) => step.step)).toEqual([
      'validate_request',
      'read_file_backed_fixture',
      'deterministic_case_match',
      'return_safe_result',
    ]);
  });

  test('returns deterministic trace not-found errors', async () => {
    await expect(buildAecMepfsResolverTraceResponse('aec-trace-missing')).rejects.toThrow(
      'Resolver trace not found',
    );
  });
});
