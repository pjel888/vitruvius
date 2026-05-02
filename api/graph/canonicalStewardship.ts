import { createHash, createHmac, timingSafeEqual } from 'node:crypto';
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, readdirSync, renameSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import type { GraphEdgeLike, GraphNodeLike } from './relationshipVisibility';
import { normalizeCanonicalLabel, normalizeCanonicalLabelLoose } from './relationshipVisibility';
import type { NodeResourceLink, ResourceLayerData } from '../resourceLayer/types';
import { resourceLayerFilePaths } from '../resourceLayer/registry';
import { resourceLayerTransactionPaths } from '../resourceLayer/transactionManifest';

export const CANONICAL_STEWARDSHIP_SCHEMA_VERSION = 'vitruvius-graph-canonical-stewardship/v1';

export type CanonicalDecisionType =
  | 'MERGE_INTO_CANONICAL'
  | 'ALIAS_TO_CANONICAL'
  | 'KEEP_SEPARATE'
  | 'NEEDS_HUMAN_REVIEW'
  | 'REJECT_DUPLICATE_CANDIDATE'
  | 'SPLIT_OR_RETYPE_NEEDED'
  | 'GOVERNED_DISAMBIGUATION'
  | 'RELATED_SPECIALIZATION'
  | 'CROSS_DOMAIN_EQUIVALENCE'
  | 'CANONICAL_LABEL_CLARIFICATION'
  | 'DISAMBIGUATED_KEEP_SEPARATE'
  | 'AEC_RELATIONSHIP_ENRICHMENT';
export type CanonicalDecisionStatus =
  | 'proposed'
  | 'pending_steward_approval'
  | 'steward_approved'
  | 'admitted'
  | 'applied'
  | 'rejected'
  | 'needs_review'
  | 'deferred'
  | 'rolled_back'
  | 'rollback_partial'
  | 'rollback_blocked';
export type CanonicalRiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type CanonicalPriorityBand = 'P0' | 'P1' | 'P2' | 'P3' | 'BLOCKED';
export type CanonicalRollbackCapability = 'full' | 'partial' | 'blocked' | 'unsupported';
export type CanonicalApprovalStatus = 'pending_steward_approval' | 'steward_approved' | 'admitted' | 'rejected' | 'deferred' | 'rolled_back';
export type CanonicalApprovalSource =
  | 'dev_admin_ui'
  | 'api'
  | 'test_fixture'
  | 'imported_decision_record'
  | 'human_record'
  | 'user_supplied_standing_steward_approval';
export type CanonicalMutationScope = 'metadata_only' | 'non_destructive_edge_admission' | 'alias_only' | 'redirect' | 'tombstone' | 'destructive_merge';
export type CanonicalP1PacketSignatureStatus = 'unsigned' | 'valid' | 'invalid' | 'missing_key' | 'unsupported';
export type CanonicalP1PacketSignatureScope = 'p1_packet_snapshot' | 'packet_content' | 'group_input' | 'edge_neighborhood';
export type CanonicalP1OntologyReviewStatus = 'unreviewed' | 'kimi_review_requested' | 'kimi_reviewed' | 'human_review_needed' | 'human_reviewed' | 'rejected' | 'deferred';
export type CanonicalP1OntologyReviewerType = 'kimi' | 'human' | 'codex' | 'system';
export type CanonicalP1OntologyReviewSource = 'kimi' | 'manual_entry' | 'imported_review' | 'test_fixture';
export type CanonicalP1OntologyReviewRiskLevel = 'low' | 'medium' | 'high' | 'blocked';
export type CanonicalP1PacketAdmissionStatus = 'not_admitted' | 'consumed_by_non_destructive_admission' | 'metadata_disambiguation_admitted';
export type CanonicalP1PacketReviewCarryForwardScope = 'custody_snapshot_refresh_only' | 'admission_overlay_applied' | 'metadata_only_disambiguation_applied';
export type CanonicalStewardshipRelationType =
  | 'DISAMBIGUATED_FROM'
  | 'RELATED_SPECIALIZATION_OF'
  | 'HAS_DOMAIN_SPECIALIZATION'
  | 'CROSS_DOMAIN_EQUIVALENT'
  | 'CROSS_DOMAIN_ALIGNMENT'
  | 'CROSS_DOMAIN_CLOSE_MATCH'
  | 'CROSS_DOMAIN_RELATED_MATCH'
  | 'CLOSE_MATCH'
  | 'RELATED_MATCH'
  | 'CONSTRAINS'
  | 'REQUIRES';
export type DuplicateCandidateCategory =
  | 'safe_review_candidate'
  | 'likely_alias_candidate'
  | 'manual_review_candidate'
  | 'unsafe_auto_merge'
  | 'false_positive_likely'
  | 'subtype_not_duplicate'
  | 'homonym_collision';

export interface CanonicalStewardshipDecision {
  decisionId: string;
  decisionType: CanonicalDecisionType;
  candidateGroupId: string;
  canonicalNodeId?: string;
  sourceNodeIds: string[];
  affectedEdgeIds: string[];
  affectedResourceLinkIds: string[];
  affectedAliases: string[];
  affectedSearchTerms: string[];
  reviewer: string;
  reviewedBy?: string;
  createdAt: string;
  rationale: string;
  riskLevel: CanonicalRiskLevel;
  beforeSnapshot: unknown;
  afterPreview: unknown;
  appliedAt?: string;
  status: CanonicalDecisionStatus;
  rollbackCapability?: 'full' | 'partial' | 'blocked' | 'unsupported';
  validationResult?: unknown;
  kimiReviewSummary?: string;
  notes?: string;
  affectedNodeIds?: string[];
  proposedRelationshipAdds?: CanonicalStewardshipRelationshipProposal[];
  proposedRelationshipUpdates?: unknown[];
  proposedAliasAdds?: CanonicalAliasRecord[];
  proposedLabelChanges?: Array<{ nodeId: string; fromLabel?: string; toLabel?: string; displayOnly?: boolean; rationale?: string }>;
  proposedDescriptionChanges?: Array<{ nodeId: string; fromDescription?: string; toDescription?: string; rationale?: string }>;
  searchDisambiguationText?: string;
  transactionManifestId?: string;
}

export interface CanonicalAliasRecord {
  alias: string;
  normalizedAlias: string;
  canonicalNodeId: string;
  sourceNodeIds: string[];
  decisionId: string;
  createdAt: string;
  aliasType?: 'exact_alias' | 'spelling_variant' | 'case_variant' | 'abbreviation' | 'legacy_label' | 'search_alias' | 'disambiguation_alias';
  status?: 'proposed' | 'approved' | 'active' | 'rejected' | 'deprecated';
  rationale?: string;
  reviewer?: string;
  appliedAt?: string;
}

export interface CanonicalRedirectRecord {
  sourceNodeId: string;
  canonicalNodeId: string;
  decisionId: string;
  createdAt: string;
  reason: string;
  redirectType?: 'merged_into' | 'canonical_redirect' | 'deprecated_duplicate' | 'legacy_id';
  status?: 'proposed' | 'approved' | 'active' | 'rejected' | 'deprecated';
  appliedAt?: string;
  rollbackCapability?: CanonicalRollbackCapability;
}

export interface CanonicalTombstoneRecord {
  nodeId: string;
  tombstoneStatus: 'deprecated' | 'merged' | 'alias_only' | 'replaced';
  canonicalTargetId?: string;
  reason: string;
  decisionId: string;
  preservedMetadata?: unknown;
  preservedEdgePolicy?: string;
  preservedResourceLinkPolicy?: string;
  createdAt: string;
}

export interface CanonicalStewardshipRelationshipProposal {
  proposalId: string;
  sourceNodeId: string;
  targetNodeId: string;
  relationType: CanonicalStewardshipRelationType;
  category: 'semantic/stewardship-disambiguation' | 'semantic/aec-mechanism';
  direction: 'outgoing' | 'bidirectional';
  confidence: 'proposed' | 'reviewed';
  weight?: number;
  rationale: string;
  provenance?: string;
  stewardshipDecisionId?: string;
  createdAt: string;
  reviewStatus: 'proposed' | 'approved' | 'rejected' | 'applied';
}

export interface CanonicalStewardshipApproval {
  approvalId: string;
  decisionId: string;
  groupId: string;
  decisionHash: string;
  approvedBy: string;
  reviewerRole: string;
  approvalSource: CanonicalApprovalSource;
  approvedAt: string;
  approvalRationale: string;
  riskAcknowledgment: boolean;
  mutationScope: CanonicalMutationScope;
  rollbackPlan: string;
  validationSnapshot: unknown;
  kimiReviewSummary?: string;
  transactionManifestId?: string;
  status: CanonicalApprovalStatus;
  admittedBy?: string;
  admittedAt?: string;
  admissionTransactionId?: string;
  postAdmissionValidationSnapshot?: unknown;
  rejectedAt?: string;
  rejectionRationale?: string;
}

export interface CanonicalAdmittedRelationship extends GraphEdgeLike {
  admissionId: string;
  source: string;
  target: string;
  type: CanonicalStewardshipRelationType;
  relationType: string;
  relationCategory: string;
  direction: string;
  confidence: string;
  weight: number;
  rationale: string;
  provenanceNote: string;
  stewardshipDecisionId: string;
  approvalId: string;
  reviewStatus: 'admitted' | 'rolled_back';
  createdAt: string;
  createdBy: string;
  reversible: boolean;
  rollbackAt?: string;
}

function isCanonicalAdmittedOverlayEdge(edge: GraphEdgeLike) {
  const candidate = edge as GraphEdgeLike & Partial<CanonicalAdmittedRelationship>;
  return candidate.reviewStatus === 'admitted'
    && typeof candidate.approvalId === 'string'
    && typeof candidate.stewardshipDecisionId === 'string';
}

function canonicalBaseGraphEdges(edges: GraphEdgeLike[]) {
  return edges.filter((edge) => !isCanonicalAdmittedOverlayEdge(edge));
}

export interface CanonicalApprovalRequest {
  approvedBy?: string;
  reviewerRole?: string;
  approvalSource?: CanonicalApprovalSource;
  approvalRationale?: string;
  riskAcknowledgment?: boolean;
  mutationScope?: CanonicalMutationScope;
  rollbackPlan?: string;
  kimiReviewSummary?: string;
  apply?: boolean;
  dryRun?: boolean;
}

export interface CanonicalP1SourceSnapshot {
  schemaVersion: string;
  generatedFrom: 'in_memory_generation_context';
  hashAlgorithm: 'sha256-stable-json-v1';
  staleCheckPolicy: 'warn_on_current_context_mismatch';
  graphNodeCount: number;
  graphEdgeCount: number;
  duplicateGroupCount: number;
  p1CandidateGroupCount: number;
  resourceCount: number;
  nodeResourceLinkCount: number;
  stewardshipDecisionCount: number;
  approvalCount: number;
  admittedRelationshipCount: number;
  aliasCount: number;
  redirectCount: number;
  tombstoneCount: number;
  nodesHash: string;
  edgesHash: string;
  groupsHash: string;
  resourcesHash: string;
  decisionsHash: string;
  approvalsHash: string;
  admittedRelationshipsHash: string;
  aliasesHash: string;
  redirectsHash: string;
  tombstonesHash: string;
  priorityOverridesHash: string;
  snapshotHash: string;
}

export interface CanonicalP1PacketSignature {
  signatureStatus: CanonicalP1PacketSignatureStatus;
  signatureAlgorithm: 'hmac-sha256';
  signatureScope: CanonicalP1PacketSignatureScope;
  signature?: string;
  signedAt?: string;
  signedBy?: string;
  signerId?: string;
  systemSignerId?: string;
  keyId?: string;
  signaturePayloadHash: string;
  signatureVerificationCheckedAt?: string;
}

export interface CanonicalP1PacketReviewEvent {
  eventId: string;
  eventType: 'created' | 'updated' | 'carried_forward';
  ontologyReviewStatus: CanonicalP1OntologyReviewStatus;
  reviewedBy: string;
  reviewerType: CanonicalP1OntologyReviewerType;
  source: CanonicalP1OntologyReviewSource;
  createdAt: string;
  reviewSummary?: string;
  nextAction?: string;
}

export interface CanonicalP1PacketCustodyRebaseEvent {
  rebasedAt: string;
  rebasedBy: string;
  rebaseReason: string;
  fromPacketContentHash?: string;
  fromSourceSnapshotHash?: string;
  toPacketContentHash?: string;
  toSourceSnapshotHash?: string;
}

export interface CanonicalP1PacketOntologyReview {
  reviewId: string;
  packetId: string;
  groupId: string;
  packetContentHash?: string;
  sourceSnapshotHash?: string;
  ontologyReviewStatus: CanonicalP1OntologyReviewStatus;
  reviewerType: CanonicalP1OntologyReviewerType;
  reviewedBy: string;
  reviewedAt: string;
  reviewSummary: string;
  acceptedSuggestions: string[];
  rejectedSuggestions: string[];
  deferredSuggestions: string[];
  recommendedAction?: string;
  reviewRiskLevel: CanonicalP1OntologyReviewRiskLevel;
  nextAction?: string;
  notes?: string;
  source: CanonicalP1OntologyReviewSource;
  reviewCaveat: string;
  mutationScope: 'review_metadata_only';
  graphMutationApplied: false;
  advisoryOnly: true;
  carriedForwardFromPacketContentHash?: string;
  carriedForwardFromSourceSnapshotHash?: string;
  carriedForwardToPacketContentHash?: string;
  carriedForwardToSourceSnapshotHash?: string;
  carriedForwardAt?: string;
  carriedForwardReason?: string;
  carryForwardScope?: CanonicalP1PacketReviewCarryForwardScope;
  carryForwardCaveat?: string;
  createdAt: string;
  updatedAt: string;
  reviewHistory: CanonicalP1PacketReviewEvent[];
}

export interface CanonicalP1PacketReviewRequest {
  ontologyReviewStatus?: CanonicalP1OntologyReviewStatus;
  reviewerType?: CanonicalP1OntologyReviewerType;
  reviewedBy?: string;
  reviewSummary?: string;
  acceptedSuggestions?: string[] | string;
  rejectedSuggestions?: string[] | string;
  deferredSuggestions?: string[] | string;
  recommendedAction?: string;
  reviewRiskLevel?: CanonicalP1OntologyReviewRiskLevel;
  nextAction?: string;
  notes?: string;
  source?: CanonicalP1OntologyReviewSource;
  dryRun?: boolean;
  apply?: boolean;
}

export interface CanonicalP1DecisionPacket {
  schemaVersion?: string;
  packetId: string;
  packetContentHash?: string;
  packetRunId?: string;
  groupId: string;
  generatedAt: string;
  sourceQueryOrBatchId?: string;
  truthCaveat?: 'advisory_packet_only_not_steward_approval_not_canonical_admission';
  priorityBand: CanonicalPriorityBand;
  priorityScore?: number;
  priorityReasons?: string[];
  riskLevel: CanonicalRiskLevel;
  riskScore?: number;
  riskReasons?: string[];
  candidateCategory: DuplicateCandidateCategory;
  normalizedLabel: string;
  nodeIds: string[];
  nodes: DuplicateCandidateNodeSummary[];
  sourceSnapshot?: CanonicalP1SourceSnapshot;
  groupInputHash?: string;
  candidateEdgeNeighborhoodHash?: string;
  signature?: CanonicalP1PacketSignature;
  ontologyReviewStatus?: CanonicalP1OntologyReviewStatus;
  ontologyReview?: CanonicalP1PacketOntologyReview;
  reviewHistory?: CanonicalP1PacketReviewEvent[];
  edgeSummary: {
    totalEdges: number;
    incoming: Array<{ nodeId: string; count: number }>;
    outgoing: Array<{ nodeId: string; count: number }>;
    topRelationTypes: Record<string, number>;
  };
  resourceLinkCount: number;
  resourceLinkIds?: string[];
  existingDecisionStatus?: string;
  existingDecisionIds?: string[];
  recommendedDecisionType: CanonicalDecisionType;
  alternateSafeDecisionTypes?: CanonicalDecisionType[];
  possibleRelationAdditions: CanonicalStewardshipRelationType[];
  proposedRelationshipAdds?: CanonicalStewardshipRelationshipProposal[];
  wouldAffectNodeIds?: string[];
  wouldAffectEdgeIds?: string[];
  wouldAffectResourceLinkIds?: string[];
  selfLoopRisks?: string[];
  duplicateEdgeConsolidationRisks?: string[];
  rollbackCapabilityPreview?: CanonicalRollbackCapability;
  remediationNeeded?: boolean;
  needsKimiReview: boolean;
  needsHumanDomainReview: boolean;
  requiredReviewerRole?: string;
  stewardDecisionStatus?: 'pending' | 'approved' | 'admitted' | 'rejected';
  mergeSafety: 'not_recommended' | 'possible_low_risk_after_review' | 'blocked_without_domain_review';
  rationale: string;
  nextAction: string;
  kimiAdvisoryOnly?: boolean;
  mergeApplied?: boolean;
  aliasApplied?: boolean;
  redirectApplied?: boolean;
  tombstoneApplied?: boolean;
  productionGraphWritePerformed?: boolean;
  resourceLinkRewritePerformed?: boolean;
  admittedRelationshipWritten?: boolean;
  packetAdmissionStatus?: CanonicalP1PacketAdmissionStatus;
  approvalIds?: string[];
  admittedRelationshipIds?: string[];
  admittedDecisionIds?: string[];
  admissionAppliedAt?: string;
  admissionSummary?: string;
  custodyRebasedAt?: string;
  custodyRebasedBy?: string;
  custodyRebaseReason?: string;
  previousPacketContentHash?: string;
  previousSourceSnapshotHash?: string;
  custodyRebaseHistory?: CanonicalP1PacketCustodyRebaseEvent[];
}

export interface CanonicalRemediationManifest {
  remediationManifestId: string;
  decisionId: string;
  rollbackId?: string;
  rollbackCapability: CanonicalRollbackCapability;
  reason: string;
  affectedNodes: string[];
  affectedEdges: string[];
  affectedResourceLinks: string[];
  affectedAliases: string[];
  affectedRedirects: string[];
  affectedTombstones: string[];
  unresolvedRestorationTasks: string[];
  recommendedManualSteps: string[];
  validationWarnings: string[];
  createdAt: string;
  reviewer: string;
  status: 'open' | 'in_progress' | 'resolved' | 'waived';
  resolutionNotes?: string;
  resolvedAt?: string;
}

export interface DuplicateCandidateNodeSummary {
  id: string;
  label: string;
  displayLabel?: string;
  type?: string;
  aliases: string[];
  taxonomyPath: string[];
  incomingEdgeCount: number;
  outgoingEdgeCount: number;
  resourceLinkCount: number;
}

export interface DuplicateCandidateGroup {
  groupId: string;
  normalizedLabel: string;
  looseNormalizedLabel: string;
  labels: string[];
  nodes: DuplicateCandidateNodeSummary[];
  nodeIds: string[];
  candidateCategory: DuplicateCandidateCategory;
  riskLevel: CanonicalRiskLevel;
  riskScore: number;
  suggestedAction: CanonicalDecisionType;
  riskReasons: string[];
  priorityBand: CanonicalPriorityBand;
  priorityScore: number;
  priorityReasons: string[];
  edgeCount: number;
  resourceLinkCount: number;
  existingDecisions: CanonicalStewardshipDecision[];
  status: 'unresolved' | 'applied' | 'keep_separate' | 'rejected' | 'needs_review' | 'disambiguated';
}

export interface CanonicalDecisionRequest {
  decisionType: CanonicalDecisionType;
  canonicalNodeId?: string;
  sourceNodeIds?: string[];
  reviewer?: string;
  rationale?: string;
  notes?: string;
  dryRun?: boolean;
  apply?: boolean;
  highRiskAcknowledged?: boolean;
  kimiReviewSummary?: string;
  searchDisambiguationText?: string;
  proposedRelationshipAdds?: CanonicalStewardshipRelationshipProposal[];
}

export interface CanonicalRelationshipAdmissionRequest {
  candidateId?: string;
  reviewer?: string;
  rationale?: string;
  notes?: string;
  riskLevel?: CanonicalRiskLevel;
  kimiReviewSummary?: string;
  relationships?: Array<{
    proposalId?: string;
    sourceNodeId: string;
    targetNodeId: string;
    relationType: CanonicalStewardshipRelationType;
    category?: CanonicalStewardshipRelationshipProposal['category'];
    direction?: CanonicalStewardshipRelationshipProposal['direction'];
    confidence?: CanonicalStewardshipRelationshipProposal['confidence'];
    weight?: number;
    rationale?: string;
    provenance?: string;
  }>;
  dryRun?: boolean;
  apply?: boolean;
}

export interface CanonicalTransactionManifest {
  transactionId: string;
  operationType: string;
  subsystem?: string;
  actor?: string;
  startedAt: string;
  completedAt?: string;
  filesTouched: string[];
  beforeHashes: Record<string, string>;
  afterHashes?: Record<string, string>;
  previousManifestHash?: string | null;
  manifestHash?: string;
  signature?: string;
  dryRun?: boolean;
  decisionIds?: string[];
  rollbackCapability?: 'full' | 'partial' | 'blocked' | 'unsupported';
  warnings?: string[];
  errors?: string[];
  validationStatus: 'pending' | 'passed' | 'failed';
  error?: string;
}

export interface CanonicalManifestAfterHashStatus {
  subsystem: string;
  filePath: string;
  latestManifestId: string;
  latestManifestPath: string;
  operationType: string;
  latestManifestStartedAt: string;
  latestManifestCompletedAt?: string;
  custodyCritical: boolean;
  strictRequired: boolean;
  currentHash: string;
  latestAfterHash: string;
  matches: boolean;
  status: 'matched_latest_manifest' | 'drift_since_latest_manifest';
}

export interface CanonicalTransactionManifestValidation {
  count: number;
  invalidManifestCount: number;
  brokenHashChainCount: number;
  unsignedManifestWarnings: number;
  transactionManifestsWithAfterHash: number;
  filesUnderManifestCustody: number;
  latestAfterHashMatches: number;
  latestAfterHashMismatches: number;
  staleManifestFiles: number;
  unmanifestedMutatedCustodyFiles: number;
  manifestChainValid: boolean;
  manifestSignatureValid: boolean;
  latestManifestAfterHashStrictMode: boolean;
  manifestAfterHashStatuses: CanonicalManifestAfterHashStatus[];
  blockers: string[];
  warnings: string[];
}

export interface CanonicalPriorityOverride {
  groupId: string;
  priorityBand: CanonicalPriorityBand;
  owner?: string;
  notes?: string;
  tags: string[];
  updatedAt: string;
  updatedBy: string;
}

export interface CanonicalBatchRecord {
  batchId: string;
  name: string;
  filters: DuplicateFilters;
  groupIds: string[];
  status: 'open' | 'in_review' | 'complete' | 'cancelled';
  reviewer?: string;
  priorityBand?: CanonicalPriorityBand;
  tags: string[];
  notes?: string;
  createdAt: string;
  updatedAt: string;
  stats: {
    groupCount: number;
    riskCounts: Record<string, number>;
    priorityCounts: Record<string, number>;
    candidateCategoryCounts: Record<string, number>;
    destructiveActionsBlocked: boolean;
  };
  decisions: Array<{
    batchDecisionId: string;
    action: string;
    reviewer: string;
    rationale: string;
    notes?: string;
    createdAt: string;
    dryRun: boolean;
    applied: boolean;
    affectedGroupIds: string[];
    blockers: string[];
    warnings: string[];
  }>;
}

const CANONICAL_DIR = join('006_System-Manifests', 'graph-canonical');
const DECISION_TYPES = new Set<CanonicalDecisionType>([
  'MERGE_INTO_CANONICAL',
  'ALIAS_TO_CANONICAL',
  'KEEP_SEPARATE',
  'NEEDS_HUMAN_REVIEW',
  'REJECT_DUPLICATE_CANDIDATE',
  'SPLIT_OR_RETYPE_NEEDED',
  'GOVERNED_DISAMBIGUATION',
  'RELATED_SPECIALIZATION',
  'CROSS_DOMAIN_EQUIVALENCE',
  'CANONICAL_LABEL_CLARIFICATION',
  'DISAMBIGUATED_KEEP_SEPARATE',
  'AEC_RELATIONSHIP_ENRICHMENT',
]);

const DISAMBIGUATION_DECISION_TYPES = new Set<CanonicalDecisionType>([
  'GOVERNED_DISAMBIGUATION',
  'RELATED_SPECIALIZATION',
  'CROSS_DOMAIN_EQUIVALENCE',
  'CANONICAL_LABEL_CLARIFICATION',
  'DISAMBIGUATED_KEEP_SEPARATE',
]);

const STEWARDSHIP_RELATIONSHIP_TYPES = new Set<CanonicalStewardshipRelationshipProposal['relationType']>([
  'DISAMBIGUATED_FROM',
  'RELATED_SPECIALIZATION_OF',
  'HAS_DOMAIN_SPECIALIZATION',
  'CROSS_DOMAIN_EQUIVALENT',
  'CROSS_DOMAIN_ALIGNMENT',
  'CROSS_DOMAIN_CLOSE_MATCH',
  'CROSS_DOMAIN_RELATED_MATCH',
  'CLOSE_MATCH',
  'RELATED_MATCH',
  'CONSTRAINS',
  'REQUIRES',
]);

const ADMITTED_RELATIONSHIP_TYPES = new Set<CanonicalStewardshipRelationType>([
  'DISAMBIGUATED_FROM',
  'RELATED_SPECIALIZATION_OF',
  'HAS_DOMAIN_SPECIALIZATION',
  'CROSS_DOMAIN_ALIGNMENT',
  'CROSS_DOMAIN_CLOSE_MATCH',
  'CROSS_DOMAIN_RELATED_MATCH',
  'CLOSE_MATCH',
  'RELATED_MATCH',
  'CONSTRAINS',
  'REQUIRES',
]);

function nowIso() {
  return new Date().toISOString();
}

function hash(value: string | Buffer) {
  return createHash('sha256').update(value).digest('hex');
}

