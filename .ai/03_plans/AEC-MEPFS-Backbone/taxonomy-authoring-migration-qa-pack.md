---
task: aec-mepfs-backbone
phase: readiness-authoring-qa
created: 2026-04-25
author: CODEX
status: DRAFT
---

# Taxonomy Authoring And Migration QA Pack

## Purpose

This pack defines the authoring, staging, review, and validation workflow needed
before broad AI-assisted classification or migration begins.

## Authoring Template

Every proposed node requires:

- canonical ID
- path code
- level
- parent path code
- preferred label
- short label
- definition
- scope note
- primary L1/L2 home
- aliases
- deprecated labels
- facet values
- relationship proposals
- source evidence
- steward
- review status
- release target

Minimum example corpus per admitted concept:

- one clean example
- one boundary example
- one non-example for a common ambiguity

## Definition Template

Definitions must answer:

- What is this concept?
- What is in scope?
- What is out of scope?
- What adjacent concepts are commonly confused with it?
- Which source families support the definition?
- Which jurisdiction or standards context affects it?

Definitions must not copy protected standard text unless source rights explicitly
permit that use.

## Synonym And Thesaurus Rules

- Aliases point to one canonical node.
- Acronyms require expanded label and domain context.
- Slang, old labels, and document-derived labels are allowed only as aliases.
- Deprecated labels must include replacement target and reason.
- Same label across domains requires disambiguation through domain or qualifier.
- Allowed synonym classes are preferred label, admitted synonym,
  acronym/abbreviation, deprecated term, regional term, and common misspelling.
- Synonyms cannot replace canonical IDs.

## Facet Handbook

Each node can carry controlled facet values for:

- lifecycle
- asset type
- performance topic
- geography/jurisdiction
- knowledge type
- standards context
- project type
- primary domain

Facet values do not create duplicate taxonomy homes.

## Relationship Vocabulary

First-wave relationship proposals must use registered predicate families only:

- hierarchy: `broader_than`, `narrower_than`, `part_of`
- applicability: `governs`, `requires`, `constrains`,
  `applicable_in_jurisdiction`
- mapping: `maps_to_external_standard`
- semantics: `conflicts_with`, `supersedes`
- evidence: `evidenced_by`
- facets: `has_facet`

New predicate proposals go to review and cannot be used in canonical content
until registered.

`related_to` is allowed only as a temporary review-state relationship. It must
not be admitted as a governed predicate for first-slice canonical authoring.

## Staging Layout

Future staging areas should separate:

- AI proposals
- human steward drafts
- reviewed candidates
- rejected/deprecated candidates
- golden dataset fixtures
- migration workbooks

No staged proposal is canonical until review status is `accepted`.

## Legacy-To-Canonical Workbook

Required columns:

- legacy ID or label
- source document
- proposed canonical ID
- mapping type: exact, broader, narrower, related, reject
- confidence score
- evidence link
- reviewer
- decision
- notes

## Validation Ruleset

Blocking validation:

- duplicate canonical ID
- duplicate preferred label in same primary home
- missing definition
- missing source evidence
- missing steward
- invalid predicate
- invalid facet value
- external standard code used as primary ID
- legal overlay inserted as taxonomy branch
- vague predicate promoted as canonical graph edge
- lossy legacy predicate mapping without steward decision
- inferred edge missing explicit evidence anchor or inference rule

Warning validation:

- very long preferred label
- weak or circular definition
- alias collision
- unreviewed source-rights row
- relationship fan-out above threshold
- inferred semantic edges outnumber explicit semantic edges for a migrated slice
- display label and source label are not separated for long document-derived
  rule names

## Review Queues

| Queue | Entry condition | Exit condition |
|---|---|---|
| `ai_proposed` | generated candidate | accepted for human review or rejected |
| `steward_draft` | human-authored or AI proposal accepted for review | peer review complete |
| `source_rights_review` | source use broader than reference-only | source steward decision |
| `jurisdiction_review` | legal/local overlay candidate | jurisdiction steward decision |
| `resolver_golden_case` | precedence/conflict example | expected output accepted |
| `release_candidate` | all checks pass | included in versioned release |

Exit states are `accepted`, `accepted_with_conditions`, `return_for_revision`,
`rejected`, and `deferred`.

## Confidence Policy Matrix

| Proposal class | Auto-accept | Human review | AI prohibited |
|---|---:|---:|---:|
| alias suggestion | no | yes | no |
| duplicate detection | no | yes | no |
| L3/L4 topic proposal | yes, only for single-clear leaf at confidence >= 0.92 through LD-8 `PlacementAssertion` workflow | 0.75-0.91 queue; sampling audit for auto-accepted cases | no |
| L1/L2 domain change | no | PRD plus steward approval plus two-human review for human-authored proposals only | yes; AI may not propose, create, mutate, or decide |
| source-rights class | no | legal/source steward | yes |
| legal precedence | no | jurisdiction/resolver steward | yes |
| equal-force conflict resolution | no | steward decision | yes |

## Human Review Ratios

| Proposal class | Minimum review |
|---|---|
| L1/L2 backbone change | 100%, two-human review plus accountable steward |
| L3/L4 topic proposal | 100% for 0.75-0.91 queue; validator and sampling audit for LD-8 auto-accepted single-clear leaves at confidence >= 0.92 |
| synonym addition | 50% sample for low-risk aliases, 100% for collisions |
| facet assignment | 50% sample, 100% for low-confidence or conflicting evidence |
| relationship proposal | 100% for cross-domain or legal/compliance relationships |
| standards mapping | 100% source/steward review |
| legacy split/merge mapping | 100% two-human review |

## Golden Dataset Target

Initial target: 250 cases.

Coverage:

- 50 taxonomy placement cases
- 50 alias/deduplication cases
- 50 external standard mapping cases
- 50 Philippines overlay/resolver cases
- 25 conflict/composition cases
- 25 negative/rejection cases

Each case requires:

- input
- expected output
- rationale
- source evidence
- owner
- review status

## Historical Failure Regression Checks

The migration QA suite must include checks for the failures seen in the current
KG audits:

- `DEFINED_BY` and `SUPPORTED_BY` are counted as provenance coverage, not
  semantic relationship quality.
- `RELATED_TO` cannot be the primary enrichment predicate.
- document-derived rule names become aliases or source labels unless a steward
  approves a user-facing canonical label.
- source-reference concepts such as professional-practice documents are
  materialized as concepts, authority documents, or evidence spans according to
  class, not duplicated across fragmented rule nodes.
- L1/L2 changes cannot be AI-proposed, and L3/L4 AI proposals must follow LD-8
  `PlacementAssertion` thresholds instead of a separate ad hoc policy.

## Pass / Fail Gate

Pass:

- templates and queues exist before AI proposal runs
- source-rights and jurisdiction reviews are separated
- golden dataset has target size, coverage, and ownership
- confidence policy blocks AI from final authority

Fail:

- broad classification runs without staging
- AI proposals can become canonical without review
- source-rights/legal decisions share the same queue as ordinary taxonomy edits
- broad migration starts before the workbook schema exists
- validation has no blocking severities
- human-review ratios are unspecified
