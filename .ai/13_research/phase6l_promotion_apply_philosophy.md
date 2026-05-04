# Phase 6L — Promotion Apply Philosophy

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Design definition

---

## 1. Core Distinctions

Promotion apply is NOT a single vague "accept" action. It is a bounded, gated, transaction-backed operation that creates a curated Resource Layer object from an external metadata candidate. The following distinctions are fundamental:

| Entity | Meaning | Creation Gate | Learner Visibility |
|--------|---------|---------------|-------------------|
| **External metadata candidate** | Proposed evidence metadata, unverified by default, reviewer-only | Created via external candidate intake | Never directly visible |
| **Resource** | Curated Resource Layer object, still NOT necessarily learner-visible | Requires promotion apply | Only if link/display gates pass and learner eligibility computed |
| **nodeResourceLink** | Node-specific evidence relationship; what appears in node sidebar | Requires node-link promotion gates | Only if accepted and learner eligibility passes |

---

## 2. Two Future Apply Modes

### Mode A: Resource-Only Promotion

Creates a Resource object only. No nodeResourceLinks. No learner exposure unless a future link operation creates an accepted link AND learner eligibility passes.

**Purpose:** Source-custody inventory. Useful when the source metadata is sound but the node relationships are not yet determined or need separate review.

**Key properties:**
- Creates exactly one Resource record
- No nodeResourceLinks created
- No impact on graph
- Resource default status: source_candidate_promoted or needs_review
- displayPolicy: reviewer_only
- learnerVisible: false
- Rollback: delete or mark rolled_back

**Recommended as Phase 6M starting point:** Yes. Resource-only is the safer, simpler first implementation.

### Mode B: Resource + nodeResourceLink Promotion

Creates a Resource object AND one or more nodeResourceLinks. Requires both resource gates AND link-specific gates to pass.

**Purpose:** Complete evidence promotion. Creates the resource and attaches it to specific graph nodes.

**Key properties:**
- Creates one Resource record
- Creates N nodeResourceLinks (one per proposed node)
- Each link requires node-specific rationale
- Links default to needs_review unless all acceptance gates pass
- No graph edges implied (links are Resource Layer metadata, not graph edges)
- learnerVisible computed per-link by isLearnerSidebarEligible

**Recommended as Phase 6N addition:** Yes. This should follow Phase 6M (resource-only) after the resource promotion path is proven.

---

## 3. What Promotion Apply Is NOT

| Misconception | Reality |
|---|---|
| "Accept and make learner-visible" | Learner visibility requires separate link acceptance + eligibility |
| "Verify the source" | No external verification in promotion apply. Verification is a separate workflow. |
| "Claim compliance" | No compliance/governing/AHJ claims without source-verified context |
| "Current standard" | No current/governing assertion without real standards workflow |
| "This replaces source custody" | Resource Layer augments source custody, does not replace it |
| "This admits graph edges" | Resource-to-node links are Resource Layer metadata, not graph edges |
| "This is the final step" | Promotion is one step in a longer evidence lifecycle (review → promote → verify → link → display) |

---

## 4. What Promotion Apply IS

| Fact | Detail |
|---|---|
| Creates a Resource record | Only when all source-custody gates pass |
| Records provenance | From external candidate ID through to created resource ID |
| Transaction-backed | Every mutation wrapped in transaction manifest with rollback |
| Reviewer-authorized | Requires explicit reviewer/rationale/sourceOfContext |
| Auditor-visible | Full audit trail including caveats and warnings |
| Rollback-capable | Transaction manifest enables state reversal |

---

## 5. Phase Ordering Recommendation

| Phase | Scope | What It Creates |
|-------|-------|-----------------|
| **6M** (next) | Independent audit of this promotion apply plan | Plan validation |
| **6N** (implementation start) | Resource-only promotion | Resource records only |
| **6O** (later) | nodeResourceLink promotion | Resource + nodeResourceLinks |

Phase 6M need not wait for full 6L approval — the audit can validate this plan while the design remains theory.

---

## 6. Design Principles

1. **No auto-promotion.** Every candidate requires explicit reviewer action to promote.
2. **No hidden learner exposure.** learnerVisible defaults to false and can only become true through separate eligibility computation.
3. **No fake verification.** Syntax-valid URL/DOI/ISBN is NOT verified source truth.
4. **No shortcut gates.** A candidate being "ready_for_promotion_review" does NOT mean it's ready for learner exposure.
5. **Transaction integrity.** Every mutation writes a manifest and supports rollback.
6. **Audit-first.** Every promotion records reviewer, rationale, caveats, and timestamp.
7. **Source-custody concern.** Resource Layer is a curated evidence inventory, not a learner-facing content library.

---

## 7. Summary

Promotion apply is a deliberate, gated, transaction-backed operation that converts a reviewer-approved external metadata candidate into a Resource Layer record (and optionally nodeResourceLinks). It does NOT make things learner-visible, does NOT verify sources, does NOT claim compliance, and does NOT mutate the graph. It is the controlled bridge between "candidate metadata" and "curated Resource Layer object."

**Recommended sequence:**
1. Phase 6M: Independent audit of this plan
2. Phase 6N: Implement resource-only promotion (Mode A)
3. Phase 6O: Implement resource + nodeResourceLink promotion (Mode B)
