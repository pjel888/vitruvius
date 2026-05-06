# Phase 8C Delegated Locator Review Packet

This packet is for delegated external AI review. This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Baseline
- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates: 12
- Candidate statuses: 2 `duplicate_candidate`, 10 `needs_review`
- Learner exposure: none
- Graph/canonical/P0/high-risk P1 mutation: none

## Reviewer Availability
- CommandCode: unavailable
- Kimi: available (`1.41.0`)
- Claude: available but not selected because Kimi is preferred after CommandCode
- OpenCode: unavailable

## Source Locator Results
- Usable exact official locators: buildingSMART IFC, WBDG Fire Protection, Uniclass, OmniClass, RIBA Plan of Work, AIA Best Practices, ICE Structural Load Paths, U.S. Access Board Accessible Routes.
- Blocked exact locator checks: AISC Specification and IStructE Guidance returned official-domain 403 interstitials.
- Existing Resource overlap: ICE Structural Load Paths and U.S. Access Board Accessible Routes already have accepted Resources/links.

## Proposed Actions For Review

1. Persist `Industry Foundation Classes (IFC) - buildingSMART International` as reviewer-only candidate.
   - URL: `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/`
   - Source family: `buildingsmart`
   - Proposed status path: candidate -> source_custody_verified -> ready_for_promotion_review -> resource_and_links promotion.
   - Proposed link: `VTN-DOM-0000092` BIM Schemas, relation `explains`, link status `needs_review`.

2. Persist `Fire Protection | WBDG - Whole Building Design Guide` as reviewer-only candidate.
   - URL: `https://www.wbdg.org/do/secure/fire-protection`
   - Source family: `wbdg_nibs`
   - Proposed status path: candidate -> source_custody_verified -> ready_for_promotion_review -> resource_and_links promotion.
   - Proposed link: `VTN-DOM-0000056` Fire Protection, relation `provides_design_guidance`, link status `needs_review`.

3. Persist `Uniclass, delivered by NBS` as reviewer-only candidate.
   - URL: `https://uniclass.thenbs.com/`
   - Source family: `uniclass_nbs`
   - Proposed status path: candidate -> source_custody_verified -> ready_for_promotion_review -> resource_and_links promotion.
   - Proposed link: `VTN-DOM-0000093` Classification Systems, relation `provides_classification`, link status `needs_review`.

## Promotion Workflow Hardening

The existing external candidate promotion code previously wrote `admissionProvenance.admittedBy: 'human'` and link `verifiedBy: 'human'` for delegated AI promotion. Phase 8C changes this to map `kimi_reviewer` to `kimi`, `script` to `script`, explicit `project_owner_human_reviewer` to `human`, and Codex/default to `codex`. This prevents fake biological human review records.

## Questions For Reviewer
1. Are the proposed locators official enough?
2. Are any metadata values invented?
3. Are the proposed source-family matches accurate?
4. Are the proposed node links specific enough, or too generic?
5. Is it safe to persist the three reviewer-only candidates?
6. Is it safe to mark them source-custody verified based on official URL reachability plus public metadata and rights/access caveats?
7. Is it safe to mark them ready for promotion review?
8. Is it safe to create reviewer-only Resources and `needs_review` nodeResourceLinks for only the listed nodes?
9. Is the reviewer identity hardening correct?
10. What must remain blocked?

## Required Verdict
One of:
- `PASS_RESOURCE_AND_LINKS_FOR_LISTED_CANDIDATES`
- `PASS_RESOURCE_ONLY_FOR_LISTED_CANDIDATES`
- `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`
- `PASS_APPLY_SAFE_STATUS_DECISIONS`
- `BLOCK_UNSAFE_LOCATORS`
- `BLOCK_MISSING_METADATA`
- `NEEDS_PROJECT_OWNER_INPUT`
