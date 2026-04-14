# Spatial Source Layer Schema (v1.0.0)

**Status:** frozen — any change requires a version bump plus a migration plan.

**Authoritative validator:** `scripts/vitruvius/spatial/schema.py` —
see `SPATIAL_SCHEMA_VERSION` and `SPATIAL_JSON_SCHEMA`. Runtime validation
uses `jsonschema.Draft7Validator` so this document and the Python module
must stay in sync.

## Version

`schema_version` MUST equal `"1.0.0"`. The validator rejects any other
value. A later schema revision (e.g., bounding box rotations, IfcGUID
cross-references) will ship as `1.1.0` under a new migration plan.

## Purpose

JSON manifests that land in `001B_Spatial-Source-Layer/` carry geometric
metadata produced by an external spatial daemon (Stream N, future). Each
manifest describes one physical model: a set of tagged instances (doors,
walls, corridors) plus a set of spatial edges between them (clearance,
intersection, containment). The ingestion walker validates every file on
load and emits `SpatialCandidate` records downstream for constraint
evaluation.

## JSON Schema (Draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://vitruvius.local/schemas/spatial-contract-v1.json",
  "title": "Vitruvius Spatial Contract",
  "type": "object",
  "required": [
    "schema_version",
    "spatial_context_id",
    "generated_at_utc",
    "instances",
    "spatial_edges"
  ],
  "properties": {
    "schema_version": {"type": "string", "enum": ["1.0.0"]},
    "spatial_context_id": {
      "type": "string",
      "pattern": "^spatial-[a-z0-9][a-z0-9-]*$"
    },
    "generated_at_utc": {"type": "string"},
    "source_daemon": {"type": "string"},
    "instances": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["instance_id", "canonical_concept_id"],
        "properties": {
          "instance_id": {
            "type": "string",
            "pattern": "^instance-[a-z0-9][a-z0-9-]*$"
          },
          "canonical_concept_id": {
            "type": "string",
            "pattern": "^concept-[a-z0-9][a-z0-9-]*$"
          },
          "bounding_box": {
            "type": "object",
            "required": ["min", "max"],
            "properties": {
              "min": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
              "max": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3}
            }
          }
        }
      }
    },
    "spatial_edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_instance", "predicate", "target_instance"],
        "properties": {
          "source_instance": {"type": "string", "pattern": "^instance-"},
          "predicate": {
            "type": "string",
            "enum": [
              "spatial_intersects",
              "spatial_clearance",
              "spatial_adjacent_to",
              "spatial_contains"
            ]
          },
          "target_instance": {"type": "string", "pattern": "^instance-"},
          "value": {"type": "number"},
          "unit": {"type": "string", "enum": ["meters", "millimeters", "feet", "inches"]}
        }
      }
    }
  }
}
```

## Predicate semantics

| Predicate | Meaning | Numeric `value` present? |
|---|---|---|
| `spatial_intersects` | source and target bounding boxes overlap | NO (boolean membership) |
| `spatial_clearance` | free distance between source surface and target surface | YES (meters after unit conversion) |
| `spatial_adjacent_to` | source and target share a face within 1mm tolerance | OPTIONAL (clearance when numeric) |
| `spatial_contains` | source completely encloses target | NO |

## Compatibility

- Adding an OPTIONAL field → minor bump (1.1.0); old validators keep working.
- Adding an ENUM value (predicate or unit) → minor bump; old validators fail closed on the new value.
- Removing a required field OR tightening a pattern → major bump with a migration plan.
- Renaming a field → major bump.

## Sample

A hand-authored fixture lives at
`scripts/tests/fixtures/spatial/sample_residential_01_spatial.json` and
exercises every required field plus optional bounding boxes. The
`sample_residential_01_expected_candidates.json` sibling is produced by
Task L.8 and locks the walker's output.