function stableStringify(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value as Record<string, unknown>).sort().map((key) => (
      `${JSON.stringify(key)}:${stableStringify((value as Record<string, unknown>)[key])}`
    )).join(',')}}`;
  }
  return JSON.stringify(value);
}

function manifestIntegrityPayload(manifest: CanonicalTransactionManifest) {
  const { manifestHash, signature, ...rest } = manifest;
  return rest;
}

function manifestHash(manifest: CanonicalTransactionManifest) {
  return hash(stableStringify(manifestIntegrityPayload(manifest)));
}

function manifestSignature(manifest: CanonicalTransactionManifest) {
  const key = process.env.VITRUVIUS_TRANSACTION_HMAC_KEY;
  if (!key) return undefined;
  const scopedKey = createHmac('sha256', key).update(manifest.subsystem || 'graph-canonical').digest();
  return createHmac('sha256', scopedKey).update(stableStringify(manifestIntegrityPayload(manifest))).digest('hex');
}

function shortHash(value: string) {
  return hash(value).slice(0, 12);
}

function fileHash(path: string) {
  if (!existsSync(path)) return 'missing';
  return hash(readFileSync(path));
}

function readManifestHash(path: string) {
  try {
    const payload = JSON.parse(readFileSync(path, 'utf-8')) as CanonicalTransactionManifest;
    return payload.manifestHash || null;
  } catch {
    return null;
  }
}

function latestManifestHash(transactionsDir: string) {
  if (!existsSync(transactionsDir)) return null;
  const manifests = readdirSync(transactionsDir)
    .filter((name) => name.endsWith('.json'))
    .map((name) => {
      try {
        const payload = JSON.parse(readFileSync(join(transactionsDir, name), 'utf-8')) as CanonicalTransactionManifest;
        return { name, startedAt: payload.startedAt || name, manifestHash: payload.manifestHash || null };
      } catch {
        return { name, startedAt: name, manifestHash: null };
      }
    })
    .sort((a, b) => a.startedAt.localeCompare(b.startedAt) || a.name.localeCompare(b.name));
  return manifests.at(-1)?.manifestHash || null;
}

function manifestAfterHashStrictMode() {
  return process.env.VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH === 'true';
}

function normalizeFileKey(path: string) {
  return resolve(path).toLowerCase();
}

function repoRelativeFilePath(repoRoot: string, path: string) {
  return relative(repoRoot, path).replace(/\\/g, '/');
}

function custodyCriticalFileSet(repoRoot: string) {
  const canonical = canonicalStewardshipPaths(repoRoot);
  const resource = resourceLayerFilePaths(repoRoot);
  const critical = [
    canonical.decisions,
    canonical.aliases,
    canonical.redirects,
    canonical.tombstones,
    canonical.approvals,
    canonical.admittedRelationships,
    canonical.remediationManifests,
    canonical.p1DecisionPackets,
    canonical.p1PacketReviews,
    canonical.batches,
    canonical.priorities,
    resource.resources,
    resource.links,
    resource.sourceFamilies,
    resource.checks,
    resource.candidates,
    resource.localFileIndex,
    resource.reviewDecisions,
  ];
  return new Set(critical.map(normalizeFileKey));
}

function deterministicWrite(path: string, payload: unknown) {
  mkdirSync(dirname(path), { recursive: true });
  const tmp = `${path}.tmp`;
  writeFileSync(tmp, `${JSON.stringify(payload, null, 2)}\n`);
  if (existsSync(path)) rmSync(path, { force: true });
  renameSync(tmp, path);
}

function writeManifest(path: string, manifest: CanonicalTransactionManifest) {
  const next: CanonicalTransactionManifest = { ...manifest };
  next.manifestHash = manifestHash(next);
  next.signature = manifestSignature(next);
  deterministicWrite(path, next);
  return next;
}

function clearStaleLock(path: string, maxAgeMs = 10 * 60 * 1000) {
  if (!existsSync(path)) return;
  const ageMs = Date.now() - statSync(path).mtimeMs;
  if (ageMs > maxAgeMs) rmSync(path, { force: true });
}

function readJson(path: string, fallback: Record<string, unknown>) {
  if (!existsSync(path)) return fallback;
  const parsed = JSON.parse(readFileSync(path, 'utf-8').replace(/^\uFEFF/, '') || '{}');
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error(`${path} must contain a JSON object`);
  return parsed as Record<string, unknown>;
}

export function canonicalStewardshipPaths(repoRoot: string) {
  const dir = resolve(repoRoot, CANONICAL_DIR);
  return {
    dir,
    decisions: join(dir, 'stewardship-decisions.json'),
    aliases: join(dir, 'aliases.json'),
    redirects: join(dir, 'redirects.json'),
    tombstones: join(dir, 'tombstones.json'),
    approvals: join(dir, 'approvals.json'),
    admittedRelationships: join(dir, 'admitted-relationships.json'),
    remediationManifests: join(dir, 'remediation-manifests.json'),
    p1DecisionPackets: join(dir, 'p1-decision-packets.json'),
    p1PacketReviews: join(dir, 'p1-packet-reviews.json'),
    batches: join(dir, 'batches.json'),
    priorities: join(dir, 'priorities.json'),
    transactionsDir: join(dir, 'transaction-manifests'),
    lock: join(dir, '.canonical-stewardship.lock'),
  };
}

export function readCanonicalDecisions(repoRoot: string): CanonicalStewardshipDecision[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).decisions, { stewardshipDecisions: [] });
  return Array.isArray(payload.stewardshipDecisions) ? payload.stewardshipDecisions as CanonicalStewardshipDecision[] : [];
}

export function readCanonicalAliases(repoRoot: string): CanonicalAliasRecord[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).aliases, { aliases: [] });
  return Array.isArray(payload.aliases) ? payload.aliases as CanonicalAliasRecord[] : [];
}

export function readCanonicalRedirects(repoRoot: string): CanonicalRedirectRecord[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).redirects, { redirects: [] });
  return Array.isArray(payload.redirects) ? payload.redirects as CanonicalRedirectRecord[] : [];
}

export function readCanonicalTombstones(repoRoot: string): CanonicalTombstoneRecord[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).tombstones, { tombstones: [] });
  return Array.isArray(payload.tombstones) ? payload.tombstones as CanonicalTombstoneRecord[] : [];
}

export function readCanonicalApprovals(repoRoot: string): CanonicalStewardshipApproval[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).approvals, { approvals: [] });
  return Array.isArray(payload.approvals) ? payload.approvals as CanonicalStewardshipApproval[] : [];
}

export function readCanonicalAdmittedRelationships(repoRoot: string): CanonicalAdmittedRelationship[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).admittedRelationships, { admittedRelationships: [] });
  return Array.isArray(payload.admittedRelationships) ? payload.admittedRelationships as CanonicalAdmittedRelationship[] : [];
}

export function readCanonicalRemediationManifests(repoRoot: string): CanonicalRemediationManifest[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).remediationManifests, { remediationManifests: [] });
  return Array.isArray(payload.remediationManifests) ? payload.remediationManifests as CanonicalRemediationManifest[] : [];
}

export function readCanonicalP1DecisionPackets(repoRoot: string): CanonicalP1DecisionPacket[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).p1DecisionPackets, { packets: [] });
  return Array.isArray(payload.packets) ? payload.packets as CanonicalP1DecisionPacket[] : [];
}

export function readCanonicalP1PacketReviews(repoRoot: string): CanonicalP1PacketOntologyReview[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).p1PacketReviews, { reviews: [] });
  return Array.isArray(payload.reviews) ? payload.reviews as CanonicalP1PacketOntologyReview[] : [];
}

export function readCanonicalPriorityOverrides(repoRoot: string): CanonicalPriorityOverride[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).priorities, { priorities: [] });
  return Array.isArray(payload.priorities) ? payload.priorities as CanonicalPriorityOverride[] : [];
}

export function readCanonicalBatches(repoRoot: string): CanonicalBatchRecord[] {
  const payload = readJson(canonicalStewardshipPaths(repoRoot).batches, { batches: [] });
  return Array.isArray(payload.batches) ? payload.batches as CanonicalBatchRecord[] : [];
}

function writeCanonicalDecisions(repoRoot: string, decisions: CanonicalStewardshipDecision[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).decisions, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    stewardshipDecisions: decisions,
  });
}

function writeCanonicalAliases(repoRoot: string, aliases: CanonicalAliasRecord[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).aliases, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    aliases,
  });
}

function writeCanonicalRedirects(repoRoot: string, redirects: CanonicalRedirectRecord[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).redirects, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    redirects,
  });
}

function writeCanonicalTombstones(repoRoot: string, tombstones: CanonicalTombstoneRecord[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).tombstones, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    tombstones,
  });
}

function writeCanonicalApprovals(repoRoot: string, approvals: CanonicalStewardshipApproval[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).approvals, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    approvals,
  });
}

function writeCanonicalAdmittedRelationships(repoRoot: string, admittedRelationships: CanonicalAdmittedRelationship[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).admittedRelationships, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    admittedRelationships,
  });
}

function writeCanonicalRemediationManifests(repoRoot: string, remediationManifests: CanonicalRemediationManifest[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).remediationManifests, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    remediationManifests,
  });
}

function writeCanonicalP1DecisionPackets(repoRoot: string, packets: CanonicalP1DecisionPacket[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).p1DecisionPackets, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    packets,
  });
}

function writeCanonicalP1PacketReviews(repoRoot: string, reviews: CanonicalP1PacketOntologyReview[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).p1PacketReviews, {
    schemaVersion: `${CANONICAL_STEWARDSHIP_SCHEMA_VERSION}/p1-packet-reviews`,
    generatedAt: nowIso(),
    reviews,
  });
}

function writeCanonicalPriorityOverrides(repoRoot: string, priorities: CanonicalPriorityOverride[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).priorities, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    priorities,
  });
}

function writeCanonicalBatches(repoRoot: string, batches: CanonicalBatchRecord[]) {
  deterministicWrite(canonicalStewardshipPaths(repoRoot).batches, {
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    batches,
  });
}

function withCanonicalTransaction<T>(repoRoot: string, operationType: string, files: string[], fn: (manifest?: CanonicalTransactionManifest) => T) {
  const paths = canonicalStewardshipPaths(repoRoot);
  mkdirSync(paths.dir, { recursive: true });
  mkdirSync(paths.transactionsDir, { recursive: true });
  let lockFd: number | null = null;
  const startedAt = nowIso();
  const transactionId = `canonical-tx-${startedAt.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${operationType}:${startedAt}`)}`;
  const manifestPath = join(paths.transactionsDir, `${transactionId}.json`);
  const manifest: CanonicalTransactionManifest = {
    transactionId,
    operationType,
    subsystem: 'graph-canonical',
    startedAt,
    filesTouched: files,
    beforeHashes: Object.fromEntries(files.map((path) => [path, fileHash(path)])),
    previousManifestHash: latestManifestHash(paths.transactionsDir),
    dryRun: false,
    warnings: [],
    errors: [],
    validationStatus: 'pending',
  };
  try {
    clearStaleLock(paths.lock);
    lockFd = openSync(paths.lock, 'wx');
    Object.assign(manifest, writeManifest(manifestPath, manifest));
    const result = fn(manifest);
    manifest.completedAt = nowIso();
    manifest.afterHashes = Object.fromEntries(files.map((path) => [path, fileHash(path)]));
    manifest.validationStatus = 'passed';
    Object.assign(manifest, writeManifest(manifestPath, manifest));
    return { result, manifest };
  } catch (error) {
    manifest.completedAt = nowIso();
    manifest.validationStatus = 'failed';
    manifest.error = error instanceof Error ? error.message : String(error);
    manifest.errors = [manifest.error];
    Object.assign(manifest, writeManifest(manifestPath, manifest));
    throw error;
  } finally {
    if (lockFd !== null) closeSync(lockFd);
    if (existsSync(paths.lock)) rmSync(paths.lock, { force: true });
  }
}

function labelFor(node: GraphNodeLike) {
  return node.displayLabel || node.label || node.id;
}

function aliasesFor(node: GraphNodeLike) {
  return Array.isArray(node.aliases) ? node.aliases.filter((value): value is string => typeof value === 'string') : [];
}

function taxonomyFor(node: GraphNodeLike) {
  return Array.isArray(node.taxonomy_path) ? node.taxonomy_path.filter((value): value is string => typeof value === 'string') : [];
}

function edgeCounts(edges: GraphEdgeLike[]) {
  const incoming = new Map<string, number>();
  const outgoing = new Map<string, number>();
  for (const edge of edges) {
    outgoing.set(edge.source, (outgoing.get(edge.source) || 0) + 1);
    incoming.set(edge.target, (incoming.get(edge.target) || 0) + 1);
  }
  return { incoming, outgoing };
}

function resourceCounts(data?: ResourceLayerData) {
  const counts = new Map<string, number>();
  for (const link of data?.nodeResourceLinks || []) counts.set(link.nodeId, (counts.get(link.nodeId) || 0) + 1);
  return counts;
}

function groupIdFor(normalized: string, nodeIds: string[]) {
  return `dup-${shortHash(`${normalized}:${nodeIds.slice().sort().join('|')}`)}`;
}

function statusFor(groupId: string, decisions: CanonicalStewardshipDecision[]): DuplicateCandidateGroup['status'] {
  const applied = decisions.find((decision) => decision.candidateGroupId === groupId && ['applied', 'steward_approved', 'admitted'].includes(decision.status));
  if (!applied) return 'unresolved';
  if (applied.decisionType === 'KEEP_SEPARATE') return 'keep_separate';
  if (DISAMBIGUATION_DECISION_TYPES.has(applied.decisionType)) return 'disambiguated';
  if (applied.decisionType === 'REJECT_DUPLICATE_CANDIDATE') return 'rejected';
  if (applied.decisionType === 'NEEDS_HUMAN_REVIEW' || applied.decisionType === 'SPLIT_OR_RETYPE_NEEDED') return 'needs_review';
  return 'applied';
}

function scoreGroup(nodes: DuplicateCandidateNodeSummary[]) {
  const reasons: string[] = [];
  let riskScore = 0;
  const types = new Set(nodes.map((node) => node.type || 'unknown'));
  const taxonomies = new Set(nodes.map((node) => node.taxonomyPath.join(' > ')));
  const totalEdges = nodes.reduce((sum, node) => sum + node.incomingEdgeCount + node.outgoingEdgeCount, 0);
  const totalResources = nodes.reduce((sum, node) => sum + node.resourceLinkCount, 0);
  if (types.size > 1) { riskScore += 0.25; reasons.push('different node types'); }
  if (taxonomies.size > 1) { riskScore += 0.25; reasons.push('different taxonomy contexts'); }
  if (totalEdges > 20) { riskScore += 0.2; reasons.push('high combined edge count'); }
  if (totalResources > 0) { riskScore += 0.15; reasons.push('resource links must be preserved'); }
  if (nodes.some((node) => /material|assembly|system|process|procedure|building|work|person/i.test(`${node.type} ${node.taxonomyPath.join(' ')}`))) {
    riskScore += 0.1;
    reasons.push('possible subtype, homonym, or instance-vs-concept distinction');
  }
  riskScore = Math.min(1, riskScore);
  const riskLevel: CanonicalRiskLevel = riskScore >= 0.75 ? 'critical' : riskScore >= 0.5 ? 'high' : riskScore >= 0.25 ? 'medium' : 'low';
  let candidateCategory: DuplicateCandidateCategory = riskLevel === 'low'
    ? 'safe_review_candidate'
    : riskLevel === 'medium'
      ? 'likely_alias_candidate'
      : riskLevel === 'high'
        ? 'manual_review_candidate'
        : 'unsafe_auto_merge';
  if (reasons.some((reason) => reason.includes('subtype'))) candidateCategory = riskLevel === 'low' ? 'likely_alias_candidate' : 'subtype_not_duplicate';
  const suggestedAction: CanonicalDecisionType = riskLevel === 'low' ? 'ALIAS_TO_CANONICAL' : 'NEEDS_HUMAN_REVIEW';
  return { riskScore, riskLevel, candidateCategory, suggestedAction, riskReasons: reasons.length ? reasons : ['exact normalized label match'] };
}

export function prioritizeDuplicateGroup(group: Pick<DuplicateCandidateGroup, 'looseNormalizedLabel' | 'nodes' | 'edgeCount' | 'resourceLinkCount' | 'riskLevel' | 'candidateCategory'>): { priorityBand: CanonicalPriorityBand; priorityScore: number; priorityReasons: string[] } {
  const label = group.looseNormalizedLabel.toLowerCase();
  const taxonomyText = group.nodes.flatMap((node) => node.taxonomyPath).join(' ').toLowerCase();
  const typeText = group.nodes.map((node) => node.type || '').join(' ').toLowerCase();
  const reasons: string[] = [];
  let score = 0;

  if (/\b(concrete|reinforced concrete)\b/.test(label)) {
    score += 100;
    reasons.push('user-mentioned concrete/reinforced concrete duplicate group');
  }
  if (/\b(building|material|wall|slab|foundation|beam|column|room|space|door|window|facade|roof)\b/.test(label)) {
    score += 35;
    reasons.push('search-critical/high-level AEC concept label');
  }
  if (/(arc|architecture|civil|str|structural)/i.test(`${taxonomyText} ${typeText}`)) {
    score += 18;
    reasons.push('Architecture/Civil/Structural taxonomy touchpoint');
  }
  if (group.edgeCount >= 50) {
    score += 30;
    reasons.push('very high edge count');
  } else if (group.edgeCount >= 20) {
    score += 18;
    reasons.push('high edge count');
  } else if (group.edgeCount >= 5) {
    score += 8;
    reasons.push('moderate relationship footprint');
  }
  if (group.resourceLinkCount > 0) {
    score += 25;
    reasons.push('Resource Layer links require preservation');
  }
  if (group.riskLevel === 'high' || group.riskLevel === 'critical') {
    score += 10;
    reasons.push('high-risk group needs steward attention before canonicalization');
  }
  if (group.candidateCategory === 'safe_review_candidate' || group.candidateCategory === 'likely_alias_candidate') {
    score += 10;
    reasons.push('likely efficient alias/keep-separate review candidate');
  }

  let priorityBand: CanonicalPriorityBand = score >= 80 ? 'P0' : score >= 45 ? 'P1' : score >= 20 ? 'P2' : 'P3';
  if (group.riskLevel === 'critical' && priorityBand !== 'P0') {
    priorityBand = 'BLOCKED';
    reasons.push('critical-risk candidate blocked from batch resolution without domain review');
  }
  return { priorityBand, priorityScore: score, priorityReasons: reasons.length ? reasons : ['low-impact duplicate candidate'] };
}

export interface DuplicateFilters {
  status?: string;
  riskLevel?: string;
  query?: string;
  label?: string;
  taxonomy?: string;
  nodeType?: string;
  hasResourceLinks?: boolean;
  hasHighEdgeCount?: boolean;
  concreteOnly?: boolean;
  safeCandidatesOnly?: boolean;
  manualReviewOnly?: boolean;
  priorityBand?: CanonicalPriorityBand;
  limit?: number;
  offset?: number;
}

export function buildDuplicateCandidateGroups(
  nodes: GraphNodeLike[],
  edges: GraphEdgeLike[],
  resourceData?: ResourceLayerData,
  decisions: CanonicalStewardshipDecision[] = [],
  filters: DuplicateFilters = {},
) {
  const byNormalized = new Map<string, GraphNodeLike[]>();
  for (const node of nodes) {
    const normalized = normalizeCanonicalLabelLoose(labelFor(node));
    if (!normalized) continue;
    byNormalized.set(normalized, [...(byNormalized.get(normalized) || []), node]);
  }
  const counts = edgeCounts(edges);
  const resources = resourceCounts(resourceData);
  const groups: DuplicateCandidateGroup[] = [];
  for (const [normalized, groupNodes] of byNormalized.entries()) {
    if (groupNodes.length < 2) continue;
    const sorted = groupNodes.slice().sort((a, b) => a.id.localeCompare(b.id));
    const summaries = sorted.map((node) => ({
      id: node.id,
      label: labelFor(node),
      displayLabel: node.displayLabel,
      type: node.type,
      aliases: aliasesFor(node),
      taxonomyPath: taxonomyFor(node),
      incomingEdgeCount: counts.incoming.get(node.id) || 0,
      outgoingEdgeCount: counts.outgoing.get(node.id) || 0,
      resourceLinkCount: resources.get(node.id) || 0,
    }));
    const nodeIds = summaries.map((node) => node.id);
    const groupId = groupIdFor(normalized, nodeIds);
    const existingDecisions = decisions.filter((decision) => decision.candidateGroupId === groupId);
    const scoring = scoreGroup(summaries);
    const baseGroup = {
      groupId,
      normalizedLabel: normalizeCanonicalLabel(labelFor(sorted[0])),
      looseNormalizedLabel: normalized,
      labels: Array.from(new Set(summaries.map((node) => node.label))).sort(),
      nodes: summaries,
      nodeIds,
      ...scoring,
      edgeCount: summaries.reduce((sum, node) => sum + node.incomingEdgeCount + node.outgoingEdgeCount, 0),
      resourceLinkCount: summaries.reduce((sum, node) => sum + node.resourceLinkCount, 0),
      existingDecisions,
      status: statusFor(groupId, existingDecisions),
    } as DuplicateCandidateGroup;
    Object.assign(baseGroup, prioritizeDuplicateGroup(baseGroup));
    groups.push(baseGroup);
  }
  let filtered = groups.sort((a, b) => b.riskScore - a.riskScore || a.looseNormalizedLabel.localeCompare(b.looseNormalizedLabel));
  const query = (filters.query || filters.label || '').toLowerCase().trim();
  if (query) filtered = filtered.filter((group) => group.looseNormalizedLabel.includes(query) || group.labels.some((label) => label.toLowerCase().includes(query)) || group.nodeIds.includes(query));
  if (filters.concreteOnly) filtered = filtered.filter((group) => group.looseNormalizedLabel.includes('concrete'));
  if (filters.status && filters.status !== 'all') filtered = filtered.filter((group) => group.status === filters.status);
  if (filters.riskLevel) filtered = filtered.filter((group) => group.riskLevel === filters.riskLevel);
  if (filters.nodeType) filtered = filtered.filter((group) => group.nodes.some((node) => node.type === filters.nodeType));
  if (filters.taxonomy) filtered = filtered.filter((group) => group.nodes.some((node) => node.taxonomyPath.join(' ').toLowerCase().includes(String(filters.taxonomy).toLowerCase())));
  if (filters.hasResourceLinks) filtered = filtered.filter((group) => group.resourceLinkCount > 0);
  if (filters.hasHighEdgeCount) filtered = filtered.filter((group) => group.edgeCount > 20);
  if (filters.safeCandidatesOnly) filtered = filtered.filter((group) => group.candidateCategory === 'safe_review_candidate' || group.candidateCategory === 'likely_alias_candidate');
  if (filters.manualReviewOnly) filtered = filtered.filter((group) => group.riskLevel === 'high' || group.riskLevel === 'critical' || group.candidateCategory === 'manual_review_candidate');
  if (filters.priorityBand) filtered = filtered.filter((group) => group.priorityBand === filters.priorityBand);
  const offset = Math.max(0, Number(filters.offset || 0));
  const limit = filters.limit == null ? undefined : Math.max(1, Number(filters.limit));
  return limit ? filtered.slice(offset, offset + limit) : filtered.slice(offset);
}

export function findDuplicateGroup(groups: DuplicateCandidateGroup[], groupId: string) {
  return groups.find((group) => group.groupId === groupId) || null;
}

function countsBy<T extends string>(values: T[]) {
  return values.reduce((acc, value) => {
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
}

function batchStats(groups: DuplicateCandidateGroup[]) {
  return {
    groupCount: groups.length,
    riskCounts: countsBy(groups.map((group) => group.riskLevel)),
    priorityCounts: countsBy(groups.map((group) => group.priorityBand)),
    candidateCategoryCounts: countsBy(groups.map((group) => group.candidateCategory)),
    destructiveActionsBlocked: true,
  };
}

export function listCanonicalBatches(repoRoot: string, groups: DuplicateCandidateGroup[] = []) {
  const byId = new Map(groups.map((group) => [group.groupId, group]));
  return readCanonicalBatches(repoRoot).map((batch) => {
    const liveGroups = batch.groupIds.map((id) => byId.get(id)).filter(Boolean) as DuplicateCandidateGroup[];
    return { ...batch, stats: liveGroups.length ? batchStats(liveGroups) : batch.stats };
  });
}

export function createCanonicalBatch(
  repoRoot: string,
  groups: DuplicateCandidateGroup[],
  request: { name?: string; filters?: DuplicateFilters; reviewer?: string; priorityBand?: CanonicalPriorityBand; tags?: string[]; notes?: string },
) {
  const timestamp = nowIso();
  const groupIds = groups.map((group) => group.groupId);
  const batchId = `canonical-batch-${timestamp.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${groupIds.join('|')}:${request.name || ''}`)}`;
  const batch: CanonicalBatchRecord = {
    batchId,
    name: request.name?.trim() || `Canonical duplicate review batch ${timestamp}`,
    filters: request.filters || {},
    groupIds,
    status: 'open',
    reviewer: request.reviewer,
    priorityBand: request.priorityBand,
    tags: Array.from(new Set(request.tags || [])).sort(),
    notes: request.notes,
    createdAt: timestamp,
    updatedAt: timestamp,
    stats: batchStats(groups),
    decisions: [],
  };
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_batch_create', [paths.batches], () => {
    const batches = readCanonicalBatches(repoRoot);
    writeCanonicalBatches(repoRoot, [...batches, batch]);
    return { batch };
  });
  return { ...result, manifest };
}

export function findCanonicalBatch(repoRoot: string, batchId: string, groups: DuplicateCandidateGroup[] = []) {
  return listCanonicalBatches(repoRoot, groups).find((batch) => batch.batchId === batchId) || null;
}

const BATCH_ACTIONS = new Set(['assign_reviewer', 'set_priority', 'tag_groups', 'mark_needs_review', 'mark_keep_separate', 'reject_duplicate_candidate']);

export function previewCanonicalBatchDecision(
  batch: CanonicalBatchRecord,
  groups: DuplicateCandidateGroup[],
  request: { action: string; reviewer?: string; rationale?: string; notes?: string; priorityBand?: CanonicalPriorityBand; tags?: string[]; dryRun?: boolean; apply?: boolean },
) {
  const blockers: string[] = [];
  const warnings: string[] = [];
  if (!BATCH_ACTIONS.has(request.action)) blockers.push(`unsupported or destructive batch action: ${request.action}`);
  if (!request.reviewer?.trim()) blockers.push('reviewer is required');
  if (!request.rationale?.trim()) blockers.push('rationale is required');
  if (request.action.toLowerCase().includes('merge')) blockers.push('batch MERGE_INTO_CANONICAL is always blocked; use per-group review only');
  if ((request.action === 'mark_keep_separate' || request.action === 'reject_duplicate_candidate') && groups.some((group) => group.priorityBand === 'P0' || group.riskLevel === 'high' || group.riskLevel === 'critical')) {
    warnings.push('batch keep-separate/reject includes P0 or high-risk groups; prefer per-group decision packets');
  }
  return {
    dryRun: true,
    batchId: batch.batchId,
    action: request.action,
    affectedGroupIds: batch.groupIds,
    priorityBand: request.priorityBand,
    tags: Array.from(new Set([...(batch.tags || []), ...(request.tags || [])])).sort(),
    blockers,
    warnings,
    beforeSnapshot: batch,
    afterPreview: {
      status: request.apply ? 'in_review' : batch.status,
      reviewer: request.reviewer || batch.reviewer,
      priorityBand: request.priorityBand || batch.priorityBand,
      tags: Array.from(new Set([...(batch.tags || []), ...(request.tags || [])])).sort(),
    },
  };
}

export function recordCanonicalBatchDecision(
  repoRoot: string,
  batchId: string,
  groups: DuplicateCandidateGroup[],
  request: { action: string; reviewer?: string; rationale?: string; notes?: string; priorityBand?: CanonicalPriorityBand; tags?: string[]; dryRun?: boolean; apply?: boolean },
) {
  const batch = findCanonicalBatch(repoRoot, batchId, groups);
  if (!batch) return { blockers: ['canonical batch not found'] };
  const preview = previewCanonicalBatchDecision(batch, groups, request);
  if (request.dryRun || !request.apply || preview.blockers.length) return { dryRun: true, preview, blockers: preview.blockers };
  const timestamp = nowIso();
  const decision = {
    batchDecisionId: `batch-decision-${timestamp.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${batchId}:${request.action}:${request.rationale}`)}`,
    action: request.action,
    reviewer: request.reviewer!.trim(),
    rationale: request.rationale!.trim(),
    notes: request.notes,
    createdAt: timestamp,
    dryRun: false,
    applied: true,
    affectedGroupIds: batch.groupIds,
    blockers: [],
    warnings: preview.warnings,
  };
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_batch_decision', [paths.batches], () => {
    const batches = readCanonicalBatches(repoRoot);
    const next = batches.map((entry) => entry.batchId === batchId ? {
      ...entry,
      status: 'in_review' as const,
      reviewer: request.reviewer || entry.reviewer,
      priorityBand: request.priorityBand || entry.priorityBand,
      tags: Array.from(new Set([...(entry.tags || []), ...(request.tags || [])])).sort(),
      notes: request.notes || entry.notes,
      updatedAt: timestamp,
      decisions: [...entry.decisions, decision],
    } : entry);
    writeCanonicalBatches(repoRoot, next);
    return { batchDecision: decision, preview };
  });
  return { ...result, manifest };
}

