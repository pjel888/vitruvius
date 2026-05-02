# Resource Layer Standards Context Cleanup Context

## Task Statement
Implement a guarded Resource Layer standards-context workflow for ASCE 7 and ACI 318 missing edition/version/scope context without inventing values or auto-promoting resources.

## Desired Outcome
Missing standard/code context is visible, reviewable, diff-previewed, validated, transaction-manifested, and editable later by a real reviewer through /dev/resource-review while current ASCE 7 and ACI 318 warnings remain truthful until context is supplied.

## Known Facts/Evidence
- Current HEAD is adff4790 and origin/main matches.
- Current Resource Layer validation passes with 7 resources, 9 nodeResourceLinks, and 2 standards_missing_context warnings.
- Warnings are ASCE 7 and ACI 318 missing edition/version context.
- Existing Resource Layer review routes include queue/candidates/local-files/standards/report and link/candidate/local-file decisions.
- Existing Resource Layer transaction manifest helper is available in api/resourceLayer/transactionManifest.ts.
- Worktree has unrelated dirty AEC relationship-improvement files and an untracked semantic overlay; these must not be overwritten or staged for this Resource Layer task.

## Constraints
- No fake editions, versions, jurisdictions, source metadata, verification, resources, or approvals.
- No auto-promotion of ASCE 7 or ACI 318.
- Preserve Resource Layer routes, graph relationship visibility, canonical stewardship behavior, and mutation gates.
- Any Resource Layer context mutation must be admin/dev gated, reviewed, logged, and transaction-manifested.
- Keep P0 Concrete/Reinforced Concrete proposed/unresolved unless real approval exists.

## Unknowns / Open Questions
- Exact minimal schema fields should fit current Resource/NodeResourceLink conventions.
- Whether to store context primarily on Resource, NodeResourceLink, or both must be verified from current data shape.
- Need avoid false blockers for existing needs_review standards while blocking unsafe accepted/promoted states.

## Likely Codebase Touchpoints
- api/resourceLayer/types.ts
- api/resourceLayer/validation.ts
- api/resourceLayer/reviewWorkflow.ts
- api/resourceLayer/registry.ts
- api/resourceLayer/transactionManifest.ts
- api/index.ts
- api/validateResourceLayer.ts
- api/resourceLayer.test.ts
- explorer/src/types/index.ts
- explorer/src/api/graphApi.ts
- explorer/src/components/resource-review/ResourceReviewAdmin.tsx
- explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx
- docs/knowledge-graph/resource-layer.md
- .ai/13_research/resource_layer_standards_context_cleanup_report.md
