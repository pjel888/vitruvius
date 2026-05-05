# Phase 7 First Candidate Batch Queue

**Date:** 2026-05-06
**Status:** QUEUE_ONLY_NO_CANDIDATES_CREATED

This queue identifies where Phase 7 should start. It does not create candidates, Resources, nodeResourceLinks, source truth claims, or learner exposure.

## Batch 1 Shape

| Field | Requirement |
|---|---|
| Batch size | 3 to 8 real resources |
| Source metadata | Steward supplied; no lookup by default |
| Initial display policy | `reviewer_only` |
| Initial verification status | `unverified` unless separately reviewed |
| First promotion mode | `resource_only` |
| Link mode | `resource_and_links` only after per-node rationale |
| Rollback | Required |
| Commit | Required after validation |

## Priority Queue

| Priority | Node family | Candidate need | Constraints |
|---:|---|---|---|
| 1 | Architecture | Real general reference or official professional source metadata | No protected payload; no fake publisher/date/URL |
| 2 | Structural Engineering | Real structural reference metadata for non-P0 concepts | Avoid Concrete/Reinforced Concrete and high-risk P1 packets |
| 3 | Civil Engineering | Real civil/site/infrastructure reference metadata | No AHJ or jurisdiction claims unless supplied and reviewed |
| 4 | MEPFS | Real system reference metadata for HVAC, plumbing, electrical, fire protection, or sanitary topics | Rights and learner eligibility must be explicit |
| 5 | Standards-linked concepts | Real standard edition/version/scope metadata | ASCE 7 and ACI 318 remain blocked until real context is supplied |
| 6 | High-traffic nodes | Real learner-useful reference metadata | Links require node-specific rationale |

## Candidate Metadata Intake Checklist

Each proposed candidate needs:

- title
- source type
- resource type
- steward-supplied URL/DOI/ISBN/local reference if available
- publisher/author only when known from the steward-supplied record
- rights status
- source-of-context note
- reviewer and rationale
- target node rationale if link creation is requested

## Deferred Items

- URL reachability verification
- DOI lookup
- ISBN lookup
- book API lookup
- PDF fetching
- protected source extraction
- ASCE 7 / ACI 318 trust promotion
- local file auto-linking
- graph/canonical admission

## First Batch Recommendation

Start with resource-only previews for a small steward-supplied set across Architecture, Structural Engineering, Civil Engineering, and MEPFS. Promote links only after the resource records are accepted and node-specific rationale is strong enough to pass `resource_and_links` gates.
