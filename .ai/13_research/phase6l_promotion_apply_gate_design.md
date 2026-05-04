# Phase 6L — Promotion Apply Gate Design

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Gate specification (not implemented)

---

## Overview

Promotion apply has **9 gate groups** (A-I). All gates in the relevant groups must pass before a promotion apply operation executes. Gates are checked in order; a failure at any gate stops the operation and returns specific failure details.

---

## A. Candidate Status Gate

**Purpose:** Ensure the candidate is in a valid, reviewable state for promotion.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| A1 | candidate exists | Stop: candidate not found |
| A2 | candidate status is `ready_for_promotion_review` | Stop: candidate not ready for promotion |
| A3 | candidate is not `rejected` | Stop: candidate was rejected |
| A4 | candidate is not `deferred` | Stop: candidate is deferred |
| A5 | candidate is not `duplicate_candidate` | Stop: candidate flagged as duplicate |
| A6 | candidate is not `promotion_blocked` | Stop: candidate is promotion blocked |
| A7 | candidate has decision history showing review path | Stop: no review decision history |
| A8 | candidate safety flags all true: `noAutoVerification`, `noAutoPromotion`, `noAutoLinking`, `noLearnerExposure` | Stop: one or more safety flags are false |

**Note:** Gate A8 ensures that even if a candidate passes status checks, the no-auto safety flags prevent automated bypass of review.

---

## B. Metadata Integrity Gate

**Purpose:** Ensure the candidate metadata is complete, non-placeholder, non-fake, and does not duplicate existing resources or candidates.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| B1 | `title` present and non-empty | Stop: missing title |
| B2 | `resourceType` present and valid | Stop: missing/invalid resourceType |
| B3 | `sourceType` present and valid | Stop: missing/invalid sourceType |
| B4 | No placeholder URL/DOI/ISBN (e.g., "http://placeholder", "000-0", "TBD") | Stop: placeholder URL/DOI/ISBN detected |
| B5 | No fake publisher/author/date/edition/scope values (e.g., "N/A", "Unknown", placeholder text) | Stop: fake metadata detected |
| B6 | Normalized metadata stable (normalization does not produce contradictions) | Stop: unstable normalization |
| B7 | Duplicate detection against existing resources and candidates passes (no duplicate title+URL, title+DOI, title+ISBN match) | Stop: duplicate detected |

**Note:** Gate B5 is a heuristic check, not a verification action. It flags obvious placeholder/fake values. It does not verify publication truth.

---

## C. Source Truth / Verification Gate

**Purpose:** Enforce that promotion apply does not claim source verification it cannot support.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| C1 | Syntax-only checks are NOT used as trust signals | Stop: syntax-only trust implied |
| C2 | `verificationStatus` must be one of: `unverified` (safe default), `reviewer_verified_metadata` (only with review decision record), NOT `source_verified` unless a real verification workflow exists | Stop: unsupported verification status |
| C3 | If `verificationStatus` = `reviewer_verified_metadata`, a review decision must exist with: reviewer, rationale, sourceOfContext | Stop: reviewer_verified_metadata without supporting decision |
| C4 | Promotion apply MUST NOT set `source_verified` unless a real verification workflow exists | Stop: source_verified claim unsupported |
| C5 | No reachability / DOI / ISBN existence claim without real verifier | Stop: unsupported existence claim |

**Key philosophy:** Promotion apply is a source-custody and metadata-curation operation. External verification is a SEPARATE workflow not authorized by this phase. Syntax-valid URLs/DOIs/ISBNs remain unverified for source truth purposes.

---

## D. Rights Gate

**Purpose:** Ensure rights metadata is complete and safe for the intended display policy.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| D1 | `rightsStatus` exists and is non-empty | Stop: missing rightsStatus |
| D2 | `rightsStatus` is NOT `unknown` for resources that would be learner-visible | Stop: unknown rights for learner-visible resource |
| D3 | `protected_content` and `excerpt_limited` rights must remain hidden or warning-gated (not displayed without caveat) | Stop: protected_content/excerpt_limited without warning gate |
| D4 | `licensed` / `internal_use_only` rights must preserve display restrictions | Stop: licensed/internal without display restriction |
| D5 | Reviewer rationale and sourceOfContext required for rights assessment | Stop: missing reviewer context for rights |

---

## E. Standards Gate

**Purpose:** Enforce that standard/code/governing-document candidates are complete, non-placeholder, and not claiming authority without context.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| E1 | Standard/code/governing-document candidates require edition/version/scope/source context, OR justified-missing context | Stop: missing required standards context |
| E2 | Placeholder edition/version/scope values rejected | Stop: placeholder standards context detected |
| E3 | ASCE 7 and ACI 318 remain incomplete and blocked unless real context supplied by a reviewer | Stop: ASCE 7 or ACI 318 incomplete context |
| E4 | No `current` / `governing` / `compliance` / `AHJ` claim without source-supported context | Stop: unsupported governing/compliance claim |

