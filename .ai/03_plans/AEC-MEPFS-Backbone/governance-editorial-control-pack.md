---
task: aec-mepfs-backbone
phase: readiness-governance
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Governance And Editorial Control Pack

## Purpose

This pack defines who can admit, change, deprecate, merge, split, or release
AEC-MEPFS Backbone content.

Accepted-readiness scope: this pack is accepted as the current governance
control surface for planning and first-slice packet design. It is not approval
to admit canonical taxonomy content, legal overlays, source-rights decisions, or
runtime code. Independent human review and legal/licensing review remain
required gates.

## Governance Principle

AI may propose and audit. AI may not be the editorial authority for canonical
taxonomy, legal overlays, source-rights decisions, or resolver precedence.

## Operating Reality - Single Steward Mode

Vitruvius is currently operating in a single named-steward mode for readiness
planning. That means one project owner can be named for accountability and
triage, but approval gates that require independent or legal review remain
blocked until those roles are filled.

Named accountable steward for this readiness packet:

- Philip Lewis

AI systems, including Codex, Kimi, Claude, Gemini, and future local agents, are
recorded as drafting, audit, and implementation assistants only. They are not
owners, legal reviewers, or canonical-content approvers.

## Document Control Requirements

Every released governance pack must record:

- canonical path
- version
- effective date
- owner
- accountable steward
- named responsible steward
- independent reviewer, when required
- legal/licensing reviewer, when required
- approval status
- approvers
- supersedes
- related release notes
- changelog entry

## Named Steward Roster

| Role | Named owner | Authority scope | Current status |
|---|---|---|---|
| Backbone steward | Philip Lewis | Accepts readiness direction, owns taxonomy-first architecture intent, decides whether a packet may move to execution planning | assigned |
| Architecture steward | Philip Lewis | Owns architecture boundary decisions and runtime sequencing until a separate reviewer is appointed | assigned, second-review required for major architecture changes |
| Resolver steward | Philip Lewis | Owns deterministic resolver behavior and conflict-return policy at planning level | assigned, implementation approval still gated |
| Source steward | Philip Lewis | Owns source-family triage and allowed-use classification at planning level | assigned, legal/licensing clearance unfilled |
| Source/legal owner | Philip Lewis | Accountable for deciding when legal review is required and blocking content ingest until clearance exists | assigned as owner, not a substitute for legal reviewer |
| Philippines overlay steward | Philip Lewis | Owns first Philippines overlay pilot planning and source-row selection | assigned, jurisdiction/code reviewer unfilled |
| Release steward | Philip Lewis | Owns readiness packet versioning and release notes for planning artifacts | assigned |
| Independent second reviewer | unfilled required role | Required for L1/L2 admission, major structural changes, and implementation acceptance | blocks score `3` |
| Legal/licensing reviewer | unfilled required role | Required for source-rights escalation, content-ingest clearance, and protected-standard reuse decisions | blocks score `3` |
| Discipline reviewers | unfilled required roles | Required before domain-specific L1/L2 or golden-case acceptance outside owner expertise | blocks score `3` where applicable |

## Steward RACI

| Area | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| L1/L2 taxonomy domains | Philip Lewis until domain steward is appointed | Philip Lewis | independent second reviewer and discipline reviewers | implementation agents |
| Source-rights rows | Philip Lewis | Philip Lewis | legal/licensing reviewer | implementation agents |
| Philippines legal overlays | Philip Lewis until jurisdiction steward is appointed | Philip Lewis | PH code/legal reviewer | implementation agents |
| Hazard overlays | Philip Lewis until hazard-data steward is appointed | Philip Lewis | PHIVOLCS/PAGASA source reviewer when available | implementation agents |
| Resolver precedence | Philip Lewis | Philip Lewis | independent architecture reviewer, domain and jurisdiction reviewers | implementation agents |
| Release notes | Philip Lewis | Philip Lewis | all filled stewards | all agents |

Philip Lewis is now the named accountable owner for first-wave readiness
planning. This closes the ownerless-placeholder gap, but it does not close the
independent-review or legal/licensing-review gap. Implementation remains blocked
where those gates are required.

## Owner Assignment Status

