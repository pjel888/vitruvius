# Phase 6L — Promotion Apply Stop Conditions

**Created:** 2026-05-04
**Phase:** 6L — Planning Only
**Status:** Stop condition specification for future implementation

---

## 1. Purpose

This document lists all conditions that MUST STOP a future promotion apply operation. These are non-negotiable safety checks. If ANY condition is met, the operation is rejected with a specific gate failure message.

---

## 2. Stop Conditions

| # | Condition | Gate | Severity |
|---|-----------|------|----------|
| 1 | Candidate not in `ready_for_promotion_review` status | A2 | STOP |
| 2 | Candidate is `rejected` | A3 | STOP |
| 3 | Candidate is `deferred` | A4 | STOP |
| 4 | Candidate is `duplicate_candidate` | A5 | STOP |
| 5 | Candidate is `promotion_blocked` | A6 | STOP |
| 6 | Candidate has no review decision history | A7 | STOP |
| 7 | Safety flag `noAutoPromotion` is false | A8 | STOP |
| 8 | Safety flag `noAutoLinking` is false (and links would be created) | A8 | STOP |
| 9 | Safety flag `noLearnerExposure` is false | A8 | STOP |
| 10 | Title is missing or empty | B1 | STOP |
| 11 | resourceType is missing or invalid | B2 | STOP |
| 12 | sourceType is missing or invalid | B3 | STOP |
| 13 | Unresolved placeholder URL/DOI/ISBN detected | B4 | STOP |
| 14 | Fake source context (publisher/author/date/edition/scope placeholder detected) | B5 | STOP |
| 15 | Normalized metadata unstable | B6 | STOP |
| 16 | Duplicate detected against existing Resource or candidate | B7 | STOP |
| 17 | Unsupported verification claim (e.g., `source_verified` without verifier) | C4 | STOP |
| 18 | URL/DOI/ISBN existence claim without real verifier | C5 | STOP |
| 19 | Incomplete standards context for standard/code type candidate | E1 | STOP |
| 20 | ASCE 7 promoted with incomplete/invented context | E3 | STOP |
| 21 | ACI 318 promoted with incomplete/invented context | E3 | STOP |
| 22 | `current` / `governing` / `compliance` / `AHJ` claim without source context | E4 | STOP |
| 23 | Proposed node ID does not exist in graph (link mode) | F2 | STOP |
| 24 | Proposed relation is invalid for Resource Layer vocabulary (link mode) | F3 | STOP |
| 25 | Node-specific rationale missing (link mode) | F4 | STOP |
| 26 | `resource_and_links` mode used without proposed node IDs | F1 | STOP |
| 27 | Unknown rights status where learner exposure would result | D2 | STOP |
| 28 | `protected_content` or `excerpt_limited` without warning gate | D3 | STOP |
| 29 | `licensed` / `internal_use_only` without display restriction | D4 | STOP |
| 30 | Missing reviewer | I1 | STOP |
| 31 | Missing rationale | I2 | STOP |
| 32 | Missing sourceOfContext | I3 | STOP |
| 33 | `learnerVisibleDefault` manually set to `true` | G3 | STOP |
| 34 | External verification claim without verifier | C4 | STOP |
| 35 | Any graph or canonical mutation attempted | F7 | STOP |
| 36 | Any resource or link duplicate collision | B7 | STOP |
| 37 | Transaction manifest missing or incomplete | H1 | STOP |
| 38 | Rollback plan missing or incomplete | H3 | STOP |
| 39 | `previewHash` does not match most recent preview | — | STOP |
| 40 | `acknowledgeWarnings` not explicitly set to `true` | — | STOP |
| 41 | `promotionCaveat` missing or empty | I6 | STOP |
| 42 | ASCE/ACI fake context attempted (invented edition/version/scope) | E3 | STOP |
| 43 | NoAuto flags suppressed without explicit rationale in decision | I7 | STOP |
| 44 | Resource created with `rollbackInfo` already populated | — | STOP (invalid initial state) |
| 45 | Link created with `status = accepted` without explicit approval | F6 | STOP |

---

## 3. Stop Condition Categories

### Candidate State (1-9)
Candidate must be in correct state with valid safety flags.

### Metadata Integrity (10-16)
Metadata must be complete, non-placeholder, non-fake, and non-duplicate.

### Verification Safety (17-18)
No unsupported verification claims.

### Standards (19-22)
Standards context must be complete and non-invented.

### Node Linking (23-26)
Node-specific prerequisites must be met.

### Rights (27-29)
Rights status must be appropriate for intended display.

### Audit (30-32)
All audit fields required.

### Learner Safety (33)
No learner visibility shortcut.

### Technical Integrity (34-45)
Transaction, rollback, hash matching, warning acknowledgment, and caveat requirements.

---

## 4. Behavior on Stop

When a stop condition is triggered:

1. The promotion apply operation is REJECTED
2. Response includes:
   - `success: false`
   - `gate`: the gate identifier (e.g., "B4")
   - `condition`: the stop condition number (e.g., 13)
   - `message`: human-readable explanation
   - `severity`: "stop"
3. No files are modified
4. No transaction is initiated
5. No candidate state changes
6. An optional warning may be logged for the UI to display
