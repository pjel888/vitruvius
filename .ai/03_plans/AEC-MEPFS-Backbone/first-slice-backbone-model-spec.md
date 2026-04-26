---
task: aec-mepfs-backbone
phase: first-slice-model-spec
created: 2026-04-26
author: CODEX
status: ACCEPTED-SHADOW-SPEC
---

# First-Slice Backbone Model Spec

## Purpose

Define the minimum admitted `BackboneNode` model for the first AEC-MEPFS
shadow-staging slice.

This spec authorizes file-backed shadow fixtures and validators only. It does
not authorize production runtime registries, Neo4j writes, protected source
ingest, graph rebuilds, default Explorer adoption, or broad ontology expansion.

## Admitted BackboneNode Fields

Every `BackboneNode` with `review_status` equal to `admitted` or
`steward_admitted` must carry:

- `id`
- `canonical_id`
- `record_type`
- `review_status`
- `label`
- `pref_label`
- `definition`
- `path_code`
- `level`
- `parent_path_code`
- `owner`
- `steward`
- `release_version`

Optional fields:

- `aliases`
- `scope_note`
- `example_concepts`

## Invariants

- `id` must equal `canonical_id`.
- `label` must equal `pref_label`.
- `owner` must equal `steward`.
- `canonical_id` must match `VTN-DOM-0000000` style IDs.
- `path_code` must be dot-delimited uppercase three-letter segments.
- `level` must equal the number of path segments.
- L1 records must have no `parent_path_code`.
- L2-L4 records must have a `parent_path_code`.
- A child `parent_path_code` must equal the path prefix before the final
  segment.
- A child parent must exist in the same admitted fixture.
- Duplicate admitted `id` and `path_code` values are invalid.
- Jurisdiction fields are forbidden on canonical BackboneNode records.
- L1/L2 fixture rows are authored from accepted planning records, not extracted
  from document-derived rule titles.

## First Fixture Boundary

The first fixture may include only a small authored L1/L2 subset from
`master-taxonomy-l1-l2-decision-record.md`.

The first fixture must not try to complete the entire AEC universe. It exists to
prove:

- ID/path stability
- parent/child integrity
- steward ownership fields
- file-backed shadow staging
- read-only preview shape

## Runtime Boundary

Passing this model spec means a fixture can enter shadow staging. It does not
mean:

- the Backbone is production-canonical
- the Explorer graph should switch defaults
- Neo4j should load Backbone nodes
- source/legal clearance is complete
- document classifications can be automatically admitted
