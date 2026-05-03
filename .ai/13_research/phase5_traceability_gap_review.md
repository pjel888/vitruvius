# Phase 5 Traceability Gap Review

Date: 2026-05-03T02:45:00+08:00

## Approval Records Missing kimiReviewSummary

### Count

**7 of 16 approval records** lack `kimiReviewSummary`.

### Identified Approvals

| Approval ID | Description | Has Kimi Summary? |
|-------------|-------------|-------------------|
| `canonical-approval-20260502175718-4563c5312008` | Wave 4 batch (33 edges) | **No** |
| `canonical-approval-20260502234200-f2d6d18013f2` | Wave 5 batch (35 edges) | **No** |
| `canonical-approval-20260502234631-163d49001e4b` | Wave 6 batch (33 edges) | **No** |
| `canonical-approval-20260502235016-3276f7f1760a` | Wave 7 batch (21 edges) | **No** |
| `canonical-approval-20260502235355-0f218fd0756b` | Wave 8 batch (18 edges) | **No** |
| `canonical-approval-20260502235751-9317e2c4ac33` | Wave 9 batch (15 edges) | **No** |
| `canonical-approval-20260503005832-9dd944ab03f3` | Phase 5 targeted gap (7 edges) | **No** |

### Assessment

**Acceptable.** These are bulk wave admissions under **project-owner standing steward approval**. The steward approval mechanism does not require per-approval Kimi review summaries. The absence of `kimiReviewSummary` does not indicate a defect; it indicates that Kimi review was not a gating requirement for these admissions.

The earlier approvals (Waves 1–3) and P1 packet reviews may have had Kimi summaries, but the bulk wave admissions were steward-approved directly.

**Recommendation**: No backfill. Document the approval model.

## Per-Edge transactionManifestId / rollbackPlan

### Current Schema

Admitted relationship records have these traceability fields:
- `stewardshipDecisionId` → links to the decision record
- `approvalId` → links to the approval record
- `admissionId` → unique per-edge admission ID

They do **not** have:
- `transactionManifestId` (direct)
- `rollbackPlan` (direct)

### Indirect Traceability

Traceability is available through:
1. `stewardshipDecisionId` → `stewardship-decisions.json` → decision record includes `transactionManifestId`
2. `approvalId` → `approvals.json` → approval record includes `transactionManifestId` and `rollbackPlan`
3. Transaction manifests in `006_System-Manifests/graph-canonical/transaction-manifests/`

### Assessment

**Acceptable.** Approval-level and decision-level traceability is sufficient for the current graph size (264 edges). Adding direct per-edge fields would:
- Denormalize the schema
- Increase registry size
- Require migration of 264 records

**Recommendation**: Document the indirect traceability model. If the graph scales beyond 1,000 edges, reconsider denormalizing key traceability fields onto edge records.

## Schema Improvement Queue

| Improvement | Priority | Effort | Blocked By |
|-------------|----------|--------|------------|
| Add `kimiReviewSummary` to bulk wave approvals | Low | Low | Not required for steward-approved batches |
| Add `transactionManifestId` to edge records | Low | Medium | Schema migration; not needed at 264 edges |
| Add `rollbackPlan` to edge records | Low | Medium | Schema migration; approval-level plan is sufficient |

## Finalization — 2026-05-03

**Indirect traceability model accepted as canonical.**

- Approval records link to transaction manifests via `transactionManifestId`
- Decision records link to transaction manifests via `transactionManifestId`
- Edge records link to approvals via `approvalId` and decisions via `stewardshipDecisionId`
- Rollback plans exist at approval level, not per-edge
- This model is sufficient for current scale (264 edges, 84 manifests)
- Reconsider denormalization if graph exceeds 1,000 edges or if audit latency becomes unacceptable
