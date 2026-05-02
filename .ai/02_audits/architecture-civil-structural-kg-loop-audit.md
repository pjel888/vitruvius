# Architecture Civil Structural KG Loop Audit

Date: 2026-05-01

## Baseline
Before the ACS loop, the file-backed backbone had 9,939 nodes, 13,459 relationships, 114 source-rights rows, and 124 resolver golden cases. Architecture/Civil/Structural relationships existed but cross-taxonomy traversal for accessible route, roof drainage, geotechnical-to-foundation, load-path, retaining wall, and movement-joint questions was incomplete.

## Findings
- Graph data lives in `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Source/provenance metadata lives in `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`.
- Resolver cases live in `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`.
- Validation surfaces existed but needed ACS quality scoring, source-reference checks, relation-category checks, and traversal tests.
- API default shadow run discovery requires timestamp-only run directories; a timestamp-only run was produced at `20260501T054000Z`.

## Risks
- `buildShadowBackboneTaxonomyPreview` impact was HIGH, so broad API metadata exposure was deferred.
- Historical duplicate normalized labels remain and require a separate cleanup pass.
