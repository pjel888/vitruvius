# Phase 6 Resource Layer API/UI Gap Review

Date: 2026-05-03T03:45:00+08:00

## Current Resource Review UI

`explorer/src/components/resource-review/ResourceReviewAdmin.tsx` supports tabs:
- Needs Review
- Candidates
- Local Files
- Rejected
- Standards Missing Context
- Accepted

Actions:
- Link review decisions (accept/reject/needs_review/downgrade/reopen)
- Candidate review decisions (accept_as_resource, link_to_node, reject_candidate, etc.)
- Local file review decisions (admit_as_resource, link_to_node, reject_local_file, etc.)
- Standards context decisions (keep_needs_review, update_context_partial, promote_if_context_complete, etc.)

## API Routes

| Route | Status | Notes |
|-------|--------|-------|
| `GET /resources/review/queue` | ✅ Implemented | Returns full queue |
| `GET /resources/review/candidates` | ✅ Implemented | |
| `GET /resources/review/local-files` | ✅ Implemented | |
| `GET /resources/review/standards` | ✅ Implemented | |
| `GET /resources/review/report` | ✅ Implemented | Metrics |
| `POST /resources/review/link/:linkId/decision` | ✅ Implemented | |
| `POST /resources/review/candidate/:candidateId/decision` | ✅ Implemented | |
| `POST /resources/review/local-file/:fileId/decision` | ✅ Implemented | |
| `GET /node/:id/resources` | ✅ Implemented | Returns ranked resources |
| `GET /resources/metrics` | ✅ Implemented | |

## Identified Gaps

### 1. Node Sidebar Ranked Resources

**Gap:** The `NodeInspector` Sources tab shows resources but does not apply the full ranking policy (3–8 limit, accepted-only hard gate, standards-context warnings).

**Impact:** Learners may see too many or unverified resources.

**Priority:** High (Loop 6B)

### 2. Local File Admission

**Gap:** 25 local files indexed, 0 admitted. The local-files tab exists but no files have been reviewed.

**Impact:** Local source custody is theoretical.

**Priority:** Medium (Loop 6C)

### 3. Source Custody Status Richness

**Gap:** The UI shows `reviewStatus` and `verificationStatus` but does not surface `custodyStatus`, `rightsStatus`, or `sourceRights` in detail.

**Impact:** Reviewers cannot see full custody metadata at a glance.

**Priority:** Medium (Loop 6C)

### 4. Book/PDF Metadata Modeling

**Gap:** Resource types include `book`, `pdf`, `local_book`, `local_pdf`, but the UI does not show ISBN, DOI, publisher, or page count prominently.

**Impact:** Book/PDF resources look like generic web links.

**Priority:** Low (Loop 6E)

### 5. External URL Verification

**Gap:** No automated URL reachability check. `lastCheckedAt` exists but is not actively updated.

**Impact:** Dead links may persist.

**Priority:** Low (Loop 6E)

### 6. DOI/ISBN Validation

**Gap**: Normalization functions exist (`normalizeDoi`, `normalizeIsbn`) but no automated validation against Crossref/DataCite/Open Library.

**Impact**: Identifier quality is manual.

**Priority**: Low (Loop 6E)

### 7. Rights-Status Model Completeness

**Gap**: `sourceRights` object exists in schema but is not fully utilized in UI or validation.

**Impact**: Rights limitations are not visible to users.

**Priority**: Medium (Loop 6C)

### 8. Evidence-Span Review

**Gap**: No evidence-span (text excerpt) review workflow. The system stores node-resource links but not specific evidence spans within resources.

**Impact**: Cannot point to specific passages supporting graph edges.

**Priority**: Medium (future phase)

### 9. Stale URL/Source Recrawl

**Gap**: No scheduled or triggered recrawl of URLs or local files.

**Impact**: Metadata becomes stale.

**Priority**: Low (future phase)

### 10. Reviewer Queue Source-Custody Triage View

**Gap**: The reviewer queue groups by status but lacks a unified "source custody triage" view that shows rights, verification, and custody status together.

**Impact**: Reviewers must switch tabs to see full picture.

**Priority**: Medium (Loop 6C)

### 11. Node Sidebar Dev Mode

**Gap**: No toggle in NodeInspector to show needs_review/candidate resources for debugging.

**Impact**: Developers must use `/dev/resource-review` separately.

**Priority**: Low

### 12. Admin/Dev Gates

**Gap**: The `/dev/resource-review` route is gated but the NodeInspector always shows the same view.

**Impact**: No learner/reviewer view differentiation in sidebar.

**Priority**: Medium (Loop 6B)

## Summary Table

| Gap | Loop | Priority | Effort |
|-----|------|----------|--------|
| Node sidebar ranked resources | 6B | High | Medium |
| Local file admission | 6C | Medium | Medium |
| Source custody status richness | 6C | Medium | Low |
| Rights-status completeness | 6C | Medium | Low |
| Reviewer triage view | 6C | Medium | Medium |
| Standards context hardening | 6D | High | Low |
| Book/PDF metadata | 6E | Low | Medium |
| External URL verification | 6E | Low | High |
| DOI/ISBN validation | 6E | Low | Medium |
| Evidence-span review | Future | Medium | High |
| Stale recrawl | Future | Low | High |
| Node sidebar dev mode | 6B | Low | Low |
