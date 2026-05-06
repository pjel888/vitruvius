# Phase 8F Accepted Link Neighborhood Inspection

**Date:** 2026-05-06

## Scope

Inspected the three Phase 8E accepted Resource Layer links and their target graph neighborhoods:

1. buildingSMART IFC -> BIM Schemas
2. WBDG Fire Protection -> Fire Protection
3. Uniclass -> Classification Systems

## Link And Node Findings

### buildingSMART IFC -> BIM Schemas

- Resource: `res_9c586758-66e4-46f2-b62a-8720db1c0976`
- Title: `Industry Foundation Classes (IFC) - buildingSMART International`
- URL: `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/`
- Source family: `buildingsmart`
- `verificationStatus`: `link_verified`
- `custodyStatus`: `source_custody_metadata_checked`
- `lastCheckedAt`: `2026-05-06T11:39:36.106Z`
- Caveat: public locator/page-title metadata only; no schema completeness, edition/version, current/governing, compliance, AHJ, or source-truth claim.
- Link: `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7`
- Target node: `VTN-DOM-0000092` / `BIM Schemas` / `DIG.BIM`
- Link relation: `explains`
- Link status: `accepted`
- Learner eligible: `false`

Neighborhood:

- Base incoming: `VTN-DOM-0000091 broader_than VTN-DOM-0000092`
- Base outgoing: `BIM Schemas broader_than Model Authoring`, `Coordination`, `Level Of Information Need`
- Admitted overlay edges touching BIM Schemas: 0
- Related existing IFC node found: `VTN-DOM-0000646` / `IFC Exchange` / `DIG.EXC.IFC`
- Existing `IFC Exchange` base neighborhood includes `Model Exchange broader_than IFC Exchange`, five IFC Exchange child nodes, and `IFC Exchange requires Maintainable Asset Record`.

Candidate implication:

- A narrow `BIM Schemas INFORMS IFC Exchange` proposal is plausible because the accepted Resource Layer link connects official IFC public metadata to BIM Schemas and an existing IFC Exchange node already exists.
- This must remain non-destructive, metadata-caveated, and not a schema completeness/current/governing/compliance claim.

### WBDG Fire Protection -> Fire Protection

- Resource: `res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40`
- Title: `Fire Protection | WBDG - Whole Building Design Guide`
- URL: `https://www.wbdg.org/do/secure/fire-protection`
- Source family: `wbdg_nibs`
- `verificationStatus`: `link_verified`
- `custodyStatus`: `source_custody_metadata_checked`
- `lastCheckedAt`: `2026-05-06T11:39:36.106Z`
- Caveat: official public locator/page-title metadata only; not fire-code authority, compliance, governing, or source truth.
- Link: `nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485`
- Target node: `VTN-DOM-0000056` / `Fire Protection` / `FLS.FPR`
- Link relation: `provides_design_guidance`
- Link status: `accepted`
- Learner eligible: `false`

Neighborhood:

- Base incoming: `VTN-DOM-0000055 broader_than VTN-DOM-0000056`, `Wind Restraint Coordination constrains Fire Protection`
- Base outgoing: `Fire Protection broader_than Sprinklers`, `Standpipes`, `Fire Pumps`
- Admitted overlay edges touching Fire Protection in current active overlay query: 0

Candidate implication:

- The accepted Resource Layer link is valuable evidence visibility for the Fire Protection node.
- No graph edge is proposed from this evidence alone because public page-title metadata does not support a specific new non-hierarchical relationship without importing fire-code/compliance or content-level claims.

### Uniclass -> Classification Systems

- Resource: `res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c`
- Title: `Uniclass, delivered by NBS`
- URL: `https://uniclass.thenbs.com/`
- Source family: `uniclass_nbs`
- `verificationStatus`: `link_verified`
- `custodyStatus`: `source_custody_metadata_checked`
- `lastCheckedAt`: `2026-05-06T11:39:36.106Z`
- Caveat: official public locator/page-title metadata only; no jurisdictional adoption or universal classification authority claim.
- Link: `nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477`
- Target node: `VTN-DOM-0000093` / `Classification Systems` / `DIG.CLS`
- Link relation: `provides_classification`
- Link status: `accepted`
- Learner eligible: `false`

Neighborhood:

- Base incoming: `VTN-DOM-0000091 broader_than VTN-DOM-0000093`
- Base outgoing: `Classification Systems broader_than Uniclass Mapping`, `OmniClass Mapping`, `MasterFormat Mapping`
- Admitted overlay edges touching Classification Systems: 0

Candidate implication:

- The existing hierarchy already expresses that `Uniclass Mapping` is under `Classification Systems`.
- No new graph edge is proposed because it would duplicate existing taxonomy or overclaim Uniclass authority/adoption from metadata-only evidence.

## Duplicate / Overclaim Risk Summary

| Area | Safe candidate? | Reason |
|---|---:|---|
| BIM Schemas / IFC Exchange | Yes, one narrow edge candidate | Existing `IFC Exchange` node plus accepted buildingSMART IFC Resource Layer evidence; no existing exact edge. |
| Fire Protection | No edge candidate | Existing hierarchy covers direct subtopics; public metadata alone cannot justify new mechanism/compliance relationships. |
| Classification Systems | No edge candidate | Existing hierarchy already covers Uniclass Mapping; new relation would be redundant or too broad. |
