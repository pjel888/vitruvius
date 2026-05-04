// Phase 6N — Resource-Only External Candidate Promotion Apply
// This file implements the promotion apply workflow for resource_only mode.
// It enforces gates A-I, creates Resource records, writes transaction manifests,
// and supports rollback preview and apply.
//
// Phase 6N scope: resource_only only. resource_and_links is NOT implemented.

import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { loadResourceLayerRegistry, saveResourceLayerRegistry } from './registry';
import { loadExternalMetadataCandidates, saveExternalMetadataCandidates } from './externalMetadataCandidates';
import type {
  ExternalCandidate,
  ResourceRecord,
  TransactionManifest,
  RollbackInfo,
  ResourceOnlyApplyInput,
  ResourceOnlyApplyResult,
  ResourceOnlyApplyFailure,
  RollbackPreviewResult,
  RollbackApplyInput,
  RollbackApplyResult,
} from './types';

// ─── Gate Result Types ───────────────────────────────────────────────────

interface GateResult {
  passed: boolean;
  gate?: string;
  message?: string;
  severity?: 'stop';
  skipped?: boolean;
}

interface GateRunnerResult {
  allPassed: boolean;
  blockingGates: string[];
  results: GateResult[];
}

// ─── Constants ────────────────────────────────────────────────────────────

const PLACEHOLDER_PATTERNS = [
  /^placeholder$/i,
  /^http:\/\/placeholder/i,
  /^https?:\/\/example\./i,
  /^000-0/i,
  /^TBD$/i,
  /^N\/A$/i,
  /^unknown$/i,
  /^todo$/i,
  /^none$/i,
];

const FAKE_VALUE_SET = new Set(['n/a', 'unknown', 'tbd', 'todo', 'placeholder', '', 'none']);

const RESOURCE_CUSTODY_PROMOTED = 'source_candidate_promoted';
const VERIFICATION_UNVERIFIED = 'unverified';
const DISPLAY_REVIEWER_ONLY = 'reviewer_only';

// ─── Gate A: Candidate Status ─────────────────────────────────────────────

function validateCandidateStatus(candidate: ExternalCandidate): GateResult {
  if (!candidate) return { passed: false, gate: 'A1', message: 'Candidate not found' };
  if (candidate.status !== 'ready_for_promotion_review') {
    return { passed: false, gate: 'A2', message: `Candidate not ready for promotion review (status: ${candidate.status})` };
  }
  if (candidate.status === 'rejected') {
    return { passed: false, gate: 'A3', message: 'Candidate was rejected' };
  }
  if (candidate.status === 'deferred') {
    return { passed: false, gate: 'A4', message: 'Candidate is deferred' };
  }
  if (candidate.status === 'duplicate_candidate') {
    return { passed: false, gate: 'A5', message: 'Candidate flagged as duplicate' };
  }
  if (candidate.status === 'promotion_blocked') {
    return { passed: false, gate: 'A6', message: 'Candidate is promotion blocked' };
  }
  if (!candidate.decisions || candidate.decisions.length === 0) {
    return { passed: false, gate: 'A7', message: 'No review decision history' };
  }

  const flags = candidate.safetyFlags || {};
  if (flags.noAutoVerification === false) {
    return { passed: false, gate: 'A8', message: 'noAutoVerification safety flag is false' };
  }
  if (flags.noAutoPromotion === false) {
    return { passed: false, gate: 'A8', message: 'noAutoPromotion safety flag is false' };
  }
  if (flags.noAutoLinking === false) {
    return { passed: false, gate: 'A8', message: 'noAutoLinking safety flag is false' };
  }
  if (flags.noLearnerExposure === false) {
    return { passed: false, gate: 'A8', message: 'noLearnerExposure safety flag is false' };
  }

  return { passed: true };
}

// ─── Gate B: Metadata Integrity ───────────────────────────────────────────

