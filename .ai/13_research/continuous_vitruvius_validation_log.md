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

---

## Resource Layer standards-context cleanup validation run

Last updated: 2026-05-02T02:58:00Z

### Commands run

- `bun test api/resourceLayer.test.ts` - passed, 19 tests.
- `cd api && bun test` - passed, 163 tests.
- `cd explorer && bun test` - passed, 112 tests.
- `cd explorer && bun run build` - passed with known Vite chunk-size warning.
- `bun run api/validateResourceLayer.ts` - passed with 5 honest standards-context warnings, 0 blockers, 0 errors.
- `bun run api/validateGraphRelationships.ts` - passed, 10,018 nodes / 13,670 edges / 0 issues.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed; P0 unresolved 2, approvals 0, admitted relationships 0, manifest afterHash matches 3/3.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - passed, 104 tests.

### Validation interpretation

The standards-context workflow makes ASCE 7 and ACI 318 warnings reviewable without treating missing context as success. Needs-review/rejected records remain warning/review items. Accepted or promoted standard/code links missing edition/version, citation/scope, or jurisdiction/geographic scope become blockers.

### Code intelligence refresh after standards-context implementation

- `bash ./scripts/refresh_code_intelligence.sh` - completed after implementation. GitNexus was already up to date; ChunkHound processed 39 files with 0 file errors; code-review-graph completed full build. Known caveats remain: missing `tree-sitter-yaml` warnings and embedding/provider errors from code-review-graph/OpenAI embedding batches.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` - completed; reported critical risk (31 staged files, 112 symbols, 25 affected processes). This is expected for a Resource Layer API/service/UI/test/report workflow change and is mitigated by targeted Resource Layer tests, full API tests, full Explorer tests/build, graph validation, Resource Layer validation, and canonical validation. Unrelated AEC dirty files remain unstaged.
- `chunkhound search --regex "standardContext|context-preview|standards-context"` - completed; confirmed changed/report concepts are indexed. Initial `--limit` variant was unsupported and returned usage error.

---

## P1 packet ontology review validation run

Last updated: 2026-05-02T04:12:51Z

### Commands run

- `bun test api/canonicalGraphStewardship.test.ts` - passed, 28 tests.
- `cd api && bun test` - passed, 166 tests.
- `cd explorer && bun test src/components/canonical-review/CanonicalReviewAdmin.test.tsx src/api/graphApi.test.ts` - initially failed on duplicate `valid` text assertion; test was corrected to use `getAllByText`.
- `cd explorer && bun test` - passed, 112 tests.
- `cd explorer && bun run build` - passed with known Vite chunk-size warning.
- `bun run api/validateGraphRelationships.ts` - passed, 10,018 nodes / 13,670 edges / 0 issues.
- `bun run api/validateResourceLayer.ts` - passed with 5 honest standards-context warnings and 0 blockers/errors.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed non-strict; 20 P1 packets unreviewed as warning only.
- `VITRUVIUS_REQUIRE_P1_PACKET_REVIEWS=true bun run api/validateCanonicalGraphStewardship.ts` - failed as expected with 20 strict review blockers.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - passed, 104 tests.

### Validation interpretation

P1 review metadata is advisory only and stored separately from immutable packet custody hashes. Unreviewed P1 packets remain backlog warnings outside strict mode; strict mode correctly blocks unreviewed coverage.

### Code intelligence refresh after P1 review implementation

- `bash ./scripts/refresh_code_intelligence.sh` - completed after implementation. GitNexus already up to date; ChunkHound processed 28 files with 0 file errors; code-review-graph completed full build with known `tree-sitter-yaml` warnings and embedding/provider context-length errors. These are known tooling warnings and not caused by the P1 review workflow.

### Change-scope checks after staging

- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` - completed; reported high risk for 25 staged files / 87 symbols / 7 affected processes because canonical stewardship service/API/UI/test surfaces changed. This was expected for this bounded feature and mitigated by full API tests, full Explorer tests/build, canonical/graph/resource validations, strict-mode smoke validation, Kimi review, and no graph mutation.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo .` - completed; reported 45 changed files, 0 affected flows, 0 test gaps, risk score 0.00.
- `chunkhound search --regex "p1PacketReview|ontologyReviewStatus|p1-packet-reviews"` - completed; confirmed P1 review concepts indexed in code/report artifacts.


---

## Top P1 packet ontology review validation run

Last updated: 2026-05-02T05:01:34Z

### Commands run

- `bun run api/validateCanonicalGraphStewardship.ts` - passed; 20 P1 packets, 8 reviewed, 12 unreviewed warnings, 3 `kimi_reviewed` status records, 5 `human_review_needed` status records, 13 P1 review transaction manifests, 0 stale/invalid review records, latest afterHash matches 4/4.
- `bun run api/validateGraphRelationships.ts` - passed, 10,018 nodes / 13,670 edges / 0 issues.
- `bun run api/validateResourceLayer.ts` - passed, 7 resources / 9 nodeResourceLinks / 0 blockers; ASCE 7 and ACI 318 context warnings remain honest.
- `cd api && bun test` - passed, 166 tests.
- `cd explorer && bun test` - passed, 112 tests.
- `cd explorer && bun run build` - passed with known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - passed, 104 tests.

### Validation interpretation

P1 review updates are review-registry metadata only. They reduce the unreviewed P1 packet backlog from 20 to 12 without changing packet custody hashes, production graph nodes/edges, Resource Layer links/resources, approvals, admitted relationships, aliases, redirects, or tombstones. The five high-risk Kimi-reviewed packets are intentionally marked `human_review_needed` rather than `human_reviewed`.


### Post-implementation code-intelligence/change-scope checks (2026-05-02T05:03:16Z)

- `bash ./scripts/refresh_code_intelligence.sh` - completed after review/report/data changes. GitNexus already up to date; ChunkHound processed 28 changed files with 0 file errors; code-review-graph completed full build with known missing `tree-sitter-yaml` warnings and known embedding-provider context-length errors.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` - completed; reported no indexed symbol/process changes because this task stages review registry, manifests, and reports rather than code.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo .` - completed; 46 changed files, 0 changed functions/classes, 0 affected flows, 0 test gaps, risk score 0.00.
- `chunkhound search --regex "first_graph_admission_queue|p1_packet_ontology_review_run_report|kimi-advisory-2026-05-02"` - completed and found the new review-session artifacts.


## 2026-05-02T05:31:17Z - Medium-risk P1 steward packet validation

Commands run:

- `bun test api/mediumRiskP1StewardPacket.test.ts` - passed, 4 tests.
- `bun test api/canonicalGraphStewardship.test.ts api/mediumRiskP1StewardPacket.test.ts` - passed, 32 tests.
- `cd api && bun test` - passed, 170 tests.
- `cd explorer && bun test` - passed, 112 tests.
- `cd explorer && bun run build` - passed with known Vite chunk-size warning.
- `bun run api/validateCanonicalGraphStewardship.ts` - passed; P1 packets 20, reviewed 8, unreviewed 12, approvals 0, admitted relationships 0, aliases/redirects/tombstones 0/0/0, latest afterHash mismatches 0.
- `bun run api/validateGraphRelationships.ts` - passed; nodes 10,018, edges 13,670, issues 0.
- `bun run api/validateResourceLayer.ts` - passed with known honest standards-context warnings; resources 7, nodeResourceLinks 9, blockers 0.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` - passed, 104 tests.
- `bash ./scripts/refresh_code_intelligence.sh` - exit 0 with known tree-sitter-yaml warnings and embedding-provider context-length/task elapsed errors during code-review-graph embedding update.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` - exit 0 but high risk because unrelated pre-existing AEC files remain dirty; staged-scope check is run before commit.

Validation conclusion: medium-risk steward packet and admission preview are advisory-only and non-mutating. No graph/resource/canonical mutation registry counts changed.

- `2026-05-02T05:31:55Z` staged GitNexus detect-changes: `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged` returned `No changes detected`; generated docs/tests are outside symbol-flow tracking and unrelated AEC dirty files remain unstaged.


## 2026-05-02T06:03:16Z - Steward-approved first graph admissions

- Recorded scoped project-owner steward approval records for Deep Foundations, Shallow Foundations, and Buildings.
- Admitted 4 active reciprocal `CROSS_DOMAIN_ALIGNMENT` stewardship overlay edges for Deep and Shallow Foundations.
- Recorded Buildings metadata-only `DISAMBIGUATED_KEEP_SEPARATE`; no visible `DISAMBIGUATED_FROM` edge was admitted.
- No merge, alias, redirect, tombstone, node rewrite, Resource Layer mutation, fake source, protected payload, or standard context mutation occurred.
- Effective API/validation graph edge count is now 13674 = base 13670 + admitted overlay 4.
- Known caveat: P1 packet source snapshots are stale relative to the new canonical/admitted state; refresh/rebase is the next exact action.



## 2026-05-02T06:05:37Z - Final validation update

- `cd api && bun test` passed: 172 tests. Initial expected-edge-count failures were fixed by updating admitted-overlay graph count contracts from 13,670 to 13,674 where API render output includes active admitted stewardship overlays.
- `cd explorer && bun test` passed: 112 tests.
- `cd explorer && bun run build` passed with known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` passed: 104 tests.
- `bun run api/validateCanonicalGraphStewardship.ts` passed with blockers 0; warnings note unsigned/stale P1 packet snapshots after admission.
- `bun run api/validateGraphRelationships.ts` passed with 10,018 nodes and 13,674 effective edges.
- `bun run api/validateResourceLayer.ts` passed with known ASCE 7 / ACI 318 context warnings.

