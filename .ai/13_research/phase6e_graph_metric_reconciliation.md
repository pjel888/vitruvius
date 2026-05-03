# Phase 6E Graph Edge Metric Reconciliation

**Generated:** 2026-05-03T01:00:00+08:00
**Commit:** e9d4e281

---

## Issue

A previous summary incorrectly stated:
> "Current Effective Edge Count: 13,670 (shadow graph)"

This conflated two distinct metrics:
1. **Base graph edge count** (shadow/backbone graph without admitted overlays)
2. **Effective edge count** (base graph + admitted relationship overlays)

---

## Verified Metrics (from `validateGraphRelationships.ts --no-write`)

| Metric | Value | Definition |
|--------|-------|------------|
| `nodeCount` | 10,018 | Total nodes in shadow graph |
| `baseEdgeCount` | 13,670 | Base hierarchy + semantic edges without admitted overlays |
| `admittedRelationshipEdgeCount` | 264 | Admitted relationship edges |
| `edgeCount` | **13,934** | **Effective edges = baseEdgeCount + admittedRelationshipEdgeCount** |
| `hierarchyEdgeCount` | 9,994 | Hierarchy edges (broader_than / narrower_than) |
| `semanticEdgeCount` | 3,940 | Semantic edges (COORDINATES_WITH, etc.) |

---

## Reconciliation

- **13,670** = `baseEdgeCount` = base-only shadow graph edges
- **13,934** = `edgeCount` = effective edges with admitted overlays
- The difference (264) equals the admitted relationship count

### Naming Convention Going Forward

| Old ambiguous phrasing | Correct phrasing |
|------------------------|------------------|
| "effective edge count: 13,670" | "base edge count: 13,670" |
| "shadow graph edges: 13,670" | "baseEdgeCount: 13,670" |
| "effective edges" (when meaning 13,934) | "effectiveEdgeCount: 13,934" |
| "effective edges with admitted overlays" | "effectiveEdgeCount: 13,934" |

---

## Files Already Correct

The following files already correctly distinguish the metrics:
- `.ai/13_research/continuous_vitruvius_loop_state.json` — has both `baselineEffectiveEdges: 13934` and `baseEdges: 13670`
- `.ai/13_research/continuous_vitruvius_quality_report.md` — states "Baseline effective edges: 13,934" and "Base graph edges: 13,670"

The error was in a transient summary, not in committed reports.

---

## Conclusion

✅ **Metric reconciled.** 13,670 is base-only. 13,934 is effective with overlays. No graph data was mutated.
