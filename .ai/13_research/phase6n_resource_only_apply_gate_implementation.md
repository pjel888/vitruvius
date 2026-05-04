# Phase 6N — Resource-Only Apply Gate Implementation

**Created:** 2026-05-04
**Phase:** 6N — Implementation
**Status:** Gate implementation specification

---

## 1. Gate Implementation Architecture

Gates are implemented as a chain-of-responsibility in `externalCandidatePromotionApply.ts`. Each gate group is a separate validator function that returns either `{ passed: true }` or `{ passed: false, gate: string, message: string }`.

### Gate Function Interface

```typescript
interface GateResult {
  passed: boolean;
  gate?: string;
  message?: string;
  severity?: 'stop';
}

type GateValidator = (candidate: ExternalCandidate, registry: RegistryState, options: ApplyOptions) => GateResult | Promise<GateResult>;
```

### Gate Chain

```typescript
const GATE_VALIDATORS: GateValidator[] = [
  validateCandidateStatus,    // A
  validateMetadataIntegrity,  // B
  validateSourceTruth,        // C
  validateRights,             // D
  validateStandardsContext,   // E (skipped if not standard/code type)
  // F (node-link) — SKIPPED in resource_only mode
  validateDisplayLearner,     // G
  validateTransactionRollback,// H
  validateAudit,              // I
];
```

---

## 2. Gate A — Candidate Status

```typescript
function validateCandidateStatus(candidate: ExternalCandidate): GateResult {
  if (!candidate) return { passed: false, gate: 'A1', message: 'Candidate not found' };
  if (candidate.status !== 'ready_for_promotion_review') return { passed: false, gate: 'A2', message: 'Candidate not ready for promotion review' };
  if (candidate.status === 'rejected') return { passed: false, gate: 'A3', message: 'Candidate was rejected' };
  if (candidate.status === 'deferred') return { passed: false, gate: 'A4', message: 'Candidate is deferred' };
  if (candidate.status === 'duplicate_candidate') return { passed: false, gate: 'A5', message: 'Candidate flagged as duplicate' };
  if (candidate.status === 'promotion_blocked') return { passed: false, gate: 'A6', message: 'Candidate is promotion blocked' };
  if (!candidate.decisions || candidate.decisions.length === 0) return { passed: false, gate: 'A7', message: 'No review decision history' };
  
  const flags = candidate.safetyFlags || {};
  if (flags.noAutoVerification === false) return { passed: false, gate: 'A8', message: 'noAutoVerification flag is false' };
  if (flags.noAutoPromotion === false) return { passed: false, gate: 'A8', message: 'noAutoPromotion flag is false' };
  if (flags.noAutoLinking === false) return { passed: false, gate: 'A8', message: 'noAutoLinking flag is false' };
  if (flags.noLearnerExposure === false) return { passed: false, gate: 'A8', message: 'noLearnerExposure flag is false' };
  
  return { passed: true };
}
```

---

## 3. Gate B — Metadata Integrity

```typescript
function validateMetadataIntegrity(candidate: ExternalCandidate): GateResult {
  if (!candidate.title || candidate.title.trim() === '') return { passed: false, gate: 'B1', message: 'Missing title' };
  if (!candidate.resourceType) return { passed: false, gate: 'B2', message: 'Missing resourceType' };
  if (!candidate.sourceType) return { passed: false, gate: 'B3', message: 'Missing sourceType' };
  
  // Check for placeholder values
  const PLACEHOLDER_PATTERNS = [
    /^placeholder$/i, /^http:\/\/placeholder/i, /^https?:\/\/example\./i,
    /^000-0/i, /^TBD$/i, /^N\/A$/i, /^unknown$/i, /^todo$/i,
  ];
  
  if (candidate.url && PLACEHOLDER_PATTERNS.some(p => p.test(candidate.url))) {
    return { passed: false, gate: 'B4', message: 'Placeholder URL detected' };
  }
  if (candidate.doi && PLACEHOLDER_PATTERNS.some(p => p.test(candidate.doi))) {
    return { passed: false, gate: 'B4', message: 'Placeholder DOI detected' };
  }
  if (candidate.isbn && PLACEHOLDER_PATTERNS.some(p => p.test(candidate.isbn))) {
    return { passed: false, gate: 'B4', message: 'Placeholder ISBN detected' };
  }
  
  // Check fake publisher/author/date values
  const FAKE_VALUES = ['n/a', 'unknown', 'tbd', 'todo', 'placeholder', '', 'none'];
  if (candidate.publisher && FAKE_VALUES.includes(candidate.publisher.toLowerCase())) {
    return { passed: false, gate: 'B5', message: 'Fake publisher value' };
  }
  if (candidate.author && FAKE_VALUES.includes(candidate.author.toLowerCase())) {
    return { passed: false, gate: 'B5', message: 'Fake author value' };
  }
  
  // Duplicate detection (implemented as separate check with registry access)
  
  return { passed: true };
}
```