function validateMetadataIntegrity(candidate: ExternalCandidate): GateResult {
  if (!candidate.title || candidate.title.trim() === '') {
    return { passed: false, gate: 'B1', message: 'Missing title' };
  }
  if (!candidate.resourceType) {
    return { passed: false, gate: 'B2', message: 'Missing resourceType' };
  }
  if (!candidate.sourceType) {
    return { passed: false, gate: 'B3', message: 'Missing sourceType' };
  }

  // Check placeholder URL/DOI/ISBN
  if (candidate.url && PLACEHOLDER_PATTERNS.some(p => p.test(candidate.url))) {
    return { passed: false, gate: 'B4', message: 'Placeholder URL detected' };
  }
  if (candidate.doi && PLACEHOLDER_PATTERNS.some(p => p.test(candidate.doi))) {
    return { passed: false, gate: 'B4', message: 'Placeholder DOI detected' };
  }
  if (candidate.isbn && PLACEHOLDER_PATTERNS.some(p => p.test(candidate.isbn))) {
    return { passed: false, gate: 'B4', message: 'Placeholder ISBN detected' };
  }

  // Check fake publisher/author/date values
  if (candidate.publisher && FAKE_VALUE_SET.has(candidate.publisher.toLowerCase())) {
    return { passed: false, gate: 'B5', message: 'Fake publisher value' };
  }
  if (candidate.author && FAKE_VALUE_SET.has(candidate.author.toLowerCase())) {
    return { passed: false, gate: 'B5', message: 'Fake author value' };
  }

  return { passed: true };
}

// ─── Gate C: Source Truth / Verification ──────────────────────────────────

function validateSourceTruth(candidate: ExternalCandidate): GateResult {
  if (candidate.verificationStatus === 'source_verified') {
    return {
      passed: false,
      gate: 'C4',
      message: 'source_verified claim unsupported — no external verification workflow exists',
    };
  }
  if (candidate.urlReachable === true) {
    return { passed: false, gate: 'C5', message: 'URL reachability claim unsupported' };
  }
  if (candidate.doiVerified === true) {
    return { passed: false, gate: 'C5', message: 'DOI verification claim unsupported' };
  }
  if (candidate.isbnVerified === true) {
    return { passed: false, gate: 'C5', message: 'ISBN verification claim unsupported' };
  }
  if (candidate.sourceVerified === true) {
    return { passed: false, gate: 'C5', message: 'Source verification claim unsupported' };
  }
  return { passed: true };
}

// ─── Gate D: Rights ──────────────────────────────────────────────────────

function validateRights(candidate: ExternalCandidate): GateResult {
  if (!candidate.rightsStatus) {
    return { passed: false, gate: 'D1', message: 'Missing rightsStatus' };
  }
  // In resource_only mode, the resource stays reviewer-only,
  // so unknown rights are acceptable as long as no learner exposure is implied.
  if (candidate.rightsStatus === 'unknown' && candidate.learnerVisible !== false) {
    return { passed: false, gate: 'D2', message: 'Unknown rights for learner-eligible resource' };
  }
  return { passed: true };
}

// ─── Gate E: Standards Context ───────────────────────────────────────────

function validateStandardsContext(candidate: ExternalCandidate): GateResult {
  const standardTypes = ['standard', 'code', 'governing-document'];
  if (!standardTypes.includes(candidate.resourceType || '')) {
    return { passed: true, skipped: true };
  }

  if (!candidate.edition && !candidate.version && !candidate.scope && !candidate.sourceContext) {
    return {
      passed: false,
      gate: 'E1',
      message: 'Missing required standards context (edition/version/scope/sourceContext)',
    };
  }

  if (candidate.edition && FAKE_VALUE_SET.has(candidate.edition.toLowerCase())) {
    return { passed: false, gate: 'E2', message: 'Placeholder standard edition' };
  }

  // Block ASCE 7 and ACI 318 without real context
  const title = candidate.title || '';
  const isASCE7 = /ASCE/i.test(title) && /\b7\b/.test(title);
  const isACI318 = /ACI/i.test(title) && /\b318\b/.test(title);
  if (isASCE7 || isACI318) {
    const hasRealContext = candidate.edition && !FAKE_VALUE_SET.has(candidate.edition.toLowerCase()) &&
      candidate.scope && !FAKE_VALUE_SET.has(candidate.scope.toLowerCase());
    if (!hasRealContext) {
      return {
        passed: false,
        gate: 'E3',
        message: `${isASCE7 ? 'ASCE 7' : 'ACI 318'} incomplete context — blocked until real context supplied by reviewer`,
      };
    }
  }

  // Block unsupported governing/compliance claims
  if (candidate.currentStandard === true) {
    return { passed: false, gate: 'E4', message: 'currentStandard claim unsupported without source-verified context' };
  }
  if (candidate.governing === true) {
    return { passed: false, gate: 'E4', message: 'governing claim unsupported without source-verified context' };
  }
  if (candidate.compliant === true) {
    return { passed: false, gate: 'E4', message: 'compliant claim unsupported without source-verified context' };
  }
  if (candidate.ahjAccepted === true) {
    return { passed: false, gate: 'E4', message: 'AHJ acceptance claim unsupported' };
  }

  return { passed: true };
}

