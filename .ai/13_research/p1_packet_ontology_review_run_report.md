# P1 Packet Ontology Review Run Report

Date: 2026-05-02T05:00:53Z

## 1. Packets selected

Selected the top eight unreviewed P1 packets by existing priority ordering, graph impact, AEC/Architecture/Civil/Structural relevance, and review value. The set includes one very high edge-count label collision, several structural/geotechnical/building-system concept overlaps, and one packet with Resource Layer links requiring preservation.

1. `p1-decision-packet-fee6fbd9a0fc` (`dup-ca1078594013`) - building; priority 75; packet risk medium; review status kimi_reviewed; review risk medium.
2. `p1-decision-packet-fa4918982178` (`dup-a403cae6e1ea`) - mat foundation; priority 71; packet risk high; review status human_review_needed; review risk high.
3. `p1-decision-packet-d5a20759fdfd` (`dup-6400e3e0c204`) - shallow foundation; priority 71; packet risk medium; review status kimi_reviewed; review risk medium.
4. `p1-decision-packet-9d2ac282265b` (`dup-db832ee203d2`) - shear wall; priority 71; packet risk high; review status human_review_needed; review risk high.
5. `p1-decision-packet-8a66e785d02a` (`dup-5c6457d515c1`) - deep foundation; priority 71; packet risk medium; review status kimi_reviewed; review risk medium.
6. `p1-decision-packet-12e81a4fbcde` (`dup-b2f8807aa183`) - retaining wall; priority 71; packet risk high; review status human_review_needed; review risk high.
7. `p1-decision-packet-0cfa6a7f88a1` (`dup-79f6cd2af6bf`) - wall finishe; priority 71; packet risk high; review status human_review_needed; review risk high.
8. `p1-decision-packet-3946860e327a` (`dup-621135f7b4b9`) - load path; priority 61; packet risk high; review status human_review_needed; review risk high.

## 2. Kimi review summary per packet

### p1-decision-packet-fee6fbd9a0fc / dup-ca1078594013 / building

- Candidate nodes: VTN-DOM-0000716 (Buildings; subtopic; HIS > HIS.PRE > HIS.PRE.BLD); VTN-DOM-0000757 (Buildings; subtopic; FIG > FIG.WRK > FIG.WRK.BUI)
- Kimi classification / action: `governed_disambiguation_candidate`
- Recorded review status: `kimi_reviewed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `medium`
- Summary: Kimi classifies this as governed disambiguation: the HIS precedent-study bucket and FIG works/projects bucket share a surface label but have different taxonomy roles and edge neighborhoods.
- Accepted suggestions: Preserve both nodes as distinct taxonomy-context concepts.; Add disambiguating labels such as Buildings (precedent studies) versus Buildings (works and projects) in a future steward review.
- Rejected suggestions: Do not merge these nodes.; Do not treat this as alias-only based on surface label alone.
- Deferred suggestions: Future non-identity disambiguation relation may be considered after steward review.
- Next action: Review child lists for label clarification only; keep consolidation out of scope.

### p1-decision-packet-fa4918982178 / dup-a403cae6e1ea / mat foundation

- Candidate nodes: VTN-DOM-0000263 (Mat Foundations; subtopic; STR > STR.FND > STR.FND.MAT); VTN-DOM-0003016 (Mat Foundations; subtopic; GEO > GEO.FOE > GEO.FOE.MAF); VTN-DOM-0012278 (Mat Foundation; concept; ARC > ARC.BLD > ARC.BLD.STR > ARC.BLD.STR.MTF)
- Kimi classification / action: `needs_edge_neighborhood_review`
- Recorded review status: `human_review_needed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `high`
- Summary: Kimi classifies this as cross-domain alignment with high directionality risk: mat or raft foundation spans STR, GEO, and ARC contexts, but the three-node alignment, type mismatch, and standard edge require careful review.
- Accepted suggestions: Preserve all nodes.; Evaluate STR-GEO-ARC alignment as non-identity only.
- Rejected suggestions: Do not merge.; Do not collapse to a single canonical replacement.
- Deferred suggestions: Future cross-domain alignment after neighborhood review.
- Next action: Inspect HAS_FACET and MAPS_TO_EXTERNAL_STANDARD edges; propose non-identity alignment only if safe.

### p1-decision-packet-d5a20759fdfd / dup-6400e3e0c204 / shallow foundation

