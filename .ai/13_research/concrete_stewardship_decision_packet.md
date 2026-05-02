# Concrete Stewardship Decision Packet

Date: 2026-05-01

## Status

No destructive merge, alias, redirect, tombstone, production edge admission, or fake steward approval was applied. Both known P0 concrete-related groups remain unresolved because the decisions recorded in this loop are proposed-only review artifacts.

## Group A: concrete

- Group ID: `dup-0aa1351d9475`
- Nodes:
  - `VTN-DOM-0000068` - Concrete, type `topic`, taxonomy `MAT > MAT.CON`, neighborhood `5 nodes / 4 edges`, Resource Layer links `0`.
  - `VTN-DOM-0000267` - Concrete, type `subtopic`, taxonomy `STR > STR.MAT > STR.MAT.CON`, neighborhood `7 nodes / 6 edges`, Resource Layer links `0`.
- Risk: high.
- Priority: P0.
- Decision record: `canonical-20260501155958-e011dc288980`.
- Decision type/status: `DISAMBIGUATED_KEEP_SEPARATE`, `proposed`.
- Recommendation: keep separate pending steward review; structural concrete context should be displayed as a specialization/contextual view of broad material concrete rather than merged.
- Proposed-only relationship: `VTN-DOM-0000267 RELATED_SPECIALIZATION_OF VTN-DOM-0000068`.
- Search disambiguation: show `Concrete (MAT > MAT.CON)` and `Concrete (STR > STR.MAT > STR.MAT.CON)` with P0 pending-review metadata.
- Rationale: MAT.CON is a broad materials topic; STR.MAT.CON is a structural-material context. Merging would conflate material and structural taxonomies.

## Group B: reinforced concrete

- Group ID: `dup-3751564358d7`
- Nodes:
  - `VTN-DOM-0000271` - Reinforced Concrete, type `subtopic`, taxonomy `STR > STR.CON > STR.CON.RCO`, neighborhood `8 nodes / 7 edges`, Resource Layer links `0`.
  - `VTN-DOM-0012147` - Reinforced Concrete, type `concept`, taxonomy `ARC > ARC.MAT > ARC.MAT.CON > ARC.MAT.CON.RCC`, neighborhood `32 nodes / 33 edges`, Resource Layer links `0`.
- Risk: high.
- Priority: P0.
- Decision record: `canonical-20260501155958-f8da3711275f`.
- Decision type/status: `CROSS_DOMAIN_EQUIVALENCE`, `proposed`.
- Recommendation: keep separate pending steward review; treat as cross-domain aligned concepts, not a destructive merge.
- Proposed-only relationships: bidirectional `CROSS_DOMAIN_EQUIVALENT`, documented as alignment rather than identity.
- Search disambiguation: show `Reinforced Concrete (STR > STR.CON > STR.CON.RCO)` and `Reinforced Concrete (ARC > ARC.MAT > ARC.MAT.CON > ARC.MAT.CON.RCC)` with P0 pending-review metadata.
- Rationale: STR.CON.RCO is structural-systems context with child topics; ARC.MAT.CON.RCC is architecture-material concept with a dense semantic neighborhood. Merging would collapse discipline boundaries.

## Kimi critique summary

Accepted:
- Concrete is taxonomy-context disambiguation, not a safe merge.
- Reinforced concrete is cross-domain alignment, not a safe merge.
- Proposed relationships must remain proposed-only until human steward approval.
- Search/UI should explain ambiguity without claiming canonical approval.

Rejected/deferred:
- Destructive merge, alias, redirect, and tombstone actions were rejected for this loop.
- `CROSS_DOMAIN_EQUIVALENT` naming is deferred for vocabulary review before any production edge admission.

## Required before future mutation

- Explicit steward approval through the canonical review workflow.
- Dry-run preview with no edge/resource loss.
- Passing graph, Resource Layer, and canonical validation.
- Hash-chained transaction manifest.
- Rollback/remediation plan.
- Kimi/domain review of exact relation vocabulary and direction.
