# 2026-04-17 Laws Pilot Operator Experience Validation

## Scope
Follow-on hardening for the accepted bounded four-law pilot lane only:
- `PD-1096`
- `RA-9514`
- `BP-344`
- `BP-220`

This validation covers:
1. single-command bounded pilot execution
2. self-contained browser HTML output
3. repo-root operator helper
4. progress-oriented CLI experience

It does **not** open generic Phase 11 expansion.

## Implemented Operator Surfaces

### 1. Single-command bounded pilot CLI
- `python3 scripts/pipeline_cli.py run-laws-pilot --skip-export-owl --open-browser`
- delegates to the bounded `run-dataset-source-to-graph` lane using:
  - `config/datasets/laws-core-bundle-m1.yaml`

### 2. Repo-root helper
- `./run-laws-pilot --skip-export-owl --open-browser`
- helper is a thin wrapper over `pipeline_cli.py run-laws-pilot`

### 3. Self-contained HTML visualization
- the generated graph HTML now bundles Cytoscape directly
- the embedded snapshot/elements payloads are parseable JSON
- opening the file directly from disk no longer depends on relative JS asset resolution

### 4. Progress output
- bounded pilot runs now emit phase/progress lines during execution
- progress lines go to terminal-oriented progress output while the final JSON summary remains available
- forced progress is supported with:
  - `VITRUVIUS_CLI_PROGRESS=1 ./run-laws-pilot --dry-run`

## Verification Evidence

### Tests
Command:

```bash
python3 -m pytest \
  scripts/tests/test_dataset_pipeline_cli.py \
  scripts/tests/test_graph_visualize_cli.py \
  scripts/tests/test_dataset_source_to_graph_pipeline.py \
  scripts/tests/test_canonicalize_body.py \
  scripts/tests/test_canonicalize_integration.py \
  scripts/tests/test_query_formatter.py -q
```

Result:
- **57 passed**

### Syntax / import checks
Command:

```bash
python3 -m py_compile \
  scripts/pipeline_cli.py \
  scripts/vitruvius/cli_experience.py \
  scripts/vitruvius/dataset_pipeline.py \
  scripts/vitruvius/graph/visualize.py \
  scripts/vitruvius/canonicalize.py
```

Result:
- **PASS**

### Repo-root helper verification
Commands:

```bash
./run-laws-pilot --dry-run
VITRUVIUS_CLI_PROGRESS=1 ./run-laws-pilot --dry-run
```

Results:
- both commands pass
- progress lines render in the terminal during dry-run verification

### Single-command browser artifact verification
Command:

```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-pilot --skip-export-owl --visualize
```

Verified output fields:
- `visualization_html_path` returned in the same JSON summary
- latest verified snapshot path:
  - `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T193115Z_graph_snapshot.json`
- latest verified HTML path:
  - `004_Derived-Content-Layer/graph-visualizations/laws-core-bundle-m1/20260416T193115Z_graph_snapshot.html`

HTML validation checks:
- bundled Cytoscape marker present
- embedded `snapshot-data` JSON parseable
- embedded `elements-data` JSON parseable
- node count = **26**
- edge count = **94**

## Truthful Current State
- the bounded pilot now has a supported single-command operator flow
- the browser HTML no longer renders as an empty layout due to escaped JSON payloads
- the helper and CLI shortcut remain bounded to the accepted 4-law pilot manifest
- generic Phase 11 expansion remains gated

## Residual Caveats
- repeated verification runs produced many dataset-local run artifacts and visualization files
- those artifacts are evidence of successful runs, but they also create worktree noise if left unmanaged
- the bounded lane remains correct for the accepted pilot, but it is still not the same thing as generic all-laws or all-corpora expansion
