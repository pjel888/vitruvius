# 2026-04-17 Validation — PD-1067 water-governance concept-fit

## Scope
Admit the smallest tranche-3 concept-fit slice needed to remove PD-1067's shallow-representation finding.

## Admitted concepts
- `concept-water-permit`
- `concept-water-right`
- `concept-groundwater-drilling`

## Admitted dataset-scoped relationships
- `law-water-code-of-the-philippines governs concept-water-permit`
- `law-water-code-of-the-philippines governs concept-water-right`
- `law-water-code-of-the-philippines governs concept-groundwater-drilling`
- `irr-amended-implementing-rules-and-regulations-of-the-water-code-of-the-philippines governs concept-water-permit`
- `irr-amended-implementing-rules-and-regulations-of-the-water-code-of-the-philippines governs concept-groundwater-drilling`

## Fresh verification
- `python3 -m py_compile scripts/tests/test_canonical_rules_additional_laws.py`
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **13 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-3.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-3.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 11 edges`

## Outcome
The tranche-3 graph is no longer blocked by the PD-1067 richness floor. The tranche remains bounded and still keeps explicit raw-alias visibility for the excluded legacy IRR variant.
