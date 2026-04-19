# Dataset MVP automation

## Goal
Run a completed trusted dataset family into the knowledge graph through a single reusable operator path.

## Generic operator wrapper
Use:

```bash
./run-dataset-mvp-graph --profile <profile-yaml> [review args]
```

This wrapper delegates to:

```bash
python3 scripts/pipeline_cli.py run-completed-aggregate-from-profile --profile <profile-yaml>
```

## Ready-family aggregate wrapper
Run all families currently marked `ready` with:

```bash
./run-ready-families-mvp-graph [review args]
```

This delegates to the catalog-driven aggregate path for every ready family.

Current execute evidence for the ready-family aggregate:
- aggregate manifest: `53 law units / 70 sources / 97 concepts / 132 relationships / 46 raw anchors`
- latest graph snapshot: **136 nodes / 265 edges**

You can also run by registered family alias:

```bash
./run-dataset-mvp-graph --family <family-name> [review args]
```

Which delegates to:

```bash
python3 scripts/pipeline_cli.py run-completed-aggregate-family --family <family-name>
```

The family registry currently lives at:

- `config/datasets/dataset-mvp-profile-catalog.yaml`

## Registering a new dataset family
Use:

```bash
python3 scripts/pipeline_cli.py register-completed-aggregate-family \
  --family <family-name> \
  --profile <profile-yaml> \
  --dataset-id <dataset-id> \
  --dataset-kind <dataset-kind> \
  --completed-ledger <completed-ledger.yaml> \
  --manifest-index <manifest-index.yaml> \
  --out-manifest <runtime-or-config-manifest.yaml> \
  --graph-output-root <graph-root> \
  --run-output-root <run-root> \
  --query-snapshot-template <template>
```

This writes:
- the family profile YAML
- the family catalog entry

After registration, the family can run through:

```bash
./run-dataset-mvp-graph --family <family-name> [review args]
```

## One-command starter lane bootstrap
To drive the starter-lane bootstrap in one command, use:

```bash
python3 scripts/pipeline_cli.py bootstrap-completed-aggregate-family-lane \
  --family <family-name> \
  --lane-id <lane-id> \
  --raw-root <repo-relative-raw-root> \
  --source-type <source-type> \
  --trust-level <trust-level> \
  --core-concept <concept> \
  --predicate covers
```

If the raw root contains multiple mixed-quality candidates, you can force a specific file with:

```bash
  --raw-path <repo-relative-raw-file>
```

This orchestrates:
- family scaffold if missing
- lane scaffold
- source inspection
- source prep
- canonical rule scaffold
- source admission execute
- concept scaffold
- relationship scaffold
- relationship promotion
- family manifest admission
- family readiness check

## Admitting completed manifests into a family
Once a family has real completed manifests, add them to the family ledger/index with:

```bash
python3 scripts/pipeline_cli.py admit-completed-aggregate-manifest \
  --family <family-name> \
  --lane-id <lane-id> \
  --manifest <manifest-yaml>
```

This updates the family’s:
- completed-lanes ledger
- manifest index

so the family aggregate build/run path can discover the newly admitted lane.

## Checking family readiness
Before trying to run a newly scaffolded or partially onboarded family, check blockers with:

```bash
python3 scripts/pipeline_cli.py check-completed-aggregate-family \
  --family <family-name>
```

This reports:
- completed lane count
- resolved manifest count
- aggregate manifest counts
- `ready_to_run`
- structured blockers if the family is not yet runnable

## Scaffolding a brand-new dataset family
If a family does not yet have:
- completed-lanes ledger
- manifest index
- profile
- catalog entry

bootstrap all of them with:

```bash
python3 scripts/pipeline_cli.py scaffold-completed-aggregate-family \
  --family <family-name> \
  --dataset-kind <dataset-kind>
```

