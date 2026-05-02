export interface GraphNode {
  id: string;
  label: string;
  displayLabel?: string;
  type: string;
  kind?: string;
  summary?: string;
  slug?: string;
  status?: string;
  confidence?: number;
  aliases?: string[];
  taxonomy_path?: string[];
  createdAt?: string;
  updatedAt?: string;
  radius?: number;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  reasoning?: string;
  confidence?: number;
  assertionId?: string;
  relationType?: string;
  relationCategory?: string;
  relationNature?: string[];
  direction?: string;
  edgeDirection?: string;
  weight?: number;
  confidenceScore?: number;
  discipline?: string[];
  lifecyclePhase?: string[];
  sourceFamilyIds?: string[];
  rationale?: string;
  provenanceNote?: string;
  generationMethod?: string;
  reviewStatus?: string;
  semanticOverlayCategory?: string;
  applicabilityBasis?: string;
  jurisdictionContext?: string;
  designBasisStatus?: string;
}

export interface TaxonomyNode {
  id: string;
  label: string;
  displayLabel?: string;
  kind: 'taxonomy' | 'topic' | 'subtopic' | 'concept' | 'rule';
  conceptCount: number;
  children: TaxonomyNode[];
}

export interface EvidenceSpan {
  id: string;
  quote: string;
  normalized_text?: string;
  deep_link?: string;
  document_id?: string;
  document_title?: string;
  confidence?: number;
}

export interface ResourceReference {
  linkId: string;
  resourceId: string;
  nodeId: string;
  title: string;
  subtitle?: string;
  authors?: string[];
  organization?: string;
  publisher?: string;
  year?: number;
  resourceType: string;
  sourceAuthority: string;
  sourceFamilyIds?: string[];
  authorityTier?: number;
  accessType: string;
  verificationStatus: string;
  reviewStatus: string;
  relationship: string;
  relevanceScore: number;
  authorityScore: number;
  confidenceScore: number;
  displayScore: number;
  rationale: string;
  pageRefs?: string[];
  chapterRefs?: string[];
  sectionRefs?: string[];
  jurisdiction?: string;
  geographicScope?: string;
  url?: string;
  canonicalUrl?: string;
  doi?: string;
  isbn13?: string;
  localFileName?: string;
  localFileType?: string;
  licenseNotes?: string;
  lastCheckedAt?: string;
  warning?: string;
}

export interface ResourceReviewMetrics {
  resourcesTotal?: number;
  resourcesNonRejected?: number;
  resourcesWithAcceptedLinks?: number;
  acceptedNodeResourceLinks?: number;
  candidateResources?: number;
  rejectedResources?: number;
  needsReviewResources?: number;
  acceptedResources: number;
  acceptedLinks: number;
  needsReviewLinks: number;
  rejectedLinks: number;
  candidateLinks?: number;
  candidates: number;
  localFilesIndexed: number;
  localFilesAdmitted: number;
  standardsMissingContext: number;
  duplicateWarnings: number;
  brokenLinkWarnings: number;
  validationWarnings?: number;
  validationErrors?: number;
  validationBlockers?: number;
  reviewDecisions?: number;
  authorityTierDistribution?: Record<string, number>;
  sourceFamilyDistribution?: Record<string, number>;
}

