# Phase 5 Relation Family Coverage Report

Date: 2026-05-03T01:00:00+08:00
Base: 257 active admitted relationships

## Relation Family Distribution

| Rank | Family | Count | % | Status |
|------|--------|-------|---|--------|
| 1 | COORDINATES_WITH | 122 | 47.5% | Dominant — reviewed, mostly strong |
| 2 | TRANSFERS_LOAD_TO | 30 | 11.7% | Healthy structural load-path coverage |
| 3 | CROSS_DOMAIN_ALIGNMENT | 22 | 8.6% | Healthy cross-domain coverage |
| 4 | SUPPORTS | 19 | 7.4% | Healthy structural support coverage |
| 5 | DISCHARGES_TO | 13 | 5.1% | Moderate MEP/civil flow coverage |
| 6 | CONVEYS | 13 | 5.1% | Moderate MEP conveyance coverage |
| 7 | CONSTRAINS | 11 | 4.3% | Moderate regulatory coverage |
| 8 | AFFECTS | 6 | 2.3% | Underrepresented |
| 9 | MITIGATES | 5 | 1.9% | Underrepresented |
| 10 | INFORMS | 5 | 1.9% | Underrepresented |
| 11 | RESISTS | 5 | 1.9% | Underrepresented |
| 12 | REQUIRES | 2 | 0.8% | Underrepresented |
| 13 | COLLECTS | 2 | 0.8% | Underrepresented |
| 14 | DRAINS_TO | 1 | 0.4% | Underrepresented |
| 15 | CONNECTS_TO | 1 | 0.4% | Underrepresented |

## Vocabulary Gap

7 relation types in the vocabulary have 0 active admitted edges:
- DISAMBIGUATED_FROM
- RELATED_SPECIALIZATION_OF
- HAS_DOMAIN_SPECIALIZATION
- CROSS_DOMAIN_CLOSE_MATCH
- CROSS_DOMAIN_RELATED_MATCH
- CLOSE_MATCH
- RELATED_MATCH

These are intentionally reserved for future P1 disambiguation and closer-match use cases.

## Discipline Pair Coverage

Top cross-discipline pairs (by node path_code prefix):

| Count | Pair |
|-------|------|
| 38 | Structural → Structural |
| 29 | Architectural → Architectural |
| 17 | Other → Architectural |
| 9 | Architectural → Other |
| 8 | Architectural → Structural |
| 6 | Structural → Geotechnical |
| 6 | Structural → Architectural |
| 6 | Other → Structural |
| 5 | Materials → Structural |
| 4 | Geotechnical → Structural |

("Other" = nodes not matching standard discipline prefixes)

## Gaps Identified

1. **Fire Protection ↔ Egress**: Zero edges connecting FLS and FLS.EGR domains
2. **Mechanical Systems → Thermal Comfort**: Zero edges connecting MEC and ARC.ECD.THC
3. **Structural Engineering → Materials**: Zero edges connecting STR and ARC.MAT
4. **Drainage → Discharge**: Drainage has incoming DISCHARGES_TO but no outgoing drain/discharge edges
5. **MEP subsystem coordination**: Limited cross-MEP coordination edges

## Recommendation

Targeted gap closure should focus on the 4 fundamental reasoning-path gaps above. Each gap represents a high-value traversal path that is currently broken in the effective graph.
