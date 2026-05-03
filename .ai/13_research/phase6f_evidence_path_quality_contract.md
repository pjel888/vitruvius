# Phase 6F — Evidence-Path Quality Contract

Date: 2026-05-03

## Purpose

Define the end-to-end safety contract for all Resource / Evidence Layer paths that surface resources to learners or reviewers. This contract is the reference for regression tests and quality gates.

---

## Flow A: Learner Selected-Node Sidebar Path

```
selected node
→ GET /node/:id/resources
→ rankNodeResources() with learner filters
→ NodeInspector Sources tab
→ warning-safe display
```

### Invariants

1. Only `accepted` and `human_reviewed` links are returned in learner mode.
2. `rejected`, `needs_review`, `candidate` links are NEVER returned.
3. Resources with `verificationStatus === 'rejected'` or `'unverified'` are NEVER returned.
4. Rights-protected resources (`isRightsProtectedContent`) are NEVER returned.
5. Standard-like resources with incomplete context and no structured justification are NEVER returned.
6. Results are hard-capped at 8.
7. Each result includes a `warning` field when contextual caveats apply (e.g., jurisdiction note).
8. The `displayPolicy` metadata identifies the response as `mode: 'learner'`.
9. Empty state uses safe wording: "No learner-visible resources linked yet."

### Unsafe Wording (Forbidden)

- "verified", "official", "governing", "current", "approved", "compliant", "AHJ accepted"

---

## Flow B: Reviewer Source-Custody Path

```
/dev/resource-review
→ GET /resources/review/source-custody
→ buildSourceCustodyQueue()
→ grouped custody queue
→ ResourceReviewAdmin Source Custody tab
```

### Invariants

1. Returns ALL Resource Layer items: links, candidates, local files.
2. Groups into 9 custody statuses:
   - `learner_visible`
   - `reviewer_only`
   - `blocked`
   - `needs_review`
   - `candidate`
   - `indexed_only`
   - `standards_incomplete`
   - `rights_limited`
3. Every item includes `learnerEligible: boolean`.
4. Every item includes `warningFlags: string[]`.
5. Every item includes `nextReviewAction: string`.
6. Every item includes `custodyStatus` and `displayPolicy`.
7. Route is read-only; no registry mutation.
8. No transaction manifest created.
9. Safe wording enforced in UI: "Reviewer only", "Hidden from learner view", "Indexed only — not admitted", "Context incomplete", "Rights/status review required".

---

## Flow C: Standards-Context Path

```
ASCE 7 / ACI 318
→ standardContextMissingFields()
→ incomplete → not learner-trusted
→ reviewer/dev visible
→ promotion blocked
→ placeholder values rejected
```

### Invariants

1. Missing `edition/version`, `jurisdiction/geographicScope`, or `citation/scope` blocks learner eligibility.
2. `hasStructuredMissingContextJustification` requires:
   - `contextStatus` in `['justified_missing', 'not_required']`
   - Non-placeholder `reviewedBy`
   - Non-placeholder `rationale`
   - Non-placeholder `sourceOfContext`
3. Placeholder values (`tbd`, `unknown`, `latest`, `current`, `placeholder`, etc.) are rejected.
4. ASCE 7 and ACI 318 remain blocked until real context is supplied.
5. No invented edition, version, jurisdiction, adoption status, or citation text.

---

## Flow D: Local-File Path

```
indexed local files (25)
→ reviewer queue visible as `indexed_only`
→ learner hidden
→ not auto-linked
→ requires explicit reviewer admission
```

### Invariants

1. Local files indexed in `local-file-index.json` appear in `localFilesIndexedOnly` group.
2. `learnerEligible` is always `false` for indexed-only files.
3. No auto-linking; `nodeResourceLinks` must not be created automatically.
4. Admission requires hash custody, rights clearance, and reviewer decision.
5. Current admitted count remains 0 unless explicit reviewer action occurs.

---

## Flow E: Candidate Path

```
resource candidates
→ reviewer queue visible as `candidate`
→ learner hidden
→ no auto-promotion
→ warning flags and next action present
```

### Invariants

1. Candidates appear in `candidates` group.
2. `learnerEligible` is always `false`.
3. `nextReviewAction` is "Review candidate for acceptance or rejection".
4. No candidate is auto-promoted to accepted.

---

## Flow F: Rejected Path

```
rejected resources/links
→ reviewer-only or blocked group
→ learner hidden
→ never shown as trusted
```

### Invariants

1. Rejected links appear in `blocked` and `rejected` groups.
2. `learnerEligible` is always `false`.
3. `custodyStatus` is `blocked`.
4. Rejected items never appear in learner mode.

---

## Flow G: Rights/Protected Path

```
rights-protected/restricted resource
→ warning flags
→ learner hidden
→ no payload text exposed
```

### Invariants

1. `isRightsProtectedContent` blocks learner view entirely.
2. `isRightsRestrictedOrProtected` adds penalty to display score.
3. Warning text includes "Rights-protected content" or "Restricted or protected content".
4. No protected payload text is copied or displayed.

---

## No-Mutation Contract

1. `GET /node/:id/resources` must not write files.
2. `GET /resources/review/source-custody` must not write files.
3. No-write validators must not dirty the worktree.
4. Route calls must not create transaction manifests.
5. Route calls must not modify `review-decisions.json`.
6. Route calls must not alter `local-file-index.json`.
7. Route calls must not alter `node-resource-links.json`.

---

## Test Coverage Requirement

Every invariant above must have at least one test covering it.
