# Test Spec — AEC-MEPFS Backbone Readiness Closure

## Required Focused Tests
- `scripts/tests/test_kg_backbone_contracts.py`

## Required Fixtures
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_minimal.json`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`

## Required S3 Assertions
- registry locations must use allowed repository prefixes and name validator
  commands
- parity runner plan must require v1 and v2 surfaces, assertion lists, report
  path, and `blocks_runtime_without_report=true`
- rollback proof plan must block destructive operations and require backup,
  restore, smoke-query, and evidence paths
- benchmark plan must define commands, report path, repetition count,
  percentile set, and thresholds
- readiness gate scorecard must fail any runtime-required gate that is not
  closed or explicitly blocked with a blocker reason

## Verification Commands
```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
python3 -m json.tool scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json
python3 -m compileall -q scripts/vitruvius/kg/backbone_contracts.py scripts/tests/test_kg_backbone_contracts.py
git diff --check
```
