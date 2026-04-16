# 2026-04-16 Laws M4 Expansion Path Validation

## Scope actually executed
This validation covers the **accepted minimal M4 slice only**:
- **M4A** — research / audit / spec / plan artifacts
- **M4B** — additive manifest/runtime/reporting support for repeatable `law_units`

It does **not** widen into:
- generic Phase 11 all-laws expansion
- runtime section-scoped graph building
- merged-graph runtime orchestration

## Runtime changes
- `scripts/vitruvius/graph/dataset_manifest.py`
  - added optional `law_units` schema support
  - validated `law_units` against existing classified raw entries and selected admitted source/concept/relationship inputs
  - surfaced `contributing_law_ids` + `law_units` in snapshot metadata and build reports
  - surfaced `contributing_law_ids` in query provenance
- `scripts/vitruvius/dataset_pipeline.py`
  - added additive `law_unit_count` + `contributing_law_ids` reporting
- `config/datasets/laws-core-bundle-m1.yaml`
  - added four explicit law-unit entries for:
    - `pd-1096`
    - `ra-9514`
    - `bp-344`
    - `bp-220`

## Test changes
- added `scripts/tests/test_dataset_manifest_law_units.py`
- updated `scripts/tests/test_dataset_pipeline_cli.py`

## Verification results
### Blast radius / impact check
- Intended GitNexus impact commands for:
  - `load_dataset_manifest`
  - `snapshot_metadata`
  - `dataset_build_report`
  - `provenance_for_snapshot`
  timed out locally with no result from the installed CLI.
- Fallback blast-radius evidence from direct repo reference scan:
  - `load_dataset_manifest` callers:
    - `scripts/vitruvius/graph/cli.py`
    - `scripts/vitruvius/dataset_pipeline.py`
  - `snapshot_metadata` caller:
    - `scripts/vitruvius/graph/cli.py`
  - `dataset_build_report` caller:
    - `scripts/vitruvius/graph/cli.py`
  - `provenance_for_snapshot` callers:
    - `scripts/vitruvius/query/cli.py`
    - `scripts/vitruvius/graph/cli.py`
- Result: the additive M4 runtime blast radius stayed bounded to dataset-manifest loading, dataset build reporting, dataset pipeline reporting, and textual/query provenance surfaces.

### Targeted automated verification
- `python3 -m py_compile scripts/vitruvius/graph/dataset_manifest.py scripts/vitruvius/dataset_pipeline.py scripts/tests/test_dataset_manifest_law_units.py scripts/tests/test_dataset_pipeline_cli.py`
  - PASS
- `PYTHONPATH=scripts pytest -q scripts/tests/test_dataset_manifest_law_units.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_graph_builder.py scripts/tests/test_graph_snapshot.py`
  - `39 passed in 25.31s`
- `git diff --check`
  - PASS

### Real bounded-run evidence
- Command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-dataset-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml --structured-check what_governs:concept-building-permit --structured-check what_governs:concept-certificate-of-occupancy --structured-check what_governs:concept-accessible-ramps --structured-check what_governs:concept-socialized-housing-projects`
- Result:
  - PASS
- Run ID:
  - `20260416T091402Z`
- Snapshot:
  - `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T091402Z_graph_snapshot.json`
- Build report:
  - `006_System-Manifests/runs/datasets/laws-core-bundle-m1/20260416T091402Z_build_graph_dataset_report.json`
- Pipeline report:
  - `006_System-Manifests/runs/datasets/laws-core-bundle-m1/20260416T091402Z_dataset_pipeline_run_report.json`

### Real-run truth checks
- `law_unit_count = 4`
- `contributing_law_ids = [pd-1096, ra-9514, bp-344, bp-220]`
- folder coverage remained:
  - `PD-1096 = covered`
  - `RA-9514 = covered`
  - `BP-344 = covered`
  - `BP-220 = covered`
- dataset-local snapshot / report / owl artifacts were written
- no evidence was found of any write to global graph `latest_*` artifacts

### Query provenance check
- Structured query against the real bounded snapshot now reports:
  - snapshot path
  - dataset id
  - run id
  - manifest hash
  - `contributing_law_ids`

### Architect verification
- Verdict:
  - APPROVED
- Architect-side fresh runtime check:
  - `run-dataset-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml`
  - succeeded with run id `20260416T091640Z`
- Approval scope:
  - the accepted minimal M4 slice only

## Scope and safety conclusion
M4 is now complete for the accepted minimal slice because:
1. the model/spec artifacts exist
2. the only runtime support added is the smallest additive repeatable-law-unit contract
3. current bounded pilot success remains intact
4. no generic Phase 11 widening was introduced

## Explicit non-claims
- This does **not** mean section-scoped runtime graphing is complete
- This does **not** mean merged-graph runtime orchestration is complete
- This does **not** lift the generic Phase 11 dataset-expansion gate
