# Ralph Context Snapshot - Canonical Operations

- Timestamp: 20260501T143709Z
- Task statement: Operationalize canonical graph stewardship after duplicate detection infrastructure: batch review, priority sorting, concrete decision packets, rollback/unmerge support, hash-chained manifests, admin gates, search ambiguity, validation/tests/docs.
- Desired outcome: scalable, auditable, reversible duplicate stewardship without broad production merges or fake decisions/resources.
- Known facts/evidence: prior loop added canonical API/UI and found 544 duplicate groups, 2 concrete groups, 0 aliases/redirects/applied decisions; graph visibility and Resource Layer tests passed; dirty worktree is broad.
- Constraints: no reckless production merge; preserve edges/resources; preserve Resource Layer and graph visibility routes; use Kimi five times; add tests and validation; dirty worktree review first.
- Unknowns/open questions: exact shape of current canonical service and UI; available auth patterns; feasibility of full destructive rollback; breadth of dirty worktree.
- Likely touchpoints: api/graph/canonicalStewardship.ts, api/index.ts, api/validateCanonicalGraphStewardship.ts, explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx, explorer/src/api/graphApi.ts, explorer/src/types/index.ts, api/resourceLayer/transactionManifest.ts, docs/.ai reports.
