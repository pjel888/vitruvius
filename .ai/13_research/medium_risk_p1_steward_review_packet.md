# Medium-Risk P1 Steward Review Packet

Date: 2026-05-02T05:24:16Z

## Scope and non-approval caveat

This packet prepares three already Kimi-reviewed P1 duplicate/canonical stewardship candidates for a future human/steward admission loop. It is advisory only. It is not steward approval, not graph mutation, not canonical admission, not a merge, not an alias, not a redirect, not a tombstone, and not a Resource Layer change.

No production graph node or edge is changed by this file. No approval record or admitted relationship record is created by this file.

## Candidate summary

| Candidate | Packet | Group | Nodes | Current review | Risk | Future steward review path |
|---|---|---|---|---|---|---|
| Buildings | `p1-decision-packet-fee6fbd9a0fc` | `dup-ca1078594013` | `VTN-DOM-0000716`, `VTN-DOM-0000757` | `kimi_reviewed` / `governed_disambiguation_candidate` | `medium` | `governed_disambiguation_candidate` |
| Shallow Foundations | `p1-decision-packet-d5a20759fdfd` | `dup-6400e3e0c204` | `VTN-DOM-0000261`, `VTN-DOM-0003010` | `kimi_reviewed` / `cross_domain_alignment_candidate` | `medium` | `cross_domain_alignment_candidate` |
| Deep Foundations | `p1-decision-packet-8a66e785d02a` | `dup-5c6457d515c1` | `VTN-DOM-0000262`, `VTN-DOM-0003013` | `kimi_reviewed` / `cross_domain_alignment_candidate` | `medium` | `cross_domain_alignment_candidate` |

## Relation vocabulary review

- `DISAMBIGUATED_FROM` is present in the canonical stewardship relation vocabulary and in the admitted relationship type set.
- `CROSS_DOMAIN_ALIGNMENT` is present in the canonical stewardship relation vocabulary and in the admitted relationship type set.
- `CROSS_DOMAIN_EQUIVALENT` remains too strong for production admission; current code normalizes it to `CROSS_DOMAIN_ALIGNMENT` for admission preview and validation blocks active admitted `CROSS_DOMAIN_EQUIVALENT` edges.
- `CROSS_DOMAIN_ALIGNMENT` requires reciprocal proposals for validation consistency; this packet does not apply either reciprocal edge.

## Candidate-by-candidate analysis

### Buildings - `p1-decision-packet-fee6fbd9a0fc`

- Group ID: `dup-ca1078594013`
- Normalized label: `building`
- Current packet review status: `kimi_reviewed`
- Current Kimi recommended action: `governed_disambiguation_candidate`
- Review risk level: `medium`
- Packet content hash: `8f16388aa4601c8e6a07c582f53a6982996efc4c1a803fe6aa3e6faecadd3120`
- Group input hash: `7a9480b9901a7e30f93ef285aa53d45fc7bfeaae4db2d300e4179037237012fa`
- Candidate edge neighborhood hash: `7d1a0065bddc6c98d52f13c49205b07d2bc50a9c124220aa135578e42975fd31`
- Source snapshot hash: `92885969a8cc72d61331742a7f1c995e9b542b881b52487e28decdd94a519f93`
- Signature status: `unsigned`; algorithm `hmac-sha256`; current environment has no configured packet HMAC key
- Resource links in packet: `0`; node-resource links for candidate nodes: `0`

Candidate nodes:
- `VTN-DOM-0000716` - label `Buildings`, type `subtopic`, taxonomy path `HIS > HIS.PRE > HIS.PRE.BLD`, graph path `HIS.PRE.BLD`, parent `HIS.PRE`
  - Aliases/codes: `HIS.PRE.BLD`, `HIS.PRE.BLD`, `buildings`, `precedent studies buildings`
  - Description field: not present in current P1 packet/graph payload; this packet must not invent one.
  - Edge neighborhood excerpt:
    - incoming broader_than from `VTN-DOM-0000106` Precedents (HIS.PRE)
    - outgoing broader_than to `VTN-DOM-0008144` Buildings Chronology And Periodization (HIS.PRE.BLD.BCP)
    - outgoing broader_than to `VTN-DOM-0008145` Buildings Regional Transmission Path (HIS.PRE.BLD.BRT)
    - outgoing broader_than to `VTN-DOM-0008146` Buildings Typology And Precedent Examples (HIS.PRE.BLD.BTP)
    - outgoing broader_than to `VTN-DOM-0008147` Buildings Material Culture And Craft Evidence (HIS.PRE.BLD.BMC)
    - outgoing broader_than to `VTN-DOM-0008148` Buildings Interpretation And Historiography (HIS.PRE.BLD.BIH)
