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
import { isLearnerSidebarEligible } from './validation';
import { NODE_RESOURCE_RELATIONSHIPS, RESOURCE_LAYER_SCHEMA_VERSION } from './types';
import type {
  AccessType,
  ExternalCandidate,
  NodeResourceLink,
  NodeResourceRelationship,
  ResourceRecord,
  ResourceType,
  ReviewStatus,
  SourceAuthority,
  ResourceAndLinksApplyResult,
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

interface NodeLinkGateOptions {
  proposedNodeIds?: string[];
  proposedRelation?: string;
  perNodeRationales?: Record<string, string>;
  existingNodeIds?: Set<string>;
  requestedLinkStatus?: ReviewStatus;
}

interface LinkLearnerEligibility {
  linkId: string;
  nodeId: string;
  reviewStatus: ReviewStatus;
  learnerEligible: boolean;
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

type NodeResourceLinkRecord = NodeResourceLink & Record<string, any>;

interface NodeResourceLinkPayload {
  schemaVersion: string;
  generatedAt?: string;
  nodeResourceLinks: NodeResourceLinkRecord[];
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

function reviewerAdmissionActor(reviewer: string | undefined): 'codex' | 'kimi' | 'human' | 'script' {
  const normalized = String(reviewer || '').toLowerCase();
  if (normalized.includes('kimi')) return 'kimi';
  if (normalized.includes('script')) return 'script';
  if (normalized === 'human' || normalized === 'project_owner_human_reviewer') return 'human';
  return 'codex';
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

function validateNodeLink(
  candidate: ExternalCandidate,
  applyMode: string,
  options: NodeLinkGateOptions = {},
): GateResult {
  if (applyMode === 'resource_only') {
    return { passed: true, skipped: true };
  }
  if (applyMode !== 'resource_and_links') {
    return { passed: false, gate: 'F0', message: `Unsupported applyMode: ${applyMode}` };
  }

  const proposedNodeIds = normalizeProposedNodeIds(options.proposedNodeIds);
  if (proposedNodeIds.length === 0) {
    return { passed: false, gate: 'F1', message: 'resource_and_links requires proposedNodeIds' };
  }
  if (proposedNodeIds.length !== new Set(proposedNodeIds).size) {
    return { passed: false, gate: 'F1', message: 'resource_and_links proposedNodeIds must be unique' };
  }
  if (options.existingNodeIds) {
    const missingNode = proposedNodeIds.find((nodeId) => !options.existingNodeIds?.has(nodeId));
    if (missingNode) {
      return { passed: false, gate: 'F2', message: `Proposed node does not exist: ${missingNode}` };
    }
  }

  if (!options.proposedRelation || !NODE_RESOURCE_RELATIONSHIPS.includes(options.proposedRelation as NodeResourceRelationship)) {
    return { passed: false, gate: 'F3', message: 'resource_and_links requires a valid proposedRelation' };
  }

  const rationales = options.perNodeRationales || {};
  for (const nodeId of proposedNodeIds) {
    const rationale = String(rationales[nodeId] || '').trim();
    if (!rationale || rationale.length < 8 || FAKE_VALUE_SET.has(rationale.toLowerCase())) {
      return { passed: false, gate: 'F4', message: `Node-specific rationale required for ${nodeId}` };
    }
  }

  const requestedStatus = options.requestedLinkStatus;
  if (requestedStatus && !['needs_review', 'accepted', 'human_reviewed'].includes(requestedStatus)) {
    return { passed: false, gate: 'F5', message: `Unsupported requestedLinkStatus: ${requestedStatus}` };
  }

  if (!candidate) {
    return { passed: false, gate: 'F6', message: 'Candidate required for node-link validation' };
  }

  return { passed: true };
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
  input: ResourceOnlyApplyInput,
  nodeLinkOptions: NodeLinkGateOptions = {},
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

  // F
  r = validateNodeLink(candidate, input.applyMode, nodeLinkOptions);
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

function generateNodeResourceLinkId(): string {
  return `nrl_${randomUUID()}`;
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
      admittedBy: reviewerAdmissionActor(input.reviewer),
      admittedAt: now,
      evidenceRef: `external-candidate:${candidateIdOf(candidate)}`,
      custodyChain: [
        'external_candidate_review',
        input.applyMode === 'resource_and_links' ? 'resource_and_links_promotion_apply' : 'resource_only_promotion_apply',
      ],
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

function normalizeProposedNodeIds(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value
    .map((item) => String(item || '').trim())
    .filter((item) => item.length > 0);
}

function normalizeRequestedLinkStatus(value: unknown): ReviewStatus {
  if (value === 'accepted' || value === 'human_reviewed') return value;
  return 'needs_review';
}

function buildNodeLinkGateOptions(
  input: Partial<ResourceOnlyApplyInput>,
  existingNodeIds?: Set<string>,
): NodeLinkGateOptions {
  return {
    proposedNodeIds: normalizeProposedNodeIds(input.proposedNodeIds),
    proposedRelation: typeof input.proposedRelation === 'string' ? input.proposedRelation : undefined,
    perNodeRationales: input.perNodeRationales && typeof input.perNodeRationales === 'object'
      ? input.perNodeRationales as Record<string, string>
      : undefined,
    existingNodeIds,
    requestedLinkStatus: typeof input.requestedLinkStatus === 'string'
      ? input.requestedLinkStatus as ReviewStatus
      : undefined,
  };
}

function buildPromotedNodeResourceLinks(
  candidate: ExternalCandidate,
  resource: ResourceRecord,
  input: ResourceOnlyApplyInput,
  promotionDecisionId: string,
  transactionManifestId: string,
): NodeResourceLinkRecord[] {
  const now = nowIso();
  const nodeIds = normalizeProposedNodeIds(input.proposedNodeIds);
  const relation = input.proposedRelation as NodeResourceRelationship;
  const rationales = input.perNodeRationales || {};
  const reviewStatus = normalizeRequestedLinkStatus(input.requestedLinkStatus);

  return nodeIds.map((nodeId) => ({
    id: generateNodeResourceLinkId(),
    nodeId,
    resourceId: resourceIdOf(resource),
    relationship: relation,
    relevanceScore: 0.5,
    authorityScore: 0.5,
    confidenceScore: 0.5,
    rationale: String(rationales[nodeId] || '').trim(),
    reviewStatus,
    reviewNotes: [
      'Created from reviewer-authorized external candidate resource_and_links promotion.',
      'No external verification performed.',
      'Learner exposure remains disabled unless accepted-link eligibility passes.',
      input.promotionCaveat,
    ].filter(Boolean).join(' '),
    verifiedBy: reviewerAdmissionActor(input.reviewer),
    createdFromExternalCandidateId: candidateIdOf(candidate),
    promotionDecisionId,
    transactionManifestId,
    learnerEligible: false,
    learnerExposure: false,
    createdAt: now,
    updatedAt: now,
  }));
}

function validateLinkLearnerEligibility(
  resource: ResourceRecord,
  links: NodeResourceLinkRecord[],
  requestedStatus: ReviewStatus,
): GateResult {
  if (requestedStatus !== 'accepted' && requestedStatus !== 'human_reviewed') {
    return { passed: true, skipped: true };
  }
  const blockedLink = links.find((link) => !isLearnerSidebarEligible(link, resource));
  if (blockedLink) {
    return {
      passed: false,
      gate: 'F7',
      message: `Accepted learner-visible link eligibility failed for ${blockedLink.nodeId}`,
    };
  }
  return { passed: true };
}

function linkEligibilitySummary(
  resource: ResourceRecord,
  links: NodeResourceLinkRecord[],
): LinkLearnerEligibility[] {
  return links.map((link) => ({
    linkId: link.id,
    nodeId: link.nodeId,
    reviewStatus: link.reviewStatus,
    learnerEligible: isLearnerSidebarEligible(link, resource),
  }));
}

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

async function buildResourceAndLinksApplyPreview(
  candidate: ExternalCandidate,
  existingResources: ResourceRecord[],
  input: Partial<ResourceOnlyApplyInput>,
  existingNodeIds?: Set<string>,
): Promise<{
  gateResults: GateRunnerResult;
  resourceDraft: ResourceRecord | null;
  nodeResourceLinkDrafts: NodeResourceLinkRecord[];
  linkEligibility: LinkLearnerEligibility[];
  caveats: Record<string, string | null>;
  canApply: boolean;
  previewHash: string;
}> {
  const fullInput: ResourceOnlyApplyInput = {
    candidateId: candidate.candidateId || candidate.id || '',
    applyMode: 'resource_and_links',
    reviewer: input.reviewer || '',
    rationale: input.rationale || '',
    sourceOfContext: input.sourceOfContext || '',
    previewHash: input.previewHash || 'preview_generation',
    acknowledgeWarnings: input.acknowledgeWarnings ?? true,
    promotionCaveat: input.promotionCaveat || '',
    proposedNodeIds: normalizeProposedNodeIds(input.proposedNodeIds),
    proposedRelation: input.proposedRelation,
    perNodeRationales: input.perNodeRationales,
    requestedLinkStatus: input.requestedLinkStatus,
  };

  const nodeLinkOptions = buildNodeLinkGateOptions(fullInput, existingNodeIds);
  const gateResults = await runAllGates(candidate, existingResources, fullInput, nodeLinkOptions);

  if (!gateResults.allPassed) {
    return {
      gateResults,
      resourceDraft: null,
      nodeResourceLinkDrafts: [],
      linkEligibility: [],
      caveats: {},
      canApply: false,
      previewHash: '',
    };
  }

  const promotionDecisionId = generatePromotionDecisionId();
  const transactionManifestId = generateTransactionManifestId();
  const resourceDraft = buildPromotedResource(candidate, fullInput, promotionDecisionId, transactionManifestId);
  const nodeResourceLinkDrafts = buildPromotedNodeResourceLinks(
    candidate,
    resourceDraft,
    fullInput,
    promotionDecisionId,
    transactionManifestId,
  );
  const requestedStatus = normalizeRequestedLinkStatus(fullInput.requestedLinkStatus);
  const learnerGate = validateLinkLearnerEligibility(resourceDraft, nodeResourceLinkDrafts, requestedStatus);
  if (!learnerGate.passed) {
    return {
      gateResults: {
        allPassed: false,
        blockingGates: [learnerGate.gate || 'F7'],
        results: [...gateResults.results, learnerGate],
      },
      resourceDraft: null,
      nodeResourceLinkDrafts: [],
      linkEligibility: [],
      caveats: {},
      canApply: false,
      previewHash: '',
    };
  }

  const linkEligibility = linkEligibilitySummary(resourceDraft, nodeResourceLinkDrafts);
  const previewHash = simpleHash(JSON.stringify({ resourceDraft, nodeResourceLinkDrafts }));

  return {
    gateResults,
    resourceDraft,
    nodeResourceLinkDrafts,
    linkEligibility,
    caveats: {
      sourceTruthCaveat: 'Not externally verified',
      standardsContextCaveat: resourceDraft.standardsContextCaveat || null,
      rightsCaveat: resourceDraft.rightsCaveat || null,
      verificationCaveat: 'No external verification performed',
    },
    canApply: true,
    previewHash,
  };
}

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
    createdResourceId: resourceIdOf(resource),
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
    createdResourceId: resourceIdOf(resource),
    createdNodeResourceLinkIds: [],
    learnerVisible: false,
    externalVerificationPerformed: false,
    graphMutationApplied: false,
    canonicalMutationApplied: false,
    nodeLinksCreated: 0,
    transactionManifestId: transaction.manifest.transactionId,
    rollbackPlan: {
      resourcesToRemove: [resourceIdOf(resource)],
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

async function applyResourceAndLinksPromotion(
  repoRoot: string,
  candidateId: string,
  input: ResourceOnlyApplyInput,
  existingNodeIds?: Set<string>,
): Promise<ResourceAndLinksApplyResult | ResourceOnlyApplyFailure> {
  if (input.applyMode !== 'resource_and_links') {
    return {
      success: false,
      gate: 'F0',
      message: 'applyResourceAndLinksPromotion requires applyMode=resource_and_links',
      severity: 'stop',
      blockingGates: ['F0'],
    };
  }

  const candidateRegistry = loadExternalCandidateRegistry(repoRoot);
  const candidate = candidateRegistry.candidates.find((c: any) => candidateIdOf(c) === candidateId);
  if (!candidate) {
    return {
      success: false,
      gate: 'A1',
      message: 'Candidate not found',
      severity: 'stop',
      blockingGates: ['A1'],
    };
  }

  const existingResources: ResourceRecord[] = loadResources(repoRoot);
  const nodeLinkOptions = buildNodeLinkGateOptions(input, existingNodeIds);
  const gateResults = await runAllGates(candidate, existingResources, input, nodeLinkOptions);
  if (!gateResults.allPassed) {
    return {
      success: false,
      gate: gateResults.blockingGates[0] || 'GATE',
      message: gateResults.results.find(r => !r.passed)?.message || 'Gate check failed',
      severity: 'stop',
      blockingGates: gateResults.blockingGates,
    };
  }

  const promotionDecisionId = generatePromotionDecisionId();
  const transactionManifestId = generateTransactionManifestId();
  const resource = buildPromotedResource(candidate, input, promotionDecisionId, transactionManifestId);
  const links = buildPromotedNodeResourceLinks(candidate, resource, input, promotionDecisionId, transactionManifestId);
  const requestedStatus = normalizeRequestedLinkStatus(input.requestedLinkStatus);
  const learnerGate = validateLinkLearnerEligibility(resource, links, requestedStatus);
  if (!learnerGate.passed) {
    return {
      success: false,
      gate: learnerGate.gate || 'F7',
      message: learnerGate.message || 'Accepted learner-visible link eligibility failed',
      severity: 'stop',
      blockingGates: [learnerGate.gate || 'F7'],
    };
  }

  const linkEligibility = linkEligibilitySummary(resource, links);
  for (const link of links) {
    const eligibility = linkEligibility.find((item) => item.linkId === link.id);
    link.learnerEligible = eligibility?.learnerEligible === true;
    link.learnerExposure = false;
  }

  const promotionDecision = {
    decisionId: promotionDecisionId,
    type: 'promotion_apply',
    applyMode: 'resource_and_links',
    createdResourceId: resourceIdOf(resource),
    createdNodeResourceLinkIds: links.map((link) => link.id),
    reviewer: input.reviewer,
    rationale: input.rationale,
    sourceOfContext: input.sourceOfContext,
    caveat: input.promotionCaveat,
    proposedNodeIds: normalizeProposedNodeIds(input.proposedNodeIds),
    proposedRelation: input.proposedRelation,
    perNodeRationales: input.perNodeRationales || {},
    timestamp: new Date().toISOString(),
    learnerExposure: false,
    externalVerification: false,
    graphMutation: false,
    canonicalMutation: false,
  };

  const paths = resourceLayerFilePaths(repoRoot);
  const transaction = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_resource_and_links_promotion_apply',
    [paths.resources, paths.links, resourceLayerExternalCandidateRegistryPath(repoRoot)],
    () => {
      const resourcesPayload = loadResourceRegistry(repoRoot);
      resourcesPayload.resources.push(resource);
      saveResourceRegistry(repoRoot, resourcesPayload);

      const linksPayload = loadNodeResourceLinkRegistry(repoRoot);
      linksPayload.nodeResourceLinks.push(...links);
      saveNodeResourceLinkRegistry(repoRoot, linksPayload);

      candidate.decisions = candidate.decisions || [];
      candidate.decisions.push(promotionDecision);
      saveExternalCandidateRegistry(repoRoot, candidateRegistry);

      return { resource, links };
    },
  );

  return {
    success: true,
    candidateId,
    applyMode: 'resource_and_links',
    createdResourceId: resourceIdOf(resource),
    createdNodeResourceLinkIds: links.map((link) => link.id),
    learnerVisible: false,
    externalVerificationPerformed: false,
    graphMutationApplied: false,
    canonicalMutationApplied: false,
    nodeLinksCreated: links.length,
    transactionManifestId: transaction.manifest.transactionId,
    rollbackPlan: {
      resourcesToRemove: [resourceIdOf(resource)],
      linksToRemove: links.map((link) => link.id),
      rollbackType: 'remove_created_links_then_resource_or_mark_rolled_back',
    },
    linkEligibility,
    sourceTruthCaveat: resource.sourceTruthCaveat || '',
    standardsContextCaveat: resource.standardsContextCaveat,
    rightsCaveat: resource.rightsCaveat,
    verificationCaveat: 'No external verification performed; URL/DOI/ISBN not verified for reachability or existence',
  };
}

async function buildRollbackPreview(
  repoRoot: string,
  resourceId: string,
): Promise<RollbackPreviewResult | { success: false; message: string }> {
  const resources: ResourceRecord[] = loadResources(repoRoot);
  const resource = resources.find(r => resourceIdOf(r) === resourceId);

  if (!resource) {
    return { success: false, message: `Resource ${resourceId} not found` };
  }

  const dependentLinks = loadNodeResourceLinks(repoRoot).filter((link) => link.resourceId === resourceId);
  const hasDependentLinks = dependentLinks.length > 0;
  const promotionDecisionId = resource.promotionDecisionId;
  const allDependentLinksOwnedByPromotion = dependentLinks.every((link) => (
    link.promotionDecisionId && link.promotionDecisionId === promotionDecisionId
  ));
  const rollbackType = !hasDependentLinks || allDependentLinksOwnedByPromotion ? 'hard_delete' : 'mark_rolled_back';

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

  const resource = resourcesPayload.resources[resourceIndex]!;
  const dependentLinks = loadNodeResourceLinks(repoRoot).filter((link) => link.resourceId === resourceId);
  const ownedDependentLinks = dependentLinks.filter((link) => (
    link.promotionDecisionId && link.promotionDecisionId === resource.promotionDecisionId
  ));
  if (dependentLinks.length > ownedDependentLinks.length && input.rollbackAction === 'hard_delete') {
    return { success: false, message: `Resource ${resourceId} has dependent nodeResourceLinks not owned by this promotion; hard_delete is blocked` };
  }

  const paths = resourceLayerFilePaths(repoRoot);
  const transaction = withResourceLayerTransaction(
    repoRoot,
    'external_candidate_promotion_rollback',
    [paths.resources, paths.links],
    () => {
      const payload = loadResourceRegistry(repoRoot);
      const idx = payload.resources.findIndex((item) => resourceIdOf(item) === resourceId);
      if (idx === -1) throw new Error(`Resource ${resourceId} not found`);
      const rollbackResource = payload.resources[idx]!;
      const linksPayload = loadNodeResourceLinkRegistry(repoRoot);
      const linksToRemove = ownedDependentLinks
        .map((link) => link.id)
        .filter((id): id is string => typeof id === 'string' && id.length > 0);
      if (input.rollbackAction === 'hard_delete') {
        if (linksToRemove.length > 0) {
          linksPayload.nodeResourceLinks = linksPayload.nodeResourceLinks.filter((link) => !linksToRemove.includes(link.id));
          saveNodeResourceLinkRegistry(repoRoot, linksPayload);
        }
        payload.resources.splice(idx, 1);
      } else {
        for (const link of linksPayload.nodeResourceLinks) {
          if (link.resourceId === resourceId && link.promotionDecisionId === rollbackResource.promotionDecisionId) {
            link.reviewStatus = 'rejected';
            link.reviewNotes = `${link.reviewNotes || ''} Rolled back by ${input.reviewer}: ${input.rationale}`.trim();
            link.updatedAt = nowIso();
          }
        }
        saveNodeResourceLinkRegistry(repoRoot, linksPayload);
        rollbackResource.rollbackInfo = {
          rolledBackAt: nowIso(),
          rolledBackBy: input.reviewer,
          rationale: input.rationale,
          rollbackManifestId: 'pending',
        };
        rollbackResource.updatedAt = nowIso();
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
    linksAffected: ownedDependentLinks
      .map((link) => link.id)
      .filter((id): id is string => typeof id === 'string' && id.length > 0),
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

function loadNodeResourceLinkRegistry(repoRoot: string): NodeResourceLinkPayload {
  const linksPath = resourceLayerFilePaths(repoRoot).links;
  if (!fs.existsSync(linksPath)) {
    return {
      schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
      generatedAt: nowIso(),
      nodeResourceLinks: [],
    };
  }
  const parsed = JSON.parse(fs.readFileSync(linksPath, 'utf-8').replace(/^\uFEFF/, '')) as NodeResourceLinkPayload | Array<{ id?: string; resourceId?: string }>;
  if (Array.isArray(parsed)) {
    return {
      schemaVersion: RESOURCE_LAYER_SCHEMA_VERSION,
      generatedAt: nowIso(),
      nodeResourceLinks: parsed as NodeResourceLinkRecord[],
    };
  }
  if (!parsed || typeof parsed !== 'object' || !Array.isArray(parsed.nodeResourceLinks)) {
    throw new Error(`${linksPath} must contain an object with a nodeResourceLinks array`);
  }
  return {
    schemaVersion: String(parsed.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION),
    generatedAt: String(parsed.generatedAt || nowIso()),
    nodeResourceLinks: parsed.nodeResourceLinks as NodeResourceLinkRecord[],
  };
}

function saveNodeResourceLinkRegistry(repoRoot: string, payload: NodeResourceLinkPayload): void {
  const linksPath = resourceLayerFilePaths(repoRoot).links;
  fs.mkdirSync(path.dirname(linksPath), { recursive: true });
  const next = {
    ...payload,
    schemaVersion: payload.schemaVersion || RESOURCE_LAYER_SCHEMA_VERSION,
    generatedAt: nowIso(),
  };
  const temp = `${linksPath}.tmp`;
  fs.writeFileSync(temp, `${JSON.stringify(next, null, 2)}\n`, 'utf-8');
  if (fs.existsSync(linksPath)) fs.rmSync(linksPath, { force: true });
  fs.renameSync(temp, linksPath);
}

function loadNodeResourceLinks(repoRoot: string): NodeResourceLinkRecord[] {
  return loadNodeResourceLinkRegistry(repoRoot).nodeResourceLinks;
}

// ─── Exports ──────────────────────────────────────────────────────────────

export {
  runAllGates,
  buildResourceOnlyApplyPreview,
  buildResourceAndLinksApplyPreview,
  applyResourceOnlyPromotion,
  applyResourceAndLinksPromotion,
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
  generateNodeResourceLinkId,
  generateTransactionManifestId,
  generatePromotionDecisionId,
};

export type { GateResult, GateRunnerResult, ResourceOnlyApplyInput, ResourceOnlyApplyResult, ResourceOnlyApplyFailure, ResourceAndLinksApplyResult };
