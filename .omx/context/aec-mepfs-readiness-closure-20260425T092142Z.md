---
task: aec-mepfs-readiness-closure
created_utc: 20260425T092142Z
mode: ralph
status: active
---

# AEC-MEPFS Readiness Closure Context

## Task Statement

Close the next AEC-MEPFS Backbone readiness gaps without starting runtime
implementation.

## Desired Outcome

- R4 has fresh GitNexus/code-impact evidence recorded.
- Governance/source gaps have named accountable owners and approval roles.
- Draft readiness specs are promoted only where supportable.
- A separate bounded implementation packet exists for the first actual code
  slice.
- No Neo4j write, graph rebuild, feature-flag change, or runtime implementation
  is performed.

## Known Facts / Evidence

- The packet lives under `.ai/03_plans/AEC-MEPFS-Backbone/`.
- Current readiness scorecard is `2.00` with verdict `not ready`.
- Final prior Kimi review approved README/packet alignment after fixes.
- Final prior architect review approved the README shadow-first cleanup sequence.
- Root README now treats KG v2 as the current MVP and blocks direct Backbone
  activation.
- `.omx/plans/aec-mepfs-backbone-readiness-plan-20260425T010419Z.md` mirrors the
  canonical readiness plan.

## Constraints

- Documentation/readiness/control artifacts only.
- Do not run Neo4j writes, graph rebuilds, destructive cleanup, backup/restore,
  or feature-flag changes.
- Respect locked decisions in `.ai/03_plans/taxonomy-governance/00_locked_decisions.md`.
- Do not revert unrelated dirty work, including `explorer/package.json`.

## Unknowns / Open Questions

- Whether GitNexus index is current and whether CLI impact/detect commands are
  available in this shell.
- Which named human owners can be assigned beyond the known repository owner,
  Philip Lewis.
- Which specs can honestly move from draft to accepted without overclaiming.

## Likely Codebase Touchpoints

- `scripts/vitruvius/kg/evidence_materializer.py::TaxonomyLoader`
- `scripts/vitruvius/kg/unified_snapshot_builder.py::UnifiedSnapshotBuilder`
- `scripts/vitruvius/kg/schemas.py::CanonicalNode`
- `scripts/vitruvius/kg/neo4j_loader.py::Neo4jLoader`
- `scripts/vitruvius/kg/relationship_enricher.py`
- `api/index.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/components/*`
- `config/vitruvius.yaml`
