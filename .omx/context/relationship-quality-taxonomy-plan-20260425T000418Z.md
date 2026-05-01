---
task: relationship-quality-taxonomy-plan
created: 2026-04-25T00:04:18Z
status: context-snapshot
---

# Relationship Quality and Taxonomy Context

## Task Statement

Plan how to evaluate and improve KG relationship quality for the current laws-only Explorer graph, using the repository taxonomy correctly.

## Desired Outcome

Produce a bounded plan that distinguishes current operational taxonomy assets from the planned taxonomy-governance backbone, then sequences relationship-quality improvements without bulk-validating shallow edges.

## Known Evidence

- Latest laws-only snapshot: `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`.
- Snapshot counts: 313 canonical nodes, 88 concepts, 214 rules, 432 relationship assertions, 734 fast edges.
- Relationship assertions: 214 `DEFINED_BY`, 214 `SUPPORTED_BY`, 3 `REQUIRES`, 1 `RELATED_TO`.
- Only 4 semantic assertions exist in the current laws-only snapshot (`REQUIRES` and `RELATED_TO`).
- Concepts with `taxonomy_path`: 88/88.
- Rules with `taxonomy_path`: 214/214.
- Current taxonomy corpus counts: 11 taxonomy root files, 23 topic files, 54 subtopic files, 88 concept files under `003_Canonical-Knowledge-Layer/shared/`.
- `TaxonomyLoader` loads `shared/taxonomy/*.md` and `shared/concepts/*.md`; topic/subtopic nodes are virtualized from `taxonomy_path` by the Neo4j loader.
- Planned taxonomy-governance backbone exists in planning/spec artifacts, but `config/vitruvius.yaml` has `k_taxonomy_v2: false`, `k_vitruvian_context: false`, and `k_backbone_validation: false`.
- `003_Canonical-Knowledge-Layer/backbone/` is not present in the repo.

## Constraints

- Do not mutate the current in-progress Explorer UI patch while planning.
- Do not treat the planned backbone as live runtime truth.
- Do not accommodate legacy taxonomy behavior as a product requirement. Vitruvius is pre-launch; old taxonomy paths may be used only as migration evidence or temporary source material, not as a compatibility contract.
- Prefer implementing the intended taxonomy-governance architecture and replacing stale legacy behavior over maintaining parallel legacy/current paths.
- Do not bulk-validate current relationship candidates to improve numbers.
- Keep source-faithful labels and evidence separate from relationship presentation.
- Relationship improvements must remain auditable and evidence-backed.

## Likely Touchpoints

- `.ai/06_specs/relationship-schema.md`
- `.ai/06_specs/vitruvian-context/01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md`
- `003_Canonical-Knowledge-Layer/shared/taxonomy/`
- `003_Canonical-Knowledge-Layer/shared/topics/`
- `003_Canonical-Knowledge-Layer/shared/subtopics/`
- `003_Canonical-Knowledge-Layer/shared/concepts/`
- `scripts/vitruvius/kg/evidence_materializer.py`
- `scripts/vitruvius/kg/unified_snapshot_builder.py`
- `scripts/vitruvius/kg/quality_report.py`
- `scripts/vitruvius/relationships/llm_proposer.py`
- `scripts/vitruvius/relationships/phase_5e_merger.py`
- `scripts/vitruvius/relationships_sections.py`
- `api/index.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`

## Open Questions

- Should relationship improvement first target same-subject semantic edges inside `001-Laws`, or should it wait until multiple subjects are admitted for cross-subject enrichment?
- What threshold should define “good enough” semantic density for Explorer use?
- Which predicates should be admitted in the bounded first pass: `REQUIRES`, `CONSTRAINS`, `APPLIES_TO`, `REGULATED_BY`, or another narrower set?
