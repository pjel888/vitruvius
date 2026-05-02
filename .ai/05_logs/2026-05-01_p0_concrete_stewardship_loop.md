# P0 Concrete Stewardship Loop Validation Log

Date: 2026-05-01

## Commands run

- `bun test` in `api` - passed, 152 tests.
- `bun test` in `explorer` - passed, 111 tests.
- `bun run build` in `explorer` - passed, chunk-size warning only.
- `bun run api/validateGraphRelationships.ts` - passed.
- `bun run api/validateResourceLayer.ts` - passed with existing standards-context warnings.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed.

## Regression status

- Graph relationship visibility: preserved.
- Sendai Mediatheque / Toyo Ito regression: covered by API tests and graph validation remained clean.
- Resource Layer routes and review UI: preserved; validation blockers empty.
- Canonical review UI: remediation and status surfaces render in tests.
- General Explorer search: fixed after canonical proposed decisions initially reranked unrelated search; regression test now passes.

## Current metrics

- Duplicate groups: 544.
- Unresolved groups: 544.
- P0 unresolved groups: 2.
- Stewardship decisions: 2 proposed-only.
- Applied decisions: 0.
- Aliases: 0.
- Redirects: 0.
- Tombstones: 0.
- Graph stewardship edge proposals: 3.
- Transaction manifests: 3.
- Validation blockers: 0.

## Post-implementation code-intelligence checks

- Code intelligence refresh completed with known YAML parser and embedding-service warnings.
- GitNexus detect-changes still reports critical broad dirty-worktree risk across previous-loop/unrelated changes.
- ChunkHound targeted regex search succeeded after setting UTF-8 output environment variables.
