---
task: aec-mepfs-backbone
phase: readiness-spec-acceptance
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Readiness Spec Acceptance Record

## Purpose

Record which AEC-MEPFS Backbone specs are accepted as readiness-control specs
and which gates still block runtime implementation.

Accepted-readiness-control means the document can govern the next implementation
packet. It does not mean canonical taxonomy content, source rights, database
mutation, feature flags, or runtime code are approved.

## Acceptance Matrix

| Spec | Acceptance status | Runtime implication | Open blockers |
|---|---|---|---|
| `relationship-predicate-registry-draft.md` | accepted as readiness predicate spec | runtime may not invent unregistered governed predicates | fixture-level validation exists; production registry location, release owner, and migration runner remain open |
| `master-taxonomy-l1-l2-decision-record.md` | accepted as first-slice L1/L2 planning candidate | runtime may use this as guardrail, not canonical node admission | independent review, domain review, LD-10 reconciliation, admitted source files |
| `standards-legal-source-pack.md` | accepted as source-family and rights-control baseline | runtime may cite/source-map only inside declared allowed-use class | fixture-level source-rights rows exist; legal/licensing reviewer, production registry, and admission currentness checks remain open |
| `governance-editorial-control-pack.md` | accepted as governance-control baseline | Philip Lewis is named accountable steward; AI remains non-authority | independent second reviewer, legal/licensing reviewer, discipline reviewers |
| `vitruvian-context-resolver-pack.md` | accepted as resolver planning contract | future resolver must be deterministic and no-LLM in hot path | fixture-level result-type coverage exists; non-PH disposition, benchmark harness, exact API assertions, and resolver runner remain open |
| `shadow-graph-database-safety-protocol.md` | accepted as database safety protocol | first code slice must be shadow-only and non-destructive | planned rollback fixture exists; backup/export proof, restore proof, executed smoke queries, and 48h monitoring design remain open |
| `api-explorer-parity-contract.md` | accepted as API/Explorer consumer contract | v1 behavior is preserved; `/v2` is additive and shadow-only | fixture-level v1/v2 boundary checks exist; exact response-shape tests, status-code rules, ordering rules, and runner remain open |
| `verification-and-benchmark-contract.md` | accepted as verification skeleton | implementation packet must fill exact commands and report paths | corpus, hardware/runtime baseline, repetition policy, percentile reporting |

## Promotion Decision

The prior drafts are promoted only to `ACCEPTED-READINESS-CONTROL`. They are not
promoted to `ACCEPTED-FOR-IMPLEMENTATION`.

Reason:

- fresh GitNexus evidence shows HIGH and CRITICAL impact roots in the KG core
- source/legal ownership is named for planning but independent legal/licensing
  review is still unfilled
- API/Explorer and resolver fixtures are contract-validated only, not runtime
  executable parity/resolver runners
- backup/restore and rollback proof have not been run
- no canonical backbone source files have been admitted

## Bounded Readiness Implementation Status

`AEC-BB-S1` and `AEC-BB-S2` are implemented and validated as file-backed
contract checks. They improve readiness evidence but do not promote any spec to
`ACCEPTED-FOR-IMPLEMENTATION`.

`AEC-BB-S2` added executable fixture validation for:

- predicate registry rows
- source-rights registry rows
- authoring/migration QA cases
- resolver golden cases
- API / Explorer parity cases
- shadow rollback plan metadata

The rows in `valid_readiness_s2.json` are contract fixtures only. They are not
canonical taxonomy data, production source-rights registry rows, legal clearance
records, database migration inputs, or runtime API/Explorer fixtures.

## First Implementation Packet Constraint

The first implementation packet must be bounded enough to respect this record:

- no edit to `CanonicalNode`
- no Neo4j write-path mutation
- no feature-flag enablement
- no graph rebuild
- no destructive cleanup/reset
- no canonical content admission
- no protected source ingest

Any packet that violates these constraints must create a new audit, impact map,
implementation plan, critique, and validation contract before code work.
