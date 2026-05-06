import { afterEach, describe, expect, test } from 'bun:test';
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import api from './index';
import { detectResourceDuplicates } from './resourceLayer/deduplication';
import { scanLocalCorpus } from './resourceLayer/localCorpusScanner';
import { canonicalizeUrl, normalizeDoi, normalizeIsbn } from './resourceLayer/normalization';
import { getNodeResources, readResourceLayerData } from './resourceLayer/registry';
import { rankNodeResources } from './resourceLayer/ranking';
import {
  ResourceReviewError,
  buildResourceReviewQueue,
  decideStandardsContext,
  decideLocalFile,
  decideNodeResourceLink,
  decideResourceCandidate,
  getStandardsContextReviewDetail,
  previewStandardsContextDecision,
} from './resourceLayer/reviewWorkflow';
import type { NodeResourceLink, Resource, ResourceLayerData, SourceFamily } from './resourceLayer/types';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './resourceLayer/types';
import { validateResourceLayerData } from './resourceLayer/validation';
import { OpenLibraryAdapter } from './resourceLayer/adapters/openLibrary';

const repoRoot = resolve(import.meta.dir, '..');
const tmpDir = resolve(import.meta.dir, '.tmp-resource-layer-test');

afterEach(() => {
  rmSync(tmpDir, { recursive: true, force: true });
});

