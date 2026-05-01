# Test Spec: AEC-MEPFS Shadow Completion Loop

## Slice Under Test

Parity runner hardening for shadow-only AEC-MEPFS Backbone graph/preview
evidence.

## Required Checks

1. Contract and parity runner tests:
   `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py`

2. Shadow graph/report tests:
   `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`

3. API affected tests:
   `cd api && bun test v2Backbone.test.ts perspectiveContracts.test.ts`

4. Explorer affected tests:
   `cd explorer && bun test src/utils/labels.test.ts src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts src/app.searchInspector.integration.test.tsx`

5. Full parity report generation:
   `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id RUN_ID`

6. Broader affected suites when the diff touches API/Explorer behavior:
   - `cd api && bun test`
   - `cd explorer && bun test`
   - `cd explorer && bun run lint`
   - `cd explorer && bun run build`

## Safety Invariants To Assert In Evidence

- No Neo4j writes.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- Preview/read-only/shadow-only behavior remains opt-in.
- Generated artifacts are file-backed and auditable.
- API/consumer parity is explicitly tested.
- Runtime promotion remains blocked.
