# 2026-04-16 Laws M2A — Source Admission Validation

## Outcome
- Verdict: **PASS for source-admission phase; graph coverage remains partial until relationship inputs exist**
- Scope: admitted truth-bearing canonical source pages for the three previously blocked laws:
  - `RA-9514`
  - `BP-344`
  - `BP-220`

## What was done
### Upstream admission steps
For each selected authoritative law variant:
1. `detect-one`
2. `convert-one`
3. `refine-one`
4. `canonicalize-plan-one`
5. `canonicalize-one`
6. update manifest admission entries
7. rerun scoped dataset graph build

### Selected admission candidates
- `RA-9514` → `RA9514-RIRR-rev-2019.pdf`
- `BP-220` → `Revised_IRR_BP220_2008.pdf`
- `BP-344` → `2024 Revised Implementing Rules and Regulations ... NCDA ... .pdf`

Policy preserved:
- `BP-344 IRR Accessibility Law DPWH.pdf` stayed reference-only
- `DPWH DO037 Enforcement of BP344 along National Roads.pdf` stayed explicit adjacent context, excluded from default canonical admission

## Newly admitted canonical source pages
- `003_Canonical-Knowledge-Layer/shared/sources/implementing-rules-and-regulations-of-the-fire-code-of-the-philippines.md`
- `003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220.md`
- `003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344.md`

## Dataset graph evidence
Latest truthful scoped build:
- snapshot: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T053618Z_graph_snapshot.json`
- integrity: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T053618Z_graph_integrity_report.json`
- report: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/20260416T053618Z_build_graph_dataset_report.json`

Coverage result:
- `PD-1096` → `covered`
- `RA-9514` → `partial` (source node admitted; no relationship-backed edges yet)
- `BP-344` → `partial` (source node admitted; no relationship-backed edges yet)
- `BP-220` → `partial` (source node admitted; no relationship-backed edges yet)

Integrity result:
- `passed: true`
- `warning_count: 3`
- all warnings are orphan source nodes for the newly admitted laws because no law-specific approved relationship inputs exist yet
- build report `incomplete` remains `true`, which is now the truthful contract for source-only admission

Thin-graph note:
- connected components: `4`
- isolated nodes: `3`
- isolated node rate: `0.125`
- this confirms source admission is real, but the newly admitted laws are not yet connected into the graph via relationships

## Verification evidence
- `python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/canonicalize.py scripts/vitruvius/graph/cli.py scripts/vitruvius/graph/dataset_manifest.py` → **PASS**
- `PYTHONPATH=scripts pytest -q scripts/tests/test_canonicalize_body.py scripts/tests/test_canonical_rules_additional_laws.py scripts/tests/test_canonicalize_plan_cli.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_pipeline_cli_byte_identity.py` → **24 passed in 1.82s**
- canonicalize previews for all three new law rules → **PASS**
- scoped graph rebuild with updated manifest → **PASS**

## Global path preservation
Global graph artifact hashes remain unchanged:
- `latest_graph_snapshot.json` → `da95cec5e676cb70bdaeb79e0c372fd6e50223c65fb3d7fa3cd69d3335cc0461`
- `latest_graph_integrity_report.json` → `3964821543ca4d13ba66d4a5fbfed19bac941c69e94e0795d034456d0f84952b`
- `latest_graph_snapshot.ttl` → `ff5ac797373eab42fded00cba2551096c7c3960e6ca4f3fa116f8c1cad371338`

## Interpretation
M2A source admission is now complete enough that the bundle is no longer blocked at the source-page layer.

However, the newly admitted laws remain source-only partial coverage in the scoped graph. That means the next truthful step is still:
- dataset-safe extraction inputs
- dataset-safe review outputs
- dataset-safe promotion inputs / audit refs
- then a scoped graph rerun with law-specific relationships
