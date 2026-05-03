# Phase 6L Promotion Apply Gate Design

**Date:** 2026-05-03
**Status:** Planning — No Implementation

---

## Gate A: Candidate Status Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| Candidate exists in registry | `loadExternalCandidateRegistry` must find candidate | Yes |
| Status is `ready_for_promotion_review` | No other status allowed | Yes |
| Not rejected | `rejected` blocks permanently | Yes |
| Not deferred | `deferred` blocks permanently | Yes |
| Not duplicate | `duplicate_candidate` blocks permanently | Yes |
| Not promotion_blocked | `promotion_blocked` blocks permanently | Yes |
| Decision history exists | At least one review decision showing path to ready | Warning |
| Safety flags intact | `noAutoVerification`, `noAutoPromotion`, `noAutoLinking`, `noLearnerExposure` all true | Yes |

---

## Gate B: Metadata Integrity Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| Title present and non-empty | `title?.trim()` must be truthy | Yes |
| resourceType valid | Must be in `RESOURCE_TYPES` | Yes |
| sourceType valid | If present, must be in `SOURCE_AUTHORITIES` | Yes |
| No placeholder URL | `fakePlaceholderFlags` must not contain `placeholder_url` | Yes |
| No placeholder DOI | `fakePlaceholderFlags` must not contain `placeholder_doi` | Yes |
| No placeholder ISBN | `fakePlaceholderFlags` must not contain `placeholder_isbn` | Yes |
| No placeholder edition | `fakePlaceholderFlags` must not contain `placeholder_edition` | Yes |
| No placeholder version | `fakePlaceholderFlags` must not contain `placeholder_version` | Yes |
| No placeholder publisher | `fakePlaceholderFlags` must not contain `placeholder_publisher` | Yes |
| No placeholder author | `fakePlaceholderFlags` must not contain `placeholder_author` | Yes |
| Normalized metadata stable | `previewHash` must match re-computed hash | Yes |
| Duplicate detection | Must not duplicate existing `Resource.id` or `Resource.title` + `Resource.resourceType` | Yes |

---

## Gate C: Source Truth / Verification Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| `verificationStatus` acceptable | Must be `unverified` or `reviewer_verified_metadata` | Yes |
| No unsupported verification claim | Must not claim `source_verified`, `link_verified`, `content_verified` without verifier | Yes |
| Reviewer verification recorded | If `reviewer_verified_metadata`, must have corresponding review decision with reviewer/rationale/sourceOfContext | Warning |
| No reachability claim | Must not set `urlReachable=true` without real reachability check | Yes |
| No DOI resolution claim | Must not set `doiVerified=true` without real DOI resolution | Yes |
| No ISBN lookup claim | Must not set `isbnVerified=true` without real ISBN lookup | Yes |

**Safe `verificationStatus` values for promoted resources:**
- `unverified` — default, no blockers
- `reviewer_verified_metadata` — allowed ONLY if review decision exists

**Forbidden `verificationStatus` values for promoted resources:**
- `source_verified` — requires real verification workflow
- `link_verified` — requires real reachability check
- `identifier_verified` — requires real DOI/ISBN resolution
- `content_verified` — requires real content inspection

---

## Gate D: Rights Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| `rightsStatus` exists | Must be explicitly set | Warning |
| `rightsStatus` not `unknown` for learner-eligible paths | If resource might become learner-visible, rights cannot be `unknown` | Yes |
| Protected content hidden | If `protected_content`, `displayPolicy` must be `reviewer_only` or `dev_only` | Yes |
| Licensed/internal restricted | If `licensed` or `internal_use_only`, display restrictions must persist | Warning |
| Reviewer rationale recorded | `rightsStatusAssessment.reviewerRationale` required if rights gate evaluated | Warning |

---

## Gate E: Standards Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| Standard candidates require context | `standard_candidate` or `guide_candidate` must have edition/version or justified missing | Yes |
| Placeholder context rejected | No placeholder values in edition, version, jurisdiction, scope | Yes |
| No current/governing claim | Must not claim `currentStandard=true` or `governing=true` without real context | Yes |
| No compliance/AHJ claim | Must not claim `compliant=true` or `ahjAccepted=true` without real context | Yes |
| ASCE 7 / ACI 318 blocked | Existing incomplete standards remain blocked | Yes |

---

## Gate F: Node-Link Gate (Apply Mode 2 only)

| Check | Rule | Blocker if fails |
|---|---|---|
| `proposedNodeIds` exist in graph | Every node ID must exist in graph registry | Yes |
| `proposedRelation` valid | Must be in `NODE_RESOURCE_RELATIONSHIPS` | Yes |
| Node-specific rationale exists | `candidateRationale` must explain relevance | Yes |
| No duplicate link | Must not create duplicate (nodeId + resourceId + relationship) | Yes |
| No graph edge implication | Candidate metadata must not imply graph topology changes | Yes |
| Link review status safe | Default to `needs_review`, never `accepted` without explicit link review | Yes |

---

## Gate G: Display / Learner Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| `learnerVisible` remains `false` | Promotion apply must not set `learnerVisible=true` | Yes |
| `displayPolicy` safe | Must be `reviewer_only` or `dev_only` at promotion time | Yes |
| Warnings preserved | `warningFlags` must not be silently cleared | Yes |
| NodeInspector safety | Learner sidebar must not expose promoted resources until link acceptance passes | Yes |

---

## Gate H: Transaction / Rollback Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| Transaction manifest wrapper | Must use `withResourceLayerTransaction()` | Yes |
| Before/after hashes | `beforeHash` and `afterHash` required for all touched files | Yes |
| Rollback plan | Manifest must include rollback strategy | Yes |
| Previous manifest hash | Must chain to previous manifest | Warning |
| No direct file mutation | All writes through transaction wrapper | Yes |
| Candidate history updated | Promotion apply decision appended to candidate history | Yes |

---

## Gate I: Audit Gate

| Check | Rule | Blocker if fails |
|---|---|---|
| Reviewer identity | `reviewer` field required | Yes |
| Rationale | `rationale` field required, minimum length enforced | Yes |
| sourceOfContext | `sourceOfContext` required | Yes |
| reviewedAt | Timestamp auto-generated | Yes |
| Promotion decision ID | Unique decision ID generated | Yes |
| Promotion caveat | `auditCaveat` required on decision record | Yes |
| noAuto flags preserved | Explicitly recorded, not silently removed | Yes |

---

## Gate Summary Table

| Gate | Resource-Only (Mode 1) | Resource + Links (Mode 2) |
|---|---|---|
| A. Candidate Status | ✅ Required | ✅ Required |
| B. Metadata Integrity | ✅ Required | ✅ Required |
| C. Source Truth | ✅ Required | ✅ Required |
| D. Rights | ✅ Required | ✅ Required |
| E. Standards | ✅ Required | ✅ Required |
| F. Node-Link | ❌ N/A | ✅ Required |
| G. Display / Learner | ✅ Required | ✅ Required |
| H. Transaction | ✅ Required | ✅ Required |
| I. Audit | ✅ Required | ✅ Required |
