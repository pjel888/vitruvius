# 2026-04-17 Laws Tranche Expansion Implementation Validation

## Scope
Implementation follow-on after tranche-expansion planning.

This slice adds:
1. a concrete tranche manifest
2. a tranche dry-run command
3. automated structure-vs-concept guardrails to catch BP220-style shallowness

## Implemented
- `config/datasets/laws-tranche-1.yaml`
  - first tranche manifest
  - current tranche target folders:
    - `PD-957`
    - `PD-1216`
    - `PD-1185`
- `scripts/vitruvius/laws_readiness.py`
  - tranche manifest loader
  - `run_laws_tranche_dry_run(...)`
  - per-law `structural_header_count`
  - automated `structure_guardrails`
- `scripts/pipeline_cli.py`
  - `run-laws-tranche-dry-run` wired to readiness path
- `scripts/tests/test_dataset_pipeline_cli.py`
  - tranche dry-run coverage
  - structure guardrail coverage
- `README.md`
  - tranche dry-run operator guidance

## Fresh verification evidence

### Tests
```bash
python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q
```
Result:
- **10 passed**

### Syntax
```bash
python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/laws_readiness.py scripts/vitruvius/cli_experience.py
```
Result:
- **PASS**

### Real tranche dry-run
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run \
  --tranche-manifest config/datasets/laws-tranche-1.yaml \
  --review-preset m2-8gb-safe
```
Result summary:
- `action = run-laws-tranche-dry-run`
- `phase_11_gate = gated`
- `tranche_id = laws-tranche-1`
- `candidate_law_folder_count = 3`
- `candidate_law_folders = [PD-957, PD-1216, PD-1185]`
- `pilot_covered_law_count = 0`
- `inventory_only_law_count = 3`
- `missing_raw_source_count = 0`
- report written under:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/.../laws_tranche_dry_run_report.json`

### Real all-laws dry-run with structure guardrails
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe
```
Result summary:
- `structure_guardrail_law_folders = [BP-220, BP-344, RA-9514]`

This is the intended safeguard:
- laws with rich section structure but weak concept/relationship admission are now surfaced automatically in readiness reporting

## Conclusion
The next safe execution path is now stronger than before:
- tranche-1 can be assessed explicitly
- broad all-laws readiness can automatically flag BP220-style structure-vs-concept shallowness
- generic all-laws execute remains gated
