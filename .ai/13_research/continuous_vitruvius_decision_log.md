# Continuous Vitruvius Decision Log

**Date:** 2026-05-03

## Decision: Phase 6I Implementation Scope

**Context:** Phase 6H planning defined the review-decision workflow. Phase 6I implements it.

**Decision:** Implement correction preview/apply, review decision preview/apply, decision history, promotion readiness helper, and UI. Do NOT implement promotion apply.

**Rationale:**
1. Review-decision workflow is a prerequisite for safe promotion.
2. Promotion apply creates production data and requires separate authorization.
3. The 8-gate promotion readiness checklist ensures candidates are properly evaluated before any future promotion.

**Consequences:**
- Candidates can be reviewed, corrected, rejected, deferred, or marked ready for promotion review.
- No resource or nodeResourceLink is created.
- No learner exposure occurs.

## Decision: Inline Decision History Storage

**Context:** Decision history could be stored in a separate file or inline with candidates.

**Decision:** Store decision history inline in `external-metadata-candidates.json` as a `decisions` array on each candidate record.

**Rationale:**
- Simpler file management (one registry file).
- Transaction manifests cover only one file.
- Candidate record immutability is not required; candidates are mutable staging data.

**Consequences:**
- Candidate records grow with decision history.
- Registry file size increases over time.
- No separate decision registry to manage.

## Decision: Expanded Status Type in Registry

**Context:** Phase 6G had only 3 status values. Phase 6I needs 11.

**Decision:** Expand `ExternalMetadataCandidateRecord.status` to include all review states.

**Rationale:** The candidate registry is the source of truth for candidate status.

**Consequences:**
- TypeScript types updated in both API and Explorer.
- Source-custody queue reflects all review states.
