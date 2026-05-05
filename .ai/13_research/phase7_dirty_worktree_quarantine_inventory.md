# Phase 7 Dirty Worktree Quarantine Inventory

**Date:** 2026-05-06
**Inventory point:** before Phase 7 delegated-review report writes
**Verdict:** QUARANTINED_WITH_REVIEW_GATE

## Raw Git Counts

- Dirty entries: 818.
- Modified tracked entries: 320.
- Deleted tracked entries: 37.
- Untracked entries: 461.
- `git diff --name-only`: 357 tracked diff paths.
- `git ls-files --others --exclude-standard`: 461 untracked paths.

## Category Counts

| Category | Count | Safe to leave unstaged | Safe to delete automatically | Requires reviewer | Blocks autopilot |
|---|---:|---|---|---|---|
| `unrelated_canonical_source_file` | 439 | yes | no | sample/audit before admission | no, if unstaged |
| `generated_conversion_or_source_markdown_artifact` | 371 | yes | no | sample/audit before admission | no, if unstaged |
| `safe_local_artifact` | 1 | yes | no automatic deletion | no | no |
| `needs_reviewer_review` | 7 | yes | no | yes | blocks Phase 7 implementation until owner/reviewer disposition |
| `unsafe_executable_script` | 0 | n/a | n/a | n/a | no |
| `production_resource_layer_registry` | 0 | n/a | n/a | n/a | no |
| `graph_canonical_registry` | 0 | n/a | n/a | n/a | no |
| `scoped_phase7_file` | 0 | n/a | n/a | n/a | no at inventory point |
| `unknown` | 0 | n/a | n/a | n/a | no |

## Representative Paths

### `unrelated_canonical_source_file`

- `003_Canonical-Knowledge-Layer/shared/relationships/rel-concept-means-of-egress-requires-concept-stairs.md`
- `003_Canonical-Knowledge-Layer/shared/relationships/rel-concept-stairs-requires-concept-fire-resistive-construction.md`
- `003_Canonical-Knowledge-Layer/shared/relationships/rel-concept-stairs-requires-concept-means-of-egress.md`
- `003_Canonical-Knowledge-Layer/shared/relationships/rel-handout-statement-that-architectural-and-architectural-interior-design-are-exclusive-to-architecture-practice-governs-concept-standards-of-professional-practice.md`
- `003_Canonical-Knowledge-Layer/shared/relationships/rel-source-no-17-098b-governs-concept-floor-area.md`

Disposition: leave unstaged. These are source/relationship artifacts and must not be admitted, deleted, or staged by this Phase 7 entry-gate task.

### `generated_conversion_or_source_markdown_artifact`

- `003_Canonical-Knowledge-Layer/shared/sources/02-basic-theory.md`
- `003_Canonical-Knowledge-Layer/shared/sources/1-0-development-framework-2015-2025.md`
- `003_Canonical-Knowledge-Layer/shared/sources/1-general.md`
- `003_Canonical-Knowledge-Layer/shared/sources/1-if-fi-wi-w.md`
- `006_System-Manifests/registries/latest_conversion_registry.csv`
- `006_System-Manifests/registries/latest_raw_file_registry.csv`

Disposition: leave unstaged. Do not delete source markdowns or generated source/conversion inventory artifacts in this task.

### `safe_local_artifact`

- `nul`

Disposition: leave unstaged. It is not executable and is not a production registry, but no automated deletion was performed.

### `needs_reviewer_review`

- `README.md`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_canonicalize_body.py`
- `scripts/tests/test_kg_pipeline_force_path.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/kg/neo4j_client.py`
- `scripts/vitruvius/rules/slug_alias_registry.yaml`

Disposition: leave unstaged. These files need project-owner or separately authorized code/content review before any future autopilot stages them or treats them as accepted.

## Registry Safety Checks

- Dirty files under `006_System-Manifests/resource-layer/`: 0.
- Dirty files under `006_System-Manifests/graph-canonical/`: 0.
- Dirty files under API/Explorer implementation paths from this task: 0.
- Production Resource Layer mutation detected: no.
- Graph-canonical registry mutation detected: no.

## Executable Script Check

No untracked executable script paths were found. Dirty tracked Python files are classified as `needs_reviewer_review`, not as delegated-review approval or execution authorization.

## Directory Counts

- `003_Canonical-Knowledge-Layer/shared/relationships`: 439.
- `003_Canonical-Knowledge-Layer/shared/sources`: 369.
- `006_System-Manifests/registries`: 2.
- `scripts/tests`: 2.
- repo root: 2.
- `scripts/vitruvius/kg`: 1.
- `scripts/vitruvius/rules`: 1.
- `scripts`: 1.
- `scripts/vitruvius`: 1.

## File-Type Counts

- `.md`: 809.
- `.py`: 5.
- `.csv`: 2.
- `.yaml`: 1.
- no extension: 1.

## Quarantine Recommendation

Keep the 818 dirty entries unstaged. Phase 7 planning may proceed only if the delegated reviewer agrees that the quarantine classification is acceptable. Phase 7 implementation remains blocked until the seven `needs_reviewer_review` files receive explicit project-owner or separately authorized implementation disposition.