## Post-Kimi implementation-safety repair (2026-05-02T06:20:00Z)

Kimi's final implementation-safety review was accepted. Before commit, the run repaired two custody issues:

- Approval records for Deep Foundations, Shallow Foundations, and Buildings now contain revalidated embedded snapshots with `ok: true` and no embedded false blocker snapshots.
- Buildings remains a metadata-only `DISAMBIGUATED_KEEP_SEPARATE` / governed-disambiguation decision; latent `CROSS_DOMAIN_ALIGNMENT` relationship proposals were cleared and no Buildings graph edge was admitted.
- A new `canonical_approval_metadata_revalidation` transaction manifest (`canonical-tx-20260502061917-f0d21c4f7013`) records the approval/decision metadata repair.
- Current canonical validation: blockers 0; approvals 3; admitted relationships 4; transaction manifests 30; latest afterHash mismatches 0.

Accepted Kimi suggestions: repair failed embedded validation snapshots; remove latent Buildings edge proposals; isolate commit scope. Rejected: none. Deferred: P1 packet custody snapshot refresh after admitted canonical state.

## Final validation pass (2026-05-02T06:22:30Z)

- `bun run api/validateCanonicalGraphStewardship.ts` ? passed; blockers 0; approvals 3; admittedRelationships 4; transactionManifests 30; latestAfterHashMismatches 0.
- `bun run api/validateGraphRelationships.ts` ? passed; 10,018 nodes; 13,670 base edges; 13,674 effective edges; issueCount 0.
- `bun run api/validateResourceLayer.ts` ? passed with known ASCE 7 / ACI 318 standards-context warnings; blockers 0.
- `cd api && bun test` ? passed; 172 tests.
- `cd explorer && bun test` ? passed; 112 tests.
- `cd explorer && bun run build` ? passed with known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` ? passed; 104 tests.

## Change-scope checks

- Post-implementation code-intelligence refresh completed. Known warnings remain: missing `tree-sitter-yaml` in code-review-graph and ChunkHound/code-review-graph embedding provider context-length errors; wrapper completed and GitNexus was up to date.
- GitNexus detect-changes on full worktree initially reported critical risk because unrelated unstaged AEC run-persistence files are present.
- GitNexus detect-changes on the staged admission scope reported medium risk: 39 files, 36 symbols, 5 affected processes.
- `git diff --cached --check` passed after removing trailing blank lines.


## 2026-05-02T07:20:07Z - P1 packet snapshot rebase validation

- `bun test api/mediumRiskP1StewardPacket.test.ts`: passed, 4 tests.
- Targeted Explorer tests for canonical review/API/search integration: passed, 18 tests.
- `cd api && bun test`: passed, 173 tests.
- `cd explorer && bun test`: passed, 112 tests.
- `cd explorer && bun run build`: passed with known Vite chunk-size warning.
- `bun run api/validateCanonicalGraphStewardship.ts`: passed; stale P1 snapshots 0, carried-forward reviews 8, latest afterHash mismatches 0.
- Strict packet-signature smoke without HMAC key: failed as expected with 20 blockers.
- Strict latest-afterHash validation: passed.
- `bun run api/validateGraphRelationships.ts`: passed; 10,018 nodes, 13,674 effective edges.
- `bun run api/validateResourceLayer.ts`: passed with known ASCE 7 / ACI 318 context warnings.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: passed, 108 tests.
- Direct selected-node neighborhood checks passed for Deep/Shallow reciprocal `CROSS_DOMAIN_ALIGNMENT`; Explorer graph payload exposes 4 `CROSS_DOMAIN_ALIGNMENT` edges.


## 2026-05-02T07:21:32Z - Code intelligence refresh

- `bash ./scripts/refresh_code_intelligence.sh`: completed with exit 0.
- GitNexus: already up to date.
- ChunkHound: completed processing, but known embedding/provider context-length errors and `_Task.elapsed` batch errors were emitted while the wrapper exited 0.
- code-review-graph: rebuilt graph, with known `tree-sitter-yaml` parser warnings for YAML files.


## 2026-05-02T07:23:22Z - Change-impact checks

- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius --scope staged`: completed; 31 staged files, 66 symbols, 3 affected flows, medium risk.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo . --brief`: completed; analyzed 54 changed files including unrelated dirty AEC worktree artifacts, reported 0 changed functions/classes, 0 affected flows, 0 test gaps, risk 0.00.
- Staged scope was manually checked to exclude unrelated AEC files/artifacts.
