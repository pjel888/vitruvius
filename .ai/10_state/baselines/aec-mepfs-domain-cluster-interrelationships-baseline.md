---
task: aec-mepfs-domain-cluster-interrelationships
phase: 02
created: 2026-05-01
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Baseline — AEC-MEPFS Domain Cluster Interrelationships

## Baseline source
- Latest file-backed shadow staging inspected: 06_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T094129Z/.
- Authoritative fixture: scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json.

## Baseline metrics
- Fixture records: 9,880 admitted BackboneNode records.
- Fixture relationships: 13,285 governed relationships.
- Predicate distribution: roader_than 9,856; has_facet 1,532; maps_to_external_standard 739; 
equires 567; constrains 379; governs 104; part_of 92; pplicable_in_jurisdiction 12; conflicts_with 2; supersedes 2.
- Source-rights rows: 106.
- Resolver golden cases: 117.
- Current graph artifact: 9,880 nodes and 13,285 edges.

## Baseline quality observations
- The graph is broad, but many learner-facing edges still rely on broad governed predicates instead of explicit mechanism metadata.
- Existing schema allows extra relationship metadata without introducing new predicates; the predicate registry remains the governed compatibility layer.
- Canonical architect↔work links do exist through has_facet in the architecture interconnectivity slice, but the user-observed concern remains valid: edge labels are not mechanism-rich enough to distinguish designed_by, engineered_by, work_uses_material, or work_exemplifies_system without metadata.
- Existing hard blockers remain: no production Neo4j/live graph promotion, no KG rebuild/reset, and no protected source payload admission.
