# 2026-04-16 Laws Mini Dataset→Graph Pipeline M1 Validation

## Outcome
- Verdict: **PARTIAL**
- M1 status: **implemented**
- M2 trigger: **not hit**

Why `PARTIAL` instead of `SUCCESS`:
- the scoped graph proof is truthful, leakage-safe, isolated, and queryable
- `PD-1096` is covered by selected canonical/promoted inputs
- `RA-9514`, `BP-344`, and `BP-220` are present in the manifest and final reporting, but remain **blocked** because no truth-bearing canonical/promoted inputs were admitted for them in M1

## Pre-edit authority / readiness check
- Truth reconciliation completed first:
  - `/.ai/05_logs/2026-04-16_laws-mini-dataset-truth-reconciliation-validation.md`
- M1 readiness gate re-checked on the current commit after reconciliation:
  - path map exists
  - blast-radius matrix exists
  - manifest contract and metadata schema are explicit
  - relationship input policy is explicit
  - scoped query/export selector choice is explicit
  - freshness semantics are explicit
  - anti-special-case + low-spec rules are explicit
- Result: **GO for bounded M1 only**

## GitNexus / impact analysis
Fresh status before coding:
- `npx --yes gitnexus@1.6.2-rc.10 status` → `Status: ✅ up-to-date`
- `gitnexus detect_changes` note: the installed GitNexus CLI in this environment does **not** expose a `detect_changes` command, so scope verification fell back to fresh `status`, `impact`, `git diff --stat`, and `git diff --check`

Impacts checked before edits:
- `build_parser` → LOW
- `run_build_graph` → LOW
- `build_snapshot` → **HIGH** (directly affects graph tests + CLI path)
- `_load_snapshot_or_fail` → **HIGH** (shared query loader)
- `run_query` / `run_query_structured` / `run_export_graph_snapshot` / `run_export_graph_owl` → LOW

High-risk note:
- `build_snapshot` and `_load_snapshot_or_fail` were the only HIGH-risk touchpoints, so the implementation stayed additive and was followed by focused builder/query/backcompat tests.

## Implemented scope
### Code / config changes
- `config/datasets/laws-core-bundle-m1.yaml`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/graph/contract.py`
- `scripts/vitruvius/graph/snapshot.py`
- `scripts/vitruvius/graph/builder.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/graph/dataset_manifest.py`
- `scripts/vitruvius/query/cli.py`
- `scripts/vitruvius/ontology/cli.py`
- targeted tests under `scripts/tests/`

### What M1 now supports
- explicit dataset manifest contract
- manifest-selected scoped graph build
- dataset-scoped snapshot + integrity + build report outputs
- explicit `--snapshot` query selection for `query`, `query-structured`, and `query-graph`
- explicit `--snapshot` / `--out` export selection for `export-graph-owl`
- manifest-hash + input-fingerprint freshness linkage embedded in dataset snapshot metadata

## Primary evidence artifacts
### Scope identity
- dataset manifest: `config/datasets/laws-core-bundle-m1.yaml`
- manifest hash: `27f68c8d41b82c802a63b465f0c2117c1ed9ad7adfc7681c983b9b513bc07f62`
- selected input fingerprint hash: `9dc8fd34e62c1d0ba1afe56722a62b1e00bce14c793ad51184c099b7e3c259b4`

### Scoped outputs
- snapshot: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T042225Z_graph_snapshot.json`
- integrity: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T042225Z_graph_integrity_report.json`
- build report: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/20260416T042225Z_build_graph_dataset_report.json`
- Turtle export: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T042225Z_graph_snapshot.ttl`

## Verification results
### 1. Leakage control
Command/evidence:
- manifest→snapshot subset check verified:
  - source nodes ⊆ selected canonical source ids
  - concept nodes ⊆ selected canonical concept ids
  - relationship edges (non-synthetic) ⊆ selected relationship input ids

Observed result:
- `unexpected_source_nodes = []`
- `unexpected_concept_nodes = []`
- `unexpected_relationship_edges = []`
- synthetic edge count (`rel-meta-*` + `rel-basis-*`) = `17`, all derived from selected source/concept inputs

Verdict: **PASS**

### 2. Artifact isolation
Global artifact hashes before and after dataset build were identical:
- `latest_graph_snapshot.json` → `da95cec5e676cb70bdaeb79e0c372fd6e50223c65fb3d7fa3cd69d3335cc0461`
- `latest_graph_integrity_report.json` → `3964821543ca4d13ba66d4a5fbfed19bac941c69e94e0795d034456d0f84952b`
- `latest_graph_snapshot.ttl` → `ff5ac797373eab42fded00cba2551096c7c3960e6ca4f3fa116f8c1cad371338`

Verdict: **PASS**

### 3. Default/global path preservation
Evidence:
- focused backcompat suite passed (see test command below)
- default global query still works without `--snapshot`
- default global query output does **not** print dataset provenance unless scoped snapshot selection is requested

Verdict: **PASS**

### 4. Freshness / manifest-hash linkage
Dataset snapshot metadata includes:
- `dataset_id`
- `dataset_kind`
- `run_id`
- `manifest_path`
- `manifest_hash`
- `input_fingerprint`
- `upstream_artifact_refs`
- explicit selected snapshot + integrity paths

Dataset query provenance echoes:
- selected snapshot path
- dataset id
- run id
- manifest hash

Verdict: **PASS**

### 5. Integrity
Scoped integrity result from the dataset snapshot:
- `passed: true`
- `warning_count: 0`
- `error_count: 0`
- duplicate node ids: `0`
- dangling edges: `0`

Verdict: **PASS**

### 6. Determinism / replay
Second build run:
- snapshot: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T041338Z_graph_snapshot.json`
- integrity: `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T041338Z_graph_integrity_report.json`

