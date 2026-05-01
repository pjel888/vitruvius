# Ralph Context Snapshot: AEC-MEPFS Expanded Taxonomy Content

Task statement: Expand the AEC-MEPFS Explorer taxonomy/backbone with many more taxonomies, topics, subtopics, concepts, and rules where supported by the current static backbone model.

Desired outcome:
- The AEC-MEPFS graph becomes substantially more comprehensive across architecture, civil/structural, MEPFS, laws, security, smart systems, sanitary/plumbing, urban planning, heritage conservation, and adjacent AEC domains.
- Existing Explorer/API behavior remains working.
- Generated backbone artifacts, reports, and tests are updated.
- Changes are verified, committed, and pushed.

Known facts/evidence:
- Current primary source fixture: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Generator: `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --repo-root . --run-id <RUN_ID> --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Current expected count from explore: 984 BackboneNode records, 24 roots, 240 L2, 720 L3, 960 broader_than relationships.
- Current commit before this pass: 0f1f641b.

Constraints:
- Do not ingest protected source text/tables/figures/datasets.
- Use public/general taxonomy labels only; avoid copying protected proprietary content.
- Preserve deterministic schema, ID/path conventions, and tests.
- Do not touch Neo4j/KG live mutation paths.

Unknowns/open questions:
- Exact generator behavior for hierarchy/counts and whether concepts/rules are modeled as BackboneNode rows or separate artifacts.
- Which generated artifacts are committed and need refresh for Explorer.

Likely touchpoints:
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/test_kg_backbone_shadow_staging.py`
- `api/v2Backbone.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/graph/VisNetworkHost.test.ts`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/`
- `.ai/05_logs/`
