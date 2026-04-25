---
task: aec-mepfs-backbone
phase: readiness-history-blast-radius-audit
created: 2026-04-25
author: CODEX
status: DRAFT
---

# Readiness Artifact History And Blast-Radius Audit

## Purpose

This audit ties the readiness artifacts back to historical Vitruvius evidence so
the AEC-MEPFS Backbone plan does not repeat the current graph failures.

This is a documentation and planning audit only. It authorizes no code edits,
Neo4j writes, graph rebuild, feature-flag change, or derived-artifact cleanup.

## Historical Evidence Reviewed

| Evidence | Key finding used by this packet |
|---|---|
| `.ai/02_audits/2026-04-25_taxonomy_first_relationship_quality_audit.md` | Laws-only graph had 313 canonical nodes, 432 relationship assertions, and only 4 semantic relationship assertions; `DEFINED_BY` and `SUPPORTED_BY` dominated relationship quality. |
| `.ai/02_audits/2026-04-24_kg_relationship_quality_and_graph_ux_audit.md` | Prior relationship registry/schema drift produced lossy mappings and shallow `RELATED_TO` behavior; display labels and source labels needed separate handling. |
| `.ai/02_audits/2026-04-24_post_laws_kg_rebuild_relationship_graph_audit.md` | Clean 001-Laws rebuild proved the MVP graph could be isolated to 001-Laws, but semantic edges remained mostly structural/provenance edges. |
| `.ai/02_audits/2026-04-25_explorer_graph_controls_and_rule_labels_audit.md` | Explorer UX fixes are separate from canonical naming and relationship truth; graph control fixes must not imply taxonomy readiness. |
| `.ai/03_plans/taxonomy-governance/00_locked_decisions.md` | Locked decisions require Layer-3 backbone source, opaque VTN IDs, no jurisdiction fork, additive `/v2`, shadow-first rollout, read-only resolver, and no vague cross-domain predicates. |
| `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_cleanup_and_blast_radius_plan.md` | Blast radius spans canonical knowledge, KG schemas/builders, Neo4j loading, API routes, Explorer graph types, tests, feature flags, and derived artifacts. |

## Failure Modes To Avoid

- Treating document-derived rule titles as concept names.
- Treating `DEFINED_BY` and `SUPPORTED_BY` provenance as semantic graph quality.
- Using broad `RELATED_TO` edges when a typed relationship is required.
- Flipping `k_taxonomy_v2` before committed backbone files and validators exist.
- Rebuilding or cleaning Neo4j before shadow graph, parity, rollback, and
  monitoring evidence exist.
- Letting PH or any jurisdiction become a forked taxonomy instead of an overlay.
- Copying licensed standards into canonical files without rights clearance.
- Allowing the resolver to choose legal winners for equal-force conflicts.

## Artifact Implications

| Artifact | Historical constraint now carried forward |
|---|---|
| `standards-legal-source-pack.md` | Source families stay reference/crosswalk unless rights allow deeper use; mirrors are discovery aids, not source truth. |
| `master-taxonomy-l1-l2-decision-record.md` | L1/L2 is authored and human-locked; document titles and legacy taxonomy roots are migration inputs, not canonical truth. |
| `relationship-predicate-registry-draft.md` | Predicate promotion must reject vague or lossy edges and separate semantic, provenance, facet, and review-state relationships. |
| `governance-editorial-control-pack.md` | AI remains proposer/auditor only; named humans and release controls are required before score `3`. |
| `vitruvian-context-resolver-pack.md` | Resolver is read-only, deterministic, no-LLM hot path, and must return conflicts instead of inventing precedence. |
| `taxonomy-authoring-migration-qa-pack.md` | Migration uses workbooks, staging, and golden datasets before broad AI classification. |
| `philippines-overlay-pilot-pack.md` | Philippines law, zoning, hazards, and project constraints are overlays over the global backbone. |

## Blast-Radius Map

| Surface | Risk if implementation starts early | Required later evidence |
|---|---|---|
| Layer 3 canonical knowledge | Polluted backbone, duplicate concepts, unstable labels | accepted backbone source files and validators |
| KG schemas/builders | Broken snapshot shape or lossy predicate mapping | impact map for `TaxonomyLoader`, `UnifiedSnapshotBuilder`, `CanonicalNode`, and assertion models |
| Neo4j load/storage | Current Explorer MVP graph lost or mixed with shadow data | shadow topology, backup/export evidence, restore proof |
| API | v1 consumer regressions or ambiguous resolver contract | additive `/v2` contract and v1 parity suite |
| Explorer | unreadable graph, duplicate names, broken copy/detail workflows | Backbone perspective contract and visual smoke checks |
| Feature flags | false sense of readiness from flag-only activation | committed backbone corpus, validators, shadow parity |
| Tests/observability | readiness claims without reproducible proof | exact verification commands, fixtures, reports, latency budgets |

## Current Limitations

- GitNexus and code-review-graph MCP tools were not exposed through the available
  MCP surface. Fresh GitNexus CLI evidence was later captured in
  `code-intelligence-impact-map.md`; this historical audit remains a
  document-level blast-radius record.
- Philip Lewis is now assigned as the readiness steward/source owner in
  `governance-editorial-control-pack.md` and `standards-legal-source-pack.md`.
  Independent second reviewer, legal/licensing reviewer, and discipline reviewer
  roles remain unfilled required gates.
- Source-rights statuses are planning classifications, not legal clearance.
- No canonical backbone content has been admitted.

## Pass / Fail Gate

Pass:

- historical KG failure modes are visible in the readiness packet
- scorecard remains conservative while owners, registries, fixtures, source
  clearance, and impact maps are incomplete
- blast radius remains documentation-only until a later execution packet

Fail:

- an implementation begins from these drafts without a fresh code-intelligence
  impact map
- the scorecard reaches `ready for bounded implementation` without owner,
  predicate-registry, source-rights, shadow, parity, and rollback evidence
