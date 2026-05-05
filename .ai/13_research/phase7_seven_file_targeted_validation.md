# Phase 7 Seven-File Targeted Validation

**Date:** 2026-05-06
**Scope:** Commands relevant to the seven needs-review files.

## Focused Commands

| Command | Result |
|---|---|
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_canonicalize_body.py` | PASS, 34 passed |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_pipeline_force_path.py` | PASS, 16 passed |
| `.venv\Scripts\python.exe scripts\pipeline_cli.py --help` | PASS |
| `.venv\Scripts\python.exe scripts\pipeline_cli.py run-kg-pipeline --help` | PASS |
| `git diff --check -- <seven files>` | PASS, no whitespace errors |

## Optional Broader Selector

Command:

```powershell
.venv\Scripts\python.exe -m pytest scripts/tests --ignore=scripts/tests/test_livewiring_bench.py --ignore=scripts/tests/test_wiring_bench.py -k "canonicalize or pipeline_cli or slug or neo4j or kg_pipeline"
```

Result:

- 208 passed
- 19 failed
- 18 skipped
- 2,417 deselected

Failure characterization:

- The selected failures are Windows path-separator expectations in tests outside the authorized seven-file disposition set, mainly `scripts/tests/test_dataset_pipeline_cli.py` and `scripts/tests/test_kg_backbone_neo4j_rehearsal.py`.
- The same selector without the two ignored bench tests fails collection on Windows because `test_livewiring_bench.py` and `test_wiring_bench.py` import the POSIX-only `resource` module.
- These broader selector failures are documented as environment/pre-existing suite issues and were not repaired because the task permits edits only in the seven needs-review files and scoped `.ai` reports.

## Baseline Full Validation Already Run In This Task

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS |
| `cd api && bun test` | PASS, 398 pass |
| `cd explorer && bun test` | PASS, 118 pass |
| `cd explorer && bun run build` | PASS |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS, 118 passed |

## Mutation Check

- No production Resource Layer registries are dirty.
- No graph-canonical registries are dirty.
- No external metadata candidates, Resources, or nodeResourceLinks were created.
- No graph/canonical mutation or edge admission was performed.
- No external verification was performed.
