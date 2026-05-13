# Explorer Source-Gap Detail Expansion Validation â€” 2026-05-13

## Scope

Added expandable detail rows to the Explorer rail Source gaps card. The details render only existing sanitized preview/proposal fields:

- workqueue ID, classification, status, final action, degree, and priority
- affected node/edge identifiers
- Resource hints with matched terms and scores
- source-link proposal metadata and rationale
- explicit pending-only/read-only reminder

No backend schema, Resource Layer, graph, or database behavior changed.

## Changed Files

- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/componentInteraction.test.tsx`

## Validation

### Focused Explorer Component Test

Command:

```bash
bun test explorer/src/components/componentInteraction.test.tsx --timeout 20000
```

Result:

```text
30 pass
0 fail
234 expect() calls
```

### Explorer Build

Command:

```bash
bun run --cwd explorer build
```

Result: passed.

Caveat: Vite still reports the existing large chunk warning.

### Whitespace Check

Command:

```bash
git diff --check
```

Result: passed.

Caveat: Git reports existing LF-to-CRLF warnings for the dirty Windows working tree.

### Code Intelligence Refresh

Command:

```bash
bash ./scripts/refresh_code_intelligence.sh
```

Result: exit code `0`.

Caveats:

- ChunkHound timed out on known large canonical/source files.
- code-review-graph reported missing `tree-sitter-yaml`.
- embedding refresh reported oversized campaign-log chunks.

### GitNexus Change Detection

Command:

```bash
cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius
```

Result: exit code `0`; full dirty-worktree risk remains `critical`.

Interpretation: scoped `BackbonePreviewPanel` impact was LOW before the edit. The critical rating is driven by the broad pre-existing uncommitted branch state.

## Safety

- No active graph mutation.
- No Resource Layer mutation.
- No pending overlay admission.
- No Neo4j/Postgres writes.
- No protected source text exposure.
- No API key or `reasoning_content` handling.
