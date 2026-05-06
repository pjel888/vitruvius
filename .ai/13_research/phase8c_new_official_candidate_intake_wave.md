# Phase 8C New Official Candidate Intake Wave

## Proposed Reviewer-Only Candidates

| Proposed title | Candidate type | Source family | Official URL | Rights/access caveat | Proposed node link | Rationale |
|---|---|---|---|---|---|---|
| Industry Foundation Classes (IFC) - buildingSMART International | `external_url_candidate` | `buildingsmart` | `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/` | Public official landing/metadata page; no standard payload copied | `VTN-DOM-0000092` BIM Schemas, `explains` | IFC is a buildingSMART schema/data standard family and directly explains BIM schema context. |
| Fire Protection \| WBDG - Whole Building Design Guide | `external_url_candidate` | `wbdg_nibs` | `https://www.wbdg.org/do/secure/fire-protection` | Public WBDG guidance page; no article payload copied into registry | `VTN-DOM-0000056` Fire Protection, `provides_design_guidance` | WBDG Fire Protection is official design guidance for fire-protection design context. |
| Uniclass, delivered by NBS | `external_url_candidate` | `uniclass_nbs` | `https://uniclass.thenbs.com/` | Public classification landing page; no classification tables ingested | `VTN-DOM-0000093` Classification Systems, `provides_classification` | Uniclass is an official NBS classification system landing page relevant to construction classification systems. |

## Defaults Required If Persisted
- `verificationStatus=unverified`
- `displayPolicy=reviewer_only`
- `learnerVisible=false`
- `reviewRequired=true`
- `noAutoVerification=true`
- `noAutoPromotion=true`
- `noAutoLinking=true`
- `noLearnerExposure=true`

## Safety Notes
- These candidates are not source truth.
- Controlled URL checks do not imply learner trust.
- Resource promotion, if later applied, remains reviewer-only and unverified.
- Link status must default to `needs_review`.
