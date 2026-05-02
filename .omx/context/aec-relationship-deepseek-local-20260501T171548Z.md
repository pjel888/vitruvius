# Ralph Context Snapshot: AEC Relationship DeepSeek Local Council

## Task Statement
Revise the pending-only AEC relationship-improvement workflow to use a Local + DeepSeek council and remove Kimi from default/adaptive relationship-discovery routing.

## Desired Outcome
- Add `deepseek_local` council mode.
- Route adaptive/cloud discovery through DeepSeek Flash, DeepSeek Pro, and local Ollama only.
- Keep local Ollama embeddings and sequential local calls.
- Preserve pending-only artifacts and strict `--apply` rejection.
- Add deterministic hierarchy and taxonomy guards before accepting proposed relationships.
- Fix verifier parsing so `VerificationDecision` is not validated as `RelationshipDecision`.
- Improve provider metadata and generation methods.
- Add DeepSeek preflight and safer DeepSeek call-cap defaults.
- Keep progress/watch UX compatible and remove Kimi from default displays/routing.

## Known Facts / Evidence
- Target module: `scripts/vitruvius/kg/aec_relationship_improvement.py`.
- CLI command: `scripts/pipeline_cli.py aec-improve-relationships`.
- Tests: `scripts/tests/test_kg_aec_relationship_improvement.py`.
- Existing workflow is pending-only and writes semantic-overlay artifacts.
- Existing target fixture has about 10,018 nodes and 13,670 existing relationships.
- Previous adaptive-cloud test showed DeepSeek worked, Kimi failed with 403, and local fallback worked.
- Project roadmap/state says production Neo4j/live graph promotion and protected payload admission remain blocked.

## Constraints
- Do not mutate active graph files or the AEC fixture.
- Do not write to Neo4j/Postgres.
- Do not use internet search, browsing, external URL fetching, or model tools.
- Do not run local Ollama calls in parallel.
- Do not expose API keys or reasoning content.
- Do not weaken `--apply` rejection.
- Do not emit blocked predicates.
- Cloud calls still require `--allow-cloud-ai`.

## Unknowns / Open Questions
- Exact current shape of provider routing and verifier merge logic needs local code inspection.
- GitNexus CLI impact command syntax differs from documented `--target` form; fallback impact evidence may need CLI help or detect-changes.
- `docs/shared/agent-tiers.md` is missing, so tier guidance cannot be read.

## Likely Codebase Touchpoints
- `COUNCIL_MODES`, provider choices, `RunConfig`, `config_from_args`, CLI argument registration.
- `CloudUsage`, `ProviderHealth`, `Checkpoint`, `RunSummary`.
- `RelationshipCouncil` routing and provider call methods.
- Prompt builders and parse/validation helpers.
- Acceptance/write path: `_maybe_accept_or_record`, `decision_to_edge_record`, candidate/rejection writers.
- Progress/watch tables.
- Unit tests in `scripts/tests/test_kg_aec_relationship_improvement.py`.
