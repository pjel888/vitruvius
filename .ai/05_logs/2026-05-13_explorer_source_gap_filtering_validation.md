# Explorer Source-Gap Filtering Validation â€” 2026-05-13

## Scope

Added local triage filters to the Explorer AEC-MEPFS rail Source gaps browser:

- `All`
- `Nodes`
- `Relationships`

The filter is client-side and read-only. It does not mutate Resource Layer files, active graph files, pending overlay artifacts, Neo4j, or Postgres.

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
227 expect() calls
```

Note: the first run exposed an ambiguous Testing Library query because the text `Nodes` appeared both as a summary label and a filter button. The test was corrected to target `getByRole("button", { name: "Nodes" })` and `getByRole("button", { name: "Relationships" })`, matching the intended accessible controls.

### Explorer Build

Command:

```bash
bun run --cwd explorer build
```

Result: passed.

Caveat: Vite still reports the existing large chunk warning for the built Explorer bundle. That warning predates this filter slice and is not a functional failure.

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

Result: completed with exit code `0`.

Caveats recorded from the refresh:

- ChunkHound timed out on several large canonical/source files.
- code-review-graph reported missing `tree-sitter-yaml`.
- OpenAI embedding refresh logged expected failures for oversized campaign logs.

These are existing tooling/data-size caveats and did not block the scoped Explorer validation.

### GitNexus Change Detection

Command:

```bash
cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius
```

Result: exit code `0`; risk level `critical` for the full dirty worktree.

Interpretation: the critical rating is driven by the broad uncommitted repository state that includes earlier API, relationship-improvement, overlay, documentation, and generated campaign artifacts. The filtering slice itself is confined to the Explorer rail component and its interaction test.

## Safety

- No active graph mutation.
- No Resource Layer mutation.
- No pending overlay admission.
- No Neo4j/Postgres writes.
- No protected source text exposure.
- No API key or `reasoning_content` handling added.
