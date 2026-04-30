import { afterEach, describe, expect, test } from 'bun:test';
import api, {
  AEC_MEPFS_RESOLVER_RESPONSE_SCHEMA_VERSION,
  AEC_MEPFS_RESOLVER_RUNTIME_DEFAULT,
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
  delete process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG];
  const enabledModule = await import(`./index.ts?resolver-runtime-default-on=${Date.now()}-${enabledImportCounter++}`);
  return enabledModule.default;
}

async function importResolverDisabledApi() {
  process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG] = 'false';
  const disabledModule = await import(`./index.ts?resolver-runtime-disabled=${Date.now()}-${enabledImportCounter++}`);
  return disabledModule.default;
}

describe('AEC-MEPFS resolver runtime gate', () => {
  test('is default-on with an explicit disable/rollback flag', () => {
    expect(AEC_MEPFS_RESOLVER_RUNTIME_DEFAULT).toBe('on');
    expect(isAecMepfsResolverRuntimeEnabled({})).toBe(true);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: 'false' })).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: '0' })).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: 'off' })).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: 'disabled' })).toBe(false);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: 'true' })).toBe(true);
    expect(isAecMepfsResolverRuntimeEnabled({ [AEC_MEPFS_RESOLVER_RUNTIME_FLAG]: '1' })).toBe(true);
  });

  test('mounts /v2/resolve and trace on the default exported API', async () => {
    delete process.env[AEC_MEPFS_RESOLVER_RUNTIME_FLAG];

    const response = await api.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify(resolverRequest()),
      headers: { 'content-type': 'application/json' },
    }));
    const payload = await response.json();

    expect(response.status).toBe(200);
    expect(payload.resultType).toBe('single_value');
    expect(payload.runtimeMode).toBe('file_backed_default_on_runtime');
    expect(payload.boundaries.defaultOnRuntimeRoute).toBe(true);
    expect(payload.boundaries.rollbackDisableFlag).toBe(AEC_MEPFS_RESOLVER_RUNTIME_FLAG);

    const traceResponse = await api.fetch(
      new Request(`http://localhost/v2/resolve/trace/${encodeURIComponent(payload.traceId)}`)
    );
    expect(traceResponse.status).toBe(200);
  });

  test('disables /v2/resolve and trace when the rollback flag is off', async () => {
    const disabledApi = await importResolverDisabledApi();

    const response = await disabledApi.fetch(new Request('http://localhost/v2/resolve', {
      method: 'POST',
      body: JSON.stringify(resolverRequest()),
      headers: { 'content-type': 'application/json' },
    }));

    expect(response.status).toBe(404);

    const traceResponse = await disabledApi.fetch(new Request('http://localhost/v2/resolve/trace/aec-trace-missing'));
    expect(traceResponse.status).toBe(404);
  });

  test('default-on /v2/resolve and trace use deterministic file-backed runtime behavior', async () => {
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



  test('resolves LEA/ALE golden query paths through the file-backed API runtime', async () => {
    const enabledApi = await importResolverEnabledApi();
    const goldenQueries = [
      ['What does R.A. 9266 govern?', 'single_value', 'LEA-RES-001'],
      ['How does the National Building Code relate to occupancy classification?', 'single_value', 'LEA-RES-006'],
      ['How does the Fire Code relate to means of egress?', 'single_value', 'LEA-RES-009'],
      ['How does B.P. 344 relate to ramps accessible parking toilets and public buildings?', 'single_value', 'LEA-RES-011'],
      ['How does the Water Code relate to site planning near waterways?', 'single_value', 'LEA-RES-013'],
      ['How does Bahay Kubo connect to tropical design?', 'single_value', 'LEA-RES-016'],
      ['How do load path structural grid columns beams slabs and foundations connect?', 'single_value', 'LEA-RES-021'],
      ['How do shafts risers equipment rooms ceiling spaces and maintenance access connect to utilities?', 'single_value', 'LEA-RES-024'],
      ['How do occupancy classification occupant load means of egress and Fire Code compose?', 'composed', 'LEA-RES-037'],
      ['How should a historic church accessibility upgrade be resolved when heritage conservation and ramp insertion conflict?', 'conflict', 'LEA-RES-042'],
      ['What are the protected reviewer answer keys for the LEA building technology mock test?', 'none', 'LEA-RES-044'],
    ] as const;

    for (const [text, resultType, caseId] of goldenQueries) {
      const response = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
        method: 'POST',
        body: JSON.stringify({ query: { text, trace_requested: true }, jurisdiction: 'PH' }),
        headers: { 'content-type': 'application/json' },
      }));
      const payload = await response.json();

      expect(response.status).toBe(200);
      expect(payload.resultType).toBe(resultType);
      expect(payload.trace?.caseId).toBe(caseId);
      expect(payload.boundaries.liveNeo4jWrites).toBe(false);
      expect(payload.boundaries.kgRebuild).toBe(false);
      expect(payload.boundaries.protectedContentIngest).toBe(false);
      expect(JSON.stringify(payload)).not.toContain('Building Laws _ Utilities Mock Test with Key.pdf');
      expect(JSON.stringify(payload)).not.toContain('reviewer text');
      expect(JSON.stringify(payload)).not.toContain('official_url');
    }
  });



  test('resolves architecture interconnectivity golden query paths through the file-backed API runtime', async () => {
    const enabledApi = await importResolverEnabledApi();
    const goldenQueries = [
      ['Who are architects that are also engineers?', 'single_value', 'ARCH-INT-001'],
      ['Which people connect architecture and structural engineering?', 'single_value', 'ARCH-INT-002'],
      ['Which Pritzker laureates are connected to concrete through specific works?', 'composed', 'ARCH-INT-003'],
      ['Which architects are associated with exposed concrete?', 'composed', 'ARCH-INT-004'],
      ['Which materials connect to tropical design?', 'single_value', 'ARCH-INT-005'],
      ['Which materials connect to Philippine vernacular architecture?', 'single_value', 'ARCH-INT-006'],
      ['Which materials are used in wet areas?', 'single_value', 'ARCH-INT-007'],
      ['How does concrete connect to slabs beams columns foundations and formwork?', 'single_value', 'ARCH-INT-008'],
      ['How does glass connect to daylighting curtain walls windows and thermal performance?', 'composed', 'ARCH-INT-011'],
      ['Which architects or engineers are connected to tensile structures?', 'single_value', 'ARCH-INT-012'],
      ['What graph path connects Zaha Hadid to concrete?', 'composed', 'ARCH-INT-016'],
      ['What graph path connects Santiago Calatrava to architecture and engineering?', 'single_value', 'ARCH-INT-017'],
      ['What graph path connects Philippine vernacular architecture to bamboo nipa timber and tropical design?', 'composed', 'ARCH-INT-019'],
      ['What path connects Zaha Hadid to concrete and long span public architecture?', 'composed', 'ARCH-INT-021'],
      ['How does Dongdaemun Design Plaza connect Zaha Hadid to aluminum facade systems?', 'composed', 'ARCH-INT-022'],
      ['What path connects Tadao Ando to exposed concrete, light, and spatial atmosphere?', 'composed', 'ARCH-INT-023'],
      ['How does Le Corbusier connect to béton brut, brise-soleil, and Brutalist material expression?', 'composed', 'ARCH-INT-024'],
      ['How does Louis Kahn connect concrete, brick, daylight, and civic monumentality?', 'composed', 'ARCH-INT-025'],
      ['How do Mies works connect glass, steel, stone, and International Style?', 'composed', 'ARCH-INT-026'],
      ['How does the Sydney Opera House connect architecture and engineering through shell structure?', 'composed', 'ARCH-INT-027'],
      ['How do Herzog and de Meuron works connect brick, steel, adaptive reuse, and contemporary civic architecture?', 'composed', 'ARCH-INT-028'],
      ['How does Glenn Murcutt connect regional houses to shading, natural ventilation, and metal roofing?', 'composed', 'ARCH-INT-029'],
      ['How does Wang Shu connect recycled masonry, brick, heritage fabric, and cultural memory?', 'composed', 'ARCH-INT-030'],
      ['How do Norman Foster works connect diagrid, glass, steel, high-rise, and bridge systems?', 'composed', 'ARCH-INT-031'],
      ['How do suspension bridges connect Roebling and Strauss to steel cables and bridge structure?', 'composed', 'ARCH-INT-032'],
      ['How does Burj Khalifa connect tall-building design to buttressed core and wind load concepts?', 'composed', 'ARCH-INT-033'],
      ['How does Peter Zumthor connect stone, board-formed concrete, atmosphere, and phenomenology?', 'composed', 'ARCH-INT-034'],
      ['How does Louvre Abu Dhabi connect dome structure, filtered daylight, steel, and climate response?', 'composed', 'ARCH-INT-035'],
      ['How does Shigeru Ban connect paper tubes to temporary works and disaster relief architecture?', 'composed', 'ARCH-INT-036'],
      ['How does Francis Kere connect local materials, ventilation, shading, and social architecture?', 'composed', 'ARCH-INT-037'],
      ['How do Gothic architecture paths connect stone, rib vaults, flying buttresses, and stained glass?', 'composed', 'ARCH-INT-038'],
      ['How do Roman and Byzantine paths connect concrete, vaults, arches, and domes?', 'composed', 'ARCH-INT-039'],
      ['How does tropical modernism connect brise soleil, natural ventilation, and concrete climate response?', 'composed', 'ARCH-INT-040'],
      ['How does Philippine vernacular architecture connect bamboo, nipa, capiz, and passive cooling?', 'composed', 'ARCH-INT-041'],
      ['How does Leandro Locsin connect Philippine modernism to thin-shell concrete?', 'composed', 'ARCH-INT-042'],
      ['How does Pablo Antonio connect Philippine Art Deco to concrete educational buildings?', 'composed', 'ARCH-INT-043'],
      ['How do materials connect to LEA subjects like construction methods, specifications, structures, interiors, and tropical design?', 'composed', 'ARCH-INT-044'],
      ['Searching Tropical Architecture should resolve the clean concept node, not raw-source filename metadata.', 'single_value', 'ARCH-INT-045'],
    ] as const;

    for (const [text, resultType, caseId] of goldenQueries) {
      const response = await enabledApi.fetch(new Request('http://localhost/v2/resolve', {
        method: 'POST',
        body: JSON.stringify({ query: { text, trace_requested: true }, jurisdiction: 'global' }),
        headers: { 'content-type': 'application/json' },
      }));
      const payload = await response.json();

      expect(response.status).toBe(200);
      expect(payload.resultType).toBe(resultType);
      expect(payload.trace?.caseId).toBe(caseId);
      expect(payload.boundaries.liveNeo4jWrites).toBe(false);
      expect(payload.boundaries.kgRebuild).toBe(false);
      expect(payload.boundaries.protectedContentIngest).toBe(false);
      expect(JSON.stringify(payload)).not.toContain('Local raw-source filename metadata');
      expect(JSON.stringify(payload)).not.toContain('protected PDF payload');
      expect(JSON.stringify(payload)).not.toContain('official_url');
    }
  });

  test('default-on routes fail closed for malformed input and missing artifacts', async () => {
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
    expect(payload.runtimeMode).toBe('file_backed_default_on_runtime');
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
      defaultOffRuntimeRoute: false,
      defaultOnRuntimeRoute: true,
      rollbackDisableFlag: AEC_MEPFS_RESOLVER_RUNTIME_FLAG,
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
