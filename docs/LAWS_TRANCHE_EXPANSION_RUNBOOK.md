# Laws Tranche Expansion Runbook

## Purpose

This runbook defines the next safe operator path after the successful
4-law bounded pilot and the repo-wide readiness dry-run. The governing rule is
simple: **expand by explicit tranche manifests, not by generic all-laws
execution**.

## Current safe baseline

### 1) Reproduce the bounded pilot safely

```bash
./run-laws-pilot --dry-run
```

This stays inside the existing `laws-core-bundle-m1` boundary.

### 2) Reproduce whole-repo readiness without widening execution

```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run \
  --review-preset m2-8gb-safe
```

This is still a planning/readiness lane. It inventories coverage and keeps
generic Phase 11 expansion gated.

## Tranche-1 rules

Tranche-1 should be introduced as a new manifest-backed sibling under
`config/datasets/`, not as a directory sweep or a blanket “all laws” mode.

Required properties:

1. **Explicit membership only**
   - Each admitted law unit must be named explicitly.
   - Each raw anchor, source, concept, and relationship input must remain
     manifest-backed.
2. **Phase 11 stays gated**
   - A tranche command must not imply generic all-laws execute readiness.
   - Dry-run must remain the first step for any new tranche.
3. **8GB-first defaults stay intact**
   - `m2-8gb-safe` remains the recommended review preset for tranche planning.
   - Any widened slice must preserve low-parallelism, low-memory expectations.
4. **Additive and reversible changes only**
   - `laws-core-bundle-m1.yaml` remains the known-good baseline.
   - Tranche manifests should be additive siblings rather than silent edits that
     erase the proven M1 boundary.

## Tranche-1 dry-run expectations

A tranche dry-run should behave like a bounded preflight, not an execution
shortcut.

Minimum expectations:

- resolve the tranche manifest explicitly
- report the selected law units
- surface review preset / model / parallelism before work begins
- refuse to imply generic Phase 11 widening
- avoid review, promotion, graph writes, or browser actions unless explicitly
  entering the execute lane later

## BP220-style shallowness guardrail

The current graph contract is still concept-centric, not section-hierarchy-
centric. That means a law can look structurally rich while still being too
shallow in admitted concept coverage.

The tranche dry-run / guardrail report should surface this kind of mismatch
automatically. At minimum, a report should make these questions answerable:

- Does the law show many section/header structures but very few law-native
  concepts?
- Are most edges routed into shared generic concepts instead of law-specific
  concepts?
- Is the law “present” only because source pages exist, while concept admission
  is still thin?

For BP220-style cases, prefer report-first language such as:

- structural richness detected
- concept admission still shallow
- keep tranche execute gated pending additional law-native concept work

Do **not** treat section-header extraction alone as proof of graph readiness.

## Code review notes to preserve during implementation

### Keep command names consistent everywhere

Current repo evidence shows a naming mismatch:

- `scripts/pipeline_cli.py` and its CLI tests use `run-laws-all-dry-run`
- some operator-facing documentation strings still say `run-all-laws-dry-run`

When tranche support is added, keep the parser, operator docs, tests, and
experience/help text on one canonical command id. Avoid repeating the existing
split-brain naming.

### Reuse the existing manifest contract

`config/datasets/laws-core-bundle-m1.yaml` already demonstrates the safety
pattern to preserve:

- explicit `law_units`
- explicit raw anchors
- explicit admitted source / concept / relationship paths
- bounded graph and run output roots

Tranche manifests should extend that contract instead of inventing a second
shape.

## Operator acceptance checklist

Before tranche-1 execute is considered safe:

- [ ] tranche-1 manifest exists and is explicit
- [ ] tranche-1 dry-run works end-to-end
- [ ] Phase 11 generic expansion is still reported as gated
- [ ] `m2-8gb-safe` remains a valid planning preset
- [ ] BP220-style structure-vs-concept shallowness is surfaced in automated output
- [ ] no generic all-laws execute path was introduced by accident

## Related artifacts

- `.ai/02_audits/2026-04-17_laws-tranche-expansion-audit.md`
- `.ai/03_plans/2026-04-17_laws-tranche-expansion-plan.md`
- `docs/LAWS_POST_TRANCHE2_MANIFEST_STRATEGY.md`
- `.omx/context/laws-tranche-implementation-20260417T012217Z.md`
