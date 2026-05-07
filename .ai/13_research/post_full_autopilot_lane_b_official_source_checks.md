# Post-Full Autopilot Lane B Official Source Checks

Date: 2026-05-07

Domain: site/civil drainage.

Limits used: official domains only, HEAD first, bounded public GET metadata only, 10 second timeout, maximum 1 MB body inspection, no protected payload, no full PDF ingestion, no learner-trust or source-truth claim.

## Candidate Checks

| Candidate | Requested URL | Final URL | Status | Content type | Official family match | Public metadata | Caveats |
|---|---|---|---:|---|---|---|---|
| FHWA HEC-22 Urban Drainage Design Manual | `https://www.fhwa.dot.gov/engineering/hydraulics/library_arc.cfm?id=189&pub_number=22` | same | 200 | `text/html;charset=UTF-8` | true (`fhwa`) | Page title: `Publications - Hydraulics - Bridges & Structures - Federal Highway Administration`; public page heading observed for `Urban Drainage Design Manual Fourth Edition`; publication number `HIF-24-006`; publication year `2024`. | HTTP success is not source truth; no current/governing/AHJ/compliance/design-adequacy claim. |
| WBDG Low Impact Development Technologies | `https://www.wbdg.org/resources/low-impact-development-technologies` | same | 200 | `text/html; charset=UTF-8` | true (`wbdg_nibs`) | Page title: `Low Impact Development Technologies | WBDG - Whole Building Design Guide`. | HTTP success is not source truth; no current/governing/AHJ/compliance/design-adequacy claim. |

## Notes

- The FHWA PDF endpoint was checked by HEAD only and identified as `application/pdf`; no PDF payload was downloaded or stored.
- WBDG exact checked locator includes `www.wbdg.org`. The existing candidate-normalization helper canonicalizes `www.` out of `proposedUrl`; the exact requested and final checked URL is preserved in the source verification decision history.
- No Resources, nodeResourceLinks, graph edges, graph nodes, canonical aliases, redirects, tombstones, or learner-visible items were created by these checks.
