# Phase 5 Graph Reasoning Path Tests Report

Date: 2026-05-03T01:40:00+08:00
Updated: 2026-05-03T02:45:00+08:00

## Test Suite

File: `api/graphReasoningPaths.test.ts`
Tests: **18** (updated from 14)
Status: **18 pass / 0 fail**

## Coverage

| # | Test | Status | Gap Addressed |
|---|------|--------|---------------|
| 1 | load path: foundation to structural element exists | PASS | baseline |
| 2 | MEP water cycle: supply to conveyance to discharge is traversable | PASS | baseline |
| 3 | cross-domain alignment connects structural and geotechnical domains | PASS | baseline |
| 4 | building envelope has resistance and mitigation relationships | PASS | baseline |
| 5 | coordination relationships exist between building service subsystems | PASS | baseline |
| 6 | constraint paths link regulatory concepts to design domains | PASS | baseline |
| 7 | support hierarchy connects substructure to superstructure | PASS | baseline |
| 8 | information flow edges connect sources to decision domains | PASS | baseline |
| 9 | underrepresented relation families have at least one valid edge each | PASS | baseline |
| 10 | cross-domain alignment pairs are reciprocal | PASS | baseline |
| 11 | admitted edges do not duplicate base graph tuples | PASS | integrity |
| 12 | reasoning path from structural engineering to materials exists | PASS | **Gap closed** (INFORMS admitted) |
| 13 | reasoning path from mechanical systems to thermal comfort exists | PASS | **Gap closed** (AFFECTS admitted) |
| 14 | reasoning path from fire protection to egress exists | PASS | **Gap closed** (CONSTRAINS admitted) |
| 15 | no active CROSS_DOMAIN_EQUIVALENT edge exists | PASS | safety gate |
| 16 | Sendai Mediatheque and Toyo Ito remain visible in graph | PASS | regression |
| 17 | deep and shallow foundations remain distinct and visible | PASS | regression |
| 18 | building envelope remains visible with taxonomy children | PASS | regression |

## Addendum: Post-Quality-Hardening Improvements (2026-05-03)

Tests 15–18 were added in the Phase 5 quality-gate hardening pass. Tests 12–14 were strengthened with exact admitted-edge ID assertions. Test 2 (Drainage) was strengthened to assert both DRAINS_TO and DISCHARGES_TO independently. Test 11 was fixed to use normalized base-edge fields.

## Soft-Logged Gaps (Historical)

Previously soft-logged gaps that are now hard-passing:
- Drainage outgoing discharge: converted from soft-log to hard assertion
- Structural Engineering → Materials: converted from soft-log to hard assertion
- Mechanical Systems → Thermal Comfort: hard assertion since admission
- Fire Protection → Egress: hard assertion since admission

## Edge Count Baseline

- Base edges: 13,670
- Admitted relationships: 264
- Effective edges: 13,934

## Conclusion

All documented reasoning-path gaps are closed and tested with hard assertions. No remaining untested gaps.
