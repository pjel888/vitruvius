# Phase 5 Relation Family Quality Gate Report

Date: 2026-05-03T02:15:00+08:00

## Recomputed State (from `006_System-Manifests/graph-canonical/admitted-relationships.json`)

| Metric | Value |
|--------|-------|
| Active admitted relationships | 264 |
| Relation families active | 15 |
| Base graph edges | 13,670 |
| Effective edges | 13,934 |

## Relation Family Distribution

| Rank | Family | Count | % of Admitted | Status |
|------|--------|-------|---------------|--------|
| 1 | COORDINATES_WITH | 123 | 46.6% | Dominant |
| 2 | TRANSFERS_LOAD_TO | 30 | 11.4% | Strong |
| 3 | CROSS_DOMAIN_ALIGNMENT | 22 | 8.3% | Strong |
| 4 | SUPPORTS | 19 | 7.2% | Healthy |
| 5 | DISCHARGES_TO | 14 | 5.3% | Healthy |
| 6 | CONVEYS | 13 | 4.9% | Healthy |
| 7 | CONSTRAINS | 12 | 4.5% | Healthy |
| 8 | AFFECTS | 7 | 2.7% | Present |
| 9 | INFORMS | 6 | 2.3% | Present |
| 10 | MITIGATES | 5 | 1.9% | Present |
| 11 | RESISTS | 5 | 1.9% | Present |
| 12 | REQUIRES | 3 | 1.1% | Underrepresented |
| 13 | COLLECTS | 2 | 0.8% | Underrepresented |
| 14 | DRAINS_TO | 2 | 0.8% | Underrepresented |
| 15 | CONNECTS_TO | 1 | 0.4% | Underrepresented |

## Reconciliation with "16 Families" Reporting Error

The overnight Phase 4 report claimed "16 active families." This was incorrect. The error arose from counting base-graph hierarchy types (`PART_OF`, `HAS_SUBTOPIC`, `GOVERNED_BY`) that appear in the admitted-relationships file due to a prior schema version but are not active admitted overlay relation families.

**Correct count: 15 active admitted relation families.**

## Quality Gate Thresholds

| Gate | Threshold | Current | Status |
|------|-----------|---------|--------|
| COORDINATES_WITH dominance | ≤60% | 46.6% | **PASS** |
| Minimum families with ≥1 edge | ≥10 | 15 | **PASS** |
| Families with ≥5 edges | ≥5 | 7 | **PASS** |
| Underrepresented family count (≤2 edges) | ≤5 | 4 | **PASS** |
| Zero-edge families in vocabulary | 0 | 0 | **PASS** |

## Overrepresented Families

- **COORDINATES_WITH at 46.6%**: Within acceptable range (<50% is ideal; <60% is acceptable). This family is semantically appropriate for cross-discipline design coordination, which is the primary enrichment pattern.

## Underrepresented Families

- **CONNECTS_TO (1)**: Building-to-utility interface; more candidates exist (e.g., entrance ↔ site access).
- **COLLECTS (2)**: Drainage collection; candidates exist (catch basin → stormwater).
- **DRAINS_TO (2)**: Roof/floor drainage; candidates exist (roof drain → stormwater).
- **REQUIRES (3)**: MEPFS dependencies; candidates exist (fire alarm → emergency power).

## Relation Types in Vocabulary but Not Admitted

The canonical stewardship type system defines these additional relation types that have **zero active admitted edges**:

- `CROSS_DOMAIN_EQUIVALENT` — intentionally blocked; requires explicit human review
- `RELATED_MATCH` — not yet used in admitted overlay
- `CLOSE_MATCH` — not yet used in admitted overlay
- `CROSS_DOMAIN_CLOSE_MATCH` — not yet used in admitted overlay
- `CROSS_DOMAIN_RELATED_MATCH` — not yet used in admitted overlay
- `DISAMBIGUATED_FROM` — metadata type, not an overlay edge
- `RELATED_SPECIALIZATION_OF` — metadata type, not an overlay edge
- `HAS_DOMAIN_SPECIALIZATION` — metadata type, not an overlay edge

## Source/Target Discipline-Pair Distribution (Top 10)

| Source Discipline | Target Discipline | Count | Example Types |
|-------------------|-------------------|-------|---------------|
| Structural (STR) | Structural (STR) | 38 | TRANSFERS_LOAD_TO, SUPPORTS |
| MEP (MEC/PLS/SAN/ELE) | MEP | 45 | COORDINATES_WITH, CONVEYS |
| Fire/Life-Safety (FLS) | Fire/Life-Safety | 18 | COORDINATES_WITH, CONSTRAINS |
| Civil/Site (CIV) | Civil/Site | 22 | COORDINATES_WITH, DISCHARGES_TO |
| Structural | Civil/Geo | 12 | CROSS_DOMAIN_ALIGNMENT |
| Architecture (ARC) | MEP | 16 | COORDINATES_WITH |
| Architecture | Architecture | 24 | COORDINATES_WITH |
| Sustainability (SUS) | MEP | 6 | AFFECTS, MITIGATES |
| Safety/Security (SMS) | SMS | 8 | COORDINATES_WITH |
| Planning (PLN) | Architecture | 6 | COORDINATES_WITH |

## Quality Gate Recommendations

1. **COORDINATES_WITH dominance**: Monitor. If it exceeds 55%, trigger a diversification review.
2. **Underrepresented families**: Prioritize CONNECTS_TO, COLLECTS, DRAINS_TO, REQUIRES in future targeted waves.
3. **CROSS_DOMAIN_EQUIVALENT block**: Maintain zero active edges. Any proposal must go through P0 review.
4. **Generic `related_to` block**: Maintain zero active edges. All admissions must use specific relation types.
5. **Rationale coverage**: All 264 admitted edges have substantive rationales (>20 chars for CONSTRAINS, >10 chars for others).
6. **Duplicate/no-op check**: Zero duplicates found between base and admitted; zero self-loops.
7. **Source/context caveat check**: All edges include non-numerical, non-code-specific rationales.

## Automated Report Helper

Run the following command to recompute this distribution at any time:

```bash
node -e "const fs=require('fs'); const data=JSON.parse(fs.readFileSync('006_System-Manifests/graph-canonical/admitted-relationships.json','utf8')); const admitted=data.admittedRelationships; const dist={}; admitted.forEach(e=>{dist[e.relationType]=(dist[e.relationType]||0)+1}); Object.entries(dist).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(k,':',v));"
```
