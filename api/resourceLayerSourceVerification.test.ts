import { afterAll, beforeEach, describe, expect, it } from 'bun:test';
import { existsSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import api from './index';
import { loadExternalCandidateRegistry } from './resourceLayer/externalCandidateRegistry';
import {
  buildSourceVerificationPreview,
  buildStandardsContextVerificationPreview,
  checkUrlMetadata,
  type ControlledSourceCheckResult,
} from './resourceLayer/sourceVerification';

const repoRoot = basename(process.cwd()) === 'api' ? join(process.cwd(), '..') : process.cwd();
const externalCandidateRegistryPath = join(repoRoot, '006_System-Manifests', 'resource-layer', 'external-metadata-candidates.json');
const resourcesPath = join(repoRoot, '006_System-Manifests', 'resource-layer', 'resources.json');
const linksPath = join(repoRoot, '006_System-Manifests', 'resource-layer', 'node-resource-links.json');
const transactionManifestsDir = join(repoRoot, '006_System-Manifests', 'resource-layer', 'transaction-manifests');
const originalExternalCandidateRegistryText = existsSync(externalCandidateRegistryPath)
  ? readFileSync(externalCandidateRegistryPath, 'utf-8')
  : `${JSON.stringify({ schemaVersion: 'vitruvius-external-metadata-candidate/v1', generatedAt: '2026-05-03T11:30:31.552Z', candidates: [] }, null, 2)}\n`;
const originalFetch = globalThis.fetch;
const baselineTransactionManifests = new Set(
  existsSync(transactionManifestsDir)
    ? readdirSync(transactionManifestsDir).filter((f) => f.endsWith('.json'))
    : [],
);

function resourceCount() {
  return JSON.parse(readFileSync(resourcesPath, 'utf-8')).resources.length;
}

function linkCount() {
  return JSON.parse(readFileSync(linksPath, 'utf-8')).nodeResourceLinks.length;
}

function baseCandidate(overrides: Record<string, unknown> = {}) {
  return {
    candidateId: 'ext-cand-earth-retaining-structures-test',
    title: 'Earth Retaining Structures',
    resourceType: 'external_url_candidate',
    sourceType: 'government_guidance',
    proposedUrl: 'https://fhwa.dot.gov/engineering/geotech/retaining',
    proposedPublisher: 'FHWA',
    proposedSourceFamilyId: 'fhwa',
    proposedRightsStatus: 'public_government_guidance_metadata_only',
    proposedNodeIds: ['VTN-DOM-0012799'],
    proposedRelation: 'provides_design_guidance',
    candidateRationale: 'Test candidate based on repo-local metadata only.',
    submittedBy: 'test',
    submittedAt: '2026-05-06T00:00:00.000Z',
    verificationStatus: 'unverified',
    displayPolicy: 'reviewer_only',
    learnerVisible: false,
    reviewRequired: true,
    warningFlags: ['URL syntax accepted; reachability not verified'],
    missingFields: ['doi', 'isbn', 'authors', 'publicationDate', 'edition/version', 'jurisdiction/scope'],
    fakePlaceholderFlags: [],
    sourceTruthCaveat: 'Unverified candidate metadata.',
    normalizedUrl: 'https://fhwa.dot.gov/engineering/geotech/retaining',
    persistedAt: '2026-05-06T00:00:00.000Z',
    previewHash: 'test-preview-hash',
    status: 'source_custody_review_needed',
    noAutoVerification: true,
    noAutoPromotion: true,
    noAutoLinking: true,
    noLearnerExposure: true,
    decisions: [],
    ...overrides,
  };
}

function asceCandidate(overrides: Record<string, unknown> = {}) {
  return baseCandidate({
    candidateId: 'ext-cand-asce-7-test',
    title: 'ASCE 7: Minimum Design Loads and Associated Criteria for Buildings and Other Structures',
    resourceType: 'standard_candidate',
    sourceType: 'professional_body',
    proposedUrl: 'https://asce.org/asce-7',
    proposedPublisher: 'ASCE',
    proposedSourceFamilyId: 'asce',
    proposedRightsStatus: 'standard_landing_page_metadata_only',
    proposedNodeIds: ['VTN-DOM-0012777'],
    proposedRelation: 'is_supplementary_reference_for',
    warningFlags: [
      'URL syntax accepted; reachability not verified',
      'Standard candidate missing edition/version',
      'Standard candidate missing jurisdiction or scope',
      'standard_candidate_not_learner_trusted',
    ],
    normalizedUrl: 'https://asce.org/asce-7',
    status: 'standards_context_needed',
    ...overrides,
  });
}

function sourceFamilyCandidate(overrides: Record<string, unknown> = {}) {
  return baseCandidate({
    candidateId: 'ext-cand-buildingsmart-source-family-test',
    title: 'buildingSMART International Source Family Reference',
    resourceType: 'source_family_reference',
    sourceType: 'official_source_family',
    proposedUrl: undefined,
    normalizedUrl: undefined,
    proposedPublisher: 'buildingSMART International',
    proposedSourceFamilyId: 'buildingsmart',
    proposedRightsStatus: 'source_family_metadata_only',
    proposedNodeIds: undefined,
    proposedRelation: undefined,
    candidateRationale: 'Repo-local source-family metadata seed only.',
    warningFlags: ['minimal_metadata', 'no_stable_identifier'],
    missingFields: ['url', 'doi', 'isbn', 'authors', 'publicationDate', 'edition/version', 'jurisdiction/scope'],
    status: 'needs_review',
    ...overrides,
  });
}

function writeRegistry(candidates: Record<string, unknown>[]) {
  writeFileSync(externalCandidateRegistryPath, `${JSON.stringify({
    schemaVersion: 'vitruvius-external-metadata-candidate/v1',
    generatedAt: '2026-05-06T00:00:00.000Z',
    candidates,
  }, null, 2)}\n`);
}

function resetExternalCandidateRegistry() {
  writeRegistry([]);
}

function restoreExternalCandidateRegistry() {
  writeFileSync(externalCandidateRegistryPath, originalExternalCandidateRegistryText);
}

function cleanTransactionManifests() {
  try {
    const files = readdirSync(transactionManifestsDir);
    for (const f of files) {
      if (f.endsWith('.json') && !baselineTransactionManifests.has(f)) {
        unlinkSync(join(transactionManifestsDir, f));
      }
    }
  } catch {
    // Directory may not exist in minimal fixtures.
  }
}

function mockOfficialHtmlFetch(title = 'Official Metadata Page', status = 200): typeof fetch {
  return async (_input: RequestInfo | URL, init?: RequestInit) => {
    const method = init?.method || 'GET';
    const body = method === 'HEAD' ? null : `<html><head><title>${title}</title></head><body>metadata only</body></html>`;
    return new Response(body, {
      status,
      headers: {
        'content-type': 'text/html; charset=utf-8',
        'content-length': '128',
      },
    });
  };
}

function mockRedirectFetch(): typeof fetch {
  return async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.includes('/old')) {
      return new Response(null, { status: 302, headers: { location: 'https://www.fhwa.dot.gov/new' } });
    }
    return new Response(null, { status: 200, headers: { 'content-type': 'text/html' } });
  };
}