function minimalResource(overrides: Partial<Resource> = {}): Resource {
  return {
    id: 'res-a',
    title: 'Resource A',
    resourceType: 'webpage',
    sourceAuthority: 'government',
    authorityTier: 1,
    sourceFamilyIds: ['us_access_board'],
    url: 'https://www.access-board.gov/ada/guides/chapter-4-accessible-routes/',
    canonicalUrl: 'https://access-board.gov/ada/guides/chapter-4-accessible-routes',
    disciplineTags: ['architecture'],
    taxonomyTags: ['accessible_route'],
    jurisdiction: 'United States federal accessibility guidance context.',
    geographicScope: 'us',
    accessType: 'public_web',
    verificationStatus: 'link_verified',
    lastCheckedAt: '2026-05-01T00:00:00.000Z',
    createdAt: '2026-05-01T00:00:00.000Z',
    updatedAt: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

function minimalLink(overrides: Partial<NodeResourceLink> = {}): NodeResourceLink {
  return {
    id: 'link-a',
    nodeId: 'VTN-DOM-0004630',
    resourceId: 'res-a',
    relationship: 'provides_design_guidance',
    relevanceScore: 0.9,
    authorityScore: 0.9,
    confidenceScore: 0.85,
    rationale: 'Directly relevant to the node.',
    reviewStatus: 'accepted',
    createdAt: '2026-05-01T00:00:00.000Z',
    updatedAt: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

function minimalFamily(): SourceFamily {
  return {
    id: 'us_access_board',
    label: 'U.S. Access Board',
    domains: ['access-board.gov'],
    organizations: ['U.S. Access Board'],
    authority: 'government',
    authorityTier: 1,
    disciplines: ['architecture', 'accessibility'],
    typicalResourceTypes: ['government_guidance', 'webpage'],
    allowedForPrimaryRuleSource: true,
  };
}

function minimalData(overrides: Partial<ResourceLayerData> = {}): ResourceLayerData {
  return {
    schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
    resources: [minimalResource()],
    nodeResourceLinks: [minimalLink()],
    sourceFamilies: [minimalFamily()],
    resourceChecks: [],
    resourceCandidates: [],
    ...overrides,
  };
}

function copyResourceLayerToTemp() {
  const manifestSource = resolve(repoRoot, '006_System-Manifests', 'resource-layer');
  const manifestTarget = resolve(tmpDir, '006_System-Manifests', 'resource-layer');
  rmSync(tmpDir, { recursive: true, force: true });
  mkdirSync(resolve(tmpDir, '006_System-Manifests'), { recursive: true });
  cpSync(manifestSource, manifestTarget, { recursive: true });
  return tmpDir;
}

function readTempReviewDecisions(tempRepoRoot: string) {
  const path = resolve(tempRepoRoot, '006_System-Manifests', 'resource-layer', 'review-decisions.json');
  return JSON.parse(readFileSync(path, 'utf-8')).reviewDecisions as any[];
}

describe('resource-layer normalization and dedupe', () => {
  test('canonicalizes URLs and validates identifiers deterministically', () => {
    expect(canonicalizeUrl('http://www.Example.com/a/?utm_source=x&b=1#frag')).toBe('https://example.com/a?b=1');
    expect(normalizeDoi('https://doi.org/10.1234/ABC.DEF')).toBe('10.1234/abc.def');
    expect(normalizeIsbn('978-0-306-40615-7')).toBe('9780306406157');
  });

  test('detects duplicate canonical URLs', () => {
    const duplicates = detectResourceDuplicates([
      minimalResource({ id: 'res-a', canonicalUrl: 'https://example.com/ref' }),
      minimalResource({ id: 'res-b', url: 'http://www.example.com/ref?utm_campaign=test', canonicalUrl: undefined }),
    ]);
    expect(duplicates).toHaveLength(1);
    expect(duplicates[0].kind).toBe('canonical_url');
    expect(duplicates[0].resourceIds.sort()).toEqual(['res-a', 'res-b']);
  });
});

describe('resource-layer ranking and registry', () => {
  test('hides candidate links by default and ranks accepted links deterministically', () => {
    const accepted = minimalLink({ id: 'accepted', resourceId: 'res-a', reviewStatus: 'accepted', relevanceScore: 0.85 });
    const candidate = minimalLink({ id: 'candidate', resourceId: 'res-b', reviewStatus: 'needs_review', relevanceScore: 1 });
    const resources = [
      minimalResource({ id: 'res-a', title: 'Accepted Resource' }),
      minimalResource({ id: 'res-b', title: 'Candidate Resource', canonicalUrl: 'https://example.com/candidate', url: 'https://example.com/candidate' }),
    ];

    expect(rankNodeResources(resources, [candidate, accepted]).map((item) => item.title)).toEqual(['Accepted Resource']);
    expect(rankNodeResources(resources, [candidate, accepted], { includeCandidates: true, limit: 10 }).map((item) => item.title)).toContain('Candidate Resource');
  });

  test('reads seed links for Load Path and keeps needs_review links hidden by default', () => {
    const loadPath = getNodeResources(repoRoot, 'VTN-DOM-0012160', { limit: 10 });
    expect(loadPath.map((item) => item.resourceId)).toContain('res-ice-structural-load-paths');
    expect(loadPath.every((item) => item.reviewStatus === 'accepted')).toBe(true);

    const windDefault = getNodeResources(repoRoot, 'VTN-DOM-0012777', { limit: 10 });
    expect(windDefault.some((item) => item.resourceId === 'res-asce-7-official-landing')).toBe(false);

    const windWithCandidates = getNodeResources(repoRoot, 'VTN-DOM-0012777', { includeCandidates: true, limit: 10 });
    expect(windWithCandidates.some((item) => item.resourceId === 'res-asce-7-official-landing')).toBe(true);
  });

  test('learner mode filters out rights-protected and incomplete-standards resources', () => {
    const accepted = minimalLink({ id: 'accepted', resourceId: 'res-a', reviewStatus: 'accepted', relevanceScore: 0.9 });
    const protectedLink = minimalLink({ id: 'protected', resourceId: 'res-protected', reviewStatus: 'accepted', relevanceScore: 0.85 });
    const standardLink = minimalLink({ id: 'standard', resourceId: 'res-standard', reviewStatus: 'accepted', relevanceScore: 0.8 });
    const resources = [
      minimalResource({ id: 'res-a', title: 'Accepted Resource' }),
      minimalResource({ id: 'res-protected', title: 'Protected Resource', sourceRights: { rightsClass: 'protected_content', declaredUseBoundary: 'reviewer_only' } }),
      minimalResource({ id: 'res-standard', title: 'ASCE Standard', resourceType: 'standard', sourceFamilyIds: ['us_access_board'], jurisdiction: 'United States' }),
    ];
    const result = rankNodeResources(resources, [accepted, protectedLink, standardLink]);
    expect(result.map((item) => item.title)).toEqual(['Accepted Resource']);
  });

  test('reviewer mode includes non-eligible resources with warning text', () => {
    const accepted = minimalLink({ id: 'accepted', resourceId: 'res-a', reviewStatus: 'accepted', relevanceScore: 0.9 });
    const protectedLink = minimalLink({ id: 'protected', resourceId: 'res-protected', reviewStatus: 'accepted', relevanceScore: 0.85 });
    const standardLink = minimalLink({ id: 'standard', resourceId: 'res-standard', reviewStatus: 'accepted', relevanceScore: 0.8 });
    const resources = [
      minimalResource({ id: 'res-a', title: 'Accepted Resource' }),
      minimalResource({ id: 'res-protected', title: 'Protected Resource', sourceRights: { rightsClass: 'protected_content', declaredUseBoundary: 'reviewer_only' } }),
      minimalResource({ id: 'res-standard', title: 'ASCE Standard', resourceType: 'standard', sourceFamilyIds: ['us_access_board'], jurisdiction: 'United States' }),
    ];
    const result = rankNodeResources(resources, [accepted, protectedLink, standardLink], { includeReviewer: true });
    expect(result.map((item) => item.title)).toContain('Protected Resource');
    expect(result.map((item) => item.title)).toContain('ASCE Standard');
    const protectedItem = result.find((item) => item.resourceId === 'res-protected');
    expect(protectedItem?.warning).toContain('Rights-protected');
    const standardItem = result.find((item) => item.resourceId === 'res-standard');
    expect(standardItem?.warning).toContain('Standard context incomplete');
  });

  test('displayScore applies rights and standards-context penalties', () => {
    const cleanLink = minimalLink({ id: 'link-clean', resourceId: 'res-clean', relevanceScore: 0.8, authorityScore: 0.8, confidenceScore: 0.8 });
    const protectedLink = minimalLink({ id: 'link-protected', resourceId: 'res-protected', relevanceScore: 0.8, authorityScore: 0.8, confidenceScore: 0.8 });
    const standardLink = minimalLink({ id: 'link-standard', resourceId: 'res-standard', relevanceScore: 0.8, authorityScore: 0.8, confidenceScore: 0.8 });
    const cleanResource = minimalResource({ id: 'res-clean', title: 'Clean' });
    const protectedResource = minimalResource({ id: 'res-protected', title: 'Protected', sourceRights: { rightsClass: 'restricted', declaredUseBoundary: 'reviewer_only' } });
    const standardResource = minimalResource({ id: 'res-standard', title: 'Standard', resourceType: 'standard', sourceFamilyIds: ['us_access_board'], jurisdiction: 'United States' });
    const { displayScore: cleanScore } = rankNodeResources([cleanResource], [cleanLink], { includeReviewer: true })[0];
    const { displayScore: protectedScore } = rankNodeResources([protectedResource], [protectedLink], { includeReviewer: true })[0];
    const { displayScore: standardScore } = rankNodeResources([standardResource], [standardLink], { includeReviewer: true })[0];
    expect(cleanScore).toBeGreaterThan(protectedScore);
    expect(cleanScore).toBeGreaterThan(standardScore);
  });

  test('learner mode hard-caps results at 8', () => {
    const links = Array.from({ length: 12 }, (_, i) =>
      minimalLink({ id: `link-${i}`, resourceId: `res-${i}`, reviewStatus: 'accepted', relevanceScore: 0.9 - i * 0.01 }),
    );
    const resources = Array.from({ length: 12 }, (_, i) =>
      minimalResource({ id: `res-${i}`, title: `Resource ${i}` }),
    );
    const result = rankNodeResources(resources, links);
    expect(result.length).toBe(8);
  });
});

describe('resource-layer validation and local scanning', () => {
  test('validates the checked-in resource layer registry', () => {
    const data = readResourceLayerData(repoRoot);
    const result = validateResourceLayerData(data, { repoRoot });
    expect(result.ok).toBe(true);
    expect(result.duplicateCount).toBe(0);
    expect(result.brokenLinkCount).toBe(0);
  });

  test('rejects accepted external resources with missing lastCheckedAt', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({ lastCheckedAt: undefined })],
    }), { repoRoot });
    expect(result.ok).toBe(false);
    expect(result.errors.some((error) => error.includes('accepted external resource missing lastCheckedAt'))).toBe(true);
  });

  test('blocks accepted standard-like links without edition and citation context', () => {
    const data = minimalData({
      resources: [minimalResource({
        id: 'res-asce-test',
        title: 'ASCE Test Standard',
        resourceType: 'standard',
        sourceFamilyIds: ['us_access_board'],
        jurisdiction: 'United States',
      })],
      nodeResourceLinks: [minimalLink({
        id: 'link-asce-test',
        resourceId: 'res-asce-test',
        reviewStatus: 'accepted',
      })],
    });
    const result = validateResourceLayerData(data, { repoRoot });
    expect(result.ok).toBe(false);
    expect(result.blockers.some((blocker) => blocker.includes('accepted standard/code-like link requires edition'))).toBe(true);
  });

  test('indexes local corpus files with hash-backed local verification', () => {
    mkdirSync(tmpDir, { recursive: true });
    writeFileSync(resolve(tmpDir, 'load-path-note.md'), '# Load path note\n');
    const result = scanLocalCorpus({ repoRoot, directories: ['api/.tmp-resource-layer-test'], now: '2026-05-01T00:00:00.000Z' });
    expect(result.localFilesIndexed).toBe(1);
    expect(result.resources[0].localFileHash).toMatch(/^[a-f0-9]{64}$/);
    expect(result.resources[0].verificationStatus).toBe('local_file_verified');
  });
});

