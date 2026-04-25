---
task: aec-mepfs-backbone
phase: readiness-source-pack
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Standards And Legal Source Pack

## Purpose

This pack defines the source families that may inform the first AEC-MEPFS
Backbone readiness slice. It is a source-control artifact, not permission to
ingest copyrighted standards or legal texts into canonical backbone content.

Accepted-readiness scope: this pack is accepted as the current source-family
triage and rights-control baseline. It does not clear any protected standard,
legal clause, table, figure, dataset, or local ordinance for content ingest.

S6 materialized the first candidate source-rights registry at
`.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`.
That file is validator-ready but not steward-admitted, legally cleared, or
runtime-consumed.

## Authority Rule

External standards, model codes, laws, and hazard sources may be used in four
ways:

| Class | Meaning | Canonical Use |
|---|---|---|
| `reference_only` | Cite source family and edition/version only | allowed |
| `metadata_crosswalk` | Store code, publisher, URL, edition, and mapping note | allowed after steward review |
| `summary_extract` | Store non-substitutive summary of source purpose/scope | allowed only when rights permit |
| `content_ingest` | Store tables, clauses, figures, or substantial text | blocked unless explicit license/legal clearance exists |

Default allowed-use class is `reference_only`. Any broader use requires the
source owner/steward to record license evidence before canonical admission.

## Stewardship Status

Philip Lewis is assigned as named source steward and source/legal owner for
readiness triage. This closes the ownerless planning gap, but it does not
substitute for legal/licensing review.

No source family in this file may score `3` or be used for content ingestion
while its legal/licensing reviewer is unfilled or its clearance state is below
`cleared_for_declared_use`.

## Source Steward And Rights Decision Model

| Decision area | Owner | Reviewer required | Current effect |
|---|---|---|---|
| Source-family inclusion in planning pack | Philip Lewis | optional second reviewer | allowed for readiness planning |
| Allowed-use class triage | Philip Lewis | legal/licensing reviewer for escalation beyond reference/crosswalk use | reference and metadata-crosswalk use may be planned; ingest remains blocked |
| Protected standards text, tables, figures, or clauses | Philip Lewis as requester | legal/licensing reviewer | blocked |
| Government legal text or ordinance clause ingestion | Philip Lewis as requester | legal/code reviewer for jurisdiction and reuse status | blocked until source-specific clearance |
| Public metadata URL and citation storage | Philip Lewis | optional | allowed when official source is recorded |
| Dataset/API local caching | Philip Lewis as requester | legal/licensing reviewer and source terms review | blocked until terms recorded |

## Rights And Clearance State Vocabulary

| Clearance state | Meaning | Runtime/canonical effect |
|---|---|---|
| `planning_reference_only` | Source family may be named and cited for planning | no content ingest |
| `metadata_crosswalk_planned` | Metadata fields and external IDs may be mapped after steward review | no source text/table ingest |
| `clearance_required` | Intended use exceeds safe reference/crosswalk bounds | blocks admission |
| `cleared_for_declared_use` | Named reviewer has recorded rights evidence for the exact declared use | may proceed only inside that declared use |
| `rejected_for_local_use` | Source cannot be used locally beyond citation/reference | blocks ingest and local caching |
| `unverified_currentness` | Source exists but edition/version/currentness is not confirmed | blocks claims of current authority |

Default clearance state for all rows in this pack is
`planning_reference_only` unless a row explicitly records a stronger state.
No current row is cleared for content ingest.

## Verification Status Vocabulary

| Status | Meaning |
|---|---|
| `verified-current` | Official source page directly states current version or current portal state |
| `verified-reference` | Official/reference source is real, but exact current edition must be checked per admission |
| `verified-portal` | Official portal exists, but content/edition access is dynamic, gated, or subscription-based |
| `unverified` | No official source was confirmed in this pass |
| `blocked` | Source cannot be used beyond citation until rights or authority issue is resolved |

## Allowed-Use Vocabulary

| Class | Meaning |
|---|---|
| `public-law` | Statutory/legal text or official public legal publication, still requiring citation/provenance review |
| `open-reference` | Public metadata or descriptive page can be referenced |
| `open-free-with-attribution` | Free-to-use source with attribution or explicit published terms |
| `licensed-crosswalk` | Mapping/reference only unless license permits deeper local use |
| `subscription-text` | Full text is behind purchase/subscription/licensed access |
| `contextual-only` | May inform context but is not normative law |
| `deferred` | Source family identified but not yet admissible |

## Global Standards Families

