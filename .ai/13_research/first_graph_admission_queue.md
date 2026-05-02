# First Graph Admission Queue

Date: 2026-05-02T05:00:53Z

This is an advisory queue, not an approval file. No item below is approved for graph mutation, merge, alias, redirect, tombstone, or admitted production relationship. Every future action still requires the appropriate steward approval, dry-run preview, transaction manifest, rollback plan, and validation gate.

## Summary

- Reviewed packets in this session: 8
- Reviewer type Kimi records: 8
- Status breakdown: Kimi reviewed 3, human review needed 5, human reviewed 0, rejected 0, deferred 0
- Graph mutations performed: 0
- Approvals/admitted relationships/aliases/redirects/tombstones created: 0 / 0 / 0 / 0 / 0
- Resource Layer mutations performed: 0

## Ready for future non-destructive admission review

### building - p1-decision-packet-fee6fbd9a0fc

- Packet ID: `p1-decision-packet-fee6fbd9a0fc`
- Group ID: `dup-ca1078594013`
- Node IDs: VTN-DOM-0000716, VTN-DOM-0000757
- Labels: Buildings, Buildings
- Current review status: `kimi_reviewed`
- Recommended future action: `governed_disambiguation_candidate`
- Why suitable or not suitable: Kimi classifies this as governed disambiguation: the HIS precedent-study bucket and FIG works/projects bucket share a surface label but have different taxonomy roles and edge neighborhoods.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: DISAMBIGUATED_FROM / governed disambiguation text; exact direction and labels require steward review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts; high combined edge count
- Next exact action: Review child lists for label clarification only; keep consolidation out of scope.

### shallow foundation - p1-decision-packet-d5a20759fdfd

- Packet ID: `p1-decision-packet-d5a20759fdfd`
- Group ID: `dup-6400e3e0c204`
- Node IDs: VTN-DOM-0000261, VTN-DOM-0003010
- Labels: Shallow Foundations, Shallow Foundations
- Current review status: `kimi_reviewed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate: STR and GEO shallow-foundation nodes likely represent the same engineering object from separate disciplinary views, with different taxonomy contexts and no resource links.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts
- Next exact action: Compare children and edge neighborhoods; draft alignment language only.

### deep foundation - p1-decision-packet-8a66e785d02a

- Packet ID: `p1-decision-packet-8a66e785d02a`
- Group ID: `dup-5c6457d515c1`
- Node IDs: VTN-DOM-0000262, VTN-DOM-0003013
- Labels: Deep Foundations, Deep Foundations
- Current review status: `kimi_reviewed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate: STR and GEO Deep Foundations nodes likely describe the same class through discipline-specific taxonomies, with low mutation pressure and no resource links.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts
- Next exact action: Compare children; if parallel, queue non-identity alignment proposal.

## Needs human review

### mat foundation - p1-decision-packet-fa4918982178

- Packet ID: `p1-decision-packet-fa4918982178`
- Group ID: `dup-a403cae6e1ea`
- Node IDs: VTN-DOM-0000263, VTN-DOM-0003016, VTN-DOM-0012278
- Labels: Mat Foundations, Mat Foundations, Mat Foundation
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment with high directionality risk: mat or raft foundation spans STR, GEO, and ARC contexts, but the three-node alignment, type mismatch, and standard edge require careful review.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect HAS_FACET and MAPS_TO_EXTERNAL_STANDARD edges; propose non-identity alignment only if safe.

### shear wall - p1-decision-packet-9d2ac282265b

- Packet ID: `p1-decision-packet-9d2ac282265b`
- Group ID: `dup-db832ee203d2`
- Node IDs: VTN-DOM-0000265, VTN-DOM-0012270
- Labels: Shear Walls, Shear Wall
- Current review status: `human_review_needed`
- Recommended future action: `related_specialization_candidate`
- Why suitable or not suitable: Kimi classifies this as related specialization candidate requiring human directionality review: STR seismic Shear Walls may be a design-topic specialization of ARC Shear Wall as building element, but directionality is risky because STR context is seismic-specific.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: RELATED_SPECIALIZATION_OF from narrower structural/seismic topic toward broader building element if human reviewer confirms scope
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Human reviewer should verify whether STR node is seismic-design specialization, not duplicate.

