# Full Autopilot Accepted-Link Reviews

Date: 2026-05-07 local

## Unit 1 - FHWA Earth Retaining Structures Link Review Packet

### Scope

Target Resource: `res-fhwa-earth-retaining-structures`

Target nodeResourceLink: `nrl-retaining-wall-fhwa-needs-review`

Target node: `VTN-DOM-0012799` / Retaining Wall

No new Resource, nodeResourceLink, graph edge, canonical mutation, protected payload, standards context claim, P0 Concrete/Reinforced Concrete action, or high-risk P1 action is proposed.

### Current State

| Field | Value |
|---|---|
| Resource title | Earth Retaining Structures |
| URL | `https://www.fhwa.dot.gov/engineering/geotech/retaining/` |
| Source family | `fhwa` |
| Resource type | `government_guidance` |
| Source authority | `government` |
| Access type | `public_web` |
| Verification status | `link_verified` |
| Existing lastCheckedAt | `2026-05-01T00:00:00.000Z` |
| Existing jurisdiction/scope | United States federal transportation/geotechnical context; `geographicScope: us` |
| Existing source rights | Public government page; metadata/rationale only; no copied payload text |
| Existing link status | `needs_review` |
| Existing relationship | `provides_design_guidance` |

Existing link rationale:

> FHWA's earth retaining structures page is relevant to retaining walls in U.S. transportation/geotechnical practice, but the generic structural retaining wall node needs context before accepted linking.

Existing review note:

> Kimi found the mapping defensible for Structural Retaining Wall, but it should remain reviewed for U.S. federal transportation scope.

### Bounded Official Source Recheck

Checked at: `2026-05-06T16:56:01.272Z`

Rules followed:

- HEAD first.
- Bounded GET for public metadata only.
- Timeout 10 seconds.
- Maximum inspected body: 1 MB.
- No full page content stored.
- No protected payload or PDF text ingested.
- No current/governing/compliance/AHJ claim.

| Method | Requested URL | Final URL | Status | Content Type | Official Domain Match | Public Metadata |
|---|---|---|---:|---|---|---|
| HEAD | `https://www.fhwa.dot.gov/engineering/geotech/retaining/` | same | 200 | `text/html;charset=UTF-8` | true | n/a |
| GET | `https://www.fhwa.dot.gov/engineering/geotech/retaining/` | same | 200 | `text/html;charset=UTF-8` | true | title: `Earth Retaining Structures - Geotech - Bridges & Structures - Federal Highway Administration`; inspected 11,321 bytes |

Source check limitations:

- HTTP success is not source truth.
- Page title and official domain match do not establish complete design guidance.
- This does not establish current, governing, compliance, AHJ, jurisdictional adoption, or universal applicability.

### Proposed Metadata-Only Correction

Apply to existing Resource only:

- `custodyStatus: source_custody_metadata_checked`
- `displayPolicy: show_warning`
- `learnerVisibleDefault: false`
- `warningFlags`:
  - `official_public_metadata_checked`
  - `metadata_only_no_source_truth_claim`
  - `protected_content_not_stored`
  - `reviewer_curated_only`
  - `transportation_geotechnical_scope_only`
  - `contextual_guidance_not_universal_requirement`
- `sourceOfContext`: bounded official FHWA public metadata check above.
- `sourceTruthCaveat`: public metadata checked only; not source truth, not complete design guidance, and not current/governing/compliance/AHJ.
- `rightsCaveat`: public U.S. government web page metadata and short rationale only; no protected payload stored and no rights clearance beyond public web access claimed.
- `protectedContentCaveat`: no protected content, PDF text, or full page payload stored.

### Proposed Link Decision

Decision: accept `nrl-retaining-wall-fhwa-needs-review`.

Rationale:

The Resource and node both specifically concern retaining/earth-retaining structures. The existing Resource already has source rights, admission provenance, public-web access, official FHWA locator, and explicit U.S. transportation/geotechnical scope. The accepted link would remain caveated as FHWA transportation/geotechnical guidance, not universal building-code guidance and not source truth.

Learner visibility:

- Do not manually set `learnerEligible`.
- Existing Resource Layer eligibility logic computes whether the accepted link appears in learner mode.
- The dry-run validation showed `resourcesAcceptedForLearner` would increase from 8 to 9 if accepted.

### Dry-Run Results

Metadata correction dry-run:

- validation: PASS
- blockers: none
- errors: none
- creates Resource: false
- creates nodeResourceLink: false
- learnerVisibleAfterApply: false
- graphMutationApplied: false
- canonicalMutationApplied: false