export function setCanonicalGroupPriority(
  repoRoot: string,
  groupId: string,
  request: { priorityBand: CanonicalPriorityBand; reviewer?: string; owner?: string; notes?: string; tags?: string[] },
) {
  const timestamp = nowIso();
  const override: CanonicalPriorityOverride = {
    groupId,
    priorityBand: request.priorityBand,
    owner: request.owner,
    notes: request.notes,
    tags: Array.from(new Set(request.tags || [])).sort(),
    updatedAt: timestamp,
    updatedBy: request.reviewer || 'local-dev-reviewer',
  };
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_group_priority', [paths.priorities], () => {
    const priorities = readCanonicalPriorityOverrides(repoRoot).filter((entry) => entry.groupId !== groupId);
    writeCanonicalPriorityOverrides(repoRoot, [...priorities, override].sort((a, b) => a.groupId.localeCompare(b.groupId)));
    return { priority: override };
  });
  return { ...result, manifest };
}

export function applyPriorityOverrides(repoRoot: string, groups: DuplicateCandidateGroup[]) {
  const overrides = new Map(readCanonicalPriorityOverrides(repoRoot).map((entry) => [entry.groupId, entry]));
  return groups.map((group) => {
    const override = overrides.get(group.groupId);
    return override
      ? { ...group, priorityBand: override.priorityBand, priorityReasons: [`manual priority override by ${override.updatedBy}`, ...group.priorityReasons], operationalTags: override.tags, assignedReviewer: override.owner, reviewNotes: override.notes }
      : group;
  }).sort((a, b) => {
    const order: Record<CanonicalPriorityBand, number> = { P0: 0, P1: 1, P2: 2, P3: 3, BLOCKED: 4 };
    return order[a.priorityBand] - order[b.priorityBand] || b.priorityScore - a.priorityScore || a.looseNormalizedLabel.localeCompare(b.looseNormalizedLabel);
  });
}

function compactNodeForSnapshot(node: GraphNodeLike | DuplicateCandidateNodeSummary) {
  const candidate = node as Record<string, any>;
  return {
    id: String(candidate.id || ''),
    label: String(candidate.label || candidate.canonicalLabel || candidate.displayLabel || ''),
    type: candidate.type ? String(candidate.type) : undefined,
  };
}

function compactEdgeForSnapshot(edge: GraphEdgeLike) {
  const candidate = edge as Record<string, any>;
  return {
    id: String(candidate.id || ''),
    source: String(candidate.source || ''),
    target: String(candidate.target || ''),
    type: String(candidate.type || candidate.relationType || ''),
  };
}

function compactGroupForSnapshot(group: DuplicateCandidateGroup) {
  return {
    groupId: group.groupId,
    label: group.looseNormalizedLabel,
    nodeIds: [...group.nodeIds].sort(),
    priorityBand: group.priorityBand,
    priorityScore: group.priorityScore,
    riskLevel: group.riskLevel,
    riskScore: group.riskScore,
    candidateCategory: group.candidateCategory,
    status: group.status,
    edgeCount: group.edgeCount,
    resourceLinkCount: group.resourceLinkCount,
    existingDecisionIds: group.existingDecisions.map((decision) => decision.decisionId).sort(),
  };
}

function compactResourceDataForSnapshot(resourceData?: ResourceLayerData) {
  return {
    schemaVersion: resourceData?.schemaVersion,
    resources: (resourceData?.resources || []).map((resource) => ({
      id: resource.id,
      type: resource.resourceType,
      verificationStatus: resource.verificationStatus,
      authority: resource.sourceAuthority,
      canonicalUrl: resource.canonicalUrl || resource.url || resource.landingPageUrl || resource.pdfUrl,
      doi: resource.doi,
      isbn10: resource.isbn10,
      isbn13: resource.isbn13,
    })).sort((a, b) => a.id.localeCompare(b.id)),
    nodeResourceLinks: (resourceData?.nodeResourceLinks || []).map((link) => ({
      id: link.id,
      nodeId: link.nodeId,
      resourceId: link.resourceId,
      relationship: link.relationship,
      reviewStatus: link.reviewStatus,
    })).sort((a, b) => a.id.localeCompare(b.id)),
    resourceCandidates: (resourceData?.resourceCandidates || []).map((candidate) => ({
      id: candidate.id,
      nodeId: candidate.nodeId,
      reviewStatus: candidate.reviewStatus,
      duplicateOfResourceId: candidate.duplicateOfResourceId,
    })).sort((a, b) => a.id.localeCompare(b.id)),
  };
}

function p1SourceSnapshotHash(snapshot: Omit<CanonicalP1SourceSnapshot, 'snapshotHash'> | CanonicalP1SourceSnapshot) {
  const { snapshotHash: _snapshotHash, ...payload } = snapshot as CanonicalP1SourceSnapshot;
  return hash(stableStringify(payload));
}

function p1PacketContentPayload(packet: Omit<CanonicalP1DecisionPacket, 'packetContentHash'> | CanonicalP1DecisionPacket) {
  const {
    packetContentHash: _packetContentHash,
    signature: _signature,
    ontologyReviewStatus: _ontologyReviewStatus,
    ontologyReview: _ontologyReview,
    reviewHistory: _reviewHistory,
    ...payload
  } = packet as CanonicalP1DecisionPacket;
  return payload;
}

function p1PacketContentHash(packet: Omit<CanonicalP1DecisionPacket, 'packetContentHash'> | CanonicalP1DecisionPacket) {
  return hash(stableStringify(p1PacketContentPayload(packet)));
}

function packetSigningConfig() {
  const packetKey = process.env.VITRUVIUS_PACKET_HMAC_KEY;
  if (packetKey) {
    return {
      key: createHmac('sha256', packetKey).update('graph-canonical:p1-packet').digest(),
      keyId: 'env:VITRUVIUS_PACKET_HMAC_KEY:graph-canonical:p1-packet',
      signerId: 'vitruvius-local-p1-packet-signer',
    };
  }
  const transactionKey = process.env.VITRUVIUS_TRANSACTION_HMAC_KEY;
  if (transactionKey) {
    return {
      key: createHmac('sha256', transactionKey).update('graph-canonical:p1-packet').digest(),
      keyId: 'env:VITRUVIUS_TRANSACTION_HMAC_KEY:graph-canonical:p1-packet',
      signerId: 'vitruvius-local-transaction-derived-p1-packet-signer',
    };
  }
  return null;
}

function requireP1PacketSignatures() {
  return String(process.env.VITRUVIUS_REQUIRE_PACKET_SIGNATURES || '').toLowerCase() === 'true';
}

function p1PacketSignaturePayload(packet: CanonicalP1DecisionPacket) {
  return {
    signaturePayloadVersion: 'vitruvius-p1-packet-signature-payload/v1',
    signaturePurpose: 'p1_packet_custody_integrity',
    schemaVersion: packet.schemaVersion,
    packetId: packet.packetId,
    packetRunId: packet.packetRunId,
    groupId: packet.groupId,
    generatedAt: packet.generatedAt,
    sourceQueryOrBatchId: packet.sourceQueryOrBatchId,
    truthCaveat: packet.truthCaveat,
    nodeIds: [...packet.nodeIds].sort(),
    sourceSnapshotHash: packet.sourceSnapshot?.snapshotHash,
    sourceSnapshotSchemaVersion: packet.sourceSnapshot?.schemaVersion,
    sourceSnapshotHashAlgorithm: packet.sourceSnapshot?.hashAlgorithm,
    sourceSnapshotStaleCheckPolicy: packet.sourceSnapshot?.staleCheckPolicy,
    packetContentHash: packet.packetContentHash,
    groupInputHash: packet.groupInputHash,
    candidateEdgeNeighborhoodHash: packet.candidateEdgeNeighborhoodHash,
    recommendedDecisionType: packet.recommendedDecisionType,
    mergeSafety: packet.mergeSafety,
    mergeApplied: Boolean(packet.mergeApplied),
    aliasApplied: Boolean(packet.aliasApplied),
    redirectApplied: Boolean(packet.redirectApplied),
    tombstoneApplied: Boolean(packet.tombstoneApplied),
    productionGraphWritePerformed: Boolean(packet.productionGraphWritePerformed),
    resourceLinkRewritePerformed: Boolean(packet.resourceLinkRewritePerformed),
    admittedRelationshipWritten: Boolean(packet.admittedRelationshipWritten),
  };
}

function p1PacketSignaturePayloadHash(packet: CanonicalP1DecisionPacket) {
  return hash(stableStringify(p1PacketSignaturePayload(packet)));
}

function attachP1PacketSignature(packet: CanonicalP1DecisionPacket, timestamp: string): CanonicalP1DecisionPacket {
  const signaturePayloadHash = p1PacketSignaturePayloadHash(packet);
  const signing = packetSigningConfig();
  if (!signing) {
    return {
      ...packet,
      signature: {
        signatureStatus: 'unsigned',
        signatureAlgorithm: 'hmac-sha256',
        signatureScope: 'p1_packet_snapshot',
        signaturePayloadHash,
        signatureVerificationCheckedAt: timestamp,
      },
    };
  }
  const signaturePayload = stableStringify(p1PacketSignaturePayload(packet));
  const signature = createHmac('sha256', signing.key).update(signaturePayload).digest('hex');
  return {
    ...packet,
    signature: {
      signatureStatus: 'valid',
      signatureAlgorithm: 'hmac-sha256',
      signatureScope: 'p1_packet_snapshot',
      signature,
      signedAt: timestamp,
      signerId: signing.signerId,
      systemSignerId: 'canonical_p1_decision_packet_generation',
      keyId: signing.keyId,
      signaturePayloadHash,
      signatureVerificationCheckedAt: timestamp,
    },
  };
}

function verifyP1PacketSignature(packet: CanonicalP1DecisionPacket, checkedAt = nowIso()) {
  const signaturePayloadHash = p1PacketSignaturePayloadHash(packet);
  const stored = packet.signature;
  const signing = packetSigningConfig();
  if (!stored || !stored.signature) {
    return {
      status: requireP1PacketSignatures() && !signing ? 'missing_key' as CanonicalP1PacketSignatureStatus : 'unsigned' as CanonicalP1PacketSignatureStatus,
      signaturePayloadHash,
      signatureVerificationCheckedAt: checkedAt,
      signatureAlgorithm: stored?.signatureAlgorithm || 'hmac-sha256',
      signatureScope: stored?.signatureScope || 'p1_packet_snapshot',
    };
  }
  if (stored.signatureAlgorithm !== 'hmac-sha256' || stored.signatureScope !== 'p1_packet_snapshot') {
    return {
      status: 'unsupported' as CanonicalP1PacketSignatureStatus,
      signaturePayloadHash,
      signatureVerificationCheckedAt: checkedAt,
      signatureAlgorithm: stored.signatureAlgorithm,
      signatureScope: stored.signatureScope,
    };
  }
  if (!signing) {
    return {
      status: 'missing_key' as CanonicalP1PacketSignatureStatus,
      signaturePayloadHash,
      signatureVerificationCheckedAt: checkedAt,
      signatureAlgorithm: stored.signatureAlgorithm,
      signatureScope: stored.signatureScope,
    };
  }
  const expected = createHmac('sha256', signing.key).update(stableStringify(p1PacketSignaturePayload(packet))).digest('hex');
  const payloadHashMatches = stored.signaturePayloadHash === signaturePayloadHash;
  const signatureMatches = (() => {
    try {
      const expectedBuffer = Buffer.from(expected, 'hex');
      const storedBuffer = Buffer.from(stored.signature, 'hex');
      return expectedBuffer.length === storedBuffer.length && timingSafeEqual(expectedBuffer, storedBuffer);
    } catch {
      return false;
    }
  })();
  return {
    status: signatureMatches && payloadHashMatches ? 'valid' as CanonicalP1PacketSignatureStatus : 'invalid' as CanonicalP1PacketSignatureStatus,
    signaturePayloadHash,
    signatureVerificationCheckedAt: checkedAt,
    signatureAlgorithm: stored.signatureAlgorithm,
    signatureScope: stored.signatureScope,
    keyId: signing.keyId,
  };
}

function buildP1SourceSnapshot(
  repoRoot: string,
  groups: DuplicateCandidateGroup[],
  edges: GraphEdgeLike[],
  options: { nodes?: GraphNodeLike[]; resourceData?: ResourceLayerData } = {},
): CanonicalP1SourceSnapshot {
  const nodes = options.nodes?.length
    ? options.nodes
    : groups.flatMap((group) => group.nodes as unknown as GraphNodeLike[]);
  const decisions = readCanonicalDecisions(repoRoot);
  const approvals = readCanonicalApprovals(repoRoot);
  const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot).filter((edge) => edge.reviewStatus !== 'rolled_back');
  const aliases = readCanonicalAliases(repoRoot);
  const redirects = readCanonicalRedirects(repoRoot);
  const tombstones = readCanonicalTombstones(repoRoot);
  const priorityOverrides = readCanonicalPriorityOverrides(repoRoot);
  const base: Omit<CanonicalP1SourceSnapshot, 'snapshotHash'> = {
    schemaVersion: `${CANONICAL_STEWARDSHIP_SCHEMA_VERSION}/p1-source-snapshot`,
    generatedFrom: 'in_memory_generation_context',
    hashAlgorithm: 'sha256-stable-json-v1',
    staleCheckPolicy: 'warn_on_current_context_mismatch',
    graphNodeCount: nodes.length,
    graphEdgeCount: edges.length,
    duplicateGroupCount: groups.length,
    p1CandidateGroupCount: groups.filter((group) => group.priorityBand === 'P1').length,
    resourceCount: options.resourceData?.resources.length || 0,
    nodeResourceLinkCount: options.resourceData?.nodeResourceLinks.length || 0,
    stewardshipDecisionCount: decisions.length,
    approvalCount: approvals.length,
    admittedRelationshipCount: admittedRelationships.length,
    aliasCount: aliases.length,
    redirectCount: redirects.length,
    tombstoneCount: tombstones.length,
    nodesHash: hash(stableStringify(nodes.map(compactNodeForSnapshot).sort((a, b) => a.id.localeCompare(b.id)))),
    edgesHash: hash(stableStringify(edges.map(compactEdgeForSnapshot).sort((a, b) => a.id.localeCompare(b.id)))),
    groupsHash: hash(stableStringify(groups.map(compactGroupForSnapshot).sort((a, b) => a.groupId.localeCompare(b.groupId)))),
    resourcesHash: hash(stableStringify(compactResourceDataForSnapshot(options.resourceData))),
    decisionsHash: hash(stableStringify(decisions.map((decision) => ({
      decisionId: decision.decisionId,
      decisionType: decision.decisionType,
      candidateGroupId: decision.candidateGroupId,
      sourceNodeIds: [...decision.sourceNodeIds].sort(),
      status: decision.status,
      riskLevel: decision.riskLevel,
      transactionManifestId: decision.transactionManifestId,
    })).sort((a, b) => a.decisionId.localeCompare(b.decisionId)))),
    approvalsHash: hash(stableStringify(approvals.map((approval) => ({
      approvalId: approval.approvalId,
      decisionId: approval.decisionId,
      decisionHash: approval.decisionHash,
      status: approval.status,
      mutationScope: approval.mutationScope,
      transactionManifestId: approval.transactionManifestId,
    })).sort((a, b) => a.approvalId.localeCompare(b.approvalId)))),
    admittedRelationshipsHash: hash(stableStringify(admittedRelationships.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: edge.type,
      stewardshipDecisionId: edge.stewardshipDecisionId,
      approvalId: edge.approvalId,
      reviewStatus: edge.reviewStatus,
    })).sort((a, b) => a.id.localeCompare(b.id)))),
    aliasesHash: hash(stableStringify(aliases.map((alias) => ({
      alias: alias.alias,
      canonicalNodeId: alias.canonicalNodeId,
      decisionId: alias.decisionId,
      status: alias.status,
    })).sort((a, b) => `${a.alias}:${a.canonicalNodeId}`.localeCompare(`${b.alias}:${b.canonicalNodeId}`)))),
    redirectsHash: hash(stableStringify(redirects.map((redirect) => ({
      sourceNodeId: redirect.sourceNodeId,
      canonicalNodeId: redirect.canonicalNodeId,
      decisionId: redirect.decisionId,
      status: redirect.status,
    })).sort((a, b) => a.sourceNodeId.localeCompare(b.sourceNodeId)))),
    tombstonesHash: hash(stableStringify(tombstones.map((tombstone) => ({
      nodeId: tombstone.nodeId,
      tombstoneStatus: tombstone.tombstoneStatus,
      canonicalTargetId: tombstone.canonicalTargetId,
      decisionId: tombstone.decisionId,
    })).sort((a, b) => a.nodeId.localeCompare(b.nodeId)))),
    priorityOverridesHash: hash(stableStringify(priorityOverrides.map((override) => ({
      groupId: override.groupId,
      priorityBand: override.priorityBand,
      owner: override.owner,
      status: override.status,
      tags: [...(override.tags || [])].sort(),
    })).sort((a, b) => a.groupId.localeCompare(b.groupId)))),
  };
  return { ...base, snapshotHash: p1SourceSnapshotHash(base) };
}

function packetRecommendationFor(group: DuplicateCandidateGroup): Pick<CanonicalP1DecisionPacket, 'recommendedDecisionType' | 'possibleRelationAdditions' | 'needsKimiReview' | 'needsHumanDomainReview' | 'mergeSafety' | 'rationale' | 'nextAction'> {
  const highRisk = group.riskLevel === 'high' || group.riskLevel === 'critical';
  const hasDifferentTaxonomy = group.riskReasons.some((reason) => reason.toLowerCase().includes('taxonomy'));
  const looksSubtype = group.candidateCategory === 'subtype_not_duplicate' || group.riskReasons.some((reason) => reason.toLowerCase().includes('subtype'));
  if (highRisk || group.resourceLinkCount > 0 || group.edgeCount > 20) {
    return {
      recommendedDecisionType: 'NEEDS_HUMAN_REVIEW',
      possibleRelationAdditions: looksSubtype ? ['RELATED_SPECIALIZATION_OF'] : ['DISAMBIGUATED_FROM'],
      needsKimiReview: true,
      needsHumanDomainReview: true,
      mergeSafety: 'blocked_without_domain_review',
      rationale: 'High-impact or high-risk duplicate group; destructive merge is blocked pending steward/domain review.',
      nextAction: 'Prepare per-group steward review with edge/resource preservation dry run.',
    };
  }
  if (hasDifferentTaxonomy || group.candidateCategory === 'homonym_collision') {
    return {
      recommendedDecisionType: 'DISAMBIGUATED_KEEP_SEPARATE',
      possibleRelationAdditions: ['DISAMBIGUATED_FROM'],
      needsKimiReview: true,
      needsHumanDomainReview: true,
      mergeSafety: 'not_recommended',
      rationale: 'Same normalized label appears across different taxonomy/type context; prefer governed disambiguation over merge.',
      nextAction: 'Ask steward to confirm distinction and add search disambiguation text.',
    };
  }
  if (group.candidateCategory === 'likely_alias_candidate' || group.candidateCategory === 'safe_review_candidate') {
    return {
      recommendedDecisionType: 'ALIAS_TO_CANONICAL',
      possibleRelationAdditions: [],
      needsKimiReview: false,
      needsHumanDomainReview: true,
      mergeSafety: 'possible_low_risk_after_review',
      rationale: 'Low-risk exact normalized-label group may be suitable for alias-only review; do not merge without explicit stewardship.',
      nextAction: 'Review node descriptions and neighborhoods, then consider alias-only decision.',
    };
  }
  return {
    recommendedDecisionType: 'NEEDS_HUMAN_REVIEW',
    possibleRelationAdditions: ['DISAMBIGUATED_FROM'],
    needsKimiReview: true,
    needsHumanDomainReview: true,
    mergeSafety: 'not_recommended',
    rationale: 'Manual review is required before any canonical action.',
    nextAction: 'Generate a group-specific decision packet and gather steward rationale.',
  };
}

function p1PacketAdmissionMetadata(repoRoot: string, group: DuplicateCandidateGroup): Pick<CanonicalP1DecisionPacket, 'packetAdmissionStatus' | 'approvalIds' | 'admittedRelationshipIds' | 'admittedDecisionIds' | 'admissionAppliedAt' | 'admissionSummary'> {
  const decisions = readCanonicalDecisions(repoRoot)
    .filter((decision) => decision.candidateGroupId === group.groupId && ['steward_approved', 'admitted', 'applied'].includes(decision.status))
    .sort((a, b) => a.decisionId.localeCompare(b.decisionId));
  const decisionIds = new Set(decisions.map((decision) => decision.decisionId));
  const approvals = readCanonicalApprovals(repoRoot)
    .filter((approval) => decisionIds.has(approval.decisionId) && approval.status !== 'rolled_back' && approval.status !== 'rejected')
    .sort((a, b) => a.approvalId.localeCompare(b.approvalId));
  const approvalIds = approvals.map((approval) => approval.approvalId);
  const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot)
    .filter((edge) => decisionIds.has(edge.stewardshipDecisionId) && edge.reviewStatus !== 'rolled_back')
    .sort((a, b) => a.id.localeCompare(b.id));
  const admittedRelationshipIds = admittedRelationships.map((edge) => edge.id);
  const admittedDecisionIds = decisions
    .filter((decision) => decision.status === 'admitted' || approvalIds.length > 0)
    .map((decision) => decision.decisionId);
  const latestAdmissionTime = [
    ...approvals.map((approval) => approval.admittedAt || approval.approvedAt),
    ...admittedRelationships.map((edge) => edge.createdAt),
    ...decisions.map((decision) => decision.appliedAt || decision.createdAt),
  ].filter(Boolean).sort().at(-1);
  if (admittedRelationships.length > 0) {
    return {
      packetAdmissionStatus: 'consumed_by_non_destructive_admission',
      approvalIds,
      admittedRelationshipIds,
      admittedDecisionIds,
      admissionAppliedAt: latestAdmissionTime,
      admissionSummary: `${group.looseNormalizedLabel} packet consumed by steward-approved non-destructive relationship admission; original ontology review remains historical/advisory and is not a merge, alias, redirect, tombstone, or source-truth claim.`,
    };
  }
  if (decisions.some((decision) => ['DISAMBIGUATED_KEEP_SEPARATE', 'GOVERNED_DISAMBIGUATION', 'KEEP_SEPARATE'].includes(decision.decisionType)) && approvals.length > 0) {
    return {
      packetAdmissionStatus: 'metadata_disambiguation_admitted',
      approvalIds,
      admittedRelationshipIds: [],
      admittedDecisionIds,
      admissionAppliedAt: latestAdmissionTime,
      admissionSummary: `${group.looseNormalizedLabel} packet consumed by steward-approved metadata-only keep-separate/disambiguation decision; no visible graph edge, merge, alias, redirect, tombstone, or Resource Layer mutation is implied.`,
    };
  }
  return {
    packetAdmissionStatus: 'not_admitted',
    approvalIds: [],
    admittedRelationshipIds: [],
    admittedDecisionIds: [],
  };
}

function p1PacketFor(
  repoRoot: string,
  group: DuplicateCandidateGroup,
  edges: GraphEdgeLike[],
  generatedAt: string,
  packetRunId: string,
  sourceSnapshot: CanonicalP1SourceSnapshot,
  existingPacket?: CanonicalP1DecisionPacket,
): CanonicalP1DecisionPacket {
  const groupNodeIds = new Set(group.nodeIds);
  const groupEdges = edges.filter((edge) => groupNodeIds.has(edge.source) || groupNodeIds.has(edge.target));
  const incoming = group.nodeIds.map((nodeId) => ({ nodeId, count: edges.filter((edge) => edge.target === nodeId).length }));
  const outgoing = group.nodeIds.map((nodeId) => ({ nodeId, count: edges.filter((edge) => edge.source === nodeId).length }));
  const topRelationTypes = countsBy(groupEdges.map((edge) => String(edge.type || edge.relationType || 'unknown')));
  const recommendation = packetRecommendationFor(group);
  const packet: Omit<CanonicalP1DecisionPacket, 'packetContentHash'> = {
    schemaVersion: `${CANONICAL_STEWARDSHIP_SCHEMA_VERSION}/p1-decision-packet`,
    packetId: existingPacket?.groupId === group.groupId ? existingPacket.packetId : `p1-decision-packet-${shortHash(`${group.groupId}:${generatedAt}`)}`,
    packetRunId,
    groupId: group.groupId,
    generatedAt,
    sourceQueryOrBatchId: 'priorityBand=P1',
    truthCaveat: 'advisory_packet_only_not_steward_approval_not_canonical_admission',
    priorityBand: group.priorityBand,
    priorityScore: group.priorityScore,
    priorityReasons: group.priorityReasons,
    riskLevel: group.riskLevel,
    riskScore: group.riskScore,
    riskReasons: group.riskReasons,
    candidateCategory: group.candidateCategory,
    normalizedLabel: group.looseNormalizedLabel,
    nodeIds: group.nodeIds,
    nodes: group.nodes,
    sourceSnapshot,
    groupInputHash: hash(stableStringify(compactGroupForSnapshot(group))),
    candidateEdgeNeighborhoodHash: hash(stableStringify(groupEdges.map(compactEdgeForSnapshot).sort((a, b) => a.id.localeCompare(b.id)))),
    edgeSummary: {
      totalEdges: groupEdges.length,
      incoming,
      outgoing,
      topRelationTypes,
    },
    resourceLinkCount: group.resourceLinkCount,
    resourceLinkIds: [],
    existingDecisionStatus: group.status,
    existingDecisionIds: group.existingDecisions.map((decision) => decision.decisionId),
    alternateSafeDecisionTypes: ['NEEDS_HUMAN_REVIEW', 'DISAMBIGUATED_KEEP_SEPARATE', 'GOVERNED_DISAMBIGUATION', 'CANONICAL_LABEL_CLARIFICATION'],
    proposedRelationshipAdds: [],
    wouldAffectNodeIds: group.nodeIds,
    wouldAffectEdgeIds: groupEdges.map((edge) => edge.id),
    wouldAffectResourceLinkIds: [],
    selfLoopRisks: [],
    duplicateEdgeConsolidationRisks: [],
    rollbackCapabilityPreview: 'full',
    remediationNeeded: false,
    requiredReviewerRole: 'domain_steward',
    stewardDecisionStatus: 'pending',
    kimiAdvisoryOnly: true,
    mergeApplied: false,
    aliasApplied: false,
    redirectApplied: false,
    tombstoneApplied: false,
    productionGraphWritePerformed: false,
    resourceLinkRewritePerformed: false,
    admittedRelationshipWritten: false,
    ...p1PacketAdmissionMetadata(repoRoot, group),
    ...recommendation,
  };
  return attachP1PacketSignature({ ...packet, packetContentHash: p1PacketContentHash(packet) }, generatedAt);
}

