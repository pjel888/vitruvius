# Full Autopilot Candidate Review Decisions

Date: 2026-05-07 local

Current unit: source-family locator discovery and source-custody advancement for ten `needs_review` candidates.

## Proposed Reviewer Packet

Reviewer identity requested: `kimi_reviewer` (`kimi, version 1.41.0`).

Required review caveat:

> This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Questions for reviewer:

1. Are the nine HTTP 200 official-family locator checks safe to persist as candidate `proposedUrl` corrections?
2. Is `source_custody_in_review` truthful for the nine passing candidates, given that only URL reachability and public metadata were checked?
3. Should any of the nine passing candidates remain `needs_review` because the locator is too broad or metadata is too weak?
4. Should RIBA remain blocked until a separate source-family domain review handles the `architecture.com -> riba.org` redirect?
5. Are any source metadata, rights, current/governing/compliance/AHJ, DOI/ISBN, standards edition/version, or learner-trust claims overbroad?
6. Is it safe to apply the proposed metadata-only/status-only batch with Resource Layer transaction manifests and no Resource/link/graph creation?

## Proposed Decisions

| Candidate | Proposed metadata correction | Proposed status | Resource/link/graph action | Rationale |
|---|---|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | `proposedUrl=https://www.buildingsmart.org/standards/` | `source_custody_in_review` | None | Official buildingSMART page returned HTTP 200 and public title. |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | `proposedUrl=https://www.aisc.org/` | `source_custody_in_review` | None | Official AISC domain returned HTTP 200 and public title. |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | `proposedUrl=https://www.aia.org/` | `source_custody_in_review` | None | Official AIA domain returned HTTP 200 and public title. |
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | `proposedUrl=https://www.access-board.gov/` | `source_custody_in_review` | None | Official U.S. Access Board domain returned HTTP 200 and public title. |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | `proposedUrl=https://www.wbdg.org/` | `source_custody_in_review` | None | Official WBDG domain returned HTTP 200 and public title. |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | `proposedUrl=https://www.istructe.org/` | `source_custody_in_review` | None | Official IStructE domain returned HTTP 200; title is generic, so only metadata reachability is claimed. |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | `proposedUrl=https://knowledgehub.ice.org.uk/` | `source_custody_in_review` | None | Official ICE Knowledge Hub domain returned HTTP 200 and public title. |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | None | Keep `needs_review` | None | Checked Architecture.com locator redirects to `riba.org`, outside the current controlled RIBA allow-list. |
| `ext-cand-uniclass-nbs-source-family-reference-motq601s-0s68` | `proposedUrl=https://uniclass.thenbs.com/` | `source_custody_in_review` | None | Official Uniclass/NBS domain returned HTTP 200 and public title. |
| `ext-cand-omniclass-csi-source-family-reference-motq602f-ktvr` | `proposedUrl=https://www.csiresources.org/standards/omniclass/standards-omniclass-about` | `source_custody_in_review` | None | Official CSI Resources OmniClass page returned HTTP 200 and public title. |

## Blockers Preserved

- No candidate in this batch is ready for Resource-only promotion.
- No candidate in this batch has node-specific Resource link rationale.
- No candidate in this batch has accepted-link eligibility.
- No standards context is completed.
- No graph/canonical mutation is proposed.
- No learner exposure is proposed.

## Applied Decisions

Applied after Kimi verdict `PASS_APPLY_SAFE_STATUS_DECISIONS`.

| Candidate | Final status | URL persisted | Latest status decision manifest |
|---|---|---|---|
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | `source_custody_in_review` | `https://www.buildingsmart.org/standards/` | `resource-layer-tx-20260506173939-60be464ec753` |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | `source_custody_in_review` | `https://www.aisc.org/` | `resource-layer-tx-20260506173939-b8b42a751830` |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | `source_custody_in_review` | `https://www.aia.org/` | `resource-layer-tx-20260506173940-8553bb29980c` |
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | `source_custody_in_review` | `https://www.access-board.gov/` | `resource-layer-tx-20260506173940-140ffe7ffed1` |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | `source_custody_in_review` | `https://www.wbdg.org/` | `resource-layer-tx-20260506173941-8bc8afcaa429` |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | `source_custody_in_review` | `https://www.istructe.org/` | `resource-layer-tx-20260506174036-13b586295954` |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | `source_custody_in_review` | `https://knowledgehub.ice.org.uk/` | `resource-layer-tx-20260506174036-9729ae6b1878` |
| `ext-cand-uniclass-nbs-source-family-reference-motq601s-0s68` | `source_custody_in_review` | `https://uniclass.thenbs.com/` | `resource-layer-tx-20260506174038-fd6d5d931117` |
| `ext-cand-omniclass-csi-source-family-reference-motq602f-ktvr` | `source_custody_in_review` | `https://www.csiresources.org/standards/omniclass/standards-omniclass-about` | `resource-layer-tx-20260506174041-de14347bbb09` |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | `needs_review` | none | none; blocked by controlled-domain redirect to `riba.org` |

Safety outcome:

- `verificationStatus` remains `unverified`.
- `displayPolicy` remains `reviewer_only`.
- `learnerVisible` remains `false`.
- No `source_custody_verified` status was asserted.
- No rights clearance, source-truth, current, governing, compliance, AHJ, DOI/ISBN, edition/version, publication-date, or learner-trust claim was asserted.

## RIBA Follow-Up Decision

Reviewer identity: `kimi_reviewer` (`kimi, version 1.41.0`).

Reviewer caveat:

> This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Kimi verdict: `PASS_APPLY_SAFE_STATUS_DECISIONS`.

Applied decision:

| Candidate | Prior status | Final status | Requested URL | Latest status decision manifest | Resource/link/graph action |
|---|---|---|---|---|---|
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | `needs_review` | `source_custody_in_review` | `https://www.riba.org/` | `resource-layer-tx-20260506175937-8e8a8996ae50` | None |

Safety outcome:

- `verificationStatus` remains `unverified`.
- `displayPolicy` remains `reviewer_only`.
- `learnerVisible` remains `false`.
- No `source_custody_verified` status was asserted.
- The candidate still has missing field `url` in the decision preview because the standard source-verification decision records the checked URL in decision history rather than mutating `proposedUrl`.
- No Resource, nodeResourceLink, promotion, graph/canonical mutation, learner exposure, rights clearance, source-truth, current, governing, compliance, AHJ, DOI/ISBN, edition/version, or publication-date claim was asserted.
