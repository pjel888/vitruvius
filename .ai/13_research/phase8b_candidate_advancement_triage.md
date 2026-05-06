# Phase 8B Candidate Advancement Triage

Checked at: 2026-05-06T17:10:32.7077958+08:00

## Summary

The registry contains 12 external metadata candidates. Two candidates have exact URL metadata and already correspond to existing production Resource records. Ten source-family reference candidates contain source-family/domain metadata only and lack exact source locators, URL/DOI/ISBN, stable identifiers, proposed nodes, and proposed relations.

No candidate is currently safe for new Resource creation or nodeResourceLink creation without either duplicating existing Resource records or inventing missing source metadata.

## Candidate Table

| candidateId | title | status | source locator | proposed nodes/relation | classification | exact blocker | recommended action |
|---|---|---:|---|---|---|---|---|
| `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` | ASCE 7: Minimum Design Loads and Associated Criteria for Buildings and Other Structures | `standards_context_in_review` | `https://asce.org/asce-7` | `VTN-DOM-0012777`, `VTN-DOM-0012778`; `is_supplementary_reference_for` | `blocked_missing_standard_context`, `duplicate_existing_resource` | Missing edition, version/year, scope, jurisdiction/applicability caveat; existing Resource `res-asce-7-official-landing`; existing needs-review nodeResourceLinks. | Mark duplicate of existing Resource if delegated reviewer approves. Do not promote or link. |
| `ext-cand-earth-retaining-structures-mosyi54y-jp9m` | Earth Retaining Structures | `source_custody_in_review` | `https://fhwa.dot.gov/engineering/geotech/retaining` | `VTN-DOM-0012799`; `provides_design_guidance` | `source_custody_can_advance`, `duplicate_existing_resource` | Official FHWA page can be checked and repo-local rights/access context exists on existing Resource `res-fhwa-earth-retaining-structures`; candidate duplicates that Resource and existing needs-review nodeResourceLink. | Prefer duplicate disposition over creating a second Resource. Do not promote or link. |
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | buildingSMART International Source Family Reference | `needs_review` | none; domains only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | American Institute of Steel Construction Source Family Reference | `needs_review` | none; domain only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | American Institute of Architects Source Family Reference | `needs_review` | none; domain only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | U.S. Access Board Source Family Reference | `needs_review` | none; domain only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | Whole Building Design Guide / NIBS Source Family Reference | `needs_review` | none; domains only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | Institution of Structural Engineers Source Family Reference | `needs_review` | none; domain only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | Institution of Civil Engineers Source Family Reference | `needs_review` | none; domains only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | Royal Institute of British Architects Source Family Reference | `needs_review` | none; domain only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-uniclass-nbs-source-family-reference-motq601s-0s68` | Uniclass / NBS Source Family Reference | `needs_review` | none; domains only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review; source family is not a primary rule source. | Keep blocked; needs project-owner/source metadata. |
| `ext-cand-omniclass-csi-source-family-reference-motq602f-ktvr` | OmniClass / CSI Source Family Reference | `needs_review` | none; domains only | none | `blocked_missing_metadata` | Missing exact URL/source locator, stable identifier, rights/access context, node target, relation, and source custody review; source family is not a primary rule source. | Keep blocked; needs project-owner/source metadata. |

## Gate Probes

No-write promotion preview results:

- ASCE 7: blocked by status `standards_context_in_review`, missing edition/version or jurisdiction/scope, and incomplete standards context.
- FHWA Earth Retaining Structures: blocked by status `source_custody_in_review` for promotion preview. A no-write hypothetical ready-state apply probe passed code gates, but it would create a duplicate semantic Resource because `res-fhwa-earth-retaining-structures` already exists.
- All 10 source-family references: blocked by status `needs_review` and source metadata gate failure (`no URL, DOI, or ISBN`).

## Safe Action Assessment

- New Resource creation: blocked.
- New nodeResourceLink creation: blocked.
- Graph/node/edge admission: blocked because no new Resource/link action is safe and existing links remain needs-review due context caveats.
- Candidate status decision: safe to ask delegated reviewer whether ASCE/FHWA should be marked `duplicate_candidate` of their existing Resource records.
