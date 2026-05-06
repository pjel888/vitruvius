# Full Autopilot Source Locator Discovery

Date: 2026-05-07 local

Scope: ten `needs_review` source-family external metadata candidates in `006_System-Manifests/resource-layer/external-metadata-candidates.json`.

Method:

- Official/public source-family domains only.
- Existing Resource Layer controlled source-check workflow.
- HEAD first, bounded GET only for public metadata.
- Timeout: 10 seconds per request.
- Body cap: 1 MB.
- No full page content stored.
- No protected standards content, PDF payload, DOI lookup, ISBN lookup, source-truth verification, current/governing/compliance/AHJ claim, or learner-trust claim.

## Results

| Candidate | Source family | Requested URL | Result | Public title / metadata | Recommended action |
|---|---|---|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | `buildingsmart` | `https://www.buildingsmart.org/standards/` | HTTP 200, official family match | `Solutions and Standards - buildingSMART International` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | `aisc` | `https://www.aisc.org/` | HTTP 200, official family match | `AISC Home Page` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | `aia` | `https://www.aia.org/` | HTTP 200, official family match | `AIA Home` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | `us_access_board` | `https://www.access-board.gov/` | HTTP 200, official family match | `U.S. Access Board - U.S. Access Board - Home` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | `wbdg_nibs` | `https://www.wbdg.org/` | HTTP 200, official family match | `WBDG Home | WBDG - Whole Building Design Guide` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | `istructe` | `https://www.istructe.org/` | HTTP 200, official family match | `Home` | Safe to record locator and move to `source_custody_in_review`; title is generic, so do not claim source truth beyond reachability/public metadata. |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | `ice` | `https://knowledgehub.ice.org.uk/` | HTTP 200, official family match | `ICE Knowledge Hub | Institution of Civil Engineers` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | `riba` | `https://www.architecture.com/knowledge-and-resources` | Redirected to `https://www.riba.org/news/`; current controlled verifier allow-list does not include `riba.org` | No safe public title captured under the current controlled family match | Keep blocked pending source-family domain review; do not update status from `needs_review`. |
| `ext-cand-uniclass-nbs-source-family-reference-motq601s-0s68` | `uniclass_nbs` | `https://uniclass.thenbs.com/` | HTTP 200, official family match | `Uniclass, delivered by NBS` | Safe to record locator and move to `source_custody_in_review`. |
| `ext-cand-omniclass-csi-source-family-reference-motq602f-ktvr` | `omniclass_csi` | `https://www.csiresources.org/standards/omniclass/standards-omniclass-about` | HTTP 200, official family match | `About OmniClass® - Construction Specifications Institute` | Safe to record locator and move to `source_custody_in_review`. |

## Caveats

- These checks only establish bounded URL reachability and public response metadata under the configured official source-family domains.
- They do not verify source truth, currentness, governing status, compliance status, AHJ adoption, edition/version, DOI/ISBN, rights clearance, or learner trust.
- The source-family candidates remain reviewer-only, no-auto-promotion, no-auto-linking, and no learner exposure.
- Resource-only promotion is still blocked for these source-family references unless a later gate proves a concrete Resource target, non-duplicate value, source custody, rights/access caveats, and node relevance.

## Proposed Safe Batch

Apply metadata-only corrections and source-custody status decisions for the nine passing candidates:

- Add `proposedUrl` from the checked official URL.
- Preserve `proposedSourceFamilyId`.
- Preserve `proposedRightsStatus=source_family_metadata_only`.
- Preserve `verificationStatus=unverified`.
- Preserve `displayPolicy=reviewer_only`.
- Preserve `learnerVisible=false`.
- Move `needs_review -> source_custody_in_review`.
- Create no Resources.
- Create no nodeResourceLinks.
- Perform no graph/canonical mutation.

RIBA remains blocked with exact blocker: checked locator redirects to `riba.org`, which is not currently in the controlled RIBA source-family allow-list.

## Apply Outcome

Applied after Kimi delegated review:

- Nine candidates received the checked `proposedUrl`.
- Nine candidates moved from `needs_review` to `source_custody_in_review`.
- RIBA remained `needs_review`.
- Resources remained 10.
- nodeResourceLinks remained 12.
- External candidates remained 15.
- Learner-visible external candidates remained 0.
- No Resource was created.
- No nodeResourceLink was created.
- No graph/canonical mutation occurred.

Latest Resource Layer custody manifest for the candidate registry: `resource-layer-tx-20260506174041-de14347bbb09`.

Validation note: an initial attempt to run mutable candidate-focused test files in parallel caused fixture registry races. The registry was restored to `HEAD`, stale untracked manifests from that interrupted attempt were removed, the Kimi-approved batch was reapplied, and the focused suites were rerun sequentially. Canonical stewardship then confirmed the latest manifest afterHash matched the candidate registry.
