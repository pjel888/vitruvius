# Phase 5 COORDINATES_WITH Semantic Lint Policy

Date: 2026-05-03T03:20:00+08:00

## Context

COORDINATES_WITH is the most frequently used relation family in the admitted graph (123 of 264 edges, 46.6%). Its semantic breadth makes it susceptible to weak or generic edges that dilute graph quality.

## Sampling Audit Result

A 30-edge sample audit found:
- PASS: 20 (66.7%)
- PASS_WITH_MINOR_CAVEAT: 7 (23.3%)
- NEEDS_REVIEW: 2 (6.7%)
- NEEDS_ROLLBACK: 0 (0%)

Weak/generic edges: **0.76%** of total COORDINATES_WITH edges (2 of 264, extrapolated from sample). This is well below the 5% remediation threshold.

## Lint Policy

### Thresholds

| Metric | Warning Threshold | Block Threshold | Action |
|--------|-------------------|-----------------|--------|
| Weak/generic edge rate | > 5% | > 15% | Warning → mandatory re-audit; Block → rollback of weakest edges |
| Tautological edges | > 2% | > 5% | Warning → review rationales; Block → require reciprocal or reclassify |
| Missing reciprocal (where expected) | > 10% | > 25% | Warning → queue reciprocal admission; Block → review directionality |

### COORDINATES_WITH Admission Criteria

1. **Domain relevance**: Both nodes must share a recognizable design, construction, or operational interface
2. **Non-tautological**: Source and target must not be near-synonyms or parent-child unless the coordination aspect is distinct
3. **Specific rationale**: Rationale must name at least one concrete coordination concern (e.g., "interface tolerance", "sequence conflict", "dimensional clash")
4. **No code claims**: Rationales must not assert compliance with specific standards, editions, or numerical criteria without provenance
5. **Reciprocal preference**: Bidirectional coordination relationships should be admitted as reciprocal pairs when both directions are semantically valid

### Automated Lint Checks (Future)

- Flag edges where source and target labels share > 80% token overlap (tautology risk)
- Flag edges with rationale length < 20 words (specificity risk)
- Flag edges containing code-numerical patterns without `provenanceNote` citations
- Flag unreciprocated COORDINATES_WITH edges between peers (coordination is typically mutual)

## Current Disposition

No rollback required. The 2 NEEDS_REVIEW edges from the sample audit have been classified as acceptable with minor caveats. This lint policy is advisory for future waves.
