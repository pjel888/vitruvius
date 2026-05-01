# AEC-MEPFS Research Integration Context

## Task Statement

Read the AECMEPFS++ research reports in `.ai/13_research/AECMEPFS++/`,
analyze them, and integrate the useful conclusions into the existing
AEC-MEPFS Backbone readiness/control plan packet.

## Desired Outcome

- Planning-only integration.
- No runtime code, Neo4j, feature flag, rebuild, backup/restore, or cleanup work.
- Existing readiness plan remains the controlling gate.
- New research is folded into the plan packet as evidence, artifact targets, and
  gate refinements.
- Consensus review from architect and critic before finalizing.

## Documents Read

- `.ai/13_research/AECMEPFS++/deep-research-report.md`
- `.ai/13_research/AECMEPFS++/deep-research-report (1).md`
- `.ai/13_research/AECMEPFS++/deep-research-report 3.md`

## Key Findings To Integrate

- Taxonomy-first, graph-second, document-ingestion-third remains the correct
  architecture.
- No external standard should become the Vitruvian backbone; external standards
  should be mapped references/crosswalks.
- The research proposes an 18-domain production backbone plus orthogonal
  lifecycle, asset, performance, geography, knowledge-type, and standards facets.
- The larger AECMEPFS++ tree includes foundational sciences, discipline domains,
  asset/space/system/product domains, process/delivery/compliance domains, and
  information/operations domains.
- Resolver design must be deterministic, traced, and separate from AI proposal
  workflows.
- The Philippines pack should be a jurisdictional overlay system, not a second
  taxonomy.
- Source rights, steward/RACI, change control, release/versioning, AI-use
  policy, review queue, golden datasets, and resolver test suite should become
  readiness deliverables.

## Constraints

- Planning only.
- The current readiness scorecard remains `not ready`.
- The current Explorer/001-Laws MVP remains protected.
- `.ai` holds governance/plans; canonical content belongs in Layer 3, not `.ai`.
- OMX state MCP returned `Transport closed`; this context snapshot is the local
  persistence fallback.

## Likely Plan Touchpoints

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_overhaul_plan.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_cleanup_and_blast_radius_plan.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_knowledge_graph_research.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_plan_validation.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.omx/plans/aec-mepfs-backbone-readiness-plan-20260425T010419Z.md`
