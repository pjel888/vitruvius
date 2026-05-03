# Phase 5 COORDINATES_WITH NEEDS_REVIEW Follow-Up

Date: 2026-05-03T02:45:00+08:00

## Sampled Edges Marked NEEDS_REVIEW

From `phase5_coordinates_with_sampling_audit.md`:

### Edge 1: Accessible Audits → Accessibility And Universal Design

| Field | Value |
|-------|-------|
| ID | `VTN-DOM-0002802--coordinates_with--VTN-DOM-0002542` |
| Source | VTN-DOM-0002802 (Accessible Audits) |
| Target | VTN-DOM-0002542 (Accessibility And Universal Design) |
| Type | COORDINATES_WITH |
| Rationale | "Accessible built environment audits coordinate with accessible routes for compliance, wayfinding, and usability; non-numerical and non-code-specific." |
| Approval | Wave 6 (`canonical-approval-20260502234631-163d49001e4b`) |

**Sampling audit concern**: "Rationale/target mismatch: says 'accessible routes' but target is 'Accessibility And Universal Design'"

**Follow-up assessment**:
- The rationale mentions "accessible routes" which is not the target node label.
- However, the source is "Accessible Audits" and the target is "Accessibility And Universal Design" — both are accessibility-related concepts.
- The rationale is slightly mismatched but the domain link is plausible.
- **Classification**: PASS_WITH_MINOR_CAVEAT — rationale should mention the actual target concept.
- **Action**: Queue for future metadata repair (rationale rewording).
- **No rollback needed**.

### Edge 2: Heritage Inventory → Steel

| Field | Value |
|-------|-------|
| ID | `VTN-DOM-0004351--coordinates_with--VTN-DOM-0000069` |
| Source | VTN-DOM-0004351 (Heritage Inventory) |
| Target | VTN-DOM-0000069 (Steel) |
| Type | COORDINATES_WITH |
| Rationale | "Historic preservation coordinates with steel materials for repair, replacement, and compatibility; non-numerical and non-code-specific." |
| Approval | Wave 8 (`canonical-approval-20260502235355-0f218fd0756b`) |

**Sampling audit concern**: "Weak/generic; heritage-steel coordination is forced"

**Follow-up assessment**:
- The source is a heritage inventory process; the target is a material.
- The rationale claims coordination for "repair, replacement, and compatibility" — this is plausible in historic preservation work where steel may need repair or replacement.
- However, the edge is generic and the coordination is indirect (heritage inventory → steel is not a direct design interface).
- **Classification**: PASS_WITH_MINOR_CAVEAT — edge is acceptable but low-value.
- **Action**: No rollback. If future graph pruning occurs, this edge could be deprioritized.
- **No rollback needed**.

## Summary

| Edge | Original Classification | Follow-Up Classification | Action |
|------|------------------------|--------------------------|--------|
| Accessible Audits → Accessibility And Universal Design | NEEDS_REVIEW | PASS_WITH_MINOR_CAVEAT | Queue rationale reword |
| Heritage Inventory → Steel | NEEDS_REVIEW | PASS_WITH_MINOR_CAVEAT | Accept; low priority |

## Threshold Assessment

- Weak/generic edges: 2 of 264 (0.76%)
- Threshold: >5% triggers bulk review
- **Result: Well below threshold. No bulk remediation required.**