// ─── Gate F: Node-Link (Skipped in resource_only) ─────────────────────────

function validateNodeLink(candidate: ExternalCandidate, applyMode: string): GateResult {
  if (applyMode === 'resource_only') {
    return { passed: true, skipped: true };
  }
  return { passed: false, gate: 'F0', message: 'resource_and_links mode not implemented in Phase 6N' };
}

// ─── Gate G: Display / Learner ────────────────────────────────────────────

function validateDisplayLearner(candidate: ExternalCandidate): GateResult {
  if (candidate.learnerVisible === true) {
    return { passed: false, gate: 'G3', message: 'learnerVisible cannot be true for resource-only promotion' };
  }
  return { passed: true };
}

// ─── Gate H: Transaction / Rollback ───────────────────────────────────────

function validateTransactionRollback(input: ResourceOnlyApplyInput): GateResult {
  if (!input.previewHash) {
    return { passed: false, gate: 'H1', message: 'Preview hash required for transaction verification' };
  }
  if (input.acknowledgeWarnings !== true) {
    return { passed: false, gate: 'H3', message: 'Warnings must be acknowledged before promotion' };
  }
  return { passed: true };
}

// ─── Gate I: Audit ────────────────────────────────────────────────────────

function validateAudit(input: ResourceOnlyApplyInput): GateResult {
  if (!input.reviewer || input.reviewer.trim() === '') {
    return { passed: false, gate: 'I1', message: 'Missing reviewer' };
  }
  if (!input.rationale || input.rationale.trim() === '') {
    return { passed: false, gate: 'I2', message: 'Missing rationale' };
  }
  if (!input.sourceOfContext || input.sourceOfContext.trim() === '') {
    return { passed: false, gate: 'I3', message: 'Missing sourceOfContext' };
  }
  if (!input.promotionCaveat || input.promotionCaveat.trim() === '') {
    return { passed: false, gate: 'I6', message: 'Missing promotion caveat' };
  }
  return { passed: true };
}

// ─── Duplicate Detection ──────────────────────────────────────────────────

function detectDuplicate(
  candidate: ExternalCandidate,
  existingResources: ResourceRecord[]
): GateResult {
  for (const res of existingResources) {
    // Check by URL
    if (candidate.url && res.url && candidate.url === res.url) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${res.resourceId} has same URL` };
    }
    // Check by DOI
    if (candidate.doi && res.doi && candidate.doi === res.doi) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${res.resourceId} has same DOI` };
    }
    // Check by ISBN
    if (candidate.isbn && res.isbn && candidate.isbn === res.isbn) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${res.resourceId} has same ISBN` };
    }
    // Check by title+sourceType
    if (candidate.title && res.title && candidate.sourceType && res.sourceType &&
        candidate.title.toLowerCase() === res.title.toLowerCase() &&
        candidate.sourceType === res.sourceType) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${res.resourceId} has same title+sourceType` };
    }
  }
  return { passed: true };
}

// ─── Main Gate Runner ─────────────────────────────────────────────────────

