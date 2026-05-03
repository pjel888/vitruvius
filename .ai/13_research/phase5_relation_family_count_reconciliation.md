# Phase 5 Relation Family Count Reconciliation

Date: 2026-05-03T01:00:00+08:00

## Claimed vs Actual

| Source | Count |
|--------|-------|
| Overnight report claim | 16 active relation families |
| Registry-derived actual | 15 active relation families |
| Vocabulary total | 22 admitted relation types |

## Registry-Derived Distribution

| Rank | Relation Family | Count | % of Total |
|------|----------------|-------|------------|
| 1 | COORDINATES_WITH | 122 | 47.5% |
| 2 | TRANSFERS_LOAD_TO | 30 | 11.7% |
| 3 | CROSS_DOMAIN_ALIGNMENT | 22 | 8.6% |
| 4 | SUPPORTS | 19 | 7.4% |
| 5 | DISCHARGES_TO | 13 | 5.1% |
| 6 | CONVEYS | 13 | 5.1% |
| 7 | CONSTRAINS | 11 | 4.3% |
| 8 | AFFECTS | 6 | 2.3% |
| 9 | MITIGATES | 5 | 1.9% |
| 10 | INFORMS | 5 | 1.9% |
| 11 | RESISTS | 5 | 1.9% |
| 12 | REQUIRES | 2 | 0.8% |
| 13 | COLLECTS | 2 | 0.8% |
| 14 | DRAINS_TO | 1 | 0.4% |
| 15 | CONNECTS_TO | 1 | 0.4% |
| **Total** | | **257** | **100%** |

## Mismatch Root Cause

The overnight report miscounted. The actual registry has **15** active relation families, not 16.

The vocabulary (`ADMITTED_RELATIONSHIP_TYPES` in `api/graph/canonicalStewardship.ts`) defines **22** possible relation types. Seven types have **0** active admitted edges:

1. `DISAMBIGUATED_FROM` — used in P1 decisions but not in admitted relationship overlay
2. `RELATED_SPECIALIZATION_OF` — 0 active
3. `HAS_DOMAIN_SPECIALIZATION` — 0 active
4. `CROSS_DOMAIN_CLOSE_MATCH` — 0 active
5. `CROSS_DOMAIN_RELATED_MATCH` — 0 active
6. `CLOSE_MATCH` — 0 active
7. `RELATED_MATCH` — 0 active

## Verification

- Sum of all 15 family counts = 257 ✓
- Matches `admittedRelationships.filter(r => !r.revoked).length` = 257 ✓
- No rolled-back edges are included in the count ✓
- No duplicate type aliases are present ✓

## Conclusion

**Reporting-only error.** The registry is internally consistent. The overnight report overstated the family count by one. No remediation of the registry is required; only the report narrative needs correction.
