# NodeInspector Source-Gap Overview Callout Validation â€” 2026-05-13

## Scope

Added an Overview tab callout when a selected node has source-gap workqueue items. The callout switches the local inspector tab to Context for review.

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
243 expect() calls
```

One intermediate assertion used plural wording against a one-item fixture and was corrected to match singular/plural text safely.

### Explorer Build

Command:

```bash
bun run --cwd explorer build
```

Result: passed.

Caveat: existing Vite large chunk warning remains.

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

## Safety

- No active graph mutation.
- No Resource Layer mutation.
- No source-link admission.
- No Neo4j/Postgres writes.
- No protected source text exposure.
