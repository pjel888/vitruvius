import { canonicalizeUrl, normalizeDoi, normalizeIsbn } from './normalization';

export type ExternalCandidateResourceType =
  | 'external_url_candidate'
  | 'book_candidate'
  | 'pdf_candidate'
  | 'standard_candidate'
  | 'guide_candidate'
  | 'article_candidate'
  | 'dataset_candidate'
  | 'source_family_reference';

export interface ExternalMetadataCandidateInput {
  candidateId?: string;
  title: string;
  resourceType: ExternalCandidateResourceType;
  sourceType?: string;
  proposedUrl?: string;
  proposedDoi?: string;
  proposedIsbn?: string;
  proposedPublisher?: string;
  proposedAuthors?: string[];
  proposedPublicationDate?: string;
  proposedEdition?: string;
  proposedVersion?: string;
  proposedScope?: string;
  proposedJurisdiction?: string;
  proposedSourceFamilyId?: string;
  proposedRightsStatus?: string;
  proposedNodeIds?: string[];
  proposedRelation?: string;
  candidateRationale?: string;
  submittedBy?: string;
}

export interface ExternalMetadataCandidatePreview {
  candidateId: string;
  title: string;
  resourceType: ExternalCandidateResourceType;
  sourceType?: string;
  proposedUrl?: string;
  proposedDoi?: string;
  proposedIsbn?: string;
  proposedPublisher?: string;
  proposedAuthors?: string[];
  proposedPublicationDate?: string;
  proposedEdition?: string;
  proposedVersion?: string;
  proposedScope?: string;
  proposedJurisdiction?: string;
  proposedSourceFamilyId?: string;
  proposedRightsStatus?: string;
  proposedNodeIds?: string[];
  proposedRelation?: string;
  candidateRationale?: string;
  submittedBy?: string;
  submittedAt: string;
  verificationStatus: 'unverified';
  displayPolicy: 'reviewer_only' | 'dev_only';
  learnerVisible: false;
  reviewRequired: true;
  warningFlags: string[];
  missingFields: string[];
  fakePlaceholderFlags: string[];
  sourceTruthCaveat: string;
  normalizedUrl?: string;
  normalizedDoi?: string;
  normalizedIsbn?: string;
}

const PLACEHOLDER_DOMAINS = new Set([
  'example.com',
  'localhost',
  'test',
  'tbd',
  'placeholder',
  'current',
  'latest',
  'unknown',
]);

const PLACEHOLDER_DOI_PATTERNS = /placeholder|example|test|dummy|mock|tbd|unknown/i;
const PLACEHOLDER_ISBN_PATTERNS = /^(0{10,13}|1{10,13}|1234567890|9876543210)$/;
const PLACEHOLDER_EDITION_PATTERNS = /^(tbd|to be determined|unknown|generic|latest|current|placeholder|sample|example|varies|n\/a)$/i;

function isPlaceholderDomain(url: string): boolean {
  try {
    const u = new URL(url);
    const hostname = u.hostname.toLowerCase().replace(/^www\./, '');
    if (PLACEHOLDER_DOMAINS.has(hostname)) return true;
    const parts = hostname.split('.');
    if (parts.some((p) => PLACEHOLDER_DOMAINS.has(p))) return true;
  } catch {
    return true;
  }
  return false;
}

function isPlaceholderDoi(doi: string): boolean {
  return PLACEHOLDER_DOI_PATTERNS.test(doi);
}

function isPlaceholderIsbn(isbn: string): boolean {
  const digits = isbn.replace(/[^0-9]/g, '');
  return PLACEHOLDER_ISBN_PATTERNS.test(digits);
}

function isPlaceholderEdition(value: string): boolean {
  return PLACEHOLDER_EDITION_PATTERNS.test(value.trim());
}

