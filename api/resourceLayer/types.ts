export const RESOURCE_LAYER_SCHEMA_VERSION = 'vitruvius-resource-layer/v1';

export const RESOURCE_TYPES = [
  'book', 'textbook', 'handbook', 'standard', 'code', 'professional_guidance',
  'government_guidance', 'academic_paper', 'technical_report', 'webpage', 'pdf',
  'local_pdf', 'local_book', 'manual', 'manufacturer_manual', 'dataset', 'video',
  'internal_document', 'classification_system', 'ontology_documentation',
] as const;

export const SOURCE_AUTHORITIES = [
  'official', 'professional_body', 'government', 'academic', 'recognized_publisher',
  'industry_body', 'manufacturer', 'internal', 'general_web', 'unknown',
] as const;

export const ACCESS_TYPES = [
  'open_access', 'public_web', 'preview_only', 'paywalled', 'local_only',
  'restricted', 'unknown',
] as const;

export const VERIFICATION_STATUSES = [
  'unverified', 'metadata_verified', 'link_verified', 'identifier_verified',
  'local_file_verified', 'content_verified', 'human_reviewed', 'rejected',
] as const;

export const NODE_RESOURCE_RELATIONSHIPS = [
  'defines', 'explains', 'governs', 'supports', 'provides_procedure',
  'provides_evidence', 'provides_example', 'provides_classification',
  'provides_design_guidance', 'provides_construction_guidance',
  'provides_analysis_method', 'provides_maintenance_guidance',
  'provides_operation_guidance', 'provides_historical_context',
  'is_primary_reference_for', 'is_supplementary_reference_for',
  'is_local_reference_for',
] as const;

export const REVIEW_STATUSES = [
  'candidate', 'accepted', 'rejected', 'needs_review', 'human_reviewed',
] as const;

export type ResourceType = typeof RESOURCE_TYPES[number];
export type SourceAuthority = typeof SOURCE_AUTHORITIES[number];
export type AccessType = typeof ACCESS_TYPES[number];
export type VerificationStatus = typeof VERIFICATION_STATUSES[number];
export type NodeResourceRelationship = typeof NODE_RESOURCE_RELATIONSHIPS[number];
export type ReviewStatus = typeof REVIEW_STATUSES[number];
export type GeographicScope = 'global' | 'international' | 'us' | 'uk' | 'eu' | 'singapore' | 'project_specific' | 'unknown';
export type LocalFileType = 'pdf' | 'epub' | 'html' | 'docx' | 'txt' | 'md';
export type StandardContextStatus = 'missing' | 'partial' | 'complete' | 'not_required' | 'rejected' | 'needs_human_review' | 'justified_missing';
export type StandardContextConfidence = 'low' | 'medium' | 'high';

export interface StandardIdentifier {
  organization?: string;
  standardNumber?: string;
  title?: string;
  edition?: string;
  version?: string;
  publicationYear?: number;
}

export interface StandardEditionContext {
  edition?: string;
  version?: string;
  publicationYear?: number;
  amendment?: string;
  errata?: string;
  accessedAt?: string;
  sourceUrl?: string;
  sourceNote?: string;
}

export interface StandardJurisdictionContext {
  jurisdiction?: string;
  geographicScope?: GeographicScope | string;
  adoptionStatus?: string;
  codeCycle?: string;
  applicabilityNote?: string;
}

export interface StandardReviewContext {
  contextStatus: StandardContextStatus;
  reviewedBy?: string;
  reviewedAt?: string;
  rationale?: string;
  sourceOfContext?: string;
  confidence?: StandardContextConfidence;
}

export interface StandardContext {
  standardIdentifier?: StandardIdentifier;
  editionContext?: StandardEditionContext;
  jurisdictionContext?: StandardJurisdictionContext;
  reviewContext?: StandardReviewContext;
}