- `VTN-DOM-0000757` - label `Buildings`, type `subtopic`, taxonomy path `FIG > FIG.WRK > FIG.WRK.BUI`, graph path `FIG.WRK.BUI`, parent `FIG.WRK`
  - Aliases/codes: `FIG.WRK.BUI`, `FIG.WRK.BUI`, `buildings`, `works and projects buildings`
  - Description field: not present in current P1 packet/graph payload; this packet must not invent one.
  - Edge neighborhood excerpt:
    - incoming broader_than from `VTN-DOM-0000114` Works And Projects (FIG.WRK)
    - outgoing broader_than to `VTN-DOM-0007219` Buildings Biographical Context (FIG.WRK.BUI.BBC)
    - outgoing broader_than to `VTN-DOM-0007220` Buildings Major Work Attribution (FIG.WRK.BUI.BMW)
    - outgoing broader_than to `VTN-DOM-0007221` Buildings Influence Network Mapping (FIG.WRK.BUI.BIN)
    - outgoing broader_than to `VTN-DOM-0007222` Buildings Practice Or Institution Role (FIG.WRK.BUI.BPI)
    - outgoing broader_than to `VTN-DOM-0007223` Buildings Citation And Source Trace (FIG.WRK.BUI.BCS)
    - outgoing broader_than to `VTN-DOM-0012024` Cultural Center Of The Philippines Complex (FIG.WRK.BUI.CCP)
    - outgoing broader_than to `VTN-DOM-0012025` Philippine International Convention Center (FIG.WRK.BUI.PIC)
    - outgoing broader_than to `VTN-DOM-0012026` San Agustin Church Manila (FIG.WRK.BUI.SJA)
    - outgoing broader_than to `VTN-DOM-0012027` UST Main Building (FIG.WRK.BUI.UST)
    - outgoing broader_than to `VTN-DOM-0012028` Folk Arts Theater (FIG.WRK.BUI.FHA)
    - outgoing broader_than to `VTN-DOM-0012029` Coconut Palace (FIG.WRK.BUI.COC)
    - outgoing broader_than to `VTN-DOM-0012483` Serpentine Pavilion 2014 (FIG.WRK.BUI.SRP)
    - ... 127 additional outgoing edges omitted from this report; see graph packet edge summary.

Kimi review basis already recorded:
> Kimi classifies this as governed disambiguation: the HIS precedent-study bucket and FIG works/projects bucket share a surface label but have different taxonomy roles and edge neighborhoods.

- Accepted suggestions: Preserve both nodes as distinct taxonomy-context concepts.; Add disambiguating labels such as Buildings (precedent studies) versus Buildings (works and projects) in a future steward review.
- Rejected suggestions: Do not merge these nodes.; Do not treat this as alias-only based on surface label alone.
- Deferred suggestions: Future non-identity disambiguation relation may be considered after steward review.
- Next action from review registry: Review child lists for label clarification only; keep consolidation out of scope.

Proposed future steward decision (not applied):
- Decision: `GOVERNED_DISAMBIGUATION or DISAMBIGUATED_KEEP_SEPARATE`
- Proposed relation type: `DISAMBIGUATED_FROM`
- Direction/symmetry: Prefer metadata-only disambiguation. If visible relation admission is approved later, propose explicit reciprocal DISAMBIGUATED_FROM edges so the UI can show bidirectional disambiguation without implying identity.
- Proposed edge IDs if visible relation admission is approved later: `VTN-DOM-0000716--disambiguated_from--VTN-DOM-0000757`, `VTN-DOM-0000757--disambiguated_from--VTN-DOM-0000716`
- Existing production edges with those IDs now: `0`
- Rationale: The HIS precedent-study bucket and FIG works/projects bucket share a surface label but represent distinct taxonomy-context containers with very different child neighborhoods.

