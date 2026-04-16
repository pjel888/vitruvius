---
task: aec-legal-family-classification
phase: 05
created: 2026-04-16
author: CODER
status: ACCEPTED
---

# 2026-04-16 AEC Legal Family Classification Plan

## Goal
Prevent semantic duplication across laws, IRRs, amendments, and adjacent regulatory instruments while preserving source truth and scaling across AEC subjects.

## Canonical model
### Work
Abstract semantic family, e.g. `work-ph-aec-building-pd-1096`

### Instrument
Concrete legal/regulatory artifact, e.g.:
- `instrument-ph-aec-building-pd-1096-law`
- `instrument-ph-aec-building-pd-1096-irr`
- `instrument-ph-aec-building-pd-1096-rirr-2004`

### Source
Actual admitted file/artifact/canonical source page.

## Minimum metadata fields
- `domain`
- `jurisdiction`
- `discipline`
- `family_id` / `work_id`
- `instrument_id`
- `instrument_kind`
- `authority_role`
- `revision_label`
- `effective_date`
- `supersedes_instrument_id` (optional)
- `implements_work_id` (optional)

## Graph semantics to add later
- `work_has_instrument`
- `instrument_manifested_as_source`
- `instrument_implements_work`
- `instrument_amends_instrument`
- `instrument_governs_concept`

## Placement in pipeline
1. classification / authority resolution
2. canonicalization
3. extraction / review / promotion
4. graph build
5. grouped query / explorer behavior

## Why this stage ordering
Identity must be resolved before graph build so the graph consumes normalized meaning instead of trying to dedupe late.

## Smallest safe implementation slice
1. write spec + bounded family registry for the 4-law pilot
2. extend canonical source metadata for those four families
3. extend graph contract minimally to represent work/instrument/source edges
4. validate with bounded pilot only

## Success criteria
- one semantic family per law family
- distinct law vs IRR identity preserved
- no duplicate semantic “PD-1096” drift
- design generalizes across AEC disciplines without subject-specific middleware