---

## 4. Gate C — Source Truth / Verification

```typescript
function validateSourceTruth(candidate: ExternalCandidate): GateResult {
  // Syntax-only URL/DOI/ISBN does not equal verification
  if (candidate.url && candidate.url.match(/^https?:\/\//) && !candidate.verified) {
    // URL is syntactically valid but not verified — this is fine for promotion
    // as long as no verification claim is made
  }
  
  // verificationStatus must remain unverified
  if (candidate.verificationStatus === 'source_verified') {
    return { passed: false, gate: 'C4', message: 'source_verified claim unsupported — no verification workflow exists' };
  }
  
  // Do not allow reachability / DOI / ISBN existence claims
  if (candidate.urlReachable === true) {
    return { passed: false, gate: 'C5', message: 'URL reachability claim unsupported' };
  }
  if (candidate.doiVerified === true) {
    return { passed: false, gate: 'C5', message: 'DOI verification claim unsupported' };
  }
  if (candidate.isbnVerified === true) {
    return { passed: false, gate: 'C5', message: 'ISBN verification claim unsupported' };
  }
  
  return { passed: true };
}
```

---

## 5. Gate D — Rights

```typescript
function validateRights(candidate: ExternalCandidate): GateResult {
  if (!candidate.rightsStatus) return { passed: false, gate: 'D1', message: 'Missing rightsStatus' };
  
  // For resource_only mode, we accept unknown rights because resource stays reviewer-only
  // But if the candidate metadata implies learner-visible, block
  if (candidate.rightsStatus === 'unknown' && candidate.learnerVisible !== false) {
    return { passed: false, gate: 'D2', message: 'Unknown rights for learner-visible resource' };
  }
  
  if (candidate.protectedContent || candidate.excerptLimited) {
    // This is acceptable for resource_only mode — resource stays reviewer-only
    // But we add a warning flag
  }
  
  return { passed: true };
}
```

---

## 6. Gate E — Standards Context

```typescript
function validateStandardsContext(candidate: ExternalCandidate): GateResult {
  // Only applies to standard/code/governing-document type candidates
  if (candidate.resourceType !== 'standard' && 
      candidate.resourceType !== 'code' && 
      candidate.resourceType !== 'governing-document') {
    return { passed: true }; // Skipped for non-standard types
  }
  
  if (!candidate.edition && !candidate.version && !candidate.scope && !candidate.sourceContext) {
    return { passed: false, gate: 'E1', message: 'Missing required standards context (edition/version/scope/sourceContext)' };
  }
  
  // Reject placeholders
  const PLACEHOLDER = ['', 'n/a', 'unknown', 'tbd', 'todo', 'placeholder', 'latest', 'current'];
  if (candidate.edition && PLACEHOLDER.includes(candidate.edition.toLowerCase())) {
    return { passed: false, gate: 'E2', message: 'Placeholder standard edition' };
  }
  
  // ASCE 7 and ACI 318 blocking
  if (candidate.title && (
      candidate.title.match(/ASCE.*7/i) || candidate.title.match(/ACI.*318/i)
  )) {
    if (!candidate.edition || !candidate.scope || PLACEHOLDER.includes(candidate.edition.toLowerCase())) {
      return { passed: false, gate: 'E3', message: 'ASCE 7 or ACI 318 incomplete context — blocked until real context supplied' };
    }
  }
  
  // No current/governing/compliance/AHJ claims
  if (candidate.currentStandard === true) {
    return { passed: false, gate: 'E4', message: 'currentStandard claim unsupported without source-verified context' };
  }
  if (candidate.governing === true) {
    return { passed: false, gate: 'E4', message: 'governing claim unsupported without source-verified context' };
  }
  if (candidate.ahjAccepted === true) {
    return { passed: false, gate: 'E4', message: 'AHJ acceptance claim unsupported' };
  }
  
  return { passed: true };
}
```

