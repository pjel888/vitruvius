<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# scripts/tests

## Purpose
Test suite for the Vitruvius pipeline and core packages. Test behavior differs materially from production code behavior.

## Key Files
| File | Description |
|------|-------------|
| `fixtures/` | Shared test fixtures and sample data |
| `test_dataset_pipeline_cli.py` | Dataset manifest and pipeline CLI tests |
| `test_graph_builder.py` | Graph construction and snapshot tests |
| `test_graph_contract.py` | Graph validation rule tests |
| `test_canonical_rules_*.py` | Canonicalization rule regression tests |

## For AI Agents

### Working In This Directory
- **Fixture ownership:** each fixture directory should have a clear owner module.
- **Determinism:** tests must produce the same result on repeated runs. Avoid unseeded randomness.
- **Feature-flag coverage:** when adding feature flags, add tests for both enabled and disabled states.
- **Regression expectations:** failing tests must be fixed or explicitly skipped with a documented reason.

### Testing Requirements
- Run targeted tests first: `python3 -m pytest scripts/tests/test_<module>.py -q`
- Run broader suite when blast radius is unclear: `python3 -m pytest scripts/tests/ -q`
- Check that fixture files are committed (they live under `scripts/tests/fixtures/`, not in gitignored output dirs).

### Common Patterns
- One test file per core module.
- Use `tmp_path` pytest fixture for temporary outputs.
- Assert on report JSON structure when testing CLI commands.
- Mock external services (Ollama, Neo4j) for unit tests.
