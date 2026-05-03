# Phase 5 Graph Reasoning Quality Gate Report

Date: 2026-05-03T02:15:00+08:00

## Test File

`api/graphReasoningPaths.test.ts` — 14 tests (prior to this review)

## Coverage Matrix

| Requirement | Test Name | Status | Notes |
|-------------|-----------|--------|-------|
| Load path traversal | "load path: foundation to structural element exists" | **PASS** | Checks Deep Foundations has structural edges |
| MEP water cycle | "MEP water cycle: supply to conveyance to discharge is traversable" | **PASS** | Checks Drainage has outgoing DISCHARGES_TO/DRAINS_TO |
| Cross-domain alignment | "cross-domain alignment connects structural and geotechnical domains" | **PASS** | Checks CROSS_DOMAIN_ALIGNMENT between STR and GEO |
| Building envelope resistance | "building envelope has resistance and mitigation relationships" | **PASS** | Checks RESISTS and MITIGATES edges |
| Coordination relationships | "coordination relationships exist between building service subsystems" | **PASS** | Checks MEP subsystem COORDINATES_WITH |
| Constraint paths | "constraint paths link regulatory concepts to design domains" | **PASS** | Checks CONSTRAINS edges with rationale |
| Support hierarchy | "support hierarchy connects substructure to superstructure" | **PASS** | Checks SUPPORTS edges |
| Information flow | "information flow edges connect sources to decision domains" | **PASS** | Checks INFORMS edges |
| Underrepresented families | "underrepresented relation families have at least one valid edge each" | **PASS** | Checks DRAINS_TO, CONNECTS_TO, REQUIRES, COLLECTS |
| Cross-domain reciprocity | "cross-domain alignment pairs are reciprocal" | **PASS** | Checks all CROSS_DOMAIN_ALIGNMENT edges have reciprocals |
| No duplicate base tuples | "admitted edges do not duplicate base graph tuples" | **PASS** | Key-value uniqueness check |
| Structural → Materials | "reasoning path from structural engineering to materials exists" | **PASS** | Phase 5 gap closure; hard assertion within 3 hops |
| Mechanical → Thermal | "reasoning path from mechanical systems to thermal comfort exists" | **PASS** | Phase 5 gap closure; hard assertion within 3 hops |
| Fire → Egress | "reasoning path from fire protection to egress exists" | **PASS** | Phase 5 gap closure; hard assertion within 3 hops |

## Gaps Identified in This Review

| Requirement | Prior Coverage | Action Taken |
|-------------|---------------|--------------|
| No active CROSS_DOMAIN_EQUIVALENT edge | Not tested | **Added** — new test verifies zero active edges |
| Sendai Mediatheque / Toyo Ito visibility | Covered in canonical stewardship API tests only | **Added** — new test verifies HAS_FACET edge visibility in graph |
| Deep/Shallow Foundations distinction | Partially covered | **Added** — new test verifies distinct path codes and edge presence |
| Building Envelope visibility | Not directly tested | **Added** — new test verifies node exists with taxonomy children |
| Cross-domain alignment ≠ merge | Covered by reciprocity test | Sufficient — no equivalence edges exist |

## Updated Test Count

- **Before**: 14 tests
- **After**: 18 tests
- **All pass**: 18/18

## Test Robustness Improvement

Normalized base-edge keys (`from_id` → `source`, `to_id` → `target`, `predicate` → `type`) so that base graph edges and admitted edges are uniformly traversable in BFS path finding. This fixes a latent issue where base edges were present in `effectiveEdges` but not indexed due to missing `source`/`type` properties.

## Quality Gate Recommendations

1. **Reasoning-path tests should remain hard assertions** — no soft `console.warn` or optional expects.
2. **Any future gap closure must add a corresponding test** before admission.
3. **BFS path tests should specify allowed relation types explicitly** — do not use generic traversals.
4. **Max depth should be bounded** (≤5 for most paths; ≤3 for targeted gaps).
5. **Node existence should be asserted before path search** — prevents false positives from missing nodes.

## Conclusion

Graph reasoning quality gate is now hardened with 18 tests covering all critical reasoning paths, cross-domain alignment safety, iconic node visibility, foundation distinction, and the CROSS_DOMAIN_EQUIVALENT block. All tests pass.