Future admission blockers/checklist:
- Real human/steward approval record must exist; Kimi review is not approval.
- Dry-run preview must show no merge, alias, redirect, tombstone, resource rewrite, or node rename.
- Packet hashes and source snapshot must remain current, or stale-review warning must be resolved by regenerating/reviewing.
- Current graph must not already contain the proposed edge tuple.
- Transaction manifest and rollback/remediation preview must be prepared before mutation.
- Candidate-specific caution: Visible DISAMBIGUATED_FROM edges between broad taxonomy containers may add learner-facing noise; metadata-only disambiguation should remain acceptable if a steward prefers it.

### Shallow Foundations - `p1-decision-packet-d5a20759fdfd`

- Group ID: `dup-6400e3e0c204`
- Normalized label: `shallow foundation`
- Current packet review status: `kimi_reviewed`
- Current Kimi recommended action: `cross_domain_alignment_candidate`
- Review risk level: `medium`
- Packet content hash: `d723c0b32a052cc8bbfd6387f6e03bc30becfc70a6542a1ffc775ca32395cc46`
- Group input hash: `0b51b39a6d2e35d080923b4e6e15b6fbad1537ffbd6482e7343c90d51ea1365d`
- Candidate edge neighborhood hash: `4bcd860c191fbca419662a911c9e95014c1312c5bf8a24e90f3d5a1ca0a607db`
- Source snapshot hash: `92885969a8cc72d61331742a7f1c995e9b542b881b52487e28decdd94a519f93`
- Signature status: `unsigned`; algorithm `hmac-sha256`; current environment has no configured packet HMAC key
- Resource links in packet: `0`; node-resource links for candidate nodes: `0`

Candidate nodes:
- `VTN-DOM-0000261` - label `Shallow Foundations`, type `subtopic`, taxonomy path `STR > STR.FND > STR.FND.SHL`, graph path `STR.FND.SHL`, parent `STR.FND`
  - Aliases/codes: `STR.FND.SHL`, `STR.FND.SHL`, `shallow foundations`, `foundations shallow foundations`, `shallow foundation system`, `near-surface foundation interface`
  - Description field: not present in current P1 packet/graph payload; this packet must not invent one.
  - Edge neighborhood excerpt:
    - incoming broader_than from `VTN-DOM-0000032` Foundations Interface (STR.FND)
    - outgoing broader_than to `VTN-DOM-0010999` Shallow Foundations Load Path Behavior (STR.FND.SHL.SFL)
    - outgoing broader_than to `VTN-DOM-0011000` Shallow Foundations Member Sizing Criteria (STR.FND.SHL.SFM)
    - outgoing broader_than to `VTN-DOM-0011001` Shallow Foundations Connection And Detailing Requirements (STR.FND.SHL.SFC)
    - outgoing broader_than to `VTN-DOM-0011002` Shallow Foundations Serviceability And Deflection Checks (STR.FND.SHL.SFS)
    - outgoing broader_than to `VTN-DOM-0011003` Shallow Foundations Inspection And Retrofit Considerations (STR.FND.SHL.SFI)
    - outgoing broader_than to `VTN-DOM-0012782` Footing Foundation (STR.FND.SHL.FTG)
    - outgoing broader_than to `VTN-DOM-0012785` Grade Beam (STR.FND.SHL.GRB)
    - outgoing broader_than to `VTN-DOM-0012786` Slab-On-Grade (STR.FND.SHL.SOG)
    - outgoing broader_than to `VTN-DOM-0012797` Foundation Bearing Capacity Interface (STR.FND.SHL.FBC)
    - outgoing broader_than to `VTN-DOM-0012798` Settlement Performance (STR.FND.SHL.STP)
    - outgoing broader_than to `VTN-DOM-0012799` Structural Retaining Wall (STR.FND.SHL.RTW)
- `VTN-DOM-0003010` - label `Shallow Foundations`, type `subtopic`, taxonomy path `GEO > GEO.FOE > GEO.FOE.SHF`, graph path `GEO.FOE.SHF`, parent `GEO.FOE`
  - Aliases/codes: `GEO.FOE.SHF`, `GEO.FOE.SHF`, `shallow foundations`
  - Description field: not present in current P1 packet/graph payload; this packet must not invent one.
  - Edge neighborhood excerpt:
    - incoming broader_than from `VTN-DOM-0003009` Foundation Engineering (GEO.FOE)
    - outgoing broader_than to `VTN-DOM-0007514` Shallow Foundations Site Investigation Parameters (GEO.FOE.SHF.SFS)
    - outgoing broader_than to `VTN-DOM-0007515` Shallow Foundations Design Assumption Controls (GEO.FOE.SHF.SFD)
    - outgoing broader_than to `VTN-DOM-0007516` Shallow Foundations Instrumentation And Monitoring Points (GEO.FOE.SHF.SFI)
    - outgoing broader_than to `VTN-DOM-0007517` Shallow Foundations Construction Risk Mitigation (GEO.FOE.SHF.SFC)
    - outgoing broader_than to `VTN-DOM-0007518` Shallow Foundations Long Term Performance Review (GEO.FOE.SHF.SFL)