**Note:** ASCE 7 and ACI 318 are known incomplete standards. They are promotion-blocked until a reviewer supplies real context. No auto-completion is permitted.

---

## F. Node-Link Gate

**Purpose:** Validate that if nodeResourceLinks are to be created, the prerequisites are met.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| F1 | If apply mode is `resource_and_links`, `proposedNodeIds` must exist | Stop: missing proposedNodeIds for link creation |
| F2 | Every proposed node must exist in the graph | Stop: proposed node does not exist |
| F3 | `proposedRelation` must be valid for Resource Layer link relation vocabulary | Stop: invalid link relation |
| F4 | Node-specific rationale must exist for each proposed link | Stop: missing node-specific rationale |
| F5 | No nodeResourceLink creation without explicit apply mode (`resource_and_links`) | Stop: links created without explicit apply mode |
| F6 | No link auto-acceptance unless link-specific acceptance gates pass | Stop: link auto-acceptance without gate passage |
| F7 | No graph edge implication from Resource Layer link | Stop: graph edge mutation attempted |

**Note:** Gate F gates are only checked if apply mode is `resource_and_links`. In `resource_only` mode, F gates are skipped. Each proposed node must have its own rationale.

---

## G. Display / Learner Gate

**Purpose:** Ensure no accidental learner exposure of unreviewed resources.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| G1 | Resource display policy defaults to `reviewer_only` on creation | Stop: learner-visible default on creation |
| G2 | nodeResourceLink review status defaults to `needs_review` unless all acceptance gates pass | Stop: link auto-accepted without gate passage |
| G3 | `learnerVisible` remains false unless a separate accepted link eligibility computation passes | Stop: learnerVisible set true without eligibility |
| G4 | NodeInspector learner sidebar must not expose unreviewed promoted resources | Stop: learner sidebar exposure of unreviewed resource |

**Safety principle:** Promotion apply creates curated Resource Layer objects, NOT learner-facing content. Learner visibility is a downstream decision.

---

## H. Transaction / Rollback Gate

**Purpose:** Enforce that every mutation is wrapped in a transaction with rollback capability.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| H1 | Transaction manifest required | Stop: no transaction manifest provided |
| H2 | `beforeHashes` / `afterHashes` required for each touched file | Stop: missing file hashes |
| H3 | Rollback plan required before execution | Stop: no rollback plan |
| H4 | Rollback must be able to remove or mark-created resource/link as `rolled_back` | Stop: rollback plan insufficient |
| H5 | No direct file write outside transaction wrapper | Stop: unwrapped file write attempted |
| H6 | Candidate history must record promotion apply intent and result | Stop: missing candidate history update |

---

## I. Audit Gate

**Purpose:** Ensure every promotion decision is fully auditable.

| Gate | Condition | Failure Action |
|------|-----------|----------------|
| I1 | `reviewer` present and non-empty | Stop: missing reviewer |
| I2 | `rationale` present and non-empty | Stop: missing rationale |
| I3 | `sourceOfContext` present and non-empty | Stop: missing sourceOfContext |
| I4 | `reviewedAt` timestamp present | Stop: missing reviewedAt timestamp |
| I5 | Promotion decision ID generated and recorded | Stop: missing promotion decision ID |
| I6 | Promotion caveat recorded (at minimum: "not external-verified", "not learner-visible") | Stop: missing promotion caveat |
| I7 | NoAuto flags preserved, OR explicitly superseded by recorded decision with rationale | Stop: noAuto flags suppressed without rationale |

---

## Gate Evaluation Order

Gates must be checked in order A through I:

1. A (Candidate Status) — cheapest, fail fast
2. B (Metadata Integrity) — medium cost
3. C (Source Truth) — enforces trust boundaries
4. D (Rights) — legal/safety check
5. E (Standards) — only if standard/code type
6. F (Node-Link) — only if `resource_and_links` mode
7. G (Display/Learner) — safety check
8. H (Transaction/Rollback) — integrity check
9. I (Audit) — final gate before commit

If any gate fails, the promotion apply operation is rejected with:
- `gate`: failed gate identifier (e.g., "A2")
- `message`: human-readable failure reason
- `severity`: "stop"

---

## Gate Applicability by Mode

| Gate | resource_only | resource_and_links |
|------|---------------|-------------------|
| A (Status) | All | All |
| B (Metadata) | All | All |
| C (Source Truth) | All | All |
| D (Rights) | All | All |
| E (Standards) | If standard/code type | If standard/code type |
| F (Node-Link) | Skipped | All |
| G (Display/Learner) | All | All |
| H (Transaction) | All | All |
| I (Audit) | All | All |

---

## Gate Checklist Output (for UI display)

The gate system should produce a checklist response with, for each gate:
- `id`: gate identifier (e.g., "B7")
- `label`: human-readable label
- `status`: "pass" | "fail" | "skipped" | "pending_check"
- `message`: optional detail on status

UI should render this as a live checklist that updates as gates pass or fail.