beforeEach(() => {
  resetExternalCandidateRegistry();
  cleanTransactionManifests();
  globalThis.fetch = originalFetch;
});

afterAll(() => {
  globalThis.fetch = originalFetch;
  cleanTransactionManifests();
  restoreExternalCandidateRegistry();
});

describe('controlled source check helpers', () => {
  it('blocks non-HTTPS URLs before fetching', async () => {
    let fetched = false;
    const result = await checkUrlMetadata('http://fhwa.dot.gov/test', {
      sourceFamily: 'fhwa',
      fetchImpl: (async () => {
        fetched = true;
        return new Response(null);
      }) as typeof fetch,
    });
    expect(result.blockers).toContain('Requested URL must use HTTPS');
    expect(result.externalVerificationPerformed).toBe(false);
    expect(fetched).toBe(false);
  });

  it('blocks unofficial domains for official source families', async () => {
    const result = await checkUrlMetadata('https://not-fhwa.example.org/resource', { sourceFamily: 'fhwa' });
    expect(result.blockers.some((b) => b.includes('outside official fhwa domains'))).toBe(true);
  });

  it('blocks placeholder-looking URLs', async () => {
    const result = await checkUrlMetadata('https://example.com/resource', { sourceFamily: 'fhwa' });
    expect(result.blockers.some((b) => b.includes('placeholder'))).toBe(true);
  });

  it('follows bounded official HTTPS redirects', async () => {
    const result = await checkUrlMetadata('https://fhwa.dot.gov/old', {
      sourceFamily: 'fhwa',
      fetchImpl: mockRedirectFetch(),
    });
    expect(result.finalUrl).toBe('https://www.fhwa.dot.gov/new');
    expect(result.redirectChain).toContain('https://www.fhwa.dot.gov/new');
    expect(result.officialSourceFamilyMatch).toBe(true);
  });

  it('stores no response payload while extracting public metadata title', async () => {
    const result = await checkUrlMetadata('https://fhwa.dot.gov/engineering/geotech/retaining', {
      sourceFamily: 'fhwa',
      fetchImpl: mockOfficialHtmlFetch('FHWA Earth Retaining Structures'),
    });
    expect(result.title).toBe('FHWA Earth Retaining Structures');
    expect(result.contentPayloadStored).toBe(false);
    expect(result.protectedContentDownloaded).toBe(false);
  });

  it('allows configured official source-family domains beyond ASCE and FHWA', async () => {
    const result = await checkUrlMetadata('https://standards.buildingsmart.org/IFC/DEV/IFC4_3/RC4/HTML/', {
      sourceFamily: 'buildingsmart',
      fetchImpl: mockOfficialHtmlFetch('buildingSMART Standards'),
    });
    expect(result.officialSourceFamilyMatch).toBe(true);
    expect(result.sourceFamily).toBe('buildingsmart');
    expect(result.blockers).toEqual([]);
    expect(result.title).toBe('buildingSMART Standards');
    expect(result.contentPayloadStored).toBe(false);
  });

  it('allows wave 2 configured official source-family domains', async () => {
    const cases: Array<{ url: string; sourceFamily: ControlledSourceCheckResult['sourceFamily']; title: string }> = [
      { url: 'https://www.access-board.gov/ada/', sourceFamily: 'us_access_board', title: 'U.S. Access Board' },
      { url: 'https://www.wbdg.org/design-objectives', sourceFamily: 'wbdg_nibs', title: 'Whole Building Design Guide' },
      { url: 'https://www.istructe.org/resources/', sourceFamily: 'istructe', title: 'Institution of Structural Engineers' },
      { url: 'https://knowledgehub.ice.org.uk/', sourceFamily: 'ice', title: 'ICE Knowledge Hub' },
      { url: 'https://www.architecture.com/knowledge-and-resources', sourceFamily: 'riba', title: 'RIBA Knowledge and Resources' },
    ];
    for (const { url, sourceFamily, title } of cases) {
      const result = await checkUrlMetadata(url, {
        sourceFamily,
        fetchImpl: mockOfficialHtmlFetch(title),
      });
      expect(result.officialSourceFamilyMatch).toBe(true);
      expect(result.sourceFamily).toBe(sourceFamily);
      expect(result.blockers).toEqual([]);
      expect(result.title).toBe(title);
      expect(result.contentPayloadStored).toBe(false);
    }
  });

  it('blocks cross-family official-looking domains', async () => {
    const result = await checkUrlMetadata('https://aisc.org/manual', {
      sourceFamily: 'aia',
      fetchImpl: mockOfficialHtmlFetch('AISC Manual'),
    });
    expect(result.officialSourceFamilyMatch).toBe(false);
    expect(result.externalVerificationPerformed).toBe(false);
    expect(result.blockers.some((b) => b.includes('outside official aia domains'))).toBe(true);
  });

  it('does not download PDF-like protected payloads', async () => {
    const result = await checkUrlMetadata('https://asce.org/asce-7.pdf', {
      sourceFamily: 'asce',
      fetchImpl: (async () => new Response(null, {
        status: 200,
        headers: { 'content-type': 'application/pdf', 'content-length': '999999' },
      })) as typeof fetch,
    });
    expect(result.protectedContentDownloaded).toBe(false);
    expect(result.warnings.some((w) => w.includes('PDF-like'))).toBe(true);
  });
});