async function runAllGates(
  candidate: ExternalCandidate | null,
  existingResources: ResourceRecord[],
  input: ResourceOnlyApplyInput
): Promise<GateRunnerResult> {
  if (!candidate) {
    return {
      allPassed: false,
      blockingGates: ['A1'],
      results: [{ passed: false, gate: 'A1', message: 'Candidate not found' }],
    };
  }

  const results: GateResult[] = [];

  // A
  let r = validateCandidateStatus(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['A' + (r.gate || '')], results };

  // B
  r = validateMetadataIntegrity(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['B' + (r.gate || '')], results };

  // B7 — Duplicate detection
  r = detectDuplicate(candidate, existingResources);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['B7'], results };

  // C
  r = validateSourceTruth(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['C' + (r.gate || '')], results };

  // D
  r = validateRights(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['D' + (r.gate || '')], results };

  // E
  r = validateStandardsContext(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['E' + (r.gate || '')], results };

  // F (skipped in resource_only)
  r = validateNodeLink(candidate, input.applyMode);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['F' + (r.gate || '')], results };

  // G
  r = validateDisplayLearner(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['G' + (r.gate || '')], results };

  // H
  r = validateTransactionRollback(input);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['H' + (r.gate || '')], results };

  // I
  r = validateAudit(input);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['I' + (r.gate || '')], results };

  return { allPassed: true, blockingGates: [], results };
}

// ─── Resource ID Generation ───────────────────────────────────────────────

function generateResourceId(): string {
  return `res_${uuidv4()}`;
}

function generateTransactionManifestId(): string {
  return `tm_${uuidv4()}`;
}

function generatePromotionDecisionId(): string {
  return `pd_${uuidv4()}`;
}

// ─── Build Promoted Resource ──────────────────────────────────────────────

function buildPromotedResource(
  candidate: ExternalCandidate,
  input: ResourceOnlyApplyInput,
  promotionDecisionId: string,
  transactionManifestId: string,
): ResourceRecord {
  const resourceId = generateResourceId();
  const now = new Date().toISOString();

  const resource: ResourceRecord = {
    resourceId,
    title: candidate.title || '',
    resourceType: candidate.resourceType || '',
    sourceType: candidate.sourceType || '',
    url: candidate.url || null,
    doi: candidate.doi || null,
    isbn: candidate.isbn || null,
    localPath: candidate.localPath || null,
    sourceFamilyId: candidate.sourceFamilyId || null,
    rightsStatus: candidate.rightsStatus || 'unknown',
    verificationStatus: VERIFICATION_UNVERIFIED,
    custodyStatus: RESOURCE_CUSTODY_PROMOTED,
    displayPolicy: DISPLAY_REVIEWER_ONLY,
    warningFlags: ['not_externally_verified', 'reviewer_curated_only'],
    sourceContext: candidate.sourceContext || null,
    reviewer: input.reviewer,
    reviewedAt: now,
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext,
    createdFromExternalCandidateId: candidate.candidateId || candidate.id || '',
    promotionDecisionId,
    transactionManifestId,
    sourceTruthCaveat: 'Source metadata curated by reviewer; not externally verified',
    standardsContextCaveat: null,
    rightsCaveat: null,
    protectedContentCaveat: null,
    learnerVisibleDefault: false,
    rollbackInfo: null,
  };

  return resource;
}

// ─── Build Transaction Manifest ───────────────────────────────────────────

function buildTransactionManifest(
  candidateId: string,
  promotionDecisionId: string,
  resourceId: string,
  input: ResourceOnlyApplyInput,
  touchedFiles: Array<{ filePath: string; beforeHash: string; afterHash: string }>,
  resourceRegistryBefore: string,
  resourceRegistryAfter: string,
  resourcesJsonBefore: string,
  resourcesJsonAfter: string,
): TransactionManifest {
  return {
    transactionManifestId: generateTransactionManifestId(),
    previousManifestHash: null,
    operationType: 'external_candidate_resource_promotion',
    candidateId,
    promotionDecisionId,
    reviewer: input.reviewer,
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext,
    appliedAt: new Date().toISOString(),
    touchedFiles: [
      {
        filePath: 'api/resourceLayer/resources.json',
        operation: 'append',
        beforeHash: simpleHash(resourcesJsonBefore),
        afterHash: simpleHash(resourcesJsonAfter),
      },
      {
        filePath: 'api/resourceLayer/externalMetadataCandidates.json',
        operation: 'update_candidate_history',
        beforeHash: simpleHash(resourceRegistryBefore),
        afterHash: simpleHash(resourceRegistryAfter),
      },
    ],
    createdResourceIds: [resourceId],
    createdLinkIds: [],
    rollbackPlan: {
      resourcesToRemove: [resourceId],
      linksToRemove: [],
      candidateAction: 'append_rollback_decision',
      rollbackType: 'hard_delete_or_mark_rolled_back',
    },
    noGraphCanonicalMutation: true,
    noExternalVerification: true,
    noLearnerExposure: true,
    learnerExposureStatus: 'none',
    rollbackInfo: null,
  };
}

