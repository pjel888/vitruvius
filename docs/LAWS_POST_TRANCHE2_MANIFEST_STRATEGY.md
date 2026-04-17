# Post–Tranche-2 Laws Manifest Strategy

## Purpose

This note proposes the safest **next manifest strategy after tranche-2** without
opening a generic `all-laws execute` path.

The governing rule stays the same:

> expand by explicit tranche manifests, not by directory sweeps or generic
> all-laws execution

## What current repo evidence says

### 1) Broad readiness is still uneven

The latest repo-wide readiness report at:

- `006_System-Manifests/runs/datasets/laws-all-readiness/20260417T055021Z/all_laws_dry_run_report.json`

still shows:

- 47 law folders inventoried
- 4 `pilot-covered`
- 2 `inventory-only`
- 41 `not-ready`

That means the corpus is still far from safe for one-shot widening.

### 2) Tranche-local evidence is newer than the whole-repo readiness report

The repo-wide readiness snapshot above predates newer tranche-local work:

- tranche-1 source admission success:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/20260417T065958Z/laws_tranche_source_admission_report.json`
- tranche-1 dry-run success:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/source_to_graph_dry_run/20260417T070003Z/laws_tranche_source_to_graph_dry_run_report.json`
- tranche-1 execute success:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/source_to_graph_execute/20260417T073704Z/laws_tranche_source_to_graph_execute_report.json`

So post–tranche-2 planning should trust **both** views:

1. repo-wide readiness for coarse inventory coverage
2. tranche-local reports for the freshest admission/execute truth

### 3) The next safe expansion unit is still a bounded cohort

Current evidence supports continuing with **small, theme-linked manifest waves**
rather than widening to an omnibus legal corpus slice.

## Recommended strategy after tranche-2

### 1. Freeze the baseline, grow by sibling manifests

Keep:

- `config/datasets/laws-core-bundle-m1.yaml` as the proven baseline
- `config/datasets/laws-tranche-1.yaml` as the first explicit widening slice
- `config/datasets/laws-tranche-2.yaml` as the next accepted slice once lane
  selection finishes

Then continue with additive siblings only:

- `config/datasets/laws-tranche-3.yaml`
- `config/datasets/laws-tranche-4.yaml`
- etc.

Do **not** repurpose one manifest into a moving target and do **not** add a
generic catch-all manifest that silently becomes “everything ready enough.”

### 2. Pick tranche-3+ from readiness cohorts, not folder order

After tranche-2, the next queue should be chosen from one of three manifest
cohorts:

### Cohort A — execute-adjacent laws

Use first.

Definition:

- already source-admitted or tranche-admitted
- bounded duplicate picture is known
- concept-fit work is plausible without inventing new corpus-wide rules

This is the safest cohort for tranche-3 because it extends a proven operating
pattern instead of opening a new readiness frontier.

### Cohort B — inventory-rich but not yet admitted laws

Use second.

Definition:

- raw source exists
- refined markdown or strong structural inventory already exists
- still needs explicit source admission before tranche execute

Current repo evidence shows this cohort should remain bounded and review-first.
It should not be executed directly from all-laws readiness alone.

### Cohort C — raw-only backlog laws

Use last.

Definition:

- raw source exists
- no refined markdown inventory yet
- no admitted source/concept evidence yet

These laws should stay outside tranche execute manifests until source prep and
source admission have produced better evidence.

### 3. Use a two-step manifest lane for every new tranche

For tranche-3 and beyond, keep the same lane every time:

1. **selection + duplicate screen**
   - identify candidate laws
   - screen duplicate/alias risk
   - record exclusions explicitly
2. **source admission**
   - prepare authoritative variants
   - admit bounded canonical source pages
   - only then permit source-to-graph dry-run
3. **dry-run**
   - require explicit manifest resolution
   - require `phase_11_generic_expansion_gated: true`
   - keep the review preset visible
4. **execute**
   - only after tranche-local blockers are empty

This prevents a future tranche from skipping from “raw files exist” straight to
graph execute.

### 4. Keep tranche size small and theme-linked

Post–tranche-2 manifests should stay intentionally small:

- prefer **2–4 laws per tranche**
- prefer one legal/theme cluster at a time
- prefer laws that already overlap existing shared concepts
- avoid mixing many unrelated agencies in a single tranche just to increase law
  count

That keeps memory, review burden, and duplicate-resolution work bounded on the
same safety model already proven for the pilot and tranche-1.

### 5. Refresh broad readiness only at tranche boundaries

Because the all-laws readiness report can become stale relative to tranche-local
admission work, rerun whole-repo readiness:

- after tranche-2 selection hardens, or
- after tranche-2 source admission / execute changes the repo-local truth

But treat that refresh as **planning evidence**, not permission to open
all-laws execute.

## Recommended post–tranche-2 operating order

1. finish tranche-2 selection and exclusion rationale
2. execute tranche-2 through the existing gated manifest lane
3. refresh whole-repo readiness to capture new tranche-local truth
4. build tranche-3 only from the highest-confidence remaining cohort
5. defer raw-only laws to later source-prep/source-admission waves

## Acceptance rule for future manifests

A post–tranche-2 manifest should be accepted only if it:

- names law units explicitly
- records authoritative raw anchors explicitly
- records admitted source/concept/relationship inputs explicitly
- keeps `phase_11_generic_expansion_gated` true
- has a tranche-local duplicate/quality screen
- does not imply generic all-laws execute readiness

## Non-goals

This strategy does **not** recommend:

- a generic `laws-all-execute` mode
- widening by directory enumeration
- treating raw-source presence as graph-readiness
- merging all remaining laws into one “tranche-3” umbrella

## Bottom line

After tranche-2, the safe strategy is **more sibling tranche manifests chosen
by readiness cohort**, with tranche-local admission/dry-run/execute gates
preserved and whole-repo readiness used only as a planning index.
