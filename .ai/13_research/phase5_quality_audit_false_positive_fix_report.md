# Phase 5 Quality Audit False Positive Fix Report

Date: 2026-05-03T02:15:00+08:00

## Prior Audit Result

From `phase5_admitted_relationship_quality_audit.md`:

| Metric | Value |
|--------|-------|
| Total active admitted | 257 (at time of audit) |
| PASS | 247 (96.1%) |
| NEEDS_REVIEW | 10 (3.9%) |
| **Real issues** | **0** |

All 10 flagged edges were **false positives** from substring-based "fake claim" detection.

## False Positive Breakdown

| Trigger | Count | Actual Context | False Positive Reason |
|---------|-------|----------------|----------------------|
| `mpa` | 6 | "compartmentation", "compatibility" | Substring matched inside common words |
| `code section` | 3 | "no specific ... code section claim" | Negative caveat treated as positive claim |
| `asce ` | 1 | "not an ASCE 7 edition" | Negative caveat treated as positive claim |

## Root Cause: Naive Substring Matching

The quality audit used simple substring checks like:

```ts
if (rationale.toLowerCase().includes('mpa')) flag();
if (rationale.toLowerCase().includes('code section')) flag();
if (rationale.toLowerCase().includes('asce')) flag();
```

This approach fails because:
1. **No word boundaries** — "mpa" matches inside "compartmentation"
2. **No negation handling** — "not a code section claim" contains "code section"
3. **No structured context fields** — the audit reads the flat rationale string instead of structured source/context caveat fields

## Recommended Fix

### 1. Word-Boundary Matching

Replace naive substring with regex word boundaries:

```ts
// Before (naive)
if (rationale.toLowerCase().includes('mpa')) flag();

// After (word boundary)
const mpaRegex = /\bmpa\b/i;
if (mpaRegex.test(rationale)) flag();
```

This prevents matching "compartmentation" and "compatibility" while still catching standalone "MPa" unit claims.

### 2. Negation-Aware Filtering

Add a simple negation detector:

```ts
function containsPositiveClaim(text: string, term: string): boolean {
  const lower = text.toLowerCase();
  const termIndex = lower.indexOf(term.toLowerCase());
  if (termIndex === -1) return false;
  // Look back up to 20 chars for negation words
  const prefix = lower.slice(Math.max(0, termIndex - 20), termIndex);
  const negationWords = ['not ', 'no ', 'without ', 'excluding ', 'absent '];
  const isNegated = negationWords.some(n => prefix.includes(n));
  return !isNegated;
}
```

### 3. Structured Cavity Fields

Future schema improvement: add explicit fields to admitted relationships:

```ts
interface AdmittedRelationship {
  // ... existing fields ...
  sourceContext?: {
    hasNumericalClaim: boolean;
    hasCodeSectionClaim: boolean;
    hasStandardReference: boolean;
    hasAHJClaim: boolean;
    caveat?: string;
  };
}
```

This would allow the audit to check structured booleans instead of parsing free-text rationales.

## Current Audit Code Location

The Phase 5 audit was performed manually and documented in `.ai/13_research/phase5_admitted_relationship_quality_audit.md`. There is **no reusable automated audit script** in the codebase.

## Recommended Next Step

Create a reusable quality audit script (`api/auditAdmittedRelationships.ts`) that:
1. Loads `admitted-relationships.json`
2. Applies word-boundary and negation-aware checks
3. Checks for duplicate base/overlay tuples
4. Checks for self-loops
5. Checks rationale length thresholds
6. Outputs a structured JSON/MD report

This is queued for future work, not implemented in this loop.

## Test Coverage for False Positives

Added to `api/graphReasoningPaths.test.ts` (via graph integrity checks):
- All admitted edges have non-empty rationales
- CONSTRAINS edges have rationales >20 chars
- Underrepresented families have rationales >10 chars

These tests do not directly test the false-positive logic but ensure the underlying data quality that the audit verifies.

## Conclusion

The 10 false positives from the Phase 5 audit are fully explained and require no rollback. The fix is to improve the audit matching logic (word boundaries + negation awareness) and eventually build a reusable audit script. No graph mutation is required.
