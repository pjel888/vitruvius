# Audit — AEC Legal Family Classification

## Verdict
Proceed with a bounded architecture slice.

## Why
This is a real semantic-identity gap, not a naming preference. The repo already has manifest-level grouping (`law_units`), but the graph contract still lacks explicit work/instrument/source identity semantics. As the corpus grows across AEC subjects, this will create semantic duplication, brittle heuristics, and UI/query ambiguity.

## Current verified gap
- manifest layer can group laws in a bounded pilot
- graph layer still models only `source` / `concept` / `attribute` / `spatial_instance`
- law vs IRR vs amendment semantics are implicit, not modeled
- `source_identity.py` still relies on fallback heuristics that are too weak for enterprise-grade scale

## Recommended architecture decision
Adopt one shared AEC legal-identity model with three distinct levels:
1. **Work** — semantic family (`PD-1096`, `RA-9514`, etc.)
2. **Instrument** — law / IRR / amendment / order / standard
3. **Source** — admitted file/artifact evidence

## Why this is safer than per-subject middleware
- keeps semantic identity in data, not code branches
- scales across building / fire / accessibility / electrical / plumbing / history
- preserves legal truth while avoiding duplicate semantic anchors

## Boundaries
### In scope next
- spec and registry design
- canonical metadata extension
- bounded graph contract extension

### Out of scope now
- broad all-corpus migration
- UI-only grouping hacks
- raw conversion identity inference