// ─── Simple Hash (placeholder — use crypto in production) ─────────────────

function simpleHash(content: string): string {
  let hash = 0;
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return `sha256-sim-${Math.abs(hash).toString(16).padStart(8, '0')}`;
}

// ─── Build Preview ────────────────────────────────────────────────────────

async function buildResourceOnlyApplyPreview(
  candidate: ExternalCandidate,
  existingResources: ResourceRecord[],
  input: Partial<ResourceOnlyApplyInput>,
): Promise<{
  gateResults: GateRunnerResult;
  resourceDraft: ResourceRecord | null;
  caveats: Record<string, string | null>;
  canApply: boolean;
  previewHash: string;
}> {
  const fullInput: ResourceOnlyApplyInput = {
    candidateId: candidate.candidateId || candidate.id || '',
    applyMode: 'resource_only',
    reviewer: input.reviewer || '',
    rationale: input.rationale || '',
    sourceOfContext: input.sourceOfContext || '',
    previewHash: '',
    acknowledgeWarnings: false,
    promotionCaveat: input.promotionCaveat || '',
  };

  const gateResults = await runAllGates(candidate, existingResources, fullInput);

  if (!gateResults.allPassed) {
    return {
      gateResults,
      resourceDraft: null,
      caveats: {},
      canApply: false,
      previewHash: '',
    };
  }

  const promotionDecisionId = generatePromotionDecisionId();
  const transactionManifestId = generateTransactionManifestId();
  const resourceDraft = buildPromotedResource(candidate, fullInput, promotionDecisionId, transactionManifestId);

  const previewHash = simpleHash(JSON.stringify(resourceDraft));

  return {
    gateResults,
    resourceDraft,
    caveats: {
      sourceTruthCaveat: 'Not externally verified',
      standardsContextCaveat: null,
      rightsCaveat: null,
      verificationCaveat: 'No external verification performed',
    },
    canApply: true,
    previewHash,
  };
}

// ─── Apply Resource-Only Promotion ────────────────────────────────────────

