---
task: aec-mepfs-backbone
phase: canonical-source-admission
created: 2026-04-25
author: CODEX
status: PREPARED-ZERO-SOURCES-ADMITTED
---

# Canonical Source Admission Packet

## Purpose

Define the first canonical source admission path for the AEC-MEPFS Backbone
without admitting source content prematurely.

## Current Admission Result

Canonical source admission count: `0`

No files were added to `003_Canonical-Knowledge-Layer/` by this packet. No
standards text, legal clauses, government PDF text, hazard data, table, figure,
or external dataset was ingested.

## Required Admission Inputs

Before the first canonical source can be admitted, the admission record must
include:

- `source_id`
- source family
- publisher/authority
- edition/version/effective date
- official URL
- source-rights class
- legal/licensing decision, when required
- currentness decision
- steward decision
- intended Vitruvius use
- declared no-ingest or ingest boundary
- citation/provenance record
- rollback/removal path

## First Candidate Admission Class

The first safe admission should be metadata-only:

- source-family metadata
- official URL
- edition/currentness metadata after human review
- declared use boundary
- provenance and reviewer decision

It should not admit source text or standards tables.

## Blockers

| Blocker | Status |
|---|---|
| Source-rights registry candidate exists | closed for candidate prep |
| Source currentness evidence exists | closed for evidence; 5 manual-review rows remain |
| Legal/licensing reviewer | unfilled |
| Human steward source admission | pending |
| Canonical source file location and schema | not yet accepted for production |
| Rollback proof | not executed in stopped/isolated Neo4j environment |

## Admission Gate

Pass only when:

- source currentness is accepted for the specific row
- legal/licensing decision is recorded when use exceeds reference/crosswalk
- steward admission is signed
- canonical admission schema is accepted
- generated canonical artifact validates
- rollback/removal path is documented

Fail when:

- admission relies on AI approval
- admission copies protected standards text
- admission treats a reachable URL as legal clearance
- admission treats the 001-Laws raw corpus as proof of current authority