### retaining wall - p1-decision-packet-12e81a4fbcde

- Packet ID: `p1-decision-packet-12e81a4fbcde`
- Group ID: `dup-b2f8807aa183`
- Node IDs: VTN-DOM-0003026, VTN-DOM-0012272
- Labels: Retaining Walls, Retaining Wall
- Current review status: `human_review_needed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate requiring human and source review: GEO retaining-wall system and ARC building-structural concept are semantically close but discipline-scoped, and the external-standard edge creates directionality and source risk.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect MAPS_TO_EXTERNAL_STANDARD target and child nodes; draft alignment only if scope matches.

### wall finishe - p1-decision-packet-0cfa6a7f88a1

- Packet ID: `p1-decision-packet-0cfa6a7f88a1`
- Group ID: `dup-79f6cd2af6bf`
- Node IDs: VTN-DOM-0000513, VTN-DOM-0003441, VTN-DOM-0012156
- Labels: Wall Finishes, Wall Finishes, Wall Finishes
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as high-risk edge-neighborhood review needed: three Wall Finishes nodes span material finish/product and ARC concept contexts, and duplicate status is unclear from type and taxonomy differences.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Review MAT.FIN versus MAT.FIP distinction before any relation proposal.

### load path - p1-decision-packet-3946860e327a

- Packet ID: `p1-decision-packet-3946860e327a`
- Group ID: `dup-621135f7b4b9`
- Node IDs: VTN-DOM-0002932, VTN-DOM-0012160
- Labels: Load Paths, Load Path
- Current review status: `human_review_needed`
- Recommended future action: `needs_human_review`
- Why suitable or not suitable: Kimi classifies this as high-risk human review needed: STR subtopic and ARC concept overlap semantically, but node type, taxonomy context, REQUIRES edges, external-standard mappings, and two resource links make mutation unsafe.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Possible cross-domain alignment only after human/source/resource review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts; resource links must be preserved
- Next exact action: Route to human structural and architectural reviewer with resource-link preservation check.

## Keep separate candidates

### building - p1-decision-packet-fee6fbd9a0fc

- Packet ID: `p1-decision-packet-fee6fbd9a0fc`
- Group ID: `dup-ca1078594013`
- Node IDs: VTN-DOM-0000716, VTN-DOM-0000757
- Labels: Buildings, Buildings
- Current review status: `kimi_reviewed`
- Recommended future action: `governed_disambiguation_candidate`
- Why suitable or not suitable: Kimi classifies this as governed disambiguation: the HIS precedent-study bucket and FIG works/projects bucket share a surface label but have different taxonomy roles and edge neighborhoods.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: DISAMBIGUATED_FROM / governed disambiguation text; exact direction and labels require steward review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts; high combined edge count
- Next exact action: Review child lists for label clarification only; keep consolidation out of scope.

### mat foundation - p1-decision-packet-fa4918982178

- Packet ID: `p1-decision-packet-fa4918982178`
- Group ID: `dup-a403cae6e1ea`
- Node IDs: VTN-DOM-0000263, VTN-DOM-0003016, VTN-DOM-0012278
- Labels: Mat Foundations, Mat Foundations, Mat Foundation
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment with high directionality risk: mat or raft foundation spans STR, GEO, and ARC contexts, but the three-node alignment, type mismatch, and standard edge require careful review.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect HAS_FACET and MAPS_TO_EXTERNAL_STANDARD edges; propose non-identity alignment only if safe.

### shallow foundation - p1-decision-packet-d5a20759fdfd

- Packet ID: `p1-decision-packet-d5a20759fdfd`
- Group ID: `dup-6400e3e0c204`
- Node IDs: VTN-DOM-0000261, VTN-DOM-0003010
- Labels: Shallow Foundations, Shallow Foundations
- Current review status: `kimi_reviewed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate: STR and GEO shallow-foundation nodes likely represent the same engineering object from separate disciplinary views, with different taxonomy contexts and no resource links.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts
- Next exact action: Compare children and edge neighborhoods; draft alignment language only.