Comparison:
- normalized snapshots equal after removing volatile freshness fields (`generated_at_utc`, `run_id`, selected output paths)
- integrity payloads equal byte-for-byte at the `integrity` object level

Verdict: **PASS**

### 7. Scoped query correctness with seeded questions
Snapshot used for all seeded checks:
- `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T042225Z_graph_snapshot.json`

Seeded evidence-bearing results:
1. `query --snapshot ... "What governs building permit?"`
   - answer: `irr-implementing-rules-and-regulations-of-the-national-building-code`, `law-national-building-code-of-the-philippines`
   - provenance block present with dataset id / run id / manifest hash
2. `query-structured --snapshot ... --function what_requires --subject concept-stairs`
   - answer: `concept-fire-resistive-construction`
3. `query-structured --snapshot ... --function what_affects --subject concept-floor-area`
   - answer: `concept-building-height`, `concept-stairs`
4. `query-structured --snapshot ... --function what_defines --subject concept-building-permit`
   - answer: `law-national-building-code-of-the-philippines`
5. `query-graph --snapshot ... --from irr-implementing-rules-and-regulations-of-the-national-building-code --to concept-building-permit --max-depth 1`
   - `path_count: 1`
   - JSON payload includes `snapshot_provenance`

Seeded hit rate:
- `5 / 5` evidence-bearing checks succeeded

Verdict: **PASS**

### 8. Bundle completeness / per-folder coverage
Per-folder coverage from the dataset build report:
- `PD-1096` → `covered` (`raw_file_count=15`, `canonical_count=23`, `approved_relationship_input_count=31`, `node_count_contributed=21`, `edge_count_contributed=47`)
- `RA-9514` → `blocked`
- `BP-344` → `blocked`
- `BP-220` → `blocked`

Missing bundle members were not hidden; they are surfaced as blocked.

Verdict: **PASS** for honesty, **not full success** for bundle completeness

### 9. Thin-graph metrics
From the dataset build report:
- connected components: `1`
- isolated nodes: `0`
- isolated node rate: `0.0`
- edge type diversity: `6` (`affects`, `defines`, `depends_on`, `governs`, `implements`, `requires`)

Thin-graph interpretation:
- the scoped graph is useful and queryable
- however the bundle is not fully covered across all four folders, so the overall pilot remains `PARTIAL`

## Low-spec observation
See: `/.ai/00_performance/2026-04-16_laws-mini-dataset-m1-low-spec-observations.md`

Key figures from the dry-run bounded build:
- wall time: `0.21 s real`
- peak memory footprint: `17,023,384 bytes`
- max resident set size: `26,198,016 bytes`

Verdict: **PASS** for the planning-level 8 GB M2-class budget

## Targeted validation command results
- `PYTHONPATH=scripts pytest -q scripts/tests/test_graph_builder.py scripts/tests/test_graph_snapshot.py scripts/tests/test_graph_cli.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_query_cli.py scripts/tests/test_ontology_owl_cli.py scripts/tests/test_pipeline_cli_byte_identity.py` → **56 passed in 2.86s**
- `python3 scripts/pipeline_cli.py build-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml` → **PASS**
- `python3 scripts/pipeline_cli.py export-graph-owl --snapshot 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T042225Z_graph_snapshot.json --out 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T042225Z_graph_snapshot.ttl` → **PASS**
- `python3 scripts/pipeline_cli.py query-structured --function what_governs --subject concept-building-permit` (default/global path) → **PASS**

## Post-deslop note
- The mandatory Ralph deslop pass was limited to the changed files only.
- Final cleanup change was restricted to `scripts/vitruvius/graph/dataset_manifest.py`:
  - removed an unused import
  - factored repeated manifest-entry parsing into a helper
  - tightened invalid-manifest list-item validation
- Regression suite + runtime checks were rerun after the cleanup and remained green.

## M1→M2 boundary decision
- M1 completed using manifest-selected approved relationship inputs.
- No dataset-scoped review/promotion rewrite was required to make the proof truthful.
- Therefore the accepted M1→M2 trigger was **not** hit.

Decision: **defer M2**

## Final judgment
M1 is **implemented and validated as `PARTIAL`**.

What is proven:
- dataset manifest contract is real and generic
- dataset-scoped graph build is additive and isolated
- scoped snapshot selection for query/export works
- manifest-hash freshness linkage is explicit
- default/global behavior is preserved when dataset mode is unused

What is not yet proven:
- full four-folder truth-bearing coverage for `RA-9514`, `BP-344`, and `BP-220`
- any need for M2 review/promotion scoping
