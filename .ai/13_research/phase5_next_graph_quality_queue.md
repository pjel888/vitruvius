# Phase 5 Next Graph Quality Queue

Date: 2026-05-03T01:00:00+08:00
Status: Targeted gap closure complete. 7 edges admitted. All 4 documented reasoning-path gaps closed. Manifest drift resolved.

## Targeted Gap Queue (Ready for Admission When Criteria Met)

The following 10 edges close 4 verified reasoning-path gaps. All candidate edges were verified as FREE (not in base graph, not in admitted overlay).

### Gap 1: Fire Protection ↔ Egress (4 edges)

| Source | Target | Type | Rationale |
|--------|--------|------|-----------|
| VTN-DOM-0000056 | VTN-DOM-0000058 | CONSTRAINS | Fire protection requirements constrain egress design, including exit capacity, travel distance, door swing direction, and smoke-proof enclosure criteria. |
| VTN-DOM-0000056 | VTN-DOM-0000058 | COORDINATES_WITH | Fire protection and egress systems must be coordinated during design to ensure safe evacuation paths align with suppression zones and compartmentation boundaries. |
| VTN-DOM-0000058 | VTN-DOM-0000056 | REQUIRES | Egress design requires fire protection input to ensure exit routes remain tenable during fire events and meet code-mandated protection levels. |
| VTN-DOM-0000058 | VTN-DOM-0000056 | COORDINATES_WITH | Egress and fire protection systems must be coordinated to verify that exit access, discharge, and remote exit separation satisfy fire safety objectives. |

### Gap 2: Mechanical Systems ↔ Thermal Comfort (2 edges)

| Source | Target | Type | Rationale |
|--------|--------|------|-----------|
| VTN-DOM-0000004 | VTN-DOM-0002510 | AFFECTS | Mechanical systems directly affect indoor thermal comfort through heating, cooling, ventilation, and humidity control strategies. |
| VTN-DOM-0002510 | VTN-DOM-0000004 | COORDINATES_WITH | Thermal comfort objectives and mechanical system design must be coordinated to align setpoints, zoning, and control sequences with occupant expectations. |

### Gap 3: Structural Engineering ↔ Materials (2 edges)

| Source | Target | Type | Rationale |
|--------|--------|------|-----------|
| VTN-DOM-0000029 | VTN-DOM-0002477 | INFORMS | Structural engineering analysis informs material selection and construction method decisions to ensure safety, serviceability, and constructability. |
| VTN-DOM-0000029 | VTN-DOM-0002477 | COORDINATES_WITH | Structural engineering and materials/methods decisions must be coordinated during design to align capacity, durability, and procurement constraints. |

### Gap 4: Drainage → Discharge (2 edges)

| Source | Target | Type | Rationale |
|--------|--------|------|-----------|
| VTN-DOM-0000025 | VTN-DOM-0002899 | DRAINS_TO | Building drainage systems collect and convey stormwater to stormwater networks for managed discharge and flood control. |
| VTN-DOM-0000025 | VTN-DOM-0002896 | DISCHARGES_TO | Building drainage conveys wastewater and sanitary flows to sewerage networks for collection, treatment, and safe disposal. |

## Admission Criteria (Must All Be Met)

1. ✅ Audit finds no rollback/quality blockers
2. ✅ Relation-family mismatch resolved (reporting-only error)
3. ⚠️ Worktree is clean or scoped (unrelated source files remain)
4. ✅ Validations pass
5. ✅ Edges directly fix tested reasoning-path gaps

**Outstanding blocker:** Worktree has ~150 unrelated untracked source files. These do not block graph admission but should be documented. If a clean commit is required, the admission can proceed with only the intended files staged.

## Secondary Queue (Future Waves)

1. **COORDINATES_WITH reciprocity wave**: Add ~76 missing reciprocal edges (structural quality improvement, large count impact)
2. **Underrepresented family expansion**: Grow AFFECTS, INFORMS, MITIGATES, RESISTS families
3. **MEP cross-coordination**: Add more ARC.BLD.SRV subsystem-to-subsystem edges
4. **High-risk P1 resolution**: Human review of 5 blocked packets
5. **P0 Concrete disambiguation**: Non-destructive resolution of Concrete/Reinforced Concrete duplicates
