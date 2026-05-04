# Phase 6L — Future Resource Record Shape

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Design specification for future implementation

---

## 1. Purpose

This document defines the shape of a Resource record that future promotion apply (Phase 6N) may create. The shape is designed to support source-custody inventory, reviewer curation, and eventual link to graph nodes — without implying learner visibility or source verification.

---

## 2. Allowed Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `resourceId` | string (UUID) | Yes | Generated at creation time |
| `title` | string | Yes | From candidate or reviewer-updated |
| `resourceType` | enum | Yes | e.g., standard, code, article, book, report, manual, specification |
| `sourceType` | enum | Yes | e.g., governing-code, industry-standard, academic, reference, internal |
| `url` | string | No | If applicable to the source; syntax-only, not verified |
| `doi` | string | No | If applicable; syntax-only, not verified |
| `isbn` | string | No | If applicable; syntax-only, not verified |
| `localPath` | string | No | If a local source file exists; not verified for this phase |
| `sourceFamilyId` | string | No | If source family is known |
| `rightsStatus` | string | Yes | Required for responsible display |
| `verificationStatus` | enum | Yes | Must not be source_verified without real verification workflow |
| `custodyStatus` | enum | Yes | Default: `needs_review` or `source_candidate_promoted` |
| `displayPolicy` | enum | Yes | Default: `reviewer_only` |
| `warningFlags` | string[] | No | Warning flags for display |
| `sourceContext` | string | No | Reviewer-provided context about the source |
| `reviewer` | string | Yes | Who performed the promotion review |
| `reviewedAt` | ISO timestamp | Yes | When the promotion was reviewed |
| `rationale` | string | Yes | Why this candidate was promoted |
| `sourceOfContext` | string | Yes | Where the reviewer obtained context |
| `createdFromExternalCandidateId` | string (UUID) | Yes | Link back to the source candidate |
| `promotionDecisionId` | string (UUID) | Yes | Link to the promotion decision |
| `transactionManifestId` | string (UUID) | Yes | Link to the transaction manifest |
| `sourceTruthCaveat` | string | No | Caveat if source truth unverified |
| `standardsContextCaveat` | string | No | Caveat if standards context incomplete |
| `rightsCaveat` | string | No | Caveat if rights status uncertain |
| `protectedContentCaveat` | string | No | Caveat if content may be protected |
| `learnerVisibleDefault` | boolean | Yes | MUST be `false` on creation |
| `rollbackInfo` | object | No | Populated if rolled back |

---

## 3. Forbidden / Dangerous Fields

The following fields MUST NOT be set to `true` (or any affirmative value) by promotion apply unless a future explicit workflow provides source-verified evidence:

| Field | Reason Forbidden |
|-------|-----------------|
| `currentStandard = true` | Implies authority and currency without verification |
| `governing = true` | Implies legal/governing authority |
| `compliant = true` | Implies compliance without compliance review |
| `ahjAccepted = true` | Implies AHJ acceptance without AHJ verification |
| `urlReachable = true` | Would require URL verification (not in scope) |
| `doiVerified = true` | Would require DOI verification (not in scope) |
| `isbnVerified = true` | Would require ISBN verification (not in scope) |
| `sourceVerified = true` | Requires real verifier workflow (does not exist yet) |
| `official = true` | Implies endorsement without verification |
| `acceptedForLearner = true` | Requires accepted nodeResourceLink eligibility computation |

**Exception:** These fields may be set if a FUTURE workflow explicitly authorizes them and provides the supporting evidence chain. Promotion apply alone does not have that authorization.

---

## 4. Default Created Resource Status

| Field | Safe Default | Alternate If Reviewer-Accepted Metadata | Rationale |
|-------|-------------|-----------------------------------------|-----------|
| `custodyStatus` | `source_candidate_promoted` | `source_candidate_promoted` | Record is promoted but not fully vetted |
| `verificationStatus` | `unverified` | `reviewer_verified_metadata` | Only if review decision exists with reviewer/rationale |
| `displayPolicy` | `reviewer_only` | `reviewer_only` | Never auto-expose to learners |
| `learnerVisibleDefault` | `false` | `false` | Always start non-visible |
| `warningFlags` | `["not_externally_verified"]` | `["reviewer_curated", "not_externally_verified"]` | Transparent about limitations |

---

## 5. JSON Skeleton (Future Implementation Reference)

```jsonc
{
  "resourceId": "res_<uuid>",
  "title": "Title from candidate",
  "resourceType": "standard",
  "sourceType": "industry-standard",
  "url": "https://example.org/doc",
  "doi": null,
  "isbn": null,
  "localPath": null,
  "sourceFamilyId": null,
  "rightsStatus": "open_access",
  "verificationStatus": "unverified",
  "custodyStatus": "source_candidate_promoted",
  "displayPolicy": "reviewer_only",
  "warningFlags": ["not_externally_verified"],
  "sourceContext": "Reviewed against publisher metadata",
  "reviewer": "reviewer_handle",
  "reviewedAt": "2026-05-04T12:00:00Z",
  "rationale": "Metadata complete, no placeholders, rights clear",
  "sourceOfContext": "Publisher website, catalog entry",
  "createdFromExternalCandidateId": "ec_<uuid>",
  "promotionDecisionId": "pd_<uuid>",
  "transactionManifestId": "tm_<uuid>",
  "sourceTruthCaveat": "URL syntax-valid but not verified reachable",
  "standardsContextCaveat": null,
  "rightsCaveat": "Rights stated as open_access from publisher metadata",
  "protectedContentCaveat": null,
  "learnerVisibleDefault": false,
  "rollbackInfo": null
}
```

---

## 6. Registry Placement

The future Resource record should be added to:
- `api/resourceLayer/registry.ts` — Resource registry
- A new or existing resources JSON file (e.g., `api/resourceLayer/resources.json`) — Production record storage

The record must NOT be placed in:
- Graph registries (003_Canonical-Knowledge-Layer)
- Graph edge stores
- Any learner-visible data set until eligibility computed
