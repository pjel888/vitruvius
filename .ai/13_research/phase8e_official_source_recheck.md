# Phase 8E Bounded Official Source Recheck

Date: 2026-05-06

Method:

- Official locators only.
- `HEAD` first with `curl.exe -I -L --max-time 10 --max-redirs 5`.
- Bounded `GET` title check with `curl.exe -L --max-time 10 --max-redirs 5 -r 0-1048575`.
- Full page payloads were not stored.
- Protected content was not downloaded or stored.
- These checks verify public locator metadata only; they do not establish source truth, full content correctness, current/governing status, compliance status, AHJ adoption, or learner trust.

## Results

| Resource | Requested URL | Final URL | HTTP | Content Type | Public Title | Redirects | Body chars inspected | Official/source-family match | Caveat |
| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| buildingSMART IFC | `https://buildingsmart.org/standards/bsi-standards/industry-foundation-classes` | `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/` | 200 | `text/html; charset=UTF-8` | `Industry Foundation Classes (IFC) - buildingSMART International` | 1 | 127,802 | Matches `buildingsmart` source-family domains | Public landing metadata only; no IFC specification payload ingested. |
| WBDG Fire Protection | `https://www.wbdg.org/do/secure/fire-protection` | `https://www.wbdg.org/do/secure/fire-protection` | 200 | `text/html; charset=UTF-8` | `Fire Protection | WBDG - Whole Building Design Guide` | 0 | 78,782 | Matches `wbdg_nibs` source-family domains | Public page metadata only; not a fire-code compliance or authority claim. |
| Uniclass | `https://uniclass.thenbs.com/` | `https://uniclass.thenbs.com/` | 200 | `text/html; charset=utf-8` | `Uniclass, delivered by NBS` | 0 | 37,166 | Matches `uniclass_nbs` source-family domains | Public page metadata only; not a jurisdictional adoption or universal-authority claim. |

## Recommended Metadata Corrections for Review

- buildingSMART IFC:
  - Correct canonical URL to the final HTTPS URL with `www` and trailing slash.
  - Set `lastCheckedAt` to the Phase 8E bounded check timestamp.
  - Move from `unverified` to `link_verified` only if delegated reviewer agrees this means locator/public metadata checked, not source truth.
  - Keep `learnerVisibleDefault=false`.

- WBDG Fire Protection:
  - Correct stored URL and canonical URL to `https://www.wbdg.org/do/secure/fire-protection`.
  - Set `lastCheckedAt` to the Phase 8E bounded check timestamp.
  - Move from `unverified` to `link_verified` only if delegated reviewer agrees this means locator/public metadata checked, not code/fire-safety truth.
  - Keep `learnerVisibleDefault=false`.

- Uniclass:
  - Keep URL `https://uniclass.thenbs.com/`.
  - Set canonical URL to the same official locator if needed.
  - Set `lastCheckedAt` to the Phase 8E bounded check timestamp.
  - Move from `unverified` to `link_verified` only if delegated reviewer agrees this means locator/public metadata checked, not adoption or classification authority truth.
  - Keep `learnerVisibleDefault=false`.
