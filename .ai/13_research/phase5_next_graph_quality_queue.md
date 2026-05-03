# Phase 5 Next Graph Quality Queue

Date: 2026-05-03T02:15:00+08:00
Status: Phase 5 quality gate hardening complete. No new admissions.

## Summary

- **Admitted relationships**: 264
- **Effective edges**: 13,934
- **All 4 reasoning-path gaps**: Closed
- **All validations**: PASS
- **P1 hash/review state**: Clean (0 mismatches, 0 stale reviews)
- **Manifest chain**: Valid

---

## 1. Ready for Targeted Safe Admission

These edges have been pre-reviewed and meet all criteria. They should be admitted **only** if a new reasoning-path gap is identified and tested first.

| Source | Target | Type | Rationale | Gap Addressed |
|--------|--------|------|-----------|---------------|
| VTN-DOM-0000056 | VTN-DOM-0000058 | COORDINATES_WITH | Fire protection and egress coordination | Redundant with CONSTRAINS |
| VTN-DOM-0000058 | VTN-DOM-0000056 | COORDINATES_WITH | Egress and fire protection coordination | Redundant with REQUIRES |
| VTN-DOM-0000029 | VTN-DOM-0002477 | COORDINATES_WITH | Structural engineering and materials coordination | Redundant with INFORMS |

**Note**: These 3 deferred edges are semantically valid but redundant for the tested reasoning paths. Admission is optional.

---

## 2. Needs Reasoning-Path Test First

| Candidate | Type | Why Deferred |
|-----------|------|--------------|
| Additional CONNECTS_TO (building entrance ↔ site access) | CONNECTS_TO | No failing test requires it |
| Additional COLLECTS (catch basin → stormwater) | COLLECTS | No failing test requires it |
| Additional DRAINS_TO (roof drain → stormwater) | DRAINS_TO | No failing test requires it |
| Additional REQUIRES (fire alarm → emergency power) | REQUIRES | No failing test requires it |

**Rule**: Do not admit without a corresponding `graphReasoningPaths.test.ts` test that would fail without the edge.

---

## 3. Needs Relation-Vocabulary Update

None. All target relation types are in the admitted vocabulary.

---

## 4. Needs Source/Context Review

| Candidate | Type | Issue |
|-----------|------|-------|
| Grade Beam → Footing Foundation (TRANSFERS_LOAD_TO) | TRANSFERS_LOAD_TO | Verify no duplicate in base graph |
| Soil Bearing Capacity → Foundation System (CONSTRAINS) | CONSTRAINS | Re-evaluate if new context emerges |

---

## 5. High-Risk Blocked

| Packet | Label | Blocker | Next Action |
|--------|-------|---------|-------------|
| p1-decision-packet-fa4918982178 | Mat Foundation | 3-way cross-domain, mixed taxonomy | Future: consider pairwise STR-GEO CROSS_DOMAIN_ALIGNMENT only |
| p1-decision-packet-3946860e327a | Load Path | Different taxonomy contexts | Remains blocked pending domain review |
| p1-decision-packet-0cfa6a7f88a1 | Wall Finishes | 3 nodes, no edges, no resources | Remains blocked; needs human domain review |
| p1-decision-packet-9d2ac282265b | Shear Wall | STR vs ARC taxonomy conflict | Remains blocked |
| p1-decision-packet-12e81a4fbcde | Retaining Wall | Different taxonomy contexts | Remains blocked |

**Standing rule**: No high-risk P1 packet may be admitted without explicit human domain review and project-owner steward approval.

---

## 6. Duplicate / No-Op

- Soil Bearing Capacity → Foundation System: existing graph context provides equivalent semantics
- Redundant footing subtype edges to Soils: deferred as no-op

---

## 7. Rejected (Do Not Revisit Without New Evidence)

- Directionally inverted stormwater flow path → surface runoff edge
- Near-duplicate Erosion And Sediment Control ↔ Civil Erosion And Sediment Control edge
- Overclaim-prone exterior route REQUIRES public-way crossing tie-in

---

## 8. Already Admitted

All 264 admitted relationships are documented in:
- `006_System-Manifests/graph-canonical/admitted-relationships.json`
- `006_System-Manifests/graph-canonical/stewardship-decisions.json`
- `006_System-Manifests/graph-canonical/approvals.json`

---

## 9. Candidate for Resource Layer Review

- `res-asce-7-official-landing`: missing edition/version context
- `res-aci-318-building-code-portal`: missing edition/version context
- `nrl-wind-load-asce-7-needs-review`: missing edition/scope context
- `nrl-seismic-load-asce-7-needs-review`: missing edition/scope context

---

## 10. Candidate for P0 Disambiguation

| Group | Nodes | Status |
|-------|-------|--------|
| Concrete | VTN-DOM-0000068, VTN-DOM-0000267 | P0 unresolved |
| Reinforced Concrete | VTN-DOM-0000271, VTN-DOM-0012147 | P0 unresolved |

**Blocked until**: Human review of whether to merge, alias, or keep separate.

---

## 11. Candidate for Future Raw Wave 10 Scaling (If Ever Resumed)

**Not recommended.** The graph is at 13,934 effective edges with 264 admitted overlays. Further raw scaling risks:
- COORDINATES_WITH dominance exceeding 50%
- Generic edge proliferation
- Quality audit fatigue

If scaling resumes, it should be:
- **Targeted by reasoning-path gaps**, not raw count
- **Limited to underrepresented families** (CONNECTS_TO, COLLECTS, DRAINS_TO, REQUIRES)
- **Preceded by a reasoning-path test** for every batch

---

## Next Recommended Action

1. Monitor reasoning-path tests for regressions.
2. Address the 2 NEEDS_REVIEW COORDINATES_WITH edges from the sampling audit (items 19 and 30).
3. Consider a COORDINATES_WITH reciprocity wave (~76 missing reciprocal edges) as a structural quality improvement.
4. Do not resume raw edge scaling.
