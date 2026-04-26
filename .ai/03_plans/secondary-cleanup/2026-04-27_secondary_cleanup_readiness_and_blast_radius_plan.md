---
task: secondary-cleanup
phase: readiness-and-blast-radius
created: 2026-04-27
author: CODEX
status: TRANSCRIPTS-AND-DUPLICATE-SKILLS-COMPLETE
---

# Secondary Cleanup Readiness And Blast Radius Plan

## Purpose

Plan safe cleanup for `.ai` reference material after the AEC-MEPFS shadow scope
closed, without confusing cleanup with runtime implementation.

## Scope

In scope:

- demote historical ChatGPT transcript files to archive/reference
- map skill and agent duplication before physical consolidation
- keep active roadmap, plan index, archive index, and implementation matrix true

Out of scope:

- moving `.ai/skills/gitnexus/`, because `scripts/gitnexus_analyze.sh` depends on it
- deleting imported skill/agent packs without an archive map
- changing runtime code or AEC-MEPFS behavior

## Blast Radius Audit Summary

| Surface | Current finding | Risk | Disposition |
|---|---|---:|---|
| `.ai/chatGPT-Conversations/` | Historical transcripts mixed into live `.ai` tree. | Low | First cleanup slice: move transcript content to `.ai/09_archive/research/chatgpt-conversations/` and leave forwarding pointer. |
| `.ai/skills/` | Compact current GitNexus/code-review skill docs. | High if moved | Keep canonical for now. Do not move. |
| `.ai/11_skills/` | Large imported/reference pack plus stale GitNexus duplicate docs. | Medium | Duplicate GitNexus and compact skill docs archived; remaining packs are reference/adoption candidates. |
| `.ai/12_agents/` | Imported agent profiles plus Vitruvius-specific Kimi collaboration note. | Medium | Pointer README added; remaining profiles are reference/adoption candidates. |

## References That Must Stay Truthful

- `.ai/README.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/IMPLEMENTATION_MATRIX.md`
- `.ai/archive/ARCHIVE_INDEX.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/INDEX.md`

## First Completed Slice

Transcript files are demoted to:

```text
.ai/09_archive/research/chatgpt-conversations/
```

A forwarding pointer remains at:

```text
.ai/chatGPT-Conversations/README.md
```

## Second Completed Slice

`/.ai/skills/` is the canonical current skill surface. Duplicate `.ai/11_skills` GitNexus docs and four compact duplicate docs were moved to:

```text
.ai/09_archive/skills/legacy-11-skills-duplicates/
```

Pointer docs now mark `.ai/11_skills/` and `.ai/12_agents/` as reference/adoption surfaces.

## Remaining Cleanup Plan

### S3 — Agent profile demotion

- Review `.ai/12_agents/` for SlateCamp/imported references.
- Preserve `.ai/12_agents/kimi-code-collaboration.md` as Vitruvius-specific reference unless superseded.
- Move imported profiles to archive/reference only after updating all references.

### S4 — Final cleanup verification

- Run reference scans for old paths.
- Update archive index and implementation matrix.
- Commit with validation log.

## Safety Invariants

- No runtime code changes.
- No KG rebuild, Neo4j operation, or source ingest.
- No AEC runtime authorization implied.
- No deletion of historical material; archive or forward only.
