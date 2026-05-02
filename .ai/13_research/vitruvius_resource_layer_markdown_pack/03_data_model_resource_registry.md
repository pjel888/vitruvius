# 03 — Data Model: Resource Registry and NodeResourceLink

## Design goals

The data model must support reusable resources, online URLs, local files, books, PDFs, standards/codes/guidance, academic papers, internal documents, verification status, source authority scoring, page/chapter references, candidate/accepted/rejected workflows, and future Document graph nodes.

## Resource model

Adapt to the existing repository’s language and storage format.

```ts
export type ResourceType =
  | "book"
  | "textbook"
  | "handbook"
  | "standard"
  | "code"
  | "professional_guidance"
  | "government_guidance"
  | "academic_paper"
  | "technical_report"
  | "webpage"
  | "pdf"
  | "local_pdf"
  | "local_book"
  | "manual"
  | "manufacturer_manual"
  | "dataset"
  | "video"
  | "internal_document"
  | "classification_system"
  | "ontology_documentation";

export type SourceAuthority =
  | "official"
  | "professional_body"
  | "government"
  | "academic"
  | "recognized_publisher"
  | "industry_body"
  | "manufacturer"
  | "internal"
  | "general_web"
  | "unknown";

export type AccessType =
  | "open_access"
  | "public_web"
  | "preview_only"
  | "paywalled"
  | "local_only"
  | "restricted"
  | "unknown";

export type VerificationStatus =
  | "unverified"
  | "metadata_verified"
  | "link_verified"
  | "identifier_verified"
  | "local_file_verified"
  | "content_verified"
  | "human_reviewed"
  | "rejected";

export type Resource = {
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
  localFileType?: "pdf" | "epub" | "html" | "docx" | "txt" | "md";
  localFileSizeBytes?: number;

  disciplineTags: string[];
  taxonomyTags: string[];
  keywords?: string[];

  jurisdiction?: string;
  geographicScope?: "global" | "international" | "us" | "uk" | "eu" | "singapore" | "project_specific" | "unknown";

  accessType: AccessType;
  licenseNotes?: string;
  copyrightNotes?: string;

  abstractOrSummary?: string;
  tableOfContentsExtracted?: boolean;

  verificationStatus: VerificationStatus;
  lastCheckedAt?: string;
  createdAt: string;
  updatedAt: string;
};
```

## NodeResourceLink model

```ts
export type NodeResourceRelationship =
  | "defines"
  | "explains"
  | "governs"
  | "supports"
  | "provides_procedure"
  | "provides_evidence"
  | "provides_example"
  | "provides_classification"
  | "provides_design_guidance"
  | "provides_construction_guidance"
  | "provides_analysis_method"
  | "provides_maintenance_guidance"
  | "provides_operation_guidance"
  | "provides_historical_context"
  | "is_primary_reference_for"
  | "is_supplementary_reference_for"
  | "is_local_reference_for";

export type ReviewStatus =
  | "candidate"
  | "accepted"
  | "rejected"
  | "needs_review"
  | "human_reviewed";

export type NodeResourceLink = {
  id: string;
  nodeId: string;
  resourceId: string;
  relationship: NodeResourceRelationship;
  relevanceScore: number;   // 0..1
  authorityScore: number;   // 0..1
  confidenceScore: number;  // 0..1
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
  verifiedBy?: "codex" | "kimi" | "human" | "script";
  reviewStatus: ReviewStatus;
  reviewNotes?: string;
  createdAt: string;
  updatedAt: string;
};
```

## SourceFamily model

```ts
export type SourceFamily = {
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
};
```

## ResourceCheck model

```ts
export type ResourceCheck = {
  id: string;
  resourceId: string;
  checkType:
    | "url_health"
    | "canonical_url"
    | "doi_resolution"
    | "isbn_normalization"
    | "metadata_crosscheck"
    | "local_file_exists"
    | "local_file_hash"
    | "content_extractability"
    | "copyright_risk"
    | "jurisdiction_context";
  status: "pass" | "fail" | "warning" | "skipped";
  checkedAt: string;
  details?: string;
};
```

## Candidate model

Candidates should not be shown as accepted sidebar references.

```ts
export type ResourceCandidate = {
  id: string;
  nodeId: string;
  adapter: string;
  query: string;
  rawTitle?: string;
  rawUrl?: string;
  rawIdentifier?: string;
  rawMetadata?: unknown;
  preliminaryScore: number;
  dedupeKey?: string;
  reviewStatus: "candidate" | "accepted" | "rejected" | "needs_review";
  rejectionReason?: string;
  createdAt: string;
};
```

## ResourceChunk model for local/extractable documents

```ts
export type ResourceChunk = {
  id: string;
  resourceId: string;
  localPath?: string;
  pageStart?: number;
  pageEnd?: number;
  sectionTitle?: string;
  headingPath?: string[];
  textPreview: string; // keep short; avoid large copyrighted excerpts
  tokenCount?: number;
  embeddingId?: string;
  keywords?: string[];
  createdAt: string;
};
```

## Minimum viable implementation

```ts
Resource = {
  id,
  title,
  resourceType,
  sourceAuthority,
  url?,
  canonicalUrl?,
  doi?,
  isbn13?,
  localPath?,
  localFileHash?,
  jurisdiction?,
  accessType,
  verificationStatus,
  lastCheckedAt?,
  createdAt,
  updatedAt
}

NodeResourceLink = {
  id,
  nodeId,
  resourceId,
  relationship,
  relevanceScore,
  authorityScore,
  confidenceScore,
  rationale,
  pageRefs?,
  reviewStatus,
  createdAt,
  updatedAt
}
```

## Identifier normalization

Normalize DOI to lowercase and remove leading `https://doi.org/`. Normalize ISBN by stripping hyphens/spaces and validating check digit where feasible. Canonicalize URLs by removing tracking params and normalizing host/trailing slash. For local files, compute hash from file bytes. Store Internet Archive identifiers separately from URLs.

## Safety rule for Rule nodes

A `Rule` node should not be shown as trusted unless it has at least one accepted `NodeResourceLink` with:

- relationship = `governs`, `is_primary_reference_for`, or equivalent,
- authorityScore >= 0.75,
- reviewStatus = `accepted` or `human_reviewed`,
- jurisdiction/context populated if code/regulatory-like.
