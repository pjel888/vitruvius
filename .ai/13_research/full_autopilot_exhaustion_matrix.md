# Full Autopilot Exhaustion Matrix

Date: 2026-05-07 local

Scope: final exhaustion check for the full evidence, Resource, link, graph, visual, and quality autopilot loop.

## Exhaustion Summary

| Workstream | Status | Evidence | Remaining blocker |
|---|---|---|---|
| Candidate review | Exhausted for safe autonomous scope | 15 external candidates inspected; statuses now 2 `duplicate_candidate`, 10 `source_custody_in_review`, 3 `ready_for_promotion_review` already represented by promoted Resources and accepted links | Broad source-family candidates are not concrete Resource targets and lack rights/access, promotion status, node-specific rationale, and accepted-link gates |
| Source locator discovery | Exhausted for safe autonomous scope | Ten source-family candidates received bounded official public metadata checks; RIBA follow-up reviewed `architecture.com -> riba.org`; ASCE/ACI public landing metadata rechecked | No further official public metadata check can safely supply rights clearance, source truth, protected standard context, or node-specific promotion evidence |
| Standards context | Blocked | ASCE and ACI public pages checked metadata-only; Resource validator still warns about missing standards context | Missing complete edition/version/scope/applicability/section context without protected standard ingestion or invented current/governing/AHJ claims |
| Resource promotion | Exhausted for safe autonomous scope | Existing 3 ready candidates were already promoted in Phase 8C; current loop created no duplicate Resources | 10 source-family candidates are source-family references, not Resource-specific promotion candidates |
| nodeResourceLink creation | Exhausted for safe autonomous scope | Existing Resource/node links inspected; FHWA existing link accepted; no unlinked Resource has safe node-specific rationale available | Standards links remain blocked; source-family candidates are not Resources and have no node-specific relation |
| Accepted-link review | Exhausted for safe autonomous scope | FHWA retaining wall link accepted; accepted count 8 -> 9; remaining needs_review links are ASCE standards-context blocked; ACI link remains rejected | ASCE/ACI missing standard context; no safe learner-trust or acceptance claim |
| Node metadata | Exhausted for safe autonomous scope | Accepted Resource-backed opportunities inspected; no non-destructive node metadata change passed without overclaim or duplication | Available evidence is Resource Layer context only, not a source-backed node metadata mutation |
| Graph edges | Exhausted for safe autonomous scope | Existing Phase 8F/8G graph edges preserved; FHWA and all accepted links reviewed for graph potential | Remaining candidates duplicate existing semantics, overclaim metadata-only evidence, or require standards context |
| Explorer/NodeInspector | Applied and exhausted for current safe gaps | Badge false-positive fixed; NodeInspector and ResourceReviewAdmin now surface Resource caveats and checked dates; INFORMS filter regression added | Browser-level visual screenshots can be added later if product UX scope requires it, but no current safety gap remains |
| Quality/validation | Complete | Resource, graph, canonical validators pass; API 434 pass; Explorer 122 pass; Explorer build pass; Python KG 118 pass | Final delegated review pending at report creation time |

## Candidate Exhaustion

| Candidate group | Count | Final disposition |
|---|---:|---|
| Duplicate candidates | 2 | ASCE 7 duplicates existing ASCE Resource; FHWA retaining-wall candidate duplicates existing FHWA Resource. No duplicate Resource should be created. |
| Ready-for-promotion candidates | 3 | buildingSMART IFC, WBDG Fire Protection, and Uniclass already have reviewer-only Resources and accepted nodeResourceLinks from earlier Phase 8 work. No duplicate promotion is safe. |
| Source-family references | 10 | All are `source_custody_in_review`; each is broad source-family metadata, not a concrete Resource target. Promotion remains blocked by missing Resource-specific target, rights/access review, and node-specific rationale. |

## Resource Exhaustion

| Resource group | Count | Final disposition |
|---|---:|---|
| Public-web accepted Resources with caveats | 5 | FHWA accepted during this loop; four older accepted public-web Resources received metadata-only caveat standardization in Phase 8H. No further safe correction identified. |
| Reviewer-only accepted Resources | 3 | buildingSMART IFC, WBDG Fire Protection, and Uniclass have metadata-only custody checked and accepted links. No graph overclaim. |
| Standards Resources | 2 | ASCE 7 and ACI 318 remain not learner-trusted; standards context incomplete. |

## Link Exhaustion

| Link class | Count | Final disposition |
|---|---:|---|
| Accepted links | 9 | Learner eligibility is computed by existing Resource Layer logic. |
| needs_review links | 2 | ASCE standard-like links remain blocked by missing real standards context. |
| rejected links | 1 | ACI 318 / Structural Column remains rejected or not learner-trusted. |

## Graph Exhaustion

Safe graph growth already admitted before this final loop:

- `BIM Schemas INFORMS IFC Exchange`
- `Structural Wind Load INFORMS Load Path`

Current full autopilot graph sweep result:

- FHWA `Retaining Wall` evidence remains Resource Layer-only because `Structural Retaining Wall RESISTS Lateral Earth Pressure` duplicates existing semantics and drainage/perimeter-drain/groundwater graph candidates overclaim metadata-only FHWA public-page evidence.
- WBDG Fire Protection remains Resource Layer-only because available evidence supports node resource context, not a precise non-duplicative graph relation.
- Uniclass remains Resource Layer-only because classification-system context does not safely imply jurisdiction, adoption, mapping, or equivalence.
- ASCE/ACI graph candidates remain blocked by standards-context requirements.

## Visual Exhaustion

Applied visual and regression work:

- Exact verification badge status matching prevents `unverified` from rendering as positive verified state.
- NodeInspector Resource cards display `sourceTruthCaveat`, `rightsCaveat`, and `lastCheckedAt`.
- ResourceReviewAdmin link cards display backing Resource caveats and checked dates.
- Explorer rail filter regression verifies admitted Resource-backed `INFORMS` relation remains available and toggleable.

No learner/reviewer mode leak was introduced.
