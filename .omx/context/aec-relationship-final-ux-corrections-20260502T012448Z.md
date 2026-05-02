# AEC Relationship Final UX Corrections Context

- task: Implement final corrections and UX/output improvements for pending-only AEC relationship-improvement workflow before larger DeepSeek-local run.
- desired_outcome: Keep Stage 1 pending-only safety while improving CLI wiring, effective/local model metadata, validation diagnostics, safe schema repair, DeepSeek prompt adherence, summary/report/TSV outputs, Git Bash progress fallback, watcher output, and next-run recommendations.
- constraints: no active graph mutation; no fixture mutation; no Neo4j/Postgres writes; no web/search/tools; no cloud calls without --allow-cloud-ai; Kimi disabled unless --enable-kimi-experimental; no API key or reasoning_content storage/logging; --apply remains rejected; local Ollama sequential only.
- known_facts: Current workflow lives in scripts/vitruvius/kg/aec_relationship_improvement.py; CLI entry is scripts/pipeline_cli.py aec-improve-relationships; tests live at scripts/tests/test_kg_aec_relationship_improvement.py. Prior run succeeded operationally but needs metadata/report/diagnostic/UX improvements.
- likely_touchpoints: RunConfig, Checkpoint, RunSummary, RelationshipCouncil, parser setup, validation parsing, prompt builders, artifact writers, progress reporter, watcher, tests.
- unknowns: exact current implementation shape after previous untracked local module; test count may shift as new cases are added.
- safety_position: all outputs stay under semantic-overlay run artifacts; no active graph writes.
