---
task: aec-mepfs-backbone
phase: readiness-sel-mcp-precheck
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# SEL / MCP Precheck

## Purpose

Record tool availability and fallback evidence for the readiness packet.

This is not implementation authorization.

## Tool Availability Observed

| Tool surface | Result | Impact |
|---|---|---|
| `tool_search` for GitNexus/code-review graph | no GitNexus or code-review graph MCP tools exposed | use project-pinned GitNexus CLI parity for R4 evidence |
| `mcp__omx_code_intel__` | AST grep surface was exposed, then returned transport closed | fallback to `rg` for symbol discovery and record transport failure |
| OMX state MCP | transport closed earlier in session | use `omx state ... --json` CLI parity instead of retrying MCP blindly |
| Kimi Code CLI | available and used read-only | returned useful `ITERATE` findings |
| Codex native subagents | available and used read-only for packet review | architect returned `ITERATE` on locked-decision conflicts |
| GitNexus CLI | available through `./scripts/gitnexus_analyze.sh` and pinned `gitnexus@1.6.2-rc.10` | fresh index and impact evidence captured for R4 |

## Fallback Evidence Used

- `./scripts/gitnexus_analyze.sh`
- `npx --yes gitnexus@1.6.2-rc.10 status`
- pinned GitNexus `impact` commands with `--repo vitruvius`
- local file discovery with `rg --files`
- local symbol/string discovery with `rg`
- existing architecture and blast-radius audits
- locked taxonomy-governance decisions
- read-only Kimi and architect review passes

## Transport Failure Handling

The MCP transport-close signal was preserved as evidence rather than retried
blindly. Ralph state was written through CLI parity:

```bash
omx state write --input '{...}' --json
```

Future debugging can run the MCP server path with:

```bash
OMX_MCP_TRANSPORT_DEBUG=1 <matching-omx-mcp-command>
```

No active team runtime was detected for this readiness lane; if a future team
runtime is active, inspect it first with `omx team status <team>` before cleanup.

## Required Later Precheck

Before implementation starts:

```bash
git status --short
./scripts/gitnexus_analyze.sh
omx state read --json
npx --yes gitnexus@1.6.2-rc.10 status
```

The later execution packet must capture exact tool outputs, stale-index status,
and any fallback if graph tooling is still unavailable.

## Pass / Fail Gate

Pass:

- tool availability is recorded before implementation
- transport failures use CLI parity or file-backed state
- missing graph tools produce a written fallback plan

Fail:

- implementation proceeds while pretending fresh graph-impact evidence exists
- MCP transport failures are retried blindly without preserving state
