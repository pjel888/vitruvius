---
task: aec-mepfs-domain-cluster-interrelationships
phase: 04
created: 2026-05-01
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — AEC-MEPFS Domain Cluster Interrelationships

## Findings
- [G001] Graph data lives in scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json; generated read-only artifacts live under 06_System-Manifests/aec-mepfs-backbone/shadow-staging/.
- [G002] Relationship predicates are intentionally constrained by scripts/vitruvius/kg/backbone_contracts.py and .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json.
- [G003] Existing architecture interconnectivity added person-work-material paths, but mechanism semantics are compressed into has_facet; the graph needs richer optional edge metadata rather than new predicates.
- [G004] The current graph has no generic 
elated_to governed predicates, but most edge metadata coverage is sparse outside generation/provenance notes.
- [G005] API uildShadowBackboneTaxonomyPreview has HIGH GitNexus upstream impact, so this pass should avoid API route-shape edits unless strictly necessary.
- [G006] _build_shadow_graph has LOW GitNexus upstream impact and can safely preserve optional relationship metadata in generated graph artifacts when present.
- [G007] Source-rights rows already cover broad ASHRAE/NFPA/IFC/WBDG categories, but BOT, Brick, Haystack, CDC Legionella, IAPMO/ASPE plumbing sources need explicit metadata-only rows for this pass.
- [G008] Validation should be additive and file-backed; do not weaken existing contract validation.

## Tooling notes
- mcp__morph_mcp__.codebase_search failed due model context-length error.
- omx explore is unavailable on this Windows host because its harness relies on POSIX wrappers.
- chunkhound research failed because no LLM provider is configured; chunkhound search --regex worked.
- ./scripts/refresh_code_intelligence.sh completed with GitNexus up to date, ChunkHound refreshed, and code-review-graph rebuilt; code-review-graph warned about missing 	ree-sitter-yaml for YAML parsing and ChunkHound emitted one embedding service batch warning.

## Risk conclusion
Proceed with a bounded, file-backed enrichment module, source-rights additions, fixture updates, optional shadow graph metadata preservation, focused validation, focused tests, and generated reports. Do not edit API route behavior because GitNexus reports HIGH impact for the main API preview builder.