function withP1PacketCustodyRebaseLineage(
  packet: CanonicalP1DecisionPacket,
  previous: CanonicalP1DecisionPacket | undefined,
  timestamp: string,
  reviewer: string,
): CanonicalP1DecisionPacket {
  if (!previous) return packet;
  const rebaseReason = 'post_steward_admission_snapshot_refresh';
  const base: CanonicalP1DecisionPacket = {
    ...packet,
    custodyRebasedAt: timestamp,
    custodyRebasedBy: reviewer,
    custodyRebaseReason: rebaseReason,
    previousPacketContentHash: previous.packetContentHash,
    previousSourceSnapshotHash: previous.sourceSnapshot?.snapshotHash,
    custodyRebaseHistory: [
      ...(previous.custodyRebaseHistory || []),
      {
        rebasedAt: timestamp,
        rebasedBy: reviewer,
        rebaseReason,
        fromPacketContentHash: previous.packetContentHash,
        fromSourceSnapshotHash: previous.sourceSnapshot?.snapshotHash,
        toSourceSnapshotHash: packet.sourceSnapshot?.snapshotHash,
      },
    ],
  };
  return attachP1PacketSignature({ ...base, packetContentHash: p1PacketContentHash(base) }, timestamp);
}

export function generateCanonicalP1DecisionPackets(
  repoRoot: string,
  groups: DuplicateCandidateGroup[],
  edges: GraphEdgeLike[],
  request: { limit?: number; reviewer?: string; dryRun?: boolean; apply?: boolean } = {},
  context: { nodes?: GraphNodeLike[]; resourceData?: ResourceLayerData } = {},
) {
  const generatedAt = nowIso();
  const packetRunId = `p1-packet-run-${generatedAt.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${request.reviewer || 'local-dev'}:${generatedAt}`)}`;
  const limit = Math.max(1, Math.min(50, Number(request.limit || 20) || 20));
  const sourceSnapshot = buildP1SourceSnapshot(repoRoot, groups, edges, context);
  const p1Groups = groups
    .filter((group) => group.priorityBand === 'P1')
    .sort((a, b) => b.priorityScore - a.priorityScore || b.edgeCount - a.edgeCount || a.looseNormalizedLabel.localeCompare(b.looseNormalizedLabel))
    .slice(0, limit);
  const existingByGroup = new Map(readCanonicalP1DecisionPackets(repoRoot).map((packet) => [packet.groupId, packet]));
  const packets = p1Groups.map((group) => p1PacketFor(repoRoot, group, edges, generatedAt, packetRunId, sourceSnapshot, existingByGroup.get(group.groupId)));
  const blockers: string[] = [];
  if (packets.some((packet) => packet.mergeSafety !== 'blocked_without_domain_review' && packet.recommendedDecisionType === 'MERGE_INTO_CANONICAL')) {
    blockers.push('P1 packet generation cannot recommend destructive merge');
  }
  if (request.dryRun || !request.apply || blockers.length) {
    return { dryRun: true, generatedAt, packets, blockers };
  }
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_p1_decision_packet_generation', [paths.p1DecisionPackets], () => {
    const previous = readCanonicalP1DecisionPackets(repoRoot);
    const groupIds = new Set(packets.map((packet) => packet.groupId));
    const next = [...previous.filter((packet) => !groupIds.has(packet.groupId)), ...packets]
      .sort((a, b) => a.priorityBand.localeCompare(b.priorityBand) || b.edgeSummary.totalEdges - a.edgeSummary.totalEdges || a.normalizedLabel.localeCompare(b.normalizedLabel));
    writeCanonicalP1DecisionPackets(repoRoot, next);
    return { packets, generatedAt };
  });
  return { ...result, manifest, blockers };
}

function p1PacketCandidateSemanticsUnchanged(previous: CanonicalP1DecisionPacket, current: CanonicalP1DecisionPacket) {
  return previous.groupId === current.groupId
    && previous.normalizedLabel === current.normalizedLabel
    && stableStringify([...(previous.nodeIds || [])].sort()) === stableStringify([...(current.nodeIds || [])].sort());
}

function carryForwardScopeForPacket(packet: CanonicalP1DecisionPacket): CanonicalP1PacketReviewCarryForwardScope {
  if (packet.packetAdmissionStatus === 'consumed_by_non_destructive_admission') return 'admission_overlay_applied';
  if (packet.packetAdmissionStatus === 'metadata_disambiguation_admitted') return 'metadata_only_disambiguation_applied';
  return 'custody_snapshot_refresh_only';
}

function carryForwardP1PacketReview(
  review: CanonicalP1PacketOntologyReview,
  previousPacket: CanonicalP1DecisionPacket,
  currentPacket: CanonicalP1DecisionPacket,
  timestamp: string,
): CanonicalP1PacketOntologyReview {
  const scope = carryForwardScopeForPacket(currentPacket);
  const reason = scope === 'admission_overlay_applied'
    ? 'P1 packet custody snapshot refreshed after steward-approved non-destructive relationship admission; candidate node set and advisory review semantics remain unchanged.'
    : scope === 'metadata_only_disambiguation_applied'
      ? 'P1 packet custody snapshot refreshed after steward-approved metadata-only disambiguation admission; candidate node set and advisory review semantics remain unchanged.'
      : 'P1 packet custody snapshot refreshed against current graph/canonical state; candidate node set and advisory review semantics remain unchanged.';
  const event: CanonicalP1PacketReviewEvent = {
    eventId: reviewEventIdFor(review.packetId, timestamp, 'carried_forward'),
    eventType: 'carried_forward',
    ontologyReviewStatus: review.ontologyReviewStatus,
    reviewedBy: review.reviewedBy,
    reviewerType: review.reviewerType,
    source: review.source,
    createdAt: timestamp,
    reviewSummary: 'Historical review carried forward after packet custody rebase; Kimi/human review was not rerun.',
    nextAction: review.nextAction,
  };
  return {
    ...review,
    carriedForwardFromPacketContentHash: review.packetContentHash || previousPacket.packetContentHash,
    carriedForwardFromSourceSnapshotHash: review.sourceSnapshotHash || previousPacket.sourceSnapshot?.snapshotHash,
    carriedForwardToPacketContentHash: currentPacket.packetContentHash,
    carriedForwardToSourceSnapshotHash: currentPacket.sourceSnapshot?.snapshotHash,
    carriedForwardAt: timestamp,
    carriedForwardReason: reason,
    carryForwardScope: scope,
    carryForwardCaveat: 'Existing ontology review was not rerun; this is a custody snapshot rebase, not a new Kimi or human review and not approval authority.',
    updatedAt: timestamp,
    reviewHistory: [...(review.reviewHistory || []), event],
  };
}

export function rebaseCanonicalP1DecisionPackets(
  repoRoot: string,
  groups: DuplicateCandidateGroup[],
  edges: GraphEdgeLike[],
  request: { limit?: number; reviewer?: string; dryRun?: boolean; apply?: boolean } = {},
  context: { nodes?: GraphNodeLike[]; resourceData?: ResourceLayerData } = {},
) {
  const generatedAt = nowIso();
  const packetRunId = `p1-packet-rebase-${generatedAt.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${request.reviewer || 'local-dev'}:${generatedAt}`)}`;
  const previousPackets = readCanonicalP1DecisionPackets(repoRoot);
  const previousByGroup = new Map(previousPackets.map((packet) => [packet.groupId, packet]));
  const previousByPacketId = new Map(previousPackets.map((packet) => [packet.packetId, packet]));
  const previousReviews = readCanonicalP1PacketReviews(repoRoot);
  const limit = Math.max(1, Math.min(50, Number(request.limit || previousPackets.length || 20) || 20));
  const sourceSnapshot = buildP1SourceSnapshot(repoRoot, groups, edges, context);
  const p1Groups = groups
    .filter((group) => group.priorityBand === 'P1')
    .sort((a, b) => b.priorityScore - a.priorityScore || b.edgeCount - a.edgeCount || a.looseNormalizedLabel.localeCompare(b.looseNormalizedLabel))
    .slice(0, limit);
  const reviewer = request.reviewer || 'local-dev';
  const refreshedPackets = p1Groups.map((group) => {
    const previous = previousByGroup.get(group.groupId);
    return withP1PacketCustodyRebaseLineage(
      p1PacketFor(repoRoot, group, edges, generatedAt, packetRunId, sourceSnapshot, previous),
      previous,
      generatedAt,
      reviewer,
    );
  });
  const refreshedByPacketId = new Map(refreshedPackets.map((packet) => [packet.packetId, packet]));
  const carriedForwardReviews: CanonicalP1PacketOntologyReview[] = [];
  const staleReviewIds: string[] = [];
  for (const review of previousReviews) {
    const currentPacket = refreshedByPacketId.get(review.packetId);
    const previousPacket = previousByPacketId.get(review.packetId);
    if (currentPacket && previousPacket && p1PacketCandidateSemanticsUnchanged(previousPacket, currentPacket)) {
      carriedForwardReviews.push(carryForwardP1PacketReview(review, previousPacket, currentPacket, generatedAt));
    } else {
      staleReviewIds.push(review.reviewId);
      carriedForwardReviews.push(review);
    }
  }
  const groupIds = new Set(refreshedPackets.map((packet) => packet.groupId));
  const nextPackets = [...previousPackets.filter((packet) => !groupIds.has(packet.groupId)), ...refreshedPackets]
    .sort((a, b) => a.priorityBand.localeCompare(b.priorityBand) || b.edgeSummary.totalEdges - a.edgeSummary.totalEdges || a.normalizedLabel.localeCompare(b.normalizedLabel));
  const nextReviews = carriedForwardReviews
    .sort((a, b) => a.packetId.localeCompare(b.packetId) || a.reviewId.localeCompare(b.reviewId));
  const packetsChanged = refreshedPackets.filter((packet) => {
    const previous = previousByPacketId.get(packet.packetId);
    return !previous
      || previous.packetContentHash !== packet.packetContentHash
      || previous.sourceSnapshot?.snapshotHash !== packet.sourceSnapshot?.snapshotHash
      || previous.groupInputHash !== packet.groupInputHash
      || previous.candidateEdgeNeighborhoodHash !== packet.candidateEdgeNeighborhoodHash;
  });
  const carriedForwardReviewIds = carriedForwardReviews
    .filter((review) => Boolean(review.carriedForwardToPacketContentHash))
    .map((review) => review.reviewId);
  const consumedPackets = refreshedPackets.filter((packet) => packet.packetAdmissionStatus && packet.packetAdmissionStatus !== 'not_admitted');
  const result = {
    dryRun: true,
    generatedAt,
    packetRunId,
    packets: refreshedPackets,
    packetsRefreshed: refreshedPackets.length,
    packetsChanged: packetsChanged.length,
    reviewsPreserved: previousReviews.length,
    reviewsCarriedForward: carriedForwardReviewIds.length,
    carriedForwardReviewIds,
    staleReviewIds,
    consumedPackets: consumedPackets.map((packet) => ({
      packetId: packet.packetId,
      groupId: packet.groupId,
      packetAdmissionStatus: packet.packetAdmissionStatus,
      approvalIds: packet.approvalIds || [],
      admittedRelationshipIds: packet.admittedRelationshipIds || [],
      admittedDecisionIds: packet.admittedDecisionIds || [],
    })),
    blockers: staleReviewIds.map((reviewId) => `P1 packet review ${reviewId} could not be carried forward because the candidate packet is missing or semantically changed`),
    warnings: staleReviewIds.length ? ['Some P1 reviews were preserved as historical only and remain stale pending fresh review.'] : [],
  };
  if (request.dryRun || !request.apply || result.blockers.length) return result;
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result: applied, manifest } = withCanonicalTransaction(repoRoot, 'canonical_p1_decision_packet_snapshot_rebase', [paths.p1DecisionPackets, paths.p1PacketReviews], () => {
    writeCanonicalP1DecisionPackets(repoRoot, nextPackets);
    writeCanonicalP1PacketReviews(repoRoot, nextReviews);
    return { ...result, dryRun: false };
  });
  return { ...applied, manifest };
}

export function listCanonicalP1DecisionPackets(repoRoot: string) {
  return readCanonicalP1DecisionPackets(repoRoot);
}

const P1_PACKET_REVIEW_CAVEAT = 'Ontology packet review is advisory only and does not approve graph mutation, merge, alias, redirect, tombstone, source truth, or canonical admission.';
const P1_ONTOLOGY_REVIEW_STATUSES = new Set<CanonicalP1OntologyReviewStatus>(['unreviewed', 'kimi_review_requested', 'kimi_reviewed', 'human_review_needed', 'human_reviewed', 'rejected', 'deferred']);
const P1_ONTOLOGY_REVIEWER_TYPES = new Set<CanonicalP1OntologyReviewerType>(['kimi', 'human', 'codex', 'system']);
const P1_ONTOLOGY_REVIEW_SOURCES = new Set<CanonicalP1OntologyReviewSource>(['kimi', 'manual_entry', 'imported_review', 'test_fixture']);
const P1_ONTOLOGY_REVIEW_RISK_LEVELS = new Set<CanonicalP1OntologyReviewRiskLevel>(['low', 'medium', 'high', 'blocked']);

function requireP1PacketOntologyReviews() {
  return String(process.env.VITRUVIUS_REQUIRE_P1_PACKET_REVIEWS || '').toLowerCase() === 'true';
}

function reviewIdForPacket(packetId: string) {
  return `p1-packet-review-${shortHash(packetId)}`;
}

