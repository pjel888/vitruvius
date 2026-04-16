# Research Pack — AEC Legal Family Classification

## Core conclusion
This should be solved as a shared identity/classification layer, not ad hoc middleware per subject.

## Canonical model
- family = semantic anchor, e.g. `pd-1096`
- instrument = legal artifact, e.g. `pd-1096-law`, `pd-1096-irr`
- source = admitted document evidence

## Minimum fields
- `domain`
- `jurisdiction`
- `family_id`
- `instrument_kind`
- `instrument_id`
- `revision_label`
- `effective_date`
- `implements_family_id`
- `supersedes_instrument_id`

## Pipeline placement
This belongs in canonical admission / semantic identity, not raw conversion.
Graph build should consume normalized identity, not invent it.