Link acceptance dry-run:

- validation: PASS
- blockers: none
- errors: none
- accepted link status would change from `needs_review` to `accepted`
- remaining warnings are unchanged ASCE/ACI standards-context warnings only
- no Resource creation
- no nodeResourceLink creation
- no graph/canonical mutation

### Review Request

Reviewer: `kimi_reviewer` using `kimi, version 1.41.0`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Requested verdict:

- `PASS_APPLY_FHWA_METADATA_AND_ACCEPT_LINK`
- `PASS_METADATA_ONLY_KEEP_LINK_NEEDS_REVIEW`
- `PASS_KEEP_AS_IS`
- `BLOCK_UNSAFE_METADATA`
- `BLOCK_LINK_OVERCLAIM`
- `NEEDS_PROJECT_OWNER_INPUT`

Questions:

1. Is the metadata-only FHWA caveat correction safe?
2. Is the official source check bounded and non-overclaiming?
3. Is the Retaining Wall link node-specific enough to accept?
4. Are rights/access sufficient for accepted-link eligibility?
5. Does any claim imply source truth, current/governing/compliance/AHJ, or universal applicability?
6. Should learner eligibility remain computed by existing logic rather than manually asserted?

### Delegated Review Result

Reviewer: `kimi_reviewer` using `kimi, version 1.41.0`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Verdict: `PASS_APPLY_FHWA_METADATA_AND_ACCEPT_LINK`.

Reviewer findings:

- The FHWA locator is official enough for metadata-only custody context.
- The source check was bounded to public metadata and did not store protected content.
- The Resource metadata correction is safe when caveated as public metadata only.
- The Retaining Wall link is node-specific enough for accepted-link review because both the Resource and target node concern retaining/earth-retaining structures.
- The accepted link must not imply universal building-code guidance, current/governing status, compliance, AHJ adoption, or source truth.
- Learner eligibility must remain computed by existing Resource Layer logic.

### Applied Decisions

Applied after dry-run and delegated review:

- Resource metadata correction manifest: `006_System-Manifests/resource-layer/transaction-manifests/resource-layer-tx-20260506165850-0c5168e0ce24.json`
- Link review decision manifest: `006_System-Manifests/resource-layer/transaction-manifests/resource-layer-tx-20260506165850-86af44e8fc4e.json`

Resource result:

- `res-fhwa-earth-retaining-structures` retained as an existing Resource.
- No Resource was created.
- `custodyStatus` set to `source_custody_metadata_checked`.
- `displayPolicy` set to `show_warning`.
- `learnerVisibleDefault` remains `false`.
- Caveats and warning flags now explicitly state public metadata only, no protected payload, no source-truth claim, no universal requirement, and FHWA transportation/geotechnical scope.

Link result:

- `nrl-retaining-wall-fhwa-needs-review` moved from `needs_review` to `accepted`.
- No nodeResourceLink was created.
- Learner eligibility was computed by existing Resource Layer logic; it was not manually forced.
- No graph, canonical, P0 Concrete/Reinforced Concrete, or high-risk P1 mutation occurred.

### Verification

Focused tests:

- `bun test api/resourceEvidencePath.test.ts`: PASS, 21 pass.
- `bun test api/resourceLayer.test.ts`: PASS, 43 pass.
- `bun test api/resourceLayerSourceVerification.test.ts`: PASS, 28 pass.
- `bun test api/resourceLayerExternalCandidates.test.ts`: PASS, 46 pass.
- `bun test api/resourceLayerExternalCandidateReview.test.ts`: PASS, 26 pass.
- `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts`: PASS, 56 pass.

Full validation and tests:

- `bun run api/validateResourceLayer.ts -- --no-write`: PASS; Resources 10, nodeResourceLinks 12, accepted links 9, needs_review links 2, blockers none.
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS; admitted relationships 266, base edges 13,670, effective edges 13,936, `CROSS_DOMAIN_EQUIVALENT` 0.
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS; latest Resource Layer manifest hashes match, blockers none.
- `cd api && bun test`: PASS; 433 pass.
- `cd explorer && bun test`: PASS; 121 pass.
- `cd explorer && bun run build`: PASS with existing Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: PASS; 118 pass.

### Remaining Work

- ASCE 7 and ACI 318 remain standards-context blocked.
- Two ASCE standard-like nodeResourceLinks remain `needs_review`.
- Ten source-family external metadata candidates remain `needs_review` and require exact official locators, source custody, and rights/access review before promotion.
- The newly accepted FHWA link needs evidence-backed graph potential review in a later packet; no graph edge was admitted in this unit.
