# Phase 6G External Candidate Registry Implementation Report

**Generated:** 2026-05-03T01:00:00+08:00

---

## Registry Location

- **File:** `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- **Schema version:** `vitruvius-external-metadata-candidate/v1`

## Implementation

### Module: `api/resourceLayer/externalCandidateRegistry.ts`

**Exports:**
- `EXTERNAL_CANDIDATE_REGISTRY_SCHEMA_VERSION`
- `EXTERNAL_CANDIDATE_REGISTRY_FILE`
- `ExternalMetadataCandidateRecord` — type
- `ExternalCandidateRegistry` — type
- `PersistResult` — type
- `loadExternalCandidateRegistry(repoRoot)` — read
- `hashExternalCandidatePreview(preview)` — SHA-256 of stable JSON
- `buildExternalCandidateId(input)` — deterministic ID generation
- `persistExternalCandidate(repoRoot, input)` — write with transaction manifest
- `listExternalCandidates(repoRoot, filters?)` — list with optional filters
- `getExternalCandidate(repoRoot, candidateId)` — detail

### Write Behavior

- Uses `withResourceLayerTransaction` from `transactionManifest.ts`
- Operation type: `external_candidate_persist`
- Files touched: `external-metadata-candidates.json`
- Deterministic write: temp file + rename
- Lock file: `.resource-layer-review.lock`

### Duplicate Detection

Checks in order:
1. normalizedUrl match
2. normalizedDoi match
3. normalizedIsbn match
4. title match (when no URL/DOI/ISBN)

---

## Safety Guarantees

- No graph mutation
- no resource creation
- No nodeResourceLink creation
- No review decision creation
- No external fetch
- Transaction manifest covers every write
- Rollback plan documented in manifest
