# NodeInspector Source-Gap Detail Validation â€” 2026-05-13

## Scope

Added proposal-level source-gap detail cards to `NodeInspector` Context tab.

Displayed fields:

- proposal title, ID, review status, target type, and suggested relationship
- source resource ID, score, target node/edge IDs, matched terms, and rationale
- pending-only/read-only reminder

## Changed Files

- `explorer/src/components/inspector/NodeInspector.tsx`
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
241 expect() calls
```

The first run found an intentionally duplicated Resource title after adding proposal cards. The test was corrected to use `getAllByText` for that repeated title.

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

Result: passed, with existing LF-to-CRLF warnings.

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

Interpretation: scoped `NodeInspector` impact was LOW before the edit. The critical rating is driven by the broad pre-existing uncommitted branch state.

## Safety

- No active graph mutation.
- No Resource Layer mutation.
- No source-link admission.
- No Neo4j/Postgres writes.
- No protected source text exposure.
- No API key or `reasoning_content` handling.
