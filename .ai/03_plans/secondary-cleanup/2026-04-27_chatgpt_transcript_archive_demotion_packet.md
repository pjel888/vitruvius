---
task: historical-transcript-demotion
phase: archive-demotion
created: 2026-04-27
author: CODEX
status: IMPLEMENTED
---

# ChatGPT Transcript Archive Demotion Packet

## Scope

Demote historical ChatGPT transcript files from the active `.ai` layer into the
archive/reference layer.

## Change

Moved transcript files from:

```text
.ai/chatGPT-Conversations/
```

to:

```text
.ai/09_archive/research/chatgpt-conversations/
```

A forwarding `README.md` remains at the original directory so older references
have a stable pointer.

## Why This Was Safe

- The transcripts are already described as historical/reference material.
- No runtime code depends on individual transcript filenames.
- No AEC-MEPFS runtime or graph behavior changes.
- No content is deleted.

## Follow-Up

The remaining secondary cleanup work is skill/agent consolidation planning.
Do not move `.ai/skills/gitnexus/` without updating `scripts/gitnexus_analyze.sh`.