| Area | Current status | Score impact |
|---|---|---|
| Backbone steward | Philip Lewis assigned | owner gap closed for readiness; independent review still blocks score `3` |
| Domain stewards | Philip Lewis assigned as interim first-wave steward | discipline-specific review still blocks score `3` |
| Source/legal steward | Philip Lewis assigned as source/legal owner | legal/licensing reviewer still blocks protected-content clearance |
| Philippines jurisdiction steward | Philip Lewis assigned as pilot steward | PH code/legal reviewer still blocks legal overlay admission |
| Resolver steward | Philip Lewis assigned | independent architecture review still required before runtime |
| Release steward | Philip Lewis assigned | release-owner gap closed for readiness |
| Independent second reviewer | unfilled | blocks L1/L2 admission and major architecture acceptance |
| Legal/licensing reviewer | unfilled | blocks content ingest and protected source reuse |

## Change Control

Every proposed change uses one of these actions:

- `add`
- `change_label`
- `change_definition`
- `add_alias`
- `deprecate`
- `merge`
- `split`
- `move_primary_home`
- `add_mapping`
- `remove_mapping`
- `change_precedence`

Change classes:

- editorial correction
- additive controlled expansion
- semantic modification
- structural change
- deprecation/removal
- emergency correction

Required fields:

- proposal ID
- proposer
- action
- affected node/source/overlay IDs
- reason
- evidence links
- backward-compatibility impact
- resolver impact
- reviewer decisions
- release target

## Review Gates

| Change class | Minimum review |
|---|---|
| L1/L2 domain or topic add/remove/move/change | PRD plus backbone steward plus accountable domain steward plus two human reviewers |
| legal overlay add/change | jurisdiction steward plus legal/code reviewer |
| source-rights class change | source steward plus legal/licensing reviewer |
| resolver precedence change | resolver steward plus architecture steward |
| alias/synonym add | domain steward or delegated reviewer |
| AI-proposed L3/L4 node | LD-8 `PlacementAssertion` workflow: auto-accept only for single-clear leaf at confidence >= 0.92; queue 0.75-0.91; reject below 0.75 |

If a required independent reviewer, discipline reviewer, PH code/legal reviewer,
or legal/licensing reviewer is unfilled, the review outcome must be `defer` or
`blocked`. The steward cannot self-approve a gate that this pack defines as
independent or legal review.

## Release And Versioning

Separate releases are required:

- taxonomy release: canonical domains/topics/facets
- mapping-pack release: external standard and source mappings
- overlay release: jurisdictional/source applicability overlays
- resolver release: precedence, conflict, and API contract behavior

Version format:

- `taxonomy.YYYY.MM.N`
- `mapping.YYYY.MM.N`
- `overlay.<jurisdiction>.YYYY.MM.N`
- `resolver.YYYY.MM.N`

Release types:

| Type | Trigger |
|---|---|
| patch | typo, clarification, non-semantic alias, metadata correction |
| minor | additive node, mapping, overlay, or review rule |
| major | L1/L2 structure, resolver precedence, ID policy, source-rights class model, or breaking semantic change |

No runtime implementation may depend on an unreleased draft artifact unless it is
behind a shadow-only feature flag and explicitly named in the execution plan.

Every release note must include scope, affected domains, breaking semantic
changes, deprecated items, migration notes, and rollback/supersession path.

## AI-Use Policy

Allowed:

- propose L3/L4 candidate nodes through the LD-8 `PlacementAssertion` workflow
- propose aliases and definitions
- compare source snippets
- flag duplicates and conflicts
- draft review comments
- generate test/golden-case candidates

Blocked:

- admitting canonical nodes
- proposing, creating, or mutating L1/L2 nodes
- choosing legal precedence
- declaring source rights
- resolving equal-force conflicts
- overwriting steward decisions
- writing directly to canonical backbone without review workflow

## Naming And Definition Policy

Canonical labels must be:

- user-readable
- domain-specific
- non-truncated
- stable across source documents
- free of document slug suffixes
- no longer than needed for disambiguation

Every admitted topic must include:

- preferred label
- short label
- definition
- scope note
- aliases
- deprecated labels, if any
- primary home
- secondary relationship links
- source evidence
- steward and review status

Definition quality bar:

- non-circular
- bounded
- distinguishable from siblings
- compatible with governed hierarchy
- one canonical definition per governed concept

## Jurisdiction Precedence Policy

Resolver precedence must distinguish:

1. validity and effective-date filtering
2. jurisdiction scope
3. legal force
4. project contractual overlay
5. specificity
6. temporal order
7. equal-force conflict handling

Examples:

- national law can set baseline obligations
- local ordinance can add local constraints inside its jurisdiction
- project contract can add stricter project requirements when legally allowed
- hazard context can inform applicability but does not become law by itself
- equal-force conflicts must return `conflict`, not an invented winner

