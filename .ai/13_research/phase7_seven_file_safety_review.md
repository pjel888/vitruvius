# Phase 7 Seven-File Safety Review

**Date:** 2026-05-06
**Reviewer:** Codex local safety review before delegated external AI review.

## A. `README.md`

- Nature: documentation.
- Initial risk: the dirty diff contained direct `rm -rf` instructions for rebuilding Layer 2 and Layer 3 source Markdown.
- Action taken during this review: replaced raw deletion instructions with guarded non-destructive refresh wording and clean-worktree/disposable-worktree cautions.
- Remaining risk: documentation still describes a pipeline command that can mutate derived outputs when an operator runs it.
- Recommendation: safe to commit only if delegated reviewer accepts the guarded wording.

## B. `scripts/pipeline_cli.py`

- Nature: code change in `run_kg_pipeline`.
- New behavior: calls `Neo4jClient.check_connectivity()` and classifies auth failure, missing driver, and unreachable server before the Neo4j load phase.
- Does not add a new command, a new default mutation path, or a new destructive default.
- Existing destructive flags such as `--reset --force-reset`, `--all`, and Neo4j operations remain pre-existing and explicitly gated.
- Risk: medium/high because `run_kg_pipeline` can load Neo4j when configured and explicitly run.
- Focused validation: `scripts/tests/test_kg_pipeline_force_path.py` passes after the seven-file test correction.

## C. `scripts/tests/test_canonicalize_body.py`

- Nature: tests only.
- Tests assert full source text is retained in canonical source cards and batch canonicalization prefers refined Markdown when present.
- Uses only temporary directories and monkeypatches.
- Risk: low.

## D. `scripts/tests/test_kg_pipeline_force_path.py`

- Nature: tests only.
- Adds auth-failure classification coverage and pipeline error-report coverage with temporary directories and fake clients.
- Also updates one existing assertion to be platform-correct on Windows.
- No production files are written by the tests.
- Risk: low/medium because the target test is slow and exercises pipeline orchestration via monkeypatches.

## E. `scripts/vitruvius/canonicalize.py`

- Nature: canonicalization output behavior.
- New behavior:
  - generated source cards include a final `## Source Text` section with the full refined text;
  - batch canonicalize starts from raw paths but uses a matching refined path when it exists.
- Determinism: output is deterministic except for the pre-existing `last_canonicalized_utc` frontmatter timestamp.
- Canonical ID behavior: no ID formula change; no merge/alias/redirect/tombstone logic added.
- Mutation behavior: writes only when an operator runs canonicalize and `canonical_diff.should_overwrite()` allows it.
- GitNexus impact: `build_structured_source_file` reported CRITICAL impact because it feeds source admission and aggregate/laws pipeline flows.
- Recommendation: safe to commit only with explicit delegated reviewer pass and validation evidence.

## F. `scripts/vitruvius/kg/neo4j_client.py`

- Nature: Neo4j connectivity wrapper.
- New behavior: `check_connectivity()` returns a structured status; `verify_connectivity()` remains a boolean compatibility wrapper.
- No credentials, endpoints, or write defaults were introduced.
- No destructive methods were changed. Existing reset methods remain pre-existing development helpers.
- Risk: medium because it wraps external graph connectivity, but the change improves fail-closed error handling.

## G. `scripts/vitruvius/rules/slug_alias_registry.yaml`

- Nature: one canonical slug collision mapping.
- Added mapping:
  - `004-technology/building construction illustrated, 5th edition`
  - `source-building-construction-illustrated-5th-edition-a394d0`
- Local evidence only:
  - raw files exist under `001_Raw-Source-Layer/004-Technology/`;
  - refined/raw conversion files exist under `002_Raw-Conversion-Layer/004-Technology/`;
  - canonical source card exists under `003_Canonical-Knowledge-Layer/shared/sources/`.
- No external verification was performed or claimed.
- No P0 Concrete/Reinforced Concrete aliasing was introduced.
- Risk: medium/high because slug rules affect future source canonicalization stability.

## Impact Analysis

- `run_kg_pipeline`: MEDIUM, 38 impacted items, direct callers include CLI `main` and pipeline tests.
- `build_structured_source_file`: CRITICAL, 10 impacted items, affected processes include source admission, laws readiness, aggregate lanes, and dataset source-to-graph.
- `run_canonicalize`: LOW, 0 upstream impacts reported.
- `Neo4jClient`: LOW, 3 import-level impacts reported.
- `verify_connectivity`: ambiguous symbol name; GitNexus reported multiple candidates, so the class-level `Neo4jClient` impact and focused tests were used.

## Safety Verdict Before Delegated Review

Codex local review recommends `PASS_COMMIT_SAFE_FILES` only if the delegated reviewer agrees. The seven-file set is coherent and tested, but the canonicalization change remains high-impact and must not be treated as approval for Phase 7 implementation, production graph work, or Resource Layer mutation.
