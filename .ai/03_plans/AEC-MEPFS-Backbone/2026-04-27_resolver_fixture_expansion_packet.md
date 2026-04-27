---
task: aec-mepfs-backbone
phase: resolver-fixture-expansion
created: 2026-04-27
author: CODEX
status: PASS
classification: GREEN,YELLOW-2
---

# Resolver Fixture Expansion Packet

## Purpose

Expand the AEC-MEPFS resolver's non-protected golden fixture coverage now that
`2026-04-27_default_off_resolver_runtime_packet.md` is complete. This packet
adds more deterministic file-backed resolver cases without changing the runtime
guard, Neo4j state, KG artifacts, Explorer defaults, feature-flag defaults, or
protected-source posture.

## Authority

- Project-owner standing directive for autonomous AEC-MEPFS completion.
- Completed source/evidence commits:
  - `fa93008b` — guarded default-off resolver runtime source slice
  - `6e91b96a` — generated evidence for guarded default-off resolver
- The current resolver route remains default-off and file-backed.

## Allowed Scope

This packet permits only:

1. Additional non-protected resolver golden cases in
   `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`.
2. Deterministic API/builder tests proving the expanded cases return only
   canonical IDs, source IDs, fallback reasons, and trace-safe rationale.
3. Resolver QA and contract count updates required by the expanded fixture.
4. State/log updates and regenerated resolver/downstream evidence after source
   commit.

## Explicitly Blocked Scope

- Neo4j writes, reloads, resets, backups, restores, or primary graph promotion.
- KG rebuild/reload/reset.
- Protected source text, table, figure, dataset, clause, or local cache ingest.
- Explorer default graph adoption or automatic preview fetches.
- Default-on feature flags or hidden cutover.
- Runtime threshold claims.
- Edits to `CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`.
- New LLM or graph-backed hot resolver behavior.

## Fixture Cases

Add metadata-only resolver cases for:

- `VTN-DOM-0000001` — Architecture backbone domain, source family
  `SRC-ISO-12006-2`, no standards text exposure.
- `VTN-JUR-0000004` — Philippines jurisdiction metadata crosswalk, source family
  `SRC-PH-PSA-PSGC`, no local API cache payload exposure.
- `VTN-OVR-0000003` — Philippines accessibility overlay metadata, source family
  `SRC-PH-DPWH-PD1096`, no code clause/table/figure exposure.

## Tests

Required focused checks:

```bash
git diff --check
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py -q
(cd api && bun test v2Resolver.test.ts)
```

Run downstream safety checks before completion:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py -q
(cd api && bun test v2Backbone.test.ts)
```

## Evidence Artifacts

After source/docs/tests are committed and the source tree is clean, regenerate:

- resolver QA report
- boundary audit
- benchmark report
- evidence manifest

Route inventory may be regenerated too if the source commit changes route hashes
or if the evidence manifest requires a fresh aligned route report.

## Safety Invariants

- Resolver remains default-off unless `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME` is explicitly true.
- Expanded cases expose IDs and metadata only, never protected payloads.
- No Neo4j/KG/protected ingest/default Explorer/default-on/threshold change.
- Existing preview routes remain stable.

## Completion Criteria

- Expanded fixture validates.
- Focused contract, resolver QA, API, and downstream safety tests pass.
- Generated evidence reflects `resolver_golden_cases=7` and `cases_passed=7`.
- Evidence log exists under `.ai/05_logs/`.
- Source and generated evidence commits are pushed to `origin/main`.

## Next Boundary

After this packet, the next safe packet may add parity coverage for the default-off
resolver route or prepare a benchmark harness. Neo4j/live graph, protected source
ingest, Explorer default adoption, default-on flags, and runtime threshold claims
remain separate gated work.
