# Phase 6N — Resource-Only Apply API Report

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Implementation complete

---

## 1. Implementation Summary

### Files Created

| File | Purpose |
|------|---------|
| `api/resourceLayer/externalCandidatePromotionApply.ts` | Core gate implementation, promotion apply logic, rollback logic |
| `api/resourceLayer/promotionApplyRoutes.ts` | Express route handlers for all 4 routes |

### Routes Implemented

| Method | Path | Read-only | Gate |
|--------|------|-----------|------|
| POST | `/resources/review/external-candidates/:candidateId/promotion-apply-preview` | Yes | req body + preview hash |
| POST | `/resources/review/external-candidates/:candidateId/promotion-apply` | No | All gates A-I |
| POST | `/resources/review/external-candidates/:candidateId/promotion-rollback-preview` | Yes | resourceId required |
| POST | `/resources/review/external-candidates/:candidateId/promotion-rollback` | No | reviewer/rationale/rollbackAction required |

---

## 2. Apply Route Details

### POST .../promotion-apply

**Required request body:**
```json
{
  "applyMode": "resource_only",
  "reviewer": "string (required)",
  "rationale": "string (required)",
  "sourceOfContext": "string (required)",
  "previewHash": "string (required, from preview)",
  "acknowledgeWarnings": true,
  "promotionCaveat": "string (optional, defaults to rationale)"
}
```

**Response (success, HTTP 201):**
```json
{
  "success": true,
  "candidateId": "ec_<uuid>",
  "applyMode": "resource_only",
  "createdResourceId": "res_<uuid>",
  "createdNodeResourceLinkIds": [],
  "learnerVisible": false,
  "externalVerificationPerformed": false,
  "graphMutationApplied": false,
  "canonicalMutationApplied": false,
  "nodeLinksCreated": 0,
  "transactionManifestId": "tm_<uuid>",
  "rollbackPlan": { "resourcesToRemove": ["res_<uuid>"], "linksToRemove": [], "rollbackType": "hard_delete_or_mark_rolled_back" },
  "sourceTruthCaveat": "Source metadata curated by reviewer; not externally verified",
  "standardsContextCaveat": null,
  "rightsCaveat": null,
  "verificationCaveat": "No external verification performed; URL/DOI/ISBN not verified"
}
```

**Response (gate failure, HTTP 400):**
```json
{
  "success": false,
  "gate": "E3",
  "message": "ASCE 7 incomplete context — blocked until real context supplied",
  "severity": "stop",
  "blockingGates": ["E3"]
}
```

---

## 3. Safety Enforcement

| Safety Invariant | Enforced |
|------------------|----------|
| resource_and_links rejected | Gate F0 — returns error message |
| Learner visibility blocked | Gate G3 — learnerVisible: false enforced |
| External verification blocked | Gate C4/C5 — source_verified claims rejected |
| Graph mutation blocked | Code design — no graph registries touched |
| Canonical mutation blocked | Code design — no canonical registries touched |
| Transaction manifest written | Always — manifest created and saved |
| Rollback plan recorded | Always — included in manifest |
| Duplicate detection | Gate B7 — URL/DOI/ISBN/title+type match |

---

## 4. Route Registration

Routes are registered via `registerPromotionApplyRoutes(app)`.

Integration point: `api/index.ts` should call:
```typescript
import { registerPromotionApplyRoutes } from './resourceLayer/promotionApplyRoutes';
registerPromotionApplyRoutes(app);
```

---

## 5. Dependencies

- `externalCandidateRegistry.ts` — for loading candidate data
- `registry.ts` — for resource registry loading/saving
- `externalMetadataCandidates.ts` — for candidate registry persistence
- Standard Node.js `fs` and `path` — for file I/O
- `uuid` — for resource/transaction ID generation
- Express `Router` — for route mounting
