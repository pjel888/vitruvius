---
task: app-integrity-reliability
phase: 07
created: 2026-04-16
author: VALIDATOR
status: ACCEPTED
---

# Validation — App Integrity Reliability

## 1. Summary
The `main` branch is now back to a truthful, validated runtime state on this machine. The original collection blocker in `run_livewiring_bench.py` was fixed, the missing test environment assets were installed, the README command ladder was exercised, and the full Python suite passed with fresh evidence.

## 2. Code and Environment Changes

### 2.1 Code fix
- `scripts/vitruvius/bench/run_livewiring_bench.py`
  - made `psutil` optional at import time
  - added an RSS fallback based on `resource.getrusage`
  - preserved the bench summary contract exercised by `test_livewiring_bench.py`

### 2.2 Environment fixes required by the full suite
- installed `en_core_web_sm` via:

```bash
python3 -m spacy download en_core_web_sm
```

- installed `maturin` via:

```bash
python3 -m pip install maturin
```

- built and installed the CPython 3.12 Rust extension wheel via:

```bash
cd scripts/vitruvius/engine_rs/pyo3_shim
python3 -m maturin build --release -i /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12
python3 -m pip install --force-reinstall ../target/wheels/vitruvius_engine_rs-0.1.0-cp312-cp312-macosx_11_0_arm64.whl
```

### 2.3 Truthfulness updates
- `README.md`
  - switched setup examples from `pip3` to `python3 -m pip`
  - documented the spaCy-model and Rust-extension prerequisites for the exact full-suite command
  - updated stale test-count snapshots to the fresh validated result on `main`

## 3. Targeted Validation Evidence

### 3.1 Bench regression
```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_livewiring_bench.py -q
```

Result:
- `2 passed in 0.16s`

### 3.2 Previously failing environment clusters
```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_dependency_bootstrap.py::test_spacy_english_model_loadable scripts/tests/test_spacy_dep_parser.py scripts/tests/test_priming_extraction_integration.py -q
```

Result:
- `15 passed in 14.31s`

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_mahalanobis_parity.py::test_rust_mahalanobis_matches_python_on_1000_embeddings scripts/tests/test_proximity_jump_weight_parity.py::test_rust_weight_matches_python_on_10k_seeds scripts/tests/test_spatial_edge_builder_parity.py::test_rust_matches_python_on_synthetic_snapshot -q
```

Result:
- `3 passed in 0.22s`

## 4. Full-Suite Evidence
Command:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/ -v
```

Result:
- `1512 passed, 14 skipped in 47.04s`

## 5. README Command Ladder Evidence

### 5.1 CLI help / lazy imports
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py --help
PYTHONPATH=scripts python3 scripts/pipeline_cli.py promote --help
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run --help
```

Result:
- all help surfaces returned successfully
- `promote --help` confirmed the lazy-import contract on a machine without ingestion-specific bootstrap work

### 5.2 Real stage: refine
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py refine
```

Result:
- `refine (batch) complete. Processed: 6, Failed: 0`

### 5.3 Real stage: enrich concepts
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py enrich-concepts
```

Result:
- `enrich-concepts complete: total=20 enriched=0 skipped=20`
- expected skip reasons on the current corpus:
  - existing concepts already in `canonical_status=enriched`
  - the four known unresolved concepts still report `no_definition_found`

## 6. Cross-Language Validation Evidence

### 6.1 TypeScript sibling project
```bash
npm test
```

Workdir:
- `spatial-daemon/`

Result:
- `21 passed (21)`

### 6.2 Rust crates
```bash
cargo test --quiet
```

Workdirs:
- `scripts/vitruvius/engine_rs`
- `scripts/vitruvius/datalog_rs`

Result:
- `engine_rs`: `26 passed`
- `datalog_rs`: `7 passed`
- combined Rust result: `33 passed`

## 7. Residual Notes
- `pipeline_cli.py status` remains a valid command surface but rewrites `latest_status_report.*` and timestamped snapshots by design.
- `active_context.md` remains historical/branch-specific rather than a live-health baseline for `main`; the fresh validated health numbers now live in this validation artifact and the updated README snapshot.
- `omx_code_intel` / `omx_state` MCP writes intermittently returned transport-closed errors during this turn, so runtime validation relied on direct command evidence instead of those helper services.

## 8. Final Validation Judgment
Accepted.

On this machine, the operator-facing README ladder now works and yields the expected results, and the full Python suite is green with fresh evidence.
