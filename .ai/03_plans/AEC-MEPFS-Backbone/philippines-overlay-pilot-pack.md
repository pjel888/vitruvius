---
task: aec-mepfs-backbone
phase: readiness-philippines-overlay
created: 2026-04-25
author: CODEX
status: DRAFT
---

# Philippines Overlay Pilot Pack

## Purpose

This pack defines the first Philippines country overlay as overlays over the
global AEC-MEPFS Backbone. It does not create a Philippines-only taxonomy fork.

## Jurisdiction Tree

First-wave jurisdiction scopes:

- `PH` - national
- `PH-REG` - region
- `PH-PROV` - province
- `PH-HUC` - highly urbanized city
- `PH-ICC` - independent component city
- `PH-CITY` - component city or municipality
- `PH-BRGY` - barangay, when source exists
- `PH-SITE` - site or hazard assessment scope
- `PH-PROJ` - project contractual scope

All local overlays inherit from broader scope unless validity, legal force, or
specificity rules produce a conflict.

Use PSA PSGC as the administrative tree authority:
https://psa.gov.ph/classifications-api/psgc

Each jurisdiction node must record name, PSGC code, admin type, parent, source
URL, and verification date. The latest PSGC version must be checked at pack
build time.

## First-Wave Authority Families

| Family | Scope | Overlay kind | Source status |
|---|---|---|---|
| PD 1096 / NBCP IRR | national | `legal_normative` | DPWH source checked |
| RA 7160 Local Government Code | national/local authority context | `legal_normative` | official legal e-library source checked |
| DILG-DPWH-DICT-DTI JMC 2018-01 | permit workflow streamlining | `guidance_reference` | official legal e-library source identified; currentness needs steward check |
| BP 344 Accessibility IRR | national | `legal_normative` | DPWH source checked; current amendment status needs steward confirmation |
| RA 9514 Fire Code RIRR | national | `legal_normative` | BFP 2019 RIRR source checked |
| PD 856 Sanitation Code | national | `legal_normative` | official DOH source not yet confirmed; keep unverified |
| Philippine Green Building Code | national/referral code | `standards_adopted` | DPWH source checked |
| BP 220 economic/socialized housing | national | `legal_normative` | DHSUD source checked; currentness review needed |
| Plumbing and electrical codes | national/professional standard | `standards_adopted` | professional statute sources checked; official current code-edition sources not yet verified |
| Local zoning ordinances | LGU | `legal_normative` | Quezon City exemplar checked; other LGUs per-pack |
| HazardHunterPH / GeoRiskPH | site/context | `hazard_contextual` | DOST-PHIVOLCS source checked |
| PHIVOLCS hazard maps | site/context | `hazard_contextual` | DOST-PHIVOLCS source checked |
| PAGASA climate data | site/context | `hazard_contextual` | DOST-PAGASA source checked |
| DENR-MGB geohazard maps | site/context | `hazard_contextual` | official MGB source identified; exact current map portal and reuse terms need review |

## Overlay Kinds

- `legal_normative` - binding law, regulation, IRR, ordinance, or permit rule
- `standards_adopted` - standard adopted by law, code, contract, or authority
- `project_contractual` - stricter project-specific obligation
- `hazard_contextual` - hazard, climate, geotechnical, or site-risk context
- `guidance_reference` - non-binding guidance or explanatory material
- `permit_workflow` - process/procedure requirements for applications,
  inspections, clearances, and occupancy processing

## Precedence Behavior

The resolver must:

- filter by validity and effective date first
- apply jurisdiction scope
- distinguish legal force from hazard context
- compose compatible national and local requirements
- return `conflict` for equal-force incompatible requirements
- preserve source trace for every decision

Hazard context can trigger applicability questions and design review, but it
does not override a legal obligation unless a law, ordinance, permit condition,
or project contract makes that hazard source normative.

## Pilot Scope

Milestone 1:

- national baseline: PD 1096, BP 344, RA 9514, PGB Code, BP 220
- hazard context: HazardHunterPH plus PHIVOLCS/PAGASA source references
- primary exemplar LGUs: Quezon City and Mauban, Quezon
- later candidate city benchmarks: Cebu City and Davao City, only after official
  building-office, ordinance, and permit-workflow sources are confirmed

Rationale:

- Quezon City has accessible official zoning material and mature urban controls.
- Mauban, Quezon appears in the existing 001-Laws-derived corpus and gives a
  non-Metro Manila municipal zoning/use case.
- Existing corpus presence is only a migration signal. It does not prove source
  currentness, legal force, or reuse rights without an official source row.

Full LGU coverage is explicitly out of scope for the first pilot.

Manila is not included until a current official source set is confirmed.

## Fallback Citation Rules

Use source priority:

1. official agency/LGU source
2. Official Gazette or official publication record
3. Lawphil for statute text where agency source is absent
4. ADB/LPR or similar institutional mirror for cross-checking
5. third-party or community mirrors only as discovery aids, never as source truth

Every fallback citation must explain why a higher-priority source is unavailable
or not yet verified.

## Source-Rights Fields

Every Philippines source row must include:

- `rights_status`: `public-domain`, `open-data`, `restricted`, or
  `rights-unclear`
- `rights_basis_url`
- `reuse_note`
- `verification_state`

Default to `rights-unclear` when the page or document has no explicit reuse
signal.

## Pass / Fail Gate

Pass:

- Philippines overlay is modeled as jurisdiction/source overlays over the global
  taxonomy
- national baseline plus exemplar city/municipality scope is explicit
- hazards are contextual unless legally adopted
- all unverified source families are marked

Fail:

- Philippines law becomes a separate taxonomy branch
- hazards are treated as legal obligations without adoption
- full LGU coverage is implied as first-slice scope
- third-party mirrors are treated as primary sources
