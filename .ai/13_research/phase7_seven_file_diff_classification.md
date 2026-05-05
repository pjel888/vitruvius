# Phase 7 Seven-File Diff Classification

**Date:** 2026-05-06
**Scope:** Seven dirty files only. Other dirty worktree entries remain quarantined and unstaged.

## Diff Summary

`git diff --stat -- <seven files>`:

- 7 files changed.
- 344 insertions.
- 28 deletions.
- No whitespace errors from `git diff --check`.

## File Classifications

| Path | Status | Classification | Diff summary | Affected subsystem | Mutation/admission/promotion touch | Resource Layer touch | Graph/canonical registry touch | Risk | Recommended action |
|---|---:|---|---|---|---|---|---|---|---|
| `README.md` | modified | intentional_documentation_change, safe_to_commit after safety edit | Documents canonical source cards containing full source text, refined Markdown corpus indexing, and a guarded non-destructive refresh command. The raw `rm -rf` rebuild wording was removed during this review. | Operator docs | Mentions pipeline refresh only; no runtime change | No | No | Low/medium because operator docs can influence destructive behavior | Commit if delegated reviewer accepts revised safety wording |
| `scripts/pipeline_cli.py` | modified | intentional_code_change, risky_mutation_capable_change, safe_to_commit if tests/reviewer pass | Adds structured Neo4j connectivity error handling in `run_kg_pipeline`, distinguishing auth failure, missing driver, and unreachable server; writes an error phase/report before returning. | Pipeline CLI / KG v2 compatibility path | Touches pipeline load phase and error reporting; does not make writes default or add new mutation path | No | No | Medium/high because CLI can load Neo4j when explicitly configured | Commit only with tests and delegated reviewer pass |
| `scripts/tests/test_canonicalize_body.py` | modified | intentional_test_change, safe_to_commit | Adds tests for `## Source Text` inclusion and refined Markdown preference; narrows an existing assertion to the Coverage section. | Canonicalization tests | Tests only | No | No | Low | Commit with corresponding canonicalize change |
| `scripts/tests/test_kg_pipeline_force_path.py` | modified | intentional_test_change, safe_to_commit | Adds Neo4j auth-failure tests for client/CLI; fixes one existing Windows path separator assertion inside this authorized file. | Pipeline CLI tests | Tests only; uses temp dirs and monkeypatches | No | No | Low/medium due slow test and Neo4j mock path | Commit with corresponding pipeline/Neo4j change |
| `scripts/vitruvius/canonicalize.py` | modified | intentional_code_change, risky_mutation_capable_change, safe_to_commit if tests/reviewer pass | Adds a `## Source Text` section containing full refined source text to generated canonical source cards; makes batch canonicalize prefer `refined_markdown` when paired raw/refined files exist. | Canonicalization / source evidence cards | Touches canonical source generation; no graph edge admission and no registry mutation by itself unless operator runs canonicalize | No | No registry file edited by this task | Critical impact per GitNexus because source admission flows call this function | Commit only with targeted tests and delegated reviewer pass |
| `scripts/vitruvius/kg/neo4j_client.py` | modified | intentional_code_change, safe_to_commit if tests/reviewer pass | Adds `Neo4jConnectivityStatus`, classifies auth/missing-driver/unreachable errors, preserves boolean `verify_connectivity()`. | Neo4j client | Does not change write methods or default connection credentials; improves error classification | No | No | Medium due external graph connectivity wrapper | Commit with CLI tests and reviewer pass |
| `scripts/vitruvius/rules/slug_alias_registry.yaml` | modified | intentional_code_change/data_rule_change, safe_to_commit if reviewer pass | Adds one collision mapping for local `Building Construction Illustrated, 5th edition` source slug to existing canonical source id. Local raw/conversion/canonical evidence exists; no external verification was performed. | Slug/canonical ID collision registry | Affects future canonical ID stability for that local source only | No | No | Medium/high semantic risk because slug rules affect canonical IDs | Commit only with reviewer acceptance |

## Dirty Worktree Category Snapshot

Initial dirty entries remained 818:

- `unrelated_canonical_source_file`: 439
- `generated_conversion_or_source_markdown_artifact`: 371
- `needs_reviewer_review`: 7
- `safe_local_artifact`: 1 (`nul`)
- `unsafe_executable_script`: 0
- `production_resource_layer_registry`: 0
- `graph_canonical_registry`: 0
- `unknown`: 0 after classifying `006_System-Manifests/registries/latest_*_registry.csv` as generated conversion registry artifacts.

## Safety Notes

- No dirty production Resource Layer registry entries were present.
- No dirty graph-canonical registry entries were present.
- No untracked executable scripts were found.
- No external source, DOI, ISBN, URL, or PDF verification was performed.
