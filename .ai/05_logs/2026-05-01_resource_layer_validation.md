# Resource Layer Validation Log

Date: 2026-05-01

## Commands
- `bun run api/validateResourceLayer.ts`
- `bun run api/indexLocalResources.ts --dir=.ai/13_research/vitruvius_resource_layer_markdown_pack --maxFiles=50`
- `bun test` in `api/`
- `bun test` in `explorer/`
- `bun run build` in `explorer/`

## Results
- Resource validation: ok; 7 resources, 9 node-resource links, 25 source families, 15 checks, 4 candidates, 0 duplicate groups, 0 broken link checks.
- Validation warnings: ASCE 7 landing page and ACI 318 portal are standards without edition/version context. These records are not accepted primary references.
- Local corpus indexing: 25 real local markdown files indexed, 0 errors.
- API tests: 123 pass, 0 fail.
- Explorer tests: 102 pass, 0 fail.
- Explorer build: pass with existing chunk-size warning.

## Notes
Candidate, needs_review, and rejected links are hidden from the sidebar by default. The API can expose them with `includeCandidates=true` for review workflows.