### shear wall - p1-decision-packet-9d2ac282265b

- Packet ID: `p1-decision-packet-9d2ac282265b`
- Group ID: `dup-db832ee203d2`
- Node IDs: VTN-DOM-0000265, VTN-DOM-0012270
- Labels: Shear Walls, Shear Wall
- Current review status: `human_review_needed`
- Recommended future action: `related_specialization_candidate`
- Why suitable or not suitable: Kimi classifies this as related specialization candidate requiring human directionality review: STR seismic Shear Walls may be a design-topic specialization of ARC Shear Wall as building element, but directionality is risky because STR context is seismic-specific.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: RELATED_SPECIALIZATION_OF from narrower structural/seismic topic toward broader building element if human reviewer confirms scope
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Human reviewer should verify whether STR node is seismic-design specialization, not duplicate.

### deep foundation - p1-decision-packet-8a66e785d02a

- Packet ID: `p1-decision-packet-8a66e785d02a`
- Group ID: `dup-5c6457d515c1`
- Node IDs: VTN-DOM-0000262, VTN-DOM-0003013
- Labels: Deep Foundations, Deep Foundations
- Current review status: `kimi_reviewed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate: STR and GEO Deep Foundations nodes likely describe the same class through discipline-specific taxonomies, with low mutation pressure and no resource links.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts
- Next exact action: Compare children; if parallel, queue non-identity alignment proposal.

### retaining wall - p1-decision-packet-12e81a4fbcde

- Packet ID: `p1-decision-packet-12e81a4fbcde`
- Group ID: `dup-b2f8807aa183`
- Node IDs: VTN-DOM-0003026, VTN-DOM-0012272
- Labels: Retaining Walls, Retaining Wall
- Current review status: `human_review_needed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate requiring human and source review: GEO retaining-wall system and ARC building-structural concept are semantically close but discipline-scoped, and the external-standard edge creates directionality and source risk.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect MAPS_TO_EXTERNAL_STANDARD target and child nodes; draft alignment only if scope matches.

### wall finishe - p1-decision-packet-0cfa6a7f88a1

- Packet ID: `p1-decision-packet-0cfa6a7f88a1`
- Group ID: `dup-79f6cd2af6bf`
- Node IDs: VTN-DOM-0000513, VTN-DOM-0003441, VTN-DOM-0012156
- Labels: Wall Finishes, Wall Finishes, Wall Finishes
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as high-risk edge-neighborhood review needed: three Wall Finishes nodes span material finish/product and ARC concept contexts, and duplicate status is unclear from type and taxonomy differences.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Review MAT.FIN versus MAT.FIP distinction before any relation proposal.

### load path - p1-decision-packet-3946860e327a

- Packet ID: `p1-decision-packet-3946860e327a`
- Group ID: `dup-621135f7b4b9`
- Node IDs: VTN-DOM-0002932, VTN-DOM-0012160
- Labels: Load Paths, Load Path
- Current review status: `human_review_needed`
- Recommended future action: `needs_human_review`
- Why suitable or not suitable: Kimi classifies this as high-risk human review needed: STR subtopic and ARC concept overlap semantically, but node type, taxonomy context, REQUIRES edges, external-standard mappings, and two resource links make mutation unsafe.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Possible cross-domain alignment only after human/source/resource review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts; resource links must be preserved
- Next exact action: Route to human structural and architectural reviewer with resource-link preservation check.

## Alias-only candidates

- None in this reviewed subset.

## Relationship-enrichment candidates

### building - p1-decision-packet-fee6fbd9a0fc

