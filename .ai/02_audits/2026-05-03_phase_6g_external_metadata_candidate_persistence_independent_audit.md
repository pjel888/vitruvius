# Phase 6G Independent Audit Report — External Metadata Candidate Persistence

**Audit Date:** 2026-05-03T17:15:24+08:00  
**Auditor:** Independent AI Agent (non-implementing)  
**Commit Under Audit:** `3408b80e` — Phase 6G implementation  
**Branch:** `main` (synced with `origin/main`)  
**Confidence Level:** HIGH  
**Overall Verdict:** ✅ **PROCEED** with minor test-hygiene recommendation

---

## 1. Audit Scope & Objectives

### Scope
- `api/resourceLayer/externalCandidateRegistry.ts` — persistence layer
- `api/resourceLayer/externalMetadataCandidates.ts` — preview/validation layer
- `api/resourceLayer/sourceCustodyQueue.ts` — source-custody integration
- `api/index.ts` — HTTP route handlers for external candidate lifecycle
- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx` — admin UI
- `006_System-Manifests/resource-layer/external-metadata-candidates.json` — production registry
- Test suite: `api/resourceLayerExternalCandidates.test.ts`
- Cross-cutting safety: no graph mutation, no learner exposure, no auto-promotion

### Objectives
1. Verify external metadata candidates can be persisted safely without mutating the canonical graph, Resource Layer production registries, or node-resource links.
2. Verify all mutation routes are gated behind `requireLocalDevAdmin`.
3. Verify no learner-facing endpoint can access external candidates.
4. Verify the UI uses safe, non-truth-claiming wording.
5. Verify transaction manifest coverage and audit trail completeness.
6. Verify duplicate detection, placeholder rejection, and schema integrity.
7. Verify source-custody queue integration does not expose candidates to learners.

---

## 2. Authority & Precedence

This audit follows the root `AGENTS.md` authority order:
1. Root `AGENTS.md` operating contract
2. `.ai/00_system/EXECUTION_LOOP.md`
3. `.ai/00_system/principles.md`
4. `.ai/01_roadmap/master-roadmap.md`
5. `.ai/01_roadmap/current-phase.md`
6. `.ai/01_roadmap/milestone-tracker.md`
7. Codebase itself

No conflicts were detected between authority documents for Phase 6G scope.

---

## 3. Research Pack Summary

### Research Files Consulted
| File | Status | Relevance |
|------|--------|-----------|
| `.ai/13_research/phase6g_external_candidate_persistence_api_report.md` | ✅ Exists | API route analysis |
| `.ai/13_research/phase6g_external_candidate_persistence_contract.md` | ✅ Exists | Contract definition |
| `.ai/13_research/phase6g_external_candidate_registry_implementation_report.md` | ✅ Exists | Registry implementation |
| `.ai/13_research/phase6g_external_candidate_tests_report.md` | ✅ Exists | Test coverage |
| `.ai/13_research/phase6g_external_candidate_ui_report.md` | ✅ Exists | UI safety analysis |
| `.ai/13_research/phase6g_next_actions.md` | ✅ Exists | Next-step guidance |
| `.ai/13_research/phase6g_preflight_audit_reconciliation.md` | ✅ Exists | Preflight reconciliation |
| `.ai/13_research/phase6g_source_custody_external_candidates_report.md` | ✅ Exists | Source-custody integration |

### Missing Research Files (Non-Blocking)
Some Phase 6A/6B/6C contract files are absent from the repo, but these are outside 6G scope and do not impact this audit.

---

## 4. Code Inspection Findings

### 4.1 Persistence Layer (`externalCandidateRegistry.ts`)
- **`persistExternalCandidate(repoRoot, input)`** reruns `buildExternalCandidatePreview` + `validateExternalMetadataCandidate` server-side.
- Rejects placeholder metadata via `fakePlaceholderFlags.length > 0` check.
- Enforces `learnerVisible === false` and `displayPolicy === 'reviewer_only' | 'dev_only'`.
- Detects duplicates by URL/DOI/ISBN/title via `detectDuplicate()`.
- Writes through `withResourceLayerTransaction()` with `operationType: 'external_candidate_persist'`.
- Every record carries safety flags:
  - `status: 'candidate'`
  - `noAutoVerification: true`
  - `noAutoPromotion: true`
  - `noAutoLinking: true`
  - `noLearnerExposure: true`
- Deterministic ID generation: `buildExternalCandidateId()` uses timestamp + random suffix.
- Integrity hash: `hashExternalCandidatePreview()` uses SHA-256 of stable-stringified preview.

### 4.2 Validation Layer (`externalMetadataCandidates.ts`)
- `validateExternalMetadataCandidate()` checks required fields, URL/DOI/ISBN syntax, and rejects placeholders.
- `buildExternalCandidatePreview()` normalizes input and generates `warningFlags`, `missingFields`, `fakePlaceholderFlags`.
- `sourceTruthCaveat` is auto-generated: unverified status is explicitly stated.
- No field on the record type claims verification, acceptance, or governance status.

### 4.3 Source-Custody Integration (`sourceCustodyQueue.ts`)
- `external_candidate` added to `itemType` union.
- `enrichExternalCandidateItem()` returns `SourceCustodyItem` with:
  - `custodyStatus: 'blocked'` (if placeholder) or `'candidate'`
  - `displayPolicy: 'blocked'` or `'dev_only'`
  - `learnerEligible: false`
  - `promotionBlocked: true`
  - Explicit `reviewerOnlyReason` / `hiddenReason` text
- External candidates appear only in the `externalCandidates` group of the source-custody queue.

### 4.4 HTTP Routes (`api/index.ts`)
| Route | Method | Gate | Behavior |
|-------|--------|------|----------|
| `/resources/review/external-candidates/preview` | POST | `requireLocalDevAdmin` | Preview only, no write |
| `/resources/review/external-candidates` | POST | `requireLocalDevAdmin` | Persist candidate |
| `/resources/review/external-candidates` | GET | `requireLocalDevAdmin` | List candidates |
| `/resources/review/external-candidates/:id` | GET | `requireLocalDevAdmin` | Get candidate detail |
| `/resources/review/source-custody` | GET | `requireLocalDevAdmin` | Queue includes externalCandidates group |

**Critical:** No `/node/:id/resources` or learner-facing route includes external candidates.

### 4.5 Admin UI (`ResourceReviewAdmin.tsx`)
- Save button text: **"Save as reviewer-only candidate"**
- Badge: **"Preview only · No auto-verification"**
- Helper text: **"Does not create resources, links, or accepted candidates."**
- `canSave` guard requires `preview.fakePlaceholderFlags.length === 0 && adminGateOpen`.
- No "apply", "admit", "accept", "verified", "official", "current", "governing", "compliant" wording found.

### 4.6 Registry Isolation
- `external-metadata-candidates.json` is **NOT** included in `resourceLayerFilePaths()` or `readResourceLayerData()`.
- `resourceLayerMetrics()` does not count external candidates.
- `rankNodeResources()` only operates on `Resource[]` + `NodeResourceLink[]` from the main registry.
- External candidates cannot leak into learner node resources through the ranking pipeline.

---

## 5. Safety Boundary Verification

### 5.1 CROSS_DOMAIN_EQUIVALENT Gate
- **Status:** ✅ CONFIRMED ZERO
- `validateGraphRelationships.ts --no-write`: `CROSS_DOMAIN_EQUIVALENT = 0`
- This is a critical safety boundary. If nonzero, it would be a blocker.

### 5.2 No Graph Mutation
- External candidate persistence writes **only** to:
  - `006_System-Manifests/resource-layer/external-metadata-candidates.json`
  - `006_System-Manifests/resource-layer/transaction-manifests/*.json`
- No canonical graph files, node-resource links, or resource records are touched.

### 5.3 No Learner Exposure
- `getNodeResources()` filters by `reviewStatus === 'accepted' | 'human_reviewed'` in learner mode.
- External candidates are not `Resource` objects and have no `NodeResourceLink` entries.
- `rankNodeResources()` cannot discover external candidates.
- `sourceCustodyQueue` is gated behind reviewer admin.

### 5.4 No Auto-Promotion
- Safety flags `noAutoVerification`, `noAutoPromotion`, `noAutoLinking` are hardcoded `true` on every record.
- No cron, batch, or background process promotes external candidates.
- No "apply" or "accept" action exists in the external candidate UI.

---

## 6. Metrics & Quantitative Evidence

### Graph Metrics (from `validateGraphRelationships.ts --no-write`)
| Metric | Value |
|--------|-------|
| Effective nodes | 13,934 |
| Base nodes | 13,670 |
| Admitted nodes | 264 |
| CROSS_DOMAIN_EQUIVALENT | 0 |

### Resource Layer Metrics (from `validateResourceLayer.ts --no-write`)
| Metric | Value |
|--------|-------|
| Resources | 7 |
| Node-resource links | 9 |
| Resource candidates | 4 |
| Local files indexed | 25 |
| Local files admitted | 0 |
| Errors | 0 |
| Blockers | 0 |

### Canonical Stewardship (from `validateCanonicalGraphStewardship.ts --no-write`)
| Metric | Value |
|--------|-------|
| Aliases | 0 |
| Redirects | 0 |
| Tombstones | 0 |
| P0 unresolved groups | 2 (`reinforced concrete`, `concrete`) — untouched by design |

### External Candidate Registry
| Metric | Value |
|--------|-------|
| Schema version | `vitruvius-external-metadata-candidate/v1` |
| Candidates (pre-test) | 0 |
| Candidates (post-test) | 1 test artifact (see Section 10) |
| Transaction manifests | Multiple (from test runs) |

---

## 7. Test Execution Results

### `api/resourceLayerExternalCandidates.test.ts`
**Result:** ✅ **45 pass / 0 fail**

Coverage areas verified:
- URL/DOI/ISBN preview validation (syntax, placeholders, schemes)
- Book, PDF, standard candidate classification and safety
- Preview route no-write guarantee
- Preview route no-resource/link/candidate/manifest creation
- Preview route gate requirement
- Resource Layer count stability after preview calls
- ASCE 7 / ACI 318 remain not learner-trusted
- Fake metadata rejection
- Placeholder detection for URL, DOI, ISBN, edition
- Classification correctness
- Schema endpoint
- Persistence route gate requirement
- Persistence re-runs preview validation
- Placeholder rejection on persist
- Candidate-only creation (no resources, no links)
- `learnerVisible=false`, `displayPolicy=reviewer_only`, `verificationStatus=unverified`
- `reviewRequired=true`
- `noAutoVerification/noAutoPromotion/noAutoLinking/noLearnerExposure`
- Standard candidate with missing context remains reviewer-only
- Duplicate detection by URL
- Transaction manifest written
- List/detail route gating
- Source-custody queue gating
- **Persisted candidate does not appear in learner node resources**
- **No graph/canonical registry mutation on persist**

### `api/resourceEvidencePath.test.ts`
**Result:** ✅ **21 pass / 0 fail**

Coverage areas verified:
- 9-group source-custody queue structure
- No-mutation safety

### `api/resourceLayer.test.ts`
**Result:** ✅ **38 pass / 0 fail**

Coverage areas verified:
- Normalization, deduplication, ranking, registry
- Learner mode filtering
- Reviewer mode warnings
- Standards context blocking
- Candidate review workflow
- Local file review
- Placeholder rejection
- Rights-restricted content handling
- Source-custody metrics

### `api/resourceLayerStandardsContext.test.ts`
**Result:** ✅ **17 pass / 0 fail**

Coverage areas verified:
- Standards-context validation rules
- ASCE 7 / ACI 318 production state
- Visibility and gating
- No-write validation safety

---

## 8. No-Write Validator Results

All no-write validators executed successfully with zero errors and zero file mutations (excluding test artifacts; see Section 10):

| Validator | Status | Errors | Blockers | File Mutations |
|-----------|--------|--------|----------|----------------|
| `validateResourceLayer.ts --no-write` | ✅ PASS | 0 | 0 | 0 |
| `validateGraphRelationships.ts --no-write` | ✅ PASS | 0 | 0 | 0 |
| `validateCanonicalGraphStewardship.ts --no-write` | ✅ PASS | 0 | 0 | 0 |

---

## 9. Transaction Manifest & Audit Trail

### Manifest Coverage
- `persistExternalCandidate()` uses `withResourceLayerTransaction()` with:
  - `operationType: 'external_candidate_persist'`
  - `filesTouched: [registryPath(repoRoot)]` — only the external candidate registry
- Before/after SHA-256 hashes are recorded.
- `previousManifestHash` chain is maintained.
- Lock file (` .resource-layer-review.lock`) prevents concurrent writes.
- Manifests are written to `006_System-Manifests/resource-layer/transaction-manifests/`.

### Manifest Exclusions
- The transaction manifest system does **not** explicitly include `external-metadata-candidates.json` in `resourceLayerFilePaths()`. This is architecturally correct because the external candidate registry is a separate subsystem, but it means `resourceLayerFilePaths()` does not enumerate it. The `persistExternalCandidate()` function passes the path explicitly to `withResourceLayerTransaction()`, so manifests are still generated correctly.

---

## 10. Pre-Existing Issues & Test Artifacts

### Test Artifact in Tracked File (Minor Hygiene Issue)
**Finding:** The test suite (`api/resourceLayerExternalCandidates.test.ts`) uses `beforeEach(() => resetExternalCandidateRegistry())` but has **no `afterAll` cleanup**. Consequently, the last test that persists a candidate leaves it in the tracked production file `006_System-Manifests/resource-layer/external-metadata-candidates.json`.

**Current artifact:**
```json
{
  "candidateId": "ext-cand-no-graph-mutate-mopo1z6g-5mox",
  "title": "No Graph Mutate",
  ...
}
```

**Risk:** LOW. The file is designed to hold candidates. The artifact is harmless and will be overwritten by the next test run. However, it dirties the git worktree.

**Recommendation:** Add `afterAll(() => resetExternalCandidateRegistry())` to the test file to restore clean state.

### P1 Stale Snapshots
- **Status:** Pre-existing, non-blocking
- 20 P1 packets have stale source snapshots.
- No Phase 6G code touches P1 packet logic.

### P0 Concrete Groups
- **Status:** Pre-existing, untouched by design
- 2 unresolved groups (`reinforced concrete`, `concrete`).
- Phase 6G does not interact with canonical duplicate resolution.

### Unsafe Duplicate Candidates
- **Status:** Pre-existing
- 293 canonical duplicate review candidates remain unprocessed.
- Phase 6G does not interact with canonical duplicate resolution.

---

## 11. Risk Assessment

| Risk | Level | Evidence | Mitigation |
|------|-------|----------|------------|
| Learner exposure of unverified external candidates | **CRITICAL** (if present) | ✅ **ABSENT** — `rankNodeResources()` cannot access external candidates; no learner route includes them | N/A — risk not realized |
| Graph mutation by external candidate persistence | **CRITICAL** (if present) | ✅ **ABSENT** — writes only to external registry + manifest; test "no graph/canonical registry mutation" passes | N/A — risk not realized |
| Auto-promotion of external candidates | **HIGH** (if present) | ✅ **ABSENT** — `noAutoPromotion: true` hardcoded; no apply/accept action exists | N/A — risk not realized |
| Admin gate bypass | **HIGH** (if present) | ✅ **ABSENT** — all mutation routes use `requireLocalDevAdmin` | N/A — risk not realized |
| Placeholder metadata admitted | **MEDIUM** (if present) | ✅ **ABSENT** — `fakePlaceholderFlags` rejected at preview and persist layers; 6 test cases verify | N/A — risk not realized |
| Duplicate candidate explosion | **MEDIUM** (if present) | ✅ **ABSENT** — `detectDuplicate()` catches URL/DOI/ISBN/title duplicates | N/A — risk not realized |
| Test artifact pollution | **LOW** | Present — tracked file dirtied by tests | Add `afterAll` cleanup |
| Missing research files (6A/6B/6C) | **LOW** | Documentation gap only | Create missing contract files |

---

## 12. Compliance Against Phase 6G Contract

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Preview-then-save workflow | ✅ | UI shows preview badge; API has separate `/preview` and `/` POST routes |
| Reviewer-only safety boundary | ✅ | `displayPolicy: 'reviewer_only'` enforced in code and UI |
| No learner visibility | ✅ | `learnerVisible: false` enforced; `noLearnerExposure: true` flagged |
| No auto-verification | ✅ | `noAutoVerification: true` flagged |
| No auto-promotion | ✅ | `noAutoPromotion: true` flagged; no apply/accept UI |
| No auto-linking | ✅ | `noAutoLinking: true` flagged |
| Placeholder rejection | ✅ | `fakePlaceholderFlags` block persist; tested |
| Duplicate detection | ✅ | `detectDuplicate()` by URL/DOI/ISBN/title; tested |
| Transaction manifest | ✅ | `withResourceLayerTransaction()` generates manifest |
| Source-custody integration | ✅ | `enrichExternalCandidateItem()` adds to queue as blocked/candidate |
| Admin gating | ✅ | `requireLocalDevAdmin` on all mutation routes |
| Safe UI wording | ✅ | No truth-claiming language; explicit caveat text |

---

## 13. Verdict & Recommendation

### Overall Verdict: ✅ PROCEED

Phase 6G External Metadata Candidate Persistence meets its safety contract. The implementation correctly:
1. Isolates external candidates from the canonical graph and Resource Layer production registries.
2. Prevents learner exposure through architectural separation (external candidates are not `Resource` objects and have no `NodeResourceLink` entries).
3. Enforces reviewer-only access at API, persistence, and UI layers.
4. Blocks auto-verification, auto-promotion, and auto-linking via hardcoded safety flags.
5. Rejects placeholder metadata at both preview and persist stages.
6. Detects duplicates to prevent registry pollution.
7. Writes transaction manifests for every persist operation.
8. Uses safe, non-truth-claiming language in the UI.

### Recommendations (Non-Blocking)
1. **Test hygiene:** Add `afterAll(() => resetExternalCandidateRegistry())` to `api/resourceLayerExternalCandidates.test.ts` to prevent tracked-file pollution.
2. **Documentation:** Create missing Phase 6A/6B/6C contract files for completeness.
3. **Future enhancement:** Consider adding `externalCandidates` count to `resourceLayerMetrics()` for dashboard visibility (read-only, no mutation).

### Gates for Phase 6H
- [ ] 6G audit report accepted (this document)
- [ ] Test hygiene recommendation implemented or deferred with ticket
- [ ] Master roadmap updated to reflect 6G completion

---

## 14. Audit Trail & Reproducibility

### Commands Executed
```powershell
# Graph metrics validation
bun run api/validateGraphRelationships.ts -- --no-write

# Resource layer validation
bun run api/validateResourceLayer.ts -- --no-write

# Canonical stewardship validation
bun run api/validateCanonicalGraphStewardship.ts -- --no-write

# External candidate tests
cd api; bun test resourceLayerExternalCandidates.test.ts

# Source-custody / evidence path tests
cd api; bun test resourceEvidencePath.test.ts

# Resource layer comprehensive tests
cd api; bun test resourceLayer.test.ts

# Standards context tests
cd api; bun test resourceLayerStandardsContext.test.ts

# Git state verification
git status --short
git diff --name-only
git diff 006_System-Manifests/resource-layer/external-metadata-candidates.json
```

### Files Read
- `api/resourceLayer/externalCandidateRegistry.ts`
- `api/resourceLayer/externalMetadataCandidates.ts`
- `api/resourceLayer/sourceCustodyQueue.ts`
- `api/resourceLayer/registry.ts`
- `api/resourceLayer/ranking.ts`
- `api/resourceLayer/transactionManifest.ts`
- `api/index.ts` (external candidate routes, node resources routes)
- `explorer/src/api/graphApi.ts`
- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- `api/resourceLayerExternalCandidates.test.ts`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`

### Environment
- OS: Windows PowerShell
- Runtime: Bun v1.3.12
- Repo: `C:\Users\phili\Desktop\vitruvius`
- Commit: `3408b80e`

---

*End of Report*
