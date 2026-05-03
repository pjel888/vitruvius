import { afterEach, describe, expect, test } from 'bun:test';
import { rmSync } from 'node:fs';
import { resolve } from 'node:path';
import { readResourceLayerData } from './resourceLayer/registry';
import { isLearnerSidebarEligible, validateResourceLayerData } from './resourceLayer/validation';
import type { NodeResourceLink, Resource, ResourceLayerData, SourceFamily } from './resourceLayer/types';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './resourceLayer/types';

const repoRoot = resolve(import.meta.dir, '..');

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

afterEach(() => {
  // Ensure any .tmp directories created by other test files are cleaned
  const tmpDir = resolve(import.meta.dir, '.tmp-resource-layer-test');
  rmSync(tmpDir, { recursive: true, force: true });
});

describe('standards-context validation rules', () => {
  test('accepted standard missing edition/version/scope becomes blocker', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        sourceFamilyIds: ['asce'],
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
      })],
      nodeResourceLinks: [minimalLink({
        id: 'link-std',
        resourceId: 'res-std',
        reviewStatus: 'accepted',
      })],
    }), { repoRoot });
    expect(result.ok).toBe(false);
    expect(result.blockers.some((b) => b.includes('accepted standard/code-like link requires edition'))).toBe(true);
  });

  test('needs-review standard missing edition/version/scope remains warning, not blocker', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
      })],
      nodeResourceLinks: [minimalLink({
        id: 'link-std',
        resourceId: 'res-std',
        reviewStatus: 'needs_review',
      })],
    }), { repoRoot });
    expect(result.ok).toBe(true);
    expect(result.blockers).toHaveLength(0);
    expect(result.warnings.some((w) => w.includes('standard/code-like link missing'))).toBe(true);
  });

  test('rejected standard missing context does not become blocker', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
      })],
      nodeResourceLinks: [minimalLink({
        id: 'link-std',
        resourceId: 'res-std',
        reviewStatus: 'rejected',
      })],
    }), { repoRoot });
    expect(result.ok).toBe(true);
    expect(result.blockers).toHaveLength(0);
  });

  test('placeholder standard edition values are rejected', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
        standardIdentifier: { organization: 'ASCE', code: '7', edition: 'latest' },
      })],
    }), { repoRoot });
    expect(result.warnings.some((w) => w.includes('placeholder'))).toBe(true);
  });

  test('placeholder standard version values are rejected', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
        editionContext: { version: 'current' },
      })],
    }), { repoRoot });
    expect(result.warnings.some((w) => w.includes('placeholder'))).toBe(true);
  });

  test('placeholder scope/citation/sourceOfContext values are rejected', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
        reviewContext: {
          contextStatus: 'justified_missing',
          reviewedBy: 'human',
          rationale: 'TBD',
          sourceOfContext: 'unknown',
        },
      })],
    }), { repoRoot });
    expect(result.warnings.some((w) => w.includes('placeholder'))).toBe(true);
  });

  test('latest and current are rejected as fake context', () => {
    const result = validateResourceLayerData(minimalData({
      resources: [minimalResource({
        id: 'res-std',
        resourceType: 'standard',
        url: 'https://example.com/std',
        canonicalUrl: 'https://example.com/std',
        edition: 'latest',
        standardIdentifier: { organization: 'ASCE', code: '7', edition: 'current', publicationYear: 2022 },
      })],
    }), { repoRoot });
    const placeholderWarnings = result.warnings.filter((w) => w.includes('placeholder'));
    expect(placeholderWarnings.length).toBeGreaterThanOrEqual(2);
  });

  test('complete standards context requires reviewer, rationale, sourceOfContext, and reviewedAt or equivalent', () => {
    const resource = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      url: 'https://standards-body.org/std-2022',
      canonicalUrl: 'https://standards-body.org/std-2022',
      edition: 'Std-2022',
      jurisdiction: 'United States',
      geographicScope: 'us',
      sourceRights: { declaredUseBoundary: 'learner_visible' },
      admissionProvenance: { admittedBy: 'human', admittedAt: '2026-05-01T00:00:00.000Z' },
      reviewContext: {
        contextStatus: 'complete',
        reviewedBy: 'human-reviewer',
        reviewedAt: '2026-05-01T00:00:00.000Z',
        rationale: 'Edition and jurisdiction confirmed against official site.',
        sourceOfContext: 'https://standards-body.org/std-2022',
        confidence: 'high',
      },
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'accepted',
      sectionRefs: ['Chapter 26'],
    });
    const result = validateResourceLayerData(minimalData({
      resources: [resource],
      nodeResourceLinks: [link],
    }), { repoRoot });
    expect(result.ok).toBe(true);
    expect(result.blockers).toHaveLength(0);
    expect(result.warnings).toHaveLength(0);
    expect(isLearnerSidebarEligible(link, resource)).toBe(true);
  });

  test('justified missing context requires reviewer, rationale, sourceOfContext, and is not placeholder', () => {
    const resourceWithJustification = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      url: 'https://example.com/std',
      canonicalUrl: 'https://example.com/std',
      sourceRights: { declaredUseBoundary: 'learner_visible' },
      admissionProvenance: { admittedBy: 'human', admittedAt: '2026-05-01T00:00:00.000Z' },
      reviewContext: {
        contextStatus: 'justified_missing',
        reviewedBy: 'human-reviewer',
        reviewedAt: '2026-05-01T00:00:00.000Z',
        rationale: 'Landing page only; full standard requires purchase for edition detail.',
        sourceOfContext: 'Reviewer assessment of ASCE landing page.',
        confidence: 'medium',
      },
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'accepted',
    });
    const result = validateResourceLayerData(minimalData({
      resources: [resourceWithJustification],
      nodeResourceLinks: [link],
    }), { repoRoot });
    expect(result.ok).toBe(true);
    expect(result.blockers).toHaveLength(0);
    expect(isLearnerSidebarEligible(link, resourceWithJustification)).toBe(true);
  });

  test('justified missing context with placeholder rationale is blocked', () => {
    const resourceWithFakeJustification = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      url: 'https://example.com/std',
      canonicalUrl: 'https://example.com/std',
      reviewContext: {
        contextStatus: 'justified_missing',
        reviewedBy: 'human-reviewer',
        reviewedAt: '2026-05-01T00:00:00.000Z',
        rationale: 'TBD',
        sourceOfContext: 'unknown',
        confidence: 'low',
      },
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'accepted',
    });
    const result = validateResourceLayerData(minimalData({
      resources: [resourceWithFakeJustification],
      nodeResourceLinks: [link],
    }), { repoRoot });
    expect(result.ok).toBe(false);
    expect(result.blockers.some((b) => b.includes('accepted standard/code-like link requires edition'))).toBe(true);
    expect(isLearnerSidebarEligible(link, resourceWithFakeJustification)).toBe(false);
  });
});

