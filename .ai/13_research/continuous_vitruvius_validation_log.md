# Continuous Vitruvius Validation Log

Last updated: 2026-05-02T01:56:01Z

## Commands run

- `bash ./scripts/refresh_code_intelligence.sh` ? completed before and after edits; known caveats: missing `tree-sitter-yaml` warnings and ChunkHound/code-review-graph embedding/provider errors while returning exit code 0.
- `bun test api/canonicalGraphStewardship.test.ts` ? passed, 23 tests.
- `cd explorer && bun test src/components/canonical-review/CanonicalReviewAdmin.test.tsx` ? passed, 2 tests.
- `cd api && bun test` ? passed, 157 tests.
- `cd explorer && bun test` ? passed, 111 tests.
- `cd explorer && bun run build` ? passed with Vite chunk-size warning.
- `.\.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` ? passed, 93 tests.
- `bun run api/validateGraphRelationships.ts` ? passed, 10,018 nodes / 13,670 edges / 0 issues.
- `bun run api/validateResourceLayer.ts` ? passed with known ASCE 7 and ACI 318 edition/context warnings.
- `bun run api/validateCanonicalGraphStewardship.ts` ? passed non-strict; P1 signed 0, unsigned 20, invalid 0.
- `VITRUVIUS_REQUIRE_PACKET_SIGNATURES=true bun run api/validateCanonicalGraphStewardship.ts` ? failed as expected with 20 strict signature blockers because no HMAC key is configured.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` ? completed after staging the HMAC loop; risk level medium (23 files, 34 symbols, 3 affected processes). Earlier combined worktree detection was critical before separating the AEC relationship-improvement commit.

## Validation interpretation

Unsigned P1 packets are warnings in non-strict mode and blockers in strict mode. A valid HMAC signature would only prove custody payload integrity under the configured key; it would not prove steward approval, ontology truth, source truth, or merge safety.

---

## Latest manifest afterHash validation run

Last updated: 2026-05-02T02:20:03Z

### Commands run

- `git status --short --branch; git rev-parse HEAD; git rev-parse origin/main` - verified `main...origin/main` at `d988f49e` before edits, with only the new Ralph context snapshot untracked.
- `bun run api/validateCanonicalGraphStewardship.ts` - baseline passed before edits.
- `bun test api/canonicalGraphStewardship.test.ts` - passed, 25 tests.
- `cd explorer && bun test src/components/canonical-review/CanonicalReviewAdmin.test.tsx` - passed, 2 tests.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed non-strict; latest afterHash matches 3/3, mismatches 0.
- `VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH=true bun run api/validateCanonicalGraphStewardship.ts` - passed strict afterHash smoke test because all manifest-governed files matched.
- `cd api && bun test` - passed, 159 tests.
- `cd explorer && bun test` - passed, 111 tests.
- `cd explorer && bun run build` - passed with known Vite chunk-size warning.
- `bun run api/validateGraphRelationships.ts` - passed, 10,018 nodes / 13,670 edges / 0 issues.
- `bun run api/validateResourceLayer.ts` - passed with known ASCE 7 and ACI 318 edition/context warnings.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed; transaction manifests 10, with afterHash 10, files under custody 3, matches 3, mismatches 0.
- `pytest scripts/tests/test_kg_aec_relationship_improvement.py` - failed because `pytest` was not on PATH in this shell.
- `.\.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - passed, 93 tests.

### Validation interpretation

Latest afterHash validation now reports current-file byte drift since the latest manifest. It does not prove source truth, ontology truth, approval, or merge safety. Older superseded manifests remain part of hash-chain validation but do not have to match current file bytes.

### Post-stage code intelligence scope

- `bash ./scripts/refresh_code_intelligence.sh` - completed after edits; GitNexus already up to date, ChunkHound processed 21 changed files with 0 file errors, code-review-graph completed with known missing `tree-sitter-yaml` and embedding/provider warnings.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` - completed; risk level medium, 22 files, 43 symbols, 5 affected processes.