export function validateExternalMetadataCandidate(input: ExternalMetadataCandidateInput): {
  ok: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  if (!input.title?.trim()) errors.push('title is required');
  if (!input.resourceType) errors.push('resourceType is required');

  // URL validation
  if (input.proposedUrl) {
    const normalized = canonicalizeUrl(input.proposedUrl);
    if (!normalized) {
      errors.push('proposedUrl is not a valid URL');
    } else if (isPlaceholderDomain(normalized)) {
      errors.push('proposedUrl uses a placeholder or test domain');
    } else if (!/^https?:\/\//i.test(normalized)) {
      errors.push('proposedUrl must use http or https scheme');
    } else {
      warnings.push('URL syntax accepted; reachability not verified');
    }
  }

  // DOI validation
  if (input.proposedDoi) {
    const normalized = normalizeDoi(input.proposedDoi);
    if (!normalized) {
      errors.push('proposedDoi is not valid DOI syntax');
    } else if (isPlaceholderDoi(normalized)) {
      errors.push('proposedDoi appears to be a placeholder value');
    } else {
      warnings.push('DOI syntax accepted; existence not verified');
    }
  }

  // ISBN validation
  if (input.proposedIsbn) {
    const normalized = normalizeIsbn(input.proposedIsbn);
    if (!normalized) {
      errors.push('proposedIsbn is not valid ISBN-10 or ISBN-13 syntax');
    } else if (isPlaceholderIsbn(normalized)) {
      errors.push('proposedIsbn appears to be a placeholder value');
    } else {
      warnings.push('ISBN syntax accepted; existence not verified');
    }
  }

  // Standard-specific checks
  if (input.resourceType === 'standard_candidate' || input.resourceType === 'guide_candidate') {
    if (!input.proposedEdition && !input.proposedVersion) {
      warnings.push('Standard candidate missing edition/version');
    }
    if (!input.proposedJurisdiction && !input.proposedScope) {
      warnings.push('Standard candidate missing jurisdiction or scope');
    }
    if (input.proposedEdition && isPlaceholderEdition(input.proposedEdition)) {
      errors.push('proposedEdition is a placeholder value');
    }
    if (input.proposedVersion && isPlaceholderEdition(input.proposedVersion)) {
      errors.push('proposedVersion is a placeholder value');
    }
  }

  // Book/PDF checks
  if (input.resourceType === 'book_candidate' || input.resourceType === 'pdf_candidate') {
    if (!input.proposedAuthors?.length && !input.proposedPublisher) {
      warnings.push('Book/PDF candidate missing author and publisher');
    }
  }

  // Rights status
  if (input.proposedRightsStatus === 'accepted' || input.proposedRightsStatus === 'verified') {
    errors.push('Rights status cannot be pre-accepted or pre-verified for a candidate');
  }

  return { ok: errors.length === 0, errors, warnings };
}

export function classifyExternalCandidate(input: ExternalMetadataCandidateInput): {
  classification: 'url_heavy' | 'identifier_heavy' | 'metadata_heavy' | 'minimal';
  completenessScore: number;
} {
  let score = 0;
  if (input.proposedUrl) score += 1;
  if (input.proposedDoi) score += 2;
  if (input.proposedIsbn) score += 2;
  if (input.proposedPublisher) score += 1;
  if (input.proposedAuthors?.length) score += 1;
  if (input.proposedPublicationDate) score += 1;
  if (input.proposedEdition || input.proposedVersion) score += 1;
  if (input.proposedJurisdiction || input.proposedScope) score += 1;
  if (input.candidateRationale?.trim()) score += 1;

  if (input.proposedUrl && !input.proposedDoi && !input.proposedIsbn) return { classification: 'url_heavy', completenessScore: score };
  if ((input.proposedDoi || input.proposedIsbn) && !input.proposedUrl) return { classification: 'identifier_heavy', completenessScore: score };
  if (score >= 4) return { classification: 'metadata_heavy', completenessScore: score };
  return { classification: 'minimal', completenessScore: score };
}

export function detectExternalMetadataPlaceholders(input: ExternalMetadataCandidateInput): string[] {
  const flags: string[] = [];
  if (input.proposedUrl) {
    const normalized = canonicalizeUrl(input.proposedUrl);
    if (!normalized || isPlaceholderDomain(normalized)) flags.push('placeholder_url');
  }
  if (input.proposedDoi) {
    const normalized = normalizeDoi(input.proposedDoi);
    if (!normalized || isPlaceholderDoi(normalized)) flags.push('placeholder_doi');
  }
  if (input.proposedIsbn) {
    const normalized = normalizeIsbn(input.proposedIsbn);
    if (!normalized || isPlaceholderIsbn(normalized)) flags.push('placeholder_isbn');
  }
  if (input.proposedEdition && isPlaceholderEdition(input.proposedEdition)) flags.push('placeholder_edition');
  if (input.proposedVersion && isPlaceholderEdition(input.proposedVersion)) flags.push('placeholder_version');
  if (input.proposedPublisher && PLACEHOLDER_EDITION_PATTERNS.test(input.proposedPublisher.trim())) flags.push('placeholder_publisher');
  if (input.proposedAuthors?.some((a) => PLACEHOLDER_EDITION_PATTERNS.test(a.trim()))) flags.push('placeholder_author');
  return flags;
}

