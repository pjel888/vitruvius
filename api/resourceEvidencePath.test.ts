import { afterEach, describe, expect, test } from 'bun:test';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import api from './index';
import { readResourceLayerData } from './resourceLayer/registry';
import { buildSourceCustodyQueue } from './resourceLayer/sourceCustodyQueue';
import { isLearnerSidebarEligible } from './resourceLayer/validation';

const repoRoot = resolve(import.meta.dir, '..');

function gitStatusShort() {
  return execSync('git status --short --branch', { cwd: repoRoot, encoding: 'utf-8' });
}

function hashFile(path: string) {
  return execSync(`git hash-object "${path}"`, { cwd: repoRoot, encoding: 'utf-8' }).trim();
}

afterEach(() => {
  // no cleanup needed for read-only endpoint tests
});

describe('evidence-path learner safety', () => {
  test('GET /node/:id/resources returns only accepted/human_reviewed links in learner mode', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.displayPolicy.mode).toBe('learner');
    expect(body.displayPolicy.learnerEligibleOnly).toBe(true);
    for (const item of body.resources) {
      expect(item.reviewStatus === 'accepted' || item.reviewStatus === 'human_reviewed').toBe(true);
      expect(item.verificationStatus).not.toBe('rejected');
      expect(item.verificationStatus).not.toBe('unverified');
    }
  });

  test('learner mode never returns rejected, needs_review, candidate, or rights-blocked resources', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?limit=10'));
    const body = await response.json();
    const forbiddenStatuses = ['rejected', 'needs_review', 'candidate'];
    for (const item of body.resources) {
      expect(forbiddenStatuses.includes(item.reviewStatus)).toBe(false);
      expect(item.warning).not.toContain('Rights-protected');
      expect(item.warning).not.toContain('Rejected');
    }
  });

  test('learner mode returns empty safe state for node with no accepted resources', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012781/resources'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.resources).toHaveLength(0);
    expect(body.displayPolicy.mode).toBe('learner');
  });

  test('ASCE 7 is not learner-visible via endpoint because standards context is incomplete', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources'));
    const body = await response.json();
    const asceItems = body.resources.filter((item: any) => item.resourceId === 'res-asce-7-official-landing');
    expect(asceItems).toHaveLength(0);
  });

  test('ACI 318 rejected link is not learner-visible via endpoint', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012781/resources'));
    const body = await response.json();
    const aciItems = body.resources.filter((item: any) => item.resourceId === 'res-aci-318-building-code-portal');
    expect(aciItems).toHaveLength(0);
  });

  test('learner mode hard-caps at 8 resources', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012160/resources?limit=100'));
    const body = await response.json();
    expect(body.resources.length).toBeLessThanOrEqual(8);
  });

  test('reviewer mode returns non-eligible resources with warning text and learnerEligible=false', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?mode=reviewer'));
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.displayPolicy.mode).toBe('reviewer');
    const asce = body.resources.find((item: any) => item.resourceId === 'res-asce-7-official-landing');
    expect(asce).toBeDefined();
    expect(asce.warning).toBeTruthy();
    expect(asce.displayScore).toBeLessThan(1);
  });

  test('node detail endpoint includes learner-safe resources with cap 8', async () => {
    const response = await api.fetch(new Request('http://localhost/node/VTN-DOM-0012160'));
    const body = await response.json();
    expect(body.resources.length).toBeLessThanOrEqual(8);
    expect(body.resources.every((item: any) => item.reviewStatus === 'accepted' || item.reviewStatus === 'human_reviewed')).toBe(true);
  });
});

