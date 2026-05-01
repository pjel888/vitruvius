# Tracked OMX handoff subset

This repository intentionally tracks only the durable, small OMX artifacts that help a codebase AI continue work after a machine move:

- `wiki/` — compact OMX wiki/session notes.
- `plans/` — workflow PRDs and test specs.
- `context/` — context snapshots and handoff summaries.
- `artifacts/` — small review/advisory artifacts.
- `notepad.md` — concise working memory.
- `project-memory.json` — durable directives and cross-session notes.

Volatile runtime data remains ignored and should stay local:

- `logs/`
- `state/`
- `team/`
- `reports/`
- runtime metrics, hud, setup, tmux-hook, PID, and socket files.

Do not commit full `.omx` runtime logs or session state; they are large, machine-specific, and may contain noisy transcripts or local paths.
