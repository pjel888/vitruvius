# KG Explorer Inspector UX Validation — 2026-04-24

## Scope
Validated the API/UI-first implementation for KG Explorer inspector reliability and long-rule display-label UX.

## Implemented Outcomes
- Node selection from graph-style state changes no longer gets cleared merely because the URL did not already contain `?node=`.
- Inspector node detail lazy-load no longer refuses valid selected nodes solely because they are absent from the current visible node array.
- API normalization now emits `displayLabel` while preserving canonical `id` and full canonical `label`.
- `/node/:id` detail query includes taxonomy relationship families and uses correct incoming relationship direction.
- Node and evidence normalization unwrap nested Neo4j node-like `{ properties }` values from collected relationship/evidence arrays.
- Explorer graph/search/rail/inspector surfaces render `displayLabel ?? label` for compact UX while keeping canonical labels and IDs available in inspector details.
- Node inspector now defaults to Overview and provides Relationships, Sources, and Metadata tabs with explicit empty states.

## Automated Validation

### API
Command:

```bash
bun test
```

Directory: `api/`

Result: **11 pass, 0 fail**

### Explorer Tests
Command:

```bash
bun test
```

Directory: `explorer/`

Result: **24 pass, 0 fail**

### Explorer Build
Command:

```bash
bun run build
```

Directory: `explorer/`

Result: **pass**

Note: Vite reported the existing `vis-network` chunk-size warning after successful build.

## Review Evidence
- Initial post-implementation review found one Critical issue and three Important issues.
- Fixed nested Neo4j relationship-node normalization, presentation-only search-state handling, API normalization test coverage, and inspector tab content coverage.
- Follow-up review found one remaining Important evidence-span normalization issue.
- Fixed nested Neo4j evidence-span normalization and added test coverage.
- Final reviewer result: **No remaining Critical or Important issues found.**

## Caveats
- LSP diagnostics could not run because `typescript-language-server` is not installed in this environment.
- Manual Playwright/browser QA was not run in this pass; automated React/API/build validation and code-reviewer verification passed.
- The repository already contains many unrelated untracked canonical source/relationship artifacts; these were not touched by this implementation.
