# AEC-MEPFS taxonomy deep population context snapshot

## Task statement
Project owner requested a heavily populated, detailed, expansive AEC-MEPFS knowledge graph taxonomy across all taxonomies, not only Architecture. Sources may include online research, local raw-source references under `001_Raw-Source-Layer`, and Kimi advisory review if available. Use multiple agents/team execution.

## Desired outcome
Add many rights-safe metadata taxonomy nodes/subnodes/concepts/rules across every taxonomy branch, including world architecture history eras, Philippine building laws, and all AEC/MEPFS domains. Preserve file-backed Explorer/API behavior and do not ingest protected source payloads.

## Known facts/evidence
- Current branch is `main` and should remain synced with `origin/main` after verified work.
- Current AEC-MEPFS taxonomy run is file-backed and already expanded for Architecture, Sanitary, Security, Smart Systems, Heritage, and Laws.
- Production Neo4j mutation, KG rebuild/reload/reset, and protected payload ingestion remain blocked unless separately authorized and legally supported.
- User explicitly wants deeper taxonomy population and accepts large metadata-only expansion.

## Constraints
- Windows-safe generated filenames and path segments.
- Rights-safe metadata taxonomy only: no protected text/tables/figures/source-payload ingestion.
- Use repo patterns and verification artifacts.
- Use Kimi where available; no Gemini requirement.
- Use team/multiple agents for independent research lanes.

## Unknowns/open questions
- Exact generator and fixture files that define the current AEC-MEPFS taxonomy.
- Current validation commands for taxonomy expansion.
- Kimi command availability and credentials.
- Local raw-source inventory relevant to AEC-MEPFS.

## Likely touchpoints
- `scripts/vitruvius/kg/`
- `scripts/tests/`
- `006_System-Manifests/aec-mepfs-backbone/`
- `.ai/13_research/`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- `api/` and `explorer/` only if generated artifact contracts require updates.
