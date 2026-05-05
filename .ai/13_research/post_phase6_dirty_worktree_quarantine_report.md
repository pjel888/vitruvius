# Post-Phase-6 Dirty Worktree Quarantine Report

**Date:** 2026-05-06
**Verification commit:** `45b906d8e39a552f6a4d182e1450bbee90674403`
**Verdict:** QUARANTINED_UNRELATED_WORKTREE

## Summary

The worktree contains 818 dirty entries. They were not staged, deleted, rewritten, or otherwise modified by this task.

| Status class | Count |
|---|---:|
| Modified tracked files | 320 |
| Deleted tracked files | 37 |
| Untracked files | 461 |
| Total dirty entries | 818 |

## Classification

| Category | Count | Handling |
|---|---:|---|
| Phase 6 scoped files | 0 | None dirty; safe for Phase 6 acceptance |
| Unrelated canonical source files | 348 | Quarantine; requires separate canonical/source review |
| Generated conversion or source markdown artifacts | 462 | Quarantine; review in a dedicated source/canonical artifact task |
| Generated test artifacts | 0 | No action |
| Unsafe untracked executable scripts | 0 | No future-autopilot blocker from untracked executables |
| Safe-to-ignore local artifacts | 1 | `nul`; leave untouched unless explicit cleanup is authorized |
| Needs human review | 7 | Do not stage without separate review |

## Count By Directory

| Directory | Count |
|---|---:|
| `003_Canonical-Knowledge-Layer/shared/relationships` | 439 |
| `003_Canonical-Knowledge-Layer/shared/sources` | 369 |
| `scripts/tests` | 2 |
| repo root | 2 |
| `006_System-Manifests/registries` | 2 |
| `scripts` | 1 |
| `scripts/vitruvius` | 1 |
| `scripts/vitruvius/kg` | 1 |
| `scripts/vitruvius/rules` | 1 |

## Count By File Type

| File type | Count |
|---|---:|
| `.md` | 809 |
| `.py` | 5 |
| `.csv` | 2 |
| `.yaml` | 1 |
| no extension | 1 |

## Registry Safety

| Area | Dirty count |
|---|---:|
| `006_System-Manifests/resource-layer/*` | 0 |
| `006_System-Manifests/graph-canonical/*` | 0 |
| Phase 6 Resource/Evidence scoped files | 0 |

## Needs Human Review

These non-canonical tracked changes are outside the Phase 6 closure scope:

- `README.md`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_canonicalize_body.py`
- `scripts/tests/test_kg_pipeline_force_path.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/kg/neo4j_client.py`
- `scripts/vitruvius/rules/slug_alias_registry.yaml`

## Recommended Handling

1. Do not stage any of the 818 quarantined entries during Resource/Evidence closure or Phase 7 planning commits.
2. Review tracked `003_Canonical-Knowledge-Layer` changes in a separate canonical/source artifact task with explicit authority.
3. Treat untracked canonical markdown relationship/source files as generated candidates until sampled, reviewed, and either admitted through the proper workflow or explicitly cleaned.
4. Review `006_System-Manifests/registries/latest_conversion_registry.csv` and `latest_raw_file_registry.csv` only in a source conversion/registry task.
5. Leave `nul` untouched in this task; it is safe to ignore but cleanup should be explicit.
6. Require human review before any future autopilot that would touch the seven non-canonical tracked files.

## Future Autopilot Blockers

No untracked executable scripts capable of mutation were found. The broader dirty worktree remains a quarantine condition for future tasks that could accidentally stage unrelated canonical/source artifacts.