- Packet ID: `p1-decision-packet-fee6fbd9a0fc`
- Group ID: `dup-ca1078594013`
- Node IDs: VTN-DOM-0000716, VTN-DOM-0000757
- Labels: Buildings, Buildings
- Current review status: `kimi_reviewed`
- Recommended future action: `governed_disambiguation_candidate`
- Why suitable or not suitable: Kimi classifies this as governed disambiguation: the HIS precedent-study bucket and FIG works/projects bucket share a surface label but have different taxonomy roles and edge neighborhoods.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: DISAMBIGUATED_FROM / governed disambiguation text; exact direction and labels require steward review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts; high combined edge count
- Next exact action: Review child lists for label clarification only; keep consolidation out of scope.

### mat foundation - p1-decision-packet-fa4918982178

- Packet ID: `p1-decision-packet-fa4918982178`
- Group ID: `dup-a403cae6e1ea`
- Node IDs: VTN-DOM-0000263, VTN-DOM-0003016, VTN-DOM-0012278
- Labels: Mat Foundations, Mat Foundations, Mat Foundation
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment with high directionality risk: mat or raft foundation spans STR, GEO, and ARC contexts, but the three-node alignment, type mismatch, and standard edge require careful review.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect HAS_FACET and MAPS_TO_EXTERNAL_STANDARD edges; propose non-identity alignment only if safe.

### shallow foundation - p1-decision-packet-d5a20759fdfd

- Packet ID: `p1-decision-packet-d5a20759fdfd`
- Group ID: `dup-6400e3e0c204`
- Node IDs: VTN-DOM-0000261, VTN-DOM-0003010
- Labels: Shallow Foundations, Shallow Foundations
- Current review status: `kimi_reviewed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate: STR and GEO shallow-foundation nodes likely represent the same engineering object from separate disciplinary views, with different taxonomy contexts and no resource links.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts
- Next exact action: Compare children and edge neighborhoods; draft alignment language only.

### shear wall - p1-decision-packet-9d2ac282265b

- Packet ID: `p1-decision-packet-9d2ac282265b`
- Group ID: `dup-db832ee203d2`
- Node IDs: VTN-DOM-0000265, VTN-DOM-0012270
- Labels: Shear Walls, Shear Wall
- Current review status: `human_review_needed`
- Recommended future action: `related_specialization_candidate`
- Why suitable or not suitable: Kimi classifies this as related specialization candidate requiring human directionality review: STR seismic Shear Walls may be a design-topic specialization of ARC Shear Wall as building element, but directionality is risky because STR context is seismic-specific.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: RELATED_SPECIALIZATION_OF from narrower structural/seismic topic toward broader building element if human reviewer confirms scope
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Human reviewer should verify whether STR node is seismic-design specialization, not duplicate.

### deep foundation - p1-decision-packet-8a66e785d02a

- Packet ID: `p1-decision-packet-8a66e785d02a`
- Group ID: `dup-5c6457d515c1`
- Node IDs: VTN-DOM-0000262, VTN-DOM-0003013
- Labels: Deep Foundations, Deep Foundations
- Current review status: `kimi_reviewed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate: STR and GEO Deep Foundations nodes likely describe the same class through discipline-specific taxonomies, with low mutation pressure and no resource links.
- Risk level: `medium`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: not before drafting non-mutating review packet; yes before any graph change
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different taxonomy contexts
- Next exact action: Compare children; if parallel, queue non-identity alignment proposal.

### retaining wall - p1-decision-packet-12e81a4fbcde

