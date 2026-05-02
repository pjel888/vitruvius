# P0 Stewardship Admission Loop Validation Log

Date: 2026-05-02

## Commands run

- `bun test api/canonicalGraphStewardship.test.ts` — 22 pass, 0 fail.
- `cd api && bun test` — 156 pass, 0 fail.
- `cd explorer && bun test` — 111 pass, 0 fail.
- `cd explorer && bun run build` — pass; Vite chunk-size warning only.
- `bun run api/validateGraphRelationships.ts` — ok true, 0 issues.
- `bun run api/validateResourceLayer.ts` — ok true, blockers [], expected standards-context warnings 2.
- `bun run api/validateCanonicalGraphStewardship.ts` — ok true, duplicate groups 544, unresolved 544, P0 unresolved 2, approvals 0, admitted relationships 0, P1 decision packets 20.
- `bash ./scripts/refresh_code_intelligence.sh` — completed; code-review-graph YAML parser warnings and `_Task.elapsed` embedding warning recorded.
- `cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` — completed with critical risk because the worktree is broadly dirty from pre-existing/prior-loop changes.
- `chunkhound search --regex --page-size 20 --path-filter "api/" "CROSS_DOMAIN_ALIGNMENT|CanonicalApproval|admitted-relationships" .` — completed, confirming canonical admission symbols are indexed.

## Regression status

- Sendai Mediatheque/Toyo Ito regression remains covered by API tests and graph relationship validation.
- Resource Layer validation remains passing.
- Canonical validation remains passing.
- No production P0 edge/resource mutation occurred.