function reviewEventIdFor(packetId: string, timestamp: string, status: string) {
  return `p1-packet-review-event-${timestamp.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${packetId}:${status}:${timestamp}`)}`;
}

function normalizeReviewSuggestionList(value: string[] | string | undefined): string[] {
  if (Array.isArray(value)) return value.map((item) => String(item).trim()).filter(Boolean);
  if (typeof value === 'string') return value.split(/\r?\n|;/).map((item) => item.trim()).filter(Boolean);
  return [];
}

function defaultReviewRiskLevel(packet: CanonicalP1DecisionPacket, requested?: CanonicalP1OntologyReviewRiskLevel): CanonicalP1OntologyReviewRiskLevel {
  if (requested && P1_ONTOLOGY_REVIEW_RISK_LEVELS.has(requested)) return requested;
  if (packet.riskLevel === 'critical') return 'blocked';
  if (packet.riskLevel === 'high') return 'high';
  if (packet.riskLevel === 'medium') return 'medium';
  return 'low';
}

function latestReviewForPacket(packetId: string, reviews: CanonicalP1PacketOntologyReview[]) {
  return reviews
    .filter((review) => review.packetId === packetId)
    .sort((a, b) => (b.updatedAt || b.reviewedAt || b.createdAt).localeCompare(a.updatedAt || a.reviewedAt || a.createdAt))[0];
}

function containsReviewApprovalClaim(review: Partial<CanonicalP1PacketOntologyReview>) {
  const text = [review.reviewSummary, review.recommendedAction, review.nextAction, review.notes].filter(Boolean).join(' ').toLowerCase();
  return /steward\s+approved|approved\s+(merge|mutation|admission|alias|redirect|tombstone|edge)|approve\s+(merge|mutation|admission|alias|redirect|tombstone|edge)|admit\s+(edge|relationship|mutation)|apply\s+(merge|alias|redirect|tombstone)/i.test(text);
}

function buildCanonicalP1PacketReview(
  packet: CanonicalP1DecisionPacket,
  request: CanonicalP1PacketReviewRequest,
  existing: CanonicalP1PacketOntologyReview | undefined,
  timestamp = nowIso(),
): CanonicalP1PacketOntologyReview {
  const status = request.ontologyReviewStatus || existing?.ontologyReviewStatus || 'human_review_needed';
  const source = request.source || existing?.source || (request.reviewerType === 'kimi' ? 'kimi' : 'manual_entry');
  const reviewerType = request.reviewerType || existing?.reviewerType || (source === 'kimi' ? 'kimi' : 'human');
  const reviewedBy = (request.reviewedBy || existing?.reviewedBy || '').trim();
  const reviewSummary = (request.reviewSummary || existing?.reviewSummary || '').trim();
  const nextAction = (request.nextAction || existing?.nextAction || '').trim();
  const review: CanonicalP1PacketOntologyReview = {
    reviewId: existing?.reviewId || reviewIdForPacket(packet.packetId),
    packetId: packet.packetId,
    groupId: packet.groupId,
    packetContentHash: packet.packetContentHash,
    sourceSnapshotHash: packet.sourceSnapshot?.snapshotHash,
    ontologyReviewStatus: status,
    reviewerType,
    reviewedBy,
    reviewedAt: timestamp,
    reviewSummary,
    acceptedSuggestions: normalizeReviewSuggestionList(request.acceptedSuggestions ?? existing?.acceptedSuggestions),
    rejectedSuggestions: normalizeReviewSuggestionList(request.rejectedSuggestions ?? existing?.rejectedSuggestions),
    deferredSuggestions: normalizeReviewSuggestionList(request.deferredSuggestions ?? existing?.deferredSuggestions),
    recommendedAction: (request.recommendedAction || existing?.recommendedAction || '').trim() || undefined,
    reviewRiskLevel: defaultReviewRiskLevel(packet, request.reviewRiskLevel || existing?.reviewRiskLevel),
    nextAction: nextAction || undefined,
    notes: (request.notes || existing?.notes || '').trim() || undefined,
    source,
    reviewCaveat: P1_PACKET_REVIEW_CAVEAT,
    mutationScope: 'review_metadata_only',
    graphMutationApplied: false,
    advisoryOnly: true,
    createdAt: existing?.createdAt || timestamp,
    updatedAt: timestamp,
    reviewHistory: [
      ...(existing?.reviewHistory || []),
      {
        eventId: reviewEventIdFor(packet.packetId, timestamp, status),
        eventType: existing ? 'updated' : 'created',
        ontologyReviewStatus: status,
        reviewedBy,
        reviewerType,
        source,
        createdAt: timestamp,
        reviewSummary: reviewSummary || undefined,
        nextAction: nextAction || undefined,
      },
    ],
  };
  return review;
}

function p1ReviewCoversCurrentPacket(review: CanonicalP1PacketOntologyReview, packet: CanonicalP1DecisionPacket) {
  const directPacketHashMatches = !review.packetContentHash || !packet.packetContentHash || review.packetContentHash === packet.packetContentHash;
  const directSnapshotHashMatches = !review.sourceSnapshotHash || !packet.sourceSnapshot?.snapshotHash || review.sourceSnapshotHash === packet.sourceSnapshot.snapshotHash;
  if (directPacketHashMatches && directSnapshotHashMatches) {
    return { current: true, carriedForward: false, stale: false, blockers: [] as string[], warnings: [] as string[] };
  }
  const carriedPacketHashMatches = Boolean(review.carriedForwardToPacketContentHash && packet.packetContentHash && review.carriedForwardToPacketContentHash === packet.packetContentHash);
  const carriedSnapshotHashMatches = Boolean(review.carriedForwardToSourceSnapshotHash && packet.sourceSnapshot?.snapshotHash && review.carriedForwardToSourceSnapshotHash === packet.sourceSnapshot.snapshotHash);
  const blockers: string[] = [];
  const warnings: string[] = [];
  if (review.carriedForwardToPacketContentHash || review.carriedForwardToSourceSnapshotHash) {
    if (!carriedPacketHashMatches) blockers.push(`P1 packet review ${review.reviewId} carried-forward packetContentHash does not match current packet`);
    if (!carriedSnapshotHashMatches) blockers.push(`P1 packet review ${review.reviewId} carried-forward sourceSnapshotHash does not match current packet`);
    if (!review.carriedForwardReason?.trim()) warnings.push(`P1 packet review ${review.reviewId} missing carried-forward reason`);
    if (!review.carryForwardCaveat?.trim()) warnings.push(`P1 packet review ${review.reviewId} missing carried-forward caveat`);
    return { current: blockers.length === 0, carriedForward: blockers.length === 0, stale: blockers.length > 0, blockers, warnings };
  }
  return { current: false, carriedForward: false, stale: true, blockers, warnings };
}

function validateP1PacketReviewRecord(review: CanonicalP1PacketOntologyReview, packet?: CanonicalP1DecisionPacket) {
  const blockers: string[] = [];
  const warnings: string[] = [];
  if (!P1_ONTOLOGY_REVIEW_STATUSES.has(review.ontologyReviewStatus)) blockers.push(`unsupported ontologyReviewStatus: ${String(review.ontologyReviewStatus)}`);
  if (!P1_ONTOLOGY_REVIEWER_TYPES.has(review.reviewerType)) blockers.push(`unsupported reviewerType: ${String(review.reviewerType)}`);
  if (!P1_ONTOLOGY_REVIEW_SOURCES.has(review.source)) blockers.push(`unsupported source: ${String(review.source)}`);
  if (!P1_ONTOLOGY_REVIEW_RISK_LEVELS.has(review.reviewRiskLevel)) blockers.push(`unsupported reviewRiskLevel: ${String(review.reviewRiskLevel)}`);
  if (!review.packetId?.trim()) blockers.push('review missing packetId');
  if (!review.groupId?.trim()) blockers.push(`review ${review.reviewId || review.packetId} missing groupId`);
  if (!packet) {
    blockers.push(`P1 packet review ${review.reviewId || review.packetId} references missing packet ${review.packetId}`);
  } else {
    if (review.groupId !== packet.groupId) blockers.push(`P1 packet review ${review.reviewId} groupId does not match packet ${packet.packetId}`);
    const coverage = p1ReviewCoversCurrentPacket(review, packet);
    blockers.push(...coverage.blockers);
    warnings.push(...coverage.warnings);
    if (coverage.stale && !coverage.blockers.length) {
      if (review.packetContentHash && packet.packetContentHash && review.packetContentHash !== packet.packetContentHash) warnings.push(`P1 packet review ${review.reviewId} references stale packetContentHash`);
      if (review.sourceSnapshotHash && packet.sourceSnapshot?.snapshotHash && review.sourceSnapshotHash !== packet.sourceSnapshot.snapshotHash) warnings.push(`P1 packet review ${review.reviewId} references stale sourceSnapshotHash`);
    }
  }
  const requiresReviewer = ['kimi_reviewed', 'human_review_needed', 'human_reviewed', 'rejected', 'deferred', 'kimi_review_requested'].includes(review.ontologyReviewStatus);
  if (requiresReviewer && !review.reviewedBy?.trim()) blockers.push(`P1 packet review ${review.reviewId} missing reviewedBy`);
  if ((review.ontologyReviewStatus === 'kimi_reviewed' || review.ontologyReviewStatus === 'human_reviewed' || review.ontologyReviewStatus === 'rejected') && !review.reviewSummary?.trim()) blockers.push(`P1 packet review ${review.reviewId} missing reviewSummary`);
  if (review.ontologyReviewStatus === 'kimi_reviewed' && review.reviewerType !== 'kimi' && review.source !== 'kimi') blockers.push(`P1 packet review ${review.reviewId} status kimi_reviewed requires reviewerType/source kimi`);
  if (review.ontologyReviewStatus === 'human_review_needed' && !review.nextAction?.trim()) blockers.push(`P1 packet review ${review.reviewId} human_review_needed requires nextAction`);
  if (review.ontologyReviewStatus === 'deferred' && !review.nextAction?.trim() && !review.notes?.trim() && !review.reviewSummary?.trim()) blockers.push(`P1 packet review ${review.reviewId} deferred requires nextAction, notes, or reviewSummary`);
  if (!Array.isArray(review.acceptedSuggestions) || !Array.isArray(review.rejectedSuggestions) || !Array.isArray(review.deferredSuggestions)) blockers.push(`P1 packet review ${review.reviewId} suggestions must be arrays`);
  if (review.mutationScope !== 'review_metadata_only' || review.graphMutationApplied !== false || review.advisoryOnly !== true) blockers.push(`P1 packet review ${review.reviewId} must be advisory review_metadata_only with graphMutationApplied=false`);
  if (containsReviewApprovalClaim(review)) blockers.push(`P1 packet review ${review.reviewId} appears to claim graph mutation approval; use separate stewardship approval workflow`);
  if (review.reviewCaveat !== P1_PACKET_REVIEW_CAVEAT) warnings.push(`P1 packet review ${review.reviewId} missing standard advisory caveat`);
  if (!Array.isArray(review.reviewHistory) || review.reviewHistory.length === 0) warnings.push(`P1 packet review ${review.reviewId} missing reviewHistory`);
  return { blockers, warnings };
}

function p1ReviewTransactionManifestCount(repoRoot: string) {
  const dir = canonicalStewardshipPaths(repoRoot).transactionsDir;
  try {
    return readdirSync(dir)
      .filter((name) => name.endsWith('.json'))
      .map((name) => readJson(join(dir, name), {}))
      .filter((manifest) => manifest.operationType === 'canonical_p1_packet_ontology_review')
      .length;
  } catch {
    return 0;
  }
}

function p1PacketReviewMetrics(repoRoot: string, packets: CanonicalP1DecisionPacket[]) {
  const reviews = readCanonicalP1PacketReviews(repoRoot);
  const packetById = new Map(packets.map((packet) => [packet.packetId, packet]));
  const latestByPacket = new Map<string, CanonicalP1PacketOntologyReview>();
  for (const packet of packets) {
    const latest = latestReviewForPacket(packet.packetId, reviews);
    if (latest) latestByPacket.set(packet.packetId, latest);
  }
  let p1PacketReviewInvalid = 0;
  let p1PacketReviewMissingReviewer = 0;
  let p1PacketReviewMissingSummary = 0;
  let p1PacketReviewMissingNextAction = 0;
  let p1PacketReviewHashMismatch = 0;
  let p1PacketReviewReferencesMissingPacket = 0;
  let p1PacketReviewStale = 0;
  let p1PacketReviewsCarriedForward = 0;
  const blockers: string[] = [];
  const warnings: string[] = [];
  for (const review of reviews) {
    const packet = packetById.get(review.packetId);
    const result = validateP1PacketReviewRecord(review, packet);
    blockers.push(...result.blockers);
    warnings.push(...result.warnings);
    if (result.blockers.length) p1PacketReviewInvalid += 1;
    if (!packet) p1PacketReviewReferencesMissingPacket += 1;
    if (!review.reviewedBy?.trim()) p1PacketReviewMissingReviewer += 1;
    if ((review.ontologyReviewStatus === 'kimi_reviewed' || review.ontologyReviewStatus === 'human_reviewed' || review.ontologyReviewStatus === 'rejected') && !review.reviewSummary?.trim()) p1PacketReviewMissingSummary += 1;
    if ((review.ontologyReviewStatus === 'human_review_needed' || review.ontologyReviewStatus === 'deferred') && !review.nextAction?.trim()) p1PacketReviewMissingNextAction += 1;
    const coverage = packet ? p1ReviewCoversCurrentPacket(review, packet) : undefined;
    if (coverage?.carriedForward) p1PacketReviewsCarriedForward += 1;
    if (packet && coverage?.stale) {
      p1PacketReviewHashMismatch += 1;
      p1PacketReviewStale += 1;
    }
  }
  const statusCounts = countsBy(packets.map((packet) => latestByPacket.get(packet.packetId)?.ontologyReviewStatus || 'unreviewed'));
  if (requireP1PacketOntologyReviews()) {
    const unreviewed = packets.filter((packet) => !latestByPacket.has(packet.packetId));
    for (const packet of unreviewed) blockers.push(`P1 packet ${packet.packetId} is unreviewed while VITRUVIUS_REQUIRE_P1_PACKET_REVIEWS=true`);
    for (const review of reviews) {
      const packet = packetById.get(review.packetId);
      if (packet && p1ReviewCoversCurrentPacket(review, packet).stale) {
        blockers.push(`P1 packet review ${review.reviewId} is stale while strict P1 packet review mode is enabled`);
      }
    }
  } else {
    const unreviewedCount = packets.length - latestByPacket.size;
    if (unreviewedCount) warnings.push(`${unreviewedCount} P1 decision packets are unreviewed; this is advisory backlog, not a validation blocker`);
  }
  return {
    reviews,
    latestByPacket,
    p1PacketsWithOntologyReview: latestByPacket.size,
    p1PacketsUnreviewed: statusCounts.unreviewed || 0,
    p1PacketsKimiReviewRequested: statusCounts.kimi_review_requested || 0,
    p1PacketsKimiReviewed: statusCounts.kimi_reviewed || 0,
    p1PacketsHumanReviewNeeded: statusCounts.human_review_needed || 0,
    p1PacketsHumanReviewed: statusCounts.human_reviewed || 0,
    p1PacketsRejected: statusCounts.rejected || 0,
    p1PacketsDeferred: statusCounts.deferred || 0,
    p1PacketReviewInvalid,
    p1PacketReviewMissingReviewer,
    p1PacketReviewMissingSummary,
    p1PacketReviewMissingNextAction,
    p1PacketReviewHashMismatch,
    p1PacketReviewReferencesMissingPacket,
    p1PacketReviewStale,
    p1PacketReviewsCarriedForward,
    p1PacketsConsumedByAdmission: packets.filter((packet) => packet.packetAdmissionStatus && packet.packetAdmissionStatus !== 'not_admitted').length,
    p1PacketsCarriedForward: Array.from(latestByPacket.values()).filter((review) => Boolean(review.carriedForwardToPacketContentHash)).length,
    p1PacketReviewDoesNotMutateGraph: reviews.every((review) => review.mutationScope === 'review_metadata_only' && review.graphMutationApplied === false),
    p1PacketReviewTransactionManifests: p1ReviewTransactionManifestCount(repoRoot),
    p1PacketReviewStrictMode: requireP1PacketOntologyReviews(),
    p1PacketReviewWarnings: warnings,
    p1PacketReviewBlockers: blockers,
  };
}

function enrichP1PacketWithReview(packet: CanonicalP1DecisionPacket, reviews: CanonicalP1PacketOntologyReview[]) {
  const latest = latestReviewForPacket(packet.packetId, reviews);
  const history = reviews
    .filter((review) => review.packetId === packet.packetId)
    .flatMap((review) => review.reviewHistory || [])
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt));
  return {
    ...packet,
    ontologyReviewStatus: latest?.ontologyReviewStatus || 'unreviewed',
    ontologyReview: latest,
    reviewHistory: history,
  };
}

export function listCanonicalP1PacketReviews(repoRoot: string) {
  return readCanonicalP1PacketReviews(repoRoot);
}

export function listCanonicalP1PacketsWithReviews(repoRoot: string, filters: Record<string, string | boolean | number | undefined> = {}) {
  const reviews = readCanonicalP1PacketReviews(repoRoot);
  let packets = readCanonicalP1DecisionPackets(repoRoot).map((packet) => enrichP1PacketWithReview(packet, reviews));
  const status = typeof filters.ontologyReviewStatus === 'string' ? filters.ontologyReviewStatus : '';
  const risk = typeof filters.reviewRiskLevel === 'string' ? filters.reviewRiskLevel : '';
  const groupId = typeof filters.groupId === 'string' ? filters.groupId : '';
  const query = typeof filters.query === 'string' ? filters.query.toLowerCase().trim() : '';
  if (status) packets = packets.filter((packet) => packet.ontologyReviewStatus === status);
  if (risk) packets = packets.filter((packet) => packet.ontologyReview?.reviewRiskLevel === risk || (!packet.ontologyReview && risk === packet.riskLevel));
  if (groupId) packets = packets.filter((packet) => packet.groupId === groupId);
  if (filters.needsKimiReview === true || filters.needsKimiReview === 'true') packets = packets.filter((packet) => packet.needsKimiReview || packet.ontologyReviewStatus === 'kimi_review_requested');
  if (filters.needsHumanReview === true || filters.needsHumanReview === 'true') packets = packets.filter((packet) => packet.needsHumanDomainReview || packet.ontologyReviewStatus === 'human_review_needed');
  if (filters.reviewed === true || filters.reviewed === 'true') packets = packets.filter((packet) => packet.ontologyReviewStatus !== 'unreviewed');
  if (filters.unreviewed === true || filters.unreviewed === 'true') packets = packets.filter((packet) => packet.ontologyReviewStatus === 'unreviewed');
  if (query) packets = packets.filter((packet) => (
    packet.packetId.toLowerCase().includes(query)
    || packet.groupId.toLowerCase().includes(query)
    || packet.normalizedLabel.toLowerCase().includes(query)
    || packet.nodeIds.some((nodeId) => nodeId.toLowerCase().includes(query))
  ));
  return packets;
}

export function getCanonicalP1PacketDetail(repoRoot: string, packetId: string) {
  const packet = listCanonicalP1PacketsWithReviews(repoRoot).find((entry) => entry.packetId === packetId);
  if (!packet) return null;
  return {
    packet,
    reviewHistory: packet.reviewHistory || [],
    custody: {
      packetContentHash: packet.packetContentHash,
      sourceSnapshotHash: packet.sourceSnapshot?.snapshotHash,
      groupInputHash: packet.groupInputHash,
      candidateEdgeNeighborhoodHash: packet.candidateEdgeNeighborhoodHash,
      signatureStatus: packet.signature?.signatureStatus || 'unsigned',
      signaturePayloadHash: packet.signature?.signaturePayloadHash,
      truthCaveat: packet.truthCaveat,
    },
    mutationScope: 'read_only_packet_detail',
  };
}

export function previewCanonicalP1PacketReview(repoRoot: string, packetId: string, request: CanonicalP1PacketReviewRequest) {
  const packets = readCanonicalP1DecisionPackets(repoRoot);
  const packet = packets.find((entry) => entry.packetId === packetId);
  if (!packet) return { dryRun: true, blockers: [`P1 decision packet not found: ${packetId}`], warnings: [] };
  const reviews = readCanonicalP1PacketReviews(repoRoot);
  const existing = latestReviewForPacket(packetId, reviews);
  const proposed = buildCanonicalP1PacketReview(packet, request, existing);
  const validation = validateP1PacketReviewRecord(proposed, packet);
  const paths = canonicalStewardshipPaths(repoRoot);
  return {
    dryRun: true,
    packetId,
    groupId: packet.groupId,
    beforeReview: existing || { ontologyReviewStatus: 'unreviewed' },
    afterReview: proposed,
    diff: {
      ontologyReviewStatus: { before: existing?.ontologyReviewStatus || 'unreviewed', after: proposed.ontologyReviewStatus },
      reviewRiskLevel: { before: existing?.reviewRiskLevel, after: proposed.reviewRiskLevel },
      nextAction: { before: existing?.nextAction, after: proposed.nextAction },
      reviewSummaryChanged: (existing?.reviewSummary || '') !== proposed.reviewSummary,
    },
    custody: {
      packetContentHash: packet.packetContentHash,
      sourceSnapshotHash: packet.sourceSnapshot?.snapshotHash,
      packetContentHashStillValid: !packet.packetContentHash || p1PacketContentHash(packet) === packet.packetContentHash,
      sourceSnapshotHashStillValid: !packet.sourceSnapshot || p1SourceSnapshotHash(packet.sourceSnapshot) === packet.sourceSnapshot.snapshotHash,
    },
    mutationScope: 'p1_packet_review_metadata_only',
    graphMutation: false,
    aliasesRedirectsTombstonesMutation: false,
    resourceLayerMutation: false,
    transactionManifestPreview: {
      operationType: 'canonical_p1_packet_ontology_review',
      filesTouched: [relative(repoRoot, paths.p1PacketReviews)],
    },
    blockers: validation.blockers,
    warnings: validation.warnings,
  };
}

export function recordCanonicalP1PacketReview(repoRoot: string, packetId: string, request: CanonicalP1PacketReviewRequest) {
  const preview = previewCanonicalP1PacketReview(repoRoot, packetId, request);
  if (request.dryRun || !request.apply || preview.blockers.length) return preview;
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_p1_packet_ontology_review', [paths.p1PacketReviews], () => {
    const existingReviews = readCanonicalP1PacketReviews(repoRoot);
    const nextReview = preview.afterReview as CanonicalP1PacketOntologyReview;
    const next = [
      ...existingReviews.filter((review) => review.reviewId !== nextReview.reviewId),
      nextReview,
    ].sort((a, b) => a.packetId.localeCompare(b.packetId) || a.reviewId.localeCompare(b.reviewId));
    writeCanonicalP1PacketReviews(repoRoot, next);
    return { review: nextReview, preview };
  });
  return { ...result, manifest };
}

function disambiguationLabelFor(node: Pick<DuplicateCandidateNodeSummary, 'label' | 'type' | 'taxonomyPath'>) {
  const path = node.taxonomyPath.length ? node.taxonomyPath.join(' > ') : node.type || 'untyped';
  return `${node.label} (${path})`;
}

function defaultSearchDisambiguationText(group: DuplicateCandidateGroup) {
  return `${group.looseNormalizedLabel} remains a governed duplicate-review group; compare taxonomy context before treating these nodes as the same concept.`;
}

function domainRoot(node: Pick<DuplicateCandidateNodeSummary, 'taxonomyPath'>) {
  return node.taxonomyPath[0] || '';
}

function proposalIdFor(sourceNodeId: string, targetNodeId: string, relationType: string) {
  return `stewardship-edge-proposal-${shortHash(`${sourceNodeId}:${relationType}:${targetNodeId}`)}`;
}

function buildDefaultRelationshipProposals(
  group: DuplicateCandidateGroup,
  decisionType: CanonicalDecisionType,
  timestamp: string,
  request?: Pick<CanonicalDecisionRequest, 'proposedRelationshipAdds' | 'rationale'>,
): CanonicalStewardshipRelationshipProposal[] {
  if (request?.proposedRelationshipAdds?.length) return request.proposedRelationshipAdds;
  if (!DISAMBIGUATION_DECISION_TYPES.has(decisionType) || group.nodes.length !== 2) return [];

  const [left, right] = group.nodes;
  const leftRoot = domainRoot(left);
  const rightRoot = domainRoot(right);
  const rationale = request?.rationale?.trim() || 'Governed disambiguation proposal; steward approval required before production graph edge admission.';
  const mk = (
    sourceNodeId: string,
    targetNodeId: string,
    relationType: CanonicalStewardshipRelationshipProposal['relationType'],
  ): CanonicalStewardshipRelationshipProposal => ({
    proposalId: proposalIdFor(sourceNodeId, targetNodeId, relationType),
    sourceNodeId,
    targetNodeId,
    relationType,
    category: 'semantic/stewardship-disambiguation',
    direction: relationType === 'CROSS_DOMAIN_EQUIVALENT' || relationType === 'CROSS_DOMAIN_ALIGNMENT' ? 'bidirectional' : 'outgoing',
    confidence: 'proposed',
    weight: 0.5,
    rationale,
    provenance: 'canonical stewardship review packet; not admitted as a production ontology edge until steward approval',
    stewardshipDecisionId: 'pending',
    createdAt: timestamp,
    reviewStatus: 'proposed',
  });

  if (decisionType === 'CROSS_DOMAIN_EQUIVALENCE') {
    return [
      mk(left.id, right.id, 'CROSS_DOMAIN_ALIGNMENT'),
      mk(right.id, left.id, 'CROSS_DOMAIN_ALIGNMENT'),
    ];
  }

  const materialNode = [left, right].find((node) => /^MAT\b/i.test(domainRoot(node)));
  const structuralNode = [left, right].find((node) => /^STR\b/i.test(domainRoot(node)));
  if (materialNode && structuralNode) {
    return [mk(structuralNode.id, materialNode.id, 'RELATED_SPECIALIZATION_OF')];
  }
  if (leftRoot && rightRoot && leftRoot !== rightRoot) {
    return [
      mk(left.id, right.id, 'CROSS_DOMAIN_ALIGNMENT'),
      mk(right.id, left.id, 'CROSS_DOMAIN_ALIGNMENT'),
    ];
  }
  return [mk(left.id, right.id, 'DISAMBIGUATED_FROM'), mk(right.id, left.id, 'DISAMBIGUATED_FROM')];
}

function chooseCanonical(group: DuplicateCandidateGroup, request: CanonicalDecisionRequest) {
  if (request.canonicalNodeId) return request.canonicalNodeId;
  return group.nodes.slice().sort((a, b) => (
    (b.resourceLinkCount - a.resourceLinkCount)
    || ((b.incomingEdgeCount + b.outgoingEdgeCount) - (a.incomingEdgeCount + a.outgoingEdgeCount))
    || a.id.localeCompare(b.id)
  ))[0]?.id;
}

function validateDecisionRequest(group: DuplicateCandidateGroup, request: CanonicalDecisionRequest) {
  const blockers: string[] = [];
  if (!DECISION_TYPES.has(request.decisionType)) blockers.push(`unsupported decisionType: ${String(request.decisionType)}`);
  if (!request.reviewer?.trim()) blockers.push('reviewer is required');
  if (!request.rationale?.trim()) blockers.push('rationale is required');
  if ((request.decisionType === 'MERGE_INTO_CANONICAL' || request.decisionType === 'ALIAS_TO_CANONICAL') && !chooseCanonical(group, request)) blockers.push('canonicalNodeId is required for merge or alias decisions');
  if ((group.riskLevel === 'high' || group.riskLevel === 'critical') && request.apply && !request.highRiskAcknowledged) blockers.push('high-risk duplicate decision requires explicit highRiskAcknowledged before apply');
  if (request.decisionType === 'MERGE_INTO_CANONICAL' && group.riskLevel !== 'low' && request.apply) blockers.push('destructive merge apply is blocked for non-low-risk groups');
  for (const proposal of request.proposedRelationshipAdds || []) {
    if (!group.nodeIds.includes(proposal.sourceNodeId)) blockers.push(`proposed relationship source is outside duplicate group: ${proposal.sourceNodeId}`);
    if (!group.nodeIds.includes(proposal.targetNodeId)) blockers.push(`proposed relationship target is outside duplicate group: ${proposal.targetNodeId}`);
    if (proposal.sourceNodeId === proposal.targetNodeId) blockers.push(`proposed relationship self-loop is not allowed: ${proposal.sourceNodeId}`);
    if (!STEWARDSHIP_RELATIONSHIP_TYPES.has(proposal.relationType)) blockers.push(`unsupported proposed stewardship relation type: ${proposal.relationType}`);
  }
  return blockers;
}

export function previewCanonicalDecision(group: DuplicateCandidateGroup, request: CanonicalDecisionRequest, edges: GraphEdgeLike[], resourceLinks: NodeResourceLink[] = []) {
  const timestamp = nowIso();
  const canonicalNodeId = request.decisionType === 'MERGE_INTO_CANONICAL' || request.decisionType === 'ALIAS_TO_CANONICAL'
    ? chooseCanonical(group, request)
    : request.canonicalNodeId;
  const sourceNodeIds = (request.sourceNodeIds?.length ? request.sourceNodeIds : group.nodeIds.filter((id) => id !== canonicalNodeId)).filter((id) => group.nodeIds.includes(id));
  const affectedEdges = edges.filter((edge) => sourceNodeIds.includes(edge.source) || sourceNodeIds.includes(edge.target));
  const edgeRewrites = affectedEdges.map((edge) => ({
    edgeId: edge.id,
    fromSource: edge.source,
    fromTarget: edge.target,
    toSource: canonicalNodeId && sourceNodeIds.includes(edge.source) ? canonicalNodeId : edge.source,
    toTarget: canonicalNodeId && sourceNodeIds.includes(edge.target) ? canonicalNodeId : edge.target,
  }));
  const resourceLinkRewrites = resourceLinks.filter((link) => canonicalNodeId && sourceNodeIds.includes(link.nodeId)).map((link) => ({ linkId: link.id, fromNodeId: link.nodeId, toNodeId: canonicalNodeId! }));
  const affectedEdgeIds = new Set(affectedEdges.map((edge) => edge.id));
  const projectedKeys = new Map<string, string[]>();
  for (const edge of edges) {
    const toSource = canonicalNodeId && sourceNodeIds.includes(edge.source) ? canonicalNodeId : edge.source;
    const toTarget = canonicalNodeId && sourceNodeIds.includes(edge.target) ? canonicalNodeId : edge.target;
    const key = `${toSource}|${toTarget}|${edge.type}`;
    projectedKeys.set(key, [...(projectedKeys.get(key) || []), edge.id]);
  }
  const duplicateEdgeConsolidations = Array.from(projectedKeys.values())
    .filter((ids) => ids.length > 1 && ids.some((id) => affectedEdgeIds.has(id)))
    .flat();
  const selfLoopRisks = edgeRewrites.filter((rewrite) => rewrite.toSource === rewrite.toTarget).map((rewrite) => rewrite.edgeId);
  const affectedAliases = Array.from(new Set(group.nodes.flatMap((node) => [node.label, ...node.aliases]).map(normalizeCanonicalLabel).filter(Boolean))).sort();
  const proposedRelationshipAdds = buildDefaultRelationshipProposals(group, request.decisionType, timestamp, request);
  const searchDisambiguationText = request.searchDisambiguationText || defaultSearchDisambiguationText(group);
  const blockers = validateDecisionRequest(group, request);
  const warnings = [
    ...group.riskReasons,
    selfLoopRisks.length ? `${selfLoopRisks.length} edge rewrites would become self-loops` : '',
    duplicateEdgeConsolidations.length ? `${duplicateEdgeConsolidations.length} rewritten edge ids may consolidate into duplicate edges` : '',
    resourceLinkRewrites.length ? `${resourceLinkRewrites.length} Resource Layer node links would need redirect/preservation` : '',
  ].filter(Boolean);
  return {
    dryRun: true,
    decisionType: request.decisionType,
    candidateGroupId: group.groupId,
    canonicalNodeId,
    sourceNodeIds,
    affectedEdgeIds: affectedEdges.map((edge) => edge.id),
    affectedResourceLinkIds: resourceLinkRewrites.map((rewrite) => rewrite.linkId),
    affectedAliases,
    affectedSearchTerms: affectedAliases,
    affectedNodeIds: group.nodeIds,
    edgeRewrites,
    duplicateEdgeConsolidations,
    selfLoopRisks,
    resourceLinkRewrites,
    proposedRelationshipAdds,
    searchDisambiguationText,
    warnings,
    blockers,
    riskLevel: group.riskLevel,
    riskScore: group.riskScore,
    beforeSnapshot: {
      schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
      nodes: group.nodes,
      disambiguationLabels: group.nodes.map((node) => ({ nodeId: node.id, disambiguationLabel: disambiguationLabelFor(node) })),
      affectedEdgeIds: affectedEdges.map((edge) => edge.id),
      affectedResourceLinkIds: resourceLinkRewrites.map((rewrite) => rewrite.linkId),
    },
    afterPreview: {
      canonicalNodeId,
      sourceNodeIds,
      aliasesToAdd: affectedAliases,
      proposedRelationshipAdds,
      searchDisambiguationText,
      redirectsToCreate: request.decisionType === 'MERGE_INTO_CANONICAL'
        ? sourceNodeIds.map((sourceNodeId) => ({ sourceNodeId, canonicalNodeId }))
        : [],
    },
  };
}

function decisionIdFor(entry: Omit<CanonicalStewardshipDecision, 'decisionId'>, existing: CanonicalStewardshipDecision[]) {
  const base = `canonical-${entry.createdAt.replace(/\D/g, '').slice(0, 14)}-${shortHash(JSON.stringify(entry))}`;
  if (!existing.some((decision) => decision.decisionId === base)) return base;
  let suffix = 2;
  while (existing.some((decision) => decision.decisionId === `${base}-${suffix}`)) suffix += 1;
  return `${base}-${suffix}`;
}

export function recordCanonicalDecision(repoRoot: string, group: DuplicateCandidateGroup, request: CanonicalDecisionRequest, edges: GraphEdgeLike[], resourceLinks: NodeResourceLink[] = []) {
  const preview = previewCanonicalDecision(group, request, edges, resourceLinks);
  const redirectTarget = preview.canonicalNodeId
    ? readCanonicalRedirects(repoRoot).find((record) => record.sourceNodeId === preview.canonicalNodeId)
    : undefined;
  const blockers = [
    ...preview.blockers,
    redirectTarget ? `canonical target ${preview.canonicalNodeId} already redirects to ${redirectTarget.canonicalNodeId}; choose the terminal canonical node` : '',
    request.apply && DISAMBIGUATION_DECISION_TYPES.has(request.decisionType)
      ? `${request.decisionType} decisions require the steward approval/admission gate; record as proposed first, then approve/admit with approval metadata`
      : '',
  ].filter(Boolean);
  const apply = Boolean(request.apply) && !request.dryRun;
  if (blockers.length) return { dryRun: Boolean(request.dryRun), preview: { ...preview, blockers }, blockers };
  const timestamp = nowIso();
  const existing = readCanonicalDecisions(repoRoot);
  const entry: Omit<CanonicalStewardshipDecision, 'decisionId'> = {
    decisionType: request.decisionType,
    candidateGroupId: group.groupId,
    canonicalNodeId: preview.canonicalNodeId,
    sourceNodeIds: preview.sourceNodeIds,
    affectedEdgeIds: preview.affectedEdgeIds,
    affectedResourceLinkIds: preview.affectedResourceLinkIds,
    affectedAliases: preview.affectedAliases,
    affectedSearchTerms: preview.affectedSearchTerms,
    affectedNodeIds: preview.affectedNodeIds,
    reviewer: request.reviewer!.trim(),
    reviewedBy: request.reviewer!.trim(),
    createdAt: timestamp,
    rationale: request.rationale!.trim(),
    riskLevel: preview.riskLevel,
    beforeSnapshot: preview.beforeSnapshot,
    afterPreview: preview.afterPreview,
    appliedAt: apply ? timestamp : undefined,
    status: apply ? 'applied' : 'proposed',
    rollbackCapability: request.decisionType === 'MERGE_INTO_CANONICAL' && (preview.affectedEdgeIds.length || preview.affectedResourceLinkIds.length) ? 'partial' : 'full',
    validationResult: { blockers: [], warnings: preview.warnings },
    kimiReviewSummary: request.kimiReviewSummary,
    notes: request.notes,
    proposedRelationshipAdds: preview.proposedRelationshipAdds.map((proposal) => ({
      ...proposal,
      stewardshipDecisionId: 'pending',
    })),
    proposedRelationshipUpdates: [],
    proposedAliasAdds: [],
    proposedLabelChanges: DISAMBIGUATION_DECISION_TYPES.has(request.decisionType)
      ? group.nodes.map((node) => ({
        nodeId: node.id,
        fromLabel: node.label,
        toLabel: disambiguationLabelFor(node),
        displayOnly: true,
        rationale: 'Display-only clarification for duplicate-review disambiguation; canonical label and node id remain unchanged.',
      }))
      : [],
    proposedDescriptionChanges: [],
    searchDisambiguationText: preview.searchDisambiguationText,
  };
  const decisionId = decisionIdFor(entry, existing);
  const decision: CanonicalStewardshipDecision = {
    decisionId,
    ...entry,
    proposedRelationshipAdds: entry.proposedRelationshipAdds?.map((proposal) => ({
      ...proposal,
      stewardshipDecisionId: decisionId,
    })),
    afterPreview: {
      ...(typeof entry.afterPreview === 'object' && entry.afterPreview ? entry.afterPreview as Record<string, unknown> : {}),
      proposedRelationshipAdds: entry.proposedRelationshipAdds?.map((proposal) => ({
        ...proposal,
        stewardshipDecisionId: decisionId,
      })),
    },
  };
  if (request.dryRun) return { dryRun: true, preview, decision };
  const paths = canonicalStewardshipPaths(repoRoot);
  const files = apply ? [paths.decisions, paths.aliases, paths.redirects] : [paths.decisions];
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_stewardship_decision', files, () => {
    const decisions = [...existing, decision];
    const aliases = readCanonicalAliases(repoRoot);
    const redirects = readCanonicalRedirects(repoRoot);
    const nextAliases = [...aliases];
    const nextRedirects = [...redirects];
    if (apply && (decision.decisionType === 'ALIAS_TO_CANONICAL' || decision.decisionType === 'MERGE_INTO_CANONICAL') && decision.canonicalNodeId) {
      for (const alias of decision.affectedAliases) {
        if (!nextAliases.some((record) => record.normalizedAlias === alias && record.canonicalNodeId === decision.canonicalNodeId && record.decisionId === decision.decisionId)) {
          nextAliases.push({ alias, normalizedAlias: alias, canonicalNodeId: decision.canonicalNodeId, sourceNodeIds: decision.sourceNodeIds, decisionId: decision.decisionId, createdAt: timestamp, aliasType: 'search_alias', status: 'active', rationale: decision.rationale, reviewer: decision.reviewer, appliedAt: timestamp });
        }
      }
    }
    if (apply && decision.decisionType === 'MERGE_INTO_CANONICAL' && decision.canonicalNodeId) {
      for (const sourceNodeId of decision.sourceNodeIds) {
        if (!nextRedirects.some((record) => record.sourceNodeId === sourceNodeId)) {
          nextRedirects.push({ sourceNodeId, canonicalNodeId: decision.canonicalNodeId, decisionId: decision.decisionId, createdAt: timestamp, reason: decision.decisionType, redirectType: 'merged_into', status: 'active', appliedAt: timestamp, rollbackCapability: decision.rollbackCapability });
        }
      }
    }
    writeCanonicalDecisions(repoRoot, decisions);
    if (apply) {
      writeCanonicalAliases(repoRoot, nextAliases);
      writeCanonicalRedirects(repoRoot, nextRedirects);
    }
    return { decision, preview };
  });
  return { ...result, manifest };
}

export function previewCanonicalRollback(repoRoot: string, decisionId: string) {
  const decisions = readCanonicalDecisions(repoRoot);
  const decision = decisions.find((entry) => entry.decisionId === decisionId);
  if (!decision) return { blockers: ['canonical decision not found'] };
  const aliases = readCanonicalAliases(repoRoot).filter((alias) => alias.decisionId === decisionId);
  const redirects = readCanonicalRedirects(repoRoot).filter((redirect) => redirect.decisionId === decisionId);
  const tombstones = readCanonicalTombstones(repoRoot).filter((tombstone) => tombstone.decisionId === decisionId);
  const approvals = readCanonicalApprovals(repoRoot).filter((approval) => approval.decisionId === decisionId && approval.status !== 'rolled_back');
  const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot).filter((edge) => edge.stewardshipDecisionId === decisionId && edge.reviewStatus !== 'rolled_back');
  const warnings: string[] = [];
  let rollbackCapability: CanonicalRollbackCapability = 'full';
  if (decision.status === 'rolled_back' || decision.status === 'rollback_partial' || decision.status === 'rollback_blocked') rollbackCapability = 'blocked';
  if (decision.decisionType === 'MERGE_INTO_CANONICAL' && (decision.affectedEdgeIds.length || decision.affectedResourceLinkIds.length)) {
    rollbackCapability = 'partial';
    warnings.push('merge rollback is metadata-complete for aliases/redirects, but graph edge/resource-link rewrite rollback is only previewed because production edge records were not destructively rewritten by this service');
  }
  if (!['applied', 'proposed', 'steward_approved', 'admitted'].includes(decision.status)) {
    rollbackCapability = 'blocked';
    warnings.push(`decision status ${decision.status} is not rollbackable`);
  }
  const blockers = rollbackCapability === 'blocked' ? warnings.slice() : [];
  return {
    decisionId,
    decision,
    rollbackCapability,
    aliasesToRemove: aliases,
    redirectsToRemove: redirects,
    tombstonesToRemove: tombstones,
    approvalsToMarkRolledBack: approvals,
    admittedRelationshipsToRollBack: admittedRelationships,
    remediationPreview: rollbackCapability === 'partial' || rollbackCapability === 'blocked' ? {
      rollbackCapability,
      reason: rollbackCapability === 'partial' ? 'partial rollback needs manual confirmation that no edge/resource-link rewrite was dropped' : 'rollback is blocked by decision status',
      affectedNodes: decision.affectedNodeIds || decision.sourceNodeIds,
      affectedEdges: decision.affectedEdgeIds,
      affectedResourceLinks: decision.affectedResourceLinkIds,
      recommendedManualSteps: [
        'Review beforeSnapshot and afterPreview for edge/resource preservation.',
        'Confirm Resource Layer nodeResourceLinks remain attached to live nodes or redirected by policy.',
        'Run canonical, graph relationship, and resource validation after remediation.',
      ],
    } : undefined,
    beforeSnapshot: decision.beforeSnapshot,
    afterPreview: {
      decisionStatus: 'rolled_back',
      removeAliases: aliases.length,
      removeRedirects: redirects.length,
      removeTombstones: tombstones.length,
      markApprovalsRolledBack: approvals.length,
      markAdmittedRelationshipsRolledBack: admittedRelationships.length,
      graphNodeMutation: false,
      edgeEndpointMutation: false,
      resourceLinkMutation: false,
    },
    warnings,
    blockers,
  };
}

function remediationIdFor(decisionId: string, createdAt: string) {
  return `canonical-remediation-${createdAt.replace(/\D/g, '').slice(0, 14)}-${shortHash(decisionId)}`;
}

function createRollbackRemediationManifest(
  decision: CanonicalStewardshipDecision,
  preview: ReturnType<typeof previewCanonicalRollback> & { remediationPreview?: any },
  request: { reviewer?: string; rationale?: string },
  rollbackId?: string,
): CanonicalRemediationManifest {
  const createdAt = nowIso();
  return {
    remediationManifestId: remediationIdFor(decision.decisionId, createdAt),
    decisionId: decision.decisionId,
    rollbackId,
    rollbackCapability: (preview as any).rollbackCapability || 'partial',
    reason: request.rationale || 'Rollback requires remediation review.',
    affectedNodes: decision.affectedNodeIds || decision.sourceNodeIds,
    affectedEdges: decision.affectedEdgeIds,
    affectedResourceLinks: decision.affectedResourceLinkIds,
    affectedAliases: (preview as any).aliasesToRemove?.map((alias: CanonicalAliasRecord) => alias.alias) || [],
    affectedRedirects: (preview as any).redirectsToRemove?.map((redirect: CanonicalRedirectRecord) => redirect.sourceNodeId) || [],
    affectedTombstones: (preview as any).tombstonesToRemove?.map((tombstone: CanonicalTombstoneRecord) => tombstone.nodeId) || [],
    unresolvedRestorationTasks: [
      'Verify production graph edge endpoints against beforeSnapshot.',
      'Verify Resource Layer nodeResourceLinks against beforeSnapshot.',
      'Resolve duplicate edge consolidation manually if any destructive graph operation is later applied.',
    ],
    recommendedManualSteps: (preview as any).remediationPreview?.recommendedManualSteps || [],
    validationWarnings: (preview as any).warnings || [],
    createdAt,
    reviewer: request.reviewer || 'local-dev-reviewer',
    status: 'open',
  };
}

export function rollbackCanonicalDecision(
  repoRoot: string,
  decisionId: string,
  request: { reviewer?: string; rationale?: string; dryRun?: boolean; apply?: boolean },
) {
  const preview = previewCanonicalRollback(repoRoot, decisionId);
  if ('decision' in preview === false) return preview;
  const blockers = [
    ...preview.blockers,
    !request.reviewer?.trim() ? 'reviewer is required' : '',
    !request.rationale?.trim() ? 'rationale is required' : '',
  ].filter(Boolean);
  if (request.dryRun || !request.apply || blockers.length) return { dryRun: true, preview: { ...preview, blockers }, blockers };
  const paths = canonicalStewardshipPaths(repoRoot);
  const files = preview.rollbackCapability === 'partial'
    ? [paths.decisions, paths.aliases, paths.redirects, paths.tombstones, paths.remediationManifests, paths.approvals, paths.admittedRelationships]
    : [paths.decisions, paths.aliases, paths.redirects, paths.tombstones, paths.approvals, paths.admittedRelationships];
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_decision_rollback', files, (tx) => {
    const timestamp = nowIso();
    if (tx) {
      tx.decisionIds = [decisionId];
      tx.rollbackCapability = preview.rollbackCapability;
    }
    const originalDecision = readCanonicalDecisions(repoRoot).find((decision) => decision.decisionId === decisionId)!;
    const rollbackStatus: CanonicalDecisionStatus = preview.rollbackCapability === 'partial' ? 'rollback_partial' : 'rolled_back';
    const decisions = readCanonicalDecisions(repoRoot).map((decision) => decision.decisionId === decisionId ? {
      ...decision,
      status: rollbackStatus,
      validationResult: {
        ...(typeof decision.validationResult === 'object' && decision.validationResult ? decision.validationResult as Record<string, unknown> : {}),
        rollback: { reviewer: request.reviewer, rationale: request.rationale, rolledBackAt: timestamp, rollbackCapability: preview.rollbackCapability },
      },
    } : decision);
    writeCanonicalDecisions(repoRoot, decisions);
    writeCanonicalAliases(repoRoot, readCanonicalAliases(repoRoot).filter((alias) => alias.decisionId !== decisionId));
    writeCanonicalRedirects(repoRoot, readCanonicalRedirects(repoRoot).filter((redirect) => redirect.decisionId !== decisionId));
    writeCanonicalTombstones(repoRoot, readCanonicalTombstones(repoRoot).filter((tombstone) => tombstone.decisionId !== decisionId));
    writeCanonicalApprovals(repoRoot, readCanonicalApprovals(repoRoot).map((approval) => approval.decisionId === decisionId ? {
      ...approval,
      status: 'rolled_back',
    } : approval));
    writeCanonicalAdmittedRelationships(repoRoot, readCanonicalAdmittedRelationships(repoRoot).map((edge) => edge.stewardshipDecisionId === decisionId ? {
      ...edge,
      reviewStatus: 'rolled_back',
      rollbackAt: timestamp,
    } : edge));
    const remediation = preview.rollbackCapability === 'partial'
      ? createRollbackRemediationManifest(originalDecision, preview as any, request, `rollback-${timestamp.replace(/\D/g, '').slice(0, 14)}`)
      : undefined;
    if (remediation) {
      writeCanonicalRemediationManifests(repoRoot, [...readCanonicalRemediationManifests(repoRoot), remediation]);
    }
    return { rollback: { decisionId, rolledBackAt: timestamp, rollbackCapability: preview.rollbackCapability, remediationManifestId: remediation?.remediationManifestId }, preview, remediation };
  });
  manifest.rollbackCapability = preview.rollbackCapability;
  return { ...result, manifest };
}

export function listCanonicalRemediationManifests(repoRoot: string) {
  return readCanonicalRemediationManifests(repoRoot).sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export function findCanonicalRemediationManifest(repoRoot: string, remediationManifestId: string) {
  return readCanonicalRemediationManifests(repoRoot).find((entry) => entry.remediationManifestId === remediationManifestId) || null;
}

export function updateCanonicalRemediationStatus(
  repoRoot: string,
  remediationManifestId: string,
  request: { status?: CanonicalRemediationManifest['status']; reviewer?: string; resolutionNotes?: string },
) {
  const current = findCanonicalRemediationManifest(repoRoot, remediationManifestId);
  if (!current) return { blockers: ['canonical remediation manifest not found'] };
  const blockers: string[] = [];
  if (!request.status || !['open', 'in_progress', 'resolved', 'waived'].includes(request.status)) blockers.push('valid remediation status is required');
  if ((request.status === 'resolved' || request.status === 'waived') && !request.resolutionNotes?.trim()) blockers.push('resolutionNotes are required to resolve or waive remediation');
  if (blockers.length) return { blockers };
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_remediation_status', [paths.remediationManifests], () => {
    const updated = readCanonicalRemediationManifests(repoRoot).map((entry) => entry.remediationManifestId === remediationManifestId ? {
      ...entry,
      status: request.status!,
      resolutionNotes: request.resolutionNotes || entry.resolutionNotes,
      reviewer: request.reviewer || entry.reviewer,
      resolvedAt: request.status === 'resolved' || request.status === 'waived' ? nowIso() : entry.resolvedAt,
    } : entry);
    writeCanonicalRemediationManifests(repoRoot, updated);
    return { remediation: updated.find((entry) => entry.remediationManifestId === remediationManifestId) };
  });
  return { ...result, manifest };
}

function relationshipAdmissionDecisionId(candidateId: string | undefined, relationships: CanonicalStewardshipRelationshipProposal[], timestamp: string) {
  return `canonical-${timestamp.replace(/\D/g, '').slice(0, 14)}-${shortHash(`aec:${candidateId || 'unscoped'}:${stableStringify(relationships)}`)}`;
}

function relationshipAdmissionCandidateGroupId(candidateId: string | undefined, relationships: CanonicalStewardshipRelationshipProposal[]) {
  return `acs-enrichment-${shortHash(`${candidateId || 'candidate'}:${relationships.map((edge) => `${edge.sourceNodeId}|${edge.relationType}|${edge.targetNodeId}`).join('|')}`)}`;
}

function canonicalNodeSnapshot(node: GraphNodeLike, edges: GraphEdgeLike[], resourceData?: ResourceLayerData) {
  const counts = edgeCounts(edges);
  return {
    id: node.id,
    label: labelFor(node),
    displayLabel: node.displayLabel || labelFor(node),
    type: node.type,
    aliases: aliasesFor(node),
    taxonomyPath: taxonomyFor(node),
    incomingEdgeCount: counts.incoming.get(node.id) || 0,
    outgoingEdgeCount: counts.outgoing.get(node.id) || 0,
    resourceLinkCount: resourceCounts(resourceData).get(node.id) || 0,
  };
}

export function previewCanonicalRelationshipAdmissionDecision(
  repoRoot: string,
  request: CanonicalRelationshipAdmissionRequest,
  nodes: GraphNodeLike[],
  edges: GraphEdgeLike[],
  resourceData?: ResourceLayerData,
) {
  const timestamp = nowIso();
  const blockers: string[] = [];
  const warnings: string[] = [];
  const reviewer = request.reviewer?.trim() || '';
  const rationale = request.rationale?.trim() || '';
  const rawRelationships = Array.isArray(request.relationships) ? request.relationships : [];
  if (!reviewer) blockers.push('reviewer is required');
  if (!rationale) blockers.push('rationale is required');
  if (!rawRelationships.length) blockers.push('at least one relationship is required');

  const nodeById = new Map(nodes.map((node) => [node.id, node]));
  const existingEdgeKeys = new Set([
    ...edges.map((edge) => `${edge.source}|${edge.type}|${edge.target}`),
    ...readCanonicalAdmittedRelationships(repoRoot)
      .filter((edge) => edge.reviewStatus !== 'rolled_back')
      .map((edge) => `${edge.source}|${edge.type}|${edge.target}`),
  ]);
  const proposedKeys = new Set<string>();
  const proposedRelationshipAdds = rawRelationships.map((relationship, index): CanonicalStewardshipRelationshipProposal => {
    const relationType = normalizeAdmissionRelationType(relationship.relationType);
    const sourceNodeId = String(relationship.sourceNodeId || '');
    const targetNodeId = String(relationship.targetNodeId || '');
    const proposalId = relationship.proposalId || `aec-edge-proposal-${shortHash(`${sourceNodeId}:${relationType}:${targetNodeId}:${index}`)}`;
    if (!nodeById.has(sourceNodeId)) blockers.push(`relationship source missing: ${sourceNodeId || '(empty)'}`);
    if (!nodeById.has(targetNodeId)) blockers.push(`relationship target missing: ${targetNodeId || '(empty)'}`);
    if (sourceNodeId && sourceNodeId === targetNodeId) blockers.push(`relationship self-loop is not allowed: ${sourceNodeId}`);
    if (!STEWARDSHIP_RELATIONSHIP_TYPES.has(relationType)) blockers.push(`unsupported relationship type: ${relationship.relationType}`);
    if (!ADMITTED_RELATIONSHIP_TYPES.has(relationType)) blockers.push(`relationship type is not admissible: ${relationship.relationType}`);
    if (relationship.relationType === 'CROSS_DOMAIN_EQUIVALENT') blockers.push('CROSS_DOMAIN_EQUIVALENT is too strong for active admitted relationships; use CROSS_DOMAIN_ALIGNMENT or a safer non-identity predicate');
    const key = `${sourceNodeId}|${relationType}|${targetNodeId}`;
    if (existingEdgeKeys.has(key)) blockers.push(`relationship duplicates existing edge: ${sourceNodeId}--${relationType.toLowerCase()}--${targetNodeId}`);
    if (proposedKeys.has(key)) blockers.push(`duplicate proposed relationship tuple: ${key}`);
    proposedKeys.add(key);
    return {
      proposalId,
      sourceNodeId,
      targetNodeId,
      relationType,
      category: relationship.category || 'semantic/aec-mechanism',
      direction: relationship.direction || 'outgoing',
      confidence: relationship.confidence || 'reviewed',
      weight: relationship.weight ?? 0.5,
      rationale: relationship.rationale || rationale,
      provenance: relationship.provenance || 'reviewed ACS domain-synthesis candidate; no standard edition, jurisdiction, numerical criterion, URL, or protected source payload claim',
      stewardshipDecisionId: 'pending',
      createdAt: timestamp,
      reviewStatus: 'proposed',
    };
  });

  const sourceNodeIds = Array.from(new Set(proposedRelationshipAdds.flatMap((proposal) => [proposal.sourceNodeId, proposal.targetNodeId]).filter(Boolean))).sort();
  const affectedEdges = edges.filter((edge) => sourceNodeIds.includes(edge.source) || sourceNodeIds.includes(edge.target));
  const sourceNodes = sourceNodeIds
    .map((nodeId) => nodeById.get(nodeId))
    .filter((node): node is GraphNodeLike => Boolean(node));
  const candidateGroupId = relationshipAdmissionCandidateGroupId(request.candidateId, proposedRelationshipAdds);
  const decisionId = relationshipAdmissionDecisionId(request.candidateId, proposedRelationshipAdds, timestamp);
  const affectedAliases = Array.from(new Set(sourceNodes.flatMap((node) => [labelFor(node), ...aliasesFor(node)]).map(normalizeCanonicalLabel).filter(Boolean))).sort();
  const preview = {
    dryRun: true,
    decisionType: 'AEC_RELATIONSHIP_ENRICHMENT' as CanonicalDecisionType,
    candidateGroupId,
    sourceNodeIds,
    affectedEdgeIds: affectedEdges.map((edge) => edge.id),
    affectedResourceLinkIds: (resourceData?.nodeResourceLinks || []).filter((link) => sourceNodeIds.includes(link.nodeId)).map((link) => link.id),
    affectedAliases,
    affectedSearchTerms: affectedAliases,
    affectedNodeIds: sourceNodeIds,
    proposedRelationshipAdds,
    graphNodeMutation: false,
    edgeEndpointMutation: false,
    resourceLayerMutation: false,
    aliasRedirectTombstoneMutation: false,
    rollbackCapability: 'full' as CanonicalRollbackCapability,
    validation: {
      blockers,
      warnings,
    },
  };
  return {
    dryRun: true,
    decisionId,
    decisionType: 'AEC_RELATIONSHIP_ENRICHMENT' as CanonicalDecisionType,
    candidateGroupId,
    preview,
    blockers,
    warnings,
  };
}

export function recordCanonicalRelationshipAdmissionDecision(
  repoRoot: string,
  request: CanonicalRelationshipAdmissionRequest,
  nodes: GraphNodeLike[],
  edges: GraphEdgeLike[],
  resourceData?: ResourceLayerData,
) {
  const preview = previewCanonicalRelationshipAdmissionDecision(repoRoot, request, nodes, edges, resourceData);
  if (request.dryRun || !request.apply || preview.blockers.length) return preview;
  const timestamp = nowIso();
  const decisionId = relationshipAdmissionDecisionId(request.candidateId, preview.preview.proposedRelationshipAdds, timestamp);
  const proposedRelationshipAdds = preview.preview.proposedRelationshipAdds.map((proposal) => ({
    ...proposal,
    stewardshipDecisionId: decisionId,
    createdAt: timestamp,
  }));
  const sourceNodes = preview.preview.sourceNodeIds
    .map((nodeId) => nodes.find((node) => node.id === nodeId))
    .filter((node): node is GraphNodeLike => Boolean(node));
  const decision: CanonicalStewardshipDecision = {
    decisionId,
    decisionType: 'AEC_RELATIONSHIP_ENRICHMENT',
    candidateGroupId: preview.candidateGroupId,
    sourceNodeIds: preview.preview.sourceNodeIds,
    affectedEdgeIds: preview.preview.affectedEdgeIds,
    affectedResourceLinkIds: preview.preview.affectedResourceLinkIds,
    affectedAliases: preview.preview.affectedAliases,
    affectedSearchTerms: preview.preview.affectedSearchTerms,
    affectedNodeIds: preview.preview.affectedNodeIds,
    reviewer: request.reviewer!.trim(),
    reviewedBy: request.reviewer!.trim(),
    createdAt: timestamp,
    rationale: request.rationale!.trim(),
    riskLevel: request.riskLevel || 'medium',
    beforeSnapshot: {
      schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
      nodes: sourceNodes.map((node) => canonicalNodeSnapshot(node, edges, resourceData)),
      affectedEdgeIds: preview.preview.affectedEdgeIds,
      affectedResourceLinkIds: preview.preview.affectedResourceLinkIds,
    },
    afterPreview: {
      proposedRelationshipAdds,
      graphNodeMutation: false,
      edgeEndpointMutation: false,
      resourceLayerMutation: false,
      aliasRedirectTombstoneMutation: false,
      caveat: 'ACS relationship enrichment decision only; approval/admission is non-destructive and must not imply source truth, merge, alias, redirect, or tombstone.',
    },
    status: 'pending_steward_approval',
    rollbackCapability: 'full',
    validationResult: {
      dryRun: true,
      blockers: [],
      warnings: preview.warnings,
      sourceContextCaveat: 'Domain-synthesis rationale only; no standard edition, jurisdiction, numerical criterion, URL, or protected source payload is claimed.',
    },
    kimiReviewSummary: request.kimiReviewSummary,
    notes: request.notes,
    proposedRelationshipAdds,
  };
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_aec_relationship_enrichment_decision', [paths.decisions], (tx) => {
    if (tx) {
      tx.decisionIds = [decisionId];
      tx.rollbackCapability = 'full';
    }
    writeCanonicalDecisions(repoRoot, [...readCanonicalDecisions(repoRoot), decision]);
    return { decision, preview: { ...preview.preview, proposedRelationshipAdds } };
  });
  manifest.decisionIds = [decisionId];
  manifest.rollbackCapability = 'full';
  return { ...result, manifest };
}

function normalizeAdmissionRelationType(relationType: CanonicalStewardshipRelationType): CanonicalStewardshipRelationType {
  return relationType === 'CROSS_DOMAIN_EQUIVALENT' ? 'CROSS_DOMAIN_ALIGNMENT' : relationType;
}

function approvalIdFor(decisionId: string, timestamp: string, request: CanonicalApprovalRequest) {
  return `canonical-approval-${timestamp.replace(/\D/g, '').slice(0, 14)}-${shortHash(`${decisionId}:${request.approvedBy}:${request.mutationScope}:${timestamp}`)}`;
}

function admittedRelationshipIdFor(sourceNodeId: string, relationType: string, targetNodeId: string) {
  return `${sourceNodeId}--${relationType.toLowerCase()}--${targetNodeId}`;
}

function approvalSourceIsFixtureOnly(request: CanonicalApprovalRequest) {
  return (request.approvalSource || 'api') === 'test_fixture';
}

function isProductionNodeId(nodeId: string) {
  return /^VTN-DOM-\d+$/i.test(nodeId);
}

function decisionApprovalHash(decision: CanonicalStewardshipDecision, mutationScope: CanonicalMutationScope) {
  return hash(stableStringify({
    decisionId: decision.decisionId,
    decisionType: decision.decisionType,
    candidateGroupId: decision.candidateGroupId,
    canonicalNodeId: decision.canonicalNodeId,
    sourceNodeIds: decision.sourceNodeIds,
    affectedEdgeIds: decision.affectedEdgeIds,
    affectedResourceLinkIds: decision.affectedResourceLinkIds,
    proposedRelationshipAdds: decision.proposedRelationshipAdds || [],
    rationale: decision.rationale,
    riskLevel: decision.riskLevel,
    mutationScope,
  }));
}

export function previewCanonicalApproval(
  repoRoot: string,
  decisionId: string,
  request: CanonicalApprovalRequest,
  nodes: GraphNodeLike[],
  edges: GraphEdgeLike[],
  resourceData?: ResourceLayerData,
) {
  const decisions = readCanonicalDecisions(repoRoot);
  const decision = decisions.find((entry) => entry.decisionId === decisionId);
  const nodeIds = new Set(nodes.map((node) => node.id));
  const existingEdgeKeys = new Set([
    ...edges.map((edge) => `${edge.source}|${edge.type}|${edge.target}`),
    ...readCanonicalAdmittedRelationships(repoRoot)
      .filter((edge) => edge.reviewStatus !== 'rolled_back')
      .map((edge) => `${edge.source}|${edge.type}|${edge.target}`),
  ]);
  const blockers: string[] = [];
  const warnings: string[] = [];
  if (!decision) blockers.push(`canonical decision not found: ${decisionId}`);
  const approvedBy = request.approvedBy?.trim() || '';
  const reviewerRole = request.reviewerRole?.trim() || '';
  const approvalRationale = request.approvalRationale?.trim() || '';
  const rollbackPlan = request.rollbackPlan?.trim() || '';
  const mutationScope = request.mutationScope || 'metadata_only';
  if (!approvedBy) blockers.push('approvedBy is required');
  if (!reviewerRole) blockers.push('reviewerRole is required');
  if (!approvalRationale) blockers.push('approvalRationale is required');
  if (!rollbackPlan) blockers.push('rollbackPlan is required');
  if (!['metadata_only', 'non_destructive_edge_admission', 'alias_only', 'redirect', 'tombstone', 'destructive_merge'].includes(mutationScope)) blockers.push(`unsupported mutationScope: ${String(mutationScope)}`);
  if (decision && (decision.riskLevel === 'high' || decision.riskLevel === 'critical') && !request.riskAcknowledgment) blockers.push('high-risk approval requires riskAcknowledgment');
  if (decision && mutationScope === 'destructive_merge') blockers.push('destructive merge admission is not supported by the P0 stewardship admission gate');
  if (decision && approvalSourceIsFixtureOnly(request) && decision.sourceNodeIds.some(isProductionNodeId)) blockers.push('test_fixture approval cannot be used for production VTN-DOM stewardship decisions');
  if (decision && approvalSourceIsFixtureOnly(request) && process.env.NODE_ENV !== 'test') blockers.push('test_fixture approval is allowed only in NODE_ENV=test');
  if (decision && ['rejected', 'deferred', 'rollback_blocked'].includes(decision.status)) blockers.push(`decision status ${decision.status} is not eligible for approval or admission`);
  if (decision && decision.status === 'admitted' && mutationScope !== 'metadata_only') blockers.push('admitted decisions cannot be re-admitted without rollback');
  if (decision && decision.status === 'rolled_back' && mutationScope === 'non_destructive_edge_admission') warnings.push('rollback replay requested; approval will bind to the current rolled-back decision snapshot');
  if (request.approvalSource === 'human_record' || request.approvalSource === 'imported_decision_record') warnings.push('human/imported approval records are accepted only as metadata; attach external provenance before production admission outside local/dev');

  const relationshipProposals = (decision?.proposedRelationshipAdds || []).map((proposal) => ({
    ...proposal,
    relationType: normalizeAdmissionRelationType(proposal.relationType),
  }));
  if (mutationScope === 'non_destructive_edge_admission' && relationshipProposals.length === 0) blockers.push('non_destructive_edge_admission requires proposed relationships');
  const admittedRelationshipPreview = mutationScope === 'non_destructive_edge_admission'
    ? relationshipProposals.map((proposal): CanonicalAdmittedRelationship => {
      const relationType = normalizeAdmissionRelationType(proposal.relationType);
      const id = admittedRelationshipIdFor(proposal.sourceNodeId, relationType, proposal.targetNodeId);
      if (!nodeIds.has(proposal.sourceNodeId)) blockers.push(`admitted relationship source missing: ${proposal.sourceNodeId}`);
      if (!nodeIds.has(proposal.targetNodeId)) blockers.push(`admitted relationship target missing: ${proposal.targetNodeId}`);
      if (proposal.sourceNodeId === proposal.targetNodeId) blockers.push(`admitted relationship self-loop: ${proposal.sourceNodeId}`);
      if (!ADMITTED_RELATIONSHIP_TYPES.has(relationType)) blockers.push(`relation type is not admissible: ${proposal.relationType}`);
      if (existingEdgeKeys.has(`${proposal.sourceNodeId}|${relationType}|${proposal.targetNodeId}`)) blockers.push(`admitted relationship duplicates existing edge: ${id}`);
      return {
        id,
        admissionId: id,
        source: proposal.sourceNodeId,
        target: proposal.targetNodeId,
        type: relationType,
        relationType,
        relationCategory: proposal.category || 'semantic/stewardship-disambiguation',
        direction: proposal.direction || 'outgoing',
        confidence: request.approvalSource === 'test_fixture' ? 'test_fixture' : 'steward_approved',
        weight: proposal.weight ?? 0.5,
        rationale: proposal.rationale || approvalRationale,
        provenanceNote: `${proposal.provenance || 'canonical stewardship decision'}; admitted via approval gate`,
        stewardshipDecisionId: decisionId,
        approvalId: 'pending',
        reviewStatus: 'admitted',
        createdAt: nowIso(),
        createdBy: approvedBy || 'pending',
        reversible: true,
      };
    })
    : [];
  for (const edge of admittedRelationshipPreview) {
    if ((edge.type === 'CROSS_DOMAIN_ALIGNMENT' || edge.direction === 'bidirectional')) {
      const reverseExists = admittedRelationshipPreview.some((other) => other.source === edge.target && other.target === edge.source && other.type === edge.type);
      if (!reverseExists) warnings.push(`symmetric admitted relationship lacks reciprocal edge: ${edge.id}`);
    }
  }
  const validationSnapshot = validateCanonicalStewardship(repoRoot, nodes, edges, resourceData);
  return {
    dryRun: true,
    decision,
    approvalPreview: {
      decisionId,
      groupId: decision?.candidateGroupId,
      approvedBy,
      reviewerRole,
      approvalSource: request.approvalSource || 'api',
      mutationScope,
      approvalRationale,
      rollbackPlan,
      riskAcknowledgment: Boolean(request.riskAcknowledgment),
      status: mutationScope === 'non_destructive_edge_admission' ? 'admitted' : 'steward_approved',
      admittedRelationshipPreview,
      validationSnapshot,
      decisionHash: decision ? decisionApprovalHash(decision, mutationScope as CanonicalMutationScope) : undefined,
    },
    blockers,
    warnings,
  };
}

export function approveCanonicalDecision(
  repoRoot: string,
  decisionId: string,
  request: CanonicalApprovalRequest,
  nodes: GraphNodeLike[],
  edges: GraphEdgeLike[],
  resourceData?: ResourceLayerData,
) {
  const preview = previewCanonicalApproval(repoRoot, decisionId, request, nodes, edges, resourceData);
  if (preview.blockers.length) return preview;
  if (request.dryRun || !request.apply) return preview;
  const paths = canonicalStewardshipPaths(repoRoot);
  const files = [paths.approvals, paths.decisions];
  if (preview.approvalPreview.mutationScope === 'non_destructive_edge_admission') files.push(paths.admittedRelationships);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_decision_approval', files, (tx) => {
    const timestamp = nowIso();
    if (tx) {
      tx.decisionIds = [decisionId];
      tx.rollbackCapability = 'full';
    }
    const approvalId = approvalIdFor(decisionId, timestamp, request);
    const admittedRelationships = preview.approvalPreview.admittedRelationshipPreview.map((edge) => ({
      ...edge,
      approvalId,
      createdAt: timestamp,
      createdBy: preview.approvalPreview.approvedBy,
    }));
    const approval: CanonicalStewardshipApproval = {
      approvalId,
      decisionId,
      groupId: preview.approvalPreview.groupId!,
      decisionHash: preview.approvalPreview.decisionHash as string,
      approvedBy: preview.approvalPreview.approvedBy,
      reviewerRole: preview.approvalPreview.reviewerRole,
      approvalSource: preview.approvalPreview.approvalSource as CanonicalApprovalSource,
      approvedAt: timestamp,
      approvalRationale: preview.approvalPreview.approvalRationale,
      riskAcknowledgment: preview.approvalPreview.riskAcknowledgment,
      mutationScope: preview.approvalPreview.mutationScope as CanonicalMutationScope,
      rollbackPlan: preview.approvalPreview.rollbackPlan,
      validationSnapshot: preview.approvalPreview.validationSnapshot,
      kimiReviewSummary: request.kimiReviewSummary,
      transactionManifestId: tx?.transactionId,
      status: preview.approvalPreview.status as CanonicalApprovalStatus,
      admittedBy: admittedRelationships.length ? preview.approvalPreview.approvedBy : undefined,
      admittedAt: admittedRelationships.length ? timestamp : undefined,
      admissionTransactionId: admittedRelationships.length ? tx?.transactionId : undefined,
      postAdmissionValidationSnapshot: admittedRelationships.length ? {
        ok: true,
        pendingTransactionFinalization: true,
        checkedAt: timestamp,
        caveat: 'Temporary in-transaction marker; replaced with a validation snapshot before the approval transaction completes.',
      } : undefined,
    };
    writeCanonicalApprovals(repoRoot, [...readCanonicalApprovals(repoRoot), approval]);
    if (admittedRelationships.length) {
      writeCanonicalAdmittedRelationships(repoRoot, [
        ...readCanonicalAdmittedRelationships(repoRoot).filter((edge) => !(edge.stewardshipDecisionId === decisionId && edge.reviewStatus !== 'rolled_back')),
        ...admittedRelationships,
      ]);
    }
    writeCanonicalDecisions(repoRoot, readCanonicalDecisions(repoRoot).map((decision) => {
      if (decision.decisionId !== decisionId) return decision;
      const nextDecision: CanonicalStewardshipDecision = {
        ...decision,
        status: admittedRelationships.length ? 'admitted' : 'steward_approved',
        appliedAt: timestamp,
        transactionManifestId: tx?.transactionId,
        validationResult: { ...(typeof decision.validationResult === 'object' && decision.validationResult ? decision.validationResult as Record<string, unknown> : {}), approvalId, admissionRelationshipCount: admittedRelationships.length },
      };
      if (!admittedRelationships.length && preview.approvalPreview.mutationScope === 'metadata_only') {
        nextDecision.proposedRelationshipAdds = [];
        nextDecision.notes = [
          decision.notes,
          'Metadata-only steward approval intentionally leaves no latent relationship proposals for admission; future visible disambiguation edges require a separate scoped preview, Kimi review, and approval.',
        ].filter(Boolean).join('\n\n');
      }
      return nextDecision;
    }));
    const postAdmissionValidationSnapshot = validateCanonicalStewardship(repoRoot, nodes, edges, resourceData);
    writeCanonicalApprovals(repoRoot, readCanonicalApprovals(repoRoot).map((entry) => entry.approvalId === approvalId ? {
      ...entry,
      postAdmissionValidationSnapshot,
    } : entry));
    return { approval, admittedRelationships };
  });
  manifest.decisionIds = [decisionId];
  manifest.rollbackCapability = 'full';
  return { ...result, manifest };
}

export function rejectCanonicalApproval(repoRoot: string, decisionId: string, request: { approvedBy?: string; reviewerRole?: string; rejectionRationale?: string; apply?: boolean; dryRun?: boolean }) {
  const decision = readCanonicalDecisions(repoRoot).find((entry) => entry.decisionId === decisionId);
  const blockers: string[] = [];
  if (!decision) blockers.push(`canonical decision not found: ${decisionId}`);
  if (!request.approvedBy?.trim()) blockers.push('approvedBy is required');
  if (!request.reviewerRole?.trim()) blockers.push('reviewerRole is required');
  if (!request.rejectionRationale?.trim()) blockers.push('rejectionRationale is required');
  if (blockers.length || request.dryRun || !request.apply) return { dryRun: true, decision, blockers };
  const paths = canonicalStewardshipPaths(repoRoot);
  const { result, manifest } = withCanonicalTransaction(repoRoot, 'canonical_approval_rejection', [paths.approvals, paths.decisions], (tx) => {
    const timestamp = nowIso();
    const approval: CanonicalStewardshipApproval = {
      approvalId: approvalIdFor(decisionId, timestamp, { approvedBy: request.approvedBy, mutationScope: 'metadata_only' }),
      decisionId,
      groupId: decision!.candidateGroupId,
      decisionHash: decisionApprovalHash(decision!, 'metadata_only'),
      approvedBy: request.approvedBy!.trim(),
      reviewerRole: request.reviewerRole!.trim(),
      approvalSource: 'api',
      approvedAt: timestamp,
      approvalRationale: request.rejectionRationale!.trim(),
      riskAcknowledgment: false,
      mutationScope: 'metadata_only',
      rollbackPlan: 'No mutation was admitted; rejection can be superseded by a later approval record.',
      validationSnapshot: { rejected: true },
      transactionManifestId: tx?.transactionId,
      status: 'rejected',
      rejectedAt: timestamp,
      rejectionRationale: request.rejectionRationale!.trim(),
    };
    writeCanonicalApprovals(repoRoot, [...readCanonicalApprovals(repoRoot), approval]);
    writeCanonicalDecisions(repoRoot, readCanonicalDecisions(repoRoot).map((entry) => entry.decisionId === decisionId ? { ...entry, status: 'rejected' } : entry));
    return { approval };
  });
  return { ...result, manifest };
}

export function mergeAdmittedRelationshipsIntoEdges(edges: GraphEdgeLike[], admittedRelationships: CanonicalAdmittedRelationship[]) {
  const seen = new Set(edges.map((edge) => edge.id));
  const active = admittedRelationships.filter((edge) => edge.reviewStatus !== 'rolled_back' && !seen.has(edge.id));
  return [...edges, ...active];
}

export function canonicalNodeStatus(repoRoot: string, nodeId: string, groups: DuplicateCandidateGroup[]) {
  const tombstone = readCanonicalTombstones(repoRoot).find((record) => record.nodeId === nodeId);
  if (tombstone) return { status: 'deprecated', canonicalNodeId: tombstone.canonicalTargetId, tombstone };
  const redirect = readCanonicalRedirects(repoRoot).find((record) => record.sourceNodeId === nodeId);
  if (redirect) return { status: 'merged_into', canonicalNodeId: redirect.canonicalNodeId, redirect };
  const activeAliases = readCanonicalAliases(repoRoot).filter((alias) => !['rejected', 'deprecated'].includes(alias.status || 'active'));
  const aliasOf = activeAliases.find((record) => record.sourceNodeIds.includes(nodeId) && record.canonicalNodeId !== nodeId);
  if (aliasOf) return { status: 'alias_of', canonicalNodeId: aliasOf.canonicalNodeId, alias: aliasOf };
  const aliases = activeAliases.filter((record) => record.canonicalNodeId === nodeId);
  const duplicateGroups = groups.filter((group) => group.nodeIds.includes(nodeId));
  const unresolved = duplicateGroups.filter((group) => group.status === 'unresolved');
  const disambiguated = duplicateGroups.filter((group) => group.status === 'disambiguated' || group.status === 'keep_separate');
  return {
    status: aliases.length ? 'canonical' : unresolved.length ? 'unresolved_duplicate_candidate' : disambiguated.length ? 'disambiguated_keep_separate' : 'canonical',
    aliases,
    duplicateGroupIds: duplicateGroups.map((group) => group.groupId),
  };
}

export function canonicalPreferredSearch(repoRoot: string, nodes: GraphNodeLike[], query: string, groups: DuplicateCandidateGroup[], limit = 20) {
  const normalizedQuery = normalizeCanonicalLabelLoose(query);
  const aliases = readCanonicalAliases(repoRoot).filter((alias) => !['rejected', 'deprecated'].includes(alias.status || 'active'));
  const redirects = readCanonicalRedirects(repoRoot);
  const tombstones = readCanonicalTombstones(repoRoot);
  const approvals = readCanonicalApprovals(repoRoot);
  const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot).filter((edge) => edge.reviewStatus !== 'rolled_back');
  const aliasMatches = aliases.filter((alias) => alias.normalizedAlias.includes(normalizedQuery) || normalizedQuery.includes(alias.normalizedAlias));
  const redirectBySource = new Map(redirects.map((record) => [record.sourceNodeId, record]));
  const tombstoneByNode = new Map(tombstones.map((record) => [record.nodeId, record]));
  const aliasCanonicalIds = new Set(aliasMatches.map((alias) => alias.canonicalNodeId));
  const duplicateNodeIds = new Set(groups.flatMap((group) => group.nodeIds));
  const duplicateGroupsByNode = new Map<string, DuplicateCandidateGroup[]>();
  for (const group of groups) {
    for (const nodeId of group.nodeIds) {
      duplicateGroupsByNode.set(nodeId, [...(duplicateGroupsByNode.get(nodeId) || []), group]);
    }
  }
  const scored = nodes.map((node) => {
    const label = labelFor(node);
    const normalizedLabel = normalizeCanonicalLabelLoose(label);
    const aliasMatch = aliasCanonicalIds.has(node.id) || aliasesFor(node).map(normalizeCanonicalLabelLoose).some((alias) => alias.includes(normalizedQuery));
    const labelMatch = normalizedLabel.includes(normalizedQuery) || normalizedQuery.includes(normalizedLabel);
    if (!aliasMatch && !labelMatch) return null;
    const redirect = redirectBySource.get(node.id);
    const tombstone = tombstoneByNode.get(node.id);
    const nodeDuplicateGroups = duplicateGroupsByNode.get(node.id) || [];
    const primaryGroup = nodeDuplicateGroups[0];
    let score = normalizedLabel === normalizedQuery ? 100 : labelMatch ? 50 : 0;
    if (aliasCanonicalIds.has(node.id)) score += 75;
    if (redirect) score -= 80;
    if (tombstone) score -= 100;
    if (duplicateNodeIds.has(node.id) && nodeDuplicateGroups.some((group) => group.status === 'unresolved')) score -= 10;
    const existingDecisionTypes = Array.from(new Set(nodeDuplicateGroups.flatMap((group) => group.existingDecisions.map((decision) => decision.decisionType))));
    const existingDecisionIds = nodeDuplicateGroups.flatMap((group) => group.existingDecisions.map((decision) => decision.decisionId));
    const approvalStatuses = Array.from(new Set(approvals.filter((approval) => existingDecisionIds.includes(approval.decisionId)).map((approval) => approval.status)));
    const admittedRelationshipCount = admittedRelationships.filter((edge) => existingDecisionIds.includes(edge.stewardshipDecisionId)).length;
    const disambiguationDecision = nodeDuplicateGroups.flatMap((group) => group.existingDecisions).find((decision) => DISAMBIGUATION_DECISION_TYPES.has(decision.decisionType));
    const disambiguationLabel = primaryGroup?.nodes.find((entry) => entry.id === node.id) ? disambiguationLabelFor(primaryGroup.nodes.find((entry) => entry.id === node.id)!) : undefined;
    const ambiguityStatus = nodeDuplicateGroups.some((group) => group.status === 'disambiguated' || group.status === 'keep_separate')
      ? 'disambiguated_concepts'
      : disambiguationDecision
        ? 'proposed_disambiguation'
        : nodeDuplicateGroups.length
          ? 'unresolved_duplicate_group'
          : undefined;
    return {
      kind: 'node',
      id: node.id,
      label,
      displayLabel: node.displayLabel,
      type: node.type,
      matchType: aliasMatch ? 'canonical_alias' : 'canonical_label',
      matchedField: aliasMatch ? 'alias' : 'label',
      canonicalStatus: tombstone ? 'deprecated' : redirect ? 'merged_into' : aliasCanonicalIds.has(node.id) ? 'canonical' : ambiguityStatus === 'disambiguated_concepts' ? 'disambiguated_keep_separate' : duplicateNodeIds.has(node.id) ? 'unresolved_duplicate_candidate' : 'canonical',
      canonicalNodeId: tombstone?.canonicalTargetId || redirect?.canonicalNodeId || node.id,
      duplicateGroupIds: nodeDuplicateGroups.map((group) => group.groupId),
      priorityBands: Array.from(new Set(nodeDuplicateGroups.map((group) => group.priorityBand))),
      riskLevels: Array.from(new Set(nodeDuplicateGroups.map((group) => group.riskLevel))),
      reviewState: ambiguityStatus,
      disambiguationLabel,
      disambiguationText: disambiguationDecision?.searchDisambiguationText || (nodeDuplicateGroups.length ? defaultSearchDisambiguationText(nodeDuplicateGroups[0]) : undefined),
      relationshipSummary: primaryGroup ? {
        groupEdgeCount: primaryGroup.edgeCount,
        nodeCount: primaryGroup.nodeIds.length,
        proposedStewardshipRelationships: primaryGroup.existingDecisions.flatMap((decision) => decision.proposedRelationshipAdds || []).length,
      } : undefined,
      resourceLinkCount: primaryGroup?.nodes.find((entry) => entry.id === node.id)?.resourceLinkCount || 0,
      existingDecisionTypes,
      approvalStatuses,
      admittedRelationshipCount,
      ambiguity: nodeDuplicateGroups.length ? {
        status: ambiguityStatus,
        priorityBands: Array.from(new Set(nodeDuplicateGroups.map((group) => group.priorityBand))),
        message: ambiguityStatus === 'disambiguated_concepts'
          ? `${nodeDuplicateGroups.length} disambiguated duplicate-review group(s) include this result`
          : disambiguationDecision
            ? `${nodeDuplicateGroups.length} duplicate-review group(s) include proposed governed disambiguation`
            : `${nodeDuplicateGroups.length} unresolved duplicate group(s) include this result`,
      } : undefined,
      score,
    };
  }).filter(Boolean) as Array<Record<string, unknown> & { score: number; id: string }>;
  return scored.sort((a, b) => b.score - a.score || a.id.localeCompare(b.id)).slice(0, limit);
}

export function validateCanonicalTransactionManifests(repoRoot: string): CanonicalTransactionManifestValidation {
  const canonicalTransactionDir = canonicalStewardshipPaths(repoRoot).transactionsDir;
  const resourceTransactionDir = resourceLayerTransactionPaths(repoRoot).transactionsDir;
  const transactionDirs = [
    { subsystem: 'graph-canonical', dir: canonicalTransactionDir },
    { subsystem: 'resource-layer', dir: resourceTransactionDir },
  ];
  const warnings: string[] = [];
  const blockers: string[] = [];
  let invalidManifestCount = 0;
  let brokenHashChainCount = 0;
  let unsignedManifestWarnings = 0;
  let transactionManifestsWithAfterHash = 0;
  let count = 0;
  let hmacMismatchCount = 0;
  const latestByFile = new Map<string, {
    manifest: CanonicalTransactionManifest;
    manifestPath: string;
    manifestName: string;
    filePath: string;
    afterHash: string;
    orderKey: string;
  }>();
  const strictRequired = manifestAfterHashStrictMode();
  const criticalFiles = custodyCriticalFileSet(repoRoot);

  for (const { subsystem, dir } of transactionDirs) {
    if (!existsSync(dir)) continue;
    const entries = readdirSync(dir).filter((name) => name.endsWith('.json')).map((name) => {
      const path = join(dir, name);
      try {
        const manifest = JSON.parse(readFileSync(path, 'utf-8')) as CanonicalTransactionManifest;
        const startedAt = manifest.startedAt || '';
        const completedAt = manifest.completedAt || startedAt;
        const transactionId = manifest.transactionId || name;
        return {
          name,
          path,
          manifest,
          orderKey: `${completedAt}|${startedAt}|${transactionId}|${name}`,
        };
      } catch {
        return {
          name,
          path,
          manifest: null,
          orderKey: `|||${name}`,
        };
      }
    }).sort((left, right) => left.orderKey.localeCompare(right.orderKey) || left.name.localeCompare(right.name));
    let previousHash: string | null = null;
    for (const entry of entries) {
      count += 1;
      const { name, path, manifest } = entry;
      if (!manifest) {
        invalidManifestCount += 1;
        blockers.push(`${subsystem} transaction manifest unreadable: ${name}`);
        continue;
      }
      const expected = manifestHash(manifest);
      if (manifest.manifestHash !== expected) {
        invalidManifestCount += 1;
        blockers.push(`${subsystem} transaction manifest hash mismatch: ${name}`);
      }
      if ((manifest.previousManifestHash || null) !== previousHash) {
        brokenHashChainCount += 1;
        blockers.push(`${subsystem} transaction manifest hash-chain break: ${name}`);
      }
      if (process.env.VITRUVIUS_TRANSACTION_HMAC_KEY && !manifest.signature) {
        unsignedManifestWarnings += 1;
        warnings.push(`${subsystem} transaction manifest missing HMAC signature: ${name}`);
      }
      if (process.env.VITRUVIUS_TRANSACTION_HMAC_KEY && manifest.signature && manifest.signature !== manifestSignature(manifest)) {
        invalidManifestCount += 1;
        hmacMismatchCount += 1;
        blockers.push(`${subsystem} transaction manifest HMAC mismatch: ${name}`);
      }
      if (manifest.afterHashes && Object.keys(manifest.afterHashes).length) {
        transactionManifestsWithAfterHash += 1;
        for (const [filePath, afterHash] of Object.entries(manifest.afterHashes)) {
          const absoluteFilePath = resolve(repoRoot, filePath);
          const fileKey = normalizeFileKey(absoluteFilePath);
          const currentLatest = latestByFile.get(fileKey);
          if (!currentLatest || entry.orderKey.localeCompare(currentLatest.orderKey) > 0) {
            latestByFile.set(fileKey, {
              manifest,
              manifestPath: path,
              manifestName: name,
              filePath: absoluteFilePath,
              afterHash,
              orderKey: entry.orderKey,
            });
          }
        }
      }
      previousHash = manifest.manifestHash || expected;
    }
  }

  const manifestAfterHashStatuses = Array.from(latestByFile.entries()).map(([fileKey, latest]) => {
    const currentHash = fileHash(latest.filePath);
    const matches = currentHash === latest.afterHash;
    const status: CanonicalManifestAfterHashStatus = {
      subsystem: latest.manifest.subsystem || 'graph-canonical',
      filePath: repoRelativeFilePath(repoRoot, latest.filePath),
      latestManifestId: latest.manifest.transactionId || latest.manifestName,
      latestManifestPath: repoRelativeFilePath(repoRoot, latest.manifestPath),
      operationType: latest.manifest.operationType || 'unknown',
      latestManifestStartedAt: latest.manifest.startedAt || '',
      latestManifestCompletedAt: latest.manifest.completedAt,
      custodyCritical: criticalFiles.has(fileKey),
      strictRequired,
      currentHash,
      latestAfterHash: latest.afterHash,
      matches,
      status: matches ? 'matched_latest_manifest' : 'drift_since_latest_manifest',
    };
    if (!matches) {
      const message = `${status.subsystem} custody file drift since latest manifest: ${status.filePath} (latest manifest ${status.latestManifestId})`;
      if (strictRequired && status.custodyCritical) blockers.push(message);
      else warnings.push(message);
    }
    return status;
  }).sort((left, right) => left.filePath.localeCompare(right.filePath) || left.latestManifestId.localeCompare(right.latestManifestId));

  const latestAfterHashMatches = manifestAfterHashStatuses.filter((status) => status.matches).length;
  const latestAfterHashMismatches = manifestAfterHashStatuses.length - latestAfterHashMatches;
  return {
    count,
    invalidManifestCount,
    brokenHashChainCount,
    unsignedManifestWarnings,
    transactionManifestsWithAfterHash,
    filesUnderManifestCustody: manifestAfterHashStatuses.length,
    latestAfterHashMatches,
    latestAfterHashMismatches,
    staleManifestFiles: latestAfterHashMismatches,
    unmanifestedMutatedCustodyFiles: 0,
    manifestChainValid: brokenHashChainCount === 0,
    manifestSignatureValid: hmacMismatchCount === 0,
    latestManifestAfterHashStrictMode: strictRequired,
    manifestAfterHashStatuses,
    blockers,
    warnings,
  };
}

export function validateCanonicalStewardship(repoRoot: string, nodes: GraphNodeLike[], edges: GraphEdgeLike[], resourceData?: ResourceLayerData) {
  const baseGraphEdges = canonicalBaseGraphEdges(edges);
  const decisions = readCanonicalDecisions(repoRoot);
  const aliases = readCanonicalAliases(repoRoot);
  const redirects = readCanonicalRedirects(repoRoot);
  const tombstones = readCanonicalTombstones(repoRoot);
  const remediationManifests = readCanonicalRemediationManifests(repoRoot);
  const approvals = readCanonicalApprovals(repoRoot);
  const admittedRelationships = readCanonicalAdmittedRelationships(repoRoot);
  const p1DecisionPackets = readCanonicalP1DecisionPackets(repoRoot);
  const p1ReviewMetrics = p1PacketReviewMetrics(repoRoot, p1DecisionPackets);
  const groups = buildDuplicateCandidateGroups(nodes, baseGraphEdges, resourceData, decisions);
  const prioritizedGroups = applyPriorityOverrides(repoRoot, groups);
  const batches = readCanonicalBatches(repoRoot);
  const manifestValidation = validateCanonicalTransactionManifests(repoRoot);
  const nodeIds = new Set(nodes.map((node) => node.id));
  const blockers: string[] = [];
  const warnings: string[] = [];
  const aliasByKey = new Map<string, string>();
  const aliasExactKeys = new Set<string>();
  for (const alias of aliases) {
    if (!nodeIds.has(alias.canonicalNodeId)) blockers.push(`alias ${alias.alias} points to missing canonical node ${alias.canonicalNodeId}`);
    if (redirects.some((redirect) => redirect.sourceNodeId === alias.canonicalNodeId)) blockers.push(`alias ${alias.alias} points to redirected canonical node ${alias.canonicalNodeId}`);
    if (alias.sourceNodeIds.some((nodeId) => redirects.some((redirect) => redirect.sourceNodeId === nodeId))) blockers.push(`alias ${alias.alias} uses a redirected source node`);
    if (['rejected', 'deprecated'].includes(alias.status || '')) warnings.push(`alias ${alias.alias} has non-active status ${alias.status} and is ignored by canonical search`);
    if (alias.sourceNodeIds.includes(alias.canonicalNodeId)) warnings.push(`alias ${alias.alias} includes canonical node ${alias.canonicalNodeId} as a source alias participant`);
    const exactKey = `${alias.normalizedAlias}|${alias.canonicalNodeId}`;
    if (aliasExactKeys.has(exactKey)) warnings.push(`duplicate alias record for ${alias.normalizedAlias} -> ${alias.canonicalNodeId}`);
    aliasExactKeys.add(exactKey);
    const previous = aliasByKey.get(alias.normalizedAlias);
    if (previous && previous !== alias.canonicalNodeId) blockers.push(`alias collision for ${alias.normalizedAlias}: ${previous} vs ${alias.canonicalNodeId}`);
    aliasByKey.set(alias.normalizedAlias, alias.canonicalNodeId);
  }
  const redirectSources = new Set<string>();
  for (const redirect of redirects) {
    if (!nodeIds.has(redirect.sourceNodeId)) blockers.push(`redirect source missing: ${redirect.sourceNodeId}`);
    if (!nodeIds.has(redirect.canonicalNodeId)) blockers.push(`redirect canonical missing: ${redirect.canonicalNodeId}`);
    if (redirect.sourceNodeId === redirect.canonicalNodeId) blockers.push(`redirect self-cycle: ${redirect.sourceNodeId}`);
    if (aliases.some((alias) => alias.sourceNodeIds.includes(redirect.canonicalNodeId))) blockers.push(`redirect canonical target ${redirect.canonicalNodeId} is also an alias source participant`);
    if (redirectSources.has(redirect.sourceNodeId)) blockers.push(`duplicate redirect source: ${redirect.sourceNodeId}`);
    redirectSources.add(redirect.sourceNodeId);
  }
  for (const redirect of redirects) {
    let current = redirect.canonicalNodeId;
    const seen = new Set([redirect.sourceNodeId]);
    while (redirectSources.has(current)) {
      if (seen.has(current)) { blockers.push(`redirect cycle involving ${redirect.sourceNodeId}`); break; }
      seen.add(current);
      current = redirects.find((item) => item.sourceNodeId === current)!.canonicalNodeId;
    }
  }
  for (const tombstone of tombstones) {
    if (!nodeIds.has(tombstone.nodeId)) blockers.push(`tombstone node missing: ${tombstone.nodeId}`);
    if (!tombstone.reason?.trim()) blockers.push(`tombstone ${tombstone.nodeId} missing reason`);
    if (tombstone.canonicalTargetId && !nodeIds.has(tombstone.canonicalTargetId)) blockers.push(`tombstone ${tombstone.nodeId} points to missing canonical target ${tombstone.canonicalTargetId}`);
    if (tombstone.canonicalTargetId === tombstone.nodeId) blockers.push(`tombstone self-target: ${tombstone.nodeId}`);
  }
  const openRemediations = remediationManifests.filter((manifest) => manifest.status === 'open' || manifest.status === 'in_progress');
  for (const remediation of remediationManifests) {
    if (!decisions.some((decision) => decision.decisionId === remediation.decisionId)) blockers.push(`remediation ${remediation.remediationManifestId} references missing decision ${remediation.decisionId}`);
    if ((remediation.status === 'resolved' || remediation.status === 'waived') && !remediation.resolutionNotes?.trim()) blockers.push(`remediation ${remediation.remediationManifestId} resolved/waived without resolution notes`);
    for (const nodeId of remediation.affectedNodes) if (!nodeIds.has(nodeId)) warnings.push(`remediation ${remediation.remediationManifestId} references missing affected node ${nodeId}`);
  }
  for (const decision of decisions) {
    if (!decision.rationale?.trim()) blockers.push(`decision ${decision.decisionId} missing rationale`);
    if (decision.status === 'applied' && !decision.appliedAt) blockers.push(`applied decision ${decision.decisionId} missing appliedAt`);
    if ((decision.riskLevel === 'high' || decision.riskLevel === 'critical') && decision.status === 'applied' && decision.decisionType === 'MERGE_INTO_CANONICAL') blockers.push(`high-risk destructive merge applied: ${decision.decisionId}`);
    if ((decision.status === 'steward_approved' || decision.status === 'admitted') && !approvals.some((approval) => approval.decisionId === decision.decisionId && (approval.status === 'steward_approved' || approval.status === 'admitted'))) {
      blockers.push(`decision ${decision.decisionId} is ${decision.status} without active approval record`);
    }
    for (const proposal of decision.proposedRelationshipAdds || []) {
      if (!nodeIds.has(proposal.sourceNodeId)) blockers.push(`stewardship relationship proposal ${proposal.proposalId} source missing: ${proposal.sourceNodeId}`);
      if (!nodeIds.has(proposal.targetNodeId)) blockers.push(`stewardship relationship proposal ${proposal.proposalId} target missing: ${proposal.targetNodeId}`);
      if (proposal.sourceNodeId === proposal.targetNodeId) blockers.push(`stewardship relationship proposal ${proposal.proposalId} is a self-loop`);
      if (!STEWARDSHIP_RELATIONSHIP_TYPES.has(proposal.relationType)) blockers.push(`stewardship relationship proposal ${proposal.proposalId} has unsupported relation type ${proposal.relationType}`);
      if (!proposal.rationale?.trim()) blockers.push(`stewardship relationship proposal ${proposal.proposalId} missing rationale`);
      if (baseGraphEdges.some((edge) => edge.source === proposal.sourceNodeId && edge.target === proposal.targetNodeId && edge.type === proposal.relationType)) warnings.push(`stewardship relationship proposal ${proposal.proposalId} duplicates an existing production edge`);
      if (proposal.direction === 'bidirectional') {
        const hasReverse = (decision.proposedRelationshipAdds || []).some((other) => (
          other.sourceNodeId === proposal.targetNodeId
          && other.targetNodeId === proposal.sourceNodeId
          && other.relationType === proposal.relationType
        ));
        if (!hasReverse) warnings.push(`bidirectional stewardship proposal ${proposal.proposalId} has no reverse proposal`);
      }
    }
    if (DISAMBIGUATION_DECISION_TYPES.has(decision.decisionType) && decision.status === 'applied') {
      warnings.push(`disambiguation decision ${decision.decisionId} is applied as stewardship metadata only; verify no production graph edge admission was intended`);
    }
    if (decision.status === 'rollback_partial' && !remediationManifests.some((manifest) => manifest.decisionId === decision.decisionId)) {
      blockers.push(`partial rollback decision ${decision.decisionId} is missing remediation manifest`);
    }
  }
  for (const approval of approvals) {
    const decision = decisions.find((entry) => entry.decisionId === approval.decisionId);
    if (!decision) blockers.push(`approval ${approval.approvalId} references missing decision ${approval.decisionId}`);
    if (!approval.decisionHash?.trim()) blockers.push(`approval ${approval.approvalId} missing decisionHash`);
    if (decision && approval.decisionHash && approval.decisionHash !== decisionApprovalHash(decision, approval.mutationScope)) blockers.push(`approval ${approval.approvalId} decisionHash does not match current decision payload`);
    if (!approval.approvedBy?.trim()) blockers.push(`approval ${approval.approvalId} missing approvedBy`);
    if (!approval.reviewerRole?.trim()) blockers.push(`approval ${approval.approvalId} missing reviewerRole`);
    if (!approval.approvalRationale?.trim()) blockers.push(`approval ${approval.approvalId} missing approvalRationale`);
    if (!approval.rollbackPlan?.trim()) blockers.push(`approval ${approval.approvalId} missing rollbackPlan`);
    if (!approval.validationSnapshot) blockers.push(`approval ${approval.approvalId} missing validationSnapshot`);
    if ((approval.status === 'steward_approved' || approval.status === 'admitted') && !approval.transactionManifestId) blockers.push(`approval ${approval.approvalId} missing transactionManifestId`);
    if (decision && (decision.riskLevel === 'high' || decision.riskLevel === 'critical') && !approval.riskAcknowledgment && approval.status !== 'rejected') blockers.push(`approval ${approval.approvalId} missing high-risk acknowledgment`);
    if (approval.approvalSource === 'test_fixture' && decision?.sourceNodeIds.some(isProductionNodeId)) blockers.push(`approval ${approval.approvalId} uses test_fixture for production VTN-DOM decision`);
    if (approval.mutationScope === 'non_destructive_edge_admission' && approval.status === 'admitted') {
      if (!approval.admittedBy?.trim()) blockers.push(`admitted approval ${approval.approvalId} missing admittedBy`);
      if (!approval.admittedAt) blockers.push(`admitted approval ${approval.approvalId} missing admittedAt`);
      if (!approval.admissionTransactionId) blockers.push(`admitted approval ${approval.approvalId} missing admissionTransactionId`);
      if (!approval.postAdmissionValidationSnapshot) blockers.push(`admitted approval ${approval.approvalId} missing postAdmissionValidationSnapshot`);
    }
  }
  const activeAdmittedEdgeKeys = new Set<string>();
  for (const edge of admittedRelationships) {
    if (edge.reviewStatus === 'rolled_back') continue;
    const decision = decisions.find((entry) => entry.decisionId === edge.stewardshipDecisionId);
    const approval = approvals.find((entry) => entry.approvalId === edge.approvalId);
    if (!nodeIds.has(edge.source)) blockers.push(`admitted relationship ${edge.id} source missing: ${edge.source}`);
    if (!nodeIds.has(edge.target)) blockers.push(`admitted relationship ${edge.id} target missing: ${edge.target}`);
    if (!decision) blockers.push(`admitted relationship ${edge.id} references missing decision ${edge.stewardshipDecisionId}`);
    if (!approval) blockers.push(`admitted relationship ${edge.id} references missing approval ${edge.approvalId}`);
    if (!ADMITTED_RELATIONSHIP_TYPES.has(edge.type as CanonicalStewardshipRelationType)) blockers.push(`admitted relationship ${edge.id} has invalid relation type ${edge.type}`);
    if (edge.type === 'CROSS_DOMAIN_EQUIVALENT') blockers.push(`admitted relationship ${edge.id} uses over-strong CROSS_DOMAIN_EQUIVALENT`);
    if (!edge.rationale?.trim()) blockers.push(`admitted relationship ${edge.id} missing rationale`);
    if (edge.confidence == null) blockers.push(`admitted relationship ${edge.id} missing confidence`);
    if (typeof edge.weight !== 'number') blockers.push(`admitted relationship ${edge.id} missing numeric weight`);
    if (edge.source === edge.target) blockers.push(`admitted relationship ${edge.id} is a self-loop`);
    const key = `${edge.source}|${edge.type}|${edge.target}`;
    if (activeAdmittedEdgeKeys.has(key)) blockers.push(`duplicate admitted relationship tuple: ${key}`);
    activeAdmittedEdgeKeys.add(key);
    if (baseGraphEdges.some((candidate) => candidate.source === edge.source && candidate.target === edge.target && candidate.type === edge.type)) blockers.push(`admitted relationship ${edge.id} duplicates production graph edge tuple`);
    if (edge.type === 'CROSS_DOMAIN_ALIGNMENT' || edge.direction === 'bidirectional') {
      const reverse = admittedRelationships.find((other) => other.reviewStatus !== 'rolled_back' && other.source === edge.target && other.target === edge.source && other.type === edge.type && other.stewardshipDecisionId === edge.stewardshipDecisionId && other.approvalId === edge.approvalId);
      if (!reverse) blockers.push(`cross-domain alignment admitted relationship ${edge.id} missing reciprocal pair`);
    }
  }
  const currentP1SourceSnapshot = buildP1SourceSnapshot(repoRoot, prioritizedGroups, baseGraphEdges, { nodes, resourceData });
  const currentGroupById = new Map(prioritizedGroups.map((group) => [group.groupId, group]));
  const packetRunSnapshotHashes = new Map<string, string>();
  const p1StalePacketIds = new Set<string>();
  let p1PacketsMissingSourceSnapshot = 0;
  let p1PacketsStaleSourceSnapshot = 0;
  let p1PacketsTamperedSourceSnapshot = 0;
  let p1PacketsContentHashMismatch = 0;
  let p1PacketsSigned = 0;
  let p1PacketsUnsigned = 0;
  let p1PacketsInvalidSignature = 0;
  let p1PacketsMissingKey = 0;
  let p1PacketsStrictSignatureBlockers = 0;
  let p1PacketsConsumedByAdmission = 0;
  let p1PacketsMetadataDisambiguationAdmitted = 0;
  const signatureAlgorithmCounts: Record<string, number> = {};
  const signatureScopeCounts: Record<string, number> = {};
  const signatureStrictMode = requireP1PacketSignatures();
  const approvalIds = new Set(approvals.map((approval) => approval.approvalId));
  const admittedDecisionIds = new Set(decisions.filter((decision) => ['admitted', 'steward_approved', 'applied'].includes(decision.status)).map((decision) => decision.decisionId));
  const activeAdmittedRelationshipIds = new Set(admittedRelationships.filter((edge) => edge.reviewStatus !== 'rolled_back').map((edge) => edge.id));
  for (const packet of p1DecisionPackets) {
    if (!packet.packetId || !packet.groupId || !packet.generatedAt || !packet.normalizedLabel) blockers.push(`P1 decision packet missing required fields: ${packet.packetId || packet.groupId || 'unknown'}`);
    if (!packet.schemaVersion) warnings.push(`P1 decision packet ${packet.packetId} missing schemaVersion`);
    if (!packet.packetRunId) warnings.push(`P1 decision packet ${packet.packetId} missing packetRunId`);
    if (!packet.packetContentHash) {
      warnings.push(`P1 decision packet ${packet.packetId} missing packetContentHash`);
    } else if (p1PacketContentHash(packet) !== packet.packetContentHash) {
      p1PacketsContentHashMismatch += 1;
      blockers.push(`P1 decision packet ${packet.packetId} packetContentHash mismatch`);
    }
    const signatureCheck = verifyP1PacketSignature(packet);
    signatureAlgorithmCounts[signatureCheck.signatureAlgorithm] = (signatureAlgorithmCounts[signatureCheck.signatureAlgorithm] || 0) + 1;
    signatureScopeCounts[signatureCheck.signatureScope] = (signatureScopeCounts[signatureCheck.signatureScope] || 0) + 1;
    if (signatureCheck.status === 'valid') {
      p1PacketsSigned += 1;
    } else if (signatureCheck.status === 'unsigned') {
      p1PacketsUnsigned += 1;
      const message = `P1 decision packet ${packet.packetId} is unsigned; packet signatures are authenticity aids only and do not imply approval or truth`;
      if (signatureStrictMode) {
        p1PacketsStrictSignatureBlockers += 1;
        blockers.push(message);
      } else {
        warnings.push(message);
      }
    } else if (signatureCheck.status === 'missing_key') {
      p1PacketsMissingKey += 1;
      const message = `P1 decision packet ${packet.packetId} signature cannot be verified because no packet HMAC key is configured`;
      if (signatureStrictMode) {
        p1PacketsStrictSignatureBlockers += 1;
        blockers.push(message);
      } else {
        warnings.push(message);
      }
    } else if (signatureCheck.status === 'invalid') {
      p1PacketsInvalidSignature += 1;
      blockers.push(`P1 decision packet ${packet.packetId} HMAC signature mismatch`);
    } else {
      p1PacketsInvalidSignature += 1;
      blockers.push(`P1 decision packet ${packet.packetId} uses unsupported signature metadata`);
    }
    if (packet.truthCaveat !== 'advisory_packet_only_not_steward_approval_not_canonical_admission') warnings.push(`P1 decision packet ${packet.packetId} missing advisory truth caveat`);
    const currentGroup = currentGroupById.get(packet.groupId);
    if (!packet.groupInputHash) {
      warnings.push(`P1 decision packet ${packet.packetId} missing groupInputHash`);
    } else if (currentGroup && packet.groupInputHash !== hash(stableStringify(compactGroupForSnapshot(currentGroup)))) {
      p1StalePacketIds.add(packet.packetId);
      warnings.push(`P1 decision packet ${packet.packetId} groupInputHash is stale relative to current duplicate group state`);
    }
    if (!packet.sourceSnapshot) {
      p1PacketsMissingSourceSnapshot += 1;
      warnings.push(`P1 decision packet ${packet.packetId} missing sourceSnapshot evidence lock`);
    } else {
      const selfHash = p1SourceSnapshotHash(packet.sourceSnapshot);
      if (selfHash !== packet.sourceSnapshot.snapshotHash) {
        p1PacketsTamperedSourceSnapshot += 1;
        blockers.push(`P1 decision packet ${packet.packetId} sourceSnapshot hash mismatch`);
      }
      if (packet.sourceSnapshot.snapshotHash !== currentP1SourceSnapshot.snapshotHash) {
        p1StalePacketIds.add(packet.packetId);
        warnings.push(`P1 decision packet ${packet.packetId} sourceSnapshot is stale relative to current graph/resource/canonical state`);
      }
      if (packet.packetRunId) {
        const existingSnapshotHash = packetRunSnapshotHashes.get(packet.packetRunId);
        if (existingSnapshotHash && existingSnapshotHash !== packet.sourceSnapshot.snapshotHash) blockers.push(`P1 decision packet run ${packet.packetRunId} has inconsistent sourceSnapshot hashes`);
        packetRunSnapshotHashes.set(packet.packetRunId, packet.sourceSnapshot.snapshotHash);
      }
    }
    if (packet.priorityBand !== 'P1') warnings.push(`decision packet ${packet.packetId} is not P1 (${packet.priorityBand})`);
    if (packet.recommendedDecisionType === 'MERGE_INTO_CANONICAL') blockers.push(`P1 decision packet ${packet.packetId} recommends destructive merge`);
    if (!packet.rationale?.trim() || !packet.nextAction?.trim()) blockers.push(`P1 decision packet ${packet.packetId} missing rationale or nextAction`);
    if (packet.mergeApplied || packet.aliasApplied || packet.redirectApplied || packet.tombstoneApplied || packet.productionGraphWritePerformed || packet.resourceLinkRewritePerformed || packet.admittedRelationshipWritten) {
      blockers.push(`P1 decision packet ${packet.packetId} records a mutation flag; packet phase must remain non-destructive`);
    }
    if (packet.packetAdmissionStatus === 'consumed_by_non_destructive_admission') {
      p1PacketsConsumedByAdmission += 1;
      if (!packet.approvalIds?.length) blockers.push(`P1 decision packet ${packet.packetId} is consumed by admission but has no approvalIds`);
      if (!packet.admittedDecisionIds?.length) blockers.push(`P1 decision packet ${packet.packetId} is consumed by admission but has no admittedDecisionIds`);
      if (!packet.admittedRelationshipIds?.length) blockers.push(`P1 decision packet ${packet.packetId} is consumed by relationship admission but has no admittedRelationshipIds`);
    } else if (packet.packetAdmissionStatus === 'metadata_disambiguation_admitted') {
      p1PacketsMetadataDisambiguationAdmitted += 1;
      if (!packet.approvalIds?.length) blockers.push(`P1 decision packet ${packet.packetId} is metadata-disambiguation admitted but has no approvalIds`);
      if (!packet.admittedDecisionIds?.length) blockers.push(`P1 decision packet ${packet.packetId} is metadata-disambiguation admitted but has no admittedDecisionIds`);
      if (packet.admittedRelationshipIds?.length) blockers.push(`P1 decision packet ${packet.packetId} metadata-only admission must not imply admitted graph relationships`);
    }
    for (const approvalId of packet.approvalIds || []) {
      if (!approvalIds.has(approvalId)) blockers.push(`P1 decision packet ${packet.packetId} references missing approval ${approvalId}`);
    }
    for (const decisionId of packet.admittedDecisionIds || []) {
      if (!admittedDecisionIds.has(decisionId)) blockers.push(`P1 decision packet ${packet.packetId} references missing admitted/steward-approved decision ${decisionId}`);
    }
    for (const relationshipId of packet.admittedRelationshipIds || []) {
      if (!activeAdmittedRelationshipIds.has(relationshipId)) blockers.push(`P1 decision packet ${packet.packetId} references missing active admitted relationship ${relationshipId}`);
    }
  }
  p1PacketsStaleSourceSnapshot = p1StalePacketIds.size;
  blockers.push(...p1ReviewMetrics.p1PacketReviewBlockers);
  warnings.push(...p1ReviewMetrics.p1PacketReviewWarnings);
  const resourceLinksToRedirected = (resourceData?.nodeResourceLinks || []).filter((link) => redirectSources.has(link.nodeId));
  if (resourceLinksToRedirected.length) warnings.push(`${resourceLinksToRedirected.length} resource links point to redirected nodes and rely on canonical redirect preservation`);
  const appliedDecisions = decisions.filter((decision) => decision.status === 'applied').length;
  const admittedDecisions = decisions.filter((decision) => decision.status === 'admitted').length;
  const transactionManifests = manifestValidation.count;
  if ((appliedDecisions > 0 || admittedDecisions > 0) && transactionManifests === 0) blockers.push('applied/admitted canonical decisions require transaction manifests');
  blockers.push(...manifestValidation.blockers);
  warnings.push(...manifestValidation.warnings);
  const groupsByRisk = countsBy(prioritizedGroups.map((group) => group.riskLevel));
  const groupsByPriority = countsBy(prioritizedGroups.map((group) => group.priorityBand));
  return {
    ok: blockers.length === 0,
    schemaVersion: CANONICAL_STEWARDSHIP_SCHEMA_VERSION,
    generatedAt: nowIso(),
    duplicateGroups: groups.length,
    unresolvedDuplicateGroups: groups.filter((group) => group.status === 'unresolved').length,
    concreteDuplicateGroups: groups.filter((group) => group.looseNormalizedLabel.includes('concrete')).length,
    groupsByRisk,
    groupsByPriority,
    p0UnresolvedGroups: prioritizedGroups.filter((group) => group.priorityBand === 'P0' && group.status === 'unresolved').length,
    concreteGroupStatus: prioritizedGroups.filter((group) => group.looseNormalizedLabel.includes('concrete')).map((group) => ({
      groupId: group.groupId,
      label: group.looseNormalizedLabel,
      priorityBand: group.priorityBand,
      status: group.status,
      riskLevel: group.riskLevel,
      nodeIds: group.nodeIds,
    })),
    batchCount: batches.length,
    batchDecisionCount: batches.reduce((sum, batch) => sum + batch.decisions.length, 0),
    stewardshipDecisions: decisions.length,
    appliedDecisions,
    admittedDecisions,
    approvals: approvals.length,
    admittedRelationships: admittedRelationships.filter((edge) => edge.reviewStatus !== 'rolled_back').length,
    p1DecisionPackets: p1DecisionPackets.length,
    p1PacketsTotal: p1DecisionPackets.length,
    p1PacketsWithOntologyReview: p1ReviewMetrics.p1PacketsWithOntologyReview,
    p1PacketsUnreviewed: p1ReviewMetrics.p1PacketsUnreviewed,
    p1PacketsKimiReviewRequested: p1ReviewMetrics.p1PacketsKimiReviewRequested,
    p1PacketsKimiReviewed: p1ReviewMetrics.p1PacketsKimiReviewed,
    p1PacketsHumanReviewNeeded: p1ReviewMetrics.p1PacketsHumanReviewNeeded,
    p1PacketsHumanReviewed: p1ReviewMetrics.p1PacketsHumanReviewed,
    p1PacketsRejected: p1ReviewMetrics.p1PacketsRejected,
    p1PacketsDeferred: p1ReviewMetrics.p1PacketsDeferred,
    p1PacketReviewInvalid: p1ReviewMetrics.p1PacketReviewInvalid,
    p1PacketReviewMissingReviewer: p1ReviewMetrics.p1PacketReviewMissingReviewer,
    p1PacketReviewMissingSummary: p1ReviewMetrics.p1PacketReviewMissingSummary,
    p1PacketReviewMissingNextAction: p1ReviewMetrics.p1PacketReviewMissingNextAction,
    p1PacketReviewHashMismatch: p1ReviewMetrics.p1PacketReviewHashMismatch,
    p1PacketReviewReferencesMissingPacket: p1ReviewMetrics.p1PacketReviewReferencesMissingPacket,
    p1PacketReviewStale: p1ReviewMetrics.p1PacketReviewStale,
    p1PacketReviewsCarriedForward: p1ReviewMetrics.p1PacketReviewsCarriedForward,
    p1PacketsCarriedForward: p1ReviewMetrics.p1PacketsCarriedForward,
    p1PacketsConsumedByAdmission,
    p1PacketsMetadataDisambiguationAdmitted,
    p1PacketReviewDoesNotMutateGraph: p1ReviewMetrics.p1PacketReviewDoesNotMutateGraph,
    p1PacketReviewTransactionManifests: p1ReviewMetrics.p1PacketReviewTransactionManifests,
    p1PacketReviewStrictMode: p1ReviewMetrics.p1PacketReviewStrictMode,
    p1PacketReviewWarnings: p1ReviewMetrics.p1PacketReviewWarnings,
    p1PacketReviewBlockers: p1ReviewMetrics.p1PacketReviewBlockers,
    p1PacketsSigned,
    p1PacketsUnsigned,
    p1PacketsInvalidSignature,
    p1PacketsMissingKey,
    p1PacketsStrictSignatureBlockers,
    p1PacketsContentHashMismatch,
    p1PacketsMissingSourceSnapshot,
    p1PacketsStaleSourceSnapshot,
    p1PacketsTamperedSourceSnapshot,
    signatureAlgorithmCounts,
    signatureScopeCounts,
    rollbackableDecisions: decisions.filter((decision) => ['applied', 'proposed', 'steward_approved', 'admitted'].includes(decision.status)).length,
    rollbackBlockedDecisions: decisions.filter((decision) => decision.status === 'rolled_back').length,
    aliases: aliases.length,
    redirects: redirects.length,
    tombstones: tombstones.length,
    aliasCycles: 0,
    redirectCycles: blockers.filter((blocker) => blocker.includes('redirect cycle')).length,
    tombstonePolicyViolations: blockers.filter((blocker) => blocker.includes('tombstone')).length,
    governedDisambiguationDecisions: decisions.filter((decision) => decision.decisionType === 'GOVERNED_DISAMBIGUATION').length,
    disambiguatedKeepSeparateDecisions: decisions.filter((decision) => decision.decisionType === 'DISAMBIGUATED_KEEP_SEPARATE').length,
    relatedSpecializationDecisions: decisions.filter((decision) => decision.decisionType === 'RELATED_SPECIALIZATION').length,
    crossDomainEquivalenceDecisions: decisions.filter((decision) => decision.decisionType === 'CROSS_DOMAIN_EQUIVALENCE').length,
    graphStewardshipEdgeProposals: decisions.reduce((sum, decision) => sum + (decision.proposedRelationshipAdds?.length || 0), 0),
    openRemediationManifests: openRemediations.length,
    remediationManifestCount: remediationManifests.length,
    partialRollbackDecisionsWithoutRemediation: decisions.filter((decision) => decision.status === 'rollback_partial' && !remediationManifests.some((manifest) => manifest.decisionId === decision.decisionId)).length,
    brokenRedirects: blockers.filter((blocker) => blocker.includes('redirect')).length,
    edgePreservationIssues: 0,
    resourceLinkPreservationIssues: 0,
    highRiskUnappliedCandidates: groups.filter((group) => (group.riskLevel === 'high' || group.riskLevel === 'critical') && group.status === 'unresolved').length,
    transactionManifests,
    invalidManifestCount: manifestValidation.invalidManifestCount,
    brokenHashChainCount: manifestValidation.brokenHashChainCount,
    unsignedManifestWarnings: manifestValidation.unsignedManifestWarnings,
    transactionManifestsWithAfterHash: manifestValidation.transactionManifestsWithAfterHash,
    filesUnderManifestCustody: manifestValidation.filesUnderManifestCustody,
    latestAfterHashMatches: manifestValidation.latestAfterHashMatches,
    latestAfterHashMismatches: manifestValidation.latestAfterHashMismatches,
    staleManifestFiles: manifestValidation.staleManifestFiles,
    unmanifestedMutatedCustodyFiles: manifestValidation.unmanifestedMutatedCustodyFiles,
    manifestChainValid: manifestValidation.manifestChainValid,
    manifestSignatureValid: manifestValidation.manifestSignatureValid,
    latestManifestAfterHashStrictMode: manifestValidation.latestManifestAfterHashStrictMode,
    manifestAfterHashStatuses: manifestValidation.manifestAfterHashStatuses,
    blockers,
    warnings,
  };
}
