# ACS External-Gated Gap Scaffold Validation

Date: 2026-05-01

## Scope

Implemented the requested non-critical and externally gated Architecture-Civil-Structural remaining gaps that can be safely closed inside the repo. This pass is file-backed and metadata-only. It does not mutate production Neo4j, rebuild/reset the KG, ingest protected payloads, admit numerical criteria, or apply canonical duplicate merges/aliases.

## Implemented

- Added 4 ACS nodes: `CIV.RDC.PED.ATI`, `CIV.HDI.CCD.CDI`, `CIV.PAV.PSI`, and `STR.LOA.CBG`.
- Added 25 governed relationships net: 21 typed non-hierarchy relationships plus 4 hierarchy relationships.
- Added resolver cases `RES-ACS-016` through `RES-ACS-018`.
- Added gated-review runner `scripts/vitruvius/kg/architecture_civil_structural_gate_review.py`.
- Added gated-review tests for duplicate review, numeric criteria packet validation, authority ledger validation, payload-leak blocking, non-`.json` JSON payload scanning, positive authority-ledger dry-run validation, raw-source output rejection, and non-report-root output rejection.
- Updated ACS quality gates to require public-way, culvert, pavement/subgrade, structural criteria gate, rainfall-basis, and drainage-maintenance relation types/traversals.

## Metrics

- Backbone nodes: 10,014 -> 10,018.
- Governed relationships: 13,645 -> 13,670.
- Source-rights rows: 123 -> 123.
- Resolver golden cases: 139 -> 142.
- ACS introduced nodes: 75 -> 79.
- ACS typed non-hierarchy relationships: 122 -> 143.
- ACS hierarchy relationships: 75 -> 79.
- Self-loops: 0.
- Generic relationships: 0.
- Introduced non-hierarchy orphans: 0.
- Quality score: 100/100.

## Validation commands

- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.backbone_shadow_staging --run-id 20260501T082100Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` - passed.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.backbone_graph_quality --run-id 20260501T082200Z_ACS_EXTERNAL_GATED_GAP_GRAPH_QUALITY --introduced-generation-method steward_governed_architecture_civil_structural_interrelationships_from_source_family_research --source-rights-registry .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` - passed, 0 errors.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.architecture_civil_structural_quality --run-id 20260501T082300Z_ACS_EXTERNAL_GATED_GAP_QUALITY` - passed, 100/100.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.backbone_resolver_qa --fixture scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json --run-id 20260501T082400Z_ACS_EXTERNAL_GATED_GAP_RESOLVER_QA` - passed, 142/142 resolver cases.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.architecture_civil_structural_gate_review --run-id 20260501T083500Z_ACS_GATED_REVIEW_HARDENED` - passed, 0 errors, 514 duplicate candidate groups exported, no admission/mutation.
- `$env:PYTHONPATH='scripts'; python -m pytest -q scripts/tests/test_kg_architecture_civil_structural_enrichment.py scripts/tests/test_kg_architecture_civil_structural_gate_review.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_backbone_graph_quality.py scripts/tests/test_kg_backbone_shadow_staging.py` - 105 passed.

## Tooling and review notes

- `docs/shared/agent-tiers.md` remains missing; Ralph/Ultrawork used local delegation judgment.
- Kimi CLI did not produce a usable review. Attempts returned no review, hit a Windows encoding error on a Unicode arrow, or reached the step limit without final critique.
- GitNexus impact for new/untracked ACS gate/enrichment symbols returned UNKNOWN because GitNexus did not resolve those new symbols even after refresh. This is recorded; blast radius was mitigated with graph-quality, ACS quality, shadow staging, resolver QA, and targeted pytest.
- Shadow staging initially rejected duplicate edge IDs for two same source-target-predicate pairs. The implementation was corrected by removing those duplicate-predicate additions and relying on existing equivalent mechanism edges.

## Boundaries maintained

- `canonical_label_mutation`: false.
- `numeric_criteria_admission`: false.
- `protected_payload_ingest`: false.
- `live_neo4j_writes`: false.
- `production_promotion`: false.
- `kg_rebuild`: false.
- `$env:PYTHONPATH='scripts'; python -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260501T082100Z` - passed and wrote the consumer report used by API/Explorer surfaces.
- `bun test api` - 118 passed after updating expected node/edge counts and latest shadow run id.
- `bun test explorer` - 106 passed.
