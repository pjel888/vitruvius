# AEC-MEPFS Four Gated Lanes Context Snapshot

- Created: 20260427T114016Z
- Mode: Ralph + Ultrawork + app-safe native subagents (tmux team runtime unavailable in direct CLI session)
- Repo: /Users/philiplewis/vitruvius
- Branch baseline: main at 64d341cf before reopened work

## Task statement
Project owner reopened AEC-MEPFS for four intentionally gated lanes: Neo4j isolated rehearsal/live-promotion preparation, protected source admission, Explorer default adoption, and runtime threshold adoption.

## Desired outcome
Complete every repo-actionable prerequisite, packet, test, evidence artifact, Kimi review, commit, and push for the four lanes while preserving the prior closure packet as the safety baseline.

## Known facts / evidence
- Previous safe autonomous scope was closed through final closure docs and commit 64d341cf.
- Latest evidence anchor in prior closure docs: commit 8b05e559, run 20260427T044757Z.
- Guarded resolver remains default-off behind VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME.
- Existing closure explicitly blocked broad/global LIVE_RUNTIME_AUTHORIZED, Neo4j/KG mutation, protected ingest, Explorer default adoption, default-on flags, and runtime threshold pass/fail claims.
- Current project-owner directive supersedes closure-only stopping for these four lanes only.

## Constraints
- Do not use Gemini; do not search for Gemini.
- Use Kimi/Moonshot advisory review where available; unavailable Kimi is not blocking.
- Use gpt-5.3-codex-spark for bounded coding tasks where available, verified by tests; unavailable Spark is not blocking.
- Do not print secrets, API keys, tokens, or environment values.
- Do not perform broad/global live authorization, destructive production Neo4j reset, production primary graph replacement, protected payload exposure, or runtime threshold claims from shadow-only evidence.
- Use Windows-safe filenames for generated docs/artifacts.

## Unknowns / open questions
- Whether valid repo records exist for protected-source ingestion authority.
- Whether an isolated Neo4j sandbox/rehearsal can run safely in the local environment without touching primary/live namespaces.
- Whether current guarded runtime path plus benchmark harness is sufficient for threshold pass/fail adoption, or only schema/harness evidence can be completed.
- Whether Explorer default adoption criteria are already satisfied or require staged/default-off selector-only work first.

## Likely codebase touchpoints
- .ai/03_plans/AEC-MEPFS-Backbone/
- .ai/05_logs/
- 006_System-Manifests/aec-mepfs-backbone/
- api/index.ts, api/v2Resolver.test.ts, api/aecResolverRuntimeBenchmark.ts
- explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx and Explorer graph state/perspective tests
- scripts/vitruvius/kg/backbone_* and related tests under scripts/tests/
- source-rights/currentness/steward docs under .ai/03_plans/AEC-MEPFS-Backbone/
- Neo4j client/loader/preflight helpers under scripts/vitruvius/kg/
