# Phase 6L Promotion Apply Stop Conditions

**Date:** 2026-05-03
**Status:** Planning — For Future Implementation

---

## Hard Stop Conditions

These conditions MUST prevent promotion apply from proceeding:

### Candidate Status

| # | Condition | Stop Message |
|---|---|---|
| 1 | Candidate not `ready_for_promotion_review` | "Candidate status is {status}. Must be ready_for_promotion_review." |
| 2 | Candidate is `rejected` | "Candidate is rejected. Promotion permanently blocked." |
| 3 | Candidate is `deferred` | "Candidate is deferred. Promotion permanently blocked." |
| 4 | Candidate is `duplicate_candidate` | "Candidate is duplicate. Promotion permanently blocked." |
| 5 | Candidate is `promotion_blocked` | "Candidate is promotion_blocked. Resolve blockers first." |
| 6 | Candidate does not exist | "Candidate not found." |

### Metadata Integrity

| # | Condition | Stop Message |
|---|---|---|
| 7 | `fakePlaceholderFlags` non-empty | "Placeholder metadata detected: {flags}. Resolve before promotion." |
| 8 | Title missing or empty | "Title is required." |
| 9 | resourceType invalid | "Invalid resourceType: {type}." |
| 10 | Duplicate resource ID exists | "Resource ID {id} already exists." |
| 11 | Duplicate (title + resourceType) exists | "Duplicate resource detected: {title} ({type})." |
| 12 | `previewHash` mismatch | "Candidate changed since preview. Refresh preview first." |

### Source Truth / Verification

| # | Condition | Stop Message |
|---|---|---|
| 13 | `verificationStatus` is `source_verified` without verifier | "Unsupported verification claim. Remove source_verified or supply verifier." |
| 14 | `verificationStatus` is `link_verified` without reachability check | "Unsupported verification claim. Remove link_verified or supply reachability proof." |
| 15 | `verificationStatus` is `identifier_verified` without resolution proof | "Unsupported verification claim. Remove identifier_verified or supply resolution proof." |
| 16 | `verificationStatus` is `content_verified` without content inspection | "Unsupported verification claim. Remove content_verified or supply inspection proof." |

### Rights

| # | Condition | Stop Message |
|---|---|---|
| 17 | `rightsStatus` is `unknown` and learner-eligible path exists | "Rights status is unknown. Explicit rights assessment required before promotion." |
| 18 | Protected content with learner-visible display policy | "Protected content cannot have learner-visible display policy." |

### Standards

| # | Condition | Stop Message |
|---|---|---|
| 19 | Standard candidate missing edition/version | "Standard candidate requires edition or version context." |
| 20 | Standard candidate missing jurisdiction/scope | "Standard candidate requires jurisdiction or scope context." |
| 21 | ASCE 7 / ACI 318 incomplete context | "ASCE 7 / ACI 318 context incomplete. Real standards context required." |
| 22 | Claim of `currentStandard=true` without proof | "currentStandard claim requires verified context." |
| 23 | Claim of `governing=true` without proof | "governing claim requires jurisdiction verification." |
| 24 | Claim of `compliant=true` without proof | "compliant claim requires compliance review." |
| 25 | Claim of `ahjAccepted=true` without proof | "ahjAccepted claim requires AHJ documentation." |

### Node-Link (Mode 2)

| # | Condition | Stop Message |
|---|---|---|
| 26 | `proposedNodeIds` present but node does not exist | "Node {nodeId} does not exist in graph." |
| 27 | `proposedRelation` invalid | "Invalid relationship: {relation}." |
| 28 | Missing node-specific rationale | "Node-specific rationale required for each link." |
| 29 | Duplicate link (nodeId + resourceId + relationship) exists | "Link already exists for node {nodeId} with relationship {relation}." |

### Transaction / Rollback

| # | Condition | Stop Message |
|---|---|---|
| 30 | Transaction manifest wrapper unavailable | "Transaction system unavailable. Promotion blocked." |
| 31 | Rollback plan missing | "Rollback plan required." |
| 32 | Before hash computation fails | "Cannot compute file hashes. Promotion blocked." |

### Audit

| # | Condition | Stop Message |
|---|---|---|
| 33 | Reviewer missing | "Reviewer identity required." |
| 34 | Rationale missing or too short | "Rationale required (minimum 20 characters)." |
| 35 | sourceOfContext missing | "sourceOfContext required." |

### Safety

| # | Condition | Stop Message |
|---|---|---|
| 36 | `learnerVisible` manually set `true` | "learnerVisible cannot be true at promotion time." |
| 37 | Any graph/canonical mutation attempted | "Graph/canonical mutation detected. Promotion blocked." |
| 38 | External verification claim without verifier | "External verification claim without verifier. Remove claim or supply verifier." |

---

## Soft Stop / Warning Conditions

These conditions should produce strong warnings but may not block if explicitly acknowledged:

| # | Condition | Warning |
|---|---|---|
| 39 | `rightsStatus` not explicitly set | "Rights status not set. Defaulting to unknown." |
| 40 | `transactionManifestId` missing from candidate history | "Candidate predates transaction manifest tracking." |
| 41 | Minimal metadata classification | "Candidate has minimal metadata. Consider enriching before promotion." |
| 42 | No stable identifier (URL/DOI/ISBN) | "No stable identifier. Resource may be hard to verify." |
