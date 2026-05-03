# Phase 5 Admitted Relationship Quality Audit

Date: 2026-05-03T01:00:00+08:00
Scope: All 257 active admitted relationships
Method: Automated audit + manual review of flagged edges

## Summary

| Metric | Value |
|--------|-------|
| Total active admitted | 257 |
| PASS | 247 (96.1%) |
| NEEDS_REVIEW | 10 (3.9%) |
| NEEDS_ROLLBACK | 0 (0%) |
| Duplicates of base graph | 0 |
| Duplicates of overlay | 0 |
| Missing source/target nodes | 0 |
| Missing approvals | 0 |
| Missing decisions | 0 |
| Self-loops | 0 |
| Empty/weak rationales | 0 |

## Issue Breakdown

The 10 flagged edges triggered substring-based "fake claim" indicators. **All 10 are false positives upon manual review.**

| Trigger | Count | Explanation |
|---------|-------|-------------|
| `mpa` | 6 | Appears inside words: "compartmentation", "compatibility" — not MPa (megapascal) unit claims |
| `code section` | 3 | Appears in negative claims: "no specific ... code section claim" — explicitly safe |
| `asce ` | 1 | Appears in negative claim: "not an ASCE 7 edition" — explicitly safe |

## Audited Subpopulations

### Underrepresented Families (all edges)

| Family | Edges | Result |
|--------|-------|--------|
| REQUIRES | 2 | PASS |
| COLLECTS | 2 | PASS |
| DRAINS_TO | 1 | PASS |
| CONNECTS_TO | 1 | PASS |

### Wave 9 Edges (all 15 edges)

| Edge | Type | Result |
|------|------|--------|
| VTN-DOM-0000033→0000121 | AFFECTS | PASS |
| VTN-DOM-0000033→0000122 | AFFECTS | PASS |
| VTN-DOM-0000025→0002490 | AFFECTS | PASS |
| VTN-DOM-0000411→0000414 | REQUIRES | PASS |
| VTN-DOM-0000255→0000033 | RESISTS | PASS |
| VTN-DOM-0000256→0000033 | RESISTS | PASS |
| VTN-DOM-0000286→0000038 | RESISTS | PASS |
| VTN-DOM-0003291→0000438 | MITIGATES | PASS |
| VTN-DOM-0000439→0000437 | MITIGATES | PASS (false positive: "compartmentation") |
| VTN-DOM-0000087→0000054 | MITIGATES | PASS |
| VTN-DOM-0000286→0000038 | MITIGATES | PASS |
| VTN-DOM-0000863→0000372 | COORDINATES_WITH | PASS |
| VTN-DOM-0000863→0000369 | COORDINATES_WITH | PASS |
| VTN-DOM-0000585↔0000086 | CROSS_DOMAIN_ALIGNMENT | PASS |
| VTN-DOM-0000086↔0000585 | CROSS_DOMAIN_ALIGNMENT | PASS |

### High-Risk P1 Adjacent Edges

All 12 edges adjacent to high-risk P1 concepts (Concrete, Reinforced Concrete, Mat Foundation, Load Path, Shear Wall, Retaining Wall) pass with 1 false positive.

## COORDINATES_WITH Sampling

See `phase5_coordinates_with_sampling_audit.md` for detailed sample results.

## Conclusion

**Zero substantive quality issues found.** All 257 active admitted relationships have:
- Valid endpoints
- Unique overlay tuples (no base/overlay duplication)
- Present and substantive rationales
- Linked approvals and decisions
- No fake source/code/AHJ/numerical claims
- No self-loops

The automated flagging produced 10 false positives from substring matching inside safe negative claims or common words. No rollback action is required.
