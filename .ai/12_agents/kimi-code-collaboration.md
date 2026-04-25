---
name: kimi-code-collaboration
description: Guidance for using Kimi Code CLI as a bounded auxiliary agent in Vitruvius.
created: 2026-04-25
status: ACTIVE
---

# Kimi Code Collaboration

Kimi Code CLI may be used as an auxiliary agent for Vitruvius when an
independent pass improves quality, speed, or confidence.

## Role

Kimi is not the primary orchestrator. Codex remains responsible for scope,
state, governance, integration, validation, and final reporting.

Use Kimi as:

- a read-only critic for architecture and plan packets
- a second-opinion reviewer for taxonomy, KG relationship quality, and naming
- a bounded reviewer for cleanup/refactor blast radius
- a test-strategy reviewer for high-risk or broad changes
- a narrow implementation helper only when write ownership is explicit

## Invocation

Preferred read-only pattern:

```bash
kimi --work-dir /Users/philiplewis/vitruvius --plan -p "Read AGENTS.md and the relevant files. Do not edit files. Return findings with file evidence only."
```

Before using Kimi for edits:

- record the intended file scope
- check `git status --short`
- make the prompt state that no other agent-owned files may be changed
- verify the diff after Kimi returns

## Guardrails

- Kimi findings are not accepted as truth until checked against local files,
  tests, or official sources where relevant.
- Kimi must not bypass the Standard Execution Loop, roadmap gates, feature-flag
  gates, or source-truth governance.
- Avoid `kimi --print` and `kimi --quiet` for mutable repo work because print
  mode implicitly enables yolo.
- Do not use Kimi for trivial tasks where the review overhead does not pay for
  itself.
- Do not run concurrent Codex and Kimi edits against the same files.