This creates starter artifacts for:
- `config/datasets/<family>-completed-lanes.yaml`
- `config/datasets/<family>-manifest-index.yaml`
- `config/datasets/<family>-mvp-profile.yaml`
- catalog registration in `config/datasets/dataset-mvp-profile-catalog.yaml`

The scaffolded family is intentionally empty until completed lanes and manifest entries are admitted.

## Scaffolding a starter lane manifest from raw inventory
To bootstrap the first manifest for a scaffolded family from a raw-root inventory:

```bash
python3 scripts/pipeline_cli.py scaffold-completed-aggregate-lane-manifest \
  --family <family-name> \
  --lane-id <lane-id> \
  --raw-root <repo-relative-raw-root> \
  --max-files 5 \
  --extension .pdf
```

If you need to force a specific file instead of taking the first matching inventory entry, add:

```bash
  --raw-path <repo-relative-raw-file>
```

To rank candidates inside a mixed-quality family root before picking one, use:

```bash
python3 scripts/pipeline_cli.py suggest-completed-aggregate-family-candidates \
  --raw-root <repo-relative-raw-root> \
  --max-candidates 5 \
  --extension .pdf
```

This writes a starter manifest that contains:
- raw slice anchors
- starter classified raw entries
- starter law-unit placeholders

It does **not** claim canonical sources or relationships yet. Those still need truthful admission before the family can become runnable.

## Inspecting starter lane source readiness
To inspect the raw-file readiness of a scaffolded starter lane:

```bash
python3 scripts/pipeline_cli.py inspect-completed-aggregate-lane-sources \
  --manifest <lane-manifest-yaml>
```

This reports:
- raw file count
- supported direct-input count
- PDF detection results
- OCR-required count
- refined-markdown ready count

Use this to understand whether the next step is:
- direct source preparation
- OCR-first handling
- or further manifest narrowing

## Preparing starter lane sources
To generate conversion/refinement outputs for a scaffolded lane:

```bash
python3 scripts/pipeline_cli.py prepare-completed-aggregate-lane-sources \
  --manifest <lane-manifest-yaml> \
  --dry-run
```

And, when ready to actually prepare files:

```bash
python3 scripts/pipeline_cli.py prepare-completed-aggregate-lane-sources \
  --manifest <lane-manifest-yaml> \
  --allow-ocr
```

This writes a source-prep report under the lane run root and makes the next canonical-admission step much more mechanical.

## Dry-running source admission for a starter lane
To see whether prepared starter-lane outputs are actually ready for canonical source admission:

```bash
python3 scripts/pipeline_cli.py source-admit-completed-aggregate-lane-dry-run \
  --manifest <lane-manifest-yaml>
```

This reports:
- admission `status`
- candidate source page count
- excluded prepared files
- blocked/failed file reports
- guardrails and next-step guidance

This is the final pre-admission diagnostic surface before truthful canonical source admission work.

## Executing canonical source admission for a starter lane
When a starter lane is ready to attempt canonical source admission:

```bash
python3 scripts/pipeline_cli.py source-admit-completed-aggregate-lane \
  --manifest <lane-manifest-yaml>
```

This writes:
- canonical source pages for admitted candidates
- a source-admission report under the lane run root
- manifest updates for:
  - `canonical_input_manifest.sources`
  - admitted source paths on matching law units

If admission still reports `status = not_ready`, that is truthful: the lane still needs canonical rules or further source curation before real admission can happen.

## Scaffolding canonical rules for a starter lane
If a starter lane is blocked because it lacks matching canonical rules, scaffold rule entries with:

```bash
python3 scripts/pipeline_cli.py scaffold-completed-aggregate-lane-canonical-rules \
  --manifest <lane-manifest-yaml> \
  --source-type handout \
  --trust-level secondary
```

By default this writes to:

- `config/datasets/canonical_rules.generated.yaml`

And `build_plan()` will merge that generated overlay with the base canonical rules file automatically.