Kimi review basis already recorded:
> Kimi classifies this as cross-domain alignment candidate: STR and GEO shallow-foundation nodes likely represent the same engineering object from separate disciplinary views, with different taxonomy contexts and no resource links.

- Accepted suggestions: Keep separate as discipline-scoped nodes.; Consider non-identity STR-GEO alignment in a future steward review.
- Rejected suggestions: Do not merge.; Do not treat as alias-only.
- Deferred suggestions: Future steward-reviewed cross-domain alignment wording.
- Next action from review registry: Compare children and edge neighborhoods; draft alignment language only.

Proposed future steward decision (not applied):
- Decision: `CROSS_DOMAIN_ALIGNMENT_CANDIDATE with keep-separate discipline scopes`
- Proposed relation type: `CROSS_DOMAIN_ALIGNMENT`
- Direction/symmetry: Symmetric cross-domain peer alignment. Current validation expects reciprocal edge proposals for CROSS_DOMAIN_ALIGNMENT.
- Proposed edge IDs if visible relation admission is approved later: `VTN-DOM-0000261--cross_domain_alignment--VTN-DOM-0003010`, `VTN-DOM-0003010--cross_domain_alignment--VTN-DOM-0000261`
- Existing production edges with those IDs now: `0`
- Rationale: The STR node captures structural shallow-foundation behavior/design topics; the GEO node captures geotechnical foundation-engineering controls for the same object family.

Future admission blockers/checklist:
- Real human/steward approval record must exist; Kimi review is not approval.
- Dry-run preview must show no merge, alias, redirect, tombstone, resource rewrite, or node rename.
- Packet hashes and source snapshot must remain current, or stale-review warning must be resolved by regenerating/reviewing.
- Current graph must not already contain the proposed edge tuple.
- Transaction manifest and rollback/remediation preview must be prepared before mutation.
- Candidate-specific caution: Do not phrase this as equivalence or merge; the safe claim is non-identity discipline-context alignment.

### Deep Foundations - `p1-decision-packet-8a66e785d02a`

- Group ID: `dup-5c6457d515c1`
- Normalized label: `deep foundation`
- Current packet review status: `kimi_reviewed`
- Current Kimi recommended action: `cross_domain_alignment_candidate`
- Review risk level: `medium`
- Packet content hash: `5469654cd4d3c42d4d4717a05bedd316678b846de62fb7e331b8b6832d3cbea7`
- Group input hash: `86a8eef6afe3f5086d22a58cd9c94afda54ba6f7fa46b89143d78039cf8e8da0`
- Candidate edge neighborhood hash: `dde9ff4db95effe4049582168f74b7135d8184ecb391bbeef00bde22b145d885`
- Source snapshot hash: `92885969a8cc72d61331742a7f1c995e9b542b881b52487e28decdd94a519f93`
- Signature status: `unsigned`; algorithm `hmac-sha256`; current environment has no configured packet HMAC key
- Resource links in packet: `0`; node-resource links for candidate nodes: `0`

Candidate nodes:
- `VTN-DOM-0000262` - label `Deep Foundations`, type `subtopic`, taxonomy path `STR > STR.FND > STR.FND.DEP`, graph path `STR.FND.DEP`, parent `STR.FND`
  - Aliases/codes: `STR.FND.DEP`, `STR.FND.DEP`, `deep foundations`, `foundations deep foundations`
  - Description field: not present in current P1 packet/graph payload; this packet must not invent one.
  - Edge neighborhood excerpt:
    - incoming broader_than from `VTN-DOM-0000032` Foundations Interface (STR.FND)
    - outgoing broader_than to `VTN-DOM-0010989` Deep Foundations Load Path Behavior (STR.FND.DEP.DFL)
    - outgoing broader_than to `VTN-DOM-0010990` Deep Foundations Member Sizing Criteria (STR.FND.DEP.DFM)
    - outgoing broader_than to `VTN-DOM-0010991` Deep Foundations Connection And Detailing Requirements (STR.FND.DEP.DFC)
    - outgoing broader_than to `VTN-DOM-0010992` Deep Foundations Serviceability And Deflection Checks (STR.FND.DEP.DFS)
    - outgoing broader_than to `VTN-DOM-0010993` Deep Foundations Inspection And Retrofit Considerations (STR.FND.DEP.DFI)
    - outgoing broader_than to `VTN-DOM-0012783` Pile Foundation System (STR.FND.DEP.PFS)
    - outgoing broader_than to `VTN-DOM-0012784` Pile Cap (STR.FND.DEP.PCP)
