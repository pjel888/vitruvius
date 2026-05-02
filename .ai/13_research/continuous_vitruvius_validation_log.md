# Continuous Vitruvius Validation Log

Last updated: 2026-05-02T09:31:05+0800

## Commands run this iteration

| Command | Result |
| --- | --- |
| `bash ./scripts/refresh_code_intelligence.sh` | Completed with caveats: code-review-graph YAML parser warnings for missing `tree-sitter-yaml`; ChunkHound processed files but emitted embedding/provider errors while returning exit code 0. |
| `cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` | Completed; reported critical risk across 34 files / 223 symbols / 28 affected processes from the broad dirty worktree. This remains a change-scope blocker, not a reason to treat production mutation as safe. |
| `bun test api/canonicalGraphStewardship.test.ts` | Passed: 22 tests. |
| `cd api; bun test` | Passed: 156 tests. |
| `cd explorer; bun test src/components/canonical-review/CanonicalReviewAdmin.test.tsx src/api/graphApi.test.ts` | Passed: 9 tests. |
| `cd explorer; bun test` | Passed: 111 tests. |
| `cd explorer; bun run build` | Passed with Vite chunk-size warning. |
| `bun run api/validateGraphRelationships.ts` | Passed: 10,018 nodes, 13,670 edges, issueCount 0. |
| `bun run api/validateResourceLayer.ts` | Passed: resources 7, nodeResourceLinks 9, blockers/errors 0, known context warnings. |
| `bun run api/validateCanonicalGraphStewardship.ts` | Passed: duplicateGroups 544, unresolved 544, P0 2, P1 66, P1 packets 20, missing/stale/tampered source snapshots 0. |

## Validation interpretation

The current implementation is safe to checkpoint as a non-destructive canonical stewardship hardening step. It does not resolve P0 Concrete/Reinforced Concrete, does not create steward approvals, and does not mutate production graph edges/resources.