export function normalizeExternalCandidateInput(input: ExternalMetadataCandidateInput): ExternalMetadataCandidateInput {
  return {
    ...input,
    title: input.title?.trim() || '',
    proposedUrl: canonicalizeUrl(input.proposedUrl) || undefined,
    proposedDoi: normalizeDoi(input.proposedDoi) || undefined,
    proposedIsbn: normalizeIsbn(input.proposedIsbn) || undefined,
    proposedAuthors: input.proposedAuthors?.map((a) => a.trim()).filter(Boolean),
    proposedPublisher: input.proposedPublisher?.trim() || undefined,
    proposedEdition: input.proposedEdition?.trim() || undefined,
    proposedVersion: input.proposedVersion?.trim() || undefined,
    proposedScope: input.proposedScope?.trim() || undefined,
    proposedJurisdiction: input.proposedJurisdiction?.trim() || undefined,
    candidateRationale: input.candidateRationale?.trim() || undefined,
    submittedBy: input.submittedBy?.trim() || undefined,
  };
}

export function buildExternalCandidatePreview(input: ExternalMetadataCandidateInput): ExternalMetadataCandidatePreview {
  const normalized = normalizeExternalCandidateInput(input);
  const validation = validateExternalMetadataCandidate(normalized);
  const classification = classifyExternalCandidate(normalized);
  const fakeFlags = detectExternalMetadataPlaceholders(normalized);

  const missingFields: string[] = [];
  if (!normalized.proposedUrl) missingFields.push('url');
  if (!normalized.proposedDoi) missingFields.push('doi');
  if (!normalized.proposedIsbn) missingFields.push('isbn');
  if (!normalized.proposedPublisher) missingFields.push('publisher');
  if (!normalized.proposedAuthors?.length) missingFields.push('authors');
  if (!normalized.proposedPublicationDate) missingFields.push('publicationDate');
  if (!normalized.proposedEdition && !normalized.proposedVersion) missingFields.push('edition/version');
  if (!normalized.proposedJurisdiction && !normalized.proposedScope) missingFields.push('jurisdiction/scope');
  if (!normalized.candidateRationale) missingFields.push('candidateRationale');

  const warningFlags: string[] = [...validation.warnings];
  if (classification.classification === 'minimal') warningFlags.push('minimal_metadata');
  if (normalized.resourceType === 'standard_candidate' || normalized.resourceType === 'guide_candidate') {
    warningFlags.push('standard_candidate_not_learner_trusted');
  }
  if (!normalized.proposedUrl && !normalized.proposedDoi && !normalized.proposedIsbn) {
    warningFlags.push('no_stable_identifier');
  }

  return {
    candidateId: normalized.candidateId || `ext-cand-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    title: normalized.title,
    resourceType: normalized.resourceType,
    sourceType: normalized.sourceType,
    proposedUrl: normalized.proposedUrl,
    proposedDoi: normalized.proposedDoi,
    proposedIsbn: normalized.proposedIsbn,
    proposedPublisher: normalized.proposedPublisher,
    proposedAuthors: normalized.proposedAuthors,
    proposedPublicationDate: normalized.proposedPublicationDate,
    proposedEdition: normalized.proposedEdition,
    proposedVersion: normalized.proposedVersion,
    proposedScope: normalized.proposedScope,
    proposedJurisdiction: normalized.proposedJurisdiction,
    proposedSourceFamilyId: normalized.proposedSourceFamilyId,
    proposedRightsStatus: normalized.proposedRightsStatus,
    proposedNodeIds: normalized.proposedNodeIds,
    proposedRelation: normalized.proposedRelation,
    candidateRationale: normalized.candidateRationale,
    submittedBy: normalized.submittedBy,
    submittedAt: new Date().toISOString(),
    verificationStatus: 'unverified',
    displayPolicy: 'reviewer_only',
    learnerVisible: false,
    reviewRequired: true,
    warningFlags: Array.from(new Set(warningFlags)),
    missingFields,
    fakePlaceholderFlags: fakeFlags,
    sourceTruthCaveat: 'This is unverified candidate metadata. No external verification has been performed. URL reachability, DOI/ISBN existence, and source truth are not confirmed.',
    normalizedUrl: normalized.proposedUrl,
    normalizedDoi: normalized.proposedDoi,
    normalizedIsbn: normalized.proposedIsbn,
  };
}
