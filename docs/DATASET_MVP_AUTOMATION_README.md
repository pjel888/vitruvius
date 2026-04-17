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