- Packet ID: `p1-decision-packet-12e81a4fbcde`
- Group ID: `dup-b2f8807aa183`
- Node IDs: VTN-DOM-0003026, VTN-DOM-0012272
- Labels: Retaining Walls, Retaining Wall
- Current review status: `human_review_needed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate requiring human and source review: GEO retaining-wall system and ARC building-structural concept are semantically close but discipline-scoped, and the external-standard edge creates directionality and source risk.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect MAPS_TO_EXTERNAL_STANDARD target and child nodes; draft alignment only if scope matches.

### wall finishe - p1-decision-packet-0cfa6a7f88a1

- Packet ID: `p1-decision-packet-0cfa6a7f88a1`
- Group ID: `dup-79f6cd2af6bf`
- Node IDs: VTN-DOM-0000513, VTN-DOM-0003441, VTN-DOM-0012156
- Labels: Wall Finishes, Wall Finishes, Wall Finishes
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as high-risk edge-neighborhood review needed: three Wall Finishes nodes span material finish/product and ARC concept contexts, and duplicate status is unclear from type and taxonomy differences.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Review MAT.FIN versus MAT.FIP distinction before any relation proposal.

## Rejected / false-positive duplicate candidates

- None in this reviewed subset.

## Blocked / high-risk candidates

### mat foundation - p1-decision-packet-fa4918982178

- Packet ID: `p1-decision-packet-fa4918982178`
- Group ID: `dup-a403cae6e1ea`
- Node IDs: VTN-DOM-0000263, VTN-DOM-0003016, VTN-DOM-0012278
- Labels: Mat Foundations, Mat Foundations, Mat Foundation
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment with high directionality risk: mat or raft foundation spans STR, GEO, and ARC contexts, but the three-node alignment, type mismatch, and standard edge require careful review.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect HAS_FACET and MAPS_TO_EXTERNAL_STANDARD edges; propose non-identity alignment only if safe.

### shear wall - p1-decision-packet-9d2ac282265b

- Packet ID: `p1-decision-packet-9d2ac282265b`
- Group ID: `dup-db832ee203d2`
- Node IDs: VTN-DOM-0000265, VTN-DOM-0012270
- Labels: Shear Walls, Shear Wall
- Current review status: `human_review_needed`
- Recommended future action: `related_specialization_candidate`
- Why suitable or not suitable: Kimi classifies this as related specialization candidate requiring human directionality review: STR seismic Shear Walls may be a design-topic specialization of ARC Shear Wall as building element, but directionality is risky because STR context is seismic-specific.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: RELATED_SPECIALIZATION_OF from narrower structural/seismic topic toward broader building element if human reviewer confirms scope
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Human reviewer should verify whether STR node is seismic-design specialization, not duplicate.

### retaining wall - p1-decision-packet-12e81a4fbcde

- Packet ID: `p1-decision-packet-12e81a4fbcde`
- Group ID: `dup-b2f8807aa183`
- Node IDs: VTN-DOM-0003026, VTN-DOM-0012272
- Labels: Retaining Walls, Retaining Wall
- Current review status: `human_review_needed`
- Recommended future action: `cross_domain_alignment_candidate`
- Why suitable or not suitable: Kimi classifies this as cross-domain alignment candidate requiring human and source review: GEO retaining-wall system and ARC building-structural concept are semantically close but discipline-scoped, and the external-standard edge creates directionality and source risk.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: CROSS_DOMAIN_ALIGNMENT between discipline-scoped nodes; direction/symmetry require edge-neighborhood review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Inspect MAPS_TO_EXTERNAL_STANDARD target and child nodes; draft alignment only if scope matches.

### wall finishe - p1-decision-packet-0cfa6a7f88a1

- Packet ID: `p1-decision-packet-0cfa6a7f88a1`
- Group ID: `dup-79f6cd2af6bf`
- Node IDs: VTN-DOM-0000513, VTN-DOM-0003441, VTN-DOM-0012156
- Labels: Wall Finishes, Wall Finishes, Wall Finishes
- Current review status: `human_review_needed`
- Recommended future action: `needs_edge_neighborhood_review`
- Why suitable or not suitable: Kimi classifies this as high-risk edge-neighborhood review needed: three Wall Finishes nodes span material finish/product and ARC concept contexts, and duplicate status is unclear from type and taxonomy differences.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Potential non-identity relation only after child/HAS_FACET/MAPS_TO_EXTERNAL_STANDARD review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts
- Next exact action: Review MAT.FIN versus MAT.FIP distinction before any relation proposal.

### load path - p1-decision-packet-3946860e327a

- Packet ID: `p1-decision-packet-3946860e327a`
- Group ID: `dup-621135f7b4b9`
- Node IDs: VTN-DOM-0002932, VTN-DOM-0012160
- Labels: Load Paths, Load Path
- Current review status: `human_review_needed`
- Recommended future action: `needs_human_review`
- Why suitable or not suitable: Kimi classifies this as high-risk human review needed: STR subtopic and ARC concept overlap semantically, but node type, taxonomy context, REQUIRES edges, external-standard mappings, and two resource links make mutation unsafe.
- Risk level: `high`
- Required approval type: future steward approval through canonical mutation/admission gate; this queue is not approval.
- Kimi reviewed: yes
- Human review still needed: yes
- Possible non-destructive relationship candidates: Possible cross-domain alignment only after human/source/resource review
- Possible alias-only candidates: none accepted by Kimi for this reviewed packet.
- Possible keep-separate candidate: yes; preserve all current nodes unless a separate future steward process decides otherwise.
- Blocked reasons: different node types; different taxonomy contexts; resource links must be preserved
- Next exact action: Route to human structural and architectural reviewer with resource-link preservation check.


## Medium-risk steward packet prepared - 2026-05-02T05:31:17Z

The three medium-risk ready candidates now have a steward-ready, non-destructive packet:

- Packet file: `.ai/13_research/medium_risk_p1_steward_review_packet.md`
- Admission preview: `.ai/13_research/medium_risk_p1_admission_preview_report.md`
- Kimi critique: `.ai/13_research/medium_risk_p1_steward_packet_kimi_review.md`

This preparation is advisory only. It creates no approval, graph edge, merge, alias, redirect, tombstone, or Resource Layer mutation.

Kimi critique accepted in this packet:
- Buildings should prefer metadata-only governed disambiguation; visible reciprocal `DISAMBIGUATED_FROM` edges are optional future proposals only if a human steward decides the UX benefit outweighs learner-facing noise.
- Shallow and Deep Foundations may be future reciprocal `CROSS_DOMAIN_ALIGNMENT` candidates; do not use `CROSS_DOMAIN_EQUIVALENT`.
- All future action remains blocked by missing real steward approval, dry-run preview, transaction manifest, rollback plan, and validation.


## 2026-05-02T06:03:16Z - Admission status update

### Admitted / steward-approved in this run

- Deep Foundations (`p1-decision-packet-8a66e785d02a`, `dup-5c6457d515c1`): admitted reciprocal `CROSS_DOMAIN_ALIGNMENT` edges under scoped project-owner steward approval.
- Shallow Foundations (`p1-decision-packet-d5a20759fdfd`, `dup-6400e3e0c204`): admitted reciprocal `CROSS_DOMAIN_ALIGNMENT` edges under scoped project-owner steward approval.
- Buildings (`p1-decision-packet-fee6fbd9a0fc`, `dup-ca1078594013`): recorded metadata-only `DISAMBIGUATED_KEEP_SEPARATE`; no production graph edge admitted.

### Still queued

- Refresh/rebase stale P1 packet snapshots after these admissions.
- Review remaining low/medium-risk P1 packets for additional non-destructive admission candidates.
- Keep high-risk/source-sensitive packets blocked until edge-neighborhood/source review.


## 2026-05-02T07:20:07Z - Post-admission/rebase status

The first three medium-risk queue items have been consumed by scoped steward-approved actions and are no longer open admission candidates:

- Deep Foundations: reciprocal `CROSS_DOMAIN_ALIGNMENT` admitted and packet `p1-decision-packet-8a66e785d02a` marked `consumed_by_non_destructive_admission`.
- Shallow Foundations: reciprocal `CROSS_DOMAIN_ALIGNMENT` admitted and packet `p1-decision-packet-d5a20759fdfd` marked `consumed_by_non_destructive_admission`.
- Buildings: metadata-only `DISAMBIGUATED_KEEP_SEPARATE` admitted and packet `p1-decision-packet-fee6fbd9a0fc` marked `metadata_disambiguation_admitted`; no visible graph edge was admitted.

Next queue work should come from newly reviewed low/medium-risk packets only after Kimi review, dry-run, validation, rollback, and graph visibility checks.
