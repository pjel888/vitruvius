# KG-first cleanup Phase 2+ context snapshot

- Task: Continue KG-first cleanup phases after Phase 1 docs reconciliation without waiting for further user approval.
- Desired outcome: Complete every safe in-scope next phase: Phase 2 CLI/operator wording, Phase 3 source-ingestion adapter clarification, Phase 4 active/archive plan surface cleanup, and Phase 5 deletion review only if strict proof gates are fully satisfied.
- Known facts: Phase 1 committed and pushed at 8fce5807. Git status clean/synced. GitNexus up-to-date at 8fce580. User requested continuous autonomous execution with $ultrawork $ralph $team.
- Constraints: no raw-source writes, no numbered layer renames, no generated-artifact deletion, no validation/provenance/source-rights evidence deletion, no KG rebuild/reload/reset, no Neo4j mutation, no protected payload ingest/exposure, no API/Explorer behavior changes, no deletion unless all deletion proof gates are met. Phase 2 code-facing edits require exact GitNexus impact and tests-first.
- Unknowns/open questions: whether CLI help tests already cover exact operator wording; whether Phase 3 can stay docstring/comment-only; whether Phase 4 live plan surface has remaining stale contradictions.
- Likely touchpoints: scripts/pipeline_cli.py, scripts/tests/test_dataset_pipeline_cli.py, scripts/tests/test_cli_operator_experience.py, scripts/vitruvius/conversion.py, scripts/vitruvius/normalization/refine.py, scripts/vitruvius/canonicalize.py, scripts/vitruvius/source_identity.py, scripts/vitruvius/dataset_pipeline.py, .ai/03_plans/kg-first-cleanup/*.
- Team feasibility: tmux, omx, claude, kimi are available. If team launches, force Claude workers to avoid Spark-backed Codex defaults.
