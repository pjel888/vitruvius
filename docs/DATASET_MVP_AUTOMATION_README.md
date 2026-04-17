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

## Integrity boundary
This operator path is for the completed trusted subset of a dataset family.
It should not silently mix in:
- drafts
- bills
- empty folders
- non-authoritative supporting guides

Those should remain explicitly dispositioned outside the trusted aggregate until a future policy admits them as a separate graph tier.