This is a bootstrap surface only:
- it gives the lane a truthful classification/type/trust starting point
- it does **not** replace source review or relationship admission

## Promoting generated canonical rules into the durable rules file
Once a generated starter rule has been reviewed, promote it with:

```bash
python3 scripts/pipeline_cli.py promote-generated-canonical-rules \
  --rule-name "<exact generated rule name>"
```

This moves the selected rule from:
- `config/datasets/canonical_rules.generated.yaml`

into:
- `scripts/vitruvius/rules/canonical_rules.yaml`

and removes it from the generated overlay.

## Scaffolding starter concepts from generated lane rules
If your generated starter rules include `core_concepts`, scaffold concept files with:

```bash
python3 scripts/pipeline_cli.py scaffold-completed-aggregate-lane-concepts \
  --manifest <lane-manifest-yaml>
```

This writes draft concept pages under:

- `003_Canonical-Knowledge-Layer/shared/concepts/`

These are bootstrap concept stubs only. They help the next relationship-input layer, but they are not a substitute for reviewed concept enrichment.

## Scaffolding starter relationship inputs
Once starter sources and concepts exist, scaffold draft relationship inputs with:

```bash
python3 scripts/pipeline_cli.py scaffold-completed-aggregate-lane-relationships \
  --manifest <lane-manifest-yaml> \
  --predicate covers
```

This writes draft relationship pages under:

- `003_Canonical-Knowledge-Layer/shared/relationships/`

and updates the lane manifest:
- `relationship_input_manifest.relationships`
- `law_units[*].admitted_relationship_paths`

For non-laws starter lanes, `covers` is the intended bootstrap predicate for source→concept coverage. These are still draft bootstrap relationships, not reviewed promoted truth.

## Profile contract
A profile YAML must define:
- `dataset_id`
- `dataset_kind`
- `completed_ledger`
- `manifest_index`
- `out_manifest`
- `graph_output_root`
- `run_output_root`
- `query_snapshot_template`

Optional:
- `scope_notes`
- `lane_note_template`

## Example: laws MVP
The laws wave now uses:

```bash
./run-laws-mvp-graph --review-preset m2-8gb-safe
```

Which delegates to the generic path with:
- `config/datasets/laws-mvp-profile.yaml`

Equivalent direct command:

```bash
./run-dataset-mvp-graph \
  --family laws \
  --review-preset m2-8gb-safe
```

Or explicitly by profile:

```bash
./run-dataset-mvp-graph \
  --profile config/datasets/laws-mvp-profile.yaml \
  --review-preset m2-8gb-safe
```

## Current registered families
- `laws`
  - completed authoritative laws-wave MVP graph
- `history`
  - first non-laws MVP proof family
  - current proof lane:
    - `history-20th-century-architects-2`
  - current graph evidence:
    - `2 nodes / 1 edge`
- `theory`
  - second non-laws MVP proof family
  - current proof lane:
    - `theory-toa-1-intro`
  - current graph evidence:
    - `2 nodes / 1 edge`
- `utilities`
  - third non-laws MVP proof family
  - current proof lane:
    - `utilities-arc-building-terms`
  - current graph evidence:
    - `2 nodes / 1 edge`
- `structural`
  - fourth non-laws MVP proof family
  - current proof lane:
    - `structural-detailing-reinforcement`
  - current graph evidence:
    - `2 nodes / 1 edge`
- `technology`
  - fifth non-laws MVP proof family
  - current proof lane:
    - `technology-architectural-cost-estimates`
  - current graph evidence:
    - `2 nodes / 1 edge`
  - current caveat:
    - review-heavy / shallow source quality remains explicit

## Integrity boundary
This operator path is for the completed trusted subset of a dataset family.
It should not silently mix in:
- drafts
- bills
- empty folders
- non-authoritative supporting guides

Those should remain explicitly dispositioned outside the trusted aggregate until a future policy admits them as a separate graph tier.
