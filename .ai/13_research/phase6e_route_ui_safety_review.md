# Phase 6E Route and UI Safety Review

**Generated:** 2026-05-03T01:00:00+08:00
**Commit:** e9d4e281

---

## API Route Safety

### GET /resources/review/external-candidates/schema

| Check | Status | Evidence |
|-------|--------|----------|
| Read-only | ✅ | Returns static JSON object |
| No auth gate | ✅ | Schema is public documentation |
| No side effects | ✅ | No file writes, no registry mutation |
| Returns safe defaults | ✅ | `verificationStatus: "unverified"`, `learnerVisible: false` |

### POST /resources/review/external-candidates/preview

| Check | Status | Evidence |
|-------|--------|----------|
| Dev/admin gated | ✅ | `requireLocalDevAdmin(c)` at line 4642 |
| Read-only | ✅ | Calls `buildExternalCandidatePreview()` — pure function |
| Valid URL remains unverified | ✅ | Warning: "URL syntax accepted; reachability not verified" |
| Valid DOI remains unverified | ✅ | Warning: "DOI syntax accepted; existence not verified" |
| Valid ISBN remains unverified | ✅ | Warning: "ISBN syntax accepted; existence not verified" |
| Placeholder URL rejected | ✅ | `example.com`, `localhost`, etc. error |
| Placeholder DOI rejected | ✅ | `10.placeholder/test` error |
| Placeholder ISBN rejected | ✅ | `0000000000` error |
| Placeholder edition/version rejected | ✅ | `TBD`, `latest`, `current` error |
| Standards missing context allowed as candidate | ✅ | Warning only, not error |
| Standards missing context reviewer-only | ✅ | `standard_candidate_not_learner_trusted` flag |
| learnerVisible=false | ✅ | Hardcoded `false` in preview output |
| displayPolicy=reviewer_only | ✅ | Hardcoded `'reviewer_only'` in preview output |
| No resource created | ✅ | No registry write |
| No candidate created | ✅ | No registry write |
| No nodeResourceLink created | ✅ | No registry write |
| No transaction manifest created | ✅ | No manifest generation |
| No external fetch performed | ✅ | No `fetch`, `axios`, or network calls |

---

## UI Safety

### External Candidates Tab (`ResourceReviewAdmin.tsx`)

| Check | Status | Evidence |
|-------|--------|----------|
| Tab renders | ✅ | Test: "External Candidates tab renders preview form with safe wording" |
| Preview-only wording appears | ✅ | Badge: "Preview only · No auto-verification" |
| No apply/admit button | ✅ | Only "Preview Candidate" button exists |
| Unverified badge appears | ✅ | `preview.verificationStatus` displayed as warning badge |
| Not learner-visible badge appears | ✅ | `preview.learnerVisible ? 'learner visible' : 'not learner visible'` |
| Reviewer-only badge appears | ✅ | `preview.displayPolicy` displayed as neutral badge |
| Placeholder warnings appear | ✅ | `preview.fakePlaceholderFlags` rendered in danger section |
| Missing fields appear | ✅ | `preview.missingFields` rendered |
| Source truth caveat appears | ✅ | `preview.sourceTruthCaveat` rendered in amber box |
| Admin gate disables preview | ✅ | Button `disabled={loading \|\| !adminGateOpen}` |

### Unsafe Wording Absence Test

| Unsafe word | Present? | Evidence |
|-------------|----------|----------|
| "verified" | NO | Regex check in UI test: `expect(container.textContent).not.toMatch(/verified\|official\|current\|governing\|compliant/i)` |
| "official" | NO | Same regex check |
| "current" | NO | Same regex check |
| "governing" | NO | Same regex check |
| "compliant" | NO | Same regex check |
| "valid DOI" | NO | Not present in UI labels |
| "valid ISBN" | NO | Not present in UI labels |
| "reachable URL" | NO | Not present in UI labels |

---

## Test Coverage Summary

### API Tests (24 tests)
- URL syntax + unverified marking
- URL placeholder rejection
- Non-HTTP scheme rejection
- DOI syntax + unverified marking
- DOI placeholder rejection
- ISBN syntax + unverified marking
- ISBN placeholder rejection
- Book candidate reviewer-only
- PDF candidate reviewer-only + no protected payload
- Standard candidate missing context = reviewer-only
- Standard candidate placeholder rejection
- No file writes
- No registry mutation
- Dev/admin gate
- ASCE 7 / ACI 318 not learner-trusted
- No fake metadata becomes learner-eligible
- Placeholder detection flags
- Classification correctness
- Schema route returns safe defaults
- Preview route returns normalized preview
- Preview route rejects placeholders
- Preview route respects gate

### Explorer Tests (2 new tests)
- External Candidates tab renders with safe wording
- Form has all required fields and no unsafe wording

---

## Conclusion

✅ **Route and UI safety verified.** All safety constraints enforced. All unsafe wording absent. All tests pass.
