// Phase 6N — Resource-Only External Candidate Promotion Apply
// This file implements the promotion apply workflow for resource_only mode.
// It enforces gates A-I, creates Resource records, writes transaction manifests,
// and supports rollback preview and apply.
//
// Phase 6N scope: resource_only only. resource_and_links is NOT implemented.

import * as fs from 'fs';
import * as path from 'path';
import { createHash, randomUUID } from 'node:crypto';
import { loadExternalCandidateRegistry, saveRegistry as saveExternalCandidateRegistry } from './externalCandidateRegistry';
import { EXTERNAL_CANDIDATE_REGISTRY_FILE } from './externalCandidateRegistry';
import { resourceLayerFilePaths } from './registry';
import { withResourceLayerTransaction } from './transactionManifest';
import { RESOURCE_LAYER_SCHEMA_VERSION } from './types';
import type {
  AccessType,
  ExternalCandidate,
  ResourceRecord,
  ResourceType,
  SourceAuthority,
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

interface ResourceRegistryPayload {
  schemaVersion: string;
  generatedAt: string;
  resources: ResourceRecord[];
}

interface NodeResourceLinkPayload {
  schemaVersion: string;
  generatedAt?: string;
  nodeResourceLinks: Array<{ id?: string; resourceId?: string }>;
}

function nowIso(): string {
  return new Date().toISOString();
}

function candidateIdOf(candidate: ExternalCandidate): string {
  return String(candidate.candidateId || candidate.id || '');
}

function resourceIdOf(resource: ResourceRecord): string {
  return String(resource.resourceId || resource.id || '');
}

function candidateSafetyFlag(candidate: ExternalCandidate, key: string): unknown {
  return candidate.safetyFlags?.[key] ?? candidate[key];
}

function candidateUrl(candidate: ExternalCandidate): string | null {
  return candidate.url || candidate.proposedUrl || candidate.normalizedUrl || null;
}

function candidateDoi(candidate: ExternalCandidate): string | null {
  return candidate.doi || candidate.proposedDoi || candidate.normalizedDoi || null;
}

function candidateIsbn(candidate: ExternalCandidate): string | null {
  return candidate.isbn || candidate.proposedIsbn || candidate.normalizedIsbn || null;
}

function candidatePublisher(candidate: ExternalCandidate): string | null {
  return candidate.publisher || candidate.proposedPublisher || null;
}

function candidateAuthors(candidate: ExternalCandidate): string[] {
  if (Array.isArray(candidate.authors)) return candidate.authors;
  if (Array.isArray(candidate.proposedAuthors)) return candidate.proposedAuthors;
  if (typeof candidate.author === 'string' && candidate.author.trim()) return [candidate.author.trim()];
  return [];
}

function candidateEdition(candidate: ExternalCandidate): string | null {
  return candidate.edition || candidate.proposedEdition || candidate.proposedVersion || null;
}

function candidateScope(candidate: ExternalCandidate): string | null {
  return candidate.scope || candidate.proposedScope || candidate.sourceContext || null;
}

function candidateJurisdiction(candidate: ExternalCandidate): string | null {
  return candidate.jurisdiction || candidate.proposedJurisdiction || null;
}

function candidateRightsStatus(candidate: ExternalCandidate): string | null {
  return candidate.rightsStatus || candidate.proposedRightsStatus || null;
}

function mapResourceType(resourceType: string | undefined): ResourceType {
  const map: Record<string, ResourceType> = {
    external_url_candidate: 'webpage',
    book_candidate: 'book',
    pdf_candidate: 'pdf',
    standard_candidate: 'standard',
    guide_candidate: 'professional_guidance',
    article_candidate: 'academic_paper',
    dataset_candidate: 'dataset',
    source_family_reference: 'internal_document',
    governing_document: 'code',
    'governing-document': 'code',
    article: 'academic_paper',
    guide: 'professional_guidance',
    standard: 'standard',
    code: 'code',
    book: 'book',
    pdf: 'pdf',
    webpage: 'webpage',
  };
  return map[String(resourceType || '').toLowerCase()] || 'webpage';
}

function mapSourceAuthority(sourceType: string | undefined): SourceAuthority {
  const value = String(sourceType || '').toLowerCase();
  if (/government|federal|state|municipal|public_agency/.test(value)) return 'government';
  if (/academic|university|journal|paper/.test(value)) return 'academic';
  if (/manufacturer|vendor/.test(value)) return 'manufacturer';
  if (/publisher|book/.test(value)) return 'recognized_publisher';
  if (/industry/.test(value)) return 'industry_body';
  if (/professional|standard|standards|society|association/.test(value)) return 'professional_body';
  if (/internal/.test(value)) return 'internal';
  if (/web|url|site/.test(value)) return 'general_web';
  return 'unknown';
}

function mapAccessType(rightsStatus: string | null): AccessType {
  const value = String(rightsStatus || '').toLowerCase();
  if (/open/.test(value)) return 'open_access';
  if (/public/.test(value)) return 'public_web';
  if (/preview/.test(value)) return 'preview_only';
  if (/paywall/.test(value)) return 'paywalled';
  if (/restricted|protected/.test(value)) return 'restricted';
  return 'unknown';
}

function parsePublicationYear(candidate: ExternalCandidate): number | undefined {
  const value = candidate.year || candidate.publicationYear || candidate.proposedPublicationDate;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value !== 'string') return undefined;
  const match = value.match(/\b(19|20)\d{2}\b/);
  return match ? Number(match[0]) : undefined;
}

