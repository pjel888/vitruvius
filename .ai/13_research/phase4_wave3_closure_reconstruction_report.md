# Phase 4 Wave 3 Closure Reconstruction Report

Date: 2026-05-03T01:00:00Z
Reconstructed by: Kimi

## Wave 3 Decision & Approval

- **Decision ID:** `canonical-20260502171741-96d8b48708fd`
- **Approval ID:** `canonical-approval-20260502171951-e01d8fde338c`
- **Decision type:** `AEC_RELATIONSHIP_ENRICHMENT`
- **Approved by:** `project_owner_steward`
- **Approved at:** 2026-05-02T17:19:51.094Z
- **Mutation scope:** `non_destructive_edge_admission`
- **Rollback capability:** `full`
- **Transaction manifest:** `canonical-tx-20260502171951-96f360c92ef4.json`

## Pre-Wave 3 Baseline

- Base graph edges: 13,670
- Admitted relationships: 80
- Effective edges: 13,750
- Nodes: 10,018
- Aliases / redirects / tombstones: 0 / 0 / 0

## Post-Wave 3 State

- Base graph edges: 13,670 (unchanged)
- Admitted relationships: 102
- Effective edges: 13,772
- Nodes: 10,018 (unchanged)
- Aliases / redirects / tombstones: 0 / 0 / 0

## Wave 3 Admitted Edge Table (22 edges)

