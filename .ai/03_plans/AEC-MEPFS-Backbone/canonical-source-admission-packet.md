---
task: aec-mepfs-backbone
phase: canonical-source-admission
created: 2026-04-25
author: CODEX
status: METADATA-STAGING-APPROVED-ZERO-CONTENT-ADMITTED
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

S8 answered the human inbox item for zero-content, metadata-only source
admission staging. This is not the same as canonical content admission.

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
| Source currentness evidence exists | closed for declared reference/metadata use |
| Legal/licensing reviewer | no-ingest posture accepted; content clearance unfilled |
| Human steward source admission | metadata-only shadow staging approved |
| Canonical source file location and schema | not yet accepted for production |
| Rollback proof | isolated throwaway import/dump/load proof executed for shadow-only first slice |
| Human inbox approval | answered in `.ai/14_human_inbox/ANSWER_HERE.md` |

## Admission Gate

Pass only when:

- source currentness is accepted for the specific row
- legal/licensing decision is recorded when use exceeds reference/crosswalk
- steward/source admission is recorded for the exact metadata-only use
- canonical admission schema is accepted
- generated canonical artifact validates
- rollback/removal path is documented

Fail when:

- admission relies on AI approval
- admission copies protected standards text
- admission treats a reachable URL as legal clearance
- admission treats the 001-Laws raw corpus as proof of current authority