async function applyResourceOnlyPromotion(
  repoRoot: string,
  candidateId: string,
  input: ResourceOnlyApplyInput,
): Promise<ResourceOnlyApplyResult | ResourceOnlyApplyFailure> {
  // Validate applyMode
  if (input.applyMode !== 'resource_only') {
    return {
      success: false,
      gate: 'F0',
      message: 'resource_and_links mode not implemented in Phase 6N',
      severity: 'stop',
      blockingGates: ['F0'],
    };
  }

  // Load registries
  const registryPath = path.join(repoRoot, 'api/resourceLayer');
  const candidatesPath = path.join(registryPath, 'externalMetadataCandidates.json');
  const resourcesPath = path.join(registryPath, 'resources.json');

  // Load external candidates
  const candidates = loadExternalMetadataCandidates(repoRoot);
  const candidate = candidates.find((c: any) => (c.candidateId || c.id) === candidateId);
  if (!candidate) {
    return {
      success: false,
      gate: 'A1',
      message: 'Candidate not found',
      severity: 'stop',
      blockingGates: ['A1'],
    };
  }

  // Load existing resources for duplicate detection
  const existingResources: ResourceRecord[] = loadResources(repoRoot);

  // Run all gates
  const gateResults = await runAllGates(candidate, existingResources, input);
  if (!gateResults.allPassed) {
    return {
      success: false,
      gate: gateResults.blockingGates[0] || 'GATE',
      message: gateResults.results.find(r => !r.passed)?.message || 'Gate check failed',
      severity: 'stop',
      blockingGates: gateResults.blockingGates,
    };
  }

  // Generate IDs
  const promotionDecisionId = generatePromotionDecisionId();
  const transactionManifestId = generateTransactionManifestId();

  // Build resource
  const resource = buildPromotedResource(candidate, input, promotionDecisionId, transactionManifestId);

  // Read current registries for hashes
  const resourceRegistryBefore = JSON.stringify(candidates, null, 2);
  const resourcesJsonBefore = JSON.stringify(existingResources, null, 2);

  // Append resource to registry
  existingResources.push(resource);
  const resourcesJsonAfter = JSON.stringify(existingResources, null, 2);

  // Update candidate history
  const promotionDecision = {
    decisionId: promotionDecisionId,
    type: 'promotion_apply',
    applyMode: 'resource_only',
    createdResourceId: resource.resourceId,
    reviewer: input.reviewer,
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext,
    caveat: input.promotionCaveat,
    timestamp: new Date().toISOString(),
    learnerExposure: false,
    externalVerification: false,
    graphMutation: false,
    canonicalMutation: false,
  };
  candidate.decisions = candidate.decisions || [];
  candidate.decisions.push(promotionDecision);
  const resourceRegistryAfter = JSON.stringify(candidates, null, 2);

  // Build transaction manifest
  const manifest = buildTransactionManifest(
    candidateId,
    promotionDecisionId,
    resource.resourceId,
    input,
    [
      {
        filePath: 'api/resourceLayer/resources.json',
        beforeHash: simpleHash(resourcesJsonBefore),
        afterHash: simpleHash(resourcesJsonAfter),
      },
      {
        filePath: 'api/resourceLayer/externalMetadataCandidates.json',
        beforeHash: simpleHash(resourceRegistryBefore),
        afterHash: simpleHash(resourceRegistryAfter),
      },
    ],
    resourceRegistryBefore,
    resourceRegistryAfter,
    resourcesJsonBefore,
    resourcesJsonAfter,
  );

  // Write back to disk
  saveResources(repoRoot, existingResources);
  saveExternalMetadataCandidates(repoRoot, candidates);
  saveTransactionManifest(repoRoot, manifest);

  return {
    success: true,
    candidateId,
    applyMode: 'resource_only',
    createdResourceId: resource.resourceId,
    createdNodeResourceLinkIds: [],
    learnerVisible: false,
    externalVerificationPerformed: false,
    graphMutationApplied: false,
    canonicalMutationApplied: false,
    nodeLinksCreated: 0,
    transactionManifestId: manifest.transactionManifestId,
    rollbackPlan: {
      resourcesToRemove: [resource.resourceId],
      linksToRemove: [],
      rollbackType: 'hard_delete_or_mark_rolled_back',
    },
    sourceTruthCaveat: resource.sourceTruthCaveat || '',
    standardsContextCaveat: resource.standardsContextCaveat,
    rightsCaveat: resource.rightsCaveat,
    verificationCaveat: 'No external verification performed; URL/DOI/ISBN not verified for reachability or existence',
  };
}

// ─── Rollback Preview ─────────────────────────────────────────────────────

async function buildRollbackPreview(
  repoRoot: string,
  resourceId: string,
): Promise<RollbackPreviewResult | { success: false; message: string }> {
  const resources: ResourceRecord[] = loadResources(repoRoot);
  const resource = resources.find(r => r.resourceId === resourceId);

  if (!resource) {
    return { success: false, message: `Resource ${resourceId} not found` };
  }

  // Check if resource can be safely hard-deleted
  const hasDependentLinks = false; // No link registry for resource_only scope
  const rollbackType = hasDependentLinks ? 'mark_rolled_back' : 'hard_delete';

  return {
    candidateId: resource.createdFromExternalCandidateId,
    promotionDecisionId: resource.promotionDecisionId,
    resourceId: resource.resourceId,
    rollbackPlan: {
      action: rollbackType,
      notes: hasDependentLinks
        ? 'Resource has dependent links — will mark as rolled_back (soft rollback)'
        : 'No dependent links — can hard-delete Resource record',
    },
    preRollbackStateSummary: {
      resourcesBefore: resources.length,
      linksBefore: 0,
    },
    canRollback: true,
  };
}