| # | Edge ID | Source | Target | Type | Weight | Rationale Summary |
|---|---------|--------|--------|------|--------|-------------------|
| 1 | VTN-DOM-0012759--collects--VTN-DOM-0012758 | VTN-DOM-0012759 | VTN-DOM-0012758 | COLLECTS | 0.5 | Catch basin collects surface runoff; non-numerical, non-jurisdiction-specific |
| 2 | VTN-DOM-0012759--drains_to--VTN-DOM-0012760 | VTN-DOM-0012759 | VTN-DOM-0012760 | DRAINS_TO | 0.5 | Catch basin drains to storm sewer pipe; no hydraulic sizing claim |
| 3 | VTN-DOM-0012760--conveys--VTN-DOM-0005262 | VTN-DOM-0012760 | VTN-DOM-0005262 | CONVEYS | 0.5 | Storm sewer pipe conveys stormwater flow path; non-numerical, non-code-specific |
| 4 | VTN-DOM-0012762--collects--VTN-DOM-0012758 | VTN-DOM-0012762 | VTN-DOM-0012758 | COLLECTS | 0.5 | Inlet capacity collects surface runoff; no capacity or design value asserted |
| 5 | VTN-DOM-0000224--mitigates--VTN-DOM-0012758 | VTN-DOM-0000224 | VTN-DOM-0012758 | MITIGATES | 0.5 | Detention/retention mitigates surface runoff; does not assert full prevention or code compliance |
| 6 | VTN-DOM-0012769--informs--VTN-DOM-0012273 | VTN-DOM-0012769 | VTN-DOM-0012273 | INFORMS | 0.5 | Geotechnical investigation informs foundation system; no numerical criterion or standard edition claim |
| 7 | VTN-DOM-0012770--informs--VTN-DOM-0012767 | VTN-DOM-0012770 | VTN-DOM-0012767 | INFORMS | 0.5 | Soil infiltration rate informs permeable pavement; no numerical design criterion asserted |
| 8 | VTN-DOM-0012280--affects--VTN-DOM-0012273 | VTN-DOM-0012280 | VTN-DOM-0012273 | AFFECTS | 0.5 | Foundation settlement affects foundation system; no specific settlement value or code compliance |
| 9 | VTN-DOM-0000317--affects--VTN-DOM-0000313 | VTN-DOM-0000317 | VTN-DOM-0000313 | AFFECTS | 0.5 | Groundwater affects excavation support; no dewatering design claim |
| 10 | VTN-DOM-0003029--constrains--VTN-DOM-0002906 | VTN-DOM-0003029 | VTN-DOM-0002906 | CONSTRAINS | 0.5 | Slope stability constrains site grading; non-numerical, non-jurisdiction-specific |
| 11 | VTN-DOM-0012773--affects--VTN-DOM-0012273 | VTN-DOM-0012773 | VTN-DOM-0012273 | AFFECTS | 0.5 | Differential settlement evaluation affects foundation system; no numerical criterion asserted |
| 12 | VTN-DOM-0012273--supports--VTN-DOM-0012269 | VTN-DOM-0012273 | VTN-DOM-0012269 | SUPPORTS | 0.5 | Foundation system supports column; does not replace load-path precision |
| 13 | VTN-DOM-0012273--supports--VTN-DOM-0012261 | VTN-DOM-0012273 | VTN-DOM-0012261 | SUPPORTS | 0.5 | Foundation system supports column grid; non-numerical, non-code-specific |
| 14 | VTN-DOM-0012269--supports--VTN-DOM-0012263 | VTN-DOM-0012269 | VTN-DOM-0012263 | SUPPORTS | 0.5 | Column supports beam; directionality is source-supports-target, not load transfer |
| 15 | VTN-DOM-0012282--resists--VTN-DOM-0000259 | VTN-DOM-0012282 | VTN-DOM-0000259 | RESISTS | 0.5 | Braced frame resists lateral loads; no capacity or member-sizing claim |
| 16 | VTN-DOM-0012283--resists--VTN-DOM-0000259 | VTN-DOM-0012283 | VTN-DOM-0000259 | RESISTS | 0.5 | Moment frame resists lateral loads; no capacity or member-sizing claim |
| 17 | VTN-DOM-0000233--coordinates_with--VTN-DOM-0012749 | VTN-DOM-0000233 | VTN-DOM-0012749 | COORDINATES_WITH | 0.5 | Site access coordinates with site finished floor elevation interface; non-numerical, non-jurisdiction-specific |
| 18 | VTN-DOM-0000012--coordinates_with--VTN-DOM-0000233 | VTN-DOM-0000012 | VTN-DOM-0000233 | COORDINATES_WITH | 0.5 | Accessible routes coordinates with site access; no code-compliance assertion |
| 19 | VTN-DOM-0012809--coordinates_with--VTN-DOM-0000012 | VTN-DOM-0012809 | VTN-DOM-0000012 | COORDINATES_WITH | 0.5 | Curb ramp geometry interface coordinates with accessible routes; non-numerical, non-jurisdiction-specific |
| 20 | VTN-DOM-0012289--coordinates_with--VTN-DOM-0012794 | VTN-DOM-0012289 | VTN-DOM-0012794 | COORDINATES_WITH | 0.5 | Expansion joint coordinates with structural movement joint; non-numerical, non-code-specific |
| 21 | VTN-DOM-0012313--coordinates_with--VTN-DOM-0012743 | VTN-DOM-0012313 | VTN-DOM-0012743 | COORDINATES_WITH | 0.5 | Facade assembly coordinates with facade anchor interface; no anchor-capacity claim |
| 22 | VTN-DOM-0012311--transfers_load_to--VTN-DOM-0012263 | VTN-DOM-0012311 | VTN-DOM-0012263 | TRANSFERS_LOAD_TO | 0.5 | Roof assembly transfers load to beam; no load value or member-sizing claim |

## Relation Type Distribution (Wave 3 only)

| Type | Count |
|------|-------|
| COORDINATES_WITH | 5 |
| AFFECTS | 3 |
| SUPPORTS | 3 |
| COLLECTS | 2 |
| INFORMS | 2 |
| RESISTS | 2 |
| CONSTRAINS | 1 |
| CONVEYS | 1 |
| DRAINS_TO | 1 |
| MITIGATES | 1 |
| TRANSFERS_LOAD_TO | 1 |
| **Total** | **22** |

## Verification Checklist

- [x] All 22 edges have existing endpoints in the shadow graph
- [x] All 22 edges use valid relation types from `CanonicalStewardshipRelationType`
- [x] No duplicate of base graph edge
- [x] No duplicate of prior admitted overlay
- [x] No self-loops
- [x] All edges carry `stewardshipDecisionId` and `approvalId`
- [x] All edges carry domain-synthesis rationale with no overclaim
- [x] Decision has full rollback capability
- [x] Transaction manifest covers all changed custody files
- [x] No alias, redirect, or tombstone created
- [x] No Resource Layer mutation
- [x] No CROSS_DOMAIN_EQUIVALENT active admitted edge