export interface CanonicalDuplicateNodeSummary {
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

export interface CanonicalStewardshipDecision {
  decisionId: string;
  decisionType: string;
  candidateGroupId: string;
  canonicalNodeId?: string;
  sourceNodeIds: string[];
  affectedEdgeIds: string[];
  affectedResourceLinkIds: string[];
  affectedAliases: string[];
  affectedSearchTerms: string[];
  reviewer: string;
  createdAt: string;
  rationale: string;
  riskLevel: string;
  status: string;
  appliedAt?: string;
  rollbackCapability?: string;
  notes?: string;
  affectedNodeIds?: string[];
  proposedRelationshipAdds?: Array<Record<string, unknown>>;
  searchDisambiguationText?: string;
  transactionManifestId?: string;
}

export interface CanonicalStewardshipApproval {
  approvalId: string;
  decisionId: string;
  groupId: string;
  decisionHash?: string;
  approvedBy: string;
  reviewerRole: string;
  approvalSource: string;
  approvedAt: string;
  approvalRationale: string;
  riskAcknowledgment: boolean;
  mutationScope: string;
  rollbackPlan: string;
  status: string;
  transactionManifestId?: string;
  admittedAt?: string;
  admittedBy?: string;
  admissionTransactionId?: string;
}

export interface CanonicalAdmittedRelationship {
  id: string;
  source: string;
  target: string;
  type: string;
  relationType?: string;
  relationCategory?: string;
  direction?: string;
  rationale?: string;
  stewardshipDecisionId: string;
  approvalId: string;
  reviewStatus: string;
}

export interface CanonicalP1DecisionPacket {
  packetId: string;
  packetContentHash?: string;
  packetRunId?: string;
  groupId: string;
  generatedAt?: string;
  truthCaveat?: string;
  normalizedLabel: string;
  priorityBand: string;
  riskLevel: string;
  candidateCategory: string;
  nodeIds: string[];
  sourceSnapshot?: {
    schemaVersion?: string;
    hashAlgorithm?: string;
    staleCheckPolicy?: string;
    graphNodeCount?: number;
    graphEdgeCount?: number;
    duplicateGroupCount?: number;
    p1CandidateGroupCount?: number;
    resourceCount?: number;
    nodeResourceLinkCount?: number;
    stewardshipDecisionCount?: number;
    approvalCount?: number;
    admittedRelationshipCount?: number;
    aliasCount?: number;
    redirectCount?: number;
    tombstoneCount?: number;
    nodesHash?: string;
    edgesHash?: string;
    groupsHash?: string;
    resourcesHash?: string;
    decisionsHash?: string;
    approvalsHash?: string;
    admittedRelationshipsHash?: string;
    aliasesHash?: string;
    redirectsHash?: string;
    tombstonesHash?: string;
    priorityOverridesHash?: string;
    snapshotHash?: string;
  };
  groupInputHash?: string;
  candidateEdgeNeighborhoodHash?: string;
  signature?: {
    signatureStatus?: 'unsigned' | 'valid' | 'invalid' | 'missing_key' | 'unsupported' | string;
    signatureAlgorithm?: string;
    signatureScope?: string;
    signature?: string;
    signedAt?: string;
    signedBy?: string;
    signerId?: string;
    systemSignerId?: string;
    keyId?: string;
    signaturePayloadHash?: string;
    signatureVerificationCheckedAt?: string;
  };
  resourceLinkCount: number;
  recommendedDecisionType: string;
  needsKimiReview: boolean;
  needsHumanDomainReview: boolean;
  mergeSafety: string;
  rationale: string;
  nextAction: string;
  edgeSummary?: Record<string, unknown>;
}

export interface CanonicalDuplicateGroup {
  groupId: string;
  normalizedLabel: string;
  looseNormalizedLabel: string;
  labels: string[];
  nodes: CanonicalDuplicateNodeSummary[];
  nodeIds: string[];
  candidateCategory: string;
  riskLevel: string;
  riskScore: number;
  suggestedAction: string;
  riskReasons: string[];
  priorityBand: 'P0' | 'P1' | 'P2' | 'P3' | 'BLOCKED';
  priorityScore: number;
  priorityReasons: string[];
  edgeCount: number;
  resourceLinkCount: number;
  existingDecisions: CanonicalStewardshipDecision[];
  status: string;
}

export interface CanonicalDuplicateQueue {
  schemaVersion: string;
  generatedAt: string;
  groups: CanonicalDuplicateGroup[];
  total: number;
}

export interface CanonicalBatchRecord {
  batchId: string;
  name: string;
  filters: Record<string, unknown>;
  groupIds: string[];
  status: string;
  reviewer?: string;
  priorityBand?: string;
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
  decisions: Array<Record<string, unknown>>;
}

export interface CanonicalDecisionPreview {
  dryRun: boolean;
  decisionType: string;
  candidateGroupId: string;
  canonicalNodeId?: string;
  sourceNodeIds: string[];
  affectedEdgeIds: string[];
  affectedResourceLinkIds: string[];
  affectedAliases: string[];
  affectedSearchTerms: string[];
  affectedNodeIds?: string[];
  edgeRewrites: unknown[];
  duplicateEdgeConsolidations: string[];
  selfLoopRisks: string[];
  resourceLinkRewrites: unknown[];
  proposedRelationshipAdds?: Array<Record<string, unknown>>;
  searchDisambiguationText?: string;
  warnings: string[];
  blockers: string[];
  riskLevel: string;
  riskScore: number;
  beforeSnapshot: unknown;
  afterPreview: unknown;
}

export interface CanonicalValidationResult {
  ok: boolean;
  duplicateGroups: number;
  unresolvedDuplicateGroups: number;
  concreteDuplicateGroups: number;
  groupsByRisk?: Record<string, number>;
  groupsByPriority?: Record<string, number>;
  p0UnresolvedGroups?: number;
  batchCount?: number;
  batchDecisionCount?: number;
  approvals?: number;
  admittedDecisions?: number;
  admittedRelationships?: number;
  p1DecisionPackets?: number;
  p1PacketsTotal?: number;
  p1PacketsSigned?: number;
  p1PacketsUnsigned?: number;
  p1PacketsInvalidSignature?: number;
  p1PacketsMissingKey?: number;
  p1PacketsStrictSignatureBlockers?: number;
  p1PacketsContentHashMismatch?: number;
  p1PacketsMissingSourceSnapshot?: number;
  p1PacketsStaleSourceSnapshot?: number;
  p1PacketsTamperedSourceSnapshot?: number;
  signatureAlgorithmCounts?: Record<string, number>;
  signatureScopeCounts?: Record<string, number>;
  stewardshipDecisions: number;
  appliedDecisions: number;
  rollbackableDecisions?: number;
  rollbackBlockedDecisions?: number;
  aliases: number;
  redirects: number;
  tombstones?: number;
  aliasCycles?: number;
  redirectCycles?: number;
  tombstonePolicyViolations?: number;
  governedDisambiguationDecisions?: number;
  disambiguatedKeepSeparateDecisions?: number;
  relatedSpecializationDecisions?: number;
  crossDomainEquivalenceDecisions?: number;
  graphStewardshipEdgeProposals?: number;
  openRemediationManifests?: number;
  remediationManifestCount?: number;
  partialRollbackDecisionsWithoutRemediation?: number;
  blockers: string[];
  warnings: string[];
  highRiskUnappliedCandidates?: number;
  transactionManifests?: number;
  invalidManifestCount?: number;
  brokenHashChainCount?: number;
  unsignedManifestWarnings?: number;
  transactionManifestsWithAfterHash?: number;
  filesUnderManifestCustody?: number;
  latestAfterHashMatches?: number;
  latestAfterHashMismatches?: number;
  staleManifestFiles?: number;
  unmanifestedMutatedCustodyFiles?: number;
  manifestChainValid?: boolean;
  manifestSignatureValid?: boolean;
  latestManifestAfterHashStrictMode?: boolean;
  manifestAfterHashStatuses?: Array<{
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
  }>;
}

export interface ResourceReviewLinkItem {
  type: 'node_resource_link';
  id: string;
  title: string;
  nodeId: string;
  resourceId: string;
  sourceFamilyIds: string[];
  authorityTier?: number;
  authorityScore?: number;
  verificationStatus: string;
  reviewStatus: string;
  relationship: string;
  rationale: string;
  reviewNotes?: string;
  missingStandardContext?: boolean;
  warnings: string[];
  resource?: Partial<ResourceReference> & Record<string, unknown>;
  link?: Record<string, unknown>;
}

export interface ResourceReviewCandidateItem {
  type: 'candidate';
  id: string;
  title: string;
  nodeId?: string;
  rawUrl?: string;
  rawIdentifier?: string;
  preliminaryScore: number;
  rankingScore: number;
  reviewStatus: string;
  dedupeKey?: string;
  duplicateResourceId?: string;
  sourceFamilyIds: string[];
  authorityTier?: number;
  warnings: string[];
  suggestedNodeId?: string;
  suggestedResourceId?: string;
  candidate?: Record<string, unknown>;
}

export interface ResourceReviewLocalFileItem {
  type: 'local_file';
  id: string;
  fileId: string;
  title: string;
  localPath?: string;
  localFileHash?: string;
  localFileType?: string;
  localFileSizeBytes?: number;
  linkedNodeCount: number;
  admitted: boolean;
  admittedResourceId?: string;
  reviewStatus: string;
  sourceFamilyIds: string[];
  authorityTier?: number;
  warnings: string[];
  resource?: Record<string, unknown>;
}

export interface ResourceReviewQueue {
  schemaVersion: string;
  generatedAt: string;
  needsReviewLinks: ResourceReviewLinkItem[];
  rejectedLinks: ResourceReviewLinkItem[];
  acceptedLinks: ResourceReviewLinkItem[];
  candidateLinks: ResourceReviewLinkItem[];
  candidates: ResourceReviewCandidateItem[];
  localFiles: ResourceReviewLocalFileItem[];
  standardsMissingContext: ResourceReviewLinkItem[];
  validationWarnings: string[];
  validationErrors: string[];
  validationBlockers?: string[];
  metrics: ResourceReviewMetrics;
}

export interface ResourceReviewCandidatesResponse {
  candidates: ResourceReviewCandidateItem[];
}

export interface ResourceReviewLocalFilesResponse {
  localFiles: ResourceReviewLocalFileItem[];
  indexedResourceCount: number;
  scannedDirectories?: string[];
  errors?: string[];
}

export interface ResourceReviewStandardsResponse {
  standards: ResourceReviewLinkItem[];
}

export interface NodeDetail {
  node: GraphNode;
  taxonomyPath: TaxonomyNode[];
  incoming: RelationDetail[];
  outgoing: RelationDetail[];
  evidence: EvidenceSpan[];
  resources?: ResourceReference[];
  canonical?: Record<string, unknown> & {
    status?: string;
    canonicalNodeId?: string;
    duplicateGroupIds?: string[];
  };
}

export interface RelationDetail {
  relType: string;
  other: GraphNode;
  reasoning?: string;
  confidence?: number;
  assertionId?: string;
  relationshipId?: string;
  sourceNodeId?: string;
  targetNodeId?: string;
  category?: 'hierarchy' | 'semantic' | string;
  isHierarchyEdge?: boolean;
  isSemanticEdge?: boolean;
  visibility?: {
    canvasEdgeType?: string;
    defaultVisible?: boolean;
    hiddenReasons?: string[];
  };
  relationType?: string;
  relationCategory?: string;
  relationNature?: string[];
  edgeDirection?: string;
  weight?: number;
  confidenceScore?: number;
  discipline?: string[];
  lifecyclePhase?: string[];
  sourceFamilyIds?: string[];
  rationale?: string;
  provenanceNote?: string;
  generationMethod?: string;
  reviewStatus?: string;
  semanticOverlayCategory?: string;
  applicabilityBasis?: string;
  jurisdictionContext?: string;
  designBasisStatus?: string;
}

export interface EdgeDetail {
  edge: GraphEdge;
  source: GraphNode;
  target: GraphNode;
  evidence: EvidenceSpan[];
}

export interface GraphNeighborhoodRelationship {
  id: string;
  sourceNodeId: string;
  targetNodeId: string;
  relationType: string;
  direction: 'incoming' | 'outgoing' | 'self' | 'undirected';
  label: string;
  category: 'hierarchy' | 'semantic';
  isHierarchyEdge: boolean;
  isSemanticEdge: boolean;
  sourceNode?: GraphNode;
  targetNode?: GraphNode;
}

export interface GraphNeighborhoodResponse {
  schemaVersion: string;
  source: string;
  nodeId: string;
  depth: number;
  limit: number;
  nodes: GraphNode[];
  edges: GraphEdge[];
  relationships: GraphNeighborhoodRelationship[];
  relationshipCounts: {
    totalDirect: number;
    visibleDirect: number;
    hiddenDirect: number;
    incoming: number;
    outgoing: number;
    hierarchy: number;
    semantic: number;
  };
  hiddenRelationships: Array<{
    id: string;
    sourceNodeId: string;
    targetNodeId: string;
    relationType: string;
    hiddenReasons: string[];
  }>;
  filters: {
    direction: string;
    includeHierarchyEdges: boolean;
    includeSemanticEdges: boolean;
    relTypes?: string[];
  };
  truncated: boolean;
}

export interface SearchResult {
  kind: 'node' | 'taxonomy' | 'action';
  id: string;
  label: string;
  displayLabel?: string;
  type?: string;
  matchType: string;
  matchedField: string;
  canonicalStatus?: string;
  canonicalNodeId?: string;
  duplicateGroupIds?: string[];
  priorityBands?: string[];
  reviewState?: string;
  disambiguationLabel?: string;
  disambiguationText?: string;
  relationshipSummary?: {
    groupEdgeCount?: number;
    nodeCount?: number;
    proposedStewardshipRelationships?: number;
  };
  resourceLinkCount?: number;
  approvalStatuses?: string[];
  admittedRelationshipCount?: number;
  ambiguity?: {
    status?: string;
    priorityBands?: string[];
    message?: string;
  };
}

export interface Perspective {
  id: string;
  name: string;
  description: string;
  nodeCount?: number;
}

export interface ApiHealth {
  status: 'ok' | 'error';
  neo4j: string;
  aecMepfs?: string;
}

export interface BackboneSummary {
  schemaVersion: string;
  source: string;
  status: string;
  reportOk: boolean;
  runId: string;
  counts: {
    predicateRegistry: number;
    sourceRightsRegistry: number;
    backboneNodes: number;
  };
  boundaries: {
    shadowOnly: boolean;
    fileBackedOnly: boolean;
    liveNeo4jWrites: boolean;
    graphRebuild: boolean;
    featureFlagCutover: boolean;
    apiExplorerCutover: boolean;
    canonicalContentAdmission: boolean;
    protectedContentIngest: boolean;
    liveMutationBoundariesClear: boolean;
    safeForReadOnlyConsumer: boolean;
  };
  noIngestBoundaryCoverage: {
    sourcesTotal: number;
    explicitNoIngestSourceCount: number;
    missingExplicitBlockCount: number;
    contentIngestSourceCount: number;
  };
  artifactPaths: {
    artifact: string;
    shadowGraph: string;
    producerReport: string;
    consumerReport: string;
  };
}

export interface BackbonePredicatePreview {
  predicate: string;
  category: string;
  direction: string;
  domainClasses: string[];
  rangeClasses: string[];
  allowedStrengthClasses: string[];
  evidenceRequiredFields: string[];
  owner: string;
}

export interface BackboneNodePreview {
  id: string;
  canonicalId: string;
  label: string;
  prefLabel: string;
  pathCode: string;
  level: number;
  parentPathCode: string;
  reviewStatus: string;
  steward: string;
  releaseVersion: string;
}

export interface BackboneShadowGraphPreview {
  available: boolean;
  counts: {
    nodes: number;
    edges: number;
    roots: number;
    maxDepth: number;
  };
  nodes: {
    id: string;
    label: string;
    pathCode: string;
    level: number;
    parentPathCode: string;
  }[];
  edges: {
    id: string;
    fromId: string;
    toId: string;
    predicate: string;
    fromPathCode: string;
    toPathCode: string;
    relationType?: string;
    relationCategory?: string;
    relationNature?: string[];
    direction?: string;
    weight?: number;
    confidenceScore?: number;
    discipline?: string[];
    lifecyclePhase?: string[];
    sourceFamilyIds?: string[];
    rationale?: string;
    provenanceNote?: string;
    generationMethod?: string;
    reviewStatus?: string;
    semanticOverlayCategory?: string;
    applicabilityBasis?: string;
    jurisdictionContext?: string;
    designBasisStatus?: string;
  }[];
}

export interface BackboneTaxonomyPreview {
  schemaVersion: string;
  source: string;
  status: string;
  reportOk: boolean;
  runId: string;
  counts: BackboneSummary['counts'];
  boundaries: BackboneSummary['boundaries'];
  noIngestBoundaryCoverage: BackboneSummary['noIngestBoundaryCoverage'];
  readiness: {
    registryMetadataAvailable: boolean;
    canonicalTaxonomyTreeAvailable: boolean;
    backboneNodesAvailable: boolean;
    shadowGraphAvailable: boolean;
    previewCompleteness: string;
    limitation: string;
  };
  predicateCategories: {
    category: string;
    count: number;
    predicates: string[];
  }[];
  predicates: BackbonePredicatePreview[];
  backboneNodes: BackboneNodePreview[];
  shadowGraph: BackboneShadowGraphPreview;
  sourceRightsClasses: {
    sourceRightsClass: string;
    count: number;
  }[];
  clearanceStates: {
    clearanceState: string;
    count: number;
  }[];
  sourceFamilies: {
    sourceId: string;
    sourceFamily: string;
    publisherAuthority: string;
    sourceRightsClass: string;
    clearanceState: string;
    declaredUseBoundary: string;
    currentnessCheckDate: string;
    stewardOwner: string;
    updateCadence: string;
  }[];
  artifactPaths: BackboneSummary['artifactPaths'];
}

export interface BackbonePlacementQaPreview {
  schemaVersion: string;
  source: string;
  status: string;
  reportOk: boolean;
  runId: string;
  fixturePath: string;
  reportPath: string;
  summary: {
    casesTotal: number;
    casesPassed: number;
    casesFailed: number;
    autoAcceptCases: number;
    proposalLevelCounts: Record<string, number>;
    reviewQueueCounts: Record<string, number>;
  };
  requiredCoverage: {
    l1_l2_human_review: boolean;
    l3_l4_ld8_auto_accept: boolean;
    legacy_label_alias: boolean;
  };
  contractValidation: {
    ok: boolean;
    warnings: string[];
  };
  boundaries: {
    shadowOnly: boolean;
    fileBackedOnly: boolean;
    liveNeo4jWrites: boolean;
    kgRebuild: boolean;
    featureFlagCutover: boolean;
    explorerDefaultAdoption: boolean;
    protectedContentIngest: boolean;
    canonicalContentAdmission: boolean;
    liveMutationBoundariesClear: boolean;
  };
  warnings: string[];
}

export interface BackboneEvidencePreview {
  schemaVersion: string;
  source: string;
  status: string;
  reportOk: boolean;
  runId: string;
  summary: {
    artifactCount: number;
    shadowGraphCounts: {
      nodes: number;
      edges: number;
      roots: number;
      maxDepth: number;
    };
    boundaryChecksPassed: number;
    boundaryChecksTotal: number;
    benchmarkOperationsPassed: number;
    benchmarkOperationsTotal: number;
    routeCount: number;
    previewRoutesPresent: number;
    previewRoutesRequired: number;
    inputHashCount: number;
    resolverRoutePolicy: string;
    benchmarkRuntimeThresholdDisposition: string;
  };
  safetyInvariants: {
    allArtifactsOk: boolean;
    benchmarkShadowFileBackedOnly: boolean;
    boundaryAuditSafetyGreen: boolean;
    noRuntimePromotion: boolean;
    resolverRoutesAbsentOrDefaultOff: boolean;
    routeInventoryPreviewRoutesComplete: boolean;
    runtimeThresholdsNotEvaluated: boolean;
    allInvariantsClear: boolean;
  };
  evidenceFiles: {
    label: string;
    path: string;
    schemaVersion: string;
    ok: boolean;
  }[];
  repoState: {
    gitHeadCommit: string;
    workingTreeDirtyAtGeneration: boolean;
    freshnessAvailable: boolean;
    sourceWorkingTreeDirtyAtGeneration: boolean | null;
    generatedEvidenceDirtyAtGeneration: boolean | null;
    sourceDirtyPathCount: number | null;
    generatedEvidenceDirtyPathCount: number | null;
  };
  reportPath: string;
}

export interface QueryResultRow {
  id: string;
  values: Record<string, string>;
}

export interface CameraState {
  x: number;
  y: number;
  ratio: number;
}

export interface SceneGraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface SceneState {
  id: string;
  name: string;
  savedAt?: string;
  perspectiveId: string;
  camera: CameraState;
  selectedNodeIds: string[];
  selectedEdgeIds: string[];
  pinnedNodeIds: string[];
  filters: {
    nodeTypes: string[];
    edgeTypes: string[];
    minConfidence: number;
    maxConfidence: number;
    searchQuery: string;
  };
  expandedNodeIds: string[];
  hiddenNodeIds: string[];
  layout: 'precomputed' | 'forceatlas2' | 'circular' | 'random' | 'clustered' | 'time';
  colorScheme: string;
  sizeBy: 'uniform' | 'confidence' | 'degree';
  graph: SceneGraphData;
}

export interface SceneSummary {
  id: string;
  name: string;
  savedAt?: string;
  perspectiveId: string;
}

export type SceneUpdateInput = Omit<SceneState, 'id' | 'savedAt'>;
