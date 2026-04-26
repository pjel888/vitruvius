---
task: secondary-cleanup
phase: skills-agents-source-of-truth
created: 2026-04-27
author: CODEX
status: IMPLEMENTED_FOR_DUPLICATE_SKILL_DOCS
---

# Skills And Agents Source Of Truth Decision

## Decision

`/.ai/skills/` is the canonical repo-managed skill documentation surface for
current Vitruvius GitNexus/code-review skill guidance.

`/.ai/11_skills/` and `/.ai/12_agents/` are reference/adoption surfaces unless a
future cleanup packet explicitly promotes a file or pack.

## Why

- `scripts/gitnexus_analyze.sh` preserves `/.ai/skills/gitnexus/` as a
  repo-managed path.
- `.ai/skills/gitnexus/*` carries the current wrapper guidance for
  `./scripts/gitnexus_analyze.sh`.
- `.ai/11_skills/gitnexus/*` was a stale duplicate surface.
- Four compact skill docs existed in both `.ai/skills/` and `.ai/11_skills/`.
- `.ai/12_agents/` is mostly imported SlateCamp-specific reference material,
  with `.ai/12_agents/kimi-code-collaboration.md` as the only clearly
  Vitruvius-specific note in this pass.

## Implemented Cleanup

Archived duplicate `.ai/11_skills` files to:

```text
.ai/09_archive/skills/legacy-11-skills-duplicates/
```

Archived duplicate paths:

- `.ai/11_skills/gitnexus/`
- `.ai/11_skills/debug-issue.md`
- `.ai/11_skills/explore-codebase.md`
- `.ai/11_skills/refactor-safely.md`
- `.ai/11_skills/review-changes.md`

Added pointer docs:

- `.ai/11_skills/README.md`
- `.ai/12_agents/README.md`

## Explicit Non-Goals

This cleanup does not:

- move `/.ai/skills/`
- edit `scripts/gitnexus_analyze.sh`
- delete imported/reference skill packs
- rewrite imported SlateCamp agent profiles
- change runtime code or AEC-MEPFS behavior

## Remaining Optional Cleanup

A later cleanup pass may either rewrite or archive imported/reference packs in:

- `.ai/11_skills/lea-*`
- `.ai/11_skills/ph-arch-*`
- `.ai/11_skills/ui-ux-pro-max/`
- `.ai/11_skills/senior-frontend/`
- `.ai/11_skills/react-best-practices/`
- `.ai/11_skills/nextjs-best-practices/`
- `.ai/11_skills/supabase-postgres-best-practices.bak/`
- `.ai/12_agents/*.md`

That later pass should update references and preserve history rather than
deleting content.
