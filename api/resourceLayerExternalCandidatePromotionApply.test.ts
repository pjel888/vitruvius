// Phase 6N — Resource-Only Promotion Apply Test Suite
// Tests for resource-only promotion apply infrastructure.
// All tests use temp/fixture registries. Production data is NOT touched.

import { describe, it, expect, beforeEach, afterEach } from 'bun:test';
import * as fs from 'fs';
import * as path from 'path';
import api from './index';

function uuidv4(): string {
  return crypto.randomUUID();
}

// Import the module under test
import {
  runAllGates,
  buildResourceOnlyApplyPreview,
  applyResourceOnlyPromotion,
  buildRollbackPreview,
  applyRollback,
  validateCandidateStatus,
  validateMetadataIntegrity,
  validateSourceTruth,
  validateRights,
  validateStandardsContext,
  validateNodeLink,
  validateDisplayLearner,
  validateAudit,
  buildPromotedResource,
  generateResourceId,
} from './resourceLayer/externalCandidatePromotionApply';

import type { ResourceRecord } from './resourceLayer/types';

// ─── Test Fixtures ────────────────────────────────────────────────────────

function makeValidCandidate(overrides: any = {}): any {
  return {
    candidateId: `ec_test_${uuidv4()}`,
    id: `ec_test_${uuidv4()}`,
    status: 'ready_for_promotion_review',
    title: 'Test Standard for Testing',
    resourceType: 'standard',
    sourceType: 'industry-standard',
    url: null,
    doi: null,
    isbn: null,
    rightsStatus: 'open_access',
    verificationStatus: 'unverified',
    learnerVisible: false,
    publisher: 'Test Publisher',
    author: 'Test Author',
    edition: '2026',
    scope: 'Testing requirements',
    sourceContext: 'Publisher metadata',
    safetyFlags: {
      noAutoVerification: true,
      noAutoPromotion: true,
      noAutoLinking: true,
      noLearnerExposure: true,
    },
    decisions: [
      {
        decisionId: `dec_${uuidv4()}`,
        type: 'correction_review',
        reviewer: 'test_reviewer',
        timestamp: new Date().toISOString(),
      },
    ],
    ...overrides,
  };
}

function makeValidApplyInput(overrides: any = {}): any {
  return {
    candidateId: 'ec_test_id',
    applyMode: 'resource_only',
    reviewer: 'test_reviewer',
    rationale: 'Testing resource-only promotion',
    sourceOfContext: 'Test fixture',
    previewHash: 'sha256-test-preview',
    acknowledgeWarnings: true,
    promotionCaveat: 'Test fixture — not externally verified',
    ...overrides,
  };
}

// ─── Test Data Directory ──────────────────────────────────────────────────

const TEST_DIR = path.join(process.cwd(), 'tmp_test_data');
const TEST_RESOURCE_LAYER_DIR = path.join(TEST_DIR, '006_System-Manifests', 'resource-layer');
const TEST_RESOURCES_PATH = path.join(TEST_RESOURCE_LAYER_DIR, 'resources.json');
const TEST_LINKS_PATH = path.join(TEST_RESOURCE_LAYER_DIR, 'node-resource-links.json');
const TEST_REGISTRY_PATH = path.join(TEST_RESOURCE_LAYER_DIR, 'external-metadata-candidates.json');
const TEST_MANIFESTS_DIR = path.join(TEST_RESOURCE_LAYER_DIR, 'transaction-manifests');

function setupTestData(): void {
  fs.mkdirSync(TEST_MANIFESTS_DIR, { recursive: true });
  fs.writeFileSync(TEST_RESOURCES_PATH, `${JSON.stringify({ schemaVersion: 'vitruvius-resource-layer/v1', generatedAt: new Date().toISOString(), resources: [] }, null, 2)}\n`);
  fs.writeFileSync(TEST_LINKS_PATH, `${JSON.stringify({ schemaVersion: 'vitruvius-resource-layer/v1', generatedAt: new Date().toISOString(), nodeResourceLinks: [] }, null, 2)}\n`);
  fs.writeFileSync(TEST_REGISTRY_PATH, `${JSON.stringify({ schemaVersion: 'vitruvius-external-metadata-candidate/v1', generatedAt: new Date().toISOString(), candidates: [] }, null, 2)}\n`);
}

