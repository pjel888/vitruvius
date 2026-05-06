# Phase 8E Resource Metadata Correction Packet

Date: 2026-05-06

Reviewer caveat required:

> This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Proposed Correction Scope

Allowed:

- Final URL/canonical URL corrections from bounded official public checks.
- `lastCheckedAt` populated from the bounded check.
- `verificationStatus` changed only to `link_verified` if interpreted narrowly as locator/public metadata checked.
- `custodyStatus` changed to `source_custody_metadata_checked`.
- `sourceOfContext`, `sourceTruthCaveat`, `rightsCaveat`, and warning flags updated with public-metadata-only caveats.
- `learnerVisibleDefault` remains `false`.

Forbidden:

- No source truth claim.
- No current/governing/compliance/AHJ claim.
- No protected content claim.
- No Resource creation.
- No new nodeResourceLink creation.
- No graph/canonical mutation.
- No manual `learnerEligible=true`.

## Candidate Corrections

### buildingSMART IFC

- Resource: `res_9c586758-66e4-46f2-b62a-8720db1c0976`.
- Link: `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7`.
- Proposed URL: `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/`.
- Proposed canonical URL: `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/`.
- Proposed `lastCheckedAt`: Phase 8E bounded check timestamp.
- Proposed verification status: `link_verified`, meaning public locator/title metadata checked only.
- Proposed custody status: `source_custody_metadata_checked`.
- Proposed caveat: public landing metadata only; no IFC schema payload ingested; not source truth.
- Link retry proposal: accept only if Resource metadata correction preview validates and delegated reviewer confirms relation/rationale are node-specific and rights/access are sufficient.

### WBDG Fire Protection

- Resource: `res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40`.
- Link: `nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485`.
- Proposed URL: `https://www.wbdg.org/do/secure/fire-protection`.
- Proposed canonical URL: `https://www.wbdg.org/do/secure/fire-protection`.
- Proposed `lastCheckedAt`: Phase 8E bounded check timestamp.
- Proposed verification status: `link_verified`, meaning public locator/title metadata checked only.
- Proposed custody status: `source_custody_metadata_checked`.
- Proposed caveat: public page metadata only; not a fire-code, governing, compliance, or AHJ claim.
- Link retry proposal: accept only if Resource metadata correction preview validates and delegated reviewer confirms relation/rationale are node-specific and WBDG remains contextual guidance, not governing authority.

### Uniclass

- Resource: `res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c`.
- Link: `nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477`.
- Proposed URL: `https://uniclass.thenbs.com/`.
- Proposed canonical URL: `https://uniclass.thenbs.com/`.
- Proposed `lastCheckedAt`: Phase 8E bounded check timestamp.
- Proposed verification status: `link_verified`, meaning public locator/title metadata checked only.
- Proposed custody status: `source_custody_metadata_checked`.
- Proposed caveat: public page metadata only; not jurisdictional adoption, universal authority, or source truth.
- Link retry proposal: accept only if Resource metadata correction preview validates and delegated reviewer confirms relation/rationale are node-specific and rights/access are sufficient.

## Questions for Delegated Reviewer

1. Are the locator corrections official and safe?
2. Is `lastCheckedAt` appropriate for these bounded public checks?
3. Is `source_custody_metadata_checked` safe, or too strong?
4. Is `link_verified` safe if scoped to locator/public metadata only?
5. Are any metadata fields invented?
6. Are rights/access caveats sufficient?
7. Can any backing link now be accepted after preview validation?
8. Should any link remain `needs_review`, move to a more precise blocker, or be rejected/deferred?
