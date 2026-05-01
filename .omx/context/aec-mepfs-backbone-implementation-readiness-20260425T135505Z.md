# Ralph Context Snapshot

Task statement:

- Make the AEC-MEPFS Backbone ready and primed for implementation by closing
  every remaining readiness item that can be closed safely: steward/source
  admission evidence, legal/currentness evidence, rollback rehearsal evidence,
  canonical source admission packet, and runtime impact packet for high-risk KG
  roots.

Desired outcome:

- Produce a readiness packet that is as close as possible to implementation
  approval without falsely claiming human/legal authority.
- Use official-source internet research, Gemini/Kimi review where available,
  local validation, and safe rollback rehearsal tooling.
- Keep Neo4j live graph and MVP Explorer/API runtime untouched unless a safe
  isolated rehearsal can be performed.

Known facts/evidence:

- Current `HEAD` is `3031a956`.
- `origin/main` matched `HEAD` at start of this Ralph turn.
- `AEC-BB-S1` through `AEC-BB-S6` are implemented, validated, committed, and
  pushed.
- S6 produced predicate and source-rights candidate rows, but they are not
  steward-admitted, legally cleared, or runtime-consumed.
- The scorecard still blocks runtime implementation on legal/licensing review,
  currentness review, stopped/isolated Neo4j dump/load proof, steward-admitted
  runtime registries, canonical source admission, and HIGH/CRITICAL runtime
  impact roots.
- Existing unrelated dirty file: `explorer/package.json`; do not stage or
  modify it.

Constraints:

- AI may prepare evidence, candidate decisions, review packets, and technical
  plans. AI may not impersonate a human steward or legal/licensing reviewer.
- Do not ingest protected standards text, legal clauses, tables, figures, or
  datasets.
- Do not edit runtime KG roots (`CanonicalNode`, `TaxonomyLoader`,
  `UnifiedSnapshotBuilder`, `Neo4jLoader`) unless a separate runtime packet and
  impact proof are in place.
- Do not mutate Neo4j, reset/rebuild the graph, or flip feature flags.
- If rollback proof is attempted, use a stopped or isolated database path that
  does not touch the live MVP graph.

Unknowns/open questions:

- Whether local Neo4j installation permits creating/stopping an isolated test
  database without production graph impact.
- Whether Kimi CLI is installed and what command name it uses.
- Which source rows have official pages that currently resolve and which require
  admission-time human currentness review.

Likely codebase touchpoints:

- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- `006_System-Manifests/aec-mepfs-backbone/`
- S6 registry candidate files
- GitNexus impact map and future runtime implementation packet