function cleanupTestData(): void {
  try {
    fs.rmSync(TEST_DIR, { recursive: true, force: true });
  } catch {}
}

function writeTempCandidate(candidate: any): void {
  fs.writeFileSync(TEST_REGISTRY_PATH, `${JSON.stringify({
    schemaVersion: 'vitruvius-external-metadata-candidate/v1',
    generatedAt: new Date().toISOString(),
    candidates: [candidate],
  }, null, 2)}\n`);
}

function readTempResources(): any[] {
  return JSON.parse(fs.readFileSync(TEST_RESOURCES_PATH, 'utf-8')).resources;
}

function readTempLinks(): any[] {
  return JSON.parse(fs.readFileSync(TEST_LINKS_PATH, 'utf-8')).nodeResourceLinks;
}

function readTempCandidates(): any[] {
  return JSON.parse(fs.readFileSync(TEST_REGISTRY_PATH, 'utf-8')).candidates;
}

function readTempManifestFiles(): string[] {
  return fs.existsSync(TEST_MANIFESTS_DIR)
    ? fs.readdirSync(TEST_MANIFESTS_DIR).filter((name) => name.endsWith('.json'))
    : [];
}

// ─── Tests ────────────────────────────────────────────────────────────────

describe('Phase 6N — Resource-Only Promotion Apply', () => {

  // ── Gate A: Candidate Status ────────────────────────────────────────────

  describe('Gate A — Candidate Status', () => {
    it('A1: rejects missing candidate', () => {
      const result = validateCandidateStatus(null as any);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('A1');
    });

    it('A2: rejects candidate not ready_for_promotion_review', () => {
      const c = makeValidCandidate({ status: 'review_pending' });
      const result = validateCandidateStatus(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('A2');
    });

    it('A3: rejects rejected candidate', () => {
      const c = makeValidCandidate({ status: 'rejected' });
      const result = validateCandidateStatus(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('A3');
    });

    it('A8: rejects candidate with noAutoPromotion=false', () => {
      const c = makeValidCandidate({ safetyFlags: { noAutoVerification: true, noAutoPromotion: false, noAutoLinking: true, noLearnerExposure: true } });
      const result = validateCandidateStatus(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('A8');
    });

    it('passes valid candidate', () => {
      const c = makeValidCandidate();
      const result = validateCandidateStatus(c);
      expect(result.passed).toBe(true);
    });
  });

  // ── Gate B: Metadata Integrity ─────────────────────────────────────────

  describe('Gate B — Metadata Integrity', () => {
    it('B1: rejects missing title', () => {
      const c = makeValidCandidate({ title: '' });
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('B1');
    });

    it('B2: rejects missing resourceType', () => {
      const c = makeValidCandidate({ resourceType: '' });
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('B2');
    });

    it('B3: rejects missing sourceType', () => {
      const c = makeValidCandidate({ sourceType: '' });
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('B3');
    });

    it('B4: rejects placeholder URL', () => {
      const c = makeValidCandidate({ url: 'http://placeholder' });
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('B4');
    });

    it('B4: rejects placeholder DOI', () => {
      const c = makeValidCandidate({ doi: 'TBD' });
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('B4');
    });

    it('B5: rejects fake publisher', () => {
      const c = makeValidCandidate({ publisher: 'N/A' });
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('B5');
    });

    it('passes clean metadata', () => {
      const c = makeValidCandidate();
      const result = validateMetadataIntegrity(c);
      expect(result.passed).toBe(true);
    });
  });

  // ── Gate C: Source Truth ────────────────────────────────────────────────

  describe('Gate C — Source Truth', () => {
    it('C4: rejects source_verified claim', () => {
      const c = makeValidCandidate({ verificationStatus: 'source_verified' });
      const result = validateSourceTruth(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('C4');
    });

    it('C5: rejects URL reachability claim', () => {
      const c = makeValidCandidate({ urlReachable: true });
      const result = validateSourceTruth(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('C5');
    });

    it('passes unverified candidate', () => {
      const c = makeValidCandidate({ verificationStatus: 'unverified' });
      const result = validateSourceTruth(c);
      expect(result.passed).toBe(true);
    });
  });

  // ── Gate E: Standards Context ──────────────────────────────────────────

  describe('Gate E — Standards Context', () => {
    it('E1: rejects standard without edition/version/scope', () => {
      const c = makeValidCandidate({ edition: '', scope: '' });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('E1');
    });

    it('E2: rejects placeholder edition', () => {
      const c = makeValidCandidate({ edition: 'N/A' });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('E2');
    });

    it('E3: blocks ASCE 7 without real context', () => {
      const c = makeValidCandidate({ title: 'ASCE/SEI 7-22', edition: '', scope: '' });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('E3');
    });

    it('E3: blocks ACI 318 without real context', () => {
      const c = makeValidCandidate({ title: 'ACI 318-19', edition: '', scope: '' });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('E3');
    });

    it('E4: rejects currentStandard claim', () => {
      const c = makeValidCandidate({ currentStandard: true });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('E4');
    });

    it('skips non-standard types', () => {
      const c = makeValidCandidate({ resourceType: 'article', edition: '' });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(true);
    });

    it('passes standard with complete context', () => {
      const c = makeValidCandidate({ edition: '2022', scope: 'Minimum design loads' });
      const result = validateStandardsContext(c);
      expect(result.passed).toBe(true);
    });
  });

  // ── Gate F: Node-Link ──────────────────────────────────────────────────

  describe('Gate F — Node-Link', () => {
    it('F: passes in resource_only mode (skipped)', () => {
      const c = makeValidCandidate();
      const result = validateNodeLink(c, 'resource_only');
      expect(result.passed).toBe(true);
      expect(result.skipped).toBe(true);
    });

    it('F0: rejects resource_and_links mode', () => {
      const c = makeValidCandidate();
      const result = validateNodeLink(c, 'resource_and_links');
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('F0');
    });
  });

  // ── Gate G: Display/Learner ────────────────────────────────────────────

  describe('Gate G — Display/Learner', () => {
    it('G3: rejects learnerVisible=true', () => {
      const c = makeValidCandidate({ learnerVisible: true });
      const result = validateDisplayLearner(c);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('G3');
    });

    it('passes learnerVisible=false', () => {
      const c = makeValidCandidate({ learnerVisible: false });
      const result = validateDisplayLearner(c);
      expect(result.passed).toBe(true);
    });
  });

  // ── Gate I: Audit ───────────────────────────────────────────────────────

  describe('Gate I — Audit', () => {
    it('I1: rejects missing reviewer', () => {
      const input = makeValidApplyInput({ reviewer: '' });
      const result = validateAudit(input);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('I1');
    });

    it('I2: rejects missing rationale', () => {
      const input = makeValidApplyInput({ rationale: '' });
      const result = validateAudit(input);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('I2');
    });

    it('I3: rejects missing sourceOfContext', () => {
      const input = makeValidApplyInput({ sourceOfContext: '' });
      const result = validateAudit(input);
      expect(result.passed).toBe(false);
      expect(result.gate).toBe('I3');
    });

    it('passes complete audit info', () => {
      const input = makeValidApplyInput();
      const result = validateAudit(input);
      expect(result.passed).toBe(true);
    });
  });

  // ── Full Gate Runner ───────────────────────────────────────────────────

  describe('Full Gate Runner', () => {
    it('rejects resource_and_links mode', async () => {
      const c = makeValidCandidate();
      const input = makeValidApplyInput({ applyMode: 'resource_and_links' });
      const result = await runAllGates(c, [], input);
      expect(result.allPassed).toBe(false);
      expect(result.blockingGates[0]).toBe('F0');
    });

    it('blocks ASCE 7 without context', async () => {
      const c = makeValidCandidate({ title: 'ASCE 7-22', edition: '', scope: '' });
      const input = makeValidApplyInput();
      const result = await runAllGates(c, [], input);
      expect(result.allPassed).toBe(false);
      expect(result.blockingGates[0]).toBe('E3');
    });

    it('passes all gates for valid candidate', async () => {
      const c = makeValidCandidate();
      const input = makeValidApplyInput();
      const result = await runAllGates(c, [], input);
      expect(result.allPassed).toBe(true);
    });
  });

  // ── Resource Creation ──────────────────────────────────────────────────

  describe('Resource Creation', () => {
    it('creates resource with safe defaults', () => {
      const c = makeValidCandidate();
      const input = makeValidApplyInput();
      const pdId = `pd_${uuidv4()}`;
      const tmId = `tm_${uuidv4()}`;
      const resource = buildPromotedResource(c, input, pdId, tmId);

      expect(resource.resourceId).toMatch(/^res_/);
      expect(resource.verificationStatus).toBe('unverified');
      expect(resource.custodyStatus).toBe('source_candidate_promoted');
      expect(resource.displayPolicy).toBe('reviewer_only');
      expect(resource.learnerVisibleDefault).toBe(false);
      expect(resource.warningFlags).toContain('not_externally_verified');
      expect(resource.createdFromExternalCandidateId).toBe(c.candidateId);
      expect(resource.promotionDecisionId).toBe(pdId);
      expect(resource.transactionManifestId).toBe(tmId);
      expect(resource.sourceTruthCaveat).toBeTruthy();
    });

    it('does not create nodeResourceLinks', () => {
      const c = makeValidCandidate();
      const input = makeValidApplyInput();
      const pdId = `pd_${uuidv4()}`;
      const tmId = `tm_${uuidv4()}`;
      const resource = buildPromotedResource(c, input, pdId, tmId);

      // Resource record has no link-related fields
      expect((resource as any).nodeResourceLinkIds).toBeUndefined();
    });

    it('sets learnerVisibleDefault to false', () => {
      const c = makeValidCandidate();
      const input = makeValidApplyInput();
      const pdId = `pd_${uuidv4()}`;
      const tmId = `tm_${uuidv4()}`;
      const resource = buildPromotedResource(c, input, pdId, tmId);

      expect(resource.learnerVisibleDefault).toBe(false);
    });
  });

  // ── Duplicate Detection ────────────────────────────────────────────────

  describe('Duplicate Detection', () => {
    it('blocks duplicate title and source type', async () => {
      const existingResources: ResourceRecord[] = [
        {
          resourceId: 'res_existing',
          title: 'Existing Standard',
          resourceType: 'standard',
          sourceType: 'industry-standard',
          custodyStatus: 'source_candidate_promoted',
          verificationStatus: 'unverified',
          displayPolicy: 'reviewer_only',
          learnerVisibleDefault: false,
          reviewer: 'test',
          reviewedAt: new Date().toISOString(),
          rationale: 'test',
          sourceOfContext: 'test',
          createdFromExternalCandidateId: 'ec_old',
          promotionDecisionId: 'pd_old',
          transactionManifestId: 'tm_old',
          sourceTruthCaveat: 'test',
          warningFlags: [],
          rightsStatus: 'open_access',
        } as ResourceRecord,
      ];

      const c = makeValidCandidate({ title: 'Existing Standard', sourceType: 'industry-standard' });
      const input = makeValidApplyInput();
      const result = await runAllGates(c, existingResources, input);

      expect(result.allPassed).toBe(false);
      expect(result.blockingGates[0]).toBe('B7');
    });
  });

  // ── Rollback ───────────────────────────────────────────────────────────

  describe('Rollback', () => {
    it('rollback preview is read-only', async () => {
      setupTestData();
      const preview = await buildRollbackPreview(TEST_DIR, 'res_nonexistent');
      expect(preview).toHaveProperty('success', false);
      cleanupTestData();
    });

    it('hard_delete removes resource record', async () => {
      setupTestData();

      const resource = {
        id: 'res_test_rollback',
        resourceId: 'res_test_rollback',
        title: 'Test Resource',
        resourceType: 'standard',
        sourceAuthority: 'professional_body',
        sourceType: 'industry-standard',
        rightsStatus: 'open_access',
        accessType: 'open_access',
        verificationStatus: 'unverified',
        custodyStatus: 'source_candidate_promoted',
        displayPolicy: 'reviewer_only',
        learnerVisibleDefault: false,
        warningFlags: [],
        disciplineTags: [],
        taxonomyTags: [],
        reviewer: 'test',
        reviewedAt: new Date().toISOString(),
        rationale: 'test',
        sourceOfContext: 'test',
        createdFromExternalCandidateId: 'ec_test',
        promotionDecisionId: 'pd_test',
        transactionManifestId: 'tm_test',
        sourceTruthCaveat: 'test',
        sourceRights: {
          declaredUseBoundary: 'Test fixture reviewer-only metadata.',
        },
        admissionProvenance: {
          admittedBy: 'human',
          admittedAt: new Date().toISOString(),
        },
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      } as ResourceRecord;
      fs.writeFileSync(TEST_RESOURCES_PATH, `${JSON.stringify({
        schemaVersion: 'vitruvius-resource-layer/v1',
        generatedAt: new Date().toISOString(),
        resources: [resource],
      }, null, 2)}\n`);

      expect(readTempResources().length).toBe(1);
      const preview = await buildRollbackPreview(TEST_DIR, 'res_test_rollback');
      expect('canRollback' in preview && preview.canRollback).toBe(true);

      const result = await applyRollback(TEST_DIR, 'res_test_rollback', {
        reviewer: 'test_reviewer',
        rationale: 'Remove temp resource created by fixture',
        rollbackAction: 'hard_delete',
      });
      expect('success' in result && result.success).toBe(true);
      expect(readTempResources().length).toBe(0);
      expect(readTempManifestFiles().length).toBeGreaterThan(0);
      cleanupTestData();
    });
  });

  describe('Hono Routes', () => {
    it('promotion-apply route rejects resource_and_links before candidate lookup', async () => {
      setupTestData();
      const beforeResources = readTempResources().length;
      const response = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fixture/promotion-apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          applyMode: 'resource_and_links',
          reviewer: 'test_reviewer',
          rationale: 'Route gate test',
          sourceOfContext: 'Test fixture',
          previewHash: 'sha256-test-preview',
          acknowledgeWarnings: true,
          promotionCaveat: 'Route gate test',
        }),
      }));
      expect(response.status).toBe(400);
      const body = await response.json();
      expect(body.gate).toBe('F0');
      expect(readTempResources().length).toBe(beforeResources);
      cleanupTestData();
    });

    it('promotion-rollback-preview route requires a resourceId', async () => {
      const response = await api.fetch(new Request('http://localhost/resources/review/external-candidates/fixture/promotion-rollback-preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      }));
      expect(response.status).toBe(400);
    });
  });

  // ── Promotion Apply E2E (via temp registries) ──────────────────────────

  describe('End-to-End Promotion Apply', () => {
    beforeEach(() => {
      setupTestData();
    });

    afterEach(() => {
      cleanupTestData();
    });

    it('creates a Resource with correct defaults', async () => {
      const c = makeValidCandidate();
      const input = makeValidApplyInput({ candidateId: c.candidateId });

      // Verify the built resource
      const pdId = `pd_${uuidv4()}`;
      const tmId = `tm_${uuidv4()}`;
      const resource = buildPromotedResource(c, input, pdId, tmId);

      expect(resource.resourceId).toMatch(/^res_/);
      expect(resource.title).toBe(c.title);
      expect(resource.verificationStatus).toBe('unverified');
      expect(resource.custodyStatus).toBe('source_candidate_promoted');
      expect(resource.displayPolicy).toBe('reviewer_only');
      expect(resource.learnerVisibleDefault).toBe(false);
      expect(resource.createdFromExternalCandidateId).toBe(c.candidateId);
    });

    it('applies resource_only promotion to temp registries only', async () => {
      const c = makeValidCandidate();
      writeTempCandidate(c);
      const input = makeValidApplyInput({ candidateId: c.candidateId });

      const result = await applyResourceOnlyPromotion(TEST_DIR, c.candidateId, input);

      expect(result.success).toBe(true);
      if (!result.success) throw new Error(result.message);
      expect(result.applyMode).toBe('resource_only');
      expect(result.createdResourceId).toMatch(/^res_/);
      expect(result.nodeLinksCreated).toBe(0);
      expect(result.createdNodeResourceLinkIds).toEqual([]);
      expect(result.learnerVisible).toBe(false);
      expect(result.externalVerificationPerformed).toBe(false);
      expect(result.graphMutationApplied).toBe(false);
      expect(result.canonicalMutationApplied).toBe(false);
      expect(result.transactionManifestId).toMatch(/^resource-layer-tx-/);

      const resources = readTempResources();
      expect(resources).toHaveLength(1);
      expect(resources[0].id).toBe(result.createdResourceId);
      expect(resources[0].resourceId).toBe(result.createdResourceId);
      expect(resources[0].verificationStatus).toBe('unverified');
      expect(resources[0].displayPolicy).toBe('reviewer_only');
      expect(resources[0].learnerVisibleDefault).toBe(false);
      expect(readTempLinks()).toHaveLength(0);
      expect(readTempCandidates()[0].decisions.some((decision: any) => decision.type === 'promotion_apply')).toBe(true);
      expect(readTempManifestFiles()).toHaveLength(1);
    });

    it('rejects resource_and_links without writing temp registries', async () => {
      const c = makeValidCandidate();
      writeTempCandidate(c);

      const result = await applyResourceOnlyPromotion(TEST_DIR, c.candidateId, {
        ...makeValidApplyInput({ candidateId: c.candidateId }),
        applyMode: 'resource_and_links',
      });

      expect(result.success).toBe(false);
      if (result.success) throw new Error('resource_and_links should be blocked');
      expect(result.gate).toBe('F0');
      expect(readTempResources()).toHaveLength(0);
      expect(readTempLinks()).toHaveLength(0);
      expect(readTempManifestFiles()).toHaveLength(0);
    });

    it('rolls back a temp resource_only promotion with a manifest', async () => {
      const c = makeValidCandidate();
      writeTempCandidate(c);
      const applyResult = await applyResourceOnlyPromotion(
        TEST_DIR,
        c.candidateId,
        makeValidApplyInput({ candidateId: c.candidateId }),
      );
      expect(applyResult.success).toBe(true);
      if (!applyResult.success) throw new Error(applyResult.message);

      const preview = await buildRollbackPreview(TEST_DIR, applyResult.createdResourceId);
      expect('canRollback' in preview && preview.canRollback).toBe(true);
      expect('rollbackPlan' in preview && preview.rollbackPlan.action).toBe('hard_delete');

      const rollbackResult = await applyRollback(TEST_DIR, applyResult.createdResourceId, {
        reviewer: 'test_reviewer',
        rationale: 'Rollback temp promotion fixture',
        rollbackAction: 'hard_delete',
      });
      expect(rollbackResult.success).toBe(true);
      expect(readTempResources()).toHaveLength(0);
      expect(readTempLinks()).toHaveLength(0);
      expect(readTempManifestFiles()).toHaveLength(2);
    });
  });
});
