# Phase 8C Official Source Locator Discovery

Bounded checks used official/public domains only, 10s timeout, HEAD first, GET only for public metadata/title, no protected payload storage, no full PDF extraction.

| Family | Requested URL | Final URL | Status | Content type | Title/public metadata | Result |
|---|---|---|---:|---|---|---|
| `buildingsmart` | `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/` | same | HEAD 200 / bounded GET 206 | `text/html; charset=UTF-8` | `Industry Foundation Classes (IFC) - buildingSMART International` | usable official locator |
| `wbdg_nibs` | `https://www.wbdg.org/do/secure/fire-protection` | same | 200 | `text/html; charset=UTF-8` | `Fire Protection | WBDG - Whole Building Design Guide` | usable official locator |
| `uniclass_nbs` | `https://uniclass.thenbs.com/` | same | 200 | `text/html; charset=utf-8` | `Uniclass, delivered by NBS` | usable official locator |
| `omniclass_csi` | `https://www.csiresources.org/standards/omniclass` | same | 200 | `text/html; charset=utf-8` | `OmniClass® - Construction Specifications Institute` | usable official locator, deferred from first apply batch |
| `riba` | `https://www.architecture.com/knowledge-and-resources/resources-landing-page/riba-plan-of-work` | `https://www.riba.org/work/insights-and-resources/riba-plan-of-work/` | 200 | `text/html; charset=utf-8` | `RIBA Plan of Work` | usable official locator, deferred for missing exact node rationale |
| `aia` | `https://www.aia.org/aia-best-practices` | same | 200 | `text/html; charset=UTF-8` | `AIA Best Practices | AIA` | usable official locator, deferred for missing exact node rationale |
| `istructe` | `https://www.istructe.org/resources/guidance/` | same | 403 | `text/html; charset=UTF-8` | `Just a moment...` | blocked by interstitial |
| `ice` | `https://knowledgehub.ice.org.uk/cpd/delivery-exc/structural-load-paths/` | same | HEAD 200 / bounded GET 206 | `text/html; charset=UTF-8` | `Explainer: Structural load paths` | existing Resource/link already covers this |
| `us_access_board` | `https://www.access-board.gov/ada/guides/chapter-4-accessible-routes/` | same | 200 | `text/html; charset=utf-8` | `Chapter 4: Accessible Routes` | existing Resource/link already covers this |
| `aisc` | `https://www.aisc.org/Specification` | same | 403 | `text/html; charset=UTF-8` | `Just a moment...` | blocked by interstitial |

## Selected Candidate Actions

1. Persist `Industry Foundation Classes (IFC) - buildingSMART International` as reviewer-only external URL candidate, then source-custody review and promote with a needs-review link to `VTN-DOM-0000092` (`BIM Schemas`) if reviewer approves.
2. Persist `Fire Protection | WBDG - Whole Building Design Guide` as reviewer-only external URL candidate, then source-custody review and promote with a needs-review link to `VTN-DOM-0000056` (`Fire Protection`) if reviewer approves.
3. Persist `Uniclass, delivered by NBS` as reviewer-only external URL candidate, then source-custody review and promote with a needs-review link to `VTN-DOM-0000093` (`Classification Systems`) if reviewer approves.

## Not Selected
- AISC and IStructE: official domains but bounded checks returned 403 interstitials.
- RIBA and AIA: official pages found, but node rationale was not strong enough for this batch.
- OmniClass: official locator found, but deferred to keep this first advancement batch small and avoid two classification links in one wave.
