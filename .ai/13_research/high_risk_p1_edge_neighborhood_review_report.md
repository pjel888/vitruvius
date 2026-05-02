# High-Risk P1 Edge-Neighborhood Review Report

Date: 2026-05-03T01:00:00Z

## Previously Reviewed

### Shear Wall (Wave 2)
- Packet: `p1-decision-packet-9d2ac282265b`
- Outcome: **Blocked** — remains high-risk. STR seismic subtopic vs ARC building coordination concept. Different taxonomy scopes.

## Wave 3 Review: Mat Foundation

### Packet Identity
- **Packet ID:** `p1-decision-packet-fa4918982178`
- **Group ID:** `dup-a403cae6e1ea`
- **Normalized label:** `mat foundation`
- **Risk level:** `high`
- **Priority band:** `P1`
- **Priority score:** 71
- **Recommended decision:** `NEEDS_HUMAN_REVIEW`
- **Merge safety:** `blocked_without_domain_review`

### Nodes (3)

| Node ID | Label | Type | Taxonomy Path | Edge Count | Resource Links |
|---------|-------|------|---------------|------------|----------------|
| VTN-DOM-0000263 | Mat Foundations | subtopic | STR.FND.MAT | 6 | 0 |
| VTN-DOM-0003016 | Mat Foundations | subtopic | GEO.FOE.MAF | 6 | 0 |
| VTN-DOM-0012278 | Mat Foundation | concept | ARC.BLD.STR.MTF | 3 | 0 |

### Edge Neighborhood

Total edges: 15
- `HAS_CHILD`: 13 (taxonomy hierarchy edges)
- `HAS_FACET`: 1 (`VTN-DOM-0012273--has_facet--VTN-DOM-0012278` — Foundation System has facet Mat Foundation)
- `MAPS_TO_EXTERNAL_STANDARD`: 1 (`VTN-DOM-0012278--maps_to_external_standard--VTN-DOM-0012198`)

### Risk Factors

1. **Different node types:** subtopic (×2) vs concept (×1)
2. **Different taxonomy contexts:** STR (Structural), GEO (Geotechnical), ARC (Architecture)
3. **Different taxonomy depths:** STR/GEO at 3 levels, ARC at 4 levels
4. **Three-way collision:** More complex than pairwise cross-domain alignment
5. **No Resource Layer links:** No external grounding for any node
6. **Existing HAS_FACET edge:** Foundation System already has Mat Foundation as a facet, indicating it's already part of a broader structural taxonomy

### Analysis

This is a classic cross-domain collision with three discipline-scoped views:
- **STR Mat Foundations:** Structural engineering perspective (subtopic under Foundations)
- **GEO Mat Foundations:** Geotechnical engineering perspective (subtopic under Foundations)
- **ARC Mat Foundation:** Architectural/building perspective (concept under Building > Structural)

The STR and GEO nodes are parallel subtopics at the same taxonomy level, similar to the Deep Foundations / Shallow Foundations case that was resolved with reciprocal `CROSS_DOMAIN_ALIGNMENT`. However, the ARC node is at a different granularity (concept vs subtopic) and sits under a different path (`ARC.BLD.STR.MTF`).

The existing `HAS_FACET` edge from Foundation System to the ARC Mat Foundation suggests the ARC node is already integrated into the structural taxonomy as a facet, not as a standalone concept. This complicates any simple cross-domain alignment.

### Downgrade Assessment

**Can this be downgraded to medium risk?**

Partially, with conditions:
1. A **pairwise `CROSS_DOMAIN_ALIGNMENT`** between STR (`VTN-DOM-0000263`) and GEO (`VTN-DOM-0003016`) could be considered in a future wave, since they are same-level subtopics in different disciplines — analogous to the approved Deep Foundations alignment.
2. The ARC node (`VTN-DOM-0012278`) should **remain separate or be aligned only as a narrower-related concept**, because:
   - It is a "concept" not a "subtopic"
   - It already has a `HAS_FACET` relationship to Foundation System
   - Its taxonomy depth differs from the other two
3. Any alignment would require:
   - Confirmation that STR and GEO nodes represent discipline-scoped views of the same object family
   - Explicit rejection of equivalence/merge/alias
   - No code, standard, numerical, or AHJ claim
   - Resource Layer review if external standards are involved (the `MAPS_TO_EXTERNAL_STANDARD` edge on the ARC node)

### Current Decision

**Remain blocked** in this closure loop.

**Reason:** Three-way cross-domain collision with mixed taxonomy depths and an existing HAS_FACET integration. A safe non-destructive admission would require splitting this into at least two separate decisions (STR-GEO alignment + ARC handling), which is beyond the scope of Wave 3 closure.

### Future Action

- Queue STR-GEO Mat Foundations as a candidate for Wave 4 cross-domain alignment review
- Inspect the `MAPS_TO_EXTERNAL_STANDARD` target (`VTN-DOM-0012198`) for source-rights risk before any ARC-adjacent admission
- Do not merge, alias, redirect, or tombstone any of these three nodes

## Other High-Risk Packets (Status Unchanged)

| Packet | Label | Status |
|--------|-------|--------|
| p1-decision-packet-3946860e327a | Load Path | Blocked — high risk, different taxonomy contexts |
| p1-decision-packet-0cfa6a7f88a1 | Wall Finishes | Blocked — high risk, 3 nodes, different types |
| p1-decision-packet-9d2ac282265b | Shear Wall | Blocked — reviewed Wave 2, remains blocked |
| p1-decision-packet-12e81a4fbcde | Retaining Wall | Blocked — high risk, 2 nodes, different contexts |

## Conclusion

No high-risk packet was admitted in this closure loop. Mat Foundation was inspected in depth and remains blocked with documented downgrade conditions for future waves.