- `VTN-DOM-0003013` - label `Deep Foundations`, type `subtopic`, taxonomy path `GEO > GEO.FOE > GEO.FOE.DEF`, graph path `GEO.FOE.DEF`, parent `GEO.FOE`
  - Aliases/codes: `GEO.FOE.DEF`, `GEO.FOE.DEF`, `deep foundations`
  - Description field: not present in current P1 packet/graph payload; this packet must not invent one.
  - Edge neighborhood excerpt:
    - incoming broader_than from `VTN-DOM-0003009` Foundation Engineering (GEO.FOE)
    - outgoing broader_than to `VTN-DOM-0007499` Deep Foundations Site Investigation Parameters (GEO.FOE.DEF.DFS)
    - outgoing broader_than to `VTN-DOM-0007500` Deep Foundations Design Assumption Controls (GEO.FOE.DEF.DFD)
    - outgoing broader_than to `VTN-DOM-0007501` Deep Foundations Instrumentation And Monitoring Points (GEO.FOE.DEF.DFI)
    - outgoing broader_than to `VTN-DOM-0007502` Deep Foundations Construction Risk Mitigation (GEO.FOE.DEF.DFC)
    - outgoing broader_than to `VTN-DOM-0007503` Deep Foundations Long Term Performance Review (GEO.FOE.DEF.DFL)

Kimi review basis already recorded:
> Kimi classifies this as cross-domain alignment candidate: STR and GEO Deep Foundations nodes likely describe the same class through discipline-specific taxonomies, with low mutation pressure and no resource links.

- Accepted suggestions: Keep separate as discipline-scoped nodes.; Consider STR-GEO cross-domain alignment.
- Rejected suggestions: Do not merge.; Do not treat as alias-only.
- Deferred suggestions: Steward-reviewed alignment wording.
- Next action from review registry: Compare children; if parallel, queue non-identity alignment proposal.

Proposed future steward decision (not applied):
- Decision: `CROSS_DOMAIN_ALIGNMENT_CANDIDATE with keep-separate discipline scopes`
- Proposed relation type: `CROSS_DOMAIN_ALIGNMENT`
- Direction/symmetry: Symmetric cross-domain peer alignment. Current validation expects reciprocal edge proposals for CROSS_DOMAIN_ALIGNMENT.
- Proposed edge IDs if visible relation admission is approved later: `VTN-DOM-0000262--cross_domain_alignment--VTN-DOM-0003013`, `VTN-DOM-0003013--cross_domain_alignment--VTN-DOM-0000262`
- Existing production edges with those IDs now: `0`
- Rationale: The STR node covers structural load/member/cap behavior; the GEO node covers investigation, assumptions, monitoring, construction risk, and long-term performance for the same foundation class.

Future admission blockers/checklist:
- Real human/steward approval record must exist; Kimi review is not approval.
- Dry-run preview must show no merge, alias, redirect, tombstone, resource rewrite, or node rename.
- Packet hashes and source snapshot must remain current, or stale-review warning must be resolved by regenerating/reviewing.
- Current graph must not already contain the proposed edge tuple.
- Transaction manifest and rollback/remediation preview must be prepared before mutation.
- Candidate-specific caution: Do not use CROSS_DOMAIN_EQUIVALENT; alignment remains non-identity and steward-gated.

## Resource Layer preservation summary

- Current Resource Layer resources: `7`.
- Current nodeResourceLinks: `9`.
- Candidate nodes have zero nodeResourceLinks in the current registry.
- Future admission, if any, must not rewrite resources, links, review decisions, standards context, local-file candidates, or source checks.

## Rollback preview