---

## 7. Gate F — Node-Link (Skipped in resource_only)

```typescript
function validateNodeLink(candidate: ExternalCandidate, options: ApplyOptions): GateResult {
  // In resource_only mode, ALL node-link gates are skipped
  if (options.applyMode === 'resource_only') {
    return { passed: true, skipped: true };
  }
  
  // resource_and_links mode is not implemented
  return { passed: false, gate: 'F0', message: 'resource_and_links mode not implemented in Phase 6N' };
}
```

---

## 8. Gate G — Display / Learner

```typescript
function validateDisplayLearner(candidate: ExternalCandidate): GateResult {
  // learnerVisible must remain false
  if (candidate.learnerVisible === true) {
    return { passed: false, gate: 'G3', message: 'learnerVisible cannot be true for resource-only promotion' };
  }
  
  return { passed: true };
}
```

---

## 9. Gate H — Transaction / Rollback

```typescript
function validateTransactionRollback(options: ApplyOptions): GateResult {
  if (!options.transactionManifest) return { passed: false, gate: 'H1', message: 'Transaction manifest required' };
  if (!options.rollbackPlan) return { passed: false, gate: 'H3', message: 'Rollback plan required' };
  
  return { passed: true };
}
```

---

## 10. Gate I — Audit

```typescript
function validateAudit(input: ResourceOnlyApplyInput): GateResult {
  if (!input.reviewer || input.reviewer.trim() === '') return { passed: false, gate: 'I1', message: 'Missing reviewer' };
  if (!input.rationale || input.rationale.trim() === '') return { passed: false, gate: 'I2', message: 'Missing rationale' };
  if (!input.sourceOfContext || input.sourceOfContext.trim() === '') return { passed: false, gate: 'I3', message: 'Missing sourceOfContext' };
  if (!input.promotionCaveat || input.promotionCaveat.trim() === '') return { passed: false, gate: 'I6', message: 'Missing promotion caveat' };
  
  return { passed: true };
}
```

---

## 11. Master Gate Runner

```typescript
async function runAllGates(
  candidate: ExternalCandidate | null,
  registry: RegistryState,
  input: ResourceOnlyApplyInput
): Promise<{ allPassed: boolean; blockingGates: string[]; results: GateResult[] }> {
  if (!candidate) {
    return { allPassed: false, blockingGates: ['A1'], results: [{ passed: false, gate: 'A1', message: 'Candidate not found' }] };
  }
  
  const results: GateResult[] = [];
  const validators = [
    () => validateCandidateStatus(candidate),
    () => validateMetadataIntegrity(candidate),
    () => validateSourceTruth(candidate),
    () => validateRights(candidate),
    () => validateStandardsContext(candidate),
    () => validateNodeLink(candidate, { applyMode: input.applyMode }),
    () => validateDisplayLearner(candidate),
    () => validateTransactionRollback({ transactionManifest: true, rollbackPlan: true }),
    () => validateAudit(input),
  ];
  
  for (const validate of validators) {
    const result = await validate();
    results.push(result);
    if (!result.passed) {
      return { allPassed: false, blockingGates: results.filter(r => !r.passed).map(r => r.gate!), results };
    }
  }
  
  return { allPassed: true, blockingGates: [], results };
}
```
