# Phase 6L Promotion Apply Philosophy

**Date:** 2026-05-03
**Status:** Planning — No Implementation

---

## Core Distinction

| Concept | Definition | Visibility |
|---|---|---|
| **External metadata candidate** | Proposed evidence metadata, unverified by default, reviewer-only | Never learner-visible |
| **Resource** | Curated Resource Layer object, admitted to production registry | Not learner-visible unless linked and accepted |
| **nodeResourceLink** | Node-specific evidence relationship | Learner-visible only if accepted + eligible |

Promotion apply is **not** a single vague "accept" action. It is a structured, gated, transaction-backed workflow with at least two distinct apply modes.

---

## Apply Mode 1: Resource-Only Promotion

**Purpose:** Add a source to the Resource Layer inventory without creating any node-specific links.

**When to use:**
- Source is relevant to the knowledge base but node placement is uncertain
- Reviewer wants to admit the source first and link later
- Source is a general reference (handbook, standard) that may link to multiple nodes in future

**Creates:**
- One `Resource` record in `resources.json`

**Does NOT create:**
- nodeResourceLinks
- Graph edges
- Learner-visible records

**Default status:**
- `custodyStatus`: `needs_review` or `source_candidate_promoted`
- `verificationStatus`: `unverified` or `reviewer_verified_metadata` (if review decision exists)
- `displayPolicy`: `reviewer_only`
- `learnerVisible`: `false`

---

## Apply Mode 2: Resource + NodeResourceLink Promotion

**Purpose:** Admit a source and immediately link it to specific graph nodes.

**When to use:**
- Candidate was submitted with explicit `proposedNodeIds` and `proposedRelation`
- Node relevance has been reviewed and approved
- Both resource gates and link-specific gates pass

**Creates:**
- One `Resource` record in `resources.json`
- One or more `nodeResourceLink` records in `node-resource-links.json`

**Link default status:**
- `reviewStatus`: `needs_review` (even if resource passes gates, links start as needs_review unless explicitly accepted)
- `learnerEligible`: computed by `isLearnerSidebarEligible`, never manually asserted
- `displayPolicy`: inherited from resource or `reviewer_only`

**Requires:**
- All resource-only gates
- PLUS: node existence validation
- PLUS: relation vocabulary validation
- PLUS: node-specific rationale
- PLUS: per-link review decision (future)

---

## Recommended Phase Sequence

**Phase 6M (future implementation):** Resource-only promotion first.
- Lower blast radius
- No graph node dependency
- Enables source inventory building
- Links can be created later via existing link review workflow

**Phase 6N+ (future implementation):** Resource + nodeResourceLink promotion.
- Higher blast radius
- Requires node existence validation
- Requires link-specific review decisions
- Only after resource-only promotion is proven safe

---

## Verification Philosophy

- **Syntax validation ≠ verification** — URL/DOI/ISBN syntax checks do not imply source truth
- **Reviewer metadata verification ≠ source verification** — A reviewer checking metadata fields is not the same as verifying the source content
- **Promotion apply must not set `verificationStatus: 'source_verified'`** unless a real verification workflow exists
- **Safe default:** `verificationStatus: 'unverified'` for all promoted resources until explicit verification workflow completes

---

## Learner Exposure Philosophy

- **Promotion apply does NOT make anything learner-visible**
- Learner visibility is determined by:
  1. Resource exists and is not blocked
  2. nodeResourceLink exists and is `accepted`
  3. `isLearnerSidebarEligible()` returns true for the link
  4. No rights/review flags block display
- A promoted resource with no links is invisible to learners
- A promoted resource with `needs_review` links is invisible to learners