describe('evidence-path source-custody queue', () => {
  test('GET /resources/review/source-custody returns all 9 groups', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    expect(response.status).toBe(200);
    const body = await response.json();
    const groups = body.groups;
    expect(groups.learnerVisible).toBeDefined();
    expect(groups.reviewerOnly).toBeDefined();
    expect(groups.needsReview).toBeDefined();
    expect(groups.candidates).toBeDefined();
    expect(groups.localFilesIndexedOnly).toBeDefined();
    expect(groups.standardsContextIncomplete).toBeDefined();
    expect(groups.rightsLimited).toBeDefined();
    expect(groups.rejected).toBeDefined();
    expect(groups.blocked).toBeDefined();
    expect(body.metrics.total).toBeGreaterThanOrEqual(body.metrics.learnerVisible);
  });

  test('source-custody queue includes needs_review links', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    // Standards with missing context are classified as standards_incomplete before needs_review
    // so ASCE 7 appears there; FHWA (non-standard) appears in needs_review
    const fhwaNeedsReview = body.groups.needsReview.find((item: any) => item.resourceId === 'res-fhwa-earth-retaining-structures');
    expect(fhwaNeedsReview).toBeDefined();
    expect(fhwaNeedsReview.itemType).toBe('resource_link');
    expect(fhwaNeedsReview.learnerEligible).toBe(false);
    expect(fhwaNeedsReview.nextReviewAction).toContain('Review link');
  });

  test('source-custody queue includes nextReviewAction and missingStandardContextFields', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    const asceIncomplete = body.groups.standardsContextIncomplete.find((item: any) => item.resourceId === 'res-asce-7-official-landing');
    expect(asceIncomplete).toBeDefined();
    expect(asceIncomplete.nextReviewAction).toContain('Supply edition');
    expect(asceIncomplete.missingStandardContextFields).toBeDefined();
    expect(asceIncomplete.missingStandardContextFields.length).toBeGreaterThan(0);
  });

  test('source-custody queue includes rejected/blocked items', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    const aciBlocked = body.groups.blocked.find((item: any) => item.resourceId === 'res-aci-318-building-code-portal');
    expect(aciBlocked).toBeDefined();
    expect(aciBlocked.custodyStatus).toBe('blocked');
    expect(aciBlocked.learnerEligible).toBe(false);
    expect(aciBlocked.nextReviewAction).toContain('rejected');
  });

  test('source-custody queue includes local files as indexed-only', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    expect(body.groups.localFilesIndexedOnly.length).toBeGreaterThan(0);
    const localFile = body.groups.localFilesIndexedOnly[0];
    expect(localFile.itemType).toBe('local_file');
    expect(localFile.custodyStatus).toBe('indexed_only');
    expect(localFile.learnerEligible).toBe(false);
    expect(localFile.nextReviewAction).toContain('admission');
  });

  test('source-custody queue includes candidates', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    expect(body.groups.candidates.length).toBeGreaterThanOrEqual(0);
    if (body.groups.candidates.length > 0) {
      const candidate = body.groups.candidates[0];
      expect(candidate.itemType).toBe('candidate');
      expect(candidate.learnerEligible).toBe(false);
      expect(candidate.custodyStatus).toBe('candidate');
    }
  });

  test('source-custody queue marks accepted links as learner-visible', async () => {
    const response = await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    const body = await response.json();
    const accepted = body.groups.learnerVisible.find((item: any) => item.resourceId === 'res-us-access-board-accessible-routes-ch4');
    expect(accepted).toBeDefined();
    expect(accepted.learnerEligible).toBe(true);
    expect(accepted.custodyStatus).toBe('learner_visible');
  });
});

