---
task: skills-agents-source-of-truth-cleanup
phase: validation
created: 2026-04-27
author: CODEX
status: PASS
---

# Skills And Agents Source Of Truth Validation

## Scope

Completed the second secondary-cleanup slice by selecting `.ai/skills/` as the
canonical repo-managed skill documentation surface, archiving stale duplicate
`.ai/11_skills` GitNexus and compact skill docs, and marking `.ai/11_skills/`
and `.ai/12_agents/` as reference/adoption surfaces.

No runtime code, API route, Explorer behavior, KG artifact, source ingest,
Neo4j operation, feature flag, or benchmark threshold changed.

## Files Changed

- `.ai/03_plans/secondary-cleanup/2026-04-27_skills_agents_source_of_truth_decision.md`
- `.ai/03_plans/secondary-cleanup/2026-04-27_secondary_cleanup_readiness_and_blast_radius_plan.md`
- `.ai/11_skills/README.md`
- `.ai/12_agents/README.md`
- `.ai/09_archive/skills/legacy-11-skills-duplicates/`
- `.ai/ACTIVE_WORK.md`
- `.ai/IMPLEMENTATION_MATRIX.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/INDEX.md`
- `.ai/archive/ARCHIVE_INDEX.md`
- `.ai/09_archive/README.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`

## Verification Commands

```bash
git status --short --branch
rg -n "\.ai/11_skills/gitnexus|11_skills/gitnexus|\.ai/skills/gitnexus|skills/gitnexus|\.ai/11_skills|\.ai/skills|\.ai/12_agents" .ai scripts AGENTS.md README.md
find .ai/skills -maxdepth 3 -type f | sort
find .ai/09_archive/skills/legacy-11-skills-duplicates -maxdepth 3 -type f | sort
git diff --check
npx --yes gitnexus@1.6.2-rc.10 status
```

## Verification Results

- GitNexus status before the slice was up to date at `3be52db`.
- `scripts/gitnexus_analyze.sh` is the only code path depending on
  `.ai/skills/gitnexus/`, so that canonical path was preserved.
- No live references required `.ai/11_skills/gitnexus/` to remain in place.
- The duplicate archive contains the six stale GitNexus skill files plus four
  compact duplicate skill docs.
- `.ai/11_skills/README.md` and `.ai/12_agents/README.md` now mark both
  directories as reference/adoption surfaces.


## Advisory Reviews

- Kimi 2.6 / `kimi-code/kimi-for-coding`: PASS, no actionable issues. It confirmed stale `.ai/11_skills` references are descriptive only, `.ai/skills/gitnexus/` remains preserved for `scripts/gitnexus_analyze.sh`, no unsafe runtime authorization was introduced, and the duplicate archive contains the claimed 10 files. Non-blocking note: `.claude/skills/gitnexus/` remains a separate physical copy and may be reviewed in a future cleanup pass.
- Gemini CLI: attempted, but unavailable due account/service-disabled authentication failure. No Gemini advice was used.
- Codex verifier subagent: PASS. It confirmed changed files are `.ai` docs/archive only, the stale `.ai/11_skills/gitnexus` tree is absent from the active location, pointer READMEs are adequate, and no runtime/API/Explorer/Neo4j/KG rebuild/protected-ingest/feature-flag/default-graph behavior changed.

## Safety Invariants

- no Neo4j writes or queries introduced
- no KG rebuild/reset/load introduced
- no protected content ingest introduced
- no feature flag cutover or default-on behavior introduced
- no `/v2/resolve*` mounting introduced
- no Explorer default graph adoption introduced
- no runtime benchmark threshold evaluation or claim introduced
- no historical material deleted; duplicates are archived

## Residual Risks

Imported/reference packs remain in `.ai/11_skills/` and `.ai/12_agents/` for a
future optional adoption/archive pass. That future pass should not move
`.ai/skills/gitnexus/` unless `scripts/gitnexus_analyze.sh` is updated first.
