# Phase 4 Wave 3 Relation Vocabulary Closure Report

Date: 2026-05-03T01:00:00Z

## Relation Type Governance Status

### Types Used in Wave 3 Admissions (22 edges)

| Type | Count | In `CanonicalStewardshipRelationType` | In `STEWARDSHIP_RELATIONSHIP_TYPES` | In `ADMITTED_RELATIONSHIP_TYPES` | Explorer UI Color | Explorer Filter | Explorer HiddenEdgeTypes |
|------|-------|--------------------------------------|-------------------------------------|----------------------------------|-------------------|-----------------|--------------------------|
| COORDINATES_WITH | 5 | Yes | Yes | Yes | Yes | Yes | Yes |
| AFFECTS | 3 | Yes | Yes | Yes | Yes | Yes | Yes |
| SUPPORTS | 3 | Yes | Yes | Yes | Yes | Yes | Yes |
| COLLECTS | 2 | Yes | Yes | Yes | Yes | Yes | Yes |
| INFORMS | 2 | Yes | Yes | Yes | Yes | Yes | Yes |
| RESISTS | 2 | Yes | Yes | Yes | Yes | Yes | Yes |
| CONSTRAINS | 1 | Yes | Yes | Yes | Yes | Yes | Yes |
| CONVEYS | 1 | Yes | Yes | Yes | Yes | Yes | Yes |
| DRAINS_TO | 1 | Yes | Yes | Yes | Yes | Yes | Yes |
| MITIGATES | 1 | Yes | Yes | Yes | Yes | Yes | Yes |
| TRANSFERS_LOAD_TO | 1 | Yes | Yes | Yes | Yes | Yes | Yes |

### Types Added to Vocabulary but Not Used in Wave 3

| Type | Status |
|------|--------|
| CONNECTS_TO | Added to all governance sets and Explorer UI; reserved for future wave |

### Types Explicitly Blocked

| Type | Blocker |
|------|---------|
| CROSS_DOMAIN_EQUIVALENT | Active admission blocked; normalized to CROSS_DOMAIN_ALIGNMENT at approval gate |

## Governance Verification

- [x] All Wave 3 used types are present in `CanonicalStewardshipRelationType` union
- [x] All Wave 3 used types are in `STEWARDSHIP_RELATIONSHIP_TYPES` (proposable set)
- [x] All Wave 3 used types are in `ADMITTED_RELATIONSHIP_TYPES` (admissible set)
- [x] Explorer `EDGE_COLORS` includes all new types
- [x] Explorer `EDGE_TYPES` filter list includes all new types
- [x] Explorer `useSceneStore.hiddenEdgeTypes` includes all new types
- [x] No CROSS_DOMAIN_EQUIVALENT active admitted edge exists
- [x] Graph validation confirms all admitted edges use valid types
- [x] Dynamic edge-filter reconciliation absorbs new types without manual hardcoding

## Semantic Appropriateness

All 22 Wave 3 edges use relation types semantically appropriate for their endpoints:
- `COLLECTS` / `DRAINS_TO` / `CONVEYS`: drainage/stormwater flow topology
- `MITIGATES`: stormwater management relationship
- `INFORMS`: knowledge-to-design relationships
- `AFFECTS`: geotechnical/performance influence relationships
- `SUPPORTS`: structural support topology (distinct from load transfer)
- `RESISTS`: structural-system-to-load relationships
- `CONSTRAINS`: geotechnical boundary relationships
- `COORDINATES_WITH`: interdisciplinary coordination interfaces
- `TRANSFERS_LOAD_TO`: structural load-path topology

## Conclusion

Relation vocabulary governance is complete for Wave 3. No unsafe admitted edges, no missing governance support, no blocked type was admitted.