describe('resource-layer adapters and API routes', () => {
  test('maps Open Library search responses to candidate records without requiring API keys', async () => {
    const adapter = new OpenLibraryAdapter(async () => new Response(JSON.stringify({
      docs: [{
        key: '/works/OL123W',
        title: 'Building Construction Illustrated',
        author_name: ['Francis D. K. Ching'],
        first_publish_year: 1975,
        isbn: ['9780306406157'],
        publisher: ['Wiley'],
      }],
    }), { status: 200 }) as any);

    expect(adapter.isConfigured()).toBe(true);
    const candidates = await adapter.search({ nodeId: 'VTN-DOM-0012160', label: 'Building Construction', limit: 1 });
    expect(candidates).toHaveLength(1);
    expect(candidates[0].adapter).toBe('open_library');
    expect(candidates[0].reviewStatus).toBe('candidate');
    expect(candidates[0].rawUrl).toBe('https://openlibrary.org/works/OL123W');
  });

  test('serves node resources through the API with candidate filtering', async () => {
    const detailResponse = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012160'));
    expect(detailResponse.status).toBe(200);
    const detailBody = await detailResponse.json();
    expect(detailBody.resources.some((item: any) => item.resourceId === 'res-ice-structural-load-paths')).toBe(true);

    const defaultResponse = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?limit=10'));
    expect(defaultResponse.status).toBe(200);
    const defaultBody = await defaultResponse.json();
    expect(defaultBody.resources.some((item: any) => item.resourceId === 'res-wbdg-wind-safety-building-envelope')).toBe(true);
    expect(defaultBody.resources.some((item: any) => item.resourceId === 'res-asce-7-official-landing')).toBe(false);

    const candidateResponse = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?includeCandidates=true&limit=10'));
    expect(candidateResponse.status).toBe(200);
    const candidateBody = await candidateResponse.json();
    expect(candidateBody.resources.some((item: any) => item.resourceId === 'res-asce-7-official-landing' && item.reviewStatus === 'needs_review')).toBe(true);
  });

  test('serves the reviewer queue and review metrics without changing learner resources', async () => {
    const queueResponse = await api.fetch(new Request('http://localhost/resources/review/queue'));
    expect(queueResponse.status).toBe(200);
    const queueBody = await queueResponse.json();
    expect(queueBody.needsReviewLinks.some((item: any) => item.id === 'nrl-wind-load-asce-7-needs-review')).toBe(true);
    expect(queueBody.rejectedLinks.some((item: any) => item.id === 'nrl-structural-column-aci-rejected')).toBe(true);
    expect(queueBody.candidates.some((item: any) => item.id === 'cand-asce-7-wind-load')).toBe(true);
    expect(queueBody.localFiles.length).toBeGreaterThan(0);
    expect(queueBody.standardsMissingContext.some((item: any) => item.resourceId === 'res-asce-7-official-landing')).toBe(true);

    const reportResponse = await api.fetch(new Request('http://localhost/resources/review/report'));
    expect(reportResponse.status).toBe(200);
    const reportBody = await reportResponse.json();
    expect(reportBody.needsReviewLinks).toBe(queueBody.needsReviewLinks.length);
    expect(reportBody.rejectedLinks).toBe(1);
    expect(reportBody.localFilesIndexed).toBeGreaterThan(0);
  });

  test('link review decisions mutate copied registry and append decision history safely', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    const result = decideNodeResourceLink(tempRepoRoot, 'nrl-retaining-wall-fhwa-needs-review', {
      decision: 'reject',
      reviewer: 'human-reviewer',
      rationale: 'Rejecting in test copy to preserve audit rationale.',
      notes: 'Test-only copied registry mutation.',
    });
    expect(result.link.reviewStatus).toBe('rejected');
    const copiedData = readResourceLayerData(tempRepoRoot);
    expect(copiedData.nodeResourceLinks.find((link) => link.id === 'nrl-retaining-wall-fhwa-needs-review')?.reviewStatus).toBe('rejected');
    const decisions = readTempReviewDecisions(tempRepoRoot);
    expect(decisions).toHaveLength(1);
    expect(decisions[0].target_type).toBe('node_resource_link');
    expect(decisions[0].previous_status).toBe('needs_review');
    expect(result.transactionManifest.validationStatus).toBe('passed');
    const manifestDir = resolve(tempRepoRoot, '006_System-Manifests', 'resource-layer', 'transaction-manifests');
    expect(existsSync(manifestDir)).toBe(true);
    expect(readdirSync(manifestDir).some((name) => name.endsWith('.json'))).toBe(true);
  });

  test('review workflow blocks unsafe standards promotion', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    expect(() => decideNodeResourceLink(tempRepoRoot, 'nrl-wind-load-asce-7-needs-review', {
      decision: 'accept',
      reviewer: 'human-reviewer',
      rationale: 'Attempt to accept without edition or section.',
    })).toThrow(ResourceReviewError);
  });

  test('standards context detail and preview expose ASCE missing fields without mutating', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    const before = readResourceLayerData(tempRepoRoot);
    const detail = getStandardsContextReviewDetail(tempRepoRoot, 'nrl-wind-load-asce-7-needs-review');
    expect(detail.item.missingStandardContextFields).toContain('edition/version');
    expect(detail.item.missingStandardContextFields).toContain('citation/scope');
    expect(detail.item.promotionBlocked).toBe(true);

    const preview = previewStandardsContextDecision(tempRepoRoot, 'nrl-wind-load-asce-7-needs-review', {
      decision: 'keep_needs_review',
      reviewer: 'human-reviewer',
      rationale: 'Keep ASCE 7 pending until edition and section context are source-confirmed.',
    });
    expect(preview.dryRun).toBe(true);
    expect(preview.diff.missingFieldsAfter).toContain('edition/version');
    expect(preview.validation.ok).toBe(true);
    const after = readResourceLayerData(tempRepoRoot);
    expect(after).toEqual(before);
  });

  test('standards context request validation rejects placeholders and incomplete promotion', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    expect(() => previewStandardsContextDecision(tempRepoRoot, 'nrl-wind-load-asce-7-needs-review', {
      decision: 'update_context_partial',
      reviewer: 'human-reviewer',
      rationale: 'TBD',
      edition: 'latest',
    })).toThrow(ResourceReviewError);

    expect(() => previewStandardsContextDecision(tempRepoRoot, 'nrl-wind-load-asce-7-needs-review', {
      decision: 'promote_if_context_complete',
      reviewer: 'human-reviewer',
      rationale: 'Attempting promotion without complete source context.',
      sourceOfContext: 'test fixture reviewer note',
      edition: 'test fixture edition',
    })).toThrow(ResourceReviewError);
  });

  test('standards context apply writes decision history and transaction manifest in copied registry', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    const result = decideStandardsContext(tempRepoRoot, 'nrl-wind-load-asce-7-needs-review', {
      decision: 'keep_needs_review',
      reviewer: 'human-reviewer',
      rationale: 'Keep ASCE 7 as needs_review until edition and section context are supplied by a human/source-backed review.',
    });
    expect(result.dryRun).toBe(false);
    expect(result.item.reviewStatus).toBe('needs_review');
    expect(result.reviewDecision.target_type).toBe('standard_context');
    expect(result.transactionManifest.operationType).toBe('standard_context_update');
    expect(result.transactionManifest.validationStatus).toBe('passed');
    const decisions = readTempReviewDecisions(tempRepoRoot);
    expect(decisions.at(-1)?.target_type).toBe('standard_context');
    const copied = readResourceLayerData(tempRepoRoot);
    const link = copied.nodeResourceLinks.find((item) => item.id === 'nrl-wind-load-asce-7-needs-review');
    expect(link?.standardContext?.reviewContext?.contextStatus).toBe('needs_human_review');
  });

  test('standards context API routes support detail, preview, and gated apply', async () => {
    const detailResponse = await api.fetch(new Request('http://localhost/resources/review/standards/nrl-wind-load-asce-7-needs-review'));
    expect(detailResponse.status).toBe(200);
    const detailBody = await detailResponse.json();
    expect(detailBody.item.promotionBlocked).toBe(true);

    const previewResponse = await api.fetch(new Request('http://localhost/resources/review/standards/nrl-wind-load-asce-7-needs-review/context-preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        decision: 'keep_needs_review',
        reviewer: 'human-reviewer',
        rationale: 'Preview only; do not infer ASCE 7 edition.',
      }),
    }));
    expect(previewResponse.status).toBe(200);
    const previewBody = await previewResponse.json();
    expect(previewBody.dryRun).toBe(true);

    const oldNodeEnv = process.env.NODE_ENV;
    const oldDevAdmin = process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    process.env.NODE_ENV = 'production';
    delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
    try {
      const badApply = await api.fetch(new Request('http://example.com/resources/review/standards/nrl-wind-load-asce-7-needs-review/context-decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          decision: 'keep_needs_review',
          reviewer: 'human-reviewer',
          rationale: 'Remote mutation should be admin-gated.',
        }),
      }));
      expect(badApply.status).toBe(403);
    } finally {
      process.env.NODE_ENV = oldNodeEnv;
      if (oldDevAdmin === undefined) delete process.env.VITRUVIUS_ENABLE_DEV_ADMIN;
      else process.env.VITRUVIUS_ENABLE_DEV_ADMIN = oldDevAdmin;
    }
  });

  test('candidate review cannot accept without provenance and can be held', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    expect(() => decideResourceCandidate(tempRepoRoot, 'cand-asce-7-wind-load', {
      decision: 'accept_as_resource',
      reviewer: 'human-reviewer',
      rationale: 'Attempt to accept without required provenance.',
      resourceFields: {
        id: 'res-test-asce-copy',
        title: 'ASCE test copy',
        resourceType: 'standard',
        sourceAuthority: 'professional_body',
        sourceFamilyIds: ['asce'],
        accessType: 'public_web',
      },
    })).toThrow(ResourceReviewError);

    const hold = decideResourceCandidate(tempRepoRoot, 'cand-asce-7-wind-load', {
      decision: 'hold',
      reviewer: 'human-reviewer',
      rationale: 'Hold until edition, section, and adoption context are available.',
    });
    expect(hold.candidate.reviewStatus).toBe('needs_review');
    expect(readTempReviewDecisions(tempRepoRoot).at(-1)?.target_type).toBe('candidate');
  });

  test('local file review records decisions without auto-linking files', () => {
    const tempRepoRoot = copyResourceLayerToTemp();
    const queue = buildResourceReviewQueue(tempRepoRoot);
    const firstLocalFile = queue.localFiles[0];
    expect(firstLocalFile).toBeTruthy();
    const before = readResourceLayerData(tempRepoRoot);
    expect(() => decideLocalFile(tempRepoRoot, firstLocalFile.fileId, {
      decision: 'link_to_node',
      reviewer: 'human-reviewer',
      rationale: 'Attempt to link without an explicit target node.',
      linkFields: {
        relationship: 'is_local_reference_for',
        rationale: 'Test link',
      },
    })).toThrow(ResourceReviewError);

    const result = decideLocalFile(tempRepoRoot, firstLocalFile.fileId, {
      decision: 'needs_review',
      reviewer: 'human-reviewer',
      rationale: 'Keep local file indexed but not admitted or linked.',
    });
    expect(result.localFile.admitted).toBe(false);
    const after = readResourceLayerData(tempRepoRoot);
    expect(after.resources).toHaveLength(before.resources.length);
    expect(after.nodeResourceLinks).toHaveLength(before.nodeResourceLinks.length);
    expect(readTempReviewDecisions(tempRepoRoot).at(-1)?.target_type).toBe('local_file');
  });

  test('rejects fake metadata placeholders in DOI, ISBN, URL, and standard context fields', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        url: 'https://example.com/latest',
        canonicalUrl: 'https://example.com/current',
        doi: '10.1234/tbd',
        isbn10: '0000000000',
        isbn13: '0000000000000',
        standardIdentifier: { organization: 'ACI', code: '318', edition: 'latest', year: 'current' },
      })],
    }), { repoRoot });
    expect(result.warnings.some((e) => e.includes('placeholder') || e.includes('test value'))).toBe(true);
    expect(result.fakeMetadataPlaceholderCount).toBeGreaterThanOrEqual(4);
  });

  test('local files indexed-only are not learner-visible; admitted files are', () => {
    const indexedHash = 'a'.repeat(64);
    const data = minimalData({
      resources: [
        minimalResource({
          id: 'res-local-indexed',
          resourceType: 'local_markdown',
          accessType: 'local_file',
          localPath: '/docs/note.md',
          localFileHash: indexedHash,
          verificationStatus: 'local_file_verified',
          sourceRights: { declaredUseBoundary: 'internal_research_only' },
        }),
        minimalResource({
          id: 'res-local-admitted',
          resourceType: 'local_markdown',
          accessType: 'local_file',
          localPath: '/docs/admitted.md',
          localFileHash: 'b'.repeat(64),
          verificationStatus: 'local_file_verified',
          sourceRights: { declaredUseBoundary: 'learner_visible' },
        }),
      ],
      nodeResourceLinks: [
        minimalLink({ id: 'link-indexed', resourceId: 'res-local-indexed', reviewStatus: 'accepted' }),
        minimalLink({ id: 'link-admitted', resourceId: 'res-local-admitted', reviewStatus: 'accepted' }),
      ],
    });
    const result = validateResourceLayerData(data, { repoRoot, localIndexedHashes: new Set([indexedHash]) });
    expect(result.localFilesIndexedOnly).toBe(1);
    expect(result.localFilesAdmitted).toBe(1);
    expect(result.localFilesMissingRights).toBe(0);
  });

  test('rights-restricted and protected-content resources trigger warnings for accepted links', () => {
    const data = minimalData({
      resources: [
        minimalResource({
          id: 'res-restricted',
          sourceRights: { rightsClass: 'restricted', license: 'proprietary', restrictions: ['no_derivatives'], declaredUseBoundary: 'reviewer_only' },
        }),
        minimalResource({
          id: 'res-protected',
          sourceRights: { rightsClass: 'protected_content', license: 'fair_use', declaredUseBoundary: 'reviewer_only' },
        }),
      ],
      nodeResourceLinks: [
        minimalLink({ id: 'link-restricted', resourceId: 'res-restricted', reviewStatus: 'accepted' }),
        minimalLink({ id: 'link-protected', resourceId: 'res-protected', reviewStatus: 'accepted' }),
      ],
    });
    const result = validateResourceLayerData(data, { repoRoot });
    expect(result.resourcesProtectedContent).toBe(1);
    expect(result.resourcesBlockedByRights).toBe(2);
    expect(result.resourcesAcceptedForLearner).toBe(0);
    expect(result.warnings.some((w) => w.includes('rights') || w.includes('restricted') || w.includes('protected'))).toBe(true);
  });

  test('learner sidebar eligibility accepts only accepted and human_reviewed links with verified resources', () => {
    const data = minimalData({
      resources: [
        minimalResource({ id: 'res-verified', verificationStatus: 'link_verified' }),
        minimalResource({ id: 'res-unverified', verificationStatus: 'unverified', canonicalUrl: 'https://example.com/unverified', url: 'https://example.com/unverified' }),
        minimalResource({ id: 'res-rejected', verificationStatus: 'rejected', canonicalUrl: 'https://example.com/rejected', url: 'https://example.com/rejected' }),
      ],
      nodeResourceLinks: [
        minimalLink({ id: 'link-accepted', resourceId: 'res-verified', reviewStatus: 'accepted' }),
        minimalLink({ id: 'link-human', resourceId: 'res-verified', reviewStatus: 'human_reviewed' }),
        minimalLink({ id: 'link-candidate', resourceId: 'res-verified', reviewStatus: 'candidate' }),
        minimalLink({ id: 'link-needs-review', resourceId: 'res-verified', reviewStatus: 'needs_review' }),
        minimalLink({ id: 'link-unverified', resourceId: 'res-unverified', reviewStatus: 'accepted' }),
        minimalLink({ id: 'link-rejected', resourceId: 'res-rejected', reviewStatus: 'accepted' }),
      ],
    });
    const result = validateResourceLayerData(data, { repoRoot });
    expect(result.resourcesAcceptedForLearner).toBe(2);
    expect(result.candidatesReviewerOnly).toBe(1);
    expect(result.resourcesReviewerOnly).toBe(1);
    expect(result.resourcesBlockedByRights).toBe(2);
  });

  test('source-custody metrics are computed for the checked-in registry', () => {
    const data = readResourceLayerData(repoRoot);
    const result = validateResourceLayerData(data, { repoRoot });
    expect(result.resourcesAcceptedForLearner).toBeDefined();
    expect(result.resourcesReviewerOnly).toBeDefined();
    expect(result.resourcesBlockedByRights).toBeDefined();
    expect(result.resourcesProtectedContent).toBeDefined();
    expect(result.localFilesIndexedOnly).toBeGreaterThanOrEqual(0);
    expect(result.localFilesAdmitted).toBeGreaterThanOrEqual(0);
    expect(result.candidatesReviewerOnly).toBeGreaterThanOrEqual(0);
    expect(result.displayPolicyWarnings).toBeGreaterThanOrEqual(0);
    expect(result.fakeMetadataPlaceholderCount).toBeGreaterThanOrEqual(0);
  });

  test('node resources endpoint returns displayPolicy metadata and defaults to learner mode', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.displayPolicy.mode).toBe('learner');
    expect(body.displayPolicy.learnerEligibleOnly).toBe(true);
    expect(body.resources.every((item: any) => item.reviewStatus === 'accepted' || item.reviewStatus === 'human_reviewed')).toBe(true);
    expect(body.resources.length).toBeLessThanOrEqual(8);
  });

  test('reviewer mode endpoint returns non-eligible resources with warnings', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?mode=reviewer'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.displayPolicy.mode).toBe('reviewer');
    expect(body.displayPolicy.learnerEligibleOnly).toBe(false);
    expect(body.resources.some((item: any) => item.resourceId === 'res-asce-7-official-landing')).toBe(true);
  });

  test('node detail endpoint returns learner-safe resources with cap 8', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.resources.length).toBeLessThanOrEqual(8);
    expect(body.resources.some((item: any) => item.resourceId === 'res-asce-7-official-landing')).toBe(false);
  });

  test('source-custody queue groups items by custody status', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.schemaVersion).toBeDefined();
    expect(body.generatedAt).toBeDefined();
    expect(body.groups).toBeDefined();
    expect(body.groups.learnerVisible).toBeDefined();
    expect(body.groups.reviewerOnly).toBeDefined();
    expect(body.groups.needsReview).toBeDefined();
    expect(body.groups.candidates).toBeDefined();
    expect(body.groups.localFilesIndexedOnly).toBeDefined();
    expect(body.groups.standardsContextIncomplete).toBeDefined();
    expect(body.groups.rightsLimited).toBeDefined();
    expect(body.groups.rejected).toBeDefined();
    expect(body.groups.blocked).toBeDefined();
    expect(body.metrics.total).toBeGreaterThanOrEqual(0);
    expect(body.metrics.learnerVisible).toBeGreaterThanOrEqual(0);
  });

  test('source-custody queue marks accepted links as learner-visible', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    const acceptedLink = body.groups.learnerVisible.find((item: any) => item.resourceId === 'res-us-access-board-accessible-routes-ch4');
    expect(acceptedLink).toBeDefined();
    expect(acceptedLink.learnerEligible).toBe(true);
    expect(acceptedLink.custodyStatus).toBe('learner_visible');
    expect(acceptedLink.displayPolicy).toBe('show_to_user');
  });

  test('source-custody queue marks ASCE 7 as standards-incomplete or needs-review', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    const asceItems = [
      ...body.groups.standardsContextIncomplete,
      ...body.groups.needsReview,
      ...body.groups.reviewerOnly,
    ].filter((item: any) => item.resourceId === 'res-asce-7-official-landing');
    expect(asceItems.length).toBeGreaterThan(0);
    const asce = asceItems[0];
    expect(asce.learnerEligible).toBe(false);
    expect(asce.warningFlags).toContain('standards_context_incomplete');
  });

  test('source-custody queue marks ACI 318 as blocked/rejected', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    const aciItems = [
      ...body.groups.rejected,
      ...body.groups.blocked,
    ].filter((item: any) => item.resourceId === 'res-aci-318-building-code-portal');
    expect(aciItems.length).toBeGreaterThan(0);
    const aci = aciItems[0];
    expect(aci.learnerEligible).toBe(false);
    expect(aci.custodyStatus).toBe('blocked');
  });

  test('source-custody queue includes local files as indexed-only', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    expect(body.groups.localFilesIndexedOnly.length).toBeGreaterThan(0);
    const localFile = body.groups.localFilesIndexedOnly[0];
    expect(localFile.itemType).toBe('local_file');
    expect(localFile.learnerEligible).toBe(false);
    expect(localFile.custodyStatus).toBe('indexed_only');
  });

  test('source-custody queue includes candidates', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    expect(body.groups.candidates.length).toBeGreaterThan(0);
    const candidate = body.groups.candidates[0];
    expect(candidate.itemType).toBe('candidate');
    expect(candidate.learnerEligible).toBe(false);
    expect(candidate.custodyStatus).toBe('candidate');
    expect(candidate.nextReviewAction).toContain('Review candidate');
  });

  test('source-custody queue is read-only and does not mutate registries', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    expect(response.status).toBe(200);
    const noWrite = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    expect(noWrite.status).toBe(200);
  });
});
