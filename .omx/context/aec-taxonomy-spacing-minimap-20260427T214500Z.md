# Ralph Context Snapshot — AEC taxonomy expansion, spacing control, minimap refresh

- Task statement: Expand the AEC-MEPFS taxonomy with additional top-level domains requested by project owner (Sanitary Engineering, Security, Smart Systems, Heritage Conservation, Laws) and add Explorer graph spacing/bounding-circle controls while preserving the minimap filter refresh fix already in progress.
- Desired outcome: Explorer shows a denser, rights-safe AEC-MEPFS taxonomy; graph can be interactively expanded/compressed; minimap tracks node-type filter changes.
- Known facts/evidence: Current fixture has 779 records / 760 relationships / 19 roots / 190 L2 / 570 L3. Current Explorer performance fixes at HEAD df8232d9. Minimap snapshot currently ignored hidden/filter state; local edit added overviewSnapshot helper but not yet verified.
- Constraints: no protected payload ingestion/exposure; no Neo4j mutation; no KG rebuild/reload/reset; no Gemini; use file-backed fixture/evidence only; Windows-safe filenames.
- Unknowns/open questions: exact count after expansion to be determined by deterministic appendix; tests/docs must be updated consistently.
- Likely touchpoints: scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json, scripts/tests/test_kg_backbone_contracts.py, api/v2Backbone.test.ts, explorer tests/components, GraphScene, VisNetworkHost, useSceneStore, evidence logs/manifests.
