---
task: weird-zoom-interaction-taxonomy-fixes
validated: 2026-04-30
status: PASS
---

# Validation Report: Weird Zoom, Interaction, Taxonomy, and Classification Fixes

## Scope validated
- Explorer graph interaction fixes:
  - Pan/select mode switches preserve selected node state.
  - Pan mode uses hand/grab cursor behavior.
  - Clicking or dragging outside the selected visible-edge neighborhood clears selection before allowing a different node interaction.
  - Zoom extent focuses the selected node when present and otherwise fits the full graph.
  - Child orbit/spread changes are reversible from tight back to loose by using a stable baseline.
  - Node inspector renders clickable taxonomy breadcrumbs.
- Taxonomy expansion:
  - AEC-MEPFS `/expand` supports bounded multi-depth child subtree expansion.
  - Explorer context menu requests directed `HAS_CHILD` descendants rather than only immediate neighbors.
- AEC-MEPFS enrichment:
  - Canonical architects and architect-engineer people are organized by metadata-only nationality facets.
  - Laws and standards are organized by metadata-only jurisdiction/scope and standards-family facets for international, country, local, AIA, RIBA, and IBS/NIBS groupings.
  - Architect/engineer bridge-role relationships are strengthened without introducing protected source payloads.

## Artifacts
- Research: `.ai/13_research/weird-zoom-interaction-taxonomy-fixes-research.md`
- Audit: `.ai/02_audits/weird-zoom-interaction-taxonomy-fixes-audit.md`
- Plan: `.ai/03_plans/weird-zoom-interaction-taxonomy-fixes-plan.md`
- PRD: `.omx/plans/prd-weird-zoom-interaction-taxonomy-fixes.md`
- Test spec: `.omx/plans/test-spec-weird-zoom-interaction-taxonomy-fixes.md`
- Enrichment report: `006_System-Manifests/aec-mepfs-backbone/architecture-interconnectivity/20260430T070000Z/architecture-interconnectivity-enrichment-report.json`
- Shadow staging report: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T070501Z/shadow-staging-report.json`
- Shadow staging consumer report: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T070501Z/shadow-staging-consumer-report.json`

## Verification commands

```bash
bun test api/v2Backbone.test.ts api/v2Resolver.test.ts
```
Result: PASS, 85 tests passed, 0 failed. Re-run after final API neighbor-payload tightening also passed.

```bash
PYTHONPATH=scripts python -m pytest \
  scripts/tests/test_kg_architecture_interconnectivity_enrichment.py \
  scripts/tests/test_kg_backbone_contracts.py \
  scripts/tests/test_kg_backbone_resolver_qa.py
```
Result: PASS, 76 tests passed, 0 failed.

```bash
cd explorer && bun test src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts
```
Result: PASS, 57 tests passed, 0 failed. Re-run after final drag-guard tightening also passed.

```bash
cd explorer && bun run build
```
Result: PASS. Re-run after final drag-guard tightening also passed. Vite emitted the existing large chunk warning for `vis-network`, not a task regression.

```bash
cd explorer && bun run lint
```
Result: PASS, exit code 0. Re-run after final drag-guard tightening also passed.

```bash
git diff --check
```
Result: PASS, no whitespace errors.

```bash
npx gitnexus status
```
Result: PASS, repository index was up to date at commit `76d83ef`.

```bash
npx gitnexus detect-changes -r vitruvius
```
Result: ATTEMPTED. GitNexus `detect-changes:file-symbols` prepare timed out repeatedly after 30000ms and was stopped; fallback scope review used targeted impact checks, `git status --short`, `git diff --name-only`, `git diff --stat`, and `git diff --check`.

## Generated data validation
- Architecture interconnectivity enrichment wrote 32 additional nodes and 119 relationships.
- Final staged graph count: 9761 nodes and 12495 relationships.
- Source-rights registry count: 102.
- Report safety fields confirmed no protected payload material, no raw-source writes, and no Neo4j/runtime cutover.

## Architect verification follow-up
- A read-only architect verifier found no blockers.
- Follow-up mitigations applied:
  - `/expand` now keeps the legacy `neighbors` payload scoped to nodes adjacent to the requested root while returning deeper subtree nodes/edges separately.
  - Outside-neighborhood drags now restore the original position immediately, temporarily disable node dragging for that frame, clear selection, and then restore normal select-mode dragging.
- Remaining accepted caveat: selected-neighborhood edge emphasis includes visible edges whose endpoints are both in the selected direct neighborhood; this preserves current visual semantics and was not changed in this pass.

## Known caveats
- Browser-level manual visual verification was not run in this pass; behavior is covered through targeted component/API/Python/build/lint checks and code review.
- GitNexus detect-changes timed out on the large unstaged/generated diff; targeted GitNexus impact checks and git diff scope checks were used as fallback evidence.
- The repository had pre-existing unrelated dirty files before this task; this validation covers the files and generated artifacts listed above.

## Fresh Ralph hook verification: 2026-04-30T07:20:30Z
Hook requested continued Ralph verification before stopping. Fresh evidence was gathered after the final API and drag-guard mitigations:

```bash
bun test api/v2Backbone.test.ts api/v2Resolver.test.ts
```
Result: PASS, 85 tests passed, 0 failed.

```bash
PYTHONPATH=scripts python -m pytest \
  scripts/tests/test_kg_architecture_interconnectivity_enrichment.py \
  scripts/tests/test_kg_backbone_contracts.py \
  scripts/tests/test_kg_backbone_resolver_qa.py
```
Result: PASS, 76 tests passed, 0 failed.

```bash
cd explorer && bun test src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts
```
Result: PASS, 57 tests passed, 0 failed.

```bash
cd explorer && bun run build
```
Result: PASS; existing Vite large-chunk warning for `vis-network` remains nonblocking.

```bash
cd explorer && bun run lint
```
Result: PASS, exit code 0.

```bash
git diff --check
```
Result: PASS, no whitespace errors.

Architect verification state: prior architect review found no blockers. The final follow-up changes only mitigated its nonblocking API-neighbor and outside-drag caveats; a fresh architect subagent was requested but did not return before timeout and was shut down. Local Ralph review accepted the narrow mitigations because the fresh API, Python, Explorer, build, lint, and diff checks all passed.