describe('source verification preview routes', () => {
  it('source-verification-preview requires dev/admin gate', async () => {
    const oldNodeEnv = process.env.NODE_ENV;
    const oldEnable = process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    process.env.NODE_ENV = 'production';
    delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    const res = await api.fetch(new Request('http://remote.invalid/resources/review/external-candidates/fake/source-verification-preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    }));
    process.env.NODE_ENV = oldNodeEnv;
    if (oldEnable === undefined) delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    else process.env.VITRUVIUS_ENABLE_DEV_ADMIN = oldEnable;
    expect(res.status).toBe(403);
  });

  it('standards-context-verification-preview requires dev/admin gate', async () => {
    const oldNodeEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'production';
    const res = await api.fetch(new Request('http://remote.invalid/resources/review/external-candidates/fake/standards-context-verification-preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    }));
    process.env.NODE_ENV = oldNodeEnv;
    expect(res.status).toBe(403);
  });

  it('preview writes no candidate registry files', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const before = loadExternalCandidateRegistry(repoRoot);
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    }));
    const after = loadExternalCandidateRegistry(repoRoot);
    expect(after.candidates[0].status).toBe(before.candidates[0].status);
    expect(after.candidates[0].decisions?.length).toBe(0);
  });

  it('preview enforces official-domain restrictions', async () => {
    const candidate = baseCandidate();
    const preview = await buildSourceVerificationPreview(candidate as any, {
      requestedUrl: 'https://example.org/not-official',
    });
    expect(preview.blockers.some((b) => b.includes('outside official fhwa domains') || b.includes('placeholder'))).toBe(true);
  });

  it('preview supports source-family reference candidates with explicit official requested URL', async () => {
    globalThis.fetch = mockOfficialHtmlFetch('AIA Contract Documents');
    const candidate = sourceFamilyCandidate({
      candidateId: 'ext-cand-aia-source-family-test',
      title: 'American Institute of Architects Source Family Reference',
      proposedPublisher: 'American Institute of Architects',
      proposedSourceFamilyId: 'aia',
    });
    writeRegistry([candidate]);
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requestedUrl: 'https://www.aia.org/resources' }),
    }));
    expect(res.status).toBe(200);
    const preview = await res.json();
    expect(preview.sourceCheck.sourceFamily).toBe('aia');
    expect(preview.sourceCheck.officialSourceFamilyMatch).toBe(true);
    expect(preview.sourceCheck.externalVerificationPerformed).toBe(true);
    expect(preview.noResourceCreated).toBe(true);
    expect(preview.noNodeResourceLinkCreated).toBe(true);
    expect(preview.learnerVisible).toBe(false);
  });

  it('preview supports wave 2 source-family reference candidates with explicit official requested URL', async () => {
    globalThis.fetch = mockOfficialHtmlFetch('U.S. Access Board Guidance');
    const candidate = sourceFamilyCandidate({
      candidateId: 'ext-cand-us-access-board-source-family-test',
      title: 'U.S. Access Board Source Family Reference',
      proposedPublisher: 'U.S. Access Board',
      proposedSourceFamilyId: 'us_access_board',
    });
    writeRegistry([candidate]);
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requestedUrl: 'https://www.access-board.gov/ada/' }),
    }));
    expect(res.status).toBe(200);
    const preview = await res.json();
    expect(preview.sourceCheck.sourceFamily).toBe('us_access_board');
    expect(preview.sourceCheck.officialSourceFamilyMatch).toBe(true);
    expect(preview.sourceCheck.externalVerificationPerformed).toBe(true);
    expect(preview.noResourceCreated).toBe(true);
    expect(preview.noNodeResourceLinkCreated).toBe(true);
    expect(preview.learnerVisible).toBe(false);
  });

  it('HTTP success does not create Resources or nodeResourceLinks', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const beforeResources = resourceCount();
    const beforeLinks = linkCount();
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    }));
    const data = await res.json();
    expect(data.noResourceCreated).toBe(true);
    expect(data.noNodeResourceLinkCreated).toBe(true);
    expect(resourceCount()).toBe(beforeResources);
    expect(linkCount()).toBe(beforeLinks);
  });
});

