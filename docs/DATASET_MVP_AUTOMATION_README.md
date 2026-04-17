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
