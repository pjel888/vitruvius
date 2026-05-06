# Phase 8H Accepted Link Graph Potential Sweep

**Date:** 2026-05-06

## Method

Inputs inspected:

- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/node-resource-links.json`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json`
- `006_System-Manifests/graph-canonical/admitted-relationships.json`
- Phase 8F and Phase 8G reports.

No external source check was performed for this sweep. No protected content was downloaded or stored.

Two read-only explorer lanes were also used:

- `Carson`: structural/load-path accepted links.
- `Plato`: digital/classification/life-safety/accessibility accepted links.

## Accepted Links Inspected

| Link | Resource | Target Node | Relation | Evidence State | Recommendation |
|---|---|---|---|---|---|
| `nrl-accessible-route-usab-ch4` | `res-us-access-board-accessible-routes-ch4` | `VTN-DOM-0004630` / Accessible Route Continuity | `provides_design_guidance` | `link_verified`, public government guidance metadata only | `visual_only_candidate` / no graph edge |
| `nrl-load-path-wbdg-wind` | `res-wbdg-wind-safety-building-envelope` | `VTN-DOM-0012160` / Load Path | `provides_design_guidance` | `link_verified`, public WBDG/NIBS guidance metadata only | `visual_only_candidate` / no new graph edge |
| `nrl-wind-load-wbdg-wind` | `res-wbdg-wind-safety-building-envelope` | `VTN-DOM-0012777` / Structural Wind Load | `provides_design_guidance` | `link_verified`, public WBDG/NIBS guidance metadata only | `visual_only_candidate` / no new graph edge |
| `nrl-seismic-load-wbdg-seismic` | `res-wbdg-seismic-design-principles` | `VTN-DOM-0012778` / Structural Seismic Load | `explains` | `link_verified`, public WBDG/NIBS guidance metadata only | `resource_layer_only` |
| `nrl-load-path-ice` | `res-ice-structural-load-paths` | `VTN-DOM-0012160` / Load Path | `explains` | `link_verified`, public professional guidance metadata only | `resource_layer_only` |
| `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7` | `res_9c586758-66e4-46f2-b62a-8720db1c0976` | `VTN-DOM-0000092` / BIM Schemas | `explains` | `link_verified`, `source_custody_metadata_checked`, metadata-only caveat | `visual_only_candidate` / no new graph edge |
| `nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485` | `res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40` | `VTN-DOM-0000056` / Fire Protection | `provides_design_guidance` | `link_verified`, `source_custody_metadata_checked`, contextual guidance caveat | `resource_layer_only` |
| `nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477` | `res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c` | `VTN-DOM-0000093` / Classification Systems | `provides_classification` | `link_verified`, `source_custody_metadata_checked`, no adoption claim | `resource_layer_only` |

## Link-by-Link Findings

### Accessible Route Continuity

- Current graph neighborhood: `Barrier Free Routes broader_than Accessible Route Continuity`.
- Resource evidence: U.S. Access Board Chapter 4 guidance, metadata/rationale only.
- Duplicate/overclaim risk: high. The graph has multiple accessible-route labels across architecture/accessibility/law contexts.
- Unsafe graph claims: compliance, governing applicability, AHJ adoption, or general accessible-route requirements.
- Safe boundary: visual disambiguation and caveat display only.

### Load Path / WBDG Wind

- Current graph neighborhood includes base `Load Path requires Tributary Area/Beam/Slab/Column/Foundation System`, curriculum/source-family mappings, and admitted `Structural Wind Load INFORMS Load Path`.
- Resource evidence: WBDG wind-safety contextual guidance.
- Duplicate risk: high for re-admitting the Phase 8G exact edge.
- Unsafe graph claims: wind-code/current/governing/AHJ/numerical/design-adequacy claims.
- Safe boundary: visual display of the existing Phase 8G evidence-backed edge and caveats.

### Structural Wind Load / WBDG Wind

- Current graph neighborhood includes `Structural Wind Load requires Diaphragm Action`, `Structural Wind Load constrains Facade Anchor Interface`, admitted `Structural Wind Load CONSTRAINS Facade Assembly`, and admitted `Structural Wind Load INFORMS Load Path`.
- Resource evidence: same WBDG wind-safety Resource.
- Duplicate risk: high for the Phase 8G edge; medium for extra facade/load semantics.
- Safe boundary: no new graph edge.

### Structural Seismic Load / WBDG Seismic

- Current graph neighborhood includes `Lateral Loads broader_than Structural Seismic Load`, `Structural Seismic Load requires Diaphragm Action`, and criteria/AHJ-coordination constraints.
- Resource evidence: WBDG seismic design principles metadata.
- Candidate risk: the locally visible second endpoint is not specific enough without source-text interpretation. `REQUIRES`, `CONSTRAINS`, and code/numerical relationships would overclaim.
- Safe boundary: Resource Layer evidence only.

### Load Path / ICE

- Current graph neighborhood overlaps with WBDG load-path context and has unresolved duplicate-label risk around load path/load paths.
- Resource evidence: ICE structural load paths metadata.
- Candidate risk: no second endpoint is justified by local metadata alone; avoid definition expansion or duplicate/canonical action.
- Safe boundary: Resource Layer evidence only.

### BIM Schemas / buildingSMART IFC

- Current graph neighborhood includes parent `Digital Delivery And Information Management`, children `Model Authoring`, `Coordination`, `Level Of Information Need`, and Phase 8F admitted `BIM Schemas INFORMS IFC Exchange`.
- Resource evidence: official public IFC landing-page metadata only; no IFC schema payload.
- Duplicate risk: high for re-proposing `BIM Schemas INFORMS IFC Exchange`; one rolled-back wording-fix record and one active admitted record share the tuple.
- Safe boundary: visual/provenance surfacing of the existing Phase 8F edge only.

### Fire Protection / WBDG Fire Protection

- Current graph neighborhood includes parent `Fire And Life Safety`, children `Sprinklers`, `Standpipes`, `Fire Pumps`, and admitted `Fire Protection CONSTRAINS Egress` plus `Egress REQUIRES Fire Protection`.
- Resource evidence: WBDG public page metadata only; contextual guidance, not fire-code authority.
- Duplicate risk: medium for new egress/fire edges because active overlays already exist.
- Overclaim risk: high for code, compliance, AHJ, or governing fire-protection authority claims.
- Safe boundary: Resource Layer evidence only.

### Classification Systems / Uniclass

- Current graph neighborhood includes parent `Digital Delivery And Information Management` and children `Uniclass Mapping`, `OmniClass Mapping`, `MasterFormat Mapping`.
- Resource evidence: Uniclass/NBS public metadata only; no jurisdictional adoption or universal authority claim.
- Duplicate risk: high for new classification-to-Uniclass graph semantics because the taxonomy already models the child mapping.
- Safe boundary: Resource Layer evidence only.

## Sweep Conclusion

No new non-destructive graph edge is recommended from the accepted-link sweep. The only plausible relationship tuples are already admitted:

- Phase 8F: `BIM Schemas INFORMS IFC Exchange`
- Phase 8G: `Structural Wind Load INFORMS Load Path`

Safe Phase 8H action is to document exact blockers, verify existing Explorer evidence visibility, and attempt Resource Layer fallback rather than forcing additional graph mutation.
