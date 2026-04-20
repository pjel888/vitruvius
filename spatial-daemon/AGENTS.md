<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# spatial-daemon

## Purpose
TypeScript spatial-compute daemon. Owns the strongest TypeScript ↔ Python contract in the repo. Communicates by file contract, not by live service coupling.

## Key Files
| File | Description |
|------|-------------|
| `src/aabb.ts` | Axis-aligned bounding box utilities |
| `src/gjk.ts` | GJK collision detection |
| `src/contract_writer.ts` | Integrity-footer and file-contract generation |
| `src/cli.ts` | CLI entrypoint |
| `src/types.ts` | Shared TypeScript types |

## For AI Agents

### Working In This Directory
- **Integrity-footer parity is critical.** The TypeScript contract_writer must remain in sync with Python-side contract readers.
- **File-contract discipline is easy to break casually.** Any change to output file format must be reflected in both TypeScript and Python consumers.
- **No live service coupling.** spatial-daemon communicates via files, not sockets or HTTP.
- TypeScript is isolated to this directory and the `explorer/` frontend.

### Testing Requirements
- Run TypeScript tests: `npm test` or equivalent from package.json.
- Verify contract output files parse correctly from Python after any change.

### Common Patterns
- One file per spatial primitive.
- Contract outputs go to predictable paths consumed by Python pipeline stages.
- Keep TypeScript deps minimal; no unnecessary frameworks.
