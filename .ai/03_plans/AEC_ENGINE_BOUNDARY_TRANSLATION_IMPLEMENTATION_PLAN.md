---
title: AEC Engine Boundary Translation Implementation Plan
type: subsystem-plan
task: aec-engine-boundary-translation
phase: "05"
status: accepted
created: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/boundary/dto.py
  - scripts/vitruvius/aec/boundary/importers.py
  - scripts/vitruvius/aec/boundary/exporters.py
  - scripts/vitruvius/aec/boundary/ifc_mapping.py
repo_grounding:
  - scripts/vitruvius/spatial/schema.py
  - scripts/vitruvius/spatial/concept_mapper.py
  - scripts/vitruvius/spatial/contract_reader.py
  - scripts/vitruvius/ontology/ifc_registry.py
  - scripts/vitruvius/ontology/ifc_mapping.yaml
  - spatial-daemon/src/contract_writer.ts
  - spatial-daemon/src/types.ts
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/07_BOUNDARY_TRANSLATION_PROTOCOL.md
  - .ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
---

# AEC Engine Boundary Translation Implementation Plan

## 0. Planning Status
- status: accepted
- execution role: selected for first bounded slice
- current use: authoritative subsystem plan for the bounded first-slice sprint

## 1. Scope
Translate external payloads such as IFC/CAD/OWL-adjacent data into canonical AEC DTOs and export bounded audit-safe payloads back out.

This layer owns mediation at the repo boundary.
It does not own internal truth.

## 2. Current Repo Anchors
- `scripts/vitruvius/spatial/schema.py` already validates imported spatial payloads
- `scripts/vitruvius/spatial/concept_mapper.py` already maps payload concepts into canonical concepts
- `scripts/vitruvius/ontology/ifc_registry.py` and `ontology/ifc_mapping.yaml` already show static IFC mapping patterns
- `spatial-daemon/src/types.ts` and `contract_writer.ts` already define and emit a bounded JSON contract

## 3. Planned Code Locations
- `scripts/vitruvius/aec/boundary/dto.py`
- `scripts/vitruvius/aec/boundary/importers.py`
- `scripts/vitruvius/aec/boundary/exporters.py`
- `scripts/vitruvius/aec/boundary/ifc_mapping.py`

## 4. V1 Supported External Surface
- one canonical DTO family for building-scale spatial/model slices
- bounded IFC class/property-set mapping
- JSON contract emission with schema versioning and integrity footer where the spatial boundary is used

Explicitly not in v1:
- broad IFC round-trip fidelity
- generic CAD kitchen-sink import
- automatic schema inference from arbitrary vendor exports

## 5. Responsibilities
- canonical DTO definition
- importer validation
- exporter validation
- versioned mapping tables
- conversion diagnostics and refusal reasons

## 6. Boundaries
- must not redefine internal engine truth around IFC terms
- must not infer legal rules from imported geometry
- must not write directly into ECS internals without DTO validation
- must not bypass the spatial integrity footer on file-based contracts

## 7. Inputs / Outputs

### Inputs
- external model payloads
- mapping tables and schema versions
- canonical concept registries

### Outputs
- canonical AEC DTOs
- export payloads
- mapping diagnostics
- refusal artifacts for unsupported inputs

## 8. Data Contracts
- `schema_version`
- `import_manifest_id`
- `frame_id`
- `unit_system`
- `canonical_concept_id`
- `mapping_diagnostic`

## 9. Dependencies
- AEC master plan
- cross-language boundary contract
- spatial kernel plan
- knowledge vault plan where rule-linked metadata is involved

## 10. Ordered Implementation Steps
1. Freeze the canonical DTO family and its versioning policy.
2. Reuse existing spatial schema and concept-mapping patterns as precedent.
3. Implement importer adapters with explicit refusal reasons for unsupported inputs.
4. Keep IFC mapping tables declarative and versioned.
5. Preserve integrity-footer parity when the spatial file contract is used.
6. Add export surfaces only after import is deterministic and validated.

## 11. Edge Cases
- unsupported IFC classes
- unit-system mismatches
- missing frame declarations
- imported objects that map to no canonical concept
- partial payloads that validate structurally but not semantically

## 12. Risks
- external schema becomes internal law by convenience
- mapping tables drift without versioning
- TypeScript and Python disagree on contract schema or footer rules
- refusal behavior is inconsistent across import paths

## 13. Validation Plan

### Existing Tests To Reuse
- `python -m pytest scripts/tests/test_spatial_schema.py`
- `python -m pytest scripts/tests/test_spatial_contract_reader.py`
- `python -m pytest scripts/tests/test_spatial_concept_mapper.py`
- `npm test && npm run typecheck` from `spatial-daemon/`

### New Tests Required
- `scripts/tests/test_aec_boundary_dto.py`
- `scripts/tests/test_aec_boundary_ifc_mapping.py`
- `scripts/tests/test_aec_boundary_refusals.py`
- `scripts/tests/test_aec_boundary_contract_parity.py`

### Acceptance Gates
- unsupported inputs fail explicitly with diagnostics
- Python and TypeScript remain in schema/footer parity where relevant
- canonical DTOs are stable across repeated imports of the same payload

## 14. Performance Considerations
- optimize only after DTO correctness is stable
- keep mapping tables declarative and cacheable
- do not introduce heavy parser dependencies into default CLI paths

## 15. Execution Checklist
- [ ] canonical DTO family frozen
- [ ] importer refusal taxonomy frozen
- [ ] mapping tables versioned
- [ ] spatial footer parity preserved
- [ ] exporter surfaces still bounded to supported DTO family
- [ ] new `test_aec_boundary_*` suite added

## 16. Stop Conditions
- internal truth begins mirroring IFC naming or structure directly
- frame or units metadata are missing
- TypeScript/Python contract parity cannot be maintained
- importer accepts payloads it cannot explain or map
