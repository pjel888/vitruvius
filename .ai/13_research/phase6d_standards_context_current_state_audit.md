# Phase 6D Standards-Context Current State Audit

Date: 2026-05-03T05:00:00+08:00

## Standard/Code/Governing-Document Resources

### ASCE 7 — Minimum Design Loads

| Field | Value |
|-------|-------|
| resourceId | `res-asce-7-official-landing` |
| title | ASCE 7 Minimum Design Loads |
| resourceType | `standard` |
| sourceAuthority | `professional_body` |
| sourceFamilyIds | `['asce']` |
| verificationStatus | `link_verified` |
| edition | *missing* |
| version | *missing* |
| publicationYear | *missing* |
| jurisdiction | "United States" |
| geographicScope | *missing* |
| reviewContext | *missing* |

#### Links

| linkId | nodeId | relationship | reviewStatus | classification |
|--------|--------|--------------|--------------|----------------|
| `nrl-wind-load-asce-7-needs-review` | VTN-DOM-0012777 | `is_supplementary_reference_for` | `needs_review` | needs_review_missing_context |
| `nrl-seismic-load-asce-7-needs-review` | VTN-DOM-0012777 | `is_supplementary_reference_for` | `needs_review` | needs_review_missing_context |

- Learner sidebar eligibility: ❌ Hidden (needs_review)
- Promotion status: ❌ Blocked (missing edition/version, citation/scope)
- Warning/blocker status: Warning (needs_review links show missing context warnings)

### ACI 318 — Building Code Portal

| Field | Value |
|-------|-------|
| resourceId | `res-aci-318-building-code-portal` |
| title | ACI 318 Building Code Portal |
| resourceType | `standard` |
| sourceAuthority | `professional_body` |
| sourceFamilyIds | `['aci']` |
| verificationStatus | `link_verified` |
| edition | *missing* |
| version | *missing* |
| publicationYear | *missing* |
| jurisdiction | "United States" |
| geographicScope | *missing* |
| reviewContext | *missing* |

#### Links

| linkId | nodeId | relationship | reviewStatus | classification |
|--------|--------|--------------|--------------|----------------|
| `nrl-structural-column-aci-rejected` | VTN-DOM-0012781 | `provides_design_guidance` | `rejected` | rejected |

- Learner sidebar eligibility: ❌ Hidden (rejected)
- Promotion status: ❌ Blocked (rejected + missing context)
- Warning/blocker status: Warning on resource (missing edition/version), not blocker because link is rejected

## Non-Standard Resources (for comparison)

| resourceId | title | resourceType | status | learner-visible |
|------------|-------|--------------|--------|-----------------|
| `res-us-access-board-accessible-routes-ch4` | ADA Accessibility Standards Ch 4 | `government_guidance` | accepted | ✅ Yes |
| `res-wbdg-wind-safety-building-envelope` | Wind Safety of the Building Envelope | `professional_guidance` | accepted | ✅ Yes (contextual guidance) |
| `res-wbdg-seismic-design-principles` | Seismic Design Principles | `professional_guidance` | accepted | ✅ Yes (contextual guidance) |
| `res-ice-structural-load-paths` | Structural Load Paths | `professional_guidance` | accepted | ✅ Yes |
| `res-fhwa-earth-retaining-structures` | Earth Retaining Structures | `government_guidance` | needs_review | ❌ Hidden |

## Standards-Context Validation Coverage

| Rule | Implementation | Test Coverage |
|------|----------------|---------------|
| Placeholder rejection | `isPlaceholderStandardContextValue` in validation.ts | ✅ Partial (latest, current, tbd, unknown, n/a) |
| ASCE promotion blocker | `validateLink` + `sourceFamilyIncludes('asce')` | ✅ Yes |
| ACI promotion blocker | `validateLink` + `sourceFamilyIncludes('aci')` | ✅ Yes |
| FHWA promotion blocker | `validateLink` + `sourceFamilyIncludes('fhwa')` | ✅ Yes |
| Accepted missing context blocker | `validateLink` + `standardContextMissingFields` | ✅ Yes |
| Justified missing context gate | `hasStructuredMissingContextJustification` in validation.ts | ⚠️ Needs explicit test |
| Placeholder in justification fields | `hasUsableValue` checks in validation.ts | ⚠️ Needs explicit test |
| Review workflow justification gate | `hasStructuredContextJustification` in reviewWorkflow.ts | ⚠️ Weaker than validation.ts — **GAP IDENTIFIED** |
| Learner sidebar eligibility | `isLearnerSidebarEligible` in validation.ts | ⚠️ Needs explicit test |
| UI "Do not guess" warning | `StandardsContextCard` in ResourceReviewAdmin.tsx | ✅ Yes |

## Gap Identified

`hasStructuredContextJustification` in `reviewWorkflow.ts` does not reject placeholder values in `reviewedBy`, `rationale`, or `sourceOfContext`, while `hasStructuredMissingContextJustification` in `validation.ts` does (via `hasUsableValue`). This creates a discrepancy where the preview/apply workflow might permit a promotion that full validation would block.

## Recommended Actions

1. Harden `hasStructuredContextJustification` in `reviewWorkflow.ts` to reject placeholder justification fields.
2. Add explicit tests for:
   - needs_review standard missing context = warning only
   - rejected standard missing context = no blocker
   - justified missing context with placeholder = blocked
   - complete standards context requiring reviewer/rationale/sourceOfContext
   - `isLearnerSidebarEligible` behavior
   - ASCE 7 / ACI 318 remain non-learner-trusted