- Candidate nodes: VTN-DOM-0000261 (Shallow Foundations; subtopic; STR > STR.FND > STR.FND.SHL); VTN-DOM-0003010 (Shallow Foundations; subtopic; GEO > GEO.FOE > GEO.FOE.SHF)
- Kimi classification / action: `cross_domain_alignment_candidate`
- Recorded review status: `kimi_reviewed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `medium`
- Summary: Kimi classifies this as cross-domain alignment candidate: STR and GEO shallow-foundation nodes likely represent the same engineering object from separate disciplinary views, with different taxonomy contexts and no resource links.
- Accepted suggestions: Keep separate as discipline-scoped nodes.; Consider non-identity STR-GEO alignment in a future steward review.
- Rejected suggestions: Do not merge.; Do not treat as alias-only.
- Deferred suggestions: Future steward-reviewed cross-domain alignment wording.
- Next action: Compare children and edge neighborhoods; draft alignment language only.

### p1-decision-packet-9d2ac282265b / dup-db832ee203d2 / shear wall

- Candidate nodes: VTN-DOM-0000265 (Shear Walls; subtopic; STR > STR.SEI > STR.SEI.WAL); VTN-DOM-0012270 (Shear Wall; concept; ARC > ARC.BLD > ARC.BLD.STR > ARC.BLD.STR.SHW)
- Kimi classification / action: `related_specialization_candidate`
- Recorded review status: `human_review_needed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `high`
- Summary: Kimi classifies this as related specialization candidate requiring human directionality review: STR seismic Shear Walls may be a design-topic specialization of ARC Shear Wall as building element, but directionality is risky because STR context is seismic-specific.
- Accepted suggestions: Keep separate.; Evaluate specialization direction from STR seismic topic toward ARC building-structural concept.
- Rejected suggestions: Do not merge.; Do not treat as alias-only.
- Deferred suggestions: Possible relationship enrichment after REQUIRES and MAPS edge review.
- Next action: Human reviewer should verify whether STR node is seismic-design specialization, not duplicate.

### p1-decision-packet-8a66e785d02a / dup-5c6457d515c1 / deep foundation

- Candidate nodes: VTN-DOM-0000262 (Deep Foundations; subtopic; STR > STR.FND > STR.FND.DEP); VTN-DOM-0003013 (Deep Foundations; subtopic; GEO > GEO.FOE > GEO.FOE.DEF)
- Kimi classification / action: `cross_domain_alignment_candidate`
- Recorded review status: `kimi_reviewed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `medium`
- Summary: Kimi classifies this as cross-domain alignment candidate: STR and GEO Deep Foundations nodes likely describe the same class through discipline-specific taxonomies, with low mutation pressure and no resource links.
- Accepted suggestions: Keep separate as discipline-scoped nodes.; Consider STR-GEO cross-domain alignment.
- Rejected suggestions: Do not merge.; Do not treat as alias-only.
- Deferred suggestions: Steward-reviewed alignment wording.
- Next action: Compare children; if parallel, queue non-identity alignment proposal.

### p1-decision-packet-12e81a4fbcde / dup-b2f8807aa183 / retaining wall

- Candidate nodes: VTN-DOM-0003026 (Retaining Walls; subtopic; GEO > GEO.RSS > GEO.RSS.REW); VTN-DOM-0012272 (Retaining Wall; concept; ARC > ARC.BLD > ARC.BLD.STR > ARC.BLD.STR.RTW)
- Kimi classification / action: `cross_domain_alignment_candidate`
- Recorded review status: `human_review_needed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `high`
- Summary: Kimi classifies this as cross-domain alignment candidate requiring human and source review: GEO retaining-wall system and ARC building-structural concept are semantically close but discipline-scoped, and the external-standard edge creates directionality and source risk.
- Accepted suggestions: Keep separate.; Consider non-identity GEO-ARC alignment.
- Rejected suggestions: Do not merge.; Do not treat as alias-only.
- Deferred suggestions: Edge-neighborhood and source review before any future steward action.
- Next action: Inspect MAPS_TO_EXTERNAL_STANDARD target and child nodes; draft alignment only if scope matches.

### p1-decision-packet-0cfa6a7f88a1 / dup-79f6cd2af6bf / wall finishe