export interface Resource {
  id: string;
  title: string;
  subtitle?: string;
  authors?: string[];
  organization?: string;
  publisher?: string;
  year?: number;
  edition?: string;
  resourceType: ResourceType;
  sourceAuthority: SourceAuthority;
  authorityTier?: 1 | 2 | 3 | 4 | 5;
  sourceFamilyIds?: string[];
  url?: string;
  canonicalUrl?: string;
  landingPageUrl?: string;
  pdfUrl?: string;
  doi?: string;
  isbn10?: string;
  isbn13?: string;
  issn?: string;
  openAlexId?: string;
  semanticScholarId?: string;
  crossrefId?: string;
  dataCiteId?: string;
  internetArchiveIdentifier?: string;
  localPath?: string;
  localFileHash?: string;
  localFileType?: LocalFileType;
  localFileSizeBytes?: number;
  disciplineTags: string[];
  taxonomyTags: string[];
  keywords?: string[];
  jurisdiction?: string;
  geographicScope?: GeographicScope;
  standardIdentifier?: StandardIdentifier;
  editionContext?: StandardEditionContext;
  jurisdictionContext?: StandardJurisdictionContext;
  reviewContext?: StandardReviewContext;
  accessType: AccessType;
  sourceRights?: {
    rightsClass?: string;
    license?: string;
    restrictions?: string[];
    attribution?: string;
    declaredUseBoundary?: string;
  };
  admissionProvenance?: {
    admittedBy?: 'codex' | 'kimi' | 'human' | 'script';
    admittedAt?: string;
    evidenceRef?: string;
    custodyChain?: string[];
    reviewSummary?: string;
  };
  licenseNotes?: string;
  copyrightNotes?: string;
  abstractOrSummary?: string;
  verificationStatus: VerificationStatus;
  lastCheckedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface NodeResourceLink {
  id: string;
  nodeId: string;
  resourceId: string;
  relationship: NodeResourceRelationship;
  relevanceScore: number;
  authorityScore: number;
  confidenceScore: number;
  rationale: string;
  pageRefs?: string[];
  chapterRefs?: string[];
  sectionRefs?: string[];
  fragmentRefs?: string[];
  matchedTerms?: string[];
  matchedAliases?: string[];
  matchedTaxonomyContext?: string[];
  evidenceClaimIds?: string[];
  supportsEdgeIds?: string[];
  verifiedBy?: 'codex' | 'kimi' | 'human' | 'script';
  reviewStatus: ReviewStatus;
  reviewNotes?: string;
  standardContext?: StandardContext;
  createdAt: string;
  updatedAt: string;
}

export interface SourceFamily {
  id: string;
  label: string;
  domains?: string[];
  organizations?: string[];
  authority: SourceAuthority;
  authorityTier: 1 | 2 | 3 | 4 | 5;
  disciplines: string[];
  typicalResourceTypes: ResourceType[];
  jurisdiction?: string;
  notes?: string;
  allowedForPrimaryRuleSource: boolean;
}

export interface ResourceCheck {
  id: string;
  resourceId: string;
  checkType: 'url_health' | 'canonical_url' | 'doi_resolution' | 'isbn_normalization' | 'metadata_crosscheck' | 'local_file_exists' | 'local_file_hash' | 'content_extractability' | 'copyright_risk' | 'jurisdiction_context' | 'deduplication';
  status: 'pass' | 'fail' | 'warning' | 'skipped';
  checkedAt: string;
  details?: string;
}

export interface ResourceCandidate {
  id: string;
  nodeId?: string;
  adapter: string;
  query: string;
  rawTitle?: string;
  rawUrl?: string;
  rawIdentifier?: string;
  rawMetadata?: unknown;
  preliminaryScore: number;
  dedupeKey?: string;
  reviewStatus: ReviewStatus;
  rejectionReason?: string;
  reviewNotes?: string;
  duplicateOfResourceId?: string;
  createdAt: string;
  updatedAt?: string;
  reviewedAt?: string;
}

export interface ResourceLayerData {
  schemaVersion: string;
  generatedAt?: string;
  resources: Resource[];
  nodeResourceLinks: NodeResourceLink[];
  sourceFamilies: SourceFamily[];
  resourceChecks: ResourceCheck[];
  resourceCandidates: ResourceCandidate[];
}

export interface NodeResourceSummary {
  linkId: string;
  resourceId: string;
  nodeId: string;
  title: string;
  subtitle?: string;
  authors?: string[];
  organization?: string;
  publisher?: string;
  year?: number;
  resourceType: ResourceType;
  sourceAuthority: SourceAuthority;
  sourceFamilyIds?: string[];
  authorityTier?: number;
  accessType: AccessType;
  verificationStatus: VerificationStatus;
  reviewStatus: ReviewStatus;
  relationship: NodeResourceRelationship;
  relevanceScore: number;
  authorityScore: number;
  confidenceScore: number;
  displayScore: number;
  rationale: string;
  pageRefs?: string[];
  chapterRefs?: string[];
  sectionRefs?: string[];
  jurisdiction?: string;
  geographicScope?: GeographicScope;
  url?: string;
  canonicalUrl?: string;
  doi?: string;
  isbn13?: string;
  localFileName?: string;
  localFileType?: LocalFileType;
  licenseNotes?: string;
  lastCheckedAt?: string;
  warning?: string;
}

export type ReviewDecisionTargetType = 'resource' | 'node_resource_link' | 'candidate' | 'local_file' | 'standard_context';

export interface ReviewDecision {
  decision_id: string;
  target_type: ReviewDecisionTargetType;
  target_id: string;
  previous_status?: string;
  new_status?: string;
  decision: string;
  reviewer: string;
  rationale: string;
  notes?: string;
  created_at: string;
  metadata?: Record<string, unknown>;
}

export interface ReviewDecisionLog {
  schemaVersion: string;
  generatedAt?: string;
  reviewDecisions: ReviewDecision[];
}

export interface LocalFileIndex {
  schemaVersion: string;
  generatedAt?: string;
  indexedResourceCount?: number;
  scannedDirectories?: string[];
  errors?: string[];
  resources: Resource[];
}

// Phase 6N resource-only promotion apply uses compatibility fields while it
// writes into the canonical Resource registry shape.
export type ExternalCandidate = Record<string, any>;

export type ResourceRecord = Resource & Record<string, any> & {
  resourceId?: string;
  sourceType?: string;
  rightsStatus?: string;
  custodyStatus?: string;
  displayPolicy?: 'reviewer_only' | 'dev_only';
  warningFlags?: string[];
  reviewer?: string;
  reviewedAt?: string;
  rationale?: string;
  sourceOfContext?: string;
  createdFromExternalCandidateId?: string;
  promotionDecisionId?: string;
  transactionManifestId?: string;
  sourceTruthCaveat?: string;
  standardsContextCaveat?: string | null;
  rightsCaveat?: string | null;
  protectedContentCaveat?: string | null;
  learnerVisibleDefault?: false;
  rollbackInfo?: Record<string, unknown> | null;
};

export interface ResourceOnlyApplyInput {
  candidateId: string;
  applyMode: 'resource_only' | 'resource_and_links';
  reviewer: string;
  rationale: string;
  sourceOfContext: string;
  previewHash: string;
  acknowledgeWarnings: boolean;
  promotionCaveat: string;
  proposedNodeIds?: string[];
  proposedRelation?: NodeResourceRelationship;
  perNodeRationales?: Record<string, string>;
  requestedLinkStatus?: ReviewStatus;
}

export interface ResourceOnlyApplyResult {
  success: true;
  candidateId: string;
  applyMode: 'resource_only';
  createdResourceId: string;
  createdNodeResourceLinkIds: string[];
  learnerVisible: false;
  externalVerificationPerformed: false;
  graphMutationApplied: false;
  canonicalMutationApplied: false;
  nodeLinksCreated: 0;
  transactionManifestId: string;
  rollbackPlan: Record<string, unknown>;
  sourceTruthCaveat: string;
  standardsContextCaveat?: string | null;
  rightsCaveat?: string | null;
  verificationCaveat: string;
}

export interface ResourceOnlyApplyFailure {
  success: false;
  gate?: string;
  message: string;
  severity?: 'stop';
  blockingGates?: string[];
}

export interface ResourceAndLinksApplyResult {
  success: true;
  candidateId: string;
  applyMode: 'resource_and_links';
  createdResourceId: string;
  createdNodeResourceLinkIds: string[];
  learnerVisible: false;
  externalVerificationPerformed: false;
  graphMutationApplied: false;
  canonicalMutationApplied: false;
  nodeLinksCreated: number;
  transactionManifestId: string;
  rollbackPlan: Record<string, unknown>;
  linkEligibility: Array<{
    linkId: string;
    nodeId: string;
    reviewStatus: ReviewStatus;
    learnerEligible: boolean;
  }>;
  sourceTruthCaveat: string;
  standardsContextCaveat?: string | null;
  rightsCaveat?: string | null;
  verificationCaveat: string;
}

export interface RollbackPreviewResult {
  candidateId?: string;
  promotionDecisionId?: string;
  resourceId: string;
  rollbackPlan: {
    action: 'hard_delete' | 'mark_rolled_back';
    notes: string;
  };
  preRollbackStateSummary: {
    resourcesBefore: number;
    linksBefore: number;
  };
  canRollback: boolean;
}

export interface RollbackApplyInput {
  promotionDecisionId?: string;
  reviewer: string;
  rationale: string;
  rollbackAction: 'hard_delete' | 'mark_rolled_back';
}

export interface RollbackApplyResult {
  success: true;
  rollbackTransactionManifestId: string;
  action: 'hard_delete' | 'mark_rolled_back';
  resourcesAffected: string[];
  linksAffected: string[];
  candidateHistoryUpdated: boolean;
}

export interface TransactionManifest {
  transactionManifestId: string;
  previousManifestHash: string | null;
  operationType: string;
  candidateId?: string;
  promotionDecisionId?: string;
  reviewer?: string;
  rationale?: string;
  sourceOfContext?: string;
  appliedAt: string;
  touchedFiles: Array<Record<string, unknown>>;
  createdResourceIds: string[];
  createdLinkIds: string[];
  rollbackPlan: Record<string, unknown> | null;
  noGraphCanonicalMutation: true;
  noExternalVerification: true;
  noLearnerExposure: true;
  learnerExposureStatus: 'none';
  rollbackInfo: Record<string, unknown> | null;
}