function resourceLayerExternalCandidateRegistryPath(repoRoot: string): string {
  return path.join(resourceLayerFilePaths(repoRoot).dir, EXTERNAL_CANDIDATE_REGISTRY_FILE);
}

// ─── Gate A: Candidate Status ─────────────────────────────────────────────

function validateCandidateStatus(candidate: ExternalCandidate): GateResult {
  if (!candidate) return { passed: false, gate: 'A1', message: 'Candidate not found' };
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
  if (candidate.status !== 'ready_for_promotion_review') {
    return { passed: false, gate: 'A2', message: `Candidate not ready for promotion review (status: ${candidate.status})` };
  }
  if (!candidate.decisions || candidate.decisions.length === 0) {
    return { passed: false, gate: 'A7', message: 'No review decision history' };
  }

  if (candidateSafetyFlag(candidate, 'noAutoVerification') === false) {
    return { passed: false, gate: 'A8', message: 'noAutoVerification safety flag is false' };
  }
  if (candidateSafetyFlag(candidate, 'noAutoPromotion') === false) {
    return { passed: false, gate: 'A8', message: 'noAutoPromotion safety flag is false' };
  }
  if (candidateSafetyFlag(candidate, 'noAutoLinking') === false) {
    return { passed: false, gate: 'A8', message: 'noAutoLinking safety flag is false' };
  }
  if (candidateSafetyFlag(candidate, 'noLearnerExposure') === false) {
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
  const url = candidateUrl(candidate);
  const doi = candidateDoi(candidate);
  const isbn = candidateIsbn(candidate);
  const publisher = candidatePublisher(candidate);
  const authors = candidateAuthors(candidate);

  if (url && PLACEHOLDER_PATTERNS.some(p => p.test(url))) {
    return { passed: false, gate: 'B4', message: 'Placeholder URL detected' };
  }
  if (doi && PLACEHOLDER_PATTERNS.some(p => p.test(doi))) {
    return { passed: false, gate: 'B4', message: 'Placeholder DOI detected' };
  }
  if (isbn && PLACEHOLDER_PATTERNS.some(p => p.test(isbn))) {
    return { passed: false, gate: 'B4', message: 'Placeholder ISBN detected' };
  }

  // Check fake publisher/author/date values
  if (publisher && FAKE_VALUE_SET.has(publisher.toLowerCase())) {
    return { passed: false, gate: 'B5', message: 'Fake publisher value' };
  }
  if (authors.some((author) => FAKE_VALUE_SET.has(String(author).toLowerCase()))) {
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
  const rightsStatus = candidateRightsStatus(candidate);
  if (!rightsStatus) {
    return { passed: false, gate: 'D1', message: 'Missing rightsStatus' };
  }
  // In resource_only mode, the resource stays reviewer-only,
  // so unknown rights are acceptable as long as no learner exposure is implied.
  if (rightsStatus === 'unknown' && candidate.learnerVisible !== false) {
    return { passed: false, gate: 'D2', message: 'Unknown rights for learner-eligible resource' };
  }
  return { passed: true };
}

// ─── Gate E: Standards Context ───────────────────────────────────────────

function validateStandardsContext(candidate: ExternalCandidate): GateResult {
  const standardTypes = ['standard', 'code', 'governing-document', 'standard_candidate', 'guide_candidate'];
  if (!standardTypes.includes(candidate.resourceType || '')) {
    return { passed: true, skipped: true };
  }

  const title = candidate.title || '';
  const isASCE7 = /ASCE/i.test(title) && /\b7\b/.test(title);
  const isACI318 = /ACI/i.test(title) && /\b318\b/.test(title);
  const edition = candidateEdition(candidate);
  const scope = candidateScope(candidate);
  if (isASCE7 || isACI318) {
    const hasRealContext = edition && !FAKE_VALUE_SET.has(edition.toLowerCase()) &&
      scope && !FAKE_VALUE_SET.has(scope.toLowerCase());
    if (!hasRealContext) {
      return {
        passed: false,
        gate: 'E3',
        message: `${isASCE7 ? 'ASCE 7' : 'ACI 318'} incomplete context — blocked until real context supplied by reviewer`,
      };
    }
  }

  if ((!edition && !candidate.version) || (!scope && !candidate.sourceContext)) {
    return {
      passed: false,
      gate: 'E1',
      message: 'Missing required standards context (edition/version/scope/sourceContext)',
    };
  }

  if (edition && FAKE_VALUE_SET.has(edition.toLowerCase())) {
    return { passed: false, gate: 'E2', message: 'Placeholder standard edition' };
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
    const existingResourceId = resourceIdOf(res);
    const existingSourceType = String(res.sourceType || res.sourceAuthority || '');
    const url = candidateUrl(candidate);
    const doi = candidateDoi(candidate);
    const isbn = candidateIsbn(candidate);
    // Check by URL
    if (url && res.url && url === res.url) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${existingResourceId} has same URL` };
    }
    // Check by DOI
    if (doi && res.doi && doi === res.doi) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${existingResourceId} has same DOI` };
    }
    // Check by ISBN
    if (isbn && (res.isbn || res.isbn10 || res.isbn13) && [res.isbn, res.isbn10, res.isbn13].includes(isbn)) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${existingResourceId} has same ISBN` };
    }
    // Check by title+sourceType
    if (candidate.title && res.title && candidate.sourceType && existingSourceType &&
        candidate.title.toLowerCase() === res.title.toLowerCase() &&
        candidate.sourceType === existingSourceType) {
      return { passed: false, gate: 'B7', message: `Duplicate detected: existing resource ${existingResourceId} has same title+sourceType` };
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
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'A'], results };

  // B
  r = validateMetadataIntegrity(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'B'], results };

  // B7 — Duplicate detection
  r = detectDuplicate(candidate, existingResources);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: ['B7'], results };

  // C
  r = validateSourceTruth(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'C'], results };

  // D
  r = validateRights(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'D'], results };

  // E
  r = validateStandardsContext(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'E'], results };

  // F (skipped in resource_only)
  r = validateNodeLink(candidate, input.applyMode);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'F'], results };

  // G
  r = validateDisplayLearner(candidate);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'G'], results };

  // H
  r = validateTransactionRollback(input);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'H'], results };

  // I
  r = validateAudit(input);
  results.push(r);
  if (!r.passed) return { allPassed: false, blockingGates: [r.gate || 'I'], results };

  return { allPassed: true, blockingGates: [], results };
}

// ─── Resource ID Generation ───────────────────────────────────────────────

function generateResourceId(): string {
  return `res_${randomUUID()}`;
}

function generateTransactionManifestId(): string {
  return `tm_${randomUUID()}`;
}

function generatePromotionDecisionId(): string {
  return `pd_${randomUUID()}`;
}

// ─── Build Promoted Resource ──────────────────────────────────────────────

function buildPromotedResource(
  candidate: ExternalCandidate,
  input: ResourceOnlyApplyInput,
  promotionDecisionId: string,
  transactionManifestId: string,
): ResourceRecord {
  const resourceId = generateResourceId();
  const now = nowIso();
  const rightsStatus = candidateRightsStatus(candidate) || 'unknown';
  const url = candidateUrl(candidate);
  const doi = candidateDoi(candidate);
  const isbn = candidateIsbn(candidate);
  const edition = candidateEdition(candidate) || undefined;
  const jurisdiction = candidateJurisdiction(candidate) || undefined;
  const sourceFamilyId = candidate.sourceFamilyId || candidate.proposedSourceFamilyId || undefined;
  const authors = candidateAuthors(candidate);

  const resource: ResourceRecord = {
    id: resourceId,
    resourceId,
    title: candidate.title || '',
    authors,
    publisher: candidatePublisher(candidate) || undefined,
    year: parsePublicationYear(candidate),
    edition,
    resourceType: mapResourceType(candidate.resourceType),
    sourceAuthority: mapSourceAuthority(candidate.sourceType),
    sourceType: candidate.sourceType || '',
    sourceFamilyIds: sourceFamilyId ? [sourceFamilyId] : [],
    url: url || undefined,
    doi: doi || undefined,
    isbn: isbn || null,
    isbn10: isbn && isbn.replace(/[^0-9X]/gi, '').length === 10 ? isbn : undefined,
    isbn13: isbn && isbn.replace(/[^0-9]/g, '').length === 13 ? isbn : undefined,
    disciplineTags: [],
    taxonomyTags: [],
    jurisdiction,
    geographicScope: jurisdiction ? undefined : 'unknown',
    accessType: mapAccessType(rightsStatus),
    sourceRights: {
      rightsClass: rightsStatus,
      restrictions: ['reviewer_only_metadata_until_accepted_link_eligibility_passes'],
      declaredUseBoundary: 'Reviewer-only Resource Layer metadata from an unverified external candidate; no protected source content admitted.',
    },
    admissionProvenance: {
      admittedBy: 'human',
      admittedAt: now,
      evidenceRef: `external-candidate:${candidateIdOf(candidate)}`,
      custodyChain: ['external_candidate_review', 'resource_only_promotion_apply'],
      reviewSummary: input.rationale,
    },
    verificationStatus: VERIFICATION_UNVERIFIED,
    custodyStatus: RESOURCE_CUSTODY_PROMOTED,
    displayPolicy: DISPLAY_REVIEWER_ONLY,
    warningFlags: ['not_externally_verified', 'reviewer_curated_only'],
    sourceContext: candidate.sourceContext || null,
    reviewer: input.reviewer,
    reviewedAt: now,
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext,
    createdFromExternalCandidateId: candidateIdOf(candidate),
    promotionDecisionId,
    transactionManifestId,
    sourceTruthCaveat: 'Source metadata curated by reviewer; not externally verified',
    standardsContextCaveat: mapResourceType(candidate.resourceType) === 'standard' || mapResourceType(candidate.resourceType) === 'code'
      ? 'Standards context is reviewer-supplied candidate metadata only and is not learner-trusted.'
      : null,
    rightsCaveat: 'Rights status is reviewer-supplied candidate metadata only; no learner exposure is enabled.',
    protectedContentCaveat: null,
    learnerVisibleDefault: false,
    rollbackInfo: null,
    createdAt: now,
    updatedAt: now,
  };

  return resource;
}

// ─── Simple Hash ──────────────────────────────────────────────────────────

function simpleHash(content: string): string {
  return `sha256:${createHash('sha256').update(content).digest('hex')}`;
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
    previewHash: input.previewHash || 'preview_generation',
    acknowledgeWarnings: input.acknowledgeWarnings ?? true,
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

  // Load external candidates
  const candidateRegistry = loadExternalCandidateRegistry(repoRoot);
  const candidates = candidateRegistry.candidates;
  const candidate = candidates.find((c: any) => candidateIdOf(c) === candidateId);
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

  const paths = resourceLayerFilePaths(repoRoot);
  const transaction = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_resource_only_promotion_apply',
    [paths.resources, resourceLayerExternalCandidateRegistryPath(repoRoot)],
    () => {
      const resourcesPayload = loadResourceRegistry(repoRoot);
      resourcesPayload.resources.push(resource);
      saveResourceRegistry(repoRoot, resourcesPayload);

      candidate.decisions = candidate.decisions || [];
      candidate.decisions.push(promotionDecision);
      saveExternalCandidateRegistry(repoRoot, candidateRegistry);

      return resource;
    },
  );

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
    transactionManifestId: transaction.manifest.transactionId,
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
  const resource = resources.find(r => resourceIdOf(r) === resourceId);

  if (!resource) {
    return { success: false, message: `Resource ${resourceId} not found` };
  }

  // Check if resource can be safely hard-deleted
  const dependentLinks = loadNodeResourceLinks(repoRoot).filter((link) => link.resourceId === resourceId);
  const hasDependentLinks = dependentLinks.length > 0;
  const rollbackType = hasDependentLinks ? 'mark_rolled_back' : 'hard_delete';

  return {
    candidateId: resource.createdFromExternalCandidateId,
    promotionDecisionId: resource.promotionDecisionId,
    resourceId: resourceIdOf(resource),
    rollbackPlan: {
      action: rollbackType,
      notes: hasDependentLinks
        ? 'Resource has dependent links — will mark as rolled_back (soft rollback)'
        : 'No dependent links — can hard-delete Resource record',
    },
    preRollbackStateSummary: {
      resourcesBefore: resources.length,
      linksBefore: dependentLinks.length,
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
  const resourcesPayload = loadResourceRegistry(repoRoot);
  const resourceIndex = resourcesPayload.resources.findIndex(r => resourceIdOf(r) === resourceId);

  if (resourceIndex === -1) {
    return { success: false, message: `Resource ${resourceId} not found` };
  }

  const dependentLinks = loadNodeResourceLinks(repoRoot).filter((link) => link.resourceId === resourceId);
  if (dependentLinks.length > 0 && input.rollbackAction === 'hard_delete') {
    return { success: false, message: `Resource ${resourceId} has dependent nodeResourceLinks; hard_delete is blocked` };
  }

  const paths = resourceLayerFilePaths(repoRoot);
  const transaction = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_resource_only_promotion_rollback',
    [paths.resources],
    () => {
      const payload = loadResourceRegistry(repoRoot);
      const idx = payload.resources.findIndex((item) => resourceIdOf(item) === resourceId);
      if (idx === -1) throw new Error(`Resource ${resourceId} not found`);
      if (input.rollbackAction === 'hard_delete') {
        payload.resources.splice(idx, 1);
      } else {
        payload.resources[idx].rollbackInfo = {
          rolledBackAt: nowIso(),
          rolledBackBy: input.reviewer,
          rationale: input.rationale,
          rollbackManifestId: 'pending',
        };
        payload.resources[idx].updatedAt = nowIso();
      }
      saveResourceRegistry(repoRoot, payload);
      return null;
    },
  );

  return {
    success: true,
    rollbackTransactionManifestId: transaction.manifest.transactionId,
    action: input.rollbackAction,
    resourcesAffected: [resourceId],
    linksAffected: [],
    candidateHistoryUpdated: false, // Not updating candidate history in this scope
  };
}

// ─── I/O Helpers ──────────────────────────────────────────────────────────

function loadResources(repoRoot: string): ResourceRecord[] {
  return loadResourceRegistry(repoRoot).resources;
}

function loadResourceRegistry(repoRoot: string): ResourceRegistryPayload {
  const resourcesPath = resourceLayerFilePaths(repoRoot).resources;
  if (!fs.existsSync(resourcesPath)) {
    return {
      schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
      generatedAt: nowIso(),
      resources: [],
    };
  }

  const parsed = JSON.parse(fs.readFileSync(resourcesPath, 'utf-8').replace(/^\uFEFF/, ''));
  if (Array.isArray(parsed)) {
    return {
      schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
      generatedAt: nowIso(),
      resources: parsed as ResourceRecord[],
    };
  }
  if (!parsed || typeof parsed !== 'object' || !Array.isArray(parsed.resources)) {
    throw new Error(`${resourcesPath} must contain an object with a resources array`);
  }
  return {
    schemaVersion: String(parsed.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION),
    generatedAt: String(parsed.generatedAt || nowIso()),
    resources: parsed.resources as ResourceRecord[],
  };
}

function saveResourceRegistry(repoRoot: string, payload: ResourceRegistryPayload): void {
  const resourcesPath = resourceLayerFilePaths(repoRoot).resources;
  fs.mkdirSync(path.dirname(resourcesPath), { recursive: true });
  const next = {
    ...payload,
    schemaVersion: payload.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
  };
  const temp = `${resourcesPath}.tmp`;
  fs.writeFileSync(temp, `${JSON.stringify(next, null, 2)}\n`, 'utf-8');
  if (fs.existsSync(resourcesPath)) fs.rmSync(resourcesPath, { force: true });
  fs.renameSync(temp, resourcesPath);
}

function loadNodeResourceLinks(repoRoot: string): Array<{ id?: string; resourceId?: string }> {
  const linksPath = resourceLayerFilePaths(repoRoot).links;
  if (!fs.existsSync(linksPath)) return [];
  const parsed = JSON.parse(fs.readFileSync(linksPath, 'utf-8').replace(/^\uFEFF/, '')) as NodeResourceLinkPayload | Array<{ id?: string; resourceId?: string }>;
  if (Array.isArray(parsed)) return parsed;
  if (!parsed || typeof parsed !== 'object' || !Array.isArray(parsed.nodeResourceLinks)) {
    throw new Error(`${linksPath} must contain an object with a nodeResourceLinks array`);
  }
  return parsed.nodeResourceLinks;
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