| Source family | Publisher | Current source checked | Intended use | Allowed-use class | Status |
|---|---|---|---|---|---|
| ISO 12006-2 | ISO | https://www.iso.org/standard/61753.html | Classification framework reference | `reference_only` | official source checked; content ingest blocked |
| ISO 12006-3 | ISO | https://www.iso.org/standard/74932.html | Object-oriented information framework reference | `reference_only` | official source should be checked again at admission |
| ISO 19650-1 | ISO | https://www.iso.org/standard/68078.html | Information management reference | `reference_only` | official source checked; content ingest blocked |
| ISO 23386 / ISO 23387 | ISO | https://www.iso.org/standard/75401.html / https://www.iso.org/standard/85391.html | Data-template/property governance reference | `reference_only` | official source should be checked again at admission |
| IFC / ISO 16739-1 | buildingSMART / ISO | https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/ | Data schema alignment and external identifier mapping | `metadata_crosswalk` | official source checked; openBIM docs may be referenced, not copied wholesale |
| bSDD | buildingSMART | https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/ | Dictionary crosswalk and terminology reference | `metadata_crosswalk` | official source checked; license review still required for local caching |
| Uniclass | NBS | https://uniclass.thenbs.com/ | Classification crosswalk | `metadata_crosswalk` | official source checked; table downloads appear free to use, but local redistribution terms need steward review |
| CCI | CCIC | https://cci-collaboration.org/the-standard/ | Reference designation and classification comparison | `reference_only` | official source checked; underlying standards are separately licensed |
| CSI MasterFormat / UniFormat / OmniClass | CSI | https://www.csiresources.org/standards/overview | Specifications/cost/classification crosswalk | `reference_only` | official source checked; copyrighted/licensed content ingest blocked |
| OmniClass / NBIMS-US | NIBS | https://nibs.org/nbims/v3/ | North American classification/BIM crosswalk | `metadata_crosswalk` | source family checked; exact table release and license terms need admission-time review |
| ICC I-Codes | ICC | https://www.iccsafe.org/about/periodicals-and-newsroom/the-international-code-council-releases-2024-international-codes/ | Model-code family reference | `reference_only` | official source checked; jurisdiction adoption must be separate overlay |
| NFPA codes and standards | NFPA | https://products.nfpa.org/view/126122027/ | Fire/life-safety standard family reference | `reference_only` | official source checked; content access is subscription/licensed |
| ASCE/SEI 7 | ASCE | https://www.asce.org/topics/asce-7 | Structural load standard reference | `reference_only` | official source checked; content ingest blocked |
| Eurocodes | CEN / European Commission JRC | https://eurocodes.jrc.ec.europa.eu/ | Structural/geotechnical reference family | `reference_only` | official source checked; country adoption and NDPs are overlays |

## Philippines Source Families

| Source family | Publisher / authority | Current source checked | Intended use | Allowed-use class | Status |
|---|---|---|---|---|---|
| PD 1096 / NBCP IRR | DPWH | https://www.dpwh.gov.ph/DPWH/references/laws_codes_orders/PD1096 | National baseline legal overlay | `metadata_crosswalk` | official source checked; clause ingest requires legal review |
| RA 7160 Local Government Code | Official legal e-library / Lawphil fallback | https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/53542 | Local-government authority context | `reference_only` | source checked as legal reference; use for jurisdiction model, not code-rule extraction |
| DILG-DPWH-DICT-DTI JMC 2018-01 | Official legal e-library | https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/89926 | Permit-workflow context | `metadata_crosswalk` | official legal source identified; currentness and implementing-office status need steward review |
| BP 344 Accessibility IRR | DPWH | https://www.dpwh.gov.ph/DPWH/sites/default/files/laws_codes_orders/BP_344_IRR_0.pdf | Accessibility overlay | `metadata_crosswalk` | official source checked; amended IRR references require steward confirmation |
| RA 9514 Fire Code RIRR | BFP | https://bfp.gov.ph/revised-irr-of-ra-9514-the-fire-code-of-the-philippines/ | Fire code legal overlay | `metadata_crosswalk` | official source checked; use 2019 RIRR unless later official BFP source supersedes |
| PD 856 Sanitation Code | DOH / law repositories | https://lpr.adb.org/resource/code-sanitation-philippines-presidential-decree-no-856-series-1975 | Sanitation/public-health overlay | `reference_only` | official DOH source not yet confirmed; keep unverified |
| Philippine Green Building Code | DPWH | https://dpwh.gov.ph/DPWH/references/laws_codes_orders/pgbc | Green-building referral-code overlay | `metadata_crosswalk` | official source checked |
| BP 220 economic/socialized housing | DHSUD / Lawphil | https://dhsud.gov.ph/wp-content/uploads/Laws_Issuances/02_IRR/Revised_IRR_BP220_2008.pdf | Housing standards overlay | `metadata_crosswalk` | official source checked; currentness needs DHSUD steward confirmation |
| Plumbing and electrical professional codes | PRC / professional statutes / professional bodies | https://lawphil.net/statutes/repacts/ra1955/ra_1378_1955.html / https://lawphil.net/statutes/repacts/ra1995/ra_7920_1995.html | Plumbing/electrical professional and standards context | `reference_only` | professional statutes checked; current plumbing/electrical code edition sources remain unverified |
| Local zoning ordinances | LGU / city council | https://www.quezoncity.gov.ph/wp-content/uploads/2021/01/Quezon-City-Zoning-Ordinance-2016.pdf | Exemplar city legal overlay | `metadata_crosswalk` | Quezon City source checked; every LGU pack requires separate source row |
| HazardHunterPH / GeoRiskPH | DOST-PHIVOLCS | https://hazardhunter.georisk.gov.ph/ | Hazard-context overlay | `metadata_crosswalk` | official source checked; hazard data is contextual, not normative law |
| PHIVOLCS hazard maps | DOST-PHIVOLCS | https://www.phivolcs.dost.gov.ph/landslide/landslide-hazard-maps/ | Earthquake/volcano/landslide hazard context | `metadata_crosswalk` | official source checked; official assessment reports may require request |
| PAGASA climate data | DOST-PAGASA | https://www.pagasa.dost.gov.ph/climate/climate-data | Climate context overlay | `metadata_crosswalk` | official source checked; exact dataset terms need review |
| DENR-MGB geohazard maps | DENR-MGB | https://www.mgb.gov.ph/2015-05-13-02-02-11/mgb-news/303-mgb-s-geohazard-maps-now-viewable-and-downloadable-online | Geohazard context overlay | `metadata_crosswalk` | official MGB source identified; exact current map portal and reuse terms need review |
| PSGC administrative geography | Philippine Statistics Authority | https://psa.gov.ph/classifications-api/psgc | Jurisdiction tree coding | `metadata_crosswalk` | official API identified; current version must be checked at pack-build time |

