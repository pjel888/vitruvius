# Phase 6 Source-Custody Model

Date: 2026-05-03T03:45:00+08:00

## Design Goal

Define a complete custody model for local and external resources without mutating production registries yet.

## Resource Record Fields

### Core Identity

| Field | Type | Description |
|-------|------|-------------|
| `resourceId` | string | Canonical UUID |
| `title` | string | Human-readable title |
| `subtitle` | string | Optional secondary title |
| `resourceType` | `ResourceType` | book, standard, code, professional_guidance, etc. |

### Source Classification

| Field | Type | Description |
|-------|------|-------------|
| `sourceType` | enum | `web_url`, `book`, `pdf`, `local_file`, `standard`, `guide`, `article`, `code`, `dataset`, `internal_note` |
| `sourceAuthority` | `SourceAuthority` | official, professional_body, government, academic, etc. |
| `sourceFamilyId` | string | Link to source-families.json entry |

### Custody Status

| Field | Type | Values |
|-------|------|--------|
| `custodyStatus` | enum | `unreviewed`, `indexed_only`, `candidate`, `needs_review`, `source_verified`, `rights_limited`, `rejected`, `accepted` |
| `reviewStatus` | enum | `candidate`, `accepted`, `rejected`, `needs_review`, `human_reviewed` |

### Rights Status

| Field | Type | Values |
|-------|------|--------|
| `rightsStatus` | enum | `unknown`, `public`, `licensed`, `internal_use_only`, `protected_content`, `excerpt_limited` |
| `accessType` | enum | `open_access`, `public_web`, `preview_only`, `paywalled`, `local_only`, `restricted`, `unknown` |
| `sourceRights` | object | `canQuote`, `canLink`, `canStore`, `canDistribute`, `rightsNote` |

### Verification Status

| Field | Type | Values |
|-------|------|--------|
| `verificationStatus` | enum | `unverified`, `metadata_verified`, `link_verified`, `identifier_verified`, `local_file_verified`, `content_verified`, `human_reviewed`, `rejected` |
| `lastCheckedAt` | ISO date | Last verification attempt |

### Source Context (Standards)

| Field | Type | Description |
|-------|------|-------------|
| `standardContext` | `StandardReviewContext` | edition, version, publicationYear, jurisdiction, scope, citationContext |
| `standardContextJustification` | string | Why context is missing or partial |
| `standardContextReviewer` | string | Who reviewed the context |
| `standardContextReviewedAt` | ISO date | When context was reviewed |

### Local File Metadata

| Field | Type | Description |
|-------|------|-------------|
| `localPath` | string | Relative path in repo |
| `localFileHash` | string | SHA-256 of file content |
| `indexedAt` | ISO date | When scanner indexed the file |
| `fileSize` | number | Bytes |
| `mimeType` | string | MIME type |
| `extractionStatus` | enum | `not_extracted`, `extracted`, `failed` |

### Resource Quality Scores

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `authorityScore` | number | 0–1 | Source authority tier |
| `relevanceScore` | number | 0–1 | Node specificity |
| `confidenceScore` | number | 0–1 | Evidence confidence |
| `nodeSpecificity` | number | 0–1 | How directly the resource addresses the node |
| `recency` | number | 0–1 | Publication/checked recency |
| `warningFlags` | string[] | — | List of quality warnings |

### Link Quality

| Field | Type | Values |
|-------|------|--------|
| `linkType` | enum | `direct`, `contextual`, `broad`, `weak`, `rejected` |
| `relationship` | enum | `defines`, `explains`, `governs`, `supports`, `provides_procedure`, etc. |

### Display Policy

| Field | Type | Values |
|-------|------|--------|
| `displayPolicy` | enum | `show_to_user`, `show_warning`, `dev_only`, `hidden`, `blocked` |

## Schema Migration Assessment

Most fields already exist in `api/resourceLayer/types.ts`. The current schema already supports:
- `ResourceType`, `SourceAuthority`, `AccessType`, `VerificationStatus`
- `StandardReviewContext`, `StandardEditionContext`, `StandardJurisdictionContext`
- `localPath`, `localFileHash`, `sourceRights`, `admissionProvenance`

**No schema migration is required for Phase 6A.** The design above documents the intended use of existing fields.

## Custody Workflow States

```
unreviewed → indexed_only → candidate → needs_review → source_verified → accepted
                                    ↘ rejected
```

- `unreviewed`: Resource discovered but not processed
- `indexed_only`: Local file scanner recorded hash/path only
- `candidate`: Identified as potentially relevant to a node
- `needs_review`: Awaiting human reviewer decision
- `source_verified`: Metadata/URL/identifier verified
- `accepted`: Reviewer approved for sidebar display
- `rejected`: Not suitable for display
- `rights_limited`: Verified but usage restricted

## Anti-Fake Safeguards

1. **No invented URLs**: URLs must be reachable or explicitly marked unverified.
2. **No invented editions**: Standards must have real edition/version or explicit "missing context" justification.
3. **No invented ISBNs/DOIs**: Identifiers must pass normalization checks; duplicates blocked.
4. **No invented local files**: Local files must exist and hash-match at indexing time.
5. **No jurisdiction guesses**: Jurisdiction notes must be scoped and truthful (e.g., "US model standard; adoption depends on local jurisdiction").