describe('standards context preview safeguards', () => {
  it('ASCE candidate cannot complete standards context with missing edition/version/scope', async () => {
    const candidate = asceCandidate();
    const preview = await buildStandardsContextVerificationPreview(candidate as any, {
      nextStatus: 'standards_context_complete',
      reviewer: 'kimi_reviewer',
      rationale: 'test',
      sourceOfContext: 'official landing page metadata only',
    }, { fetchImpl: mockOfficialHtmlFetch('ASCE 7') });
    expect(preview.blockers.some((b) => b.includes('standards_context_complete requires'))).toBe(true);
  });

  it('standards context rejects latest/current/TBD/unknown placeholders', async () => {
    const candidate = asceCandidate();
    const preview = await buildStandardsContextVerificationPreview(candidate as any, {
      nextStatus: 'standards_context_complete',
      reviewer: 'kimi_reviewer',
      rationale: 'test',
      sourceOfContext: 'official landing page metadata only',
      standardsContext: {
        standardTitle: 'ASCE 7',
        edition: 'latest',
        version: 'current',
        scope: 'TBD',
        jurisdictionApplicabilityCaveat: 'unknown',
      },
    }, { fetchImpl: mockOfficialHtmlFetch('ASCE 7') });
    expect(preview.blockers.some((b) => b.includes('placeholder'))).toBe(true);
  });
});

