---
task: kg-first-cleanup
phase: plan-critique
created: 2026-04-29
author: CODEX
status: COMPLETE
---

# KG-First Cleanup Plan Critique

## Adversarial Findings

### 1. The old six-layer model is still a filesystem contract

Risk: If the cleanup treats the old model as obsolete everywhere, it may weaken
raw-source immutability, source provenance, or generated artifact boundaries.

Mitigation: Preserve numbered layer paths as storage/custody contracts while
changing the product narrative to KG-first.

### 2. `pipeline_cli.py` is too central for early refactor

Risk: GitNexus maps many tests/processes through the CLI; a broad CLI cleanup
could break laws/dataset/graph workflows.

Mitigation: Phase 2 must be help-text/command-grouping only unless exact
function impact is rerun and tests are added first.

### 3. Evidence ingestion may look legacy but is core to the new direction

Risk: Source attachment to graph nodes depends on evidence IDs, spans, and
provenance. Removing ingestion code would move the product backward.

Mitigation: Keep `EvidenceIngestor` and source admission machinery. Rename or
wrap only after tests and impact evidence.

### 4. Documentation cleanup could silently rewrite governance history

Risk: `.ai` contains historical plans and validation logs. Deleting or rewriting
history would destroy auditability.

Mitigation: Use archive pointers and new superseding docs. Do not edit old
validation logs except for explicit correction packets.

### 5. AEC-MEPFS runtime and Explorer work must not be bundled into cleanup

Risk: Combining code cleanup with Explorer/API behavior changes would make
failures hard to diagnose and could regress the current graph UX.

Mitigation: Keep API/Explorer code out of the first cleanup slices unless a bug
is directly caused by documentation/operator cleanup.

### 6. Kimi/team review is useful but not authoritative

Risk: Agent review may miss repo-specific contracts or hallucinate safe deletes.

Mitigation: Treat Kimi as advisory only. GitNexus, tests, and repository state
remain the authority.

## Required Plan Adjustments Before Implementation

- First implementation slice must be docs-only or tests-first.
- Any code cleanup slice must name exact symbols and rerun GitNexus impact.
- Any deletion candidate must have a keep/deprecate/delete proof table.
- Any generated artifact cleanup must use an explicit reset protocol, not manual
  deletion.

## Verdict

The plan is acceptable as a cleanup roadmap **only because it forbids immediate
code deletion** and sequences docs/tests/impact before refactor.
