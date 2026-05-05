# Phase 6C Source-Custody Reviewer Queue Contract

Date: 2026-05-03

## Purpose

Provide a unified, read-only reviewer/dev view of all Resource Layer items grouped by their source-custody disposition. The queue makes it easy to see why a resource is learner-visible, reviewer-only, blocked, rights-limited, standards-context-incomplete, local-file-indexed-only, or candidate-only.

## Endpoint

```
GET /resources/review/source-custody
```

- Read-only; no registry mutation.
- No file writes.
- No transaction manifest.
- Returns grouped source-custody queue.
- Does not expose protected payload text.
- Does not imply source verification or standards compliance.

## Response Schema

```ts
interface SourceCustodyItem {
  itemType: 'resource_link' | 'candidate' | 'local_file';
  id: string;
  title: string;
  resourceId?: string;
  nodeId?: string;
  resourceType?: string;
  sourceAuthority?: string;
  reviewStatus: string;
  verificationStatus?: string;
  custodyStatus: 'learner_visible' | 'reviewer_only' | 'blocked' | 'needs_review' | 'candidate' | 'indexed_only' | 'standards_incomplete' | 'rights_limited';
  displayPolicy: 'show_to_user' | 'show_warning' | 'dev_only' | 'hidden' | 'blocked';
  learnerEligible: boolean;
  reviewerOnlyReason?: string;
  hiddenReason?: string;
  warningFlags: string[];
  rightsStatus?: string;
  standardsContextStatus?: string;
  missingStandardContextFields?: string[];
  promotionBlocked?: boolean;
  nextReviewAction?: string;
  // Existing review-workflow item fields are preserved
}

interface SourceCustodyQueue {
  schemaVersion: string;
  generatedAt: string;
  groups: {
    learnerVisible: SourceCustodyItem[];
    reviewerOnly: SourceCustodyItem[];
    needsReview: SourceCustodyItem[];
    candidates: SourceCustodyItem[];
    localFilesIndexedOnly: SourceCustodyItem[];
    standardsContextIncomplete: SourceCustodyItem[];
    rightsLimited: SourceCustodyItem[];
    rejected: SourceCustodyItem[];
    blocked: SourceCustodyItem[];
  };
  metrics: {
    total: number;
    learnerVisible: number;
    reviewerOnly: number;
    needsReview: number;
    candidates: number;
    localFilesIndexedOnly: number;
    standardsContextIncomplete: number;
    rightsLimited: number;
    rejected: number;
    blocked: number;
  };
}
```

## Classification Rules

### Resource Link Classification

1. **learner_visible** — `isLearnerSidebarEligible(link, resource)` returns `true`
2. **blocked** — `reviewStatus === 'rejected'`
3. **rights_limited** — `isRightsProtectedContent(resource)` returns `true` AND not already blocked
4. **standards_incomplete** — standard-like resource with missing context AND no structured justification
5. **needs_review** — `reviewStatus === 'needs_review'` AND none of the above
6. **reviewer_only** — `reviewStatus === 'candidate'` or other non-accepted status

### Candidate Classification

Always **candidate** / `dev_only`.

### Local File Classification

1. **learner_visible** — admitted AND linked resource is learner-eligible
2. **indexed_only** — not admitted
3. **reviewer_only** — admitted but linked resource is not learner-eligible

## Safe Wording

- "Source custody review"
- "Reviewer-only"
- "Hidden from learner view"
- "Indexed only — not admitted"
- "Context incomplete"
- "Rights/status review required"
- "Not a compliance claim"
- "Not source-verified"
- "Candidate — not accepted"

## Unsafe Wording (Avoid)

- "verified", "official", "governing", "current", "approved", "compliant", "AHJ accepted"
