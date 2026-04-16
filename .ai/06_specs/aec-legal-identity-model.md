# AEC Legal Identity Model

## Layers
### Work
Semantic family anchor. Example: `work-ph-aec-building-pd-1096`

### Instrument
Concrete legal/regulatory instrument under a work. Example: `instrument-ph-aec-building-pd-1096-irr`

### Source
Actual admitted evidence artifact.

## Required fields
- `work_id`
- `instrument_id`
- `instrument_kind`
- `authority_role`
- `domain`
- `jurisdiction`
- `discipline`
- `title`
- `revision_label` (optional)
- `effective_date` (optional)
- `supersedes_instrument_id` (optional)
- `implements_work_id` (optional)

## Design rule
Do not collapse law and IRR into one node. Preserve distinct instruments and connect them under one work.