describe('ASCE 7 and ACI 318 production state', () => {
  test('ASCE 7 remains incomplete and not learner-trusted', () => {
    const data = readResourceLayerData(repoRoot);
    const asceResource = data.resources.find((r) => r.id === 'res-asce-7-official-landing');
    expect(asceResource).toBeTruthy();
    expect(asceResource!.resourceType).toBe('standard');
    const asceLinks = data.nodeResourceLinks.filter((l) => l.resourceId === 'res-asce-7-official-landing');
    expect(asceLinks.length).toBeGreaterThanOrEqual(1);
    for (const link of asceLinks) {
      expect(link.reviewStatus).not.toBe('accepted');
      expect(isLearnerSidebarEligible(link, asceResource!)).toBe(false);
    }
  });

  test('ACI 318 remains incomplete and not learner-trusted', () => {
    const data = readResourceLayerData(repoRoot);
    const aciResource = data.resources.find((r) => r.id === 'res-aci-318-building-code-portal');
    expect(aciResource).toBeTruthy();
    expect(aciResource!.resourceType).toBe('standard');
    const aciLinks = data.nodeResourceLinks.filter((l) => l.resourceId === 'res-aci-318-building-code-portal');
    expect(aciLinks.length).toBeGreaterThanOrEqual(1);
    for (const link of aciLinks) {
      expect(link.reviewStatus).not.toBe('accepted');
      expect(isLearnerSidebarEligible(link, aciResource!)).toBe(false);
    }
  });
});

describe('standards-context visibility and gating', () => {
  test('incomplete accepted standard is learner-hidden unless justified', () => {
    const resource = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      sourceFamilyIds: ['asce'],
      url: 'https://example.com/std',
      canonicalUrl: 'https://example.com/std',
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'accepted',
    });
    expect(isLearnerSidebarEligible(link, resource)).toBe(false);
  });

  test('incomplete accepted standard with justification is learner-warning-gated', () => {
    const resource = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      sourceFamilyIds: ['asce'],
      url: 'https://example.com/std',
      canonicalUrl: 'https://example.com/std',
      reviewContext: {
        contextStatus: 'justified_missing',
        reviewedBy: 'human-reviewer',
        reviewedAt: '2026-05-01T00:00:00.000Z',
        rationale: 'Landing page only; full standard requires purchase for edition detail.',
        sourceOfContext: 'Reviewer assessment of ASCE landing page.',
        confidence: 'medium',
      },
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'accepted',
    });
    expect(isLearnerSidebarEligible(link, resource)).toBe(true);
  });

  test('needs_review incomplete standard is reviewer-only visible', () => {
    const resource = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      sourceFamilyIds: ['asce'],
      url: 'https://example.com/std',
      canonicalUrl: 'https://example.com/std',
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'needs_review',
    });
    expect(isLearnerSidebarEligible(link, resource)).toBe(false);
  });

  test('human_reviewed complete standard is learner-visible', () => {
    const resource = minimalResource({
      id: 'res-std',
      resourceType: 'standard',
      sourceFamilyIds: ['asce'],
      url: 'https://example.com/std',
      canonicalUrl: 'https://example.com/std',
      edition: 'ASCE 7-22',
      jurisdiction: 'United States',
      geographicScope: 'us',
      reviewContext: {
        contextStatus: 'complete',
        reviewedBy: 'human-reviewer',
        reviewedAt: '2026-05-01T00:00:00.000Z',
        rationale: 'Edition and jurisdiction confirmed.',
        sourceOfContext: 'ASCE official site',
        confidence: 'high',
      },
    });
    const link = minimalLink({
      id: 'link-std',
      resourceId: 'res-std',
      reviewStatus: 'human_reviewed',
      sectionRefs: ['Chapter 26'],
    });
    expect(isLearnerSidebarEligible(link, resource)).toBe(true);
  });
});

describe('no-write validation safety', () => {
  test('Resource Layer no-write validation does not dirty files', () => {
    const { execSync } = require('node:child_process');
    const before = execSync('git status --short --branch', { cwd: repoRoot, encoding: 'utf-8' });
    validateResourceLayerData(readResourceLayerData(repoRoot), { repoRoot });
    const after = execSync('git status --short --branch', { cwd: repoRoot, encoding: 'utf-8' });
    expect(after).toBe(before);
  });
});
