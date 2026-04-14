# 001B — Spatial Source Layer

> **Purpose:** Landing zone for JSON manifests produced by the decoupled
> spatial daemon (`spatial-daemon/`). Files here conform to the contract
> in `.ai/06_specs/spatial-schema.md` v1.0.0.
>
> **Pipeline stage:** 1D. Consumed by `scripts/vitruvius/spatial/walker.py`
> only when `features.l_spatial_ingestion` is true.
>
> **Non-breaking guarantee:** With the flag off, this directory is ignored.