## Blocked Until Steward Review

- Do not import ISO, CSI, ICC, NFPA, ASCE, or CEN protected text, tables, figures,
  or clause content.
- Do not cache bSDD, Uniclass, IFC, or HazardHunterPH datasets locally until the
  allowed API/download terms are recorded.
- Do not treat Lawphil, ADB, third-party mirrors, or Reddit claims as primary
  source truth where an official agency page exists.
- Do not model local zoning as national law. Local ordinances are LGU overlays
  with local validity scope.
- Do not assume government-hosted PDFs inherit a broad reuse license from the
  parent agency site. Record page-level or document-level rights when available.
- Do not treat existing raw-source corpus membership, including 001-Laws local
  ordinance files, as proof of legal authority, currentness, or reuse rights.

## Unverified Claims Log

- Any `current edition` claim not read directly from an official source page at
  admission time remains `unverified`.
- Any claim that ISO, NFPA, ICC, ASCE, CSI, CEN, or Eurocode text is locally
  redistributable remains `blocked`.
- Any future draft or replacement edition remains `unverified` until effective
  publication is confirmed.
- Any local zoning/source status remains `unverified` until the target LGU is
  selected and official source URL is recorded.
- Any hazard-source output is contextual unless an official law, ordinance,
  permit, or contract makes it binding.

## Minimum Registry Fields

Every source admitted later must have:

- source family
- publisher / authority
- edition / version / effective date
- official URL
- mirror URL, if any
- source-rights class
- clearance state
- intended Vitruvius use
- steward owner
- legal/licensing reviewer, if required
- reviewer decision and date, if required
- declared use boundary
- update cadence
- currentness check date
- currentness evidence URL
- blocking notes

Recommended future `source-rights-registry.md` columns:

| Column | Required | Notes |
|---|---|---|
| `source_id` | yes | stable Vitruvius source-family or source-edition ID |
| `source_family` | yes | human-readable family name |
| `publisher_authority` | yes | publisher, agency, standards body, or LGU |
| `edition_version_effective_date` | yes | exact edition/version/date or `unverified_currentness` |
| `official_url` | yes | primary source where possible |
| `mirror_url` | no | fallback only, not authority when official exists |
| `source_rights_class` | yes | allowed-use vocabulary value |
| `clearance_state` | yes | rights clearance vocabulary value |
| `intended_vitruvius_use` | yes | exact use boundary |
| `steward_owner` | yes | currently Philip Lewis unless reassigned |
| `legal_reviewer` | conditional | required for escalation/content ingest/local caching |
| `reviewer_decision` | conditional | required when legal reviewer is required |
| `currentness_check_date` | yes | date of latest official-source check |
| `update_cadence` | yes | planned review cadence |
| `blocking_notes` | yes | explicit blocker or `none` |

## Pass / Fail Gate

Pass:

- every first-wave source has an official URL or is marked `unverified`
- every source has an allowed-use class
- copyrighted standards are reference/crosswalk only
- Philippines legal and hazard sources are separated by overlay kind
- Philip Lewis is recorded as readiness source steward/source-legal owner, with
  legal/licensing reviewer gates still blocking content ingest

Fail:

- any source with unknown rights is used as canonical seed material
- any standards table or legal clause text is copied into canonical backbone
  content without explicit clearance
- any hazard source is treated as a legal obligation
