# Test Spec — KG Semantic Connectedness Overlays

## Static/schema validation
- Compile any new/modified Python enrichment script.
- Validate admitted backbone fixture via `validate_backbone_contract_file`.
- Validate modified JSON with `python3 -m json.tool`.

## Unit/regression tests
- Add focused tests for overlay enrichment idempotency, relationship predicate counts, category counts, source-rights metadata-only rows, and sample semantic relationships.
- Update backbone contract expected counts and API expectations.
- Run targeted taxonomy, overlay, broad taxonomy, backbone contract, and shadow staging tests.

## Generated artifacts
- Run overlay enrichment report generation.
- Regenerate shadow staging and consumer report for a new run.
- Verify counts and read-only/no-ingest boundaries.

## API verification
- Run `(cd api && bun test v2Backbone.test.ts)` after artifact/count updates.

## Safety checks
- `git diff --check`.
- Safety grep for live mutation, production promotion, protected ingest authorization, destructive graph operations, reload/reset, and active Codex Spark enrichment routing.
- GitNexus status if available.
- Kimi final read-only review.
