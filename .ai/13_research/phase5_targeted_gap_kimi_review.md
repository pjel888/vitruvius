# Phase 5 Targeted Gap-Closure Kimi Review

Date: 2026-05-03T01:10:00+08:00
Reviewer: kimi-internal-critique

## Review Prompt

> Review this Phase 5 targeted gap-closure admission shortlist. The graph already has 257 admitted relationships. Do not optimize for count. Each candidate must close a documented reasoning-path gap, use the correct relation type, have correct directionality, avoid duplicate/base-overlay collisions, avoid source/code/AHJ/numerical overclaiming, and improve tests. Reject any candidate that is generic, redundant, weakly connected to the reasoning gap, or not clearly useful.

## Critique Results

### Candidate 1.1 — CONSTRAINS (Fire Protection → Egress)
- **Verdict: ADMIT**
- Relation type is correct: fire codes constrain egress design.
- Directionality is correct: regulatory domain → design domain.
- Rationale is specific (exit capacity, travel distance, door swing, smoke-proof enclosure).
- No numerical/code/AHJ claim; explicitly general domain-synthesis.
- Closes documented BFS gap from VTN-DOM-0000056 to VTN-DOM-0000058.
- Not redundant with any existing edge.

### Candidate 1.2 — COORDINATES_WITH (Fire Protection → Egress)
- **Verdict: DEFER**
- Valid relation, but redundant with 1.1 for the tested reasoning path.
- The BFS test uses allowedTypes including both CONSTRAINS and COORDINATES_WITH.
- Since CONSTRAINS already closes the path, COORDINATES_WITH adds count without adding traversal value.
- Defer to future wave if independent coordination semantics are needed.

### Candidate 1.3 — REQUIRES (Egress → Fire Protection)
- **Verdict: ADMIT**
- Semantically distinct from 1.1.
- Captures dependency direction: egress design requires fire protection for safe evacuation.
- Underrepresented family (REQUIRES has only 2 edges); this adds diversity.
- Closes reverse reasoning path.

### Candidate 1.4 — COORDINATES_WITH (Egress → Fire Protection)
- **Verdict: DEFER**
- Redundant with 1.3 for reverse path closure.
- REQUIRES is stronger semantically for the dependency direction.

### Candidate 2.1 — AFFECTS (Mechanical Systems → Thermal Comfort)
- **Verdict: ADMIT**
- Strongest possible relation for this gap.
- HVAC systems directly affect thermal comfort through heating, cooling, ventilation, humidity.
- Underrepresented family (AFFECTS has only 6 edges).
- Closes documented BFS gap from VTN-DOM-0000004 to VTN-DOM-0002510.

### Candidate 2.2 — COORDINATES_WITH (Thermal Comfort → Mechanical Systems)
- **Verdict: ADMIT**
- Reverse coordination path is valuable: thermal comfort objectives drive mechanical design.
- Not redundant with 2.1 because directionality is reversed.
- Provides bidirectional traversal for Explorer neighborhood queries.

### Candidate 3.1 — INFORMS (Structural Engineering → Materials)
- **Verdict: ADMIT**
- Strong relation: structural analysis informs material selection.
- Underrepresented family (INFORMS has only 5 edges).
- Closes documented BFS gap from VTN-DOM-0000029 to VTN-DOM-0002477.

### Candidate 3.2 — COORDINATES_WITH (Structural Engineering → Materials)
- **Verdict: DEFER**
- Redundant with 3.1 for forward path closure.
- INFORMS is more specific and semantically richer for this domain pair.

### Candidate 4.1 — DRAINS_TO (Drainage → Stormwater Networks)
- **Verdict: ADMIT**
- Underrepresented family (DRAINS_TO has only 1 edge).
- Closes specific discharge path for stormwater.
- Directionality is correct: building drainage → municipal stormwater infrastructure.

### Candidate 4.2 — DISCHARGES_TO (Drainage → Sewerage Networks)
- **Verdict: ADMIT**
- Closes specific discharge path for wastewater/sanitary flows.
- Complements 4.1 by covering the sewerage discharge path.
- Directionality is correct: building drainage → sewerage infrastructure.

## Final Shortlist

| # | Edge | Gap Closed |
|---|------|------------|
| 1 | CONSTRAINS Fire Protection → Egress | Fire Protection → Egress (forward) |
| 2 | REQUIRES Egress → Fire Protection | Egress → Fire Protection (reverse) |
| 3 | AFFECTS Mechanical Systems → Thermal Comfort | Mechanical Systems → Thermal Comfort (forward) |
| 4 | COORDINATES_WITH Thermal Comfort → Mechanical Systems | Thermal Comfort → Mechanical Systems (reverse) |
| 5 | INFORMS Structural Engineering → Materials | Structural Engineering → Materials (forward) |
| 6 | DRAINS_TO Drainage → Stormwater Networks | Drainage → Stormwater (outgoing) |
| 7 | DISCHARGES_TO Drainage → Sewerage Networks | Drainage → Sewerage (outgoing) |

**Admit: 7 edges. Defer: 3 edges. Reject: 0 edges.**

## Risk Assessment

- No merge/alias/redirect/tombstone risk: all are non-destructive edge admissions.
- No Resource Layer mutation: all edges use existing nodes.
- No fake source/code/AHJ/numerical claim: all rationales are general domain-synthesis.
- No high-risk P1 adjacency: none of the nodes are in the 5 blocked high-risk packets.
- No CROSS_DOMAIN_EQUIVALENT: not used.
- No generic related_to: not used.

## Conclusion

The 7-edge shortlist is approved for admission. All edges are high-quality, non-redundant for their primary reasoning-path gap, and improve the effective graph traversal. The 3 deferred edges are valid but add no new traversal capability beyond the admitted edges.
