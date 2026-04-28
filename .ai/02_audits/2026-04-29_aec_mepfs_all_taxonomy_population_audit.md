---
task: aec-mepfs-all-taxonomy-population-audit
phase: AEC-MEPFS taxonomy expansion
status: completed
created: 2026-04-29
---

# AEC-MEPFS All-Taxonomy Population Audit

## Current implementation surface

Primary authored fixture:

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`

Generated evidence surfaces:

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/<run-id>/`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/<run-id>/`
- `006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/<run-id>/`

## Baseline before this slice

- Starting commit: `c5b52c4f`
- Latest pre-expansion run used by API/Explorer tests: `20260428T144427Z`
- Fixture counts: 2697 `BackboneNode` records, 2673 `broader_than` relationships, 24 roots, max depth 4.
- Level counts: L1 24, L2 261, L3 804, L4 1608.
- Architecture had been expanded to 374 nodes, but most non-Architecture roots remained at uniform 101-node scaffolds.

## Gap

The Explorer now exposes the AEC-MEPFS graph by default, so sparse branches make the product feel incomplete. The user specifically requested more comprehensive coverage for all taxonomies, including Sanitary Engineering, Electrical Engineering, Security, Smart Systems, Heritage Conservation, Laws, and world-history Architecture branches.

## Safety and governance controls

- Add only `BackboneNode` metadata records.
- Preserve existing max depth 4 and `broader_than` hierarchy pattern.
- Use public professional, accreditation, curriculum, code-family, and filename-level source signals only.
- Do not copy protected source text, standards clauses, tables, figures, datasets, or exam questions.
- Do not mutate Neo4j.
- Do not rebuild/reload/reset KG.
- Do not alter API runtime behavior.
- Do not alter Explorer runtime behavior.
- Regenerate file-backed shadow staging and route inventory evidence for the new counts.

## Audit conclusion

The all-taxonomy expansion is safe as a bounded metadata-only population slice. It substantially deepens all AEC-MEPFS roots while preserving existing runtime and source-rights boundaries.