describe('source verification decision apply', () => {
  it('Earth candidate can move only to in-review without rights/access completion', async () => {
    const candidate = baseCandidate();
    const preview = await buildSourceVerificationPreview(candidate as any, {}, {
      fetchImpl: mockOfficialHtmlFetch('FHWA Earth Retaining Structures'),
    });
    expect(preview.proposedNextStatus).toBe('source_custody_in_review');
    expect(preview.sourceCheck.ok).toBe(true);
  });

  it('decision apply requires reviewer, rationale, and sourceOfContext', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nextStatus: 'source_custody_in_review' }),
    }));
    const data = await res.json();
    expect(res.status).toBe(500);
    expect(data.error.message).toContain('reviewer is required');
  });

  it('decision apply reruns preview when no previewHash is supplied and writes history only', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const beforeResources = resourceCount();
    const beforeLinks = linkCount();
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reviewer: 'kimi_reviewer',
        rationale: 'Official FHWA URL reached; rights/access remains reviewer-only.',
        sourceOfContext: 'controlled official FHWA URL metadata check',
        nextStatus: 'source_custody_in_review',
      }),
    }));
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.decision.previewRerun).toBe(true);
    expect(data.candidate.status).toBe('source_custody_in_review');
    expect(data.candidate.decisions.length).toBe(1);
    expect(resourceCount()).toBe(beforeResources);
    expect(linkCount()).toBe(beforeLinks);
  });

  it('source_custody_verified is blocked without rights/access fields', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reviewer: 'kimi_reviewer',
        rationale: 'try verified',
        sourceOfContext: 'controlled official FHWA URL metadata check',
        nextStatus: 'source_custody_verified',
      }),
    }));
    const data = await res.json();
    expect(res.status).toBe(500);
    expect(data.error.message).toContain('rightsStatus');
  });

  it('decision apply writes a transaction manifest', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const res = await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reviewer: 'kimi_reviewer',
        rationale: 'Official FHWA URL reached; rights/access remains reviewer-only.',
        sourceOfContext: 'controlled official FHWA URL metadata check',
        nextStatus: 'source_custody_in_review',
      }),
    }));
    const data = await res.json();
    expect(data.manifest.transactionId).toMatch(/^resource-layer-tx-/);
  });

  it('learner node resources hide source-verified candidates', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reviewer: 'kimi_reviewer',
        rationale: 'Official FHWA URL reached; rights/access remains reviewer-only.',
        sourceOfContext: 'controlled official FHWA URL metadata check',
        nextStatus: 'source_custody_in_review',
      }),
    }));
    const res = await api.fetch(new Request('http://localhost/node/load-path/resources'));
    const data = await res.json();
    const externalCandidate = data.resources.find((r: any) => r.resourceId?.startsWith('ext-cand-'));
    expect(externalCandidate).toBeUndefined();
  });

  it('source-custody queue reflects updated source custody status', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reviewer: 'kimi_reviewer',
        rationale: 'Official FHWA URL reached; rights/access remains reviewer-only.',
        sourceOfContext: 'controlled official FHWA URL metadata check',
        nextStatus: 'source_custody_in_review',
      }),
    }));
    const res = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const data = await res.json();
    const item = data.groups.externalCandidates.find((c: any) => c.id === candidate.candidateId);
    expect(item.reviewStatus).toBe('source_custody_in_review');
    expect(item.learnerEligible).toBe(false);
  });

  it('decision apply keeps production Resource Layer registries unchanged', async () => {
    const candidate = baseCandidate();
    writeRegistry([candidate]);
    globalThis.fetch = mockOfficialHtmlFetch('FHWA Earth Retaining Structures');
    const beforeResources = resourceCount();
    const beforeLinks = linkCount();
    await api.fetch(new Request(`http://localhost/resources/review/external-candidates/${candidate.candidateId}/source-verification-decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reviewer: 'kimi_reviewer',
        rationale: 'Official FHWA URL reached; rights/access remains reviewer-only.',
        sourceOfContext: 'controlled official FHWA URL metadata check',
        nextStatus: 'source_custody_in_review',
      }),
    }));
    expect(resourceCount()).toBe(beforeResources);
    expect(linkCount()).toBe(beforeLinks);
  });
});