// ─── Rollback Apply ───────────────────────────────────────────────────────

async function applyRollback(
  repoRoot: string,
  resourceId: string,
  input: RollbackApplyInput,
): Promise<RollbackApplyResult | { success: false; message: string }> {
  const resources: ResourceRecord[] = loadResources(repoRoot);
  const resourceIndex = resources.findIndex(r => r.resourceId === resourceId);

  if (resourceIndex === -1) {
    return { success: false, message: `Resource ${resourceId} not found` };
  }

  const resource = resources[resourceIndex];
  const rollbackManifestId = generateTransactionManifestId();

  if (input.rollbackAction === 'hard_delete') {
    // Check if any other record references this resource
    // In resource_only mode, no nodeResourceLinks exist, so hard-delete is safe
    resources.splice(resourceIndex, 1);
  } else {
    // Mark as rolled_back
    resource.rollbackInfo = {
      rolledBackAt: new Date().toISOString(),
      rolledBackBy: input.reviewer,
      rationale: input.rationale,
      rollbackManifestId,
    };
  }

  saveResources(repoRoot, resources);

  // Create rollback manifest
  const rollbackManifest: TransactionManifest = {
    transactionManifestId: rollbackManifestId,
    previousManifestHash: null,
    operationType: 'external_candidate_resource_promotion_rollback',
    candidateId: resource.createdFromExternalCandidateId,
    promotionDecisionId: resource.promotionDecisionId,
    reviewer: input.reviewer,
    rationale: input.rationale,
    sourceOfContext: '',
    appliedAt: new Date().toISOString(),
    touchedFiles: [
      {
        filePath: 'api/resourceLayer/resources.json',
        operation: input.rollbackAction === 'hard_delete' ? 'remove' : 'update',
        beforeHash: '',
        afterHash: '',
      },
    ],
    createdResourceIds: [],
    createdLinkIds: [],
    rollbackPlan: null,
    noGraphCanonicalMutation: true,
    noExternalVerification: true,
    noLearnerExposure: true,
    learnerExposureStatus: 'none',
    rollbackInfo: null,
  };
  saveTransactionManifest(repoRoot, rollbackManifest);

  return {
    success: true,
    rollbackTransactionManifestId: rollbackManifestId,
    action: input.rollbackAction,
    resourcesAffected: [resourceId],
    linksAffected: [],
    candidateHistoryUpdated: false, // Not updating candidate history in this scope
  };
}

// ─── I/O Helpers ──────────────────────────────────────────────────────────

function loadResources(repoRoot: string): ResourceRecord[] {
  const resourcesPath = path.join(repoRoot, 'api/resourceLayer/resources.json');
  try {
    const data = fs.readFileSync(resourcesPath, 'utf-8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

function saveResources(repoRoot: string, resources: ResourceRecord[]): void {
  const resourcesPath = path.join(repoRoot, 'api/resourceLayer/resources.json');
  fs.writeFileSync(resourcesPath, JSON.stringify(resources, null, 2), 'utf-8');
}

function saveTransactionManifest(repoRoot: string, manifest: TransactionManifest): void {
  const manifestsPath = path.join(repoRoot, 'api/resourceLayer/transactionManifests.json');
  let manifests: TransactionManifest[] = [];
  try {
    const data = fs.readFileSync(manifestsPath, 'utf-8');
    manifests = JSON.parse(data);
  } catch {
    manifests = [];
  }
  manifests.push(manifest);
  fs.writeFileSync(manifestsPath, JSON.stringify(manifests, null, 2), 'utf-8');
}

// ─── Exports ──────────────────────────────────────────────────────────────

export {
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
  validateTransactionRollback,
  validateAudit,
  buildPromotedResource,
  generateResourceId,
  generateTransactionManifestId,
  generatePromotionDecisionId,
};

export type { GateResult, GateRunnerResult, ResourceOnlyApplyInput, ResourceOnlyApplyResult, ResourceOnlyApplyFailure };
