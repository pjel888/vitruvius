# Phase 6H External Candidate Review Workflow Design

**Date:** 2026-05-03
**Status:** Planning — NOT Implemented

## Overview

Phase 6H defines the review-decision workflow for external metadata candidates. It does NOT implement promotion. Candidates remain reviewer-only and unverified.

## Workflow Steps

### 1. Preview Correction

**Purpose:** Reviewer edits candidate metadata safely.

**Flow:**
1. Reviewer submits proposed metadata patch.
2. System validates patch against `correctionPatch` rules.
3. System returns:
   - `diff` (before/after)
   - `blockers` (violations of correction rules)
   - `warnings` (remaining concerns)
4. No file mutation.

**Gate:** `requireLocalDevAdmin`

### 2. Apply Correction

**Purpose:** Persist validated metadata correction.

**Flow:**
1. Reviewer confirms correction.
2. System re-validates patch.
3. System updates candidate record in `external-metadata-candidates.json`.
4. System writes transaction manifest.
5. System appends decision record to `external-candidate-decisions.json`.
6. Candidate status becomes `candidate` or `metadata_correction_needed` → `candidate`.

**Mutations:**
- `external-metadata-candidates.json` (candidate metadata only)
- `external-candidate-decisions.json` (decision history)
- Transaction manifest

**No mutations:**
- No resource created.
- No nodeResourceLink created.
- No graph mutation.

**Gate:** `requireLocalDevAdmin`

### 3. Review Decision Preview

**Purpose:** Reviewer chooses a disposition without applying it.

**Supported decisions:**
- `reject`
- `defer`
- `needs_more_context`
- `ready_for_promotion_review`
- `duplicate_candidate`

**Flow:**
1. Reviewer selects decision type and provides rationale.
2. System validates required fields for decision type.
3. System runs promotion readiness gates if decision is `ready_for_promotion_review`.
4. System returns preview with blockers if gates fail.
5. No file mutation.

**Gate:** `requireLocalDevAdmin`

### 4. Apply Review Decision

**Purpose:** Persist reviewer decision.

**Flow:**
1. Reviewer confirms decision.
2. System validates required fields.
3. System updates candidate `status`.
4. System appends decision record.
5. System writes transaction manifest.

**Mutations:**
- `external-metadata-candidates.json` (status field only)
- `external-candidate-decisions.json`
- Transaction manifest

**No mutations:**
- No resource created.
- No nodeResourceLink created.
- No graph mutation.

**Gate:** `requireLocalDevAdmin`

### 5. Promotion Preview (Future Phase)

**Purpose:** Preview what a candidate-to-resource promotion would look like.

**Flow:**
1. Reviewer requests promotion preview for a `ready_for_promotion_review` candidate.
2. System validates all promotion readiness gates.
3. System generates preview:
   - Proposed `Resource` object
   - Proposed `NodeResourceLink` objects (if `proposedNodeIds` present)
   - Blockers if any gate fails
4. No file mutation.

**Explicitly NOT implemented in Phase 6H.**

### 6. Promotion Apply (Future Phase)

**Purpose:** Create accepted resource and optional links.

**Flow:**
1. Requires explicit authorization beyond 6H.
2. Creates `Resource` in `resources.json`.
3. Creates `NodeResourceLink`(s) in `node-resource-links.json` if applicable.
4. Updates candidate status to `promoted` or removes from active candidates.
5. Writes transaction manifest.
6. Updates source-custody queue.

**Explicitly NOT implemented in Phase 6H.**

## Decision History

All decisions are append-only. A candidate's full history is the sequence of decisions in `external-candidate-decisions.json` filtered by `candidateId`.

## Transaction Manifests

Every mutating step (apply correction, apply review decision) writes a transaction manifest:

```
resource-layer-tx-{timestamp}-{hash}.json
```

Manifest includes:
- `operationType`: `external_candidate_correction` or `external_candidate_review_decision`
- `affectedFiles`: `[external-metadata-candidates.json, external-candidate-decisions.json]`
- `beforeHash`, `afterHash`
- `rollbackPlan`
