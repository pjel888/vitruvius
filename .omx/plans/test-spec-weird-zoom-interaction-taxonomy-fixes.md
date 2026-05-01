# Test spec - Weird zoom interaction taxonomy fixes

## Unit and integration coverage
- `explorer/src/components/componentInteraction.test.tsx`
  - scene store preserves selected node when entering pan and returning to select.
  - NodeInspector renders clickable taxonomy breadcrumbs and dispatches selected node changes.
- `explorer/src/components/graph/VisNetworkHost.test.ts`
  - layout spread scaling supports both expansion and contraction.
- API tests under `api/`
  - AEC-MEPFS expand route/helper returns descendant child nodes beyond first hop for child-subtree expansion.
- Python enrichment tests under `scripts/tests/`
  - metadata-only organization relationships are present and idempotent.

## Verification commands
- `cd explorer && bun test src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts`
- `cd explorer && bun run build`
- `bun test api/v2Backbone.test.ts api/v2Resolver.test.ts` or available API test command.
- `python -m pytest scripts/tests/test_kg_architecture_interconnectivity_enrichment.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py`

## Regression focus
- Selection, pan/select, context menu, filters, and inspector behavior.
- AEC-MEPFS file-backed graph routes only.
- Rights-safe metadata-only enrichment boundaries.
