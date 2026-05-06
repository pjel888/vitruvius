# Phase 8D Link Source Context Recheck

Run date: 2026-05-06

## Method

Bounded official public metadata checks only:

- HEAD first.
- GET only for bounded public HTML metadata/title inspection.
- Timeout: 10 seconds per request.
- Redirects: max 5.
- Body inspected: max 1 MB.
- No full content stored.
- No protected payload stored.
- No compliance, current, governing, AHJ, or source-truth claim made.

## Results

| Link | Requested URL | Final URL | HTTP status | Content type | Public title | Official domain match | Source family match | Protected content avoided | Accepted-link readiness |
|---|---|---|---:|---|---|---|---|---|---|
| buildingSMART IFC -> BIM Schemas | `https://buildingsmart.org/standards/bsi-standards/industry-foundation-classes` | `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/` | 200 | `text/html; charset=UTF-8` | `Industry Foundation Classes (IFC) - buildingSMART International` | yes | yes | yes | Not ready: backing Resource is unverified and missing `lastCheckedAt` |
| WBDG Fire Protection -> Fire Protection | `https://wbdg.org/do/secure/fire-protection` | `https://www.wbdg.org/` | 200 | `text/html; charset=UTF-8` | `WBDG Home | WBDG - Whole Building Design Guide` | yes | partial | yes | Not ready: stored URL redirects to home; exact `www` locator resolves separately; backing Resource is unverified and missing `lastCheckedAt` |
| WBDG exact locator check | `https://www.wbdg.org/do/secure/fire-protection` | `https://www.wbdg.org/do/secure/fire-protection` | 200 | `text/html; charset=UTF-8` | `Fire Protection | WBDG - Whole Building Design Guide` | yes | yes | yes | Source locator correction is needed before acceptance |
| Uniclass -> Classification Systems | `https://uniclass.thenbs.com/` | `https://uniclass.thenbs.com/` | 200 | `text/html; charset=utf-8` | `Uniclass, delivered by NBS` | yes | yes | yes | Not ready: backing Resource is unverified and missing `lastCheckedAt` |

## Caveats

- HTTP success confirms reachability only within the bounded check; it does not establish source truth.
- Page titles are public metadata only.
- No protected specifications, standards, classification payloads, or WBDG content were stored.
- WBDG requires a locator correction from the stored non-`www` URL to the exact `www` URL before accepted-link review can be reconsidered.
- None of the three links currently passes accepted-link validation because their Resources remain `verificationStatus: unverified` and lack `lastCheckedAt`.

## Recommended Statuses For Review Packet

| Link | Recommended status | Reason |
|---|---|---|
| buildingSMART IFC -> BIM Schemas | `needs_review` | Official public metadata page matches, but Resource verification is still unverified and accepted-link validation blocks. |
| WBDG Fire Protection -> Fire Protection | `needs_review` | Stored locator redirects to home; exact official locator exists but Resource metadata correction and verification are not part of this acceptance step. |
| Uniclass -> Classification Systems | `needs_review` | Official public metadata page matches, but Resource verification is still unverified and accepted-link validation blocks. |