- Metadata-only future decision rollback: mark or remove the non-destructive decision/review metadata through canonical rollback controls and transaction manifest.
- Future admitted relationship rollback: roll back admitted relationship records/edges by transaction ID and verify node/resource counts remain unchanged.
- No edge rollback is needed for this packet because no edge is added in this run.

## Graph visibility preview

- If future `CROSS_DOMAIN_ALIGNMENT` edges are admitted, `/node/:id/neighborhood?depth=1&direction=both` should expose both reciprocal foundation alignment edges and Explorer dynamic filters must include `CROSS_DOMAIN_ALIGNMENT`.
- If future `DISAMBIGUATED_FROM` edges are admitted for Buildings, both directions should be visible to avoid one-sided disambiguation; however Kimi recommends metadata-only disambiguation unless visible edges improve learner UX.
- This run does not change graph visibility; existing graph edge count remains expected at 13,670.

## Validation preview

- Admission must be blocked until real steward approval exists.
- Admission must be blocked if packet hashes/snapshots are stale or if proposed edge tuples already exist.
- Admission must be blocked if it would create `CROSS_DOMAIN_EQUIVALENT`, a self-loop, missing reciprocal `CROSS_DOMAIN_ALIGNMENT`, or any alias/redirect/tombstone/merge without explicit destructive gates.
- Future transaction manifest should cover any touched graph-canonical custody files and latest afterHash validation must match after mutation.

## Human/steward approval checklist

1. Confirm the candidate node IDs, labels, and taxonomy paths still match this packet.
2. Confirm packet content hash, source snapshot hash, and candidate edge neighborhood hash are current or regenerate/review before action.
3. Confirm human/steward approval metadata is real and distinct from Kimi/advisory review.
4. Confirm mutation scope is non-destructive edge admission or metadata-only disambiguation.
5. Confirm no merge, alias, redirect, tombstone, resource rewrite, or node rename is requested.
6. For foundation pairs, require reciprocal `CROSS_DOMAIN_ALIGNMENT` preview.
7. For Buildings, decide explicitly between metadata-only disambiguation and visible reciprocal `DISAMBIGUATED_FROM` edges.
8. Run canonical, graph relationship, Resource Layer, API, Explorer, and build validation before and after any admission.
9. Verify rollback/remediation plan and transaction manifest before applying mutation.
10. Verify Explorer/search wording does not imply equivalence, merge, or canonicalized identity.

## Kimi critique summary

Kimi accepted the packet as a future-review candidate with safeguards. Kimi accepted reciprocal `CROSS_DOMAIN_ALIGNMENT` for Shallow and Deep Foundations, rejected `CROSS_DOMAIN_EQUIVALENT`, rejected merge/alias/redirect/tombstone paths, and cautioned that Buildings should prefer metadata-only disambiguation unless visible `DISAMBIGUATED_FROM` edges improve learner UX. Actual admission and learner-facing wording remain deferred to a future human/steward loop.

## Exact next action if approved later

Create a real steward approval record for one bounded non-destructive candidate, run canonical relationship admission preview, verify reciprocal edge requirements and UI visibility, then apply through the existing gated admission workflow with transaction manifest and rollback preview.

## Exact next action if rejected

Keep the packet review metadata advisory, mark the candidate as keep-separate or rejected in future review metadata, and do not admit graph edges.

## Confirmation

- No production graph mutation occurred in preparing this packet.
- No approval, admitted relationship, alias, redirect, tombstone, merge, or Resource Layer mutation occurred.

## 2026-05-02T06:03:16Z - Admission status update

### Admitted / steward-approved in this run

- Deep Foundations (`p1-decision-packet-8a66e785d02a`, `dup-5c6457d515c1`): admitted reciprocal `CROSS_DOMAIN_ALIGNMENT` edges under scoped project-owner steward approval.
- Shallow Foundations (`p1-decision-packet-d5a20759fdfd`, `dup-6400e3e0c204`): admitted reciprocal `CROSS_DOMAIN_ALIGNMENT` edges under scoped project-owner steward approval.
- Buildings (`p1-decision-packet-fee6fbd9a0fc`, `dup-ca1078594013`): recorded metadata-only `DISAMBIGUATED_KEEP_SEPARATE`; no production graph edge admitted.

### Still queued

- Refresh/rebase stale P1 packet snapshots after these admissions.
- Review remaining low/medium-risk P1 packets for additional non-destructive admission candidates.
- Keep high-risk/source-sensitive packets blocked until edge-neighborhood/source review.