- Candidate nodes: VTN-DOM-0000513 (Wall Finishes; subtopic; MAT > MAT.FIN > MAT.FIN.WFI); VTN-DOM-0003441 (Wall Finishes; subtopic; MAT > MAT.FIP > MAT.FIP.WAF); VTN-DOM-0012156 (Wall Finishes; concept; ARC > ARC.MAT > ARC.MAT.FIN > ARC.MAT.FIN.WLF)
- Kimi classification / action: `needs_edge_neighborhood_review`
- Recorded review status: `human_review_needed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `high`
- Summary: Kimi classifies this as high-risk edge-neighborhood review needed: three Wall Finishes nodes span material finish/product and ARC concept contexts, and duplicate status is unclear from type and taxonomy differences.
- Accepted suggestions: Keep separate pending review.; Inspect child nodes and external-standard edge.
- Rejected suggestions: Do not merge all three nodes.; Do not treat as alias-only.
- Deferred suggestions: Possible governed disambiguation or relationship enrichment after neighborhood review.
- Next action: Review MAT.FIN versus MAT.FIP distinction before any relation proposal.

### p1-decision-packet-3946860e327a / dup-621135f7b4b9 / load path

- Candidate nodes: VTN-DOM-0002932 (Load Paths; subtopic; STR > STR.SAF > STR.SAF.LOP); VTN-DOM-0012160 (Load Path; concept; ARC > ARC.BLD > ARC.BLD.STR > ARC.BLD.STR.LDP)
- Kimi classification / action: `needs_human_review`
- Recorded review status: `human_review_needed`
- Reviewer type/source: `kimi` / `kimi`
- Risk level: `high`
- Summary: Kimi classifies this as high-risk human review needed: STR subtopic and ARC concept overlap semantically, but node type, taxonomy context, REQUIRES edges, external-standard mappings, and two resource links make mutation unsafe.
- Accepted suggestions: Preserve both nodes.; Inspect the resource-linked ARC node before any relationship proposal.; Preserve resource links during any future review.
- Rejected suggestions: Do not merge.; Do not move resource links.; Do not treat as alias-only.
- Deferred suggestions: Possible cross-domain alignment only after source and resource review.
- Next action: Route to human structural and architectural reviewer with resource-link preservation check.

## 3. Admission queue summary

- Ready for future non-destructive steward review: Buildings governed disambiguation, Shallow Foundations STR-GEO alignment, Deep Foundations STR-GEO alignment.
- Needs human/edge-neighborhood review before any future steward packet: Load Path, Wall Finishes, Mat Foundation, Shear Wall, Retaining Wall.
- Alias-only candidates: none accepted in this reviewed subset.
- Rejected/false-positive duplicate candidates: none fully rejected as false-positive in this reviewed subset.

## 4. Mutation and approval confirmation

- Production graph mutation: none.
- Steward approval: none.
- Merge/alias/redirect/tombstone/admitted relationship: none.
- Resource Layer mutation: none.
- Packet custody payload mutation: none; reviews are stored separately in `p1-packet-reviews.json`.

## 5. Review metrics after this run

- P1 packets total: 20
- P1 reviewed: 8
- P1 unreviewed: 12
- Reviewer type Kimi records: 8
- Status Kimi reviewed: 3
- Status human review needed: 5
- Human reviewed: 0
- Rejected: 0
- Deferred: 0
- Review risk counts: {'high': 5, 'medium': 3}
- Recommended action counts: {'needs_edge_neighborhood_review': 2, 'cross_domain_alignment_candidate': 3, 'needs_human_review': 1, 'related_specialization_candidate': 1, 'governed_disambiguation_candidate': 1}
- P1 review transaction manifests: 13
- Total canonical transaction manifests after updates: 23

## 6. Kimi critique handling

Accepted: preserve separate taxonomy-context nodes, reject merge/alias-only shortcuts, use cross-domain alignment/governed disambiguation/related specialization as future non-destructive candidates, and route high-risk/resource-linked packets to human or edge-neighborhood review.

Rejected: no Kimi suggestion was accepted as graph approval or immediate mutation. Any merge/alias-only interpretation for the reviewed packets was rejected.

Deferred: future steward approval packets, edge-neighborhood inspections, source/resource review for Load Path and standard-mapped packets, and any production graph relationship admission.

## 7. Validation/test results

- Canonical validation after applying reviews passed: 8 reviewed, 12 unreviewed, 3 status Kimi reviewed, 5 status human review needed, 0 stale/invalid reviews, 13 P1 review transaction manifests, 0 approvals/admitted relationships/aliases/redirects/tombstones.
- Graph relationship validation passed after review application: 10,018 nodes, 13,670 edges, 0 issues.
- Resource Layer validation passed after review application: 7 resources, 9 nodeResourceLinks, no blockers; ASCE/ACI standards-context warnings remain honest.
- Full validation also passed: cd api && bun test (166), cd explorer && bun test (112), cd explorer && bun run build (known Vite chunk warning only), and .venv\\Scripts\\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py (104).

## 8. Exact next action

Use the first graph admission queue to prepare a bounded non-destructive steward review packet for the medium-risk candidates only, while keeping high-risk packets in human/source/edge-neighborhood review and keeping P0 Concrete/Reinforced Concrete blocked until real steward approval exists.


## 2026-05-02T05:31:17Z - Medium-risk steward packet follow-up

- Converted the three medium-risk ready Kimi-reviewed packets into a steward-ready advisory packet and admission preview.
- Included Buildings (`p1-decision-packet-fee6fbd9a0fc`), Shallow Foundations (`p1-decision-packet-d5a20759fdfd`), and Deep Foundations (`p1-decision-packet-8a66e785d02a`).
- Proposed future decisions remain non-destructive and steward-gated: Buildings governed disambiguation/keep-separate; Shallow/Deep Foundations reciprocal `CROSS_DOMAIN_ALIGNMENT` candidates.
- No P1 review registry mutation was performed in this follow-up; reviewed/unreviewed counts remain 8 / 12.
- No production graph mutation, approval, admitted relationship, alias, redirect, tombstone, merge, or Resource Layer mutation occurred.