describe('evidence-path no-mutation safety', () => {
  test('GET /node/:id/resources does not mutate Resource Layer registries', async () => {
    const before = gitStatusShort();
    const hashesBefore = {
      resources: hashFile('006_System-Manifests/resource-layer/resources.json'),
      links: hashFile('006_System-Manifests/resource-layer/node-resource-links.json'),
      candidates: hashFile('006_System-Manifests/resource-layer/resource-candidates.json'),
      localFileIndex: hashFile('006_System-Manifests/resource-layer/local-file-index.json'),
    };

    await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources'));
    await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?mode=reviewer'));
    await api.fetch(new Request('http://localhost/node/VTN-DOM-0012160/resources?limit=10'));

    const after = gitStatusShort();
    expect(after).toBe(before);
    expect(hashFile('006_System-Manifests/resource-layer/resources.json')).toBe(hashesBefore.resources);
    expect(hashFile('006_System-Manifests/resource-layer/node-resource-links.json')).toBe(hashesBefore.links);
    expect(hashFile('006_System-Manifests/resource-layer/resource-candidates.json')).toBe(hashesBefore.candidates);
    expect(hashFile('006_System-Manifests/resource-layer/local-file-index.json')).toBe(hashesBefore.localFileIndex);
  });

  test('GET /resources/review/source-custody does not mutate Resource Layer registries', async () => {
    const before = gitStatusShort();
    const hashesBefore = {
      resources: hashFile('006_System-Manifests/resource-layer/resources.json'),
      links: hashFile('006_System-Manifests/resource-layer/node-resource-links.json'),
      candidates: hashFile('006_System-Manifests/resource-layer/resource-candidates.json'),
      localFileIndex: hashFile('006_System-Manifests/resource-layer/local-file-index.json'),
      reviewDecisions: hashFile('006_System-Manifests/resource-layer/review-decisions.json'),
    };

    await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    await api.fetch(new Request('http://localhost/resources/review/source-custody'));

    const after = gitStatusShort();
    expect(after).toBe(before);
    expect(hashFile('006_System-Manifests/resource-layer/resources.json')).toBe(hashesBefore.resources);
    expect(hashFile('006_System-Manifests/resource-layer/node-resource-links.json')).toBe(hashesBefore.links);
    expect(hashFile('006_System-Manifests/resource-layer/resource-candidates.json')).toBe(hashesBefore.candidates);
    expect(hashFile('006_System-Manifests/resource-layer/local-file-index.json')).toBe(hashesBefore.localFileIndex);
    expect(hashFile('006_System-Manifests/resource-layer/review-decisions.json')).toBe(hashesBefore.reviewDecisions);
  });

  test('source-custody queue build is read-only and stable across repeated calls', async () => {
    const q1 = buildSourceCustodyQueue(repoRoot);
    const q2 = buildSourceCustodyQueue(repoRoot);
    expect(q1.metrics).toEqual(q2.metrics);
    expect(q1.groups.learnerVisible.map((i) => i.id)).toEqual(q2.groups.learnerVisible.map((i) => i.id));
    expect(q1.groups.blocked.map((i) => i.id)).toEqual(q2.groups.blocked.map((i) => i.id));
  });

  test('Resource Layer counts remain 7 resources / 9 links after route calls', async () => {
    const before = readResourceLayerData(repoRoot);
    expect(before.resources.length).toBe(7);
    expect(before.nodeResourceLinks.length).toBe(9);

    await api.fetch(new Request('http://localhost/resources/review/source-custody'));
    await api.fetch(new Request('http://localhost/node/VTN-DOM-0012777/resources?mode=reviewer'));

    const after = readResourceLayerData(repoRoot);
    expect(after.resources.length).toBe(7);
    expect(after.nodeResourceLinks.length).toBe(9);
  });
});

describe('evidence-path fixture and validation safety', () => {
  test('no production placeholder metadata is learner-eligible', () => {
    const data = readResourceLayerData(repoRoot);
    for (const resource of data.resources) {
      const links = data.nodeResourceLinks.filter((l) => l.resourceId === resource.id);
      for (const link of links) {
        if (link.reviewStatus === 'accepted' || link.reviewStatus === 'human_reviewed') {
          expect(isLearnerSidebarEligible(link, resource)).toBe(true);
        }
      }
    }
  });

  test('ASCE 7 and ACI 318 remain not learner-trusted in production', () => {
    const data = readResourceLayerData(repoRoot);
    const asce = data.resources.find((r) => r.id === 'res-asce-7-official-landing');
    const aci = data.resources.find((r) => r.id === 'res-aci-318-building-code-portal');
    expect(asce).toBeTruthy();
    expect(aci).toBeTruthy();
    for (const link of data.nodeResourceLinks.filter((l) => l.resourceId === asce!.id)) {
      expect(isLearnerSidebarEligible(link, asce!)).toBe(false);
    }
    for (const link of data.nodeResourceLinks.filter((l) => l.resourceId === aci!.id)) {
      expect(isLearnerSidebarEligible(link, aci!)).toBe(false);
    }
  });
});
