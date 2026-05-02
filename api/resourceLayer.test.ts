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
  decideLocalFile,
  decideNodeResourceLink,
  decideResourceCandidate,
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
    expect(reportBody.needsReviewLinks).toBe(3);
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
});
