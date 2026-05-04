# Phase 6L — Next Actions

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Active next-actions document

---

## Current Phase Status

- Phase 6L planning: COMPLETED (design only, no implementation)
- Promotion apply: REMAINS UNIMPLEMENTED
- Candidate-to-resource creation: REMAINS BLOCKED
- Candidate-to-nodeResourceLink creation: REMAINS BLOCKED

---

## Immediate Next Actions

### Priority 1: Phase 6M — Independent Audit of Promotion Apply Plan
- Audit all Phase 6L planning documents
- Verify gate design completeness
- Verify no implementation occurred
- Verify no production mutation occurred
- Verify resource/link creation remains blocked
- Approve or reject gate design for implementation

### Priority 2: Phase 6N — Resource-Only Promotion Implementation
Only after Phase 6M audit passes:
- Implement `promotion-apply-preview` route extension
- Implement `promotion-apply` route (resource_only mode only)
- Implement gate checks A-I (skipping F for resource_only)
- Implement transaction manifest and rollback
- Implement candidate history update
- No nodeResourceLink creation
- No learner exposure
- No external verification
- No graph mutation

### Priority 3: Phase 6O — Resource + nodeResourceLink Promotion Implementation
Only after Phase 6N is stable:
- Add node-link gate checks (F)
- Implement nodeResourceLink creation
- Implement `promotion-apply` (resource_and_links mode)
- Link integration with NodeInspector learner sidebar

---

## Validation Needed (Future Session)

Before implementing any Phase 6L design, a session with working terminal tools should:
1. Run bun validators (see .ai/05_logs/2026-05-04_phase6l_no_mutation_validation.md)
2. Run focused API tests
3. Run full test suite
4. Verify git status and branch sync
5. Verify production data integrity
