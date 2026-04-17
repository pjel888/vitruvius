# 2026-04-17 Validation — Tranche-5 richness

## Scope
Remove tranche-5 shallow-representation findings while keeping the tranche bounded to `PD-856`, `RA-7160`, and `RA-9257`.

## Admitted concepts
### PD-856
- `concept-floor-area`
- `concept-food-establishment`
- `concept-local-health-authority`

### RA-7160
- `concept-local-autonomy`
- `concept-prior-consultations`
- `concept-comprehensive-land-use-plan`

### RA-9257 / RA-9275
- `concept-water-quality-management-area`
- `concept-wastewater-charge-system`
- `concept-discharge-permit`

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-5.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-5.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 7`
  - `shallow_representation_count = 0`
  - graph snapshot: `13 nodes / 24 edges`

## Outcome
Tranche-5 is no longer concept-shallow and the RA-9257 folder/file naming mismatch remains handled truthfully through canonicalization to the Philippine Clean Water Act of 2004.