## Pass / Fail Gate

Pass:

- named stewards exist for each first-wave domain and source family
- every change type has a review path
- AI authority is explicitly bounded
- release/versioning policy is separate for taxonomy, mappings, overlays, and
  resolver behavior

Fail:

- AI output can directly promote canonical content
- legal/source-rights decisions lack a human accountable owner
- release artifacts mix taxonomy, mapping, overlay, and resolver changes without
  separable versions

## Appendix Pack

### Appendix A - Named RACI Template

| Role | Human owner | Backup | Appointment evidence | Review cadence |
|---|---|---|---|---|
| Backbone steward | Philip Lewis | TBD | project-owner direction in AEC-MEPFS readiness session, 2026-04-25 | per release |
| Domain steward | Philip Lewis, interim | TBD | project-owner direction in AEC-MEPFS readiness session, 2026-04-25 | per domain release |
| Source/legal steward | Philip Lewis, as owner not legal reviewer | TBD | project-owner direction in AEC-MEPFS readiness session, 2026-04-25 | per source pack |
| Jurisdiction steward | Philip Lewis, interim PH pilot | TBD | project-owner direction in AEC-MEPFS readiness session, 2026-04-25 | per overlay release |
| Resolver steward | Philip Lewis | TBD | project-owner direction in AEC-MEPFS readiness session, 2026-04-25 | per resolver release |
| Release steward | Philip Lewis | TBD | project-owner direction in AEC-MEPFS readiness session, 2026-04-25 | per release |
| Independent second reviewer | unfilled required role | TBD | none | every L1/L2 or major architecture release |
| Legal/licensing reviewer | unfilled required role | TBD | none | every source-rights escalation or content-ingest request |

### Appendix B - Change-Class Matrix

| Change class | Review owner | Evidence required | Release impact |
|---|---|---|---|
| editorial correction | domain or release steward | before/after text and reason | patch |
| additive controlled expansion | domain steward | definition, examples, source evidence | minor |
| semantic modification | accountable steward | impact note and migration path | minor or major |
| structural change | backbone steward | PRD, audit, two-human review | major |
| deprecation/removal | backbone steward | redirects, migration, rollback note | major |
| emergency correction | accountable steward | incident note and follow-up review | patch or minor |

### Appendix C - Review-Gate Checklist

- steward assigned
- L1/L2 change has PRD, backbone steward approval, and two-human review
- L3/L4 AI proposal follows LD-8 confidence thresholds
- source evidence linked
- source-rights class checked
- predicate registered
- jurisdiction effect checked
- resolver impact checked
- migration impact checked
- release target named
- rollback or supersession path written

### Appendix D - Pass/Fail Checklist

- Pass only if AI has proposal/audit authority, not admission authority.
- Pass only if source-rights and legal precedence decisions have named owners.
- Fail if a staged proposal can become canonical without human review.
- Fail if runtime implementation depends on a draft artifact without a
  shadow-only execution packet.

### Appendix E - Release-Classification Table

| Release class | Typical use | Requires migration note |
|---|---|---|
| patch | typo, metadata correction, non-semantic alias | no |
| minor | additive node, mapping, overlay, fixture, or review rule | sometimes |
| major | L1/L2 structure, ID policy, resolver precedence, source-rights model | yes |

### Appendix F - AI-Use Disclosure Template

- AI tool:
- prompt or task summary:
- generated candidate type:
- human reviewer:
- accepted/rejected/deferred:
- reason:
- source evidence checked:

### Appendix G - Jurisdiction-Precedence Decision Table

| Scenario | Expected handling |
|---|---|
| national baseline plus stricter local ordinance | compose compatible obligations |
| equal-force incompatible local rules | return `conflict` |
| hazard data without adoption | contextual only |
| project contract stricter than baseline and legally allowed | compose as project overlay |
| superseded edition | return deprecation/supersession warning |

### Appendix H - Glossary

- `canonical admission`: promotion into governed source-of-truth content.
- `overlay`: jurisdictional, contractual, or contextual attachment to a global
  concept.
- `steward`: human accountable owner for a content family or release surface.
- `review-state relationship`: temporary staging edge that is not graph truth.
- `release`: versioned publication of taxonomy, mapping, overlay, or resolver
  behavior.

## Required Before Score `3`

- RACI matrix with named humans
- named owner appointment evidence
- source/legal steward acceptance
- release steward acceptance
- one completed sample change proposal through the checklist
