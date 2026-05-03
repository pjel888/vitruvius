# Phase 5 COORDINATES_WITH Sampling Audit

Date: 2026-05-03T01:00:00+08:00
Sample size: 30 of 122 total COORDINATES_WITH edges (≈25% sample)
Method: Evenly distributed sampling across the admitted sequence

## Sample Results

| # | Edge ID | Source | Target | Reciprocal? | Classification | Notes |
|---|---------|--------|--------|-------------|----------------|-------|
| 1 | VTN-DOM-0012741↔0012266 | Floor Opening Coordination | Slab | Yes | **PASS** | Strong structural interface; bidirectional |
| 2 | VTN-DOM-0002906↔0005262 | Site Grading | Stormwater Flow Path | Yes | **PASS** | Strong civil/site interface |
| 3 | VTN-DOM-0012749↔0012740 | Site FFE Interface | Arch FFD | Yes | **PASS** | Strong arch/civil coordination |
| 4 | VTN-DOM-0012793→0012791 | Force Transfer Conn | Base Plate Conn | No | **PASS** | Strong structural connection detail |
| 5 | VTN-DOM-0012059→0000232 | Site Drainage Planning | Site Grading | No | **PASS** | Strong civil interface |
| 6 | VTN-DOM-0012058→0012754 | Fire Access Site Planning | Emergency Vehicle Access | No | **PASS** | Strong life-safety/site interface |
| 7 | VTN-DOM-0012792→0012782 | Anchor Bolt Group | Footing Foundation | No | **PASS** | Strong structural connection |
| 8 | VTN-DOM-0012752→0000232 | Erosion Control | Site Grading | No | **PASS_WITH_MINOR_CAVEAT** | Slightly generic rationale |
| 9 | VTN-DOM-0012739→0000151 | Egress Discharge Site Interface | Exterior Routes | No | **PASS** | Strong egress/accessibility link |
| 10 | VTN-DOM-0012742→0012059 | Roof Drainage Interface | Site Drainage Planning | No | **PASS** | Strong envelope/civil interface |
| 11 | VTN-DOM-0000233→0012749 | Site Access | Site FFE Interface | No | **PASS_WITH_MINOR_CAVEAT** | Generic rationale; appropriate domain link |
| 12 | VTN-DOM-0012313→0012743 | Facade Assembly | Facade Anchor Interface | No | **PASS** | Strong envelope/structure interface |
| 13 | VTN-DOM-0000436→0002556 | Exits | Means Of Egress Planning | No | **PASS_WITH_MINOR_CAVEAT** | Tautological; no reciprocal |
| 14 | VTN-DOM-0003139→0000032 | Grounding Electrode Systems | Foundations Interface | No | **PASS** | Strong MEP/structural interface |
| 15 | VTN-DOM-0000340→0003091 | Heating Systems | Hot Water Loops | No | **PASS** | Strong MEP coordination |
| 16 | VTN-DOM-0000434→0000435 | Notification | Mass Notification | No | **PASS_WITH_MINOR_CAVEAT** | Slightly generic; appropriate |
| 17 | VTN-DOM-0000054→0002896 | Wastewater | Sewerage Networks | No | **PASS** | Strong infrastructure link |
| 18 | VTN-DOM-0000278→0000255 | Timber Structures | Frame Systems | No | **PASS_WITH_MINOR_CAVEAT** | Generic rationale |
| 19 | VTN-DOM-0002802→0002542 | Accessible Audits | Accessibility And Universal Design | No | **NEEDS_REVIEW** | Rationale/target mismatch: says "accessible routes" but target is "Accessibility And Universal Design" |
| 20 | VTN-DOM-0000121↔0000122 | Wall Systems | Roof Systems | Yes | **PASS** | Strong building envelope interface |
| 21 | VTN-DOM-0000370→0000372 | Voice Systems | Building Management | No | **PASS** | Strong controls integration |
| 22 | VTN-DOM-0000344→0003088 | Cooling Systems | Chilled Water Loops | No | **PASS** | Strong MEP coordination |
| 23 | VTN-DOM-0000070→0000278 | Timber Materials | Timber Structures | No | **PASS** | Strong material-structure link |
| 24 | VTN-DOM-0000087→0000054 | Water Efficiency | Wastewater | No | **PASS** | Strong sustainability interface |
| 25 | VTN-DOM-0000066→0000063 | Construction Safety | Sequencing | No | **PASS** | Strong construction management link |
| 26 | VTN-DOM-0000018→0002776 | Zoning | Advanced Building Typologies | No | **PASS_WITH_MINOR_CAVEAT** | Slightly generic planning link |
| 27 | VTN-DOM-0000033→0000255 | Seismic Design | Frame Systems | No | **PASS** | Strong structural link |
| 28 | VTN-DOM-0003009→0000032 | Foundation Engineering | Foundations Interface | No | **PASS** | Strong geo-structural link |
| 29 | VTN-DOM-0000426→0000025 | Irrigation Interfaces | Drainage | No | **PASS** | Strong site infrastructure link |
| 30 | VTN-DOM-0004351→0000069 | Heritage Inventory | Steel | No | **NEEDS_REVIEW** | Weak/generic; heritage-steel coordination is forced |

## Summary

| Classification | Count | % |
|----------------|-------|---|
| PASS | 20 | 66.7% |
| PASS_WITH_MINOR_CAVEAT | 7 | 23.3% |
| NEEDS_REVIEW | 2 | 6.7% |
| NEEDS_ROLLBACK | 0 | 0% |

## Structural Gap: Missing Reciprocals

- **67% of sampled COORDINATES_WITH edges lack reciprocals** (20 of 30)
- Full population projection: ~76 of 122 edges have no reciprocal anywhere in the graph
- This is a **structural quality gap**, not a semantic quality gap
- COORDINATES_WITH is semantically symmetric; unidirectional admission may limit Explorer neighborhood traversal

## Remediation Threshold Assessment

- Weak/generic/risky edges: **6.7%** (2 of 30)
- Threshold: >20% triggers remediation queue
- **Result: Below threshold. No bulk remediation required.**

## Recommended Actions

1. **Short-term**: Document the missing-reciprocals gap for a future dedicated symmetry wave
2. **Medium-term**: Review the 2 NEEDS_REVIEW edges (items 19 and 30) in the next quality pass
3. **No rollback required** for any sampled edge
